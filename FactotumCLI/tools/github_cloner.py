import requests
from git import Repo
from rich.console import Console
from rich.progress import track
import questionary
from dotenv import load_dotenv
import os
import time
from FactotumCLI.logger import log_task  # adjust import based on your structure

console = Console()

# Load environment variables from .env file
load_dotenv()

# Later, use:
token = os.getenv("GITHUB_TOKEN", "")

def github_repo_cloner(username: str, token: str = "", output_dir: str = "cloned_repos", progress=None):
    """
    Clone multiple GitHub repositories from a user.

    Args:
        username (str): GitHub username.
        token (str): Optional GitHub Personal Access Token (for private repos).
        output_dir (str): Directory to clone repositories into.
    """

    # Use token from environment if not provided
    if not token:
        token = os.getenv("GITHUB_TOKEN", "")

    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    url = "https://api.github.com/user/repos?per_page=100&type=all"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos = response.json()

        if not repos:
            console.print("❌ No repositories found.", style="bold red")
            return

        console.print("\n[bold cyan]Use ↑ ↓ arrows to navigate, spacebar to select, and enter to confirm.[/bold cyan]\n")

        # Interactive checkbox list
        repo_choices = [questionary.Choice(repo["name"], value=repo["clone_url"]) for repo in repos]
        selected_repos = questionary.checkbox(
            "🧩 Select repositories to clone:",
            choices=repo_choices,
        ).ask()

        if not selected_repos:
            console.print("❌ No repositories selected. Exiting.", style="bold red")
            return

        os.makedirs(output_dir, exist_ok=True)

        # Track stats
        success_count = 0
        skip_count = 0
        fail_count = 0

        # Track time
        start_time = time.time()

        # Clone with progress
        task = progress.add_task(description="🚀 Cloning repositories...", total=len(selected_repos))

        for repo_url in selected_repos:
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            destination = os.path.join(output_dir, repo_name)

            if os.path.exists(destination):
                console.print(f"⚠️ Repository '{repo_name}' already exists. Skipping.", style="yellow")
                skip_count += 1
                progress.advance(task)
                continue

            try:
                Repo.clone_from(repo_url, destination)
                console.print(f"✅ Cloned '{repo_name}' successfully!", style="bold green")
                success_count += 1
            except Exception as e:
                console.print(f"❌ Failed to clone '{repo_name}': {e}", style="bold red")
                fail_count += 1

            progress.advance(task)

        progress.remove_task(task)

        end_time = time.time()
        elapsed_time = end_time - start_time

        console.print("\n[bold cyan]📊 Clone Summary:[/bold cyan]")
        console.print(f"✅ Successful clones: [bold green]{success_count}[/bold green]")
        console.print(f"⚠️ Skipped (already exists): [bold yellow]{skip_count}[/bold yellow]")
        console.print(f"❌ Failed clones: [bold red]{fail_count}[/bold red]")
        console.print(f"🕒 Total time: [bold magenta]{elapsed_time:.2f}[/bold magenta] seconds\n")

        summary_message = (
            f"📊 Clone Summary: "
            f"✅ {success_count} successful, "
            f"⚠️ {skip_count} skipped, "
            f"❌ {fail_count} failed, "
            f"🕒 {elapsed_time:.2f} seconds."
        )
        log_task(summary_message)



    except requests.RequestException as e:
        console.print(f"❌ Error fetching repositories: {e}", style="bold red")
