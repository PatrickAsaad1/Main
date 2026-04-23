# Bot_games/number_game.py
import random
import asyncio
import logging
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="number", aliases=["Number", "NUMBER", "num", "Num"])
    async def number_game(ctx):
        logging.info(f"User {ctx.author} selected number game")

        number = random.randint(1, 20)

        await ctx.send(
            "🎲 I'm thinking of a number from 1-20. You have 5 attempts!\n"
            "Type `quit` to stop playing."
        )
        await asyncio.sleep(0.5)

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
                logging.warning(f"User {ctx.author} entered invalid guess: {uguess}")
                continue

            guess_num = int(uguess)

            if guess_num < 1 or guess_num > 20:
                await ctx.send("❌ Please enter a number between 1-20!")
                logging.warning(
                    f"User {ctx.author} entered out of range guess: {guess_num}"
                )
                continue

            attempts += 1

            if guess_num < number:
                await ctx.send("📈 Too low!")
                logging.info(f"User {ctx.author} guessed {guess_num} (too low)")
            elif guess_num > number:
                await ctx.send("📉 Too high!")
                logging.info(f"User {ctx.author} guessed {guess_num} (too high)")
            else:
                await ctx.send(
                    f"🎉 **YOU GOT IT!** The number was {number}!\n"
                    f"You won in {attempts} attempt(s)!"
                )
                logging.info(f"User {ctx.author} guessed correctly: {number}")
                break
        else:
            await ctx.send(f"💀 **Out of attempts!** The number was {number}.")
            logging.info(f"User {ctx.author} lost. The number was {number}")

        await ctx.send("\nPlay again? (yes/no)")
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() in ["yes", "y"]:
                await number_game(ctx)
            else:
                await ctx.send("Thanks for playing!")
        except asyncio.TimeoutError:
            await ctx.send("Thanks for playing!")
