import requests
import base64

def get_repo_structure(repo_url):
    """
    Fetch repository structure from GitHub API.
    repo_url: https://github.com/username/repo
    """
    try:
        # Parse repo URL
        parts = repo_url.rstrip('/').split('/')
        owner = parts[-2]
        repo = parts[-1]
        
        # Try multiple branch names
        branches = ['main', 'master', 'HEAD']
        
        for branch in branches:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                tree = data.get('tree', [])
                
                # Filter important files
                important_files = []
                for item in tree:
                    path = item['path']
                    # Focus on code files, ignore node_modules, build, etc
                    if any(path.startswith(ignore) for ignore in ['node_modules/', 'build/', 'dist/', '.git/']):
                        continue
                    if item['type'] == 'blob' and any(path.endswith(ext) for ext in ['.js', '.jsx', '.py', '.java', '.ts', '.tsx', '.json', '.md', '.html', '.css']):
                        important_files.append(path)
                
                return important_files[:20], None  # Limit to 20 files
        
        # If all branches fail, try getting repo info
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            repo_data = response.json()
            return [], f"Repository found: {repo_data.get('description', 'No description')}. Language: {repo_data.get('language', 'Unknown')}"
        
        return None, f"Could not access repository (Status: {response.status_code})"
        
    except Exception as e:
        return None, str(e)


def get_file_content(repo_url, file_path):
    """
    Fetch content of a specific file from GitHub.
    """
    try:
        parts = repo_url.rstrip('/').split('/')
        owner = parts[-2]
        repo = parts[-1]
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        content = base64.b64decode(data['content']).decode('utf-8')
        return content[:2000]  # Limit to first 2000 chars
        
    except Exception as e:
        return None


def analyze_repo(repo_url):
    """
    Analyze a GitHub repository and return summary.
    """
    files, error = get_repo_structure(repo_url)
    
    if error and not files:
        # Try to get basic repo info
        try:
            parts = repo_url.rstrip('/').split('/')
            owner = parts[-2]
            repo = parts[-1]
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return f"""📁 Repository: {data.get('name', 'Unknown')}
📝 Description: {data.get('description', 'No description')}
💻 Language: {data.get('language', 'Unknown')}
⭐ Stars: {data.get('stargazers_count', 0)}
🔀 Forks: {data.get('forks_count', 0)}

Note: Could not access detailed file structure. Repository might be empty or private."""
        except:
            pass
        
        return f"Error accessing repository: {error}"
    
    if not files and error:
        return error
    
    if not files:
        return "Repository appears to be empty."
    
    # Get content of key files
    key_files = ['package.json', 'README.md', 'requirements.txt', 'pom.xml', 'index.html']
    file_contents = {}
    
    for key_file in key_files:
        if key_file in files:
            content = get_file_content(repo_url, key_file)
            if content:
                file_contents[key_file] = content
    
    # Build summary
    summary = f"📁 Repository Structure ({len(files)} files):\n\n"
    
    # Group by extension
    extensions = {}
    for f in files:
        ext = f.split('.')[-1] if '.' in f else 'other'
        extensions[ext] = extensions.get(ext, 0) + 1
    
    summary += "File types:\n"
    for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
        summary += f"  • {ext}: {count} files\n"
    
    summary += f"\n📄 Key files found:\n"
    for f in files[:10]:
        summary += f"  • {f}\n"
    
    if file_contents:
        summary += f"\n📝 File contents:\n"
        for filename, content in file_contents.items():
            summary += f"\n--- {filename} ---\n{content[:500]}...\n"
    
    return summary
