import asyncio
from collections import deque
import discord
from discord import app_commands
from Utils.Logger import setup_logging
import yt_dlp

logging = setup_logging()

SONG_QUEUES = {}


async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))


def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)


async def play_next_song(voice_client, guild_id, channel, bot):
    if guild_id in SONG_QUEUES and SONG_QUEUES[guild_id]:
        audio_url, title = SONG_QUEUES[guild_id].popleft()

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn -c:a libopus -b:a 96k",
        }

        try:
            source = discord.FFmpegOpusAudio(
                audio_url,
                **ffmpeg_options,
                executable="C:\\Users\\smile\\OneDrive\\Documenti\\Development\\Projects\\CLI-Game-And-A-Discord-Bot\\bin\\ffmpeg\\ffmpeg.exe",
            )
        except Exception as e:
            logging.error(f"FFmpeg init error for {title}: {e}")
            asyncio.run_coroutine_threadsafe(
                play_next_song(voice_client, guild_id, channel, bot), bot.loop
            )
            return

        def after_play(error):
            if error:
                logging.error(f"Error playing {title}: {error}")
            asyncio.run_coroutine_threadsafe(
                play_next_song(voice_client, guild_id, channel, bot), bot.loop
            )

        voice_client.play(source, after=after_play)
        asyncio.create_task(channel.send(f"Now playing: **{title}**"))
    else:
        if voice_client.is_connected():
            await voice_client.disconnect()
        if guild_id in SONG_QUEUES:
            del SONG_QUEUES[guild_id]
        logging.info(f"Queue empty for Guild {guild_id}. Disconnected.")


def setup(bot):

    @bot.tree.command(name="skip", description="Skips the current playing song")
    async def skip(interaction: discord.Interaction):
        logging.info(f"{interaction.user} used /skip command")
        if interaction.guild.voice_client and (
            interaction.guild.voice_client.is_playing()
            or interaction.guild.voice_client.is_paused()
        ):
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("Skipped the current song.")
        else:
            await interaction.response.send_message("Not playing anything to skip.")

    @bot.tree.command(name="pause", description="Pause the currently playing song.")
    async def pause(interaction: discord.Interaction):
        logging.info(f"{interaction.user} used /pause command")
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            return await interaction.response.send_message(
                "I'm not in a voice channel."
            )

        if not voice_client.is_playing():
            return await interaction.response.send_message(
                "Nothing is currently playing."
            )

        voice_client.pause()
        await interaction.response.send_message("Playback paused!")

    @bot.tree.command(name="resume", description="Resume the currently paused song.")
    async def resume(interaction: discord.Interaction):
        logging.info(f"{interaction.user} used /resume command")
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            return await interaction.response.send_message(
                "I'm not in a voice channel."
            )

        if not voice_client.is_paused():
            return await interaction.response.send_message(
                "I'm not paused right now."
            )  # FIXED: smart quote ' → '

        voice_client.resume()
        await interaction.response.send_message("Playback resumed!")

    @bot.tree.command(name="stop", description="Stop playback and clear the queue.")
    async def stop(interaction: discord.Interaction):
        logging.info(f"{interaction.user} used /stop command")
        voice_client = interaction.guild.voice_client

        if not voice_client or not voice_client.is_connected():
            return await interaction.response.send_message(
                "I'm not connected to any voice channel."
            )

        guild_id_str = str(interaction.guild_id)
        if guild_id_str in SONG_QUEUES:
            SONG_QUEUES[guild_id_str].clear()

        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()

        await voice_client.disconnect()
        await interaction.response.send_message("Stopped playback and disconnected!")

    @bot.tree.command(name="play", description="Play a song or add it to the queue.")
    @app_commands.describe(song_query="Search query")
    async def play(interaction: discord.Interaction, song_query: str):
        logging.info(f"{interaction.user} used /play command with query: {song_query}")
        await interaction.response.defer()

        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.followup.send(
                "You must be in a voice channel to use this command."
            )
            return

        voice_channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_channel != voice_client.channel:
            await voice_client.move_to(voice_channel)

        ydl_options = {
            "format": "bestaudio[abr<=96]/bestaudio",
            "noplaylist": True,
            "youtube_include_dash_manifest": False,
            "youtube_include_hls_manifest": False,
            "quiet": True,
        }

        query = "ytsearch1:" + song_query
        try:
            results = await search_ytdlp_async(query, ydl_options)
            tracks = results.get("entries", [])
        except Exception as e:
            logging.error(f"YTDL Search Error: {e}")
            await interaction.followup.send(
                "An error occurred while fetching the song."
            )
            return

        if not tracks:
            await interaction.followup.send("No results found.")
            return

        first_track = tracks[0]
        audio_url = first_track["url"]
        title = first_track.get("title", "Untitled")

        guild_id = str(interaction.guild_id)
        if guild_id not in SONG_QUEUES:
            SONG_QUEUES[guild_id] = deque()

        SONG_QUEUES[guild_id].append((audio_url, title))

        if voice_client.is_playing() or voice_client.is_paused():
            await interaction.followup.send(f"Added to queue: **{title}**")
        else:
            await interaction.followup.send(f"Processing your request...")
            await play_next_song(voice_client, guild_id, interaction.channel, bot)
