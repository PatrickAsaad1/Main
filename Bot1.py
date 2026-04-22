# ============================================
# INSANE DISCORD BOT - EVERYTHING IN ONE FILE
# ============================================

import os
import sys
import io
import json
import random
import asyncio
import logging
import string
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ============================================
# WINDOWS UTF-8 FIX
# ============================================
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# ============================================
# LOGGER SETUP
# ============================================
def setup_logging():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, "bot.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger()


logger = setup_logging()

# ============================================
# BOT SETUP
# ============================================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID", 0))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ============================================
# GLOBAL CHANNEL CHECK
# ============================================
@bot.check
async def globally_block_dms(ctx):
    """Block commands from DMs and restrict to specific channel."""
    if ctx.guild is None:
        await ctx.send("❌ Commands cannot be used in DMs!")
        return False

    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send("❌ You cannot use commands here!")
        return False

    return True


# ============================================
# ERROR HANDLER
# ============================================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CheckFailure):
        return
    else:
        logger.error(f"Command error: {error}")


# ============================================
# EVENTS
# ============================================
@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord!")
    print(f"✅ {bot.user} is online!")

    channel_id = int(os.getenv("DISCORD_CHANNEL", 0))
    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send("I Am Ready!")
            await asyncio.sleep(1)
            await channel.send("I hope you enjoy the games! Type `!help` for commands.")


@bot.event
async def on_member_join(member):
    try:
        await member.send(
            f"Hello {member.mention}, Welcome to ✧ Meta Competition ✧! Have Fun!"
        )
    except:
        pass


# ============================================
# PING COMMAND
# ============================================
@bot.command(name="ping")
async def ping(ctx):
    logger.info(f"Ping command by: {ctx.author}")
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")


# ============================================
# CALCULATOR COMMAND
# ============================================
@bot.command(name="calc", aliases=["Calc", "CALC", "calculate", "Calculate"])
async def calc(ctx, *, expression: str = None):
    logger.info(f"Calc by {ctx.author}: {expression}")

    if not expression:
        await ctx.send("❌ Usage: `!calc 5 + 3` or `!calc 5+3`")
        return

    expression = expression.replace("x", "*").replace("×", "*").replace("÷", "/")

    if " " not in expression:
        for op in ["+", "-", "*", "/"]:
            if op in expression:
                parts = expression.split(op)
                if len(parts) == 2:
                    try:
                        num1 = float(parts[0])
                        num2 = float(parts[1])
                    except ValueError:
                        await ctx.send("❌ Invalid numbers!")
                        return

                    if op == "+":
                        result = num1 + num2
                    elif op == "-":
                        result = num1 - num2
                    elif op == "*":
                        result = num1 * num2
                    elif op == "/":
                        if num2 == 0:
                            await ctx.send("❌ Can't divide by zero!")
                            return
                        result = num1 / num2

                    await ctx.send(f"🧮 {expression} = {result}")
                    return
        await ctx.send("❌ Invalid format!")
        return

    parts = expression.split()
    if len(parts) < 3 or len(parts) % 2 == 0:
        await ctx.send("❌ Invalid format! Example: `!calc 5 + 3 + 2`")
        return

    for i in range(1, len(parts), 2):
        if parts[i] not in ["+", "-", "*", "/"]:
            await ctx.send(f"❌ Invalid operator: {parts[i]}")
            return

    try:
        result = float(parts[0])
        for i in range(1, len(parts), 2):
            op = parts[i]
            num = float(parts[i + 1])

            if op == "+":
                result += num
            elif op == "-":
                result -= num
            elif op == "*":
                result *= num
            elif op == "/":
                if num == 0:
                    await ctx.send("❌ Can't divide by zero!")
                    return
                result /= num

        await ctx.send(f"🧮 {expression} = {result}")
    except ValueError:
        await ctx.send("❌ Invalid numbers!")


