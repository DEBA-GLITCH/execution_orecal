import os
import subprocess
import shutil
from pathlib import Path


class WorkspaceSecurityError(Exception):
    pass


class WorkspaceManager:

    def __init__(self):
        self.agent_root = Path(os.getcwd()).resolve()
        self.workspace_root = None
        self.original_remote = None

    # ----------------------------------
    # Workspace Setup
    # ----------------------------------

    def set_workspace(self, path: str):
        if not path:
            raise WorkspaceSecurityError("Workspace path cannot be empty.")

        workspace = Path(path).expanduser().resolve()

        if self.agent_root in workspace.parents or workspace == self.agent_root:
            raise WorkspaceSecurityError(
                "Workspace cannot be inside execution_orecal repository."
            )

        self.workspace_root = workspace
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    # ----------------------------------
    # Clone Repo
    # ----------------------------------

    def clone_repo(self, repo_url: str):
        if not self.workspace_root:
            raise WorkspaceSecurityError("Workspace not initialized.")

        if any(self.workspace_root.iterdir()):
            raise WorkspaceSecurityError(
                "Workspace must be empty before cloning."
            )

        try:
            subprocess.check_call(
                ["git", "clone", repo_url, "."],
                cwd=self.workspace_root
            )
        except subprocess.CalledProcessError as e:
            raise WorkspaceSecurityError(f"Git clone failed: {str(e)}")

    # ----------------------------------
    # Branch Safety
    # ----------------------------------

    def create_ai_branch(self, branch_name: str):
        self._run_git(["git", "checkout", "-b", branch_name])

    def get_current_branch(self):
        return self._run_git(["git", "branch", "--show-current"]).strip()

    # ----------------------------------
    # Commit Identity (Repo-Local Only)
    # ----------------------------------

    def set_commit_identity(self, username: str):
        """
        Sets commit identity ONLY inside workspace repo.
        Does NOT touch global git config.
        """
        if not self.workspace_root:
            raise WorkspaceSecurityError("Workspace not initialized.")

        email = f"{username}@users.noreply.github.com"

        self._run_git(["git", "config", "user.name", username])
        self._run_git(["git", "config", "user.email", email])

    # ----------------------------------
    # Safe File Writing
    # ----------------------------------

    def write_file(self, relative_path: str, content: str):
        if not self.workspace_root:
            raise WorkspaceSecurityError("Workspace not initialized.")

        target_path = (self.workspace_root / relative_path).resolve()

        if self.workspace_root not in target_path.parents and target_path != self.workspace_root:
            raise WorkspaceSecurityError("Attempted write outside workspace.")

        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

    # ----------------------------------
    # Diff Preview
    # ----------------------------------

    def get_diff(self):
        return self._run_git(["git", "diff", "--cached"])

    # ----------------------------------
    # Git Operations
    # ----------------------------------

    def git_add_all(self):
        self._run_git(["git", "add", "."])

    def git_commit(self, message: str):
        self._run_git(["git", "commit", "-m", message])

    # ----------------------------------
    # Secure Push (PAT Based)
    # ----------------------------------

    def push_with_pat(self, username: str, token: str, branch: str):

        original_url = self._run_git(
            ["git", "remote", "get-url", "origin"]
        ).strip()

        self.original_remote = original_url

        if not original_url.startswith("https://"):
            raise WorkspaceSecurityError("Repo must use HTTPS for PAT push.")

        auth_url = original_url.replace(
            "https://",
            f"https://{username}:{token}@"
        )

        try:
            self._run_git(["git", "remote", "set-url", "origin", auth_url])
            self._run_git(["git", "push", "origin", branch])
        finally:
            self._run_git(["git", "remote", "set-url", "origin", original_url])

    # ----------------------------------
    # Internal Runner
    # ----------------------------------

    def _run_git(self, command: list):
        if not self.workspace_root:
            raise WorkspaceSecurityError("Workspace not initialized.")

        try:
            result = subprocess.check_output(
                command,
                cwd=self.workspace_root,
                stderr=subprocess.STDOUT
            )
            return result.decode("utf-8")
        except subprocess.CalledProcessError as e:
            raise WorkspaceSecurityError(e.output.decode("utf-8"))

    # ----------------------------------
    # Cleanup
    # ----------------------------------

    def delete_workspace(self):
        if self.workspace_root and self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)
