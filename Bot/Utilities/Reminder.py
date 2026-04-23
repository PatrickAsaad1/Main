# Bot/Reminder.py
import asyncio
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="remind", aliases=["Remind", "REMIND", "reminder"])
    async def remind(ctx, time: str = None, *, reminder: str = None):
        """
        Set a reminder.
        Usage: !remind <time> <message>
        Examples:
          !remind 30s check food
          !remind 5m meeting
          !remind 2h break
        """
        logging.info(f"{ctx.author} set a reminder for {time}: {reminder}")

        if not time or not reminder:
            await ctx.send("❌ Usage: `!remind <time> <message>`")
            await ctx.send("Examples: `!remind 30s check food`, `!remind 5m meeting`")
            return

        # Parse time
        time_dict = {"s": 1, "m": 60, "h": 3600}
        unit = time[-1].lower()

        if unit not in time_dict:
            await ctx.send("❌ Invalid time format! Use `s`, `m`, or `h`")
            await ctx.send("Example: `!remind 30s` or `!remind 5m` or `!remind 2h`")
            return

        try:
            amount = int(time[:-1])
        except ValueError:
            await ctx.send("❌ Invalid number! Example: `!remind 30s`")
            return

        seconds = amount * time_dict[unit]

        if seconds <= 0:
            await ctx.send("❌ Time must be positive!")
            return

        if seconds > 7200:  # 2 hours max
            await ctx.send("❌ Maximum reminder is 2 hours!")
            return

        # Format display time
        if unit == "s":
            display = f"{amount} second{'s' if amount != 1 else ''}"
        elif unit == "m":
            display = f"{amount} minute{'s' if amount != 1 else ''}"
        else:
            display = f"{amount} hour{'s' if amount != 1 else ''}"

        await ctx.send(f"⏰ Reminder set! I'll remind you in {display}.")

        await asyncio.sleep(seconds)

        try:
            await ctx.author.send(f"🔔 **Reminder ({display} ago):** {reminder}")
            logging.info(f"Reminder sent to {ctx.author}")
        except:
            await ctx.send(f"{ctx.author.mention} 🔔 **Reminder:** {reminder}")
            logging.info(f"Reminder sent to channel for {ctx.author}")
