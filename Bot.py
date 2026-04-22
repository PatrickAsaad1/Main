import Utils.Windows_Fix
import os
import discord
import time
import asyncio
import logging
from discord.ext import commands
from dotenv import load_dotenv
from Utils.Logger import setup_logging
from Bot import (
    Ping,
    Calculator,
    Rps,
    Guess_The_Num,
    Help,
    Number_Game,
    Bot_Talk,
    Quotes,
    Password,
    EncryptDecrypt,
)

setup_logging()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

ALLOWED_CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID", 0))


@bot.check
async def globally_block_dms(ctx):
    """Block all commands from DMs and only allow specific channel."""
    if ctx.guild is None:
        await ctx.send("❌ Commands cannot be used in DMs!")
        return False

    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send("❌ You cannot use commands here!")
        return False

    return True


@bot.event
async def on_command_error(ctx, error):
    """Stop CheckFailure from spamming console."""
    if isinstance(error, commands.CheckFailure):
        return
    raise error


@bot.event
async def on_member_join(member):
    try:
        await member.send(
            f"Hello {member.mention}, Welcome to ✧ Meta Competition ✧! Have Fun!"
        )
    except:
        pass  # If DMs are closed, just ignore


@bot.event
async def on_ready():
    CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL"))
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"{bot.user} Is Ready To Go")
        logging.info(f"{bot.user} has connected to Discord!")
    else:
        logging.error("Could not find the channel to send the ready message.")


Ping.setup(bot)
Calculator.setup(bot)
Rps.setup(bot)
Guess_The_Num.setup(bot)
Help.setup(bot)
Number_Game.setup(bot)
Bot_Talk.setup(bot)
Quotes.setup(bot)
Password.setup(bot)
EncryptDecrypt.setup(bot)

bot.run(TOKEN)
