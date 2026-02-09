from groq import Groq
from app.config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)

def expand_phase(phase_number, phase_name, project, tech, features):
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
