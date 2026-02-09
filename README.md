# execution_orecal

**execution_orecal** is an AI-powered project manager CLI that guides you through building software projects step-by-step. It breaks down your idea into execution phases, generates concrete developer tasks, and verifies your progress by checking your GitHub commits.

## Features

- **🤖 Phase Generation**: Automatically breaks down your project into logical execution phases.
- **📝 Context-Aware Task Generation**: Reads your current file structure to generate relevant, actionable tasks.
- **🔍 Interactive Planning**: Review, edit, or regenerate the project plan before starting.
- **✅ GitHub Verification**: Verifies that you have completed a phase by checking if your latest commit message matches the required intent.
- **octocat: GitHub Issue Integration**: Automatically creates GitHub Issues for generated tasks with a single click.

## Prerequisites

- Python 3.8+
- A [Groq API Key](https://console.groq.com/) (for AI generation)
- A GitHub Account & [Personal Access Token](https://github.com/settings/tokens) (for repo verification and issue creation)
- Git installed and configured locally

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <your-repo-url>
    cd execution_orecal
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root directory with the following keys:

```ini
# .env file

# Required: API Key for Groq (LLM provider)
GROQ_API_KEY=gsk_...

# Optional: Documentation says it defaults to llama3-8b-8192
MODEL_NAME=llama3-8b-8192

# Required: GitHub Token for verification and creating issues
# Scopes needed: 'repo' (for private repos) or 'public_repo' (for public)
GITHUB_TOKEN=ghp_...
```

## Usage

Run the CLI tool from the root directory:

```bash
python -m app.cli.run
```

### Workflow

1.  **Initialization**: The tool asks for your **Project Name**, **Tech Stack**, **Features**, and **Platform**.
2.  **Planning**: It generates a high-level plan (Phases).
    - You can **[A]pprove**, **[R]egenerate**, or **[E]dit** this plan interactively.
3.  **Repository Setup**: It asks for your **GitHub Repository URL** and whether you want to auto-create GitHub Issues.
4.  **Execution Loop**:
    - **Current Phase**: displays the phase name.
    - **Tasks**: lists concrete tasks to complete.
    - **Issues**: If enabled, creates GitHub issues for these tasks.
    - **Work**: You write the code, complete the tasks, and commit your changes.
    - **Commit Intent**: You MUST use the specific commit message format provided by the tool (e.g., `phase-1: setup complete`).
    - **Verification**: Type `next-phase`. The tool checks your GitHub repo's latest commit. If the message matches, you proceed to the next phase.

## Troubleshooting

-   **"Phase NOT verified"**: Ensure you have `git push`'ed your commits to the remote repo. The tool checks the *remote* GitHub repo, not your local git.
-   **"GROQ_API_KEY missing"**: Ensure you created the `.env` file and it is valid.
-   **Issues not creating**: Check if your `GITHUB_TOKEN` has the `repo` or `public_repo` scope.

## Project Structure

```
execution_orecal/
├── app/
│   ├── agents/          # AI Logic (Planner, task expander)
│   ├── cli/             # Main entry point (run.py)
│   ├── state/           # State management
│   └── utils/           # Utilities (GitHub, File System)
├── requirements.txt     # Python dependencies
├── .env                 # API Keys (gitignored)
└── README.md            # This file
```
