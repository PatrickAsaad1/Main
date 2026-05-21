import discord
import random
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(name="roll", description="Roll a six-sided die.")
    async def roll(interaction: discord.Interaction):
        logging.info(
            f"{interaction.user} used /roll command"
        )  # FIXED: changed !roll to /roll
        result = random.randint(1, 6)
        await interaction.response.send_message(f"🎲 You rolled a **{result}**!")
