import requests
from app.config import GITHUB_TOKEN

def create_issue(repo_url, title, body=""):
    """
    Creates a GitHub issue in the specified repository.
    
    Args:
        repo_url (str): The full URL of the GitHub repository.
        title (str): The title of the issue.
        body (str): The body content of the issue.
        
    Returns:
        tuple: (bool, str) -> (Success/Failure, Message/URL)
    """
    if not GITHUB_TOKEN:
        return False, "GITHUB_TOKEN is missing in .env"

    # Extract owner and repo name from URL
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
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        
        if response.status_code == 201:
            issue_data = response.json()
            return True, issue_data.get("html_url")
        else:
            return False, f"Failed to create issue. Status: {response.status_code}, Error: {response.text}"
            
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"
