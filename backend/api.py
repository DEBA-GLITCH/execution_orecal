from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.planner import generate_phases
from agents.task_expander import expand_phase
from agents.conversation_agent import get_conversation_response
from state.store import Store

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = Store()

@app.post("/chat")
def chat(data: dict):
    message = data.get("message", "")
    history = data.get("history", [])
    
    try:
        # Check if user is asking to generate a plan (keywords)
        generate_keywords = ["generate", "create plan", "roadmap", "show me", "build plan", "execution plan"]
        should_generate_plan = any(keyword in message.lower() for keyword in generate_keywords)
        
        # If user wants a plan and we have project info in history
        if should_generate_plan and len(history) > 0:
            # Extract project info from conversation
            project_info = message
            for msg in history:
                if msg.get("role") == "user":
                    project_info = msg.get("content", "")
            
            # Generate phases
            phases = generate_phases(project_info)
            
            if phases:
                phase_data = []
                for i, phase_line in enumerate(phases[:3]):
                    try:
                        phase_name = phase_line.split(":", 1)[1].strip() if ":" in phase_line else phase_line
                        tasks, commit_msg = expand_phase(i+1, phase_name, project_info, "", "")
                        
                        phase_data.append({
                            "number": i+1,
                            "name": phase_name,
                            "tasks": tasks,
                            "commit_msg": commit_msg,
                            "status": "active" if i == 0 else "pending"
                        })
                    except Exception as e:
                        print(f"Error expanding phase {i+1}: {e}")
                        continue
                
                return {
                    "reply": f"Here's your execution plan:\n\nNow, please share your GitHub repository URL so I can review your code and help you get started!",
                    "phases": phase_data
                }
        
        # Otherwise, use conversational agent
        reply = get_conversation_response(message, history)
        
        return {"reply": reply}
        
    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return {"reply": f"I encountered an error. Could you rephrase that?"}

@app.post("/start-project")
def start_project(data: dict):
    idea = data.get("idea", "")
    
    # Generate phases from the idea
    phases = generate_phases(idea)
    
    if not phases:
        return {"error": "Failed to generate phases"}
    
    store.save_plan(phases)
    
    # Expand phases to get tasks (limit to first 3 for performance)
    phase_data = []
    for i, phase_line in enumerate(phases[:3]):
        try:
            phase_name = phase_line.split(":", 1)[1].strip() if ":" in phase_line else phase_line
            tasks, commit_msg = expand_phase(i+1, phase_name, idea, "", "")
            
            phase_data.append({
                "number": i+1,
                "name": phase_name,
                "tasks": tasks,
                "commit_msg": commit_msg,
                "status": "active" if i == 0 else "pending"
            })
        except Exception as e:
            print(f"Error expanding phase {i+1}: {e}")
            continue
    
    return {
        "message": f"Execution plan generated for: {idea}",
        "phases": phase_data
    }
