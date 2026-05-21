import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Import Modules
from Bot.Core import Admin, Help, Ping
from Bot.Fun import (
    Advice,
    Cat_Dog,
    CoinFlip,
    GameNews,
    HourlyPets,
    Joke,
    Lyrics,
    MCTiers,
    Meme,
    Music,
    Quotes,
    Random_Picker,
    RapNews,
    Roll,
    Weather,
)
from Bot.Games import Guess_The_Num, Number_Game, Rps
from Bot.Security import EncryptDecrypt, Password
from Bot.Utilities import (
    Bot_Talk,
    Cafe,
    Calculator,
    Groq,
    Morse,
    QR,
    Reminder,
    ServerInfo,
    SetChannel,
    TextSearch,
)
from Utils.Config import get_allowed_channels
from Utils.Logger import setup_logging
import Utils.Windows_Fix

setup_logging()
logging = setup_logging()  # FIXED: Added missing local reference for logging

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize Bot
bot = commands.Bot(command_prefix="!", intents=intents)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# ==========================================
# ASYNC PRE-START EXTENSION LOADING
# ==========================================
async def load_extensions():
    # Core
    Ping.setup(bot)
    Help.setup(bot)
    Admin.setup(bot)

    # Games
    Rps.setup(bot)
    Guess_The_Num.setup(bot)
    Number_Game.setup(bot)

    # Fun
    Quotes.setup(bot)
    Random_Picker.setup(bot)
    Weather.setup(bot)
    Cat_Dog.setup(bot)
    CoinFlip.setup(bot)
    Roll.setup(bot)
    Joke.setup(bot)
    Meme.setup(bot)
    Lyrics.setup(bot)
    Advice.setup(bot)
    MCTiers.setup(bot)
    Music.setup(bot)

    # Utilities
    Calculator.setup(bot)
    Bot_Talk.setup(bot)
    TextSearch.setup(bot)
    Reminder.setup(bot)
    Cafe.setup(bot)
    SetChannel.setup(bot)
    ServerInfo.setup(bot)
    QR.setup(bot)
    Morse.setup(bot)
    Groq.setup(bot)

    # Security
    Password.setup(bot)
    EncryptDecrypt.setup(bot)


@bot.check
async def check_all(ctx):
    """Block DMs and restrict prefix commands to set channels."""
    if ctx.guild is None:
        await ctx.send("❌ Commands cannot be used in DMs!")
        return False

    allowed_channels = get_allowed_channels(ctx.guild.id)
    if allowed_channels and ctx.channel.id not in allowed_channels:
        await ctx.send("❌ You cannot use commands here!")
        return False

    return True


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        logging.info(f"{ctx.author} tried to use command in wrong channel")
        return
    elif isinstance(error, commands.CommandNotFound):
        logging.info(f"{ctx.author} tried unknown command: {ctx.message.content}")
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        return
    else:
        logging.error(f"Unexpected error: {error}")
        raise error


@bot.event
async def on_member_join(member):
    try:
        await member.send(
            f"Welcome {member.mention}, Welcome to ✧ Meta Competition ✧!\n"
            f"Please make sure to check <#1454850144943083562> and <#1454885928983204056>\n"
            f"Have Fun!"
        )
    except Exception:
        pass


@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    logging.info(f"{bot.user} has connected to Discord!")
    await bot.user.edit(username="TripleT")

    # FORCE SLASH COMMAND TREES SYNC DIRECTLY ONCE READY
    try:
        print("🔄 Syncing slash commands globally...")
        synced = await bot.tree.sync()
        print(f"✨ Successfully synced {len(synced)} slash commands globally!")
    except Exception as e:
        logging.error(f"Failed to sync command tree: {e}")
        print(f"❌ Failed to sync slash commands: {e}")

    await bot.change_presence(activity=discord.Game(name="Made with Python 🐍"))

    # Start Background Loop Tasks Safely
    HourlyPets.send_pet_pic.bot = bot
    if (
        not HourlyPets.send_pet_pic.is_running()
    ):  # FIXED: Added check to prevent duplicate start
        HourlyPets.send_pet_pic.start()
    RapNews.send_rap_news.bot = bot
    if (
        not RapNews.send_rap_news.is_running()
    ):  # FIXED: Added check to prevent duplicate start
        RapNews.send_rap_news.start()
    GameNews.send_game_news.bot = bot
    if (
        not GameNews.send_game_news.is_running()
    ):  # FIXED: Added check to prevent duplicate start
        GameNews.send_game_news.start()

    # Guild Join Messages
    for guild in bot.guilds:
        channel_ids = get_allowed_channels(guild.id)
        if channel_ids:
            for channel_id in channel_ids:
                channel = guild.get_channel(channel_id)
                if channel:
                    try:
                        await channel.send(f"{bot.user} Is Ready To Go")
                    except Exception:
                        continue
        else:
            for channel in guild.text_channels:
                permissions = channel.permissions_for(guild.me)
                if permissions.send_messages:
                    try:
                        await channel.send(
                            f"{bot.user} Is Ready To Go\n💡 Use `/setchannel` to set a specific channel!"  # FIXED: !setchannel → /setchannel
                        )
                        break
                    except Exception:
                        continue


# ==========================================
# MAIN RUNNER WITH ASYNC LOOP INJECTION
# ==========================================
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
