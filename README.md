# Execution Orecal - AI-Powered Planning Dashboard

An intelligent execution planning system that transforms your project ideas into structured, actionable development phases. Get realistic roadmaps, task breakdowns, and execution strategies — all powered by AI.

## What It Does

Stop overthinking the roadmap. Just describe your project, and the system will:
- Analyze your idea and scope
- Generate a structured execution plan with phases
- Break down each phase into concrete tasks
- Suggest commit messages and milestones
- Provide an interactive dashboard to visualize and track progress

Perfect for startups, indie developers, and teams who need to move fast without losing clarity.

---

## 🛠 Tech Stack

- **Backend**: FastAPI with Python 3.10+
- **Frontend**: React 19 + Vite
- **AI Engine**: Groq LLaMA 3 (8B)
- **Styling**: CSS with modern glass-morphism UI

---

## 📋 Prerequisites

Before you start, make sure you have:

- **Python 3.10 or higher**
- **Node.js 18+ and npm** (for the frontend)
- **A Groq API key** (free tier available at [console.groq.com](https://console.groq.com))
- **Git** (optional, for cloning the repo)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/DEBA-GLITCH/execution_orecal.git
cd execution_orecal
```

### 2. Set Up Environment Variables

Create a `.env` file in the `backend/` directory with your API keys:

```bash
cd backend
touch .env
```

Add the following to `backend/.env`:

```
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama3-8b-8192
GITHUB_TOKEN=your_github_token_here  # Optional, for GitHub integration
```

**How to get your Groq API key:**
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API keys
4. Create a new API key and copy it

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or if you prefer using a virtual environment (recommended):

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 5. Run the Application

**Start the backend** (from the `backend/` directory):

```bash
python cli/run.py
```

The backend will be available at `http://localhost:8000`

**In a new terminal, start the frontend** (from the `frontend/` directory):

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

Open your browser to `http://localhost:5173` and you're ready to go!

---

## 📁 Project Structure

```
execution_orecal/
│
├── backend/                          # Python FastAPI backend
│   ├── agents/                       # AI reasoning agents
│   │   ├── conversation_agent.py    # Natural language conversations
│   │   ├── planner.py               # Generates execution phases
│   │   ├── task_expander.py         # Breaks phases into tasks
│   │   ├── suggestion_agent.py      # Code suggestions & improvements
│   │   ├── repo_analyzer.py         # Analyzes GitHub repositories
│   │   └── verifier.py              # Validates execution plans
│   │
│   ├── state/
│   │   └── store.py                 # State management & storage
│   │
│   ├── utils/                        # Shared utilities
│   │   ├── file_utils.py            # File I/O operations
│   │   ├── git_utils.py             # Git operations
│   │   ├── github.py                # GitHub API integration
│   │   ├── task_manager.py          # Task tracking
│   │   ├── rollback.py              # Undo/rollback functionality
│   │   └── ui.py                    # CLI formatting
│   │
│   ├── cli/
│   │   └── run.py                   # CLI entry point
│   │
│   ├── api.py                        # FastAPI routes
│   ├── config.py                     # Configuration & environment
│   └── requirements.txt              # Python dependencies
│
├── frontend/                         # React + Vite frontend
│   ├── src/
│   │   ├── components/              # Reusable UI components
│   │   │   ├── TopBar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── MainBody.jsx
│   │   │   ├── FeatureCard.jsx
│   │   │   └── GlassCard.js
│   │   │
│   │   ├── features/                # Feature modules
│   │   │   └── Onboarding.js
│   │   │
│   │   ├── App.jsx                  # Main app component
│   │   ├── main.jsx                 # Entry point
│   │   ├── App.css                  # App styles
│   │   └── index.css                # Global styles
│   │
│   ├── public/                      # Static assets
│   ├── package.json                 # Node dependencies
│   ├── vite.config.js               # Vite configuration
│   └── eslint.config.js             # Linting rules
│
└── README.md                         # This file
```

---

## 📝 How to Use

1. **Start the application** using the steps above
2. **Enter your project idea** in the text input (e.g., "Build a mobile app for tracking personal finances")
3. **Generate the plan** - the AI will break down your idea into phases
4. **Review the execution plan** - see tasks, recommendations, and milestones
5. **Track progress** - use the dashboard to monitor each phase

---

## 🔌 API Endpoints

### Chat Endpoint
```
POST /chat
```
Send a message and get AI-powered responses or plans.

**Request:**
```json
{
  "message": "Create a plan for building a social media app",
  "history": []
}
```

**Response:**
```json
{
  "reply": "Here's your execution plan...",
  "phases": [
    {
      "number": 1,
      "name": "Phase One",
      "tasks": ["Task 1", "Task 2"],
      "commit_msg": "Initial commit",
      "status": "active"
    }
  ]
}
```

### Start Project Endpoint
```
POST /start-project
```
Initialize a new project with an idea.

**Request:**
```json
{
  "idea": "Build a real-time collaborative document editor"
}
```

---

## 🧠 How the AI Works

The system uses multiple specialized agents:

1. **Planner Agent** - Takes your idea and generates major execution phases
2. **Task Expander** - Breaks each phase into concrete, actionable tasks
3. **Conversation Agent** - Engages in natural conversation to gather requirements
4. **Suggestion Agent** - Provides code improvements and best practices
5. **Verifier** - Validates the execution plan for feasibility
6. **Repo Analyzer** - Analyzes existing GitHub repositories for context

All agents use Groq's LLaMA 3 model for reasoning and planning.

---

## 🐛 Troubleshooting

### Backend won't start
- Verify Python version: `python --version` (should be 3.10+)
- Check if `.env` file exists and has `GROQ_API_KEY`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Frontend shows error connecting to backend
- Ensure backend is running on `http://localhost:8000`
- Check if frontend is on `http://localhost:5173`
- Look at browser console for CORS or network errors

### API key error
- Double-check your Groq API key is correct
- Ensure `.env` file is in the `backend/` directory (not in root)
- Try regenerating a new API key from the Groq console

### Slow responses
- Groq free tier may have rate limits - wait a moment and retry
- Try with a shorter project description for faster responses

---

## 🛠 Development

### Backend Development

```bash
cd backend
source venv/bin/activate
python cli/run.py
```

The backend reloads automatically on file changes (thanks to FastAPI's reload mode).

### Frontend Development

```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` - Vite provides hot module replacement (HMR) for instant updates.

### Linting

```bash
cd frontend
npm run lint
```

### Production Build

```bash
cd frontend
npm run build
```

---

## 📦 Dependencies

### Backend
- `fastapi` - Modern web framework
- `groq` - LLM API client
- `python-dotenv` - Environment variable management
- `requests` - HTTP library
- `rich` - Beautiful CLI output

### Frontend
- `react` - UI library
- `react-dom` - React DOM rendering
- `lucide-react` - Icons
- `vite` - Build tool (dev dependency)

---

## 🤝 Contributing

Found a bug or have a feature request? Here's how to help:

1. **Report issues** - Open a GitHub issue with details
2. **Submit PRs** - Fork, create a branch, and submit a pull request
3. **Improve docs** - Help us keep documentation clear and accurate

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## ❓ FAQ

**Q: Do I need a paid Groq account?**
A: No, the free tier is sufficient for development and testing.

**Q: Can I use a different LLM?**
A: Yes, you can modify `backend/config.py` to use different LLM providers (OpenAI, Anthropic, etc.).

**Q: Is my data stored anywhere?**
A: Currently, data is stored locally. No external storage is configured by default.

**Q: Can I deploy this to production?**
A: Yes! You'll need to configure proper environment variables, database setup, and deploy both backend and frontend separately.

---

## Autonomous coder agent (Experimental)

Features:
- Adaptive complexity planning
- Branch-safe execution
- File-by-file diff preview
- Rewrite loop
- Resumable session recovery
- PAT-based GitHub push

