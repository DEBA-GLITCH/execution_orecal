import re
import getpass
from agents.autonomous_planner import AutonomousPlanner
from agents.autonomous_coder import AutonomousCoder
from workspace.workspace_manager import WorkspaceManager, WorkspaceSecurityError
from utils.diff_utils import print_diff
from utils.github import create_issue, create_milestone
from session.session_manager import SessionManager


def ask_input(prompt):
    return input(f"{prompt}: ").strip()


def ask_confirm(prompt):
    return input(f"{prompt} (y/n): ").strip().lower() == "y"


def sanitize_branch(name):
    name = name.lower().replace(" ", "-")
    name = re.sub(r"[^a-z0-9-_]", "", name)
    return name


def main():
    print("\n=== Autonomous Dev Platform  (Resumable) ===\n")

    planner = AutonomousPlanner()
    coder = AutonomousCoder()
    wm = WorkspaceManager()
    session = SessionManager()

    try:
        # -----------------------------------
        # RESUME CHECK
        # -----------------------------------
        if session.exists():
            if ask_confirm("Previous session found. Resume?"):
                state = session.load()
                print("Resuming previous session...\n")
            else:
                session.clear()
                state = None
        else:
            state = None

        # -----------------------------------
        # NEW SESSION INITIALIZATION
        # -----------------------------------
        if not state:

            idea = ask_input("What do you want to build")
            plan = planner.generate_plan(idea)

            print("\nDetected Complexity:", plan["complexity"])
            print("\nProposed File Structure:")
            for f in plan["file_structure"]:
                print(" -", f)

            if not ask_confirm("\nApprove plan?"):
                return

            repo_url = ask_input("\nEnter GitHub HTTPS Repository URL")
            workspace_path = ask_input("Enter local empty workspace path")

            wm.set_workspace(workspace_path)
            wm.clone_repo(repo_url)

            branch_name = f"ai/{sanitize_branch(plan['project_name'])}"
            wm.create_ai_branch(branch_name)

            state = {
                "idea": idea,
                "plan": plan,
                "repo_url": repo_url,
                "workspace_path": workspace_path,
                "branch_name": branch_name,
                "current_file_index": 0,
                "complexity": plan["complexity"],
                "status": "generating_files"
            }

            session.save(state)

        else:
            idea = state["idea"]
            plan = state["plan"]
            repo_url = state["repo_url"]
            workspace_path = state["workspace_path"]
            branch_name = state["branch_name"]

            wm.set_workspace(workspace_path)

        # -----------------------------------
        # ISSUE CREATION (Only Once)
        # -----------------------------------
        if state["complexity"] != "simple" and state["status"] == "generating_files":

            print("\nCreating milestone and issues...")

            success, milestone_number = create_milestone(
                repo_url,
                plan["project_name"],
                f"Milestone for {plan['project_name']}"
            )

            for idx, phase in enumerate(plan["phases"], start=1):
                create_issue(
                    repo_url,
                    f"Phase {idx}: {phase['phase_name']}",
                    phase.get("description", "")
                )

        # -----------------------------------
        # FILE GENERATION LOOP (Resumable)
        # -----------------------------------
        files = plan["file_structure"]
        start_index = state["current_file_index"]

        for index in range(start_index, len(files)):

            file_path = files[index]

            while True:
                print(f"\nGenerating code for: {file_path}")

                code = coder.generate_file_code(idea, file_path)

                wm.write_file(file_path, code)
                wm.git_add_all()

                diff = wm.get_diff()
                print_diff(diff)

                choice = input("Approve (a) | Rewrite (r) | Cancel (c): ").strip().lower()

                if choice == "a":
                    state["current_file_index"] = index + 1
                    session.save(state)
                    break
                elif choice == "r":
                    continue
                else:
                    print("Aborted.")
                    return

        # -----------------------------------
        # COMMIT & PUSH
        # -----------------------------------
        commit_message = f"AI: Implementation for {plan['project_name']}"

        print("\nCommit Message:", commit_message)

        if not ask_confirm("\nApprove commit?"):
            return

        username = ask_input("GitHub Username")
        token = getpass.getpass("GitHub PAT (hidden): ")

        wm.set_commit_identity(username)
        wm.git_commit(commit_message)
        wm.push_with_pat(username, token, branch_name)

        print("\nCode pushed successfully.")

        state["status"] = "completed"
        session.clear()

    except WorkspaceSecurityError as e:
        print("\nSecurity Error:", e)
    except Exception as e:
        print("\nError:", e)


if __name__ == "__main__":
    main()
