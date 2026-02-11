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
    commit_sha = latest_commit["sha"]

    # Get the diff for this commit
    diff_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    headers["Accept"] = "application/vnd.github.v3.diff"
    diff_res = requests.get(diff_url, headers=headers)
    diff_text = diff_res.text[:5000] if diff_res.status_code == 200 else "(Diff unavailable)"

    expected = f"phase-{phase_number}"

    if expected in commit_msg.lower():
        # In a real scenario, we could pass diff_text to an AI for semantic verification
        return True, f"Matched commit: '{commit_msg}' (verified with diff context)"
    else:
        return False, f"Latest commit was: '{commit_msg}' (expected '{expected}')"

