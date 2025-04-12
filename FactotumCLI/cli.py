import argparse
import importlib
import pkgutil
from pathlib import Path
from rich.console import Console

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
    parser.add_argument("--task", required=True, help="Task to perform")
    parser.add_argument("--length", type=int, help="Password length")
    parser.add_argument("--specials", type=str, help="Include special characters: y/n")
    parser.add_argument("--directory", type=str, help="Directory for file operations")
    parser.add_argument("--coin", type=str, help="Crypto coin ID")
    parser.add_argument("--url", type=str, help="URL of the web page")
    parser.add_argument("--output", type=str, help="Output filename")
    parser.add_argument("--tool", type=str, help="Specific tool to show help for")

    args = parser.parse_args()

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
