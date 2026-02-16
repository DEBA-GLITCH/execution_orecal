# AI-Powered Execution Planning Dashboard

Turn your project ideas into structured execution phases using AI.

Built with:
- ⚡ FastAPI (Backend)
- ⚛️ React + Vite (Frontend)
- 🧠 LLM-based Planning Engine

---

## 🏆 Hackathon Project Overview

Execution Orecal is an AI-driven execution planning system that transforms raw ideas into structured development phases.

Instead of manually breaking down ideas, users can:

1. Enter a project idea
2. Instantly generate execution phases
3. Visualize the roadmap in a modern dashboard UI

---

## 🏗 Project Structure

```
execution_orecal/
│
├── backend/              # FastAPI + AI logic
│   ├── agents/
│   ├── state/
│   ├── utils/
│   ├── api.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/             # React + Vite dashboard
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# ⚙️ Prerequisites

- Python 3.10+
- Node.js 18+
- npm

---

# 🔧 Backend Setup

### 1️⃣ Navigate to backend

```bash
cd backend
```

### 2️⃣ Create virtual environment (optional)

```bash
python -m venv venv
```


### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create environment file

Create `.env` file inside `backend/`:

```
GROQ_API_KEY=your_api_key_here
MODEL_NAME=your_model_name
```

### 5️⃣ Run backend server

```bash
uvicorn api:app --reload
```

Backend will run at:

```
http://localhost:8000
```

Swagger docs available at:

```
http://localhost:8000/docs
```

---

# 💻 Frontend Setup

### 1️⃣ Navigate to frontend

```bash
cd frontend
```

### 2️⃣ Install dependencies

```bash
npm install
```

### 3️⃣ Start development server

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🔄 How It Works

1. User enters project idea in dashboard
2. Frontend sends POST request to `/start-project`
3. Backend generates structured execution phases
4. Phases are returned as JSON
5. UI renders the execution roadmap

---

# 🌟 Key Features

- AI-powered phase generation
- Modern glassmorphism UI
- Clean backend architecture
- Swagger API documentation
- Modular agent-based design

---

# 🛡 Security Note

Do NOT commit `.env` file.

Use `.env.example` as template.

---

# 🚀 Future Scope

- Task expansion per phase
- Auto GitHub issue creation
- Code generation agent
- Phase progress tracking
- Deployment support

---

# 👨‍💻 Built For Hackathon

Execution Orecal demonstrates:

- Full-stack AI integration
- LLM workflow automation
- Clean API architecture
- Modern frontend experience

---

### 💡 Turn ideas into action.
