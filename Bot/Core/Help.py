# Bot/Core/Help.py
import discord
from discord.ext import commands
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    # Remove the default help command
    bot.remove_command("help")

    @bot.command(
        name="help", aliases=["Help", "HELP", "h", "H", "commands", "Commands"]
    )
    async def custom_help(ctx, command_name: str = None):
        logging.info(f"Help command used by: {ctx.author}")

        # If user typed !help calc
        if command_name:
            await send_command_help(ctx, command_name)
            return

        # Otherwise show general help
        embed = discord.Embed(
            title="📚 **Help Menu**",
            description="Use `!help <command>` for more details on a specific command.",
            color=discord.Color.blue(),
        )

        # Games section
        games = ""
        games += "`!rps` - Rock Paper Scissors (solo or versus a friend)\n"
        games += "`!guess` - Guess the number game (reach 3 points to win)\n"
        games += "`!number` - Guess a number between 1-20 (5 attempts)\n"
        embed.add_field(name="🎮 **Games**", value=games, inline=False)

        # Simulation section
        sim = ""
        sim += "`!cafe` - Pat Cafe ordering system\n"
        embed.add_field(name="🏪 **Simulation**", value=sim, inline=False)

        # Fun section
        fun = ""
        fun += "`!quote` - Get a random inspirational quote\n"
        fun += "`!picker` - Create a list and pick random items\n"
        embed.add_field(name="🎉 **Fun**", value=fun, inline=False)

        # Utilities section
        utils = ""
        utils += "`!ping` - Check the bot's connection latency\n"
        utils += "`!calc <expression>` - Perform arithmetic calculations\n"
        utils += "`!weather <city>` - Get current weather for any city\n"
        utils += (
            "`!remind <time> <message>` - Set a reminder (e.g., `!remind 5m break`)\n"
        )
        utils += "`!say <message>` - The bot will DM you the message\n"
        utils += "`!repeat <message>` - Spam a message to your DMs (max 10)\n"
        utils += "`!reply <message>` - The bot will reply to your message\n"
        utils += "`!search` - Search for a word in a large text block\n"
        embed.add_field(name="🔧 **Utilities**", value=utils, inline=False)

        # Security section
        security = ""
        security += "`!passgen` - Generate secure random passwords\n"
        security += "`!encrypt <message>` - Encrypt a message and get the key\n"
        security += "`!decrypt` - Decrypt a message using the key\n"
        embed.add_field(name="🔐 **Security**", value=security, inline=False)

        # Help section
        help_text = ""
        help_text += "`!help` - Display this message\n"
        help_text += "`!help <command>` - View detailed information about a command\n"
        embed.add_field(name="📖 **Help**", value=help_text, inline=False)

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

        await ctx.send(embed=embed)


