# Bot_games/rps.py
import random
import asyncio
import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="rps", aliases=["Rps", "RPS", "RPs", "rPs", "rpS"])
    async def rps(ctx):
        logging.info(f"RPS game started by: {ctx.author}")

        # Ask if they want to play with a friend
        await ctx.send("👥 Do you want to play with a friend? (yes/no)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            play_with_friend = msg.content.lower() in ["yes", "y"]
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Starting solo game...")
            play_with_friend = False

        if play_with_friend:
            await ctx.send(
                "👤 Mention the friend you want to play with! (e.g., `@Friend`)"
            )

            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                if msg.mentions:
                    opponent = msg.mentions[0]
                    if opponent == ctx.author:
                        await ctx.send("❌ You can't play against yourself!")
                        return
                    if opponent.bot:
                        await ctx.send(
                            "❌ You can't play against a bot! Use solo mode instead."
                        )
                        return

                    await multiplayer_rps(ctx, bot, opponent)
                else:
                    await ctx.send("❌ No user mentioned! Starting solo game...")
                    await solo_rps(ctx, bot)
            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Starting solo game...")
                await solo_rps(ctx, bot)
        else:
            await solo_rps(ctx, bot)


async def solo_rps(ctx, bot):
    """Play RPS against the computer."""
    choices = ["rock", "paper", "scissors"]
    player_score = 0
    computer_score = 0

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send(
        "🎮 **Rock Paper Scissors** - First to 3 wins!\nType `rock`, `paper`, or `scissors`. Type `quit` to stop."
    )

    while player_score < 3 and computer_score < 3:
        # Single message with score AND prompt
        await ctx.send(
            f"🏆 Score: You **{player_score}** | Computer **{computer_score}**\n"
            f"🎯 Your choice (`rock`/`paper`/`scissors`):"
        )

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            choice = msg.content.lower()

            if choice == "quit":
                await ctx.send("👋 Game cancelled!")
                return

            if choice not in choices:
                await ctx.send("❌ Invalid! Choose: `rock`, `paper`, or `scissors`")
                continue

            computer = random.choice(choices)

            # Determine result
            if choice == computer:
                result = "😐 Tie!"
            elif (
                (choice == "rock" and computer == "scissors")
                or (choice == "paper" and computer == "rock")
                or (choice == "scissors" and computer == "paper")
            ):
                result = "✅ You win this round!"
                player_score += 1
            else:
                result = "❌ Computer wins this round!"
                computer_score += 1

            # Single message with round result
            await ctx.send(f"🤖 Computer chose: **{computer}**\n" f"{result}")

            await asyncio.sleep(1)

        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Game cancelled.")
            return

    # Final result
    if player_score == 3:
        await ctx.send(f"\n🎉🎉🎉 **YOU WIN!** {player_score}-{computer_score} 🎉🎉🎉")
    else:
        await ctx.send(f"\n💻 **COMPUTER WINS!** {computer_score}-{player_score} 💻")

    logging.info(
        f"RPS game ended: {ctx.author} - Final score {player_score}-{computer_score}"
    )
    await ask_play_again(ctx, bot, solo_rps)


async def multiplayer_rps(ctx, bot, opponent):
    """Play RPS against another player. Updates in DMs, final result in channel."""
    choices = ["rock", "paper", "scissors"]
    player1 = ctx.author
    player2 = opponent
    player1_score = 0
    player2_score = 0

    await ctx.send(
        f"🎮 **{player1.display_name} vs {player2.display_name}** - First to 3 wins!"
    )
    await ctx.send(f"{player2.mention}, do you accept the challenge? (yes/no)")

    def check_opponent(m):
        return m.author == player2 and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check_opponent)
        if msg.content.lower() not in ["yes", "y"]:
            await ctx.send(f"❌ {player2.display_name} declined. Game cancelled.")
            return
    except asyncio.TimeoutError:
        await ctx.send(f"⏰ {player2.display_name} didn't respond. Game cancelled.")
        return

    await ctx.send(
        f"✅ Challenge accepted! **{player1.display_name} vs {player2.display_name}**"
    )
    await ctx.send("📩 Game updates will be sent to your DMs!")

    # Send initial DM to both players
    await player1.send(
        f"🎮 **RPS Game: You vs {player2.display_name}**\nFirst to 3 wins!\n"
    )
    await player2.send(
        f"🎮 **RPS Game: You vs {player1.display_name}**\nFirst to 3 wins!\n"
    )

    while player1_score < 3 and player2_score < 3:
        # Get choices from both players via DM
        await player1.send("🎯 Your turn! Type `rock`, `paper`, or `scissors`:")
        player1_choice = await get_choice_dm(bot, player1, choices)
        if player1_choice is None:
            await ctx.send(f"❌ {player1.mention} took too long. Game cancelled.")
            await player2.send(
                f"❌ {player1.display_name} took too long. Game cancelled."
            )
            return
        logging.info(f"{player1.display_name} chose {player1_choice}")

        await player2.send("🎯 Your turn! Type `rock`, `paper`, or `scissors`:")
        player2_choice = await get_choice_dm(bot, player2, choices)
        if player2_choice is None:
            await ctx.send(f"❌ {player2.mention} took too long. Game cancelled.")
            await player1.send(
                f"❌ {player2.display_name} took too long. Game cancelled."
            )
            return
        logging.info(f"{player2.display_name} chose {player2_choice}")

        # Determine round winner
        if player1_choice == player2_choice:
            result = "😐 Tie!"
        elif (
            (player1_choice == "rock" and player2_choice == "scissors")
            or (player1_choice == "paper" and player2_choice == "rock")
            or (player1_choice == "scissors" and player2_choice == "paper")
        ):
            result = f"✅ {player1.display_name} wins this round!"
            player1_score += 1
        else:
            result = f"✅ {player2.display_name} wins this round!"
            player2_score += 1

        # Send round result to BOTH players' DMs
        round_msg = f"""
**Round Result:**
{player1.display_name} chose **{player1_choice}**
{player2.display_name} chose **{player2_choice}**
{result}
🏆 Score: {player1.display_name} **{player1_score}** | {player2.display_name} **{player2_score}**
"""
        await player1.send(round_msg)
        await player2.send(round_msg)

        await asyncio.sleep(1)

    # Game over - send final result to CHANNEL
    if player1_score == 3:
        final_msg = f"\n🎉🎉🎉 **{player1.display_name} WINS THE GAME!** {player1_score}-{player2_score} 🎉🎉🎉"
    else:
        final_msg = f"\n🎉🎉🎉 **{player2.display_name} WINS THE GAME!** {player2_score}-{player1_score} 🎉🎉🎉"

    await ctx.send(final_msg)

    # Also DM final result
    await player1.send(f"**GAME OVER**\n{final_msg}")
    await player2.send(f"**GAME OVER**\n{final_msg}")

    logging.info(
        f"RPS Multiplayer ended: {player1.display_name} vs {player2.display_name} - {player1_score}-{player2_score}"
    )


async def get_choice_dm(bot, player, choices):
    """Get a player's choice via DM."""
    try:

        def check_dm(m):
            return m.author == player and isinstance(m.channel, discord.DMChannel)

        msg = await bot.wait_for("message", timeout=30.0, check=check_dm)
        choice = msg.content.lower()

        if choice in choices:
            await player.send(f"✅ You chose **{choice}**!")
            return choice
        else:
            await player.send("❌ Invalid choice! Randomly selecting...")
            return random.choice(choices)

    except asyncio.TimeoutError:
        await player.send("⏰ Time's up! Randomly selecting...")
        return random.choice(choices)


async def ask_play_again(ctx, bot, game_func):
    """Ask if the player wants to play again."""

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("\nPlay again? (yes/no)")
    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.lower() in ["yes", "y"]:
            await game_func(ctx, bot)
        else:
            await ctx.send("Thanks for playing!")
    except asyncio.TimeoutError:
        await ctx.send("Thanks for playing!")
