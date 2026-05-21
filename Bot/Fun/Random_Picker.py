import asyncio
import random
import discord
from Utils.Helpers import returnx
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="picker",
        description="Create a list of items and randomly pick from it.",
    )
    async def Picker(interaction: discord.Interaction):
        """Create a list of items and randomly pick from it."""
        logging.info(f"{interaction.user} selected random picker")
        choices = []

        await interaction.response.send_message(
            "===== RANDOM PICKER WHEEL =====\n"
            "Commands: 'done' = finish list, 'quit' to return to main menu"
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        while True:
            try:
                await interaction.channel.send(f"Enter item #{len(choices)+1}: ")
                user_input = await bot.wait_for("message", timeout=30.0, check=check)
                content = user_input.content

                if returnx(content):
                    return

                content_lower = content.lower()

                if content_lower == "done":
                    logging.info(
                        f"{interaction.user} finished building the list for random picker"
                    )
                    break
                elif content_lower == "quit":
                    await interaction.channel.send("👋 Game cancelled!")
                    return
                elif content.strip():
                    if content in choices:
                        await interaction.channel.send(
                            f"❌ `{content}` is already in the list!"
                        )
                        logging.info(
                            f"{interaction.user} tried to add duplicate: {content}"
                        )
                        continue
                    choices.append(content)
                    await interaction.channel.send(f"✅ Added: {content}")
                    logging.info(f"Current list: {choices}")
                else:
                    await interaction.channel.send("❌ Please enter a valid item!")
                    logging.warning("User entered empty item")
            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ Time's up! Cancelled.")
                return

        await interaction.channel.send(
            f"📋 Your list ({len(choices)} items): {', '.join(choices)}"
        )

        try:
            await interaction.channel.send("🗑️ Do you want to remove any items? (y/n)")
            remove_response = await bot.wait_for("message", timeout=30.0, check=check)

            if returnx(remove_response.content):
                return

            if remove_response.content.lower() in ["yes", "y"]:
                await interaction.channel.send(f"Current items (1-{len(choices)}):")
                for i, item in enumerate(choices, 1):
                    await interaction.channel.send(f"  {i}. {item}")

                await interaction.channel.send(
                    "Enter the number(s) to remove (comma-separated, or 'all'):"
                )
                remove_input = await bot.wait_for("message", timeout=30.0, check=check)

                if returnx(remove_input.content):
                    return

                remove_content = remove_input.content.lower()

                if remove_content == "all":
                    choices.clear()
                    await interaction.channel.send("🗑️ All items removed!")
                else:
                    try:
                        indices = [
                            int(x.strip()) - 1 for x in remove_content.split(",")
                        ]
                        indices.sort(reverse=True)

                        for idx in indices:
                            if 0 <= idx < len(choices):
                                removed_item = choices.pop(idx)
                                await interaction.channel.send(
                                    f"✅ Removed: {removed_item}"
                                )
                            else:
                                await interaction.channel.send(
                                    f"⚠️ Invalid index: {idx + 1}"
                                )

                        if not choices:
                            await interaction.channel.send("No items left in the list!")
                            return
                    except ValueError:
                        await interaction.channel.send(
                            "❌ Invalid input! Please enter numbers separated by commas."
                        )
                        return  # FIXED: Added return to prevent continuing with invalid input

                if choices:
                    await interaction.channel.send(
                        f"📋 Updated list: {', '.join(choices)}"
                    )
            else:
                await interaction.channel.send("✅ Keeping the list as is.")

        except asyncio.TimeoutError:
            await interaction.channel.send("⏰ Time's up! Skipping removal.")

        if not choices:
            await interaction.channel.send("No items to pick from!")
            return

        while True:
            winner = random.choice(choices)
            await interaction.channel.send(
                f"🎲 **The computer picks:** --- {winner} ---"
            )

            try:
                await interaction.channel.send("Pick again? (y/n or 'quit' to exit): ")
                pick_another = await bot.wait_for("message", timeout=30.0, check=check)

                if returnx(pick_another.content):
                    return

                pick_content = pick_another.content.lower()

                if pick_content in ["n", "no"]:
                    await interaction.channel.send(
                        "Thanks for using the random picker!"
                    )
                    logging.info(f"{interaction.user} finished using the random picker")
                    return
                elif pick_content in ["y", "yes"]:
                    continue
                elif pick_content == "quit":
                    await interaction.channel.send("👋 Game cancelled!")
                    return
                else:
                    await interaction.channel.send("❌ Please enter y, n, or quit.")
                    logging.warning(
                        f"{interaction.user} entered invalid input: {pick_content}"
                    )
                    continue
            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ Time's up! Cancelled.")
                return
