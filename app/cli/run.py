from app.state.store import STATE
from app.agents.planner import generate_phases
from app.agents.task_expander import expand_phase
from app.agents.verifier import verify_phase


def main():
    print("\n=== execution_orecal : Execution Oracle CLI ===\n")

    # -----------------------------
    # ONE-TIME PROJECT CONTEXT
    # -----------------------------
    STATE["project"] = input("What do you want to build?\n> ").strip()
    STATE["tech"] = input("Tech stack?\n> ").strip()
    STATE["features"] = input("Core features?\n> ").strip()
    STATE["platform"] = input("Platform (web/mobile)?\n> ").strip()

    print("\nPlanning execution phases...\n")

    STATE["phases"] = generate_phases(
        STATE["project"],
        STATE["tech"],
        STATE["features"],
        STATE["platform"]
    )

    if not STATE["phases"]:
        print("❌ Failed to generate phases. Exiting.")
        return

    print("Here is your execution plan:\n")
    for p in STATE["phases"]:
        print(p)

    # -----------------------------
    # GITHUB REPO (ONCE)
    # -----------------------------
    STATE["repo_url"] = input("\nPaste PUBLIC GitHub repo URL:\n> ").strip()

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
            phase_number = idx + 1
            phase_name = phase_line.split(":", 1)[1].strip()
        except Exception:
            print("❌ Invalid phase format:", phase_line)
            return

        print(f"\n=== {phase_line} ===\n")

        # Generate REAL tasks
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
        else:
            print("\n❌ Phase NOT verified.")
            print(message)
            print("Fix the commit message, push again, then type next-phase.")

    print("\n🎉 All phases completed.")
    print("execution_orecal finished execution successfully.")


if __name__ == "__main__":
    main()
