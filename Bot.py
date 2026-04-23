import Utils.Windows_Fix
import os
import discord
import asyncio
import logging
from discord.ext import commands
from dotenv import load_dotenv
from Utils.Logger import setup_logging
from Bot.Core import Ping, Help
from Bot.Games import Rps, Guess_The_Num, Number_Game
from Bot.Fun import Quotes, Random_Picker, Weather, Cat_Dog
from Bot.Utilities import Calculator, Bot_Talk, TextSearch, Reminder, Cafe
from Bot.Security import Password, EncryptDecrypt

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
    if ctx.guild is None:
        await ctx.send("❌ Commands cannot be used in DMs!")
        return False

    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
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
    else:
        logging.error(f"Unexpected error: {error}")
        raise error


@bot.event
async def on_member_join(member):
    try:
        await member.send(
            f"Welcome {member.mention}, Welcome to ✧ Meta Competition ✧!\nPlease make sure to check <#1454850144943083562> and <#1454885928983204056>\nHave Fun!"
        )
    except:
        pass


@bot.event
async def on_ready():
    CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL"))
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"{bot.user} Is Ready To Go")
        logging.info(f"{bot.user} has connected to Discord!")
    else:
        logging.error("Could not find the channel to send the ready message.")


# Core
Ping.setup(bot)
Help.setup(bot)

# Games
Rps.setup(bot)
Guess_The_Num.setup(bot)
Number_Game.setup(bot)

# Fun
Quotes.setup(bot)
Random_Picker.setup(bot)
Weather.setup(bot)
Cat_Dog.setup(bot)

# Utilities
Calculator.setup(bot)
Bot_Talk.setup(bot)
TextSearch.setup(bot)
Reminder.setup(bot)
Cafe.setup(bot)

# Security
Password.setup(bot)
EncryptDecrypt.setup(bot)

bot.run(TOKEN)
