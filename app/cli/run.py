from app.state.store import STATE, load_state, save_state, clear_state, archive_state
from app.agents.planner import generate_phases
from app.agents.task_expander import expand_phase
from app.agents.verifier import verify_phase
from app.utils.github import create_issue
from app.utils.ui import (
    console, print_header, print_success, print_error, print_warning, print_info,
    print_phase_header, print_tasks_table, print_phases_list, ask_input, ask_confirm,
    print_commit_message, print_note, print_welcome, print_separator
)


def handle_startup_state():
    """
    Check for existing session state and handle resume/new scenarios.
    
    Returns:
        bool: True if we should skip setup (resuming), False if starting fresh
    """
    saved_state = load_state()
    
    if not saved_state:
        # No saved state, start fresh
        return False
    
    project_name = saved_state.get("project", "Unknown Project")
    status = saved_state.get("status", "unknown")
    
    # Handle COMPLETED projects
    if status == "completed":
        print_success(f"Project '{project_name}' was already completed.")
        console.print()
        choice = ask_confirm("Start a NEW project?", default=True)
        
        if not choice:
            print_info("Exiting. Resume your work anytime!")
            exit(0)
        else:
            # Archive the completed project and start fresh
            archive_state()
            print_info("Starting a new project...")
            console.print()
            return False
    
    # Handle IN-PROGRESS projects
    elif status == "in_progress":
        current_phase = saved_state.get("current_phase", 0)
        total_phases = len(saved_state.get("phases", []))
        
        console.print()
        print_info(f"Found in-progress session: [bold]{project_name}[/bold]")
        console.print(f"   Phase {current_phase + 1} of {total_phases}", style="dim")
        console.print()
        
        choice = ask_confirm("Resume this session?", default=True)
        
        if not choice:
            # User wants to start fresh, confirm first
            console.print()
            confirm = ask_confirm("⚠️  This will CLEAR your in-progress session. Are you sure?", default=False)
            
            if confirm:
                clear_state()
                print_info("Starting a new project...")
                console.print()
                return False
            else:
                print_info("Exiting. Resume your work anytime!")
                exit(0)
        else:
            # Resume the session
            print_success(f"Resuming '{project_name}'...")
            console.print()
            STATE.update(saved_state)
            return True
    
    # Unknown status, treat as corrupted and start fresh
    else:
        console.print()
        print_warning("Session file appears corrupted. Starting fresh.")
        console.print()
        clear_state()
        return False


