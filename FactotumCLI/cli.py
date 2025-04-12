import argparse
import importlib
import pkgutil
from pathlib import Path
from rich.console import Console
import questionary
from questionary import Style
from rich.panel import Panel
from rich.text import Text

custom_style = Style([
    ('qmark', 'fg:#00c0ff bold'),     # Question mark
    ('question', 'bold'),             # Question text
    ('answer', 'fg:#91e4ff bold'),    # User's answer
    ('pointer', 'fg:#91e4ff bold'),   # Pointer for select
    ('highlighted', 'fg:#91e4ff bold'), # Highlighted choice
    ('selected', 'fg:#00ff00'),       # Style for a selected item
    ('separator', 'fg:#cc5454'),
    ('instruction', ''),              # User instructions
    ('text', ''),                     # Plain text
    ('disabled', 'fg:#858585 italic') # Disabled choices
])

console = Console()

# Dynamic import of all tools
from . import tools

tool_functions = {}

# Discover and import all tool modules
for loader, module_name, is_pkg in pkgutil.iter_modules(tools.__path__):
    module = importlib.import_module(f"{tools.__name__}.{module_name}")
    for attr in dir(module):
        if not attr.startswith("_") and callable(getattr(module, attr)):
            tool_functions[attr.replace("_", "-")] = getattr(module, attr)

# Main function to handle command line arguments
def main():
    console.print("[bold blue]🔧 FactotumCLI — Your Personal Assistant[/bold blue]")

    parser = argparse.ArgumentParser(description="FactotumCLI Tasks")
    parser.add_argument("--task", help="Task to perform")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive mode")
    parser.add_argument("--length", type=int, help="Password length")
    parser.add_argument("--specials", type=str, help="Include special characters: y/n")
    parser.add_argument("--directory", type=str, help="Directory for file operations")
    parser.add_argument("--coin", type=str, help="Crypto coin ID")
    parser.add_argument("--url", type=str, help="URL of the web page")
    parser.add_argument("--output", type=str, help="Output filename")
    parser.add_argument("--tool", type=str, help="Specific tool to show help for")

    args = parser.parse_args()

    if args.interactive:
        run_interactive_mode()
        return

    task = args.task.lower()

    if task in tool_functions:
        # Pass arguments dynamically based on function signature
        kwargs = vars(args)
        del kwargs['task']  # Remove task name from kwargs
        # Filter kwargs to only those accepted by the function
        from inspect import signature
        sig = signature(tool_functions[task])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters and v is not None}

        tool_functions[task](**filtered_kwargs)
    
    elif task == "list":
        console.print("🧩 Available tasks:", style="bold cyan")
        for func_name, func in tool_functions.items():
            doc = func.__doc__.strip() if func.__doc__ else "No description available."
            short_doc = doc.split('\n')[0]
            console.print(f"• [bold green]{func_name}[/bold green] — {short_doc}")

    elif task == "help":
        if not args.tool:
            console.print("Please specify a tool with --tool", style="bold red")
        elif args.tool in tool_functions:
            func = tool_functions[args.tool]
            doc = func.__doc__.strip() if func.__doc__ else "No documentation available."
            console.print(f"🧩 [bold cyan]{args.tool}[/bold cyan] documentation:\n")
            console.print(doc)
        else:
            console.print(f"Tool '{args.tool}' not found.", style="bold red")


    else:
        console.print(f"❌ Unknown task: '{task}'", style="bold red")
        console.print("🧩 Available tasks:", style="bold cyan")
        for func_name, func in tool_functions.items():
            doc = func.__doc__.strip() if func.__doc__ else "No description available."
            # Only show the first line of the docstring for brevity
            short_doc = doc.split('\n')[0]
            console.print(f"• [bold green]{func_name}[/bold green] — {short_doc}")

def run_interactive_mode():
    console = Console()

    # Build your splash screen text properly
    splash_text = Text(justify="center")
    splash_text.append("""
███████╗ █████╗  ██████╗████████╗ ██████╗ ████████╗██╗   ██╗███╗   ███╗
██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗╚══██╔══╝██║   ██║████╗ ████║
█████╗  ███████║██║        ██║   ██║   ██║   ██║   ██║   ██║██╔████╔██║
██╔══╝  ██╔══██║██║        ██║   ██║   ██║   ██║   ██║   ██║██║╚██╔╝██║
██║     ██║  ██║╚██████╗   ██║   ╚██████╔╝   ██║   ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝
\n""")
    splash_text.append("Welcome to ", style="bold")
    splash_text.append("FactotumCLI", style="bold magenta")
    splash_text.append(" 🎩\n", style="bold")
    splash_text.append("Your personal terminal assistant.\n", style="bold cyan")

    console.print(Panel(splash_text, style="bold blue"))

    console.print("\n[bold cyan]🧩 Choose a task from the menu below:[/bold cyan]\n")
    
    # List all available functions
    choices = [
        questionary.Choice(
            title=f"{name} — {func.__doc__.strip().splitlines()[0] if func.__doc__ else 'No description'}",
            value=name
        )
        for name, func in tool_functions.items()
    ]


    task_choice = questionary.select(
        "",
        choices=choices,
        style=custom_style
    ).ask()

    if not task_choice:
        console.print("❌ No task selected. Exiting.", style="bold red")
        return

    selected_func = tool_functions[task_choice]

    # Get function parameters dynamically
    from inspect import signature

    params = signature(selected_func).parameters
    kwargs = {}

    for param_name, param in params.items():
        param_type = param.annotation if param.annotation != param.empty else str
        default_value = param.default if param.default != param.empty else None

        question_text = f"Enter value for '{param_name}'"
        if default_value is not None:
            question_text += f" (default: {default_value})"

        answer = questionary.text(
            question_text + ":",
            default=str(default_value) if default_value is not None else "",
            style=custom_style,
        ).ask()

        # If user leaves it blank, use default
        if not answer and default_value is not None:
            kwargs[param_name] = default_value
            continue

        # Convert the answer to the correct type
        try:
            if param_type == bool:
                answer = answer.lower() in ["yes", "y", "true", "1"]
            else:
                answer = param_type(answer)
            kwargs[param_name] = answer
        except ValueError:
            console.print(f"❌ Invalid input for parameter '{param_name}'. Expected {param_type.__name__}.", style="bold red")
            return  # Exit early on invalid input


    from rich.progress import Progress, SpinnerColumn, TextColumn

    console.print(f"\n🚀 [bold cyan]Running task:[/bold cyan] [green]{task_choice}[/green]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Working on it...", total=None)
        selected_func(**kwargs)

    console.print("\n✅ [bold green]Task completed successfully![/bold green] 🚀\n")


