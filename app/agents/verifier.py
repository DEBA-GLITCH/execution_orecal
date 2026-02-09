import requests
from app.config import GITHUB_TOKEN

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

    expected = f"phase-{phase_number}"

    if expected in commit_msg.lower():
        return True, f"Matched commit: '{commit_msg}'"
    else:
        return False, f"Latest commit was: '{commit_msg}' (expected '{expected}')"
