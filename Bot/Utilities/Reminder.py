import asyncio
import re
import discord
from Utils.Logger import setup_logging

logging = setup_logging()
reminder_tasks = {}  # user_id -> asyncio.Task


async def _remind_user(interaction: discord.Interaction, seconds, reminder):
    try:
        await asyncio.sleep(seconds)
        try:
            await interaction.user.send(
                f"{interaction.user.mention} 🔔 **Reminder:** {reminder}"
            )
        except discord.Forbidden:
            # Fallback to the channel if their DMs are closed
            await interaction.channel.send(
                f"{interaction.user.mention} 🔔 **Reminder:** {reminder}"
            )
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logging.error(f"Error executing reminder: {e}")
    finally:
        # Check to make sure we don't accidentally pop a newly scheduled reminder
        if reminder_tasks.get(interaction.user.id) == asyncio.current_task():
            reminder_tasks.pop(interaction.user.id, None)


def setup(bot):  # FIXED: Merged both setup functions into one

    @bot.tree.command(
        name="remind",
        description="Set a reminder. Time format: 30s, 5m, 2h",
    )
    async def remind(interaction: discord.Interaction, time: str, reminder: str):
        logging.info(f"{interaction.user} used /remind command")

        # Parse time with regex
        match = re.match(r"^(\d+)([smh])$", time.lower())
        if not match:
            await interaction.response.send_message(
                "❌ Invalid time format! Use `30s`, `5m`, or `2h`"
            )
            return

        amount, unit = int(match.group(1)), match.group(2)
        time_dict = {"s": 1, "m": 60, "h": 3600}
        seconds = amount * time_dict[unit]

        if seconds <= 0 or seconds > 7200:
            await interaction.response.send_message(
                "❌ Time must be positive and ≤ 2 hours"
            )
            return

        # Display time
        unit_names = {"s": "second", "m": "minute", "h": "hour"}
        display = f"{amount} {unit_names[unit]}{'s' if amount != 1 else ''}"

        await interaction.response.send_message(
            f"⏰ Reminder set! I'll remind you in {display}."
        )

        # Cancel any preexisting reminder task for this user
        if interaction.user.id in reminder_tasks:
            reminder_tasks[interaction.user.id].cancel()

        # Store task for potential cancellation
        task = asyncio.create_task(_remind_user(interaction, seconds, reminder))
        reminder_tasks[interaction.user.id] = task

    @bot.tree.command(name="cancel_remind", description="Cancel your active reminder.")
    async def cancel_remind(interaction: discord.Interaction):
        logging.info(f"{interaction.user} used /cancel_remind command")

        if interaction.user.id in reminder_tasks:
            reminder_tasks[interaction.user.id].cancel()
            reminder_tasks.pop(interaction.user.id, None)
            await interaction.response.send_message("✅ Reminder cancelled.")
        else:
            await interaction.response.send_message("❌ No active reminder found.")
