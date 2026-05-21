import discord
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(name="advice", description="Get a random piece of advice.")
    async def advice(interaction: discord.Interaction):
        """Get a random piece of advice."""
        try:
            response = requests.get("https://api.adviceslip.com/advice")
            json_data = response.json()
            advice_text = json_data["slip"]["advice"]
            await interaction.response.send_message(f"💡 **{advice_text}**")
            logging.info(
                f"{interaction.user} used /advice and got: {advice_text}"
            )  # FIXED: changed !advice to /advice
        except Exception as e:
            logging.error(f"Advice API error: {e}")
            await interaction.response.send_message(
                "❌ Could not fetch advice right now. Try again later!"
            )
