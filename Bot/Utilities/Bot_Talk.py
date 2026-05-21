import asyncio
import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(name="say", description="Make the bot repeat what you say in DMs")
    async def say(interaction: discord.Interaction, msg: str):
        """Make the bot repeat what you say in DMs"""
        logging.info(f"User {interaction.user} used /say {msg}")
        try:
            await interaction.user.send(msg)
            await interaction.response.send_message("✅ Check your DMs!")
            logging.info(f"{interaction.user} made the bot say {msg}")
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I couldn't DM you! Check your privacy settings."
            )
            logging.error(f"Couldn't dm {interaction.user}")

    @bot.tree.command(
        name="repeat", description="Make the bot spam a message in your DMs"
    )
    async def repeat(interaction: discord.Interaction, msg: str):
        """Make the bot spam a message in your DMs"""
        logging.info(
            f"User {interaction.user} used /repeat {msg}"
        )  # FIXED: changed !repeat to /repeat

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        await interaction.response.send_message(
            "🔢 How many times do you want that message to be sent? (Max: 10)"
        )

        try:
            response = await bot.wait_for("message", timeout=30.0, check=check)
            times = int(response.content)

            if times <= 0:
                await interaction.followup.send(
                    "❌ Number must be positive!"
                )  # FIXED: use followup instead of channel.send
                return

            if times > 10:
                await interaction.followup.send(  # FIXED: use followup instead of channel.send
                    "❌ Maximum is 10 times to prevent spam!"
                )
                times = 10

            await interaction.followup.send(  # FIXED: use followup instead of channel.send
                f"✅ Sending `{msg}` {times} time(s) to your DMs!"
            )

            for i in range(times):
                try:
                    await interaction.user.send(f"{i+1}. {msg}")
                    await asyncio.sleep(0.5)
                except discord.Forbidden:
                    await interaction.followup.send(  # FIXED: use followup instead of channel.send
                        "❌ I couldn't DM you! Check your privacy settings."
                    )
                    logging.error(f"Couldn't dm {interaction.user} during repeat")
                    return

            await interaction.followup.send(
                "✅ Done! Check your DMs!"
            )  # FIXED: use followup instead of channel.send
            logging.info(f"{interaction.user} repeated message {times} times")

        except ValueError:
            await interaction.followup.send(
                "❌ Please enter a valid number!"
            )  # FIXED: use followup instead of channel.send
        except asyncio.TimeoutError:
            await interaction.followup.send(
                "⏰ Time's up! Command cancelled."
            )  # FIXED: use followup instead of channel.send
        except Exception as e:
            await interaction.followup.send(
                "❌ Something went wrong!"
            )  # FIXED: use followup instead of channel.send
            logging.error(f"Repeat command error: {e}")

    @bot.tree.command(name="reply", description="Make the bot reply to your message")
    async def reply_cmd(interaction: discord.Interaction, msg: str = None):
        """Reply to the message that triggered this command"""
        logging.info(f"User {interaction.user} used /reply")
        if msg:
            await interaction.response.send_message(msg)
        else:
            await interaction.response.send_message("This is a reply to your message!")
