import requests
from app.config import GITHUB_TOKEN

def create_issue(repo_url, title, body="", milestone=None, labels=None):
    """
    Creates a GitHub issue in the specified repository.
    """
    if not GITHUB_TOKEN:
        return False, "GITHUB_TOKEN is missing"

    try:
        parts = repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]
    except IndexError:
        return False, "Invalid GitHub Repository URL"

    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "title": title,
        "body": body
    }
    if milestone:
        payload["milestone"] = milestone
    if labels:
        payload["labels"] = labels
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Check for label permission error (403)
        if response.status_code == 403 and "label" in response.text.lower() and labels:
            # Retry without labels
            payload.pop("labels")
            response = requests.post(api_url, json=payload, headers=headers)
            
        if response.status_code == 201:
            return True, response.json().get("html_url")
        return False, f"Error: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"
def create_pull_request(repo_url, title, head, base="main", body=""):
    """
    Creates a GitHub Pull Request.
    """
    if not GITHUB_TOKEN:
        return False, "GITHUB_TOKEN is missing"

    try:
        parts = repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]
    except IndexError:
        return False, "Invalid Repository URL"

    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"title": title, "head": head, "base": base, "body": body}
    
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 201:
        return True, response.json().get("html_url")
    return False, f"Error: {response.status_code}, {response.text}"

def create_label(repo_url, name, color, description=""):
    """
    Creates a label if it doesn't exist.
    """
    if not GITHUB_TOKEN: return False, "Missing token"
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"name": name, "color": color, "description": description}
    
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code in [201, 422]: # 422 usually means already exists
        return True, "Label ensured"
    return False, response.text

def add_labels_to_issue(repo_url, issue_number, labels):
    """
    Adds labels to an existing issue.
    """
    if not GITHUB_TOKEN: return False, "Missing token"
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"labels": labels}
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.status_code == 200, response.text

def create_milestone(repo_url, title, description=""):
    """
    Creates a milestone and returns its number.
    """
    if not GITHUB_TOKEN: return False, "Missing token"
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/milestones"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"title": title, "description": description}
    
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 201:
        return True, response.json()["number"]
    return False, response.text
