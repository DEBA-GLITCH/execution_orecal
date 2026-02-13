# 🔮 Execution Oracle

> **An AI-Powered, Context-Aware Project Execution Assistant**

**Execution Oracle** is a sophisticated CLI tool designed to streamline your development workflow. It bridges the gap between planning and execution by generating phase-specific tasks, tracking progress, and automating your GitHub workflow—all while maintaining deep context awareness of your codebase.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🌟 Key Features

### 🧠 Smart Context & AI
*   **Context-Aware Task Generation**: Analyzes your file structure and `git diff` to generate relevant, actionable tasks for each development phase.
*   **AI Semantic Verification**: Uses **Groq AI** to semantically analyze your code changes and verify if they actually meet the phase goals—not just keyword matching.
*   **Smart Suggestions**: Run `suggest` to get AI-powered coding advice based on your current work-in-progress.

### 🎨 Rich Terminal UI
*   **Modern Interface**: Built with `rich` for a beautiful, colorful, and readable terminal experience.
*   **Visual Progress**: Track phase completion with dynamic progress bars and status indicators (✅/☐).
*   **Interactive Tables**: View and manage tasks in clean, formatted tables.

### ⚡ Enhanced Task Management
*   **Granular Control**: Add, edit, delete, and mark tasks as complete/incomplete interactively.
*   **State Persistence**: Your progress is saved automatically. Quit and resume exactly where you left off.
*   **Time Tracking**: Automatically tracks time spent on each phase for productivity insights.

### 🛡️ Safety & Navigation
*   **Rollback & Retry**: Made a mistake? Rollback to a previous phase or retry the current one with a single command.
*   **Undo Verification**: Accidentally verified a phase? Undo it and keep working.
*   **History Tracking**: View a complete history of verified phases and time spent.

### 🐙 Deep GitHub Integration
*   **Automated Project Management**:
    *   **Milestones**: Automatically creates GitHub Milestones for each phase.
    *   **Issues**: Generates GitHub Issues for tasks, auto-tagged with labels (`phase-X`) and assigned to milestones.
    *   **Robust Handling**: Automatically handles permission errors (like missing label scopes) gracefully.
*   **Pull Request Automation**: Suggests and creates detailed Pull Requests upon phase completion.
*   **Branch Strategy**: Detects `main` branch usage and suggests creating feature branches to keep your workflow clean.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.8+
*   A Groq API Key (for AI features)
*   A GitHub Personal Access Token (for integration features)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/execution_orecal.git
    cd execution_orecal
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_groq_api_key
    GITHUB_TOKEN=your_github_token
    MODEL_NAME=llama3-8b-8192  # or your preferred Groq model
    ```

---

## 📖 Usage

### Start the Oracle
Run the CLI application:
```bash
python3 -m app.cli.run
```

### Navigation & Commands
Once inside the tool, you have a powerful command suite at your disposal:

| Command | Description |
| :--- | :--- |
| **Task Management** | |
| `mark <n>` | Mark task #n as complete |
| `unmark <n>` | Mark task #n as incomplete |
| `add-task` | Add a custom task to the current phase |
| `edit-task <n>` | Edit the description of task #n |
| `delete-task <n>` | Remove task #n |
| `list-tasks` | Show the task table again |
| **Navigation** | |
| `next-phase` | Verify current work and proceed to the next phase |
| `rollback` | Go back to a previous phase (destructive for current progress) |
| `retry-phase` | Restart the current phase from scratch |
| `undo-verify` | Undo the last successful verification |
| `history` | Show the session history log |
| **AI** | |
| `suggest` | Request AI analysis and next-step suggestions |
| `help` | Show this help menu |

---

## 📂 Project Structure

```
execution_orecal/
├── app/
│   ├── agents/          # AI Agents (Planner, Expander, Verifier, Suggestion)
│   ├── cli/             # Main CLI entry point and logic
│   ├── state/           # Session state management
│   └── utils/           # Utilities (UI, Git, GitHub, Files, Tasks)
├── .oracle_data/        # Local session storage (auto-generated)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Built with passion by Deba-Glitch*
