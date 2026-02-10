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


def print_tasks_table(tasks, title="Tasks"):
    """Print tasks in a formatted table"""
    table = Table(title=title, box=box.ROUNDED, border_style="blue", show_header=True, header_style="bold cyan")
    
    table.add_column("", style="dim", width=3)
    table.add_column("Task", style="white")
    
    for i, task in enumerate(tasks, 1):
        table.add_row(f"{i}.", task)
    
    console.print(table)


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