async def send_command_help(ctx, command_name):
    """Send help for a specific command."""
    command_name = command_name.lower()

    if command_name == "ping":
        embed = discord.Embed(
            title="📖 `!ping`",
            description="Check the bot's connection latency to Discord.",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!ping`", inline=False)
        embed.add_field(name="Example", value="`!ping` → `🏓 Pong! 47ms`", inline=False)

    elif command_name == "calc":
        embed = discord.Embed(
            title="🧮 `!calc`",
            description="Perform basic arithmetic calculations with support for multiple operations.",
            color=discord.Color.green(),
        )
        embed.add_field(
            name="Usage",
            value="`!calc <expression>`\nSupports both spaced and unspaced formats.",
            inline=False,
        )
        embed.add_field(
            name="Operators",
            value="`+` (addition)\n`-` (subtraction)\n`*` or `x` (multiplication)\n`/` (division)",
            inline=False,
        )
        embed.add_field(
            name="Examples",
            value="`!calc 5 + 3` → `🧮 5.0 + 3.0 = 8.0`\n`!calc 5+3` → `🧮 5+3 = 8.0`\n`!calc 5 + 3 + 2` → `🧮 5 + 3 + 2 = 10.0`",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Calculations are performed left-to-right. Standard order of operations is not applied.",
            inline=False,
        )

    elif command_name == "rps":
        embed = discord.Embed(
            title="🪨📄✂️ `!rps`",
            description="Play Rock Paper Scissors against the computer or challenge a friend!",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!rps`", inline=False)
        embed.add_field(
            name="Solo Mode",
            value="Play against the computer. First to 3 points wins.\nType `rock`, `paper`, or `scissors` when prompted.\nType `quit` to stop.",
            inline=False,
        )
        embed.add_field(
            name="Multiplayer Mode",
            value="Type `yes` when asked if you want to play with a friend, then mention the user you wish to challenge.\nChoices are submitted privately via DM.\nOnly the final result is announced in the channel.",
            inline=False,
        )

    elif command_name == "guess":
        embed = discord.Embed(
            title="🎲 `!guess`",
            description="Guess the randomly generated number. Reach 3 points to win!",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!guess`", inline=False)
        embed.add_field(
            name="Difficulties",
            value="`easy` — Numbers 1-3\n`med` or `medium` — Numbers 1-5\n`hard` — Numbers 1-10",
            inline=False,
        )
        embed.add_field(
            name="How to Play",
            value="Select a difficulty level, then guess the number.\nCorrect guess: +1 point\nIncorrect guess: -1 point (if score > 0)\nType `quit` to exit the game.",
            inline=False,
        )

    elif command_name == "number":
        embed = discord.Embed(
            title="🔢 `!number`",
            description="Guess a number between 1 and 20. You have 5 attempts.",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!number`", inline=False)
        embed.add_field(
            name="How to Play",
            value="The bot will select a random number between 1 and 20.\nYou have 5 attempts to guess correctly.\nThe bot will tell you if your guess is too high or too low.\nType `quit` to exit the game.",
            inline=False,
        )

    elif command_name == "say":
        embed = discord.Embed(
            title="📨 `!say`",
            description="Have the bot send a private message to you containing your text.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Usage", value="`!say <message>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Say`, `!send`, `!Send`, `!dm`, `!Dm`, `!DM`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value='`!say Hello, world!` → The bot will DM you "Hello, world!"',
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="If your DMs are closed, the bot will be unable to send the message and will notify you in the channel.",
            inline=False,
        )

    elif command_name == "repeat":
        embed = discord.Embed(
            title="🔁 `!repeat`",
            description="Have the bot spam a message to your DMs.",
            color=discord.Color.purple(),
        )
        embed.add_field(name="Usage", value="`!repeat <message>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Repeat`, `!REPEAT`, `!spam`, `!Spam`, `!SPAM`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="After typing the command, the bot will ask how many times you want the message sent (maximum 10).\nThe messages will be delivered to your DMs.",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!repeat Hello!` → Bot asks for amount → You type `5` → Bot DMs you 'Hello!' 5 times",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Maximum is 10 times to prevent spam. If your DMs are closed, the command will fail.",
            inline=False,
        )

    elif command_name == "reply":
        embed = discord.Embed(
            title="💬 `!reply`",
            description="The bot will reply directly to the message that triggered this command.",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Usage", value="`!reply` or `!reply <message>`", inline=False
        )
        embed.add_field(name="Aliases", value="`!Reply`, `!REPLY`, `!r`", inline=False)
        embed.add_field(
            name="Example",
            value="`!reply Hello!` → The bot replies to your message with 'Hello!'",
            inline=False,
        )

    elif command_name == "quote":
        embed = discord.Embed(
            title="💬 `!quote`",
            description="Get a random inspirational quote from the ZenQuotes API.",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Usage", value="`!quote`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Quotes`, `!QUOTES`, `!QUOTE`, `!Quote`, `!q`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!quote` → `✨ When your intuition is strong, follow it. — *Lolly Daskal*`",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Quotes are fetched from ZenQuotes API. Requires internet connection.",
            inline=False,
        )

    elif command_name in ["passgen", "password", "genpass", "bgen"]:
        embed = discord.Embed(
            title="🔑 `!passgen`",
            description="Generate secure random passwords.",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!passgen`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!password`, `!genpass`, `!bgen`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="The bot will ask how many passwords you want (max 10) and how many characters per password (4-50).\nPasswords include letters, numbers, and symbols.",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!passgen` → Bot asks for amount → You type `3` → Bot asks for length → You type `16` → Bot DMs you 3 passwords of 16 characters each",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Passwords are sent via DM for privacy. Type `quit` to cancel at any time.",
            inline=False,
        )

    elif command_name == "search":
        embed = discord.Embed(
            title="🔍 `!search`",
            description="Search for a word in a large block of text.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Usage", value="`!search`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!SEARCH`, `!Search`, `!searchtxt`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="Paste a large block of text, then enter the word you want to find.\nThe bot will tell you if the word exists in the text.",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Maximum text length is 50,000 characters. Type `quit` to cancel.",
            inline=False,
        )

    elif command_name in ["encrypt", "enc"]:
        embed = discord.Embed(
            title="🔒 `!encrypt`",
            description="Encrypt a message using Fernet encryption.",
            color=discord.Color.dark_blue(),
        )
        embed.add_field(name="Usage", value="`!encrypt <message>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Encrypt`, `!ENCRYPT`, `!enc`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="The bot generates a unique key and encrypts your message.\nBoth the encrypted message and key are sent to your DMs.",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!encrypt Hello World` → Bot DMs you the encrypted message and key",
            inline=False,
        )
        embed.add_field(
            name="⚠️ Important",
            value="**SAVE THE KEY!** Without it, the message cannot be decrypted. The bot does not store keys.",
            inline=False,
        )

    elif command_name in ["decrypt", "dec"]:
        embed = discord.Embed(
            title="🔓 `!decrypt`",
            description="Decrypt a message using the provided key.",
            color=discord.Color.dark_blue(),
        )
        embed.add_field(name="Usage", value="`!decrypt`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Decrypt`, `!DECRYPT`, `!dec`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="The bot will DM you and ask for the encrypted message, then the key.\nIf both are correct, the decrypted message is sent to your DMs.",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="For privacy, the entire process happens in DMs. The bot never sees your decrypted message in the channel.",
            inline=False,
        )

    elif command_name in ["picker", "wheel"]:
        embed = discord.Embed(
            title="🎲 `!picker`",
            description="Create a custom list and let the bot pick random items from it.",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Usage", value="`!picker`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Picker`, `!PICKER`, `!Wheel`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="1. Add items to your list one by one\n2. Type `done` when finished\n3. Optionally remove items by number\n4. The bot picks random items from your list",
            inline=False,
        )
        embed.add_field(
            name="Commands During Pick",
            value="`done` - Finish adding items\n`quit` - Exit at any time\n`y/n` - Pick again or stop",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!picker` → Add 'Pizza', 'Burger', 'Sushi' → `done` → Bot picks: 'Sushi'",
            inline=False,
        )

    elif command_name in ["cafe", "Cafe", "CAFE"]:
        embed = discord.Embed(
            title="🏪 `!cafe`",
            description="Pat Cafe ordering system - order food and drinks!",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!cafe`", inline=False)
        embed.add_field(name="Aliases", value="`!Cafe`, `!CAFE`", inline=False)
        embed.add_field(
            name="Menu",
            value="🍕 Pizza - $8\n🍔 Burger - $7\n☕ Tea - $2\n☕ Coffee - $3\n☕ Latte - $4",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="1. Choose an item from the menu\n2. Enter quantity (limits apply)\n3. Add more items or finish\n4. Get your total bill",
            inline=False,
        )
        embed.add_field(
            name="Quantity Limits",
            value="Pizza: 10 | Burger: 15 | Drinks: 50",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Type `quit` at any time to cancel your order.",
            inline=False,
        )

    elif command_name in ["remind", "reminder"]:
        embed = discord.Embed(
            title="⏰ `!remind`",
            description="Set a reminder and the bot will DM you when time is up.",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Usage", value="`!remind <time> <message>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Remind`, `!REMIND`, `!reminder`",
            inline=False,
        )
        embed.add_field(
            name="Time Formats",
            value="`30s` - 30 seconds\n`5m` - 5 minutes\n`2h` - 2 hours",
            inline=False,
        )
        embed.add_field(
            name="Examples",
            value="`!remind 30s check food`\n`!remind 5m meeting`\n`!remind 2h take a break`",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Maximum reminder is 2 hours. Reminders are lost if the bot restarts.",
            inline=False,
        )

    elif command_name == "weather":
        embed = discord.Embed(
            title="🌤️ `!weather`",
            description="Get current weather for any city in the world.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Usage", value="`!weather <city>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Weather`, `!WEATHER`, `!temp`",
            inline=False,
        )
        embed.add_field(
            name="Examples",
            value='`!weather Cairo`\n`!weather London`\n`!weather "New York"`',
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Uses Open-Meteo API. Works for virtually any city worldwide.",
            inline=False,
        )

    elif command_name == "help":
        embed = discord.Embed(
            title="📚 `!help`",
            description="You are currently viewing it!",
            color=discord.Color.green(),
        )
        embed.add_field(
            name="Usage",
            value="`!help` — Display all available commands\n`!help <command>` — View detailed information about a specific command",
            inline=False,
        )

    else:
        embed = discord.Embed(
            title="❌ Command Not Found",
            description=f"No help information is available for `{command_name}`.",
            color=discord.Color.red(),
        )
        embed.add_field(
            name="Tip",
            value="Use `!help` to see a list of all available commands.",
            inline=False,
        )

    embed.set_footer(
        text=f"Requested by {ctx.author.name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
    )
    await ctx.send(embed=embed)
