import discord
import requests
from Utils.Config import get_lyrics_channel
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="lyrics",
        description="Get lyrics for a song. Format: Artist - Song Name",
    )
    async def lyric(interaction: discord.Interaction, query: str):
        logging.info(f"{interaction.user} used lyrics command")

        # Channel restriction
        lyrics_channel = get_lyrics_channel(interaction.guild.id)
        if lyrics_channel and interaction.channel.id != lyrics_channel:
            channel = interaction.guild.get_channel(lyrics_channel)
            if channel:
                await interaction.response.send_message(
                    f"❌ This command only works in {channel.mention}!"
                )
            return

        if not query:
            await interaction.response.send_message(
                "❌ Usage: `/lyrics Artist - Song Name`\nExample: `/lyrics Coldplay - Yellow`"
            )
            return

        if " - " not in query:
            await interaction.response.send_message(
                "❌ Please use format: `Artist - Song Name`"
            )
            return

        try:
            parts = query.split(" - ", 1)
            artist = parts[0].strip()
            song = parts[1].strip()

            apis = [
                f"https://api.lyrics.ovh/v1/{artist}/{song}",
                f"https://api.lyrics.ovh/v1/{artist.lower()}/{song.lower()}",
                f"https://api.lyrics.ovh/v1/{artist.title()}/{song.title()}",
                f"https://api.lyrics.ovh/v1/{artist.lower().replace(' ', '')}/{song.lower().replace(' ', '')}",
            ]

            lyrics = None
            for api_url in apis:
                response = requests.get(api_url)
                if response.status_code == 200:
                    json_data = response.json()
                    lyrics = json_data.get("lyrics", "No lyrics found.")
                    if lyrics and lyrics != "No lyrics found.":
                        break

            if not lyrics:
                await interaction.response.send_message(
                    f"❌ Lyrics not found for **{song}** by **{artist}**"
                )
                return

            if len(lyrics) > 1900:
                await interaction.response.send_message(
                    f"🎵 **{song}** by **{artist}**\n"
                )
                for i in range(0, len(lyrics), 1900):
                    chunk = lyrics[i : i + 1900]
                    await interaction.followup.send(
                        chunk
                    )  # FIXED: Use followup for subsequent messages
            else:
                await interaction.response.send_message(
                    f"🎵 **{song}** by **{artist}**\n\n{lyrics}"
                )

            logging.info(f"Lyrics shown for {song} by {artist}")

        except Exception as e:
            logging.error(f"Lyrics API error: {e}")
            await interaction.response.send_message(
                "❌ Could not fetch lyrics. Try again later!"
            )
