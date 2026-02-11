"""
UI utilities for rich terminal output
Provides consistent, colorful formatting for the execution_orecal CLI
"""

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.text import Text
from rich import box
from rich.prompt import Prompt, Confirm

# Global console instance
console = Console()


def print_header(title, subtitle=""):
    """Print a styled header with optional subtitle"""
    if subtitle:
        text = f"[bold cyan]{title}[/bold cyan]\n[dim]{subtitle}[/dim]"
    else:
        text = f"[bold cyan]{title}[/bold cyan]"
    
    console.print(Panel(text, box=box.DOUBLE, border_style="cyan"))


def print_success(message):
    """Print a success message in green"""
    console.print(f"✅ [bold green]{message}[/bold green]")


def print_error(message):
    """Print an error message in red"""
    console.print(f"❌ [bold red]{message}[/bold red]")


def print_warning(message):
    """Print a warning message in yellow"""
    console.print(f"⚠️  [bold yellow]{message}[/bold yellow]")


def print_info(message):
    """Print an info message in blue"""
    console.print(f"ℹ️  [blue]{message}[/blue]")


def print_separator():
    """Print a visual separator line"""
    console.print("─" * console.width, style="dim")


def print_phase_header(phase_number, phase_name, total_phases):
    """Print a styled phase header with progress"""
    progress_percent = (phase_number / total_phases) * 100
    
    title = f"Phase {phase_number} of {total_phases}: {phase_name}"
    subtitle = f"Overall Progress: {progress_percent:.0f}%"
    
    # Create progress bar text
    filled = int(progress_percent / 5)  # 20 blocks for 100%
    bar = "█" * filled + "░" * (20 - filled)
    
    panel_content = f"[bold white]{title}[/bold white]\n\n{bar} [cyan]{progress_percent:.0f}%[/cyan]\n[dim]{subtitle}[/dim]"
    
    console.print(Panel(panel_content, box=box.HEAVY, border_style="magenta", padding=(1, 2)))


def print_tasks_table(tasks, title="Tasks", show_status=False):
    """
    Print tasks in a formatted table
    
    Args:
        tasks: List of task strings OR list of task objects with 'task' and 'completed' keys
        title: Table title
        show_status: If True, shows completion status column
    """
    table = Table(title=title, box=box.ROUNDED, border_style="blue", show_header=True, header_style="bold cyan")
    
    table.add_column("", style="dim", width=3)
    table.add_column("Task", style="white")
    
    if show_status:
        table.add_column("Status", width=10)
    
    for i, task in enumerate(tasks, 1):
        # Handle both string tasks and task objects
        if isinstance(task, dict):
            task_text = task["task"]
            if show_status:
                status = "[green]✅ Done[/green]" if task.get("completed", False) else "[dim]☐ Todo[/dim]"
                table.add_row(f"{i}.", task_text, status)
            else:
                table.add_row(f"{i}.", task_text)
        else:
            # String task
            table.add_row(f"{i}.", task)
            if show_status:
                table.add_row(f"{i}.", task, "[dim]☐ Todo[/dim]")
    
    console.print(table)


def print_task_stats(completed, total, phase_number=None):
    """
    Print task completion statistics
    
    Args:
        completed: Number of completed tasks
        total: Total number of tasks
        phase_number: Optional phase number to display
    """
    percentage = (completed / total * 100) if total > 0 else 0
    
    # Progress bar
    filled = int(percentage / 5)  # 20 blocks for 100%
    bar = "█" * filled + "░" * (20 - filled)
    
    if phase_number:
        title = f"Phase {phase_number} Progress"
    else:
        title = "Task Progress"
    
    content = f"{bar} [cyan]{percentage:.0f}%[/cyan]\n[bold]{completed}/{total} tasks completed[/bold]"
    
    console.print(Panel(content, title=title, border_style="cyan", box=box.ROUNDED))


def print_task_commands():
    """Print available task management commands"""
    commands_text = """
[bold cyan]Task Management Commands:[/bold cyan]

  [yellow]mark <number>[/yellow]          Mark task as complete (e.g., 'mark 1')
  [yellow]unmark <number>[/yellow]        Mark task as incomplete
  [yellow]add-task[/yellow]               Add a new task to current phase
  [yellow]edit-task <number>[/yellow]     Edit task description
  [yellow]delete-task <number>[/yellow]   Remove a task
  [yellow]list-tasks[/yellow]             Show all tasks with status

[bold cyan]Navigation Commands:[/bold cyan]

  [yellow]next-phase[/yellow]             Proceed to verification (move to next phase)
  [yellow]rollback[/yellow]               Go back to a previous phase
  [yellow]retry-phase[/yellow]            Reset current phase and start over
  [yellow]undo-verify[/yellow]            Undo last phase verification
  [yellow]history[/yellow]                View phase completion history
  [yellow]help[/yellow]                   Show this help message
"""
    console.print(Panel(commands_text.strip(), border_style="blue", box=box.ROUNDED))


