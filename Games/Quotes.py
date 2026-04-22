import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def run(name=None):
    """Loads a random quote from the ZenQuotes API."""
    try:
        response = requests.get("https://zenquotes.io/api/random")
        json_data = response.json()
        quote = f"💬 {json_data[0]['q']} — *{json_data[0]['a']}*"
        return quote
    except Exception as e:
        logging.error(f"Quote API error: {e}")
        return "❌ Could not fetch a quote right now. Try again later!"