# ============================================
# RPS COMMAND
# ============================================
@bot.command(name="rps", aliases=["Rps", "RPS"])
async def rps(ctx):
    logger.info(f"RPS game started by: {ctx.author}")

    await ctx.send("👥 Do you want to play with a friend? (yes/no)")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        play_with_friend = msg.content.lower() in ["yes", "y"]
    except asyncio.TimeoutError:
        await ctx.send("⏰ Time's up! Starting solo game...")
        play_with_friend = False

    if play_with_friend:
        await ctx.send("👤 Mention the friend you want to play with! (e.g., `@Friend`)")
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.mentions:
                opponent = msg.mentions[0]
                if opponent == ctx.author:
                    await ctx.send("❌ You can't play against yourself!")
                    return
                if opponent.bot:
                    await ctx.send(
                        "❌ You can't play against a bot! Use solo mode instead."
                    )
                    return
                await multiplayer_rps(ctx, opponent)
            else:
                await ctx.send("❌ No user mentioned! Starting solo game...")
                await solo_rps(ctx)
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Starting solo game...")
            await solo_rps(ctx)
    else:
        await solo_rps(ctx)


async def solo_rps(ctx):
    choices = ["rock", "paper", "scissors"]
    player_score = 0
    computer_score = 0

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send(
        "🎮 **Rock Paper Scissors** - First to 3 wins!\nType `rock`, `paper`, or `scissors`. Type `quit` to stop."
    )

    while player_score < 3 and computer_score < 3:
        await ctx.send(
            f"🏆 Score: You **{player_score}** | Computer **{computer_score}**\n🎯 Your choice (`rock`/`paper`/`scissors`):"
        )

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            choice = msg.content.lower()

            if choice == "quit":
                await ctx.send("👋 Game cancelled!")
                return
            if choice not in choices:
                await ctx.send("❌ Invalid! Choose: `rock`, `paper`, or `scissors`")
                continue

            computer = random.choice(choices)

            if choice == computer:
                result = "😐 Tie!"
            elif (
                (choice == "rock" and computer == "scissors")
                or (choice == "paper" and computer == "rock")
                or (choice == "scissors" and computer == "paper")
            ):
                result = "✅ You win this round!"
                player_score += 1
            else:
                result = "❌ Computer wins this round!"
                computer_score += 1

            await ctx.send(f"🤖 Computer chose: **{computer}**\n{result}")
            await asyncio.sleep(1)

        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Game cancelled.")
            return

    if player_score == 3:
        await ctx.send(f"\n🎉🎉🎉 **YOU WIN!** {player_score}-{computer_score} 🎉🎉🎉")
    else:
        await ctx.send(f"\n💻 **COMPUTER WINS!** {computer_score}-{player_score} 💻")

    logger.info(
        f"RPS game ended: {ctx.author} - Final score {player_score}-{computer_score}"
    )
    await ask_play_again(ctx, solo_rps)


async def multiplayer_rps(ctx, opponent):
    choices = ["rock", "paper", "scissors"]
    player1 = ctx.author
    player2 = opponent
    player1_score = 0
    player2_score = 0

    await ctx.send(
        f"🎮 **{player1.display_name} vs {player2.display_name}** - First to 3 wins!"
    )
    await ctx.send(f"{player2.mention}, do you accept the challenge? (yes/no)")

    def check_opponent(m):
        return m.author == player2 and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check_opponent)
        if msg.content.lower() not in ["yes", "y"]:
            await ctx.send(f"❌ {player2.display_name} declined. Game cancelled.")
            return
    except asyncio.TimeoutError:
        await ctx.send(f"⏰ {player2.display_name} didn't respond. Game cancelled.")
        return

    await ctx.send(
        f"✅ Challenge accepted! **{player1.display_name} vs {player2.display_name}**"
    )
    await ctx.send("📩 Game updates will be sent to your DMs!")

    await player1.send(
        f"🎮 **RPS Game: You vs {player2.display_name}**\nFirst to 3 wins!\n"
    )
    await player2.send(
        f"🎮 **RPS Game: You vs {player1.display_name}**\nFirst to 3 wins!\n"
    )

    while player1_score < 3 and player2_score < 3:
        player1_choice = await get_choice_dm(player1, choices)
        if player1_choice is None:
            await ctx.send(f"❌ {player1.mention} took too long. Game cancelled.")
            return

        player2_choice = await get_choice_dm(player2, choices)
        if player2_choice is None:
            await ctx.send(f"❌ {player2.mention} took too long. Game cancelled.")
            return

        if player1_choice == player2_choice:
            result = "😐 Tie!"
        elif (
            (player1_choice == "rock" and player2_choice == "scissors")
            or (player1_choice == "paper" and player2_choice == "rock")
            or (player1_choice == "scissors" and player2_choice == "paper")
        ):
            result = f"✅ {player1.display_name} wins this round!"
            player1_score += 1
        else:
            result = f"✅ {player2.display_name} wins this round!"
            player2_score += 1

        round_msg = f"""
**Round Result:**
{player1.display_name} chose **{player1_choice}**
{player2.display_name} chose **{player2_choice}**
{result}
🏆 Score: {player1.display_name} **{player1_score}** | {player2.display_name} **{player2_score}**
"""
        await player1.send(round_msg)
        await player2.send(round_msg)
        await asyncio.sleep(1)

    if player1_score == 3:
        final_msg = f"\n🎉🎉🎉 **{player1.display_name} WINS THE GAME!** {player1_score}-{player2_score} 🎉🎉🎉"
    else:
        final_msg = f"\n🎉🎉🎉 **{player2.display_name} WINS THE GAME!** {player2_score}-{player1_score} 🎉🎉🎉"

    await ctx.send(final_msg)
    await player1.send(f"**GAME OVER**\n{final_msg}")
    await player2.send(f"**GAME OVER**\n{final_msg}")

    logger.info(
        f"RPS Multiplayer ended: {player1.display_name} vs {player2.display_name} - {player1_score}-{player2_score}"
    )


