from app.state.store import STATE, load_state, save_state, clear_state, archive_state
from app.agents.planner import generate_phases
from app.agents.task_expander import expand_phase
from app.agents.verifier import verify_phase
from app.utils.github import create_issue
from app.utils.ui import (
    console, print_header, print_success, print_error, print_warning, print_info,
    print_phase_header, print_tasks_table, print_phases_list, ask_input, ask_confirm,
    print_commit_message, print_note, print_welcome, print_separator, print_task_stats,
    print_task_commands
)
from app.utils.task_manager import (
    save_tasks, get_tasks, mark_task_complete, mark_task_incomplete,
    add_task, delete_task, edit_task, get_task_stats, start_phase_timer, complete_phase_timer
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

        # Start phase timer
        start_phase_timer(idx)

        # Generate REAL tasks (Context Aware) - only if not already saved
        existing_tasks = get_tasks(idx)
        
        if not existing_tasks:
            # First time seeing this phase, generate tasks
            task_strings, expected_commit = expand_phase(
                phase_number,
                phase_name,
                STATE["project"],
                STATE["tech"],
                STATE["features"]
            )

            if not task_strings:
                print_error("No tasks generated. This should not happen.")
                return
            
            # Save tasks to state
            save_tasks(idx, task_strings)
            tasks = get_tasks(idx)
        else:
            # Resuming phase, use existing tasks
            tasks = existing_tasks
            # Regenerate commit message
            _, expected_commit = expand_phase(
                phase_number,
                phase_name,
                STATE["project"],
                STATE["tech"],
                STATE["features"]
            )

        # Display tasks with status
        print_tasks_table(tasks, title=f"📝 Phase {phase_number} Tasks", show_status=True)
        console.print()
        
        # Show task progress
        stats = get_task_stats(idx)
        if stats["total"] > 0:
            print_task_stats(stats["completed"], stats["total"], phase_number)
            console.print()

        # Create GitHub Issues if requested (only if tasks were just generated)
        if create_issues and not existing_tasks:
            print_info("Creating GitHub Issues...")
            for task_obj in tasks:
                task_text = task_obj["task"] if isinstance(task_obj, dict) else task_obj
                success, url = create_issue(STATE["repo_url"], title=f"Phase {phase_number}: {task_text}", body=f"Task generated by execution_orecal for Phase {phase_number}.")
                if success:
                    print_success(f"Issue created: {url}")
                else:
                    print_error(f"Failed to create issue: {url}")
            console.print()

        print_commit_message(expected_commit)
        console.print()

        print_task_commands()
        console.print()

        # Task management command loop
        while True:
            cmd = console.input('[cyan]> [/cyan]').strip()

            if cmd == "next-phase":
                # Check if all tasks are complete
                stats = get_task_stats(idx)
                if stats["completed"] < stats["total"]:
                    console.print()
                    print_warning(f"Only {stats['completed']}/{stats['total']} tasks completed.")
                    proceed = ask_confirm("Proceed to verification anyway?", default=False)
                    if not proceed:
                        console.print()
                        print_info("Continue working on tasks.")
                        console.print()
                        continue
                
                # Exit task loop and proceed to verification
                break
            
            elif cmd == "help":
                console.print()
                print_task_commands()
                console.print()
            
            elif cmd == "list-tasks":
                console.print()
                tasks = get_tasks(idx)
                print_tasks_table(tasks, title=f"📝 Phase {phase_number} Tasks", show_status=True)
                console.print()
                stats = get_task_stats(idx)
                print_task_stats(stats["completed"], stats["total"], phase_number)
                console.print()
            
            elif cmd.startswith("mark "):
                try:
                    task_num = int(cmd.split()[1]) - 1  # Convert to 0-based index
                    if mark_task_complete(idx, task_num):
                        print_success(f"Task {task_num + 1} marked as complete")
                    else:
                        print_error(f"Invalid task number: {task_num + 1}")
                except (ValueError, IndexError):
                    print_error("Usage: mark <number>")
            
            elif cmd.startswith("unmark "):
                try:
                    task_num = int(cmd.split()[1]) - 1
                    if mark_task_incomplete(idx, task_num):
                        print_info(f"Task {task_num + 1} marked as incomplete")
                    else:
                        print_error(f"Invalid task number: {task_num + 1}")
                except (ValueError, IndexError):
                    print_error("Usage: unmark <number>")
            
            elif cmd == "add-task":
                console.print()
                task_desc = ask_input("Enter new task description")
                if task_desc:
                    add_task(idx, task_desc)
                    print_success("Task added successfully")
                console.print()
            
            elif cmd.startswith("edit-task "):
                try:
                    task_num = int(cmd.split()[1]) - 1
                    console.print()
                    tasks = get_tasks(idx)
                    if 0 <= task_num < len(tasks):
                        current = tasks[task_num]["task"]
                        console.print(f"[dim]Current: {current}[/dim]")
                        new_desc = ask_input("Enter new description")
                        if new_desc:
                            edit_task(idx, task_num, new_desc)
                            print_success("Task updated successfully")
                    else:
                        print_error(f"Invalid task number: {task_num + 1}")
                    console.print()
                except (ValueError, IndexError):
                    print_error("Usage: edit-task <number>")
            
            elif cmd.startswith("delete-task "):
                try:
                    task_num = int(cmd.split()[1]) - 1
                    console.print()
                    confirm = ask_confirm(f"Delete task {task_num + 1}?", default=False)
                    if confirm:
                        if delete_task(idx, task_num):
                            print_success("Task deleted successfully")
                        else:
                            print_error(f"Invalid task number: {task_num + 1}")
                    console.print()
                except (ValueError, IndexError):
                    print_error("Usage: delete-task <number>")
            
            else:
                print_error(f'Unknown command: {cmd}. Type "help" for available commands.')
                console.print()

        # -----------------------------
        # GITHUB VERIFICATION
        # -----------------------------
        success, message = verify_phase(STATE["repo_url"], phase_number)

        console.print()
        if success:
            # Complete phase timer
            time_spent = complete_phase_timer(idx)
            
            print_success("Phase verified successfully!")
            console.print(f"   {message}", style="dim")
            
            if time_spent:
                console.print(f"   [dim]Time spent: {time_spent}[/dim]")
            
            console.print()
            
            STATE["current_phase"] += 1
            # Save progress after each phase completion
            save_state()
        else:
            print_error("Phase NOT verified.")
            console.print(f"   {message}", style="dim")
            print_warning("Fix the commit message, push again, then type next-phase.")
            console.print()

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
