# Bot/Utilities/QR.py
import requests
from Utils.Logger import setup_logging
import asyncio

logging = setup_logging()


def setup(bot):
    @bot.command(name="qr", aliases=["Qr", "QR", "qrcode"])
    async def qr(ctx):
        logging.info(f"{ctx.author} chose to generate a QR code")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            await ctx.send("What text or URL do you want to generate a QR code for?")
            text = await bot.wait_for("message", timeout=30.0, check=check)

            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text.content}"
            await ctx.send(qr_url)
            logging.info(f"QR code generated for: {text.content}")

        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Cancelled.")