async def get_choice_dm(player, choices):
    try:

        def check_dm(m):
            return m.author == player and isinstance(m.channel, discord.DMChannel)

        msg = await bot.wait_for("message", timeout=30.0, check=check_dm)
        choice = msg.content.lower()

        if choice in choices:
            await player.send(f"✅ You chose **{choice}**!")
            return choice
        else:
            await player.send("❌ Invalid choice! Randomly selecting...")
            return random.choice(choices)
    except asyncio.TimeoutError:
        await player.send("⏰ Time's up! Randomly selecting...")
        return random.choice(choices)


async def ask_play_again(ctx, game_func):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("\nPlay again? (yes/no)")
    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.lower() in ["yes", "y"]:
            await game_func(ctx)
        else:
            await ctx.send("Thanks for playing!")
    except asyncio.TimeoutError:
        await ctx.send("Thanks for playing!")


# ============================================
# GUESS THE NUMBER COMMAND
# ============================================
@bot.command(name="guess", aliases=["Guess", "GUESS"])
async def guess(ctx):
    logger.info(f"User {ctx.author} started Guess The Number game.")

    score = 0
    difficulty_ranges = {
        "easy": (1, 3),
        "med": (1, 5),
        "medium": (1, 5),
        "hard": (1, 10),
    }

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Choose difficulty: `easy`, `med`, or `hard`")

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        game = msg.content.lower()
    except asyncio.TimeoutError:
        await ctx.send("⏰ Time's up!")
        return

    if game == "quit":
        await ctx.send("👋 Game cancelled!")
        return

    if game not in difficulty_ranges:
        await ctx.send("❌ Invalid! Choose: easy, med, or hard")
        return

    low, high = difficulty_ranges[game]
    await ctx.send(f"Great! I'll pick a number between {low} and {high}")
    await ctx.send(f"Try to reach 3 points to win! Type `quit` to stop.")

    while score < 3:
        rnum = random.randint(low, high)
        await ctx.send(f"\n🎯 Guess a number ({low}-{high}):")

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            user_input = msg.content.lower()
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up!")
            return

        if user_input == "quit":
            await ctx.send("👋 Game cancelled!")
            return

        try:
            unum = int(user_input)
        except ValueError:
            await ctx.send("❌ Please enter a number!")
            continue

        if unum < low or unum > high:
            await ctx.send(f"❌ Enter a number between {low} and {high}!")
            continue

        await ctx.send(f"The number was: **{rnum}**")

        if unum == rnum:
            await ctx.send("✅ You got it right! +1 point!")
            score += 1
        else:
            await ctx.send("❌ Wrong guess!")
            if score > 0:
                score -= 1

        await ctx.send(f"📊 Your score: **{score}/3**")

    await ctx.send("🎉🎉🎉 **YOU WON! Reached 3 points!** 🎉🎉🎉")
    logger.info(f"User {ctx.author} won the guessing game!")

    await ctx.send("\nPlay again? (yes/no)")
    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.lower() in ["yes", "y"]:
            await guess(ctx)
        else:
            await ctx.send("Thanks for playing!")
    except asyncio.TimeoutError:
        await ctx.send("Thanks for playing!")


