import argparse
import importlib
import pkgutil
from pathlib import Path
from rich.console import Console
import questionary
from questionary import Style
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from FactotumCLI.config import custom_style
from collections import defaultdict

__version__ = "0.1.0"

console = Console()

# Dynamic import of all tools
from . import tools

tool_functions = {}

# Discover and import all tool modules
tool_functions = {}
tool_metadata = {}  # New: metadata storage

for loader, module_name, is_pkg in pkgutil.iter_modules(tools.__path__):
    module = importlib.import_module(f"{tools.__name__}.{module_name}")
    category = getattr(module, "CATEGORY", "Other")
    description = getattr(module, "DESCRIPTION", "No description provided.")

    for attr in dir(module):
        if not attr.startswith("_") and callable(getattr(module, attr)):
            cli_name = attr.replace("_", "-")
            tool_functions[cli_name] = getattr(module, attr)
            tool_metadata[cli_name] = {
                "category": category,
                "description": description
            }

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
    splash_text.append(f"FactotumCLI v{__version__}", style="bold magenta")
    splash_text.append(" 🎩\n", style="bold")
    splash_text.append("Your personal terminal assistant.\n", style="bold cyan")

    console.print(Panel(splash_text, style="bold blue"))

    while True:
        console.print("\n[bold cyan]🧩 Choose a task from the menu below:[/bold cyan]\n")

        # Group functions by category
        grouped_tools = defaultdict(list)
        for name, meta in tool_metadata.items():
            grouped_tools[meta["category"]].append(name)

        choices = []

        for category, tools_in_category in grouped_tools.items():
            choices.append(questionary.Separator(f"📂 {category}"))
            for name in tools_in_category:
                description = tool_metadata[name]["description"]
                choices.append(
                    questionary.Choice(
                        title=f"{name} — {description}",
                        value=name
                    )
                )

        choices.append(questionary.Choice(title="❌ Exit", value="exit"))

        task_choice = questionary.select(
            "",
            choices=choices,
            style=custom_style
        ).ask()

        if task_choice == "exit" or task_choice is None:
            graceful_exit(console)
            break

        selected_func = tool_functions[task_choice]

        from inspect import signature

        params = signature(selected_func).parameters
        kwargs = {}

        internal_params = {"progress"}

        for param_name, param in params.items():
            if param_name in internal_params:
                continue  # Skip internal-use parameters

            param_type = param.annotation if param.annotation != param.empty else str
            default_value = param.default if param.default != param.empty else None

            question_text = f"Enter value for '{param_name}'"
            if default_value is not None:
                question_text += f" (default: {default_value})"

            answer = questionary.text(
                question_text + ":",
                default=str(default_value) if default_value is not None else "",
                style=custom_style
            ).ask()

            if not answer and default_value is not None:
                kwargs[param_name] = default_value
                continue

            try:
                if param_type == bool:
                    answer = answer.lower() in ["yes", "y", "true", "1"]
                else:
                    answer = param_type(answer)
                kwargs[param_name] = answer
            except ValueError:
                console.print(f"❌ Invalid input for parameter '{param_name}'. Expected {param_type.__name__}.", style="bold red")
                return

        # Progress bar wrapper
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Working on it...", total=None)
            # Pass progress to the function
            kwargs["progress"] = progress
            from inspect import signature
            sig = signature(selected_func)
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}

            selected_func(**filtered_kwargs)


        console.print("\n✅ [bold green]Task completed successfully![/bold green] 🚀\n")

        # Ask to run another task
        another = questionary.confirm("Would you like to run another task?", style=custom_style).ask()
        if not another:
            graceful_exit(console)
            break


def graceful_exit(console):
    console.print("\n[bold magenta]Thank you for using FactotumCLI! Goodbye! 👋[/bold magenta]\n")
