import json
import os
from pathlib import Path
from datetime import datetime

# STATE dictionary holds all session information
STATE = {
    "project": "",
    "tech": "",
    "features": "",
    "platform": "",
    "repo_url": "",
    "phases": [],
    "current_phase": 0,
    "status": "setup",  # Possible values: 'setup', 'in_progress', 'completed'
    "phase_tasks": {},  # Format: {phase_index: [{"task": "...", "completed": bool, "started_at": timestamp}]}
    "phase_time_tracking": {},  # Format: {phase_index: {"started_at": timestamp, "completed_at": timestamp}}
    "phase_history": []  # Format: [{"phase": 0, "completed_at": timestamp, "commit": "sha", "tasks_snapshot": [...]}]
}

# Storage configuration
# Store session data in .oracle_data/ folder in project root
STORAGE_DIR = Path(".oracle_data")
STATE_FILE = STORAGE_DIR / "session.json"
ARCHIVE_DIR = STORAGE_DIR / "archive"


def load_state():
    """
    Load session state from .oracle_data/session.json if it exists.
    
    Returns:
        dict: The loaded state, or None if file doesn't exist or is invalid
    """
    if not STATE_FILE.exists():
        return None
    
    try:
        with open(STATE_FILE, 'r') as f:
            loaded_data = json.load(f)
            # Validate that loaded data has required keys
            if "project" in loaded_data and "status" in loaded_data:
                return loaded_data
            return None
    except (json.JSONDecodeError, IOError):
        # If file is corrupted or unreadable, return None
        return None


def save_state():
    """
    Save the current STATE to .oracle_data/session.json.
    Creates the directory if it doesn't exist.
    """
    # Create .oracle_data directory if it doesn't exist
    STORAGE_DIR.mkdir(exist_ok=True)
    
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(STATE, f, indent=2)
    except IOError as e:
        print(f"⚠️  Warning: Failed to save state: {e}")


def clear_state():
    """
    Delete the session.json file.
    Used when user wants to start a completely fresh session.
    """
    if STATE_FILE.exists():
        try:
            STATE_FILE.unlink()
        except IOError as e:
            print(f"⚠️  Warning: Failed to clear state: {e}")


def archive_state():
    """
    Move the current session.json to archive/ with a timestamp.
    Used when completing a project or starting a new one after completion.
    """
    if not STATE_FILE.exists():
        return
    
    # Create archive directory if needed
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp-based archive filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = STATE.get("project", "unknown").replace(" ", "_")[:30]
    archive_file = ARCHIVE_DIR / f"{timestamp}_{project_name}.json"
    
    try:
        # Move session.json to archive
        STATE_FILE.rename(archive_file)
        print(f"✅ Session archived to: {archive_file}")
    except IOError as e:
        print(f"⚠️  Warning: Failed to archive state: {e}")


class Store:
    def save_plan(self, phases):
        STATE["phases"] = phases
        save_state()