# ============================================
# NUMBER GAME COMMAND
# ============================================
@bot.command(name="number", aliases=["Number", "NUMBER", "num", "Num"])
async def number_game(ctx):
    logger.info(f"User {ctx.author} selected number game")

    secret = random.randint(1, 20)

    await ctx.send("🎲 I'm thinking of a number from 1-20. You have 5 attempts!")
    await asyncio.sleep(1)
    await ctx.send("Type `quit` to stop playing.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    attempts = 0

    while attempts < 5:
        await ctx.send(f"\n📊 Attempt {attempts + 1}/5\nWhat's your guess?")

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            uguess = msg.content.lower()
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Game cancelled.")
            return

        if uguess == "quit":
            await ctx.send("👋 Game cancelled!")
            return

        if not uguess.isdigit():
            await ctx.send("❌ Please enter a number between 1-20!")
            continue

        guess_num = int(uguess)

        if guess_num < 1 or guess_num > 20:
            await ctx.send("❌ Please enter a number between 1-20!")
            continue

        attempts += 1

        if guess_num < secret:
            await ctx.send("📈 Too low!")
        elif guess_num > secret:
            await ctx.send("📉 Too high!")
        else:
            await ctx.send(f"🎉 **YOU GOT IT!** The number was {secret}!")
            await ctx.send(f"You won in {attempts} attempt(s)!")
            break
    else:
        await ctx.send(f"💀 **Out of attempts!** The number was {secret}.")

    await ctx.send("\nPlay again? (yes/no)")
    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.lower() in ["yes", "y"]:
            await number_game(ctx)
        else:
            await ctx.send("Thanks for playing!")
    except asyncio.TimeoutError:
        await ctx.send("Thanks for playing!")


# ============================================
# PASSWORD GENERATOR COMMAND
# ============================================
@bot.command(name="passgen", aliases=["password", "genpass", "bgen"])
async def password_gen(ctx):
    logger.info(f"{ctx.author} selected password generator")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send(
        "🔢 How many passwords do you want to generate? (Max: 10, type `quit` to cancel)"
    )

    while True:
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() == "quit":
                await ctx.send("👋 Cancelled!")
                return

            if not msg.content.isdigit():
                await ctx.send("❌ Please enter a valid number! (Max: 10)")
                continue

            manypass = int(msg.content)

            if manypass <= 0:
                await ctx.send("❌ Number must be positive!")
                continue
            if manypass > 10:
                await ctx.send("❌ Maximum is 10 passwords!")
                continue
            break
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Cancelled.")
            return

    await ctx.send(
        "📏 How many characters per password? (Max: 50, type `quit` to cancel)"
    )

    while True:
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() == "quit":
                await ctx.send("👋 Cancelled!")
                return

            if not msg.content.isdigit():
                await ctx.send("❌ Please enter a valid number!")
                continue

            manychar = int(msg.content)

            if manychar < 4:
                await ctx.send("❌ Password must be at least 4 characters!")
                continue
            if manychar > 50:
                await ctx.send("❌ Maximum is 50 characters!")
                continue
            break
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Cancelled.")
            return

    characters = (
        "!@#$%&*_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    )

    await ctx.send(
        f"✅ Generating {manypass} password(s) with {manychar} characters each... Check your DMs!"
    )

    passwords = []
    for _ in range(manypass):
        password = "".join(random.choice(characters) for _ in range(manychar))
        passwords.append(password)

    try:
        if manypass == 1:
            await ctx.author.send(f"🔑 **Your Password:** `{passwords[0]}`")
        else:
            msg = "🔑 **Your Passwords:**\n"
            for i, pwd in enumerate(passwords, 1):
                msg += f"**{i}.** `{pwd}`\n"
            await ctx.author.send(msg)
        await ctx.author.send("⚠️ Save these somewhere safe! I don't store them.")
    except:
        await ctx.send("❌ I couldn't DM you! Check your privacy settings.")


# ============================================
# QUOTE COMMAND
# ============================================
@bot.command(name="quote", aliases=["Quotes", "QUOTES", "QUOTE", "Quote", "q"])
async def quote(ctx):
    logger.info(f"{ctx.author} used !quote")
    try:
        response = requests.get("https://zenquotes.io/api/random")
        json_data = response.json()
        quote_text = f"💬 {json_data[0]['q']} — *{json_data[0]['a']}*"
        await ctx.send(quote_text)
    except Exception as e:
        logger.error(f"Quote API error: {e}")
        await ctx.send("❌ Could not fetch a quote right now. Try again later!")


# ============================================
# SAY COMMAND
# ============================================
@bot.command(name="say", aliases=["Say", "Send", "send", "SEND", "dm", "Dm", "DM"])
async def say(ctx, *, msg: str):
    logger.info(f"User {ctx.author} used !say")
    try:
        await ctx.author.send(msg)
        await ctx.send("✅ Check your DMs!")
    except:
        await ctx.send("❌ I couldn't DM you! Check your privacy settings.")


# ============================================
# REPEAT COMMAND
# ============================================
@bot.command(name="repeat", aliases=["Repeat", "REPEAT", "spam", "Spam", "SPAM"])
async def repeat(ctx, *, msg: str):
    logger.info(f"User {ctx.author} used !repeat")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("🔢 How many times do you want that message to be sent? (Max: 10)")

    try:
        response = await bot.wait_for("message", timeout=30.0, check=check)
        times = int(response.content)

        if times <= 0:
            await ctx.send("❌ Number must be positive!")
            return
        if times > 10:
            await ctx.send("❌ Maximum is 10 times!")
            times = 10

        await ctx.send(f"✅ Sending `{msg}` {times} time(s) to your DMs!")

        for i in range(times):
            try:
                await ctx.author.send(f"{i+1}. {msg}")
                await asyncio.sleep(0.5)
            except:
                await ctx.send("❌ I couldn't DM you! Check your privacy settings.")
                return

        await ctx.send("✅ Done! Check your DMs!")
    except ValueError:
        await ctx.send("❌ Please enter a valid number!")
    except asyncio.TimeoutError:
        await ctx.send("⏰ Time's up! Command cancelled.")


# ============================================
# REPLY COMMAND
# ============================================
@bot.command(name="reply", aliases=["Reply", "REPLY", "r"])
async def reply_cmd(ctx, *, msg: str = None):
    logger.info(f"User {ctx.author} used !reply")
    if msg:
        await ctx.reply(msg)
    else:
        await ctx.reply("This is a reply to your message!")


# ============================================
# TEXT SEARCH COMMAND
# ============================================
@bot.command(name="search", aliases=["SEARCH", "Search", "searchtxt"])
async def search(ctx):
    logger.info(f"{ctx.author} selected text search")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("📝 Drop a big chunk of text below. Type `quit` to cancel.")

    try:
        msg = await bot.wait_for("message", timeout=60.0, check=check)
        fat_text = msg.content
        if fat_text.lower() == "quit":
            await ctx.send("👋 Cancelled!")
            return
    except asyncio.TimeoutError:
        await ctx.send("⏰ Time's up! Cancelled.")
        return

    if len(fat_text) > 50000:
        await ctx.send("⚠️ Very large text detected. Continue? (y/n)")
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() not in ["y", "yes"]:
                await ctx.send("👋 Cancelled!")
                return
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Cancelled.")
            return

    while True:
        await ctx.send("🔍 What word do you want to search for? Type `quit` to cancel.")

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            search_word = msg.content
            if search_word.lower() == "quit":
                await ctx.send("👋 Cancelled!")
                return
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Cancelled.")
            return

        if search_word in fat_text:
            await ctx.send(f"✅ Found **'{search_word}'** in the text!")
        else:
            await ctx.send(f"❌ **'{search_word}'** not found in the text.")

        await ctx.send("\nSearch for another word? (y/n)")
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() not in ["y", "yes"]:
                await ctx.send("Thanks for using text search!")
                break
        except asyncio.TimeoutError:
            await ctx.send("Thanks for using text search!")
            break


# ============================================
# HELP COMMAND
# ============================================
@bot.command(name="help", aliases=["Help", "HELP", "h", "H", "commands", "Commands"])
async def custom_help(ctx, command_name: str = None):
    logger.info(f"Help command used by: {ctx.author}")

    if command_name:
        await send_command_help(ctx, command_name)
        return

    embed = discord.Embed(
        title="📚 **Help Menu**",
        description="Use `!help <command>` for more details on a specific command.",
        color=discord.Color.blue(),
    )

    games = "`!rps` - Rock Paper Scissors (solo or vs friend)\n"
    games += "`!guess` - Guess the number game (3 points)\n"
    games += "`!number` - Guess a number 1-20 (5 attempts)\n"
    embed.add_field(name="🎮 **Games**", value=games, inline=False)

    fun = "`!quote` - Get a random inspirational quote\n"
    embed.add_field(name="🎉 **Fun**", value=fun, inline=False)

    utils = "`!ping` - Check bot latency\n"
    utils += "`!calc <expression>` - Calculator\n"
    utils += "`!passgen` - Generate secure passwords\n"
    utils += "`!say <message>` - Bot DMs you\n"
    utils += "`!repeat <message>` - Spam your DMs\n"
    utils += "`!reply <message>` - Bot replies\n"
    utils += "`!search` - Search text for a word\n"
    embed.add_field(name="🔧 **Utilities**", value=utils, inline=False)

    help_text = "`!help` - Show this message\n"
    help_text += "`!help <command>` - Command details\n"
    embed.add_field(name="📖 **Help**", value=help_text, inline=False)

    embed.set_footer(
        text=f"Requested by {ctx.author.name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
    )
    await ctx.send(embed=embed)


async def send_command_help(ctx, command_name):
    command_name = command_name.lower()
    embed = discord.Embed(color=discord.Color.green())
    embed.set_footer(
        text=f"Requested by {ctx.author.name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
    )

    if command_name == "ping":
        embed.title = "📖 `!ping`"
        embed.description = "Check the bot's connection latency."
        embed.add_field(name="Usage", value="`!ping`", inline=False)
    elif command_name == "calc":
        embed.title = "🧮 `!calc`"
        embed.description = "Perform arithmetic calculations."
        embed.add_field(name="Usage", value="`!calc <expression>`", inline=False)
        embed.add_field(name="Example", value="`!calc 5 + 3`", inline=False)
    elif command_name == "rps":
        embed.title = "🪨📄✂️ `!rps`"
        embed.description = "Rock Paper Scissors - solo or vs friend!"
        embed.add_field(name="Usage", value="`!rps`", inline=False)
    elif command_name == "guess":
        embed.title = "🎲 `!guess`"
        embed.description = "Guess the number. Reach 3 points to win!"
        embed.add_field(name="Usage", value="`!guess`", inline=False)
    elif command_name == "number":
        embed.title = "🔢 `!number`"
        embed.description = "Guess a number 1-20. 5 attempts."
        embed.add_field(name="Usage", value="`!number`", inline=False)
    elif command_name in ["passgen", "password", "bgen"]:
        embed.title = "🔑 `!passgen`"
        embed.description = "Generate secure passwords."
        embed.add_field(name="Usage", value="`!passgen`", inline=False)
    elif command_name == "quote":
        embed.title = "💬 `!quote`"
        embed.description = "Get a random quote."
        embed.add_field(name="Usage", value="`!quote`", inline=False)
    elif command_name == "say":
        embed.title = "📨 `!say`"
        embed.description = "Bot DMs you the message."
        embed.add_field(name="Usage", value="`!say <message>`", inline=False)
    elif command_name == "repeat":
        embed.title = "🔁 `!repeat`"
        embed.description = "Spam a message to your DMs."
        embed.add_field(name="Usage", value="`!repeat <message>`", inline=False)
    elif command_name == "reply":
        embed.title = "💬 `!reply`"
        embed.description = "Bot replies to your message."
        embed.add_field(name="Usage", value="`!reply <message>`", inline=False)
    elif command_name == "search":
        embed.title = "🔍 `!search`"
        embed.description = "Search for a word in text."
        embed.add_field(name="Usage", value="`!search`", inline=False)
    elif command_name == "help":
        embed.title = "📚 `!help`"
        embed.description = "You're looking at it!"
    else:
        embed.title = "❌ Command Not Found"
        embed.description = f"No help for `{command_name}`."
        embed.color = discord.Color.red()

    await ctx.send(embed=embed)


# ============================================
# RUN BOT
# ============================================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: No token found in .env file!")
    else:
        bot.run(TOKEN)
