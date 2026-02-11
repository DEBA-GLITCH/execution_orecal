import subprocess
import os

def get_git_diff():
    """Returns the current unstaged and staged diff of the repository."""
    try:
        # Get staged changes
        staged = subprocess.check_output(["git", "diff", "--cached"], stderr=subprocess.STDOUT).decode("utf-8")
        # Get unstaged changes
        unstaged = subprocess.check_output(["git", "diff"], stderr=subprocess.STDOUT).decode("utf-8")
        return f"--- Staged Changes ---\n{staged}\n\n--- Unstaged Changes ---\n{unstaged}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Not a git repository or git not found."

def get_last_commit_diff():
    """Returns the diff of the last commit."""
    try:
        return subprocess.check_output(["git", "show", "HEAD"], stderr=subprocess.STDOUT).decode("utf-8")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "No commits found or not a git repository."

def get_project_summary():
    """Returns a summary of the project structure (files)."""
    try:
        # List files, ignoring .git and common ignores
        files = subprocess.check_output(["git", "ls-files"], stderr=subprocess.STDOUT).decode("utf-8")
        return f"--- Project Files ---\n{files}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to os.walk if not a git repo
        summary = []
        for root, dirs, filenames in os.walk("."):
            if ".git" in dirs:
                dirs.remove(".git")
            if ".oracle_data" in dirs:
                dirs.remove(".oracle_data")
            for f in filenames:
                summary.append(os.path.join(root, f))
        return "\n".join(summary)

def is_git_repo():
    """Checks if the current directory is inside a git repository."""
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False
