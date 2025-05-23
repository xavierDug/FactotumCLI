from rich.console import Console
from ..logger import log_task

CATEGORY = "File Management"
DESCRIPTION = "Download a webpage and save it locally."

console = Console()

# Function to download a webpage
def download_webpage(url: str, output: str = "downloaded_page.html"):
    """
    Download a webpage and save it locally.

    Args:
        url (str): The URL of the webpage to download.
        output_file (str): The name of the output HTML file. Defaults to 'downloaded_page.html'.

    Example:
        factotum --task download-webpage --url https://example.com --output example.html

    Description:
        Downloads the HTML content of the given webpage and saves it to a local file.
        Useful for offline reading, backups, or basic web archiving.
    """
    
    import requests
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(output, 'w', encoding='utf-8') as file:
            file.write(response.text)

        console.print(f"✅ Webpage downloaded successfully: {output}", style="bold green")
        log_task(f"Webpage downloaded: {url} -> {output}")

    except requests.RequestException as e:
        console.print(f"❌ Error downloading webpage: {e}", style="bold red")
        log_task(f"Error downloading webpage: {e}")