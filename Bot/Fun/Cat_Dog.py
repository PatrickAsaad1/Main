import discord
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(name="cat", description="Get a random cat picture.")
    async def Cat(interaction: discord.Interaction):
        logging.info(
            f"{interaction.user} used /cat command"
        )  # FIXED: changed !cat to /cat
        try:
            response = requests.get(
                "https://api.thecatapi.com/v1/images/search", timeout=30.0
            )
            data = response.json()
            await interaction.response.send_message(data[0]["url"])
            logging.info(f"Cat pic was sent to {interaction.user}")
        except:
            await interaction.response.send_message(
                "Couldn't get a cat pic, try again later!"
            )
            logging.error("Cat API error")

    @bot.tree.command(name="dog", description="Get a random dog picture.")
    async def Dog(interaction: discord.Interaction):
        logging.info(
            f"{interaction.user} used /dog command"
        )  # FIXED: changed !dog to /dog
        try:
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            data = response.json()
            await interaction.response.send_message(data["message"])
            logging.info(f"Dog pic was sent to {interaction.user}")
        except:
            await interaction.response.send_message(
                "Couldn't get a dog pic, try again later!"
            )
            logging.error("Dog API error")
