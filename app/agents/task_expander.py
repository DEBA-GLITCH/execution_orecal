from groq import Groq
from app.config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)

from app.utils.file_utils import get_file_tree

def expand_phase(phase_number, phase_name, project, tech, features):
    # Get the current project structure for context
    try:
        file_tree = get_file_tree()
    except Exception:
        file_tree = "(No file context available)"

    prompt = f"""
You are an execution agent.

Generate 4 to 6 concrete developer tasks for this phase.
Tasks must be clear actions a developer can do.
DO NOT use headings.
DO NOT explain.
Each task must be on a new line.

Phase: {phase_name}
Project: {project}
Tech stack: {tech}
Core features: {features}

Current File Structure (for context):
{file_tree}

If files already exist, suggest editing them instead of creating new ones.
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
