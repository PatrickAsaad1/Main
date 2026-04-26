from Utils.Logger import setup_logging
from discord.ext import commands

logging = setup_logging()


def setup(bot):
    @bot.command(name="servers", aliases=["Servers", "SERVERS"])
    @commands.is_owner()
    async def servers(ctx):
        """List all servers the bot is in."""
        guilds = bot.guilds
        server_list = "\n".join(
            [f"• {guild.name} (ID: {guild.id})" for guild in guilds]
        )
        await ctx.send(f"📊 **Bot is in {len(guilds)} servers:**\n{server_list}")
        logging.info(f"{ctx.author} viewed server list")

    @bot.command(name="leaveserver", aliases=["LeaveServer", "LEAVESERVER"])
    @commands.is_owner()
    async def leave_server(ctx, guild_id: int):
        """Make the bot leave a server by ID."""
        guild = bot.get_guild(guild_id)
        if guild:
            await guild.leave()
            await ctx.send(f"✅ Left server: **{guild.name}**")
            logging.info(f"{ctx.author} made bot leave server: {guild.name}")
        else:
            await ctx.send("❌ Server not found! Check the ID.")
    @bot.command(name="guildchannels", aliases=["GuildChannels"])
    @commands.is_owner()
    async def guild_channels(ctx, guild_id: int):
        guild = bot.get_guild(guild_id)
        if guild:
            channel_list = "\n".join([f"• {channel.name} (ID: {channel.id})" for channel in guild.text_channels])
            await ctx.send(f"📋 **Channels in {guild.name}:**\n{channel_list}")
        else:
            await ctx.send("❌ Server not found!")
