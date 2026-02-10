from app.state.store import STATE, load_state, save_state, clear_state, archive_state
from app.agents.planner import generate_phases
from app.agents.task_expander import expand_phase
from app.agents.verifier import verify_phase
from app.utils.github import create_issue


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
        print(f"\n✅ Project '{project_name}' was already completed.\n")
        choice = input("Start a NEW project? (Y/n): ").strip().lower()
        
        if choice == 'n':
            print("\nExiting. Resume your work anytime!")
            exit(0)
        else:
            # Archive the completed project and start fresh
            archive_state()
            print("\n🆕 Starting a new project...\n")
            return False
    
    # Handle IN-PROGRESS projects
    elif status == "in_progress":
        current_phase = saved_state.get("current_phase", 0)
        total_phases = len(saved_state.get("phases", []))
        
        print(f"\n📂 Found in-progress session: '{project_name}'")
        print(f"   Phase {current_phase + 1} of {total_phases}\n")
        
        choice = input("Resume this session? (Y/n): ").strip().lower()
        
        if choice == 'n':
            # User wants to start fresh, confirm first
            confirm = input("\n⚠️  This will CLEAR your in-progress session. Are you sure? (y/N): ").strip().lower()
            
            if confirm == 'y':
                clear_state()
                print("\n🆕 Starting a new project...\n")
                return False
            else:
                print("\nExiting. Resume your work anytime!")
                exit(0)
        else:
            # Resume the session
            print(f"\n▶️  Resuming '{project_name}'...\n")
            STATE.update(saved_state)
            return True
    
    # Unknown status, treat as corrupted and start fresh
    else:
        print("\n⚠️  Session file appears corrupted. Starting fresh.\n")
        clear_state()
        return False


def main():
    print("\n=== execution_orecal : Execution Oracle CLI ===\n")

    # -----------------------------
    # STARTUP: Check for existing session
    # -----------------------------
    should_resume = handle_startup_state()
    
    # If resuming, skip the setup phase and jump to execution loop
    if not should_resume:
        # -----------------------------
        # ONE-TIME PROJECT CONTEXT (Fresh Start)
        # -----------------------------
        STATE["project"] = input("What do you want to build?\n> ").strip()
        STATE["tech"] = input("Tech stack?\n> ").strip()
        STATE["features"] = input("Core features?\n> ").strip()
        STATE["platform"] = input("Platform (web/mobile)?\n> ").strip()

        print("\nPlanning execution phases...\n")

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
                print("❌ Failed to generate phases. Retrying...")
                continue

            print("\nHere is your execution plan:\n")
            for i, p in enumerate(STATE["phases"]):
                print(f"{i+1}. {p}")

            print("\n[A]pprove Plan")
            print("[R]egenerate Plan")
            print("[E]dit Plan Manually")
            
            choice = input("\nChoice (A/R/E): ").strip().upper()

            if choice == 'A':
                # Plan approved, mark as in-progress and save
                STATE["status"] = "in_progress"
                save_state()
                break
            elif choice == 'R':
                print("\n♻️ Regenerating plan...")
                continue
            elif choice == 'E':
                print("\nEnter phases manually (one per line). End with an empty line.")
                new_phases = []
                while True:
                    line = input("> ").strip()
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
                    print("❌ No phases entered. Keeping original plan.")

    # -----------------------------
    # GITHUB REPO (ONCE)
    # -----------------------------
    # Only ask for repo URL if starting fresh (not resuming)
    if not should_resume:
        STATE["repo_url"] = input("\nPaste PUBLIC GitHub repo URL:\n> ").strip()
        
        # Ask about GitHub Issues
        create_issues_input = input("Create GitHub Issues for tasks? (y/n): ").strip().lower()
        STATE["create_issues"] = (create_issues_input == 'y')
        
        # Save state after getting repo info
        save_state()
    
    create_issues = STATE.get("create_issues", False)

    print("\nNOTE:")
    print("- Repo must be PUBLIC")
    print("- You must PUSH commits to GitHub")
    print("- execution_orecal checks ONLY the latest commit message\n")

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
            print("❌ Parsing error for phase:", phase_line)
            # Fallback
            phase_number = idx + 1
            phase_name = phase_line

        print(f"\n=== {phase_line} ===\n")

        # Generate REAL tasks (Context Aware)
        tasks, expected_commit = expand_phase(
            phase_number,
            phase_name,
            STATE["project"],
            STATE["tech"],
            STATE["features"]
        )

        if not tasks:
            print("❌ No tasks generated. This should not happen.")
            return

        print("Tasks:")
        for t in tasks:
            print(f"- {t}")

        # Create GitHub Issues if requested
        if create_issues:
            print("\nCreating GitHub Issues...")
            for t in tasks:
                success, url = create_issue(STATE["repo_url"], title=f"Phase {phase_number}: {t}", body=f"Task generated by execution_orecal for Phase {phase_number}.")
                if success:
                    print(f"  ✅ Issue created: {url}")
                else:
                    print(f"  ❌ Failed to create issue: {url}")

        print("\nExpected commit message (intent-based):")
        print(expected_commit)

        print("\nAfter completing tasks:")
        print("1. Commit with the message above")
        print("2. PUSH the commit to GitHub")
        print('3. Type "next-phase"\n')

        cmd = input('> ').strip()

        if cmd != "next-phase":
            print('❌ Invalid command. Type exactly: next-phase')
            continue

        # -----------------------------
        # GITHUB VERIFICATION
        # -----------------------------
        success, message = verify_phase(STATE["repo_url"], phase_number)

        if success:
            print("\n✅ Phase verified successfully.")
            print(message)
            STATE["current_phase"] += 1
            # Save progress after each phase completion
            save_state()
        else:
            print("\n❌ Phase NOT verified.")
            print(message)
            print("Fix the commit message, push again, then type next-phase.")

    # All phases completed!
    print("\n🎉 All phases completed.")
    print("execution_orecal finished execution successfully.")
    
    # Mark as completed and save final state
    STATE["status"] = "completed"
    save_state()


if __name__ == "__main__":
    main()
