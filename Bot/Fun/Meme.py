import discord
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(name="meme", description="Get a random meme.")
    async def meme(interaction: discord.Interaction):
        logging.info(
            f"{interaction.user} used /meme command"
        )  # FIXED: changed !meme to /meme
        try:
            response = requests.get("https://meme-api.com/gimme")
            json_data = response.json()
            await interaction.response.send_message(json_data["url"])
            logging.info(f"Meme sent from r/{json_data['subreddit']}")
        except Exception as e:
            logging.error(f"Meme API error: {e}")
            await interaction.response.send_message(
                "❌ Could not fetch a meme right now. Try again later!"
            )
