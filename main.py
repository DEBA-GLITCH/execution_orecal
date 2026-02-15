# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from app.agents.planner import client, MODEL_NAME, generate_phases

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    message: str
    history: List[ChatMessage]

@app.post("/chat")
async def chat_with_oracle(data: ChatInput):
    try:
        # This prompt mimics your run.py logic but lets the AI be creative
        system_message = {
            "role": "system", 
            "content": (
                "You are the Execution Oracle CLI. Follow this logic: "
                "1. If user greets you, ask what they want to build. "
                "2. When they describe a project, provide 2-3 professional implementation tips and ask for their tech stack. "
                "3. If they name a tech stack (like Flutter or React), suggest a modern folder structure and ask for core features or platform. "
                "4. Maintain a helpful, technical, yet concise tone. Always end with a clear question."
            )
        }

        messages = [system_message] + [m.dict() for m in data.history] + [{"role": "user", "content": data.message}]

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7
        )

        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start")
async def start_project(data: dict):
    # This remains for when you eventually want to generate the final Phase list
    try:
        phases = generate_phases(data['project'], data['tech'], data['features'], data['platform'])
        return {"phases": phases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))