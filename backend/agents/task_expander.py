from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
from utils.file_utils import get_file_tree
from utils.git_utils import get_git_diff, is_git_repo

client = Groq(api_key=GROQ_API_KEY)

def expand_phase(phase_number, phase_name, project, tech, features):
    # Get the current project structure and git diff for context
    try:
        file_tree = get_file_tree()
    except Exception:
        file_tree = "(No file context available)"

    git_context = ""
    if is_git_repo():
        git_context = f"\nRecent Code Changes (Git Diff):\n{get_git_diff()[:2000]}\n"

    prompt = f"""
You are an execution agent helping to build: {project}

Generate 4 to 6 concrete developer tasks for this phase.
Tasks must be clear actions a developer can do to build {project}.
DO NOT suggest tasks for execution_orecal or any other tool.
FOCUS ONLY on building: {project}

Phase: {phase_name}
Project: {project}
Tech stack: {tech}
Core features: {features}

Each task must be on a new line.
DO NOT use headings or explanations.

Example tasks:
- Create main.py file with Flask app initialization
- Add user authentication endpoints
- Design database schema for users table
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )

    raw_lines = res.choices[0].message.content.split("\n")

    # take any meaningful line as a task
    tasks = [
        line.strip()
        for line in raw_lines
        if line.strip() and not line.lower().startswith("phase")
    ]

    commit_msg = f"phase-{phase_number}: {phase_name.lower()} complete"

    return tasks, commit_msg

