import asyncio
import random
import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="passgen",
        description="Generate random passwords with customizable options.",
    )
    async def password_gen(interaction: discord.Interaction):
        """Generate random passwords."""
        logging.info(f"{interaction.user} selected password generator")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        # Attempt to prompt the user in DMs first to keep credentials hidden
        try:
            await interaction.user.send(
                "🔢 How many passwords do you want to generate? (Max: 10, type `quit` to cancel)"
            )
            # Acknowledge the slash command inside the guild channel safely
            await interaction.response.send_message(
                "✅ Check your DMs to set up your password configuration!"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I couldn't DM you! Check your privacy settings.",
                ephemeral=True,
            )
            return

        # Explicit check logic switch to use DM context
        def check_dm(m):
            return m.author == interaction.user and isinstance(
                m.channel, discord.DMChannel
            )

        while True:
            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check_dm)
                if msg.content.lower() == "quit":
                    await interaction.user.send("👋 Cancelled!")
                    return

                if not msg.content.isdigit():
                    await interaction.user.send(
                        "❌ Please enter a valid number! (Max: 10)"
                    )
                    continue

                manypass = int(msg.content)

                if manypass <= 0:
                    await interaction.user.send("❌ Number must be positive!")
                    continue

                if manypass > 10:
                    await interaction.user.send("❌ Maximum is 10 passwords!")
                    continue

                break

            except asyncio.TimeoutError:
                await interaction.user.send("⏰ Time's up! Cancelled.")
                return

        logging.info(f"{interaction.user} wants to generate {manypass} passwords")

        await interaction.user.send(
            "📏 How many characters per password? (Max: 50, type `quit` to cancel)"
        )

        while True:
            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check_dm)
                if msg.content.lower() == "quit":
                    await interaction.user.send("👋 Cancelled!")
                    return

                if not msg.content.isdigit():
                    await interaction.user.send("❌ Please enter a valid number!")
                    continue

                manychar = int(msg.content)

                if manychar < 4:
                    await interaction.user.send(
                        "❌ Password must be at least 4 characters!"
                    )
                    continue

                if manychar > 50:
                    await interaction.user.send("❌ Maximum is 50 characters!")
                    continue

                break

            except asyncio.TimeoutError:
                await interaction.user.send("⏰ Time's up! Cancelled.")
                return

        logging.info(
            f"{interaction.user} wants each password to be {manychar} characters long"
        )

        characters = (
            "!@#$%&*_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )

        await interaction.user.send(
            f"✅ Generating {manypass} password(s) with {manychar} characters each..."
        )

        passwords = []
        for _ in range(manypass):
            password = "".join(random.choice(characters) for _ in range(manychar))
            passwords.append(password)

        if manypass == 1:
            await interaction.user.send(f"🔑 **Your Password:** `{passwords[0]}`")
        else:
            msg_content = "🔑 **Your Passwords:**\n"
            for i, pwd in enumerate(passwords, 1):
                msg_content += f"**{i}.** `{pwd}`\n"
            await interaction.user.send(msg_content)

        await interaction.user.send("⚠️ Save these somewhere safe! I don't store them.")
        logging.info(f"{interaction.user} successfully generated {manypass} passwords")
