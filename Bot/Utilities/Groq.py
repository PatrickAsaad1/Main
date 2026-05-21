import os
import discord
from dotenv import load_dotenv
from groq import Groq
from Utils.Logger import setup_logging

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logging = setup_logging()

conversations = {}


def setup(bot):

    # ==========================================
    # SLASH COMMAND: /ask
    # ==========================================
    @bot.tree.command(name="ask", description="Ask Groq AI a question.")
    async def ask(interaction: discord.Interaction, msg: str):
        """Ask Groq AI a question."""
        logging.info(f"{interaction.user} used Groq: {msg[:50]}")

        if not GROQ_API_KEY:
            await interaction.response.send_message(
                "❌ This feature is currently unavailable. Please contact the bot owner.",
                ephemeral=True,
            )
            logging.error("Groq API key not found")
            return

        # Defer response since AI generation can take longer than Discord's 3-second limit
        await interaction.response.defer()

        user_id = interaction.user.id

        if user_id not in conversations:
            conversations[user_id] = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Keep answers concise.",
                }
            ]

        conversations[user_id].append({"role": "user", "content": msg})

        try:
            ai_reply = await get_ai_response(user_id)

            if len(ai_reply) > 1900:
                ai_reply = ai_reply[:1900] + "..."

            await interaction.followup.send(ai_reply)

        except Exception as e:
            await interaction.followup.send(
                "❌ Could not fetch AI response. Try again later!"
            )
            logging.error(f"Groq error: {e}")

    # ==========================================
    # SLASH COMMAND: /forget
    # ==========================================
    @bot.tree.command(
        name="forget", description="Clear your conversation history with Groq AI."
    )
    async def forget(interaction: discord.Interaction):
        """Clear your conversation history."""
        user_id = interaction.user.id
        if user_id in conversations:
            conversations[user_id] = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Keep answers concise.",
                }
            ]
        await interaction.response.send_message("🧹 Conversation history cleared!")
        logging.info(f"{interaction.user} cleared their Groq conversation history")

    # ==========================================
    # ON MESSAGE EVENT: Reply to bot & @mention
    # ==========================================
    @bot.event
    async def on_message(message: discord.Message):
        # Ignore messages from the bot itself
        if message.author == bot.user:
            return

        # Still process prefix commands (like !setchannel etc.)
        await bot.process_commands(message)

        if not GROQ_API_KEY:
            return

        user_id = message.author.id
        should_respond = False
        user_msg = None

        # CHECK 1: Reply to the bot's message
        if message.reference and message.reference.resolved:
            replied_to = message.reference.resolved
            if replied_to.author == bot.user:
                # Get the text after removing the mention/ping if any
                user_msg = message.content.strip()
                if user_msg:
                    should_respond = True
                    logging.info(f"{message.author} replied to bot: {user_msg[:50]}")

        # CHECK 2: @mention the bot
        if not should_respond and bot.user in message.mentions:
            # Remove the @mention from the message
            user_msg = (
                message.content.replace(f"<@{bot.user.id}>", "")
                .replace(f"<@!{bot.user.id}>", "")
                .strip()
            )
            if user_msg:
                should_respond = True
                logging.info(f"{message.author} mentioned bot: {user_msg[:50]}")

        if not should_respond:
            return

        # Initialize conversation if needed
        if user_id not in conversations:
            conversations[user_id] = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Keep answers concise.",
                }
            ]

        conversations[user_id].append({"role": "user", "content": user_msg})

        # Show typing indicator while generating
        async with message.channel.typing():
            try:
                ai_reply = await get_ai_response(user_id)

                if len(ai_reply) > 1900:
                    ai_reply = ai_reply[:1900] + "..."

                # Reply to the user's message
                await message.reply(ai_reply)

            except Exception as e:
                await message.reply("❌ Could not fetch AI response. Try again later!")
                logging.error(f"Groq error (on_message): {e}")


# ==========================================
# HELPER: Get AI response from Groq
# ==========================================
async def get_ai_response(user_id: int) -> str:
    """Get AI response and update conversation history."""
    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversations[user_id],
        max_tokens=1000,
    )

    ai_reply = response.choices[0].message.content
    conversations[user_id].append({"role": "assistant", "content": ai_reply})

    return ai_reply
