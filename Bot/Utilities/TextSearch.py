# games/text_search.py
from Utils.Logger import setup_logging
import asyncio

logging = setup_logging()


def setup(bot):
    @bot.command(name="search", aliases=["SEARCH", "Search", "searchtxt"])
    async def txt(ctx):
        """Search for a word in a large text block."""
        logging.info(f"{ctx.author} selected text search")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(
            "📝 Drop a big chunk of text below, then tell me a word and I'll hunt it down for you!\n"
            "Type `quit` to cancel."
        )

        try:
            msg = await bot.wait_for("message", timeout=60.0, check=check)
            fat_text = msg.content

            if fat_text.lower() == "quit":
                await ctx.send("👋 Cancelled!")
                return

        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Cancelled.")
            return

        logging.info(f"{ctx.author} submitted text for search")

        if len(fat_text) > 50000:
            await ctx.send(
                "⚠️ Warning: Very large text detected. This might slow down the search.\n"
                "Continue anyway? (y/n)"
            )
            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                if msg.content.lower() not in ["y", "yes"]:
                    await ctx.send("👋 Cancelled!")
                    return
            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Cancelled.")
                return

        while True:
            await ctx.send("🔍 What word do you want to search for?\nType `quit` to cancel.")

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
                logging.info(f"{ctx.author} found '{search_word}' in the text")
            else:
                await ctx.send(f"❌ **'{search_word}'** not found in the text.")
                logging.info(f"{ctx.author} did not find '{search_word}' in the text")

            await ctx.send("\n🔄 Want to see a secret word reverser? (y/n)")
            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                secret = msg.content.lower()

                if secret in ["y", "yes"]:
                    logging.info(f"{ctx.author} chose to use word reverser")
                    await ctx.send("Enter a word to reverse:")

                    try:
                        msg = await bot.wait_for("message", timeout=30.0, check=check)
                        word = msg.content

                        if word.lower() == "quit":
                            await ctx.send("👋 Skipping reverser...")
                        elif word:
                            reversed_word = word[::-1]
                            await ctx.send(f"🔄 Reversed: **{reversed_word}**")
                            logging.info(f"{ctx.author} reversed '{word}' to '{reversed_word}'")
                        else:
                            await ctx.send("❌ No word entered!")

                    except asyncio.TimeoutError:
                        await ctx.send("⏰ Time's up! Skipping reverser...")

                elif secret in ["n", "no"]:
                    logging.info(f"{ctx.author} skipped word reverser")
                else:
                    await ctx.send("❌ Invalid choice! Skipping...")

            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Skipping reverser...")

            await ctx.send("\n🔍 Do you want to search for another word? (y/n)")
            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                again = msg.content.lower()

                if again in ["y", "yes"]:
                    continue
                else:
                    await ctx.send("👋 Thanks for using text search!")
                    return

            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Thanks for using text search!")
                return