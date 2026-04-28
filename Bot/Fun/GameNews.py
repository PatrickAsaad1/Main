# Bot/Fun/GameNews.py
import os
import requests
from discord.ext import tasks
from Utils.Logger import setup_logging
from Utils.Config import get_game_news_channel
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

logging = setup_logging()


@tasks.loop(hours=3)
async def send_game_news():
    if not NEWS_API_KEY:
        logging.error("News API key not found")
        return

    try:
        news_url = f"https://newsapi.org/v2/everything?q=gaming&apiKey={NEWS_API_KEY}"
        response = requests.get(news_url)
        articles = response.json().get("articles", [])[:5]

        if not articles:
            return

        headlines = [a["title"] for a in articles]
        headlines_text = "\n".join(headlines)

        ai_prompt = f"Summarize these gaming news headlines into a short, exciting update:\n{headlines_text}"
        ai_response = requests.post(
            "https://text.pollinations.ai/",
            json={"messages": [{"role": "user", "content": ai_prompt}]},
        )
        news = ai_response.text[:1900]

        for guild in send_game_news.bot.guilds:
            channel_id = get_game_news_channel(guild.id)
            if channel_id:
                channel = guild.get_channel(channel_id)
                if channel and channel.permissions_for(guild.me).send_messages:
                    await channel.send(f"🎮 **Gaming News Update**\n\n{news}")

        logging.info("Game news sent successfully")

    except Exception as e:
        logging.error(f"Game news error: {e}")


@send_game_news.before_loop
async def before_game_news():
    await send_game_news.bot.wait_until_ready()


def setup(bot):
    send_game_news.bot = bot
    send_game_news.start()
