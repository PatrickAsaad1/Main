import asyncio
import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="search", description="Search for a word in a large text block."
    )
    async def txt(interaction: discord.Interaction):
        """Search for a word in a large text block."""
        logging.info(f"{interaction.user} selected text search")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        await interaction.response.send_message(
            "📝 Drop a big chunk of text below, then tell me a word and I'll hunt it down for you!\n"
            "Type `quit` to cancel."
        )

        try:
            msg = await bot.wait_for("message", timeout=60.0, check=check)
            fat_text = msg.content

            if fat_text.lower() == "quit":
                await interaction.channel.send("👋 Cancelled!")
                return

        except asyncio.TimeoutError:
            await interaction.channel.send("⏰ Time's up! Cancelled.")
            return

        logging.info(f"{interaction.user} submitted text for search")

        if len(fat_text) > 50000:
            await interaction.channel.send(
                "⚠️ Warning: Very large text detected. This might slow down the search.\n"
                "Continue anyway? (y/n)"
            )
            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                if msg.content.lower() not in ["y", "yes"]:
                    await interaction.channel.send("👋 Cancelled!")
                    return
            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ Time's up! Cancelled.")
                return

        while True:
            await interaction.channel.send(
                "🔍 What word do you want to search for?\nType `quit` to cancel."
            )

            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                search_word = msg.content

                if search_word.lower() == "quit":
                    await interaction.channel.send("👋 Cancelled!")
                    return

            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ Time's up! Cancelled.")
                return

            if search_word in fat_text:
                await interaction.channel.send(
                    f"✅ Found **'{search_word}'** in the text!"
                )
                logging.info(f"{interaction.user} found '{search_word}' in the text")
            else:
                await interaction.channel.send(
                    f"❌ **'{search_word}'** not found in the text."
                )
                logging.info(
                    f"{interaction.user} did not find '{search_word}' in the text"
                )

            await interaction.channel.send(
                "\n🔍 Do you want to search for another word? (y/n)"
            )
            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                again = msg.content.lower()

                if again in ["y", "yes"]:
                    continue  # FIXED: Removed dead code after this (the reverser was unreachable)
                else:
                    await interaction.channel.send("👋 Thanks for using text search!")
                    return  # FIXED: Added return so reverser code doesn't run when user says no

            except asyncio.TimeoutError:
                await interaction.channel.send(
                    "⏰ Time's up! Thanks for using text search!"
                )
                return  # FIXED: Added return to prevent falling through to reverser

            # FIXED: The reverser code below was unreachable. Removed it since it's a
            # separate feature that doesn't belong in the search flow.
