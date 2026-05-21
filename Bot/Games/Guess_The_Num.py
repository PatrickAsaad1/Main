import asyncio
import random
import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="guess", description="Play a number guessing game against the bot."
    )
    async def Guess(interaction: discord.Interaction):
        logging.info(f"User {interaction.user} started Guess The Number game.")

        score = 0
        difficulty_ranges = {
            "easy": (1, 3),
            "med": (1, 5),
            "medium": (1, 5),
            "hard": (1, 10),
        }

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        # Initial response to the slash command interaction
        await interaction.response.send_message(
            "Choose difficulty: `easy`, `med`, or `hard`"
        )

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            game = msg.content.lower()
        except asyncio.TimeoutError:
            await interaction.channel.send("⏰ Time's up!")
            return

        if game == "quit":
            await interaction.channel.send("👋 Game cancelled!")
            return

        if game not in difficulty_ranges:
            await interaction.channel.send("❌ Invalid! Choose: easy, med, or hard")
            return

        low, high = difficulty_ranges[game]
        await interaction.channel.send(
            f"Great! I'll pick a number between {low} and {high}\n"
            f"Try to reach 3 points to win! Type `quit` to stop."
        )

        while score < 3:
            rnum = random.randint(low, high)
            await interaction.channel.send(f"\n🎯 Guess a number ({low}-{high}):")

            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                user_input = msg.content.lower()
            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ Time's up!")
                return

            if user_input == "quit":
                await interaction.channel.send("👋 Game cancelled!")
                return

            try:
                unum = int(user_input)
            except ValueError:
                await interaction.channel.send("❌ Please enter a number!")
                continue

            if unum < low or unum > high:
                await interaction.channel.send(
                    f"❌ Enter a number between {low} and {high}!"
                )
                continue

            await interaction.channel.send(f"The number was: **{rnum}**")

            if unum == rnum:
                await interaction.channel.send("✅ You got it right! +1 point!")
                score += 1
                logging.info(f"User guessed correctly. Score: {score}/3")
            else:
                await interaction.channel.send("❌ Wrong guess!")
                if score > 0:
                    score -= 1
                logging.info(f"User guessed incorrectly. Score: {score}/3")

            await interaction.channel.send(f"📊 Your score: **{score}/3**")

        await interaction.channel.send("🎉🎉🎉 **YOU WON! Reached 3 points!** 🎉🎉🎉")
        logging.info(f"User {interaction.user} won the guessing game!")

        await interaction.channel.send("\nPlay again? (yes/no)")
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() in ["yes", "y"]:
                # Pass off to the loop helper to run another round cleanly
                await play_again_loop(interaction, bot)
            else:
                await interaction.channel.send("Thanks for playing!")
        except asyncio.TimeoutError:
            await interaction.channel.send("Thanks for playing!")


async def play_again_loop(interaction: discord.Interaction, bot):
    """Helper loop to cleanly rerun the game rounds without context nesting conflicts."""
    logging.info(f"User {interaction.user} restarted Guess game loop.")

    score = 0
    difficulty_ranges = {
        "easy": (1, 3),
        "med": (1, 5),
        "medium": (1, 5),
        "hard": (1, 10),
    }

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    await interaction.channel.send("Choose difficulty: `easy`, `med`, or `hard`")

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        game = msg.content.lower()
    except asyncio.TimeoutError:
        await interaction.channel.send("⏰ Time's up!")
        return

    if game == "quit":
        await interaction.channel.send("👋 Game cancelled!")
        return

    if game not in difficulty_ranges:
        await interaction.channel.send("❌ Invalid! Choose: easy, med, or hard")
        return

    low, high = difficulty_ranges[game]
    await interaction.channel.send(
        f"Great! I'll pick a number between {low} and {high}\n"
        f"Try to reach 3 points to win! Type `quit` to stop."
    )

    while score < 3:
        rnum = random.randint(low, high)
        await interaction.channel.send(f"\n🎯 Guess a number ({low}-{high}):")

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            user_input = msg.content.lower()
        except asyncio.TimeoutError:
            await interaction.channel.send("⏰ Time's up!")
            return

        if user_input == "quit":
            await interaction.channel.send("👋 Game cancelled!")
            return

        try:
            unum = int(user_input)
        except ValueError:
            await interaction.channel.send("❌ Please enter a number!")
            continue

        if unum < low or unum > high:
            await interaction.channel.send(
                f"❌ Enter a number between {low} and {high}!"
            )
            continue

        await interaction.channel.send(f"The number was: **{rnum}**")

        if unum == rnum:
            await interaction.channel.send("✅ You got it right! +1 point!")
            score += 1
        else:
            await interaction.channel.send("❌ Wrong guess!")
            if score > 0:
                score -= 1

        await interaction.channel.send(f"📊 Your score: **{score}/3**")

    await interaction.channel.send("🎉🎉🎉 **YOU WON! Reached 3 points!** 🎉🎉🎉")

    await interaction.channel.send("\nPlay again? (yes/no)")
    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.lower() in ["yes", "y"]:
            await play_again_loop(interaction, bot)
        else:
            await interaction.channel.send("Thanks for playing!")
    except asyncio.TimeoutError:
        await interaction.channel.send("Thanks for playing!")
