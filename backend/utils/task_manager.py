"""
Task management utilities for execution_orecal
Handles task CRUD operations, completion tracking, and time tracking
"""

from datetime import datetime
from app.state.store import STATE, save_state


def save_tasks(phase_index, tasks):
    """
    Save tasks for a specific phase
    
    Args:
        phase_index: Index of the phase
        tasks: List of task description strings
    """
    # Initialize phase_tasks if it doesn't exist (backward compatibility)
    if "phase_tasks" not in STATE:
        STATE["phase_tasks"] = {}
    
    # Convert string tasks to task objects if new
    phase_key = str(phase_index)
    
    if phase_key not in STATE["phase_tasks"]:
        # New phase, create task objects
        STATE["phase_tasks"][phase_key] = [
            {
                "task": task,
                "completed": False,
                "started_at": None
            }
            for task in tasks
        ]
    # If tasks already exist, don't overwrite (preserves completion status)
    
    save_state()


def get_tasks(phase_index):
    """
    Retrieve tasks for a specific phase with completion status
    
    Args:
        phase_index: Index of the phase
        
    Returns:
        List of task objects with completion status
    """
    if "phase_tasks" not in STATE:
        STATE["phase_tasks"] = {}
    
    phase_key = str(phase_index)
    return STATE["phase_tasks"].get(phase_key, [])


def mark_task_complete(phase_index, task_index):
    """
    Mark a task as complete
    
    Args:
        phase_index: Index of the phase
        task_index: Index of the task (0-based)
        
    Returns:
        bool: True if successful, False if task doesn't exist
    """
    tasks = get_tasks(phase_index)
    
    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = True
        if tasks[task_index]["started_at"] is None:
            tasks[task_index]["started_at"] = datetime.now().isoformat()
        save_state()
        return True
    
    return False


def mark_task_incomplete(phase_index, task_index):
    """
    Mark a task as incomplete
    
    Args:
        phase_index: Index of the phase
        task_index: Index of the task (0-based)
        
    Returns:
        bool: True if successful, False if task doesn't exist
    """
    tasks = get_tasks(phase_index)
    
    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = False
        save_state()
        return True
    
    return False


def add_task(phase_index, task_description):
    """
    Add a new task to the current phase
    
    Args:
        phase_index: Index of the phase
        task_description: Description of the new task
    """
    if "phase_tasks" not in STATE:
        STATE["phase_tasks"] = {}
    
    phase_key = str(phase_index)
    
    if phase_key not in STATE["phase_tasks"]:
        STATE["phase_tasks"][phase_key] = []
    
    STATE["phase_tasks"][phase_key].append({
        "task": task_description,
        "completed": False,
        "started_at": None
    })
    
    save_state()


def delete_task(phase_index, task_index):
    """
    Remove a task from the phase
    
    Args:
        phase_index: Index of the phase
        task_index: Index of the task (0-based)
        
    Returns:
        bool: True if successful, False if task doesn't exist
    """
    tasks = get_tasks(phase_index)
    
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
        save_state()
        return True
    
    return False


def edit_task(phase_index, task_index, new_description):
    """
    Edit a task's description
    
    Args:
        phase_index: Index of the phase
        task_index: Index of the task (0-based)
        new_description: New task description
        
    Returns:
        bool: True if successful, False if task doesn't exist
    """
    tasks = get_tasks(phase_index)
    
    if 0 <= task_index < len(tasks):
        tasks[task_index]["task"] = new_description
        save_state()
        return True
    
    return False


def get_task_stats(phase_index):
    """
    Get task completion statistics for a phase
    
    Args:
        phase_index: Index of the phase
        
    Returns:
        dict: {"completed": int, "total": int, "percentage": float}
    """
    tasks = get_tasks(phase_index)
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    percentage = (completed / total * 100) if total > 0 else 0
    
    return {
        "completed": completed,
        "total": total,
        "percentage": percentage
    }


def start_phase_timer(phase_index):
    """
    Start tracking time for a phase
    
    Args:
        phase_index: Index of the phase
    """
    if "phase_time_tracking" not in STATE:
        STATE["phase_time_tracking"] = {}
    
    phase_key = str(phase_index)
    
    if phase_key not in STATE["phase_time_tracking"]:
        STATE["phase_time_tracking"][phase_key] = {
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        save_state()


def complete_phase_timer(phase_index):
    """
    Stop tracking time for a phase
    
    Args:
        phase_index: Index of the phase
        
    Returns:
        str: Human-readable time spent (e.g., "2h 15m")
    """
    if "phase_time_tracking" not in STATE:
        return None
    
    phase_key = str(phase_index)
    
    if phase_key in STATE["phase_time_tracking"]:
        STATE["phase_time_tracking"][phase_key]["completed_at"] = datetime.now().isoformat()
        save_state()
        
        # Calculate duration
        started = datetime.fromisoformat(STATE["phase_time_tracking"][phase_key]["started_at"])
        completed = datetime.fromisoformat(STATE["phase_time_tracking"][phase_key]["completed_at"])
        duration = completed - started
        
        # Format as human-readable
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    return None
