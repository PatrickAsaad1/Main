import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="serverinfo", description="Get information about the server."
    )
    async def serverinfo(interaction: discord.Interaction):
        logging.info(f"{interaction.user} used /serverinfo")

        guild = interaction.guild

        embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.blue())

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(
            name="👑 Owner",
            value=guild.owner.mention if guild.owner else "Unknown",
            inline=True,
        )
        embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
        embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
        embed.add_field(
            name="📅 Created",
            value=guild.created_at.strftime("%B %d, %Y"),
            inline=True,
        )
        embed.add_field(name="💬 Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)

        await interaction.response.send_message(embed=embed)
