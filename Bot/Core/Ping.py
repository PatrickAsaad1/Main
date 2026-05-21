# Bot/ping.py
import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.tree.command(name="ping", description="Check the bot's latency.")
    async def ping(interaction: discord.Interaction):
        logging.info(f"Ping command by: {interaction.user}")
        await interaction.response.send_message(
            f"🏓 Pong! {round(bot.latency * 1000)}ms"
        )
