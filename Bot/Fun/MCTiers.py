# Bot/Fun/MCTiers.py
from Utils.Logger import setup_logging
import requests
import discord

logging = setup_logging()


def setup(bot):
    @bot.command(name="mc", aliases=["Mc", "MC", "mcinfo", "Mcinfo", "MCINFO"])
    async def mc(ctx, *, username: str = None):
        """Get Minecraft player info from MCTiers."""
        if not username:
            await ctx.send("❌ Please provide a username! Example: `!mc Notch`")
            logging.error(f"{ctx.author} used !mc command without username")
            return

        logging.info(f"{ctx.author} used !mc command for: {username}")

        try:
            response = requests.get(
                f"https://mctiers.com/api/v2/profile/by-name/{username}", timeout=10
            )

            if response.status_code == 404:
                await ctx.send(f"❌ Player **{username}** not found!")
                return

            if response.status_code != 200:
                await ctx.send("❌ API error. Try again later!")
                return

            data = response.json()

            embed = discord.Embed(
                title=f"📊 {data['name']}",
                description=f"**UUID:** `{data['uuid']}`",
                color=discord.Color.green(),
            )

            embed.add_field(
                name="🌍 Region", value=data.get("region", "Unknown"), inline=True
            )
            embed.add_field(name="⭐ Points", value=data.get("points", 0), inline=True)
            embed.add_field(
                name="🏆 Overall Rank",
                value=f"#{data.get('overall', 'N/A')}",
                inline=True,
            )

            if data.get("discord_id"):
                embed.add_field(
                    name="💬 Discord", value=f"<@{data['discord_id']}>", inline=True
                )

            rankings = data.get("rankings", {})
            if rankings:
                rankings_text = ""
                for mode, stats in rankings.items():
                    status = "🔴 Retired" if stats.get("retired") else "🟢 Active"
                    rankings_text += (
                        f"**{mode.replace('_', ' ').title()}**\n"
                        f"Tier {stats['tier']} • Pos {stats['pos']} • {status}\n"
                    )
                embed.add_field(name="🎮 Gamemodes", value=rankings_text, inline=False)

            if data.get("badges"):
                badges_text = "\n".join(
                    [f"🏅 {b['title']} — {b['desc']}" for b in data["badges"]]
                )
                embed.add_field(name="🏅 Badges", value=badges_text, inline=False)

            embed.set_footer(text="Data from MCTiers API")
            await ctx.send(embed=embed)
            logging.info(f"MC info sent for {data['name']}")

        except requests.exceptions.Timeout:
            await ctx.send("❌ Request timed out. Try again later!")
            logging.error("MCTiers API timeout")
        except Exception as e:
            await ctx.send("❌ Could not fetch Minecraft info. Try again later!")
            logging.error(f"MCTiers API error: {e}")
