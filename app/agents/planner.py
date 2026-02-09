from groq import Groq
from app.config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)

def generate_phases(project, tech, features, platform):
    prompt = f"""
Return ONLY execution phases.
No explanations. No markdown.

Format:
Phase 1: <short name>
Phase 2: <short name>

Project: {project}
Tech: {tech}
Features: {features}
Platform: {platform}
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200
    )

    return [
        l.strip() for l in res.choices[0].message.content.split("\n")
        if l.strip().startswith("Phase")
    ]
