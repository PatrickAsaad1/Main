# Bot/Utilities/SetChannel.py
import discord
from discord.ext import commands
from Utils.Config import (
    add_allowed_channel,
    remove_allowed_channel,
    get_allowed_channels,
    set_lyrics_channel,
)
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="setchannel", aliases=["SetChannel", "SETCHANNEL"])
    @commands.has_permissions(administrator=True)
    async def set_channel(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        add_allowed_channel(ctx.guild.id, channel.id)
        await ctx.send(f"✅ {channel.mention} added to allowed channels!")
        logging.info(f"{ctx.author} added {channel.name} in {ctx.guild.name}")

    @bot.command(name="removechannel", aliases=["RemoveChannel", "REMOVECHANNEL"])
    @commands.has_permissions(administrator=True)
    async def remove_channel(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        remove_allowed_channel(ctx.guild.id, channel.id)
        await ctx.send(f"🗑️ {channel.mention} removed from allowed channels!")
        logging.info(f"{ctx.author} removed {channel.name} in {ctx.guild.name}")

    @bot.command(name="channels", aliases=["Channels", "CHANNELS"])
    @commands.has_permissions(administrator=True)
    async def list_channels(ctx):
        channels = get_allowed_channels(ctx.guild.id)
        if not channels:
            await ctx.send("No channels set! Use `!setchannel #channel` to add one.")
            return
        mentions = []
        for cid in channels:
            channel = ctx.guild.get_channel(cid)
            if channel:
                mentions.append(channel.mention)
        await ctx.send(f"📋 Allowed channels: {', '.join(mentions)}")

    @bot.command(name="setlyrics", aliases=["SetLyrics", "SETLYRICS"])
    @commands.has_permissions(administrator=True)
    async def set_lyrics(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        set_lyrics_channel(ctx.guild.id, channel.id)
        await ctx.send(f"✅ Lyrics will now be sent to {channel.mention}!")
        logging.info(
            f"{ctx.author} set lyrics channel to {channel.name} in {ctx.guild.name}"
        )
