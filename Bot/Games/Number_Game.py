import asyncio
import random
import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="number",
        description="Play a number guessing game against the bot.",
    )
    async def number_game(interaction: discord.Interaction):
        logging.info(f"User {interaction.user} selected number game")

        number = random.randint(1, 20)

        # Initial slash command response context
        await interaction.response.send_message(
            "🎲 I'm thinking of a number from 1-20. You have 5 attempts!\n"
            "Type `quit` to stop playing."
        )
        await asyncio.sleep(0.5)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        attempts = 0

        while attempts < 5:
            await interaction.channel.send(
                f"\n📊 Attempt {attempts + 1}/5\nWhat's your guess?"
            )

            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                uguess = msg.content.lower()
            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ Time's up! Game cancelled.")
                return

            if uguess == "quit":
                await interaction.channel.send("👋 Game cancelled!")
                return

            if not uguess.isdigit():
                await interaction.channel.send("❌ Please enter a number between 1-20!")
                logging.warning(
                    f"User {interaction.user} entered invalid guess: {uguess}"
                )
                continue

            guess_num = int(uguess)

            if guess_num < 1 or guess_num > 20:
                await interaction.channel.send("❌ Please enter a number between 1-20!")
                logging.warning(
                    f"User {interaction.user} entered out of range guess: {guess_num}"
                )
                continue

            attempts += 1

            if guess_num < number:
                await interaction.channel.send("📈 Too low!")
                logging.info(f"User {interaction.user} guessed {guess_num} (too low)")
            elif guess_num > number:
                await interaction.channel.send("📉 Too high!")
                logging.info(f"User {interaction.user} guessed {guess_num} (too high)")
            else:
                await interaction.channel.send(
                    f"🎉 **YOU GOT IT!** The number was {number}!\n"
                    f"You won in {attempts} attempt(s)!"
                )
                logging.info(f"User {interaction.user} guessed correctly: {number}")
                break
        else:
            await interaction.channel.send(
                f"💀 **Out of attempts!** The number was {number}."
            )
            logging.info(f"User {interaction.user} lost. The number was {number}")

        await interaction.channel.send("\nPlay again? (yes/no)")
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() in ["yes", "y"]:
                # When restarting the game recursively, pass the interaction object down
                await play_again_loop(interaction, bot)
            else:
                await interaction.channel.send("Thanks for playing!")
        except asyncio.TimeoutError:
            await interaction.channel.send("Thanks for playing!")


async def play_again_loop(interaction: discord.Interaction, bot):
    """Helper loop to handle game restarts without breaking interaction contexts."""
    logging.info(f"User {interaction.user} is playing another round")

    number = random.randint(1, 20)

    await interaction.channel.send(
        "🎲 I'm thinking of a number from 1-20. You have 5 attempts!\n"
        "Type `quit` to stop playing."
    )

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    attempts = 0

    while attempts < 5:
        await interaction.channel.send(
            f"\n📊 Attempt {attempts + 1}/5\nWhat's your guess?"
        )

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            uguess = msg.content.lower()
        except asyncio.TimeoutError:
            await interaction.channel.send("⏰ Time's up! Game cancelled.")
            return

        if uguess == "quit":
            await interaction.channel.send("👋 Game cancelled!")
            return

        if not uguess.isdigit():
            await interaction.channel.send("❌ Please enter a number between 1-20!")
            continue

        guess_num = int(uguess)

        if guess_num < 1 or guess_num > 20:
            await interaction.channel.send("❌ Please enter a number between 1-20!")
            continue

        attempts += 1

        if guess_num < number:
            await interaction.channel.send("📈 Too low!")
        elif guess_num > number:
            await interaction.channel.send("📉 Too high!")
        else:
            await interaction.channel.send(
                f"🎉 **YOU GOT IT!** The number was {number}!\n"
                f"You won in {attempts} attempt(s)!"
            )
            break
    else:
        await interaction.channel.send(
            f"💀 **Out of attempts!** The number was {number}."
        )

    await interaction.channel.send("\nPlay again? (yes/no)")
    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.lower() in ["yes", "y"]:
            await play_again_loop(interaction, bot)
        else:
            await interaction.channel.send("Thanks for playing!")
    except asyncio.TimeoutError:
        await interaction.channel.send("Thanks for playing!")
