#!/usr/bin/env python3
"""
Quick test script to verify Rich UI components are working
"""
from app.utils.ui import (
    print_welcome,
    print_header,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_phase_header,
    print_tasks_table,
    print_phases_list,
    print_commit_message,
    print_note,
    print_separator,
    console
)

def test_ui():
    # Test welcome banner
    print_welcome()
    console.print()
    
    # Test header
    print_header("UI Component Test", "Testing all rich UI components")
    console.print()
    
    # Test message types
    print_success("This is a success message")
    print_error("This is an error message")
    print_warning("This is a warning message")
    print_info("This is an info message")
    console.print()
    
    # Test separator
    print_separator()
    console.print()
    
    # Test phases list
    phases = [
        "Phase 1: Setup Repository",
        "Phase 2: Create Backend API",
        "Phase 3: Build Frontend",
        "Phase 4: Deploy Application"
    ]
    print_phases_list(phases, current_phase=1)
    console.print()
    
    # Test phase header
    print_phase_header(2, "Create Backend API", 4)
    console.print()
    
    # Test tasks table
    tasks = [
        "Initialize Express.js server",
        "Create database schema",
        "Implement user authentication",
        "Add API routes for CRUD operations"
    ]
    print_tasks_table(tasks, title="📝 Backend Tasks")
    console.print()
    
    # Test commit message
    print_commit_message("phase-2: backend api complete")
    console.print()
    
    # Test note
    print_note("Important Notes", [
        "Ensure all tests pass",
        "Update documentation",
        "Push changes to GitHub"
    ])
    console.print()
    
    print_separator()
    print_success("✨ All UI components working correctly!")

if __name__ == "__main__":
    test_ui()
