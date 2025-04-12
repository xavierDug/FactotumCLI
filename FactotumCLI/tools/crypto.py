from rich.console import Console
from ..logger import log_task

console = Console()

# Function to check the current price of a cryptocurrency
def check_crypto_price(coin: str = "bitcoin"):
    """
    Check the current price of a cryptocurrency (in CAD).

    Args:
        coin (str): The coin ID to check. Defaults to 'bitcoin'.

    Example:
        factotum --task check-crypto-price --coin ethereum

    Description:
        Fetches real-time cryptocurrency prices using the CoinGecko API.
        Displays the current price in Canadian Dollars (CAD).
        Supports any coin ID recognized by CoinGecko (e.g., 'bitcoin', 'ethereum', 'dogecoin').
    """
    
    import requests

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=cad"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if coin in data:
            price = data[coin]['cad']
            message = f"The current price of {coin.capitalize()} is: ${price:.2f} CAD"
            console.print(f"💰 {message}", style="bold green")
            log_task(message)
        else:
            console.print(f"⚠️ Coin '{coin}' not found. Please check the coin ID.", style="bold yellow")
            log_task(f"Coin '{coin}' not found.")
    except requests.RequestException as e:
        console.print(f"❌ Error fetching price: {e}", style="bold red")
        log_task(f"Error fetching price: {e}")