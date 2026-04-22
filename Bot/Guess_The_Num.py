# Bot_games/guess.py
import random
import asyncio
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="guess", aliases=["Guess", "GUESS"])
    async def Guess(ctx):
        logging.info(f"User {ctx.author} started Guess The Number game.")

        score = 0
        difficulty_ranges = {
            "easy": (1, 3),
            "med": (1, 5),
            "medium": (1, 5),
            "hard": (1, 10),
        }

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Step 1: Choose difficulty
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

        # Step 2: Main game loop
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
                logging.info(f"User guessed correctly. Score: {score}/3")
            else:
                await ctx.send("❌ Wrong guess!")
                if score > 0:
                    score -= 1
                logging.info(f"User guessed incorrectly. Score: {score}/3")

            await ctx.send(f"📊 Your score: **{score}/3**")

        # Step 3: Win!
        await ctx.send("🎉🎉🎉 **YOU WON! Reached 3 points!** 🎉🎉🎉")
        logging.info(f"User {ctx.author} won the guessing game!")

        # Step 4: Play again?
        await ctx.send("\nPlay again? (yes/no)")
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() in ["yes", "y"]:
                await Guess(ctx)  # Restart
            else:
                await ctx.send("Thanks for playing!")
        except asyncio.TimeoutError:
            await ctx.send("Thanks for playing!")
