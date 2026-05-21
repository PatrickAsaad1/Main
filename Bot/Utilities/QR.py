import discord
import requests  # FIXED: Added missing import
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="qr", description="Generate a QR code from the provided text."
    )
    async def qr(interaction: discord.Interaction, text: str):
        logging.info(f"{interaction.user} chose to generate a QR code")

        # URL-encode the string to handle spaces and special characters cleanly
        encoded_text = requests.utils.quote(text)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded_text}"

        await interaction.response.send_message(qr_url)
        logging.info(f"QR code generated for: {text}")
