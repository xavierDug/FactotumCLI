from rich.console import Console
from ..logger import log_task

console = Console()

# Function to generate a random password
def generate_password(length=12, specials=False):
    """
    Generate a secure random password.

    Args:
        length (int): The desired length of the password. Defaults to 12.
        specials (bool): Include special characters (like !@#). Use 'y' for yes. Defaults to False.

    Example:
        factotum --task generate-password --length 16 --specials y

    Description:
        Creates a random password containing uppercase and lowercase letters,
        numbers, and optionally special characters for extra security.
    """

    import random
    import string

    characters = string.ascii_letters + string.digits
    if specials:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    message = f"Generated password: {password}"
    console.print(f"✅ {message}", style="bold green")
    log_task(message)