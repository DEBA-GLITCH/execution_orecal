from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
from agents.repo_analyzer import analyze_repo
import re

client = Groq(api_key=GROQ_API_KEY)

def get_conversation_response(message, history):
    """
    Conversational agent that guides users through project planning.
    """
    
    # Check if message contains a GitHub URL
    github_pattern = r'https?://github\.com/[\w-]+/[\w-]+'
    github_match = re.search(github_pattern, message)
    
    if github_match:
        repo_url = github_match.group(0)
        print(f"Analyzing repo: {repo_url}")
        
        # Analyze the repository
        repo_summary = analyze_repo(repo_url)
        
        # Build conversation context with repo analysis
        messages = [
            {
                "role": "system",
                "content": f"""You are Execution Oracle, a code review assistant.

The user shared their GitHub repository. Here's what I found:

{repo_summary}

Based on this analysis:
1. Summarize what the project currently has
2. Identify what's missing or needs improvement
3. Suggest next steps to implement their desired features
4. Be specific and actionable

Keep response concise and helpful."""
            }
        ]
        
        # Add recent history for context
        for msg in history[-4:]:
            messages.append(msg)
        
        messages.append({"role": "user", "content": f"Here's my repo: {repo_url}. Please review it and suggest what I should do next."})
        
    else:
        # Regular conversation
        messages = [
            {
                "role": "system",
                "content": """You are Execution Oracle, a friendly AI assistant that helps developers plan and build projects.

Your conversation flow:
1. When user greets you (hi, hello, etc), ask them about their project idea
2. When they describe a project, ask clarifying questions about:
   - Tech stack preference
   - Core features
   - Platform (web/mobile/desktop)
3. Once you have enough info, generate a step-by-step roadmap
4. After showing roadmap, ask for their GitHub repo URL to review code
5. If they provide a repo, acknowledge and offer to review it

Be conversational, friendly, and helpful. Keep responses concise."""
            }
        ]
        
        # Add conversation history
        for msg in history:
            messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": message})
    
    # Get response from Groq
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content
