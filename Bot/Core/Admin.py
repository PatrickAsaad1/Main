# Bot/Core/Servers.py (or whatever filename you use)
import discord
from Utils.Logger import setup_logging
from discord.ext import commands

logging = setup_logging()


def setup(bot):
    @bot.tree.command(name="servers", description="List all servers the bot is in.")
    @commands.is_owner()
    async def servers(interaction: discord.Interaction):
        """List all servers the bot is in."""
        guilds = bot.guilds
        server_list = "\n".join(
            [f"• {guild.name} (ID: {guild.id})" for guild in guilds]
        )
        await interaction.response.send_message(
            f"📊 **Bot is in {len(guilds)} servers:**\n{server_list}"
        )
        logging.info(f"{interaction.user} viewed server list")

    @bot.tree.command(
        name="leaveserver", description="Make the bot leave a server by ID."
    )
    @commands.is_owner()
    async def leave_server(interaction: discord.Interaction, guild_id: str):
        """Make the bot leave a server by ID."""
        guild = bot.get_guild(int(guild_id))
        if guild:
            await guild.leave()
            await interaction.response.send_message(f"✅ Left server: **{guild.name}**")
            logging.info(f"{interaction.user} made bot leave server: {guild.name}")
        else:
            await interaction.response.send_message(
                "❌ Server not found! Check the ID."
            )

    @bot.tree.command(
        name="guildchannels", description="List all text channels in a server by ID."
    )
    @commands.is_owner()
    async def guild_channels(interaction: discord.Interaction, guild_id: str):
        """List all text channels in a server by ID."""
        guild = bot.get_guild(int(guild_id))
        if guild:
            channel_list = "\n".join(
                [
                    f"• {channel.name} (ID: {channel.id})"
                    for channel in guild.text_channels
                ]
            )
            await interaction.response.send_message(
                f"📋 **Channels in {guild.name}:**\n{channel_list}"
            )
        else:
            await interaction.response.send_message("❌ Server not found!")