def main():
    print_welcome()

    # -----------------------------
    # STARTUP: Check for existing session
    # -----------------------------
    should_resume = handle_startup_state()
    
    # If resuming, skip the setup phase and jump to execution loop
    if not should_resume:
        # -----------------------------
        # ONE-TIME PROJECT CONTEXT (Fresh Start)
        # -----------------------------
        print_header("Project Setup", "Let's configure your project")
        console.print()
        
        STATE["project"] = ask_input("What do you want to build?")
        STATE["tech"] = ask_input("Tech stack?")
        STATE["features"] = ask_input("Core features?")
        STATE["platform"] = ask_input("Platform (web/mobile)?", default="web")

        console.print()
        print_info("Planning execution phases...")
        console.print()

    # INTERACTIVE PLANNING LOOP
    # Skip this if resuming an existing session
    if not should_resume:
        while True:
            STATE["phases"] = generate_phases(
                STATE["project"],
                STATE["tech"],
                STATE["features"],
                STATE["platform"]
            )

            if not STATE["phases"]:
                print_error("Failed to generate phases. Retrying...")
                continue

            console.print()
            print_phases_list(STATE["phases"], current_phase=0)
            console.print()

            console.print("[A]pprove Plan", style="bold green")
            console.print("[R]egenerate Plan", style="bold yellow")
            console.print("[E]dit Plan Manually", style="bold blue")
            console.print()
            
            choice = ask_input("Choice (A/R/E)").strip().upper()

            if choice == 'A':
                # Plan approved, mark as in-progress and save
                STATE["status"] = "in_progress"
                save_state()
                break
            elif choice == 'R':
                console.print()
                print_info("Regenerating plan...")
                continue
            elif choice == 'E':
                console.print()
                print_info("Enter phases manually (one per line). End with an empty line.")
                new_phases = []
                while True:
                    line = console.input("[cyan]>[/cyan] ").strip()
                    if not line:
                        break
                    # Ensure format "Phase X: Name"
                    if not line.lower().startswith("phase"):
                        line = f"Phase {len(new_phases)+1}: {line}"
                    new_phases.append(line)
                
                if new_phases:
                    STATE["phases"] = new_phases
                    # Plan approved via manual edit, save state
                    STATE["status"] = "in_progress"
                    save_state()
                    break
                else:
                    print_error("No phases entered. Keeping original plan.")

    # -----------------------------
    # GITHUB REPO (ONCE)
    # -----------------------------
    # Only ask for repo URL if starting fresh (not resuming)
    if not should_resume:
        console.print()
        STATE["repo_url"] = ask_input("Paste PUBLIC GitHub repo URL")
        
        # Ask about GitHub Issues
        STATE["create_issues"] = ask_confirm("Create GitHub Issues for tasks?", default=False)
        
        # Save state after getting repo info
        save_state()
    
    create_issues = STATE.get("create_issues", False)

    console.print()
    print_note("Important Notes", [
        "Repo must be PUBLIC",
        "You must PUSH commits to GitHub",
        "execution_orecal checks ONLY the latest commit message"
    ])
    console.print()

    # -----------------------------
    # EXECUTION LOOP
    # -----------------------------
    while STATE["current_phase"] < len(STATE["phases"]):
        idx = STATE["current_phase"]
        phase_line = STATE["phases"][idx]

        # Extract phase number + name
        try:
            # Handle user manually entered phases that might not have colons ideally
            if ":" in phase_line:
                phase_number_str = phase_line.split(":")[0].replace("Phase", "").strip()
                phase_name = phase_line.split(":", 1)[1].strip()
                phase_number = int(phase_number_str) if phase_number_str.isdigit() else idx + 1
            else:
                phase_number = idx + 1
                phase_name = phase_line
        except Exception:
            print_error(f"Parsing error for phase: {phase_line}")
            # Fallback
            phase_number = idx + 1
            phase_name = phase_line

        console.print()
        print_phase_header(phase_number, phase_name, len(STATE["phases"]))
        console.print()

        # Generate REAL tasks (Context Aware)
        tasks, expected_commit = expand_phase(
            phase_number,
            phase_name,
            STATE["project"],
            STATE["tech"],
            STATE["features"]
        )

        if not tasks:
            print_error("No tasks generated. This should not happen.")
            return

        print_tasks_table(tasks, title=f"📝 Phase {phase_number} Tasks")
        console.print()

        # Create GitHub Issues if requested
        if create_issues:
            print_info("Creating GitHub Issues...")
            for t in tasks:
                success, url = create_issue(STATE["repo_url"], title=f"Phase {phase_number}: {t}", body=f"Task generated by execution_orecal for Phase {phase_number}.")
                if success:
                    print_success(f"Issue created: {url}")
                else:
                    print_error(f"Failed to create issue: {url}")
            console.print()

        print_commit_message(expected_commit)
        console.print()

        print_note("Next Steps", [
            "1. Commit with the message above",
            "2. PUSH the commit to GitHub",
            '3. Type "next-phase"'
        ])
        console.print()

        cmd = console.input('[cyan]> [/cyan]').strip()

        if cmd != "next-phase":
            print_error('Invalid command. Type exactly: next-phase')
            continue

        # -----------------------------
        # GITHUB VERIFICATION
        # -----------------------------
        success, message = verify_phase(STATE["repo_url"], phase_number)

        console.print()
        if success:
            print_success("Phase verified successfully!")
            console.print(f"   {message}", style="dim")
            STATE["current_phase"] += 1
            # Save progress after each phase completion
            save_state()
        else:
            print_error("Phase NOT verified.")
            console.print(f"   {message}", style="dim")
            print_warning("Fix the commit message, push again, then type next-phase.")

    # All phases completed!
    console.print()
    print_separator()
    print_success("🎉 All phases completed!")
    print_success("execution_orecal finished execution successfully.")
    print_separator()
    console.print()
    
    # Mark as completed and save final state
    STATE["status"] = "completed"
    save_state()


if __name__ == "__main__":
    main()