def print_phase_history(history, current_phase_index):
    """
    Print phase completion history in a table
    
    Args:
        history: List of history entries
        current_phase_index: Current phase index
    """
    from datetime import datetime
    
    table = Table(title="📜 Phase Completion History", box=box.ROUNDED, border_style="cyan", show_header=True)
    
    table.add_column("Phase", style="bold", width=10)
    table.add_column("Name", style="white")
    table.add_column("Completed", style="dim", width=20)
    table.add_column("Tasks", width=10)
    table.add_column("Time", width=10)
    
    # Filter only completion entries (not rollback/retry/undo actions)
    completions = [h for h in history if "action" not in h]
    
    if not completions:
        console.print("[dim]No phases completed yet[/dim]")
        return
    
    for entry in completions:
        phase_num = entry.get("phase", 0) + 1
        phase_name = entry.get("phase_name", f"Phase {phase_num}")
        
        # Remove "Phase X:" prefix if exists
        if ":" in phase_name:
            phase_name = phase_name.split(":", 1)[1].strip()
        
        # Format timestamp
        completed_at = entry.get("completed_at", "")
        if completed_at:
            try:
                dt = datetime.fromisoformat(completed_at)
                formatted_time = dt.strftime("%b %d, %I:%M %p")
            except:
                formatted_time = "Unknown"
        else:
            formatted_time = "Unknown"
        
        tasks_info = f"{entry.get('tasks_completed', 0)}/{entry.get('total_tasks', 0)}"
        time_spent = entry.get('time_spent', '-')
        
        table.add_row(
            f"Phase {phase_num}",
            phase_name,
            formatted_time,
            tasks_info,
            time_spent
        )
    
    console.print(table)


def print_rollback_warning(current_phase, target_phase, phases):
    """
    Print warning about rollback consequences
    
    Args:
        current_phase: Current phase index
        target_phase: Target phase index to roll back to
        phases: List of all phases
    """
    current_name = phases[current_phase] if current_phase < len(phases) else f"Phase {current_phase + 1}"
    target_name = phases[target_phase] if target_phase < len(phases) else f"Phase {target_phase + 1}"
    
    warning_text = f"""[bold red]⚠️  WARNING: Rollback Consequences[/bold red]

[yellow]You are about to:[/yellow]
  • Roll back from {current_name} to {target_name}
  • Clear all tasks for phases after Phase {target_phase + 1}
  • Reset progress for {current_phase - target_phase} phase(s)

[green]What will be preserved:[/green]
  • Phase history (for reference)
  • Tasks for {target_name} and earlier phases

[bold]This action will require you to redo the cleared phases.[/bold]
"""
    
    console.print(Panel(warning_text.strip(), border_style="red", box=box.HEAVY, padding=(1, 2)))


def ask_rollback_target(choices):
    """
    Ask user to select which phase to roll back to
    
    Args:
        choices: List of (phase_index, phase_name) tuples
        
    Returns:
        int or None: Selected phase index, or None if cancelled
    """
    console.print()
    console.print("[bold cyan]Select phase to roll back to:[/bold cyan]")
    console.print()
    
    for i, (phase_idx, phase_name) in enumerate(choices, 1):
        # Remove "Phase X:" prefix if exists
        if ":" in phase_name:
            phase_name = phase_name.split(":", 1)[1].strip()
        console.print(f"  [yellow]{i}.[/yellow] Phase {phase_idx + 1}: {phase_name}")
    
    console.print()
    choice = ask_input("Enter phase number (or 'c' to cancel)")
    
    if choice.lower() == 'c':
        return None
    
    try:
        selection = int(choice)
        if 1 <= selection <= len(choices):
            return choices[selection - 1][0]  # Return phase_index
        else:
            print_error(f"Invalid selection. Please choose 1-{len(choices)}")
            return None
    except ValueError:
        print_error("Invalid input. Please enter a number or 'c' to cancel")
        return None




def print_phases_list(phases, current_phase=0):
    """Print all phases with status indicators"""
    table = Table(title="📋 Execution Plan", box=box.ROUNDED, border_style="cyan", show_header=True)
    
    table.add_column("Phase", style="bold", width=10)
    table.add_column("Name", style="white")
    table.add_column("Status", width=12)
    
    for i, phase in enumerate(phases):
        # Extract phase name (remove "Phase X:" prefix if exists)
        phase_name = phase.split(":", 1)[1].strip() if ":" in phase else phase
        
        if i < current_phase:
            status = "[green]✅ Done[/green]"
        elif i == current_phase:
            status = "[yellow]⚡ Active[/yellow]"
        else:
            status = "[dim]⏳ Pending[/dim]"
        
        table.add_row(f"Phase {i+1}", phase_name, status)
    
    console.print(table)


def ask_input(prompt_text, default=None):
    """Get user input with styled prompt"""
    if default:
        return Prompt.ask(f"[bold cyan]{prompt_text}[/bold cyan]", default=default)
    return Prompt.ask(f"[bold cyan]{prompt_text}[/bold cyan]")


def ask_confirm(question, default=True):
    """Ask a yes/no question"""
    return Confirm.ask(f"[bold yellow]{question}[/bold yellow]", default=default)


def print_commit_message(commit_msg):
    """Print the expected commit message in a highlighted panel"""
    console.print(Panel(
        f"[bold green]{commit_msg}[/bold green]",
        title="📝 Expected Commit Message",
        border_style="green",
        box=box.ROUNDED
    ))


def print_note(title, messages):
    """Print a note panel with multiple lines"""
    content = "\n".join(f"• {msg}" for msg in messages)
    console.print(Panel(content, title=f"📌 {title}", border_style="yellow", box=box.ROUNDED))


def create_spinner(text="Processing..."):
    """Create a progress spinner for long operations"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        console=console,
        transient=True
    )


def print_welcome():
    """Print welcome banner"""
    banner = """
[bold cyan]╔═══════════════════════════════════════╗
║                                       ║
║     execution_orecal 🔮               ║
║     Your AI Execution Oracle          ║
║                                       ║
╚═══════════════════════════════════════╝[/bold cyan]
"""
    console.print(banner)
