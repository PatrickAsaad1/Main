import discord
from discord import app_commands
from Utils.Config import (
    add_allowed_channel,
    get_allowed_channels,
    remove_allowed_channel,
    remove_game_news_channel,
    remove_lyrics_channel,
    remove_rap_news_channel,
    set_game_news_channel,
    set_lyrics_channel,
    set_pet_channel,
    set_rap_news_channel,
)
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="setchannel",
        description="Add a channel to the allowed channels list (defaults to current).",
    )
    @app_commands.default_permissions(administrator=True)
    async def set_channel(
        interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = interaction.channel
        add_allowed_channel(interaction.guild_id, channel.id)
        await interaction.response.send_message(
            f"✅ {channel.mention} added to allowed channels!"
        )
        logging.info(
            f"{interaction.user} added {channel.name} in {interaction.guild.name}"
        )

    @bot.tree.command(
        name="removechannel",
        description="Remove a channel from the allowed channels list (defaults to current).",
    )
    @app_commands.default_permissions(administrator=True)
    async def remove_channel(
        interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = interaction.channel
        remove_allowed_channel(interaction.guild_id, channel.id)
        await interaction.response.send_message(
            f"🗑️ {channel.mention} removed from allowed channels!"
        )
        logging.info(
            f"{interaction.user} removed {channel.name} in {interaction.guild.name}"
        )

    @bot.tree.command(
        name="channels",
        description="List all allowed channels for bot commands.",
    )
    @app_commands.default_permissions(administrator=True)
    async def list_channels(interaction: discord.Interaction):
        channels = get_allowed_channels(interaction.guild_id)
        if not channels:
            await interaction.response.send_message(
                "No channels set! Use `/setchannel channel:#channel` to add one."
            )
            return
        mentions = []
        for cid in channels:
            channel = interaction.guild.get_channel(cid)
            if channel:
                mentions.append(channel.mention)
        await interaction.response.send_message(
            f"📋 Allowed channels: {', '.join(mentions)}"
        )

    @bot.tree.command(
        name="setlyrics",
        description="Set a channel for lyrics updates (defaults to current).",
    )
    @app_commands.default_permissions(administrator=True)
    async def set_lyrics(
        interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = interaction.channel
        set_lyrics_channel(interaction.guild_id, channel.id)
        await interaction.response.send_message(
            f"✅ Lyrics will be sent to {channel.mention}!"
        )
        logging.info(
            f"{interaction.user} set lyrics channel to {channel.name} in {interaction.guild.name}"
        )

    @bot.tree.command(name="removelyrics", description="Remove the lyrics channel.")
    @app_commands.default_permissions(administrator=True)
    async def remove_lyrics(interaction: discord.Interaction):
        remove_lyrics_channel(interaction.guild_id)
        await interaction.response.send_message("🗑️ Lyrics channel removed!")
        logging.info(
            f"{interaction.user} removed lyrics channel in {interaction.guild.name}"
        )

    @bot.tree.command(
        name="setrapnews",
        description="Set a channel for rap news updates (defaults to current).",
    )
    @app_commands.default_permissions(administrator=True)
    async def set_rap_news(
        interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = interaction.channel
        set_rap_news_channel(interaction.guild_id, channel.id)
        await interaction.response.send_message(
            f"✅ Rap news will be sent to {channel.mention}!"
        )
        logging.info(
            f"{interaction.user} set rap news channel to {channel.name} in {interaction.guild.name}"
        )

    @bot.tree.command(
        name="sethourlypets",
        description="Set a channel for hourly pet pictures (defaults to current).",
    )
    @app_commands.default_permissions(administrator=True)
    async def set_hourly_pets(
        interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = interaction.channel
        set_pet_channel(interaction.guild_id, channel.id)
        await interaction.response.send_message(
            f"✅ Hourly pet pictures will be sent to {channel.mention}!"
        )
        logging.info(
            f"{interaction.user} set pet channel to {channel.name} in {interaction.guild.name}"
        )

    @bot.tree.command(
        name="setgamenews",
        description="Set a channel for gaming news updates (defaults to current).",
    )
    @app_commands.default_permissions(administrator=True)
    async def set_game_news(
        interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = interaction.channel
        set_game_news_channel(interaction.guild_id, channel.id)
        await interaction.response.send_message(
            f"✅ Gaming news will be sent to {channel.mention}!"
        )
        logging.info(
            f"{interaction.user} set game news channel to {channel.name} in {interaction.guild.name}"
        )

    @bot.tree.command(name="removerapnews", description="Remove the rap news channel.")
    @app_commands.default_permissions(administrator=True)
    async def remove_rap_news(interaction: discord.Interaction):
        remove_rap_news_channel(interaction.guild_id)
        await interaction.response.send_message("🗑️ Rap news channel removed!")
        logging.info(
            f"{interaction.user} removed rap news channel in {interaction.guild.name}"
        )

    @bot.tree.command(
        name="removegamenews", description="Remove the gaming news channel."
    )
    @app_commands.default_permissions(administrator=True)
    async def remove_game_news(interaction: discord.Interaction):
        remove_game_news_channel(interaction.guild_id)
        await interaction.response.send_message("🗑️ Gaming news channel removed!")
        logging.info(
            f"{interaction.user} removed game news channel in {interaction.guild.name}"
        )
