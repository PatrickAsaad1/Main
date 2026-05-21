import discord
import random
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="coinflip",
        description="Flip a coin and get heads or tails.",
    )
    async def coinflip(interaction: discord.Interaction):
        """Flip a coin and get heads or tails."""
        coin = random.choice(["Heads", "Tails"])
        logging.info(f"{interaction.user} flipped a coin: {coin}")
        await interaction.response.send_message(f"🪙 The coin landed on **{coin}**!")
