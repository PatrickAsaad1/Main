# games/random_picker.py
from Utils.Logger import setup_logging
import random
import asyncio
from Utils.Helpers import returnx

logging = setup_logging()


def setup(bot):
    @bot.command(name="picker", aliases=["Picker", "PICKER", "Wheel"])
    async def Picker(ctx):
        """Create a list of items and randomly pick from it."""
        logging.info(f"{ctx.author} selected random picker")
        choices = []

        await ctx.send(
            "===== RANDOM PICKER WHEEL =====\n"
            "Commands: 'done' = finish list, 'quit' to return to main menu"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while True:
            try:
                await ctx.send(f"Enter item #{len(choices)+1}: ")
                user_input = await bot.wait_for("message", timeout=30.0, check=check)
                content = user_input.content

                if returnx(content):
                    return

                content_lower = content.lower()

                if content_lower == "done":
                    logging.info(
                        f"{ctx.author} finished building the list for random picker"
                    )
                    break
                elif content_lower == "quit":
                    await ctx.send("👋 Game cancelled!")
                    return
                elif content.strip():
                    if content in choices:
                        await ctx.send(f"❌ `{content}` is already in the list!")
                        logging.info(f"{ctx.author} tried to add duplicate: {content}")
                        continue
                    choices.append(content)
                    await ctx.send(f"✅ Added: {content}")
                    logging.info(f"Current list: {choices}")
                else:
                    await ctx.send("❌ Please enter a valid item!")
                    logging.warning("User entered empty item")
            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Cancelled.")
                return

        if not choices:
            await ctx.send("You didn't enter any items!")
            logging.warning(
                f"{ctx.author} tried to use random picker without entering any items"
            )
            return

        await ctx.send(f"📋 Your list ({len(choices)} items): {', '.join(choices)}")

        try:
            await ctx.send("🗑️ Do you want to remove any items? (y/n)")
            remove_response = await bot.wait_for("message", timeout=30.0, check=check)

            if returnx(remove_response.content):
                return

            if remove_response.content.lower() in ["yes", "y"]:
                await ctx.send(f"Current items (1-{len(choices)}):")
                for i, item in enumerate(choices, 1):
                    await ctx.send(f"  {i}. {item}")

                await ctx.send(
                    "Enter the number(s) to remove (comma-separated, or 'all'):"
                )
                remove_input = await bot.wait_for("message", timeout=30.0, check=check)

                if returnx(remove_input.content):
                    return

                remove_content = remove_input.content.lower()

                if remove_content == "all":
                    choices.clear()
                    await ctx.send("🗑️ All items removed!")
                else:
                    try:
                        indices = [
                            int(x.strip()) - 1 for x in remove_content.split(",")
                        ]
                        indices.sort(reverse=True)

                        for idx in indices:
                            if 0 <= idx < len(choices):
                                removed_item = choices.pop(idx)
                                await ctx.send(f"✅ Removed: {removed_item}")
                            else:
                                await ctx.send(f"⚠️ Invalid index: {idx + 1}")

                        if not choices:
                            await ctx.send("No items left in the list!")
                            return
                    except ValueError:
                        await ctx.send(
                            "❌ Invalid input! Please enter numbers separated by commas."
                        )

                if choices:
                    await ctx.send(f"📋 Updated list: {', '.join(choices)}")
            else:
                await ctx.send("✅ Keeping the list as is.")

        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Skipping removal.")

        if not choices:
            await ctx.send("No items to pick from!")
            return

        while True:
            winner = random.choice(choices)
            await ctx.send(f"🎲 **The computer picks:** --- {winner} ---")

            try:
                await ctx.send("Pick again? (y/n or 'quit' to exit): ")
                pick_another = await bot.wait_for("message", timeout=30.0, check=check)

                if returnx(pick_another.content):
                    return

                pick_content = pick_another.content.lower()

                if pick_content in ["n", "no"]:
                    await ctx.send("Thanks for using the random picker!")
                    logging.info(f"{ctx.author} finished using the random picker")
                    return
                elif pick_content in ["y", "yes"]:
                    continue
                elif pick_content == "quit":
                    await ctx.send("👋 Game cancelled!")
                    return
                else:
                    await ctx.send("❌ Please enter y, n, or quit.")
                    logging.warning(
                        f"{ctx.author} entered invalid input: {pick_content}"
                    )
                    continue
            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Cancelled.")
                return
