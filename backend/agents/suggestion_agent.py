from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
from utils.git_utils import get_git_diff, is_git_repo, get_project_summary

client = Groq(api_key=GROQ_API_KEY)

def get_suggestions(project, tech, features):
    """Generates smart coding suggestions based on context and git diff."""
    
    git_context = "Not a git repository."
    if is_git_repo():
        git_context = get_git_diff()
        
    project_summary = get_project_summary()

    prompt = f"""
You are an expert developer assistant. 
Based on the current project context and recent code changes, suggest the next 3 logical steps or code improvements.

Project: {project}
Tech stack: {tech}
Core features: {features}

Project File Structure:
{project_summary}

Current Code Changes (Git Diff):
{git_context}

Provide concise, actionable advice. Format as a bulleted list.
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=500
    )

    return res.choices[0].message.content.strip()
