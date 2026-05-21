import discord
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="joke",
        description="Get a random dad joke.",
    )
    async def joke(interaction: discord.Interaction):
        logging.info(
            f"{interaction.user} used /joke command"
        )  # FIXED: changed !joke to /joke
        try:
            headers = {"Accept": "application/json"}
            response = requests.get("https://icanhazdadjoke.com/", headers=headers)
            json_data = response.json()
            await interaction.response.send_message(f"😂 **{json_data['joke']}**")
            logging.info("Joke sent successfully")
        except:
            await interaction.response.send_message(
                "❌ Couldn't fetch a joke right now. Try again later!"
            )
            logging.error("Joke API error")
