import requests
from groq import Groq
from app.config import GITHUB_TOKEN, GROQ_API_KEY, MODEL_NAME

def verify_phase(repo_url, phase_number):
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return False, f"GitHub API error: {res.status_code}"

    latest_commit = res.json()[0]
    commit_msg = latest_commit["commit"]["message"]
    commit_sha = latest_commit["sha"]

    # Get the diff for this commit
    diff_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    headers["Accept"] = "application/vnd.github.v3.diff"
    diff_res = requests.get(diff_url, headers=headers)
    diff_text = diff_res.text[:5000] if diff_res.status_code == 200 else "(Diff unavailable)"

    expected = f"phase-{phase_number}"

    if expected in commit_msg.lower():
        # AI-based semantic verification of the diff context
        try:
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f"""
            Verify if the following code changes (Git Diff) actually implement the goals for Phase {phase_number}.
            
            Commit Message: {commit_msg}
            Git Diff (truncated):
            {diff_text}
            
            Return 'YES' if it looks correct, or 'NO' if it looks unrelated or incomplete.
            Add a very brief 1-sentence explanation.
            """
            
            res = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=100
            )
            ai_opinion = res.choices[0].message.content.strip()
            
            if ai_opinion.upper().startswith("NO"):
                return False, f"Matched commit but AI rejected it: {ai_opinion}"
            
            return True, f"Matched commit and AI verified: {ai_opinion}"
            
        except Exception as e:
            # Fallback to simple matching if AI fails
            return True, f"Matched commit: '{commit_msg}' (AI verification skipped: {e})"
    else:
        return False, f"Latest commit was: '{commit_msg}' (expected '{expected}')"

