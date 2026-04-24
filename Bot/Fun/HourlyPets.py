# Bot/Fun/HourlyPets.py
import requests
from discord.ext import tasks
from Utils.Logger import setup_logging

logging = setup_logging()

send_cat = True  # Start with cat


@tasks.loop(hours=1)
async def send_pet_pic():
    global send_cat

    try:
        if send_cat:
            response = requests.get(
                "https://api.thecatapi.com/v1/images/search", timeout=30.0
            )
            data = response.json()
            url = data[0]["url"]
            emoji = "🐱"
            send_cat = False
        else:
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            data = response.json()
            url = data["message"]
            emoji = "🐶"
            send_cat = True

        # Send to the first available channel
        for guild in send_pet_pic.bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(f"{emoji} **Hourly Pet Picture!**\n{url}")
                    break

        logging.info(f"Hourly pet sent: {'cat' if not send_cat else 'dog'}")
    except Exception as e:
        logging.error(f"Hourly pet error: {e}")


@send_pet_pic.before_loop
async def before_send():
    await send_pet_pic.bot.wait_until_ready()


def setup(bot):
    send_pet_pic.bot = bot
    send_pet_pic.start()
