import discord
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(name="quote", description="Get a random inspirational quote.")
    async def quote(interaction: discord.Interaction):
        """Loads a random quote from the ZenQuotes API."""
        try:
            response = requests.get("https://zenquotes.io/api/random")
            json_data = response.json()
            await interaction.response.send_message(
                f"✨ {json_data[0]['q']} — *{json_data[0]['a']}*"
            )

            logging.info(
                f"{interaction.user} used /quote and got: {json_data[0]['q'][:50]}..."  # FIXED: changed !quote to /quote
            )

        except Exception as e:
            logging.error(f"Quote API error: {e}")
            await interaction.response.send_message(
                "❌ Could not fetch a quote right now. Try again later!"
            )
