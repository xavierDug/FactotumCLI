from rich.console import Console
from ..logger import log_task

console = Console()

# Function to organize files in a directory by their extensions
def organize_files(directory):
    """
    Organize files in a directory by their extensions.

    Args:
        directory (str): Path to the directory to organize.

    Example:
        factotum --task organize-files --directory ./downloads

    Description:
        Scans the given folder and moves files into subfolders based on their file extensions.
        For example, .jpg files go into an 'jpg/' folder, .pdf files into 'pdf/', etc.
        Helps keep your directories clean and organized automatically.
    """
    
    from pathlib import Path
    import shutil

    path = Path(directory)
    if not path.exists():
        print(f"Directory '{directory}' does not exist.")
        return

    for file in path.iterdir():
        if file.is_file():
            ext = file.suffix.lower()[1:] or "no_extension"
            folder = path / ext
            folder.mkdir(exist_ok=True)
            shutil.move(str(file), str(folder / file.name))
            console.print(f"✅ Moved {file.name} to {folder}/", style="bold green")
            log_task(f"Moved {file.name} to {folder}/")