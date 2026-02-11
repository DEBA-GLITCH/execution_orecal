"""
Rollback and phase navigation utilities for execution_orecal
Handles phase history, rollback operations, and phase retry functionality
"""

from datetime import datetime
from app.state.store import STATE, save_state


def record_phase_completion(phase_index, phase_name, commit_sha="", time_spent=""):
    """
    Record a phase completion in history
    
    Args:
        phase_index: Index of the completed phase
        phase_name: Name of the phase
        commit_sha: Git commit SHA (optional)
        time_spent: Human-readable time spent (e.g., "1h 23m")
    """
    # Initialize phase_history if it doesn't exist (backward compatibility)
    if "phase_history" not in STATE:
        STATE["phase_history"] = []
    
    # Count completed tasks
    from app.utils.task_manager import get_tasks
    tasks = get_tasks(phase_index)
    tasks_completed = sum(1 for task in tasks if task.get("completed", False))
    
    # Create history entry
    history_entry = {
        "phase": phase_index,
        "phase_name": phase_name,
        "completed_at": datetime.now().isoformat(),
        "commit_sha": commit_sha,
        "time_spent": time_spent,
        "tasks_completed": tasks_completed,
        "total_tasks": len(tasks)
    }
    
    STATE["phase_history"].append(history_entry)
    save_state()


def get_phase_history():
    """
    Get the phase completion history
    
    Returns:
        list: Phase history entries
    """
    if "phase_history" not in STATE:
        STATE["phase_history"] = []
    
    return STATE["phase_history"]


def rollback_to_phase(phase_index):
    """
    Roll back to a specific phase
    
    Args:
        phase_index: Index of the phase to roll back to
        
    Returns:
        bool: True if successful, False if invalid
    """
    if phase_index < 0 or phase_index >= len(STATE.get("phases", [])):
        return False
    
    if phase_index >= STATE.get("current_phase", 0):
        # Can't roll back to current or future phase
        return False
    
    # Clear tasks for phases after the rollback point
    if "phase_tasks" in STATE:
        phases_to_clear = list(range(phase_index + 1, STATE["current_phase"] + 1))
        for p in phases_to_clear:
            phase_key = str(p)
            if phase_key in STATE["phase_tasks"]:
                del STATE["phase_tasks"][phase_key]
    
    # Clear time tracking for future phases
    if "phase_time_tracking" in STATE:
        phases_to_clear = list(range(phase_index + 1, STATE["current_phase"] + 1))
        for p in phases_to_clear:
            phase_key = str(p)
            if phase_key in STATE["phase_time_tracking"]:
                del STATE["phase_time_tracking"][phase_key]
    
    # Update current phase
    STATE["current_phase"] = phase_index
    
    # Add rollback record to history (for tracking)
    if "phase_history" not in STATE:
        STATE["phase_history"] = []
    
    STATE["phase_history"].append({
        "action": "rollback",
        "rolled_back_to": phase_index,
        "timestamp": datetime.now().isoformat()
    })
    
    save_state()
    return True


def retry_current_phase():
    """
    Reset the current phase to start over
    
    Returns:
        bool: True if successful
    """
    current = STATE.get("current_phase", 0)
    phase_key = str(current)
    
    # Clear tasks for current phase
    if "phase_tasks" in STATE and phase_key in STATE["phase_tasks"]:
        del STATE["phase_tasks"][phase_key]
    
    # Clear time tracking for current phase
    if "phase_time_tracking" in STATE and phase_key in STATE["phase_time_tracking"]:
        del STATE["phase_time_tracking"][phase_key]
    
    # Add retry record to history
    if "phase_history" not in STATE:
        STATE["phase_history"] = []
    
    STATE["phase_history"].append({
        "action": "retry",
        "phase": current,
        "timestamp": datetime.now().isoformat()
    })
    
    save_state()
    return True


def can_rollback():
    """
    Check if rollback is possible
    
    Returns:
        bool: True if at least one phase has been completed
    """
    return STATE.get("current_phase", 0) > 0


def get_rollback_choices():
    """
    Get list of phases that can be rolled back to
    
    Returns:
        list: List of (phase_index, phase_name) tuples
    """
    current = STATE.get("current_phase", 0)
    phases = STATE.get("phases", [])
    
    choices = []
    for i in range(current):
        phase_name = phases[i] if i < len(phases) else f"Phase {i+1}"
        choices.append((i, phase_name))
    
    return choices


def undo_last_verification():
    """
    Undo the last phase verification (go back one phase)
    Only works if we just moved forward
    
    Returns:
        bool: True if successful, False if can't undo
    """
    current = STATE.get("current_phase", 0)
    
    if current == 0:
        return False  # Can't undo from first phase
    
    # Move back one phase
    previous_phase = current - 1
    STATE["current_phase"] = previous_phase
    
    # Add undo record to history
    if "phase_history" not in STATE:
        STATE["phase_history"] = []
    
    STATE["phase_history"].append({
        "action": "undo",
        "from_phase": current,
        "to_phase": previous_phase,
        "timestamp": datetime.now().isoformat()
    })
    
    save_state()
    return True


def get_completed_phases_count():
    """
    Get count of completed phases (for display)
    
    Returns:
        int: Number of completed phases
    """
    history = get_phase_history()
    # Count only completion entries (not rollback/retry/undo)
    return sum(1 for entry in history if "action" not in entry)
