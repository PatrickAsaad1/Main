# Bot/Fun/RapNews.py
import os
import requests
from discord.ext import tasks
from Utils.Logger import setup_logging
from Utils.Config import get_rap_news_channel
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

logging = setup_logging()


@tasks.loop(hours=3)
async def send_rap_news():
    if not NEWS_API_KEY:
        logging.error("News API key not found")
        return

    try:
        news_url = (
            f"https://newsapi.org/v2/top-headlines?country=eg&apiKey={NEWS_API_KEY}"
        )
        response = requests.get(news_url)
        articles = response.json().get("articles", [])[:5]

        if not articles:
            return

        headlines = [a["title"] for a in articles]
        headlines_text = "\n".join(headlines)

        ai_prompt = (
            f"Turn these news headlines into a short rap verse:\n{headlines_text}"
        )
        ai_response = requests.post(
            "https://text.pollinations.ai/",
            json={"messages": [{"role": "user", "content": ai_prompt}]},
        )
        rap = ai_response.text[:1900]

        for guild in send_rap_news.bot.guilds:
            channel_id = get_rap_news_channel(guild.id)
            if channel_id:
                channel = guild.get_channel(channel_id)
                if channel and channel.permissions_for(guild.me).send_messages:
                    await channel.send(f"🎤 **Rap News Update**\n\n{rap}")

        logging.info("Rap news sent successfully")

    except Exception as e:
        logging.error(f"Rap news error: {e}")


@send_rap_news.before_loop
async def before_rap_news():
    await send_rap_news.bot.wait_until_ready()


def setup(bot):
    send_rap_news.bot = bot
    send_rap_news.start()
