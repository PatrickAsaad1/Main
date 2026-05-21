import asyncio
import discord
from Utils.Logger import setup_logging

try:
    from cryptography.fernet import Fernet, InvalidToken

    FERNET_AVAILABLE = True
except ImportError:
    FERNET_AVAILABLE = False
    print("⚠️ cryptography not installed. Encrypt/Decrypt features disabled.")
    print("Run: pip install cryptography")

logging = setup_logging()


def setup(bot):

    @bot.tree.command(name="encrypt", description="Encrypt a message using Fernet.")
    async def encrypt(interaction: discord.Interaction, msg: str):
        """Encrypt a message using Fernet."""
        logging.info(f"{interaction.user} selected encrypt")

        if not FERNET_AVAILABLE:
            await interaction.response.send_message(
                "❌ This feature is currently unavailable. Please contact the bot owner.",
                ephemeral=True,
            )
            return

        try:
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted = cipher.encrypt(msg.encode())

            try:
                await interaction.user.send(
                    f"🔒 **Encrypted:** `{encrypted.decode()}`\n"
                    f"🔑 **Key (SAVE THIS):** `{key.decode()}`\n"
                    "⚠️ Without this key, the message is lost forever!"
                )
                await interaction.response.send_message(
                    "✅ Check your DMs for the encrypted message and key!"
                )
                logging.info(f"{interaction.user} encrypted a message successfully")
            except discord.Forbidden:
                await interaction.response.send_message(
                    "❌ I couldn't DM you! Check your privacy settings.",
                    ephemeral=True,
                )
                logging.error(f"Couldn't DM {interaction.user} for encryption")

        except Exception as e:
            await interaction.response.send_message(
                "❌ Encryption failed!", ephemeral=True
            )
            logging.error(f"Encryption error: {e}")

    @bot.tree.command(name="decrypt", description="Decrypt a message using the key.")
    async def decrypt(interaction: discord.Interaction):
        """Decrypt a message using the key."""
        logging.info(f"{interaction.user} selected decrypt")

        if not FERNET_AVAILABLE:
            await interaction.response.send_message(
                "❌ This feature is currently unavailable. Please contact the bot owner.",
                ephemeral=True,
            )
            return

        def check(m):
            return m.author == interaction.user and isinstance(
                m.channel, discord.DMChannel
            )

        # Attempt to prompt the user in DMs first
        try:
            await interaction.user.send("🔒 Please enter the **encrypted message**:")
            # Acknowledge the slash command inside the guild channel safely
            await interaction.response.send_message(
                "✅ Check your DMs to continue decryption!"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I couldn't DM you! Check your privacy settings.",
                ephemeral=True,
            )
            return

        try:
            encrypted_msg = await bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await interaction.user.send("⏰ Time's up! Cancelled.")
            return

        try:
            await interaction.user.send("🔑 Please enter the **key**:")
            key_input = await bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await interaction.user.send("⏰ Time's up! Cancelled.")
            return

        try:
            key = key_input.content.encode()
            encrypted_bytes = encrypted_msg.content.encode()
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_bytes)

            await interaction.user.send(f"🔓 **Decrypted:** `{decrypted.decode()}`")
            logging.info(f"{interaction.user} decrypted a message successfully")

        except InvalidToken:
            await interaction.user.send(
                "❌ Invalid key or encrypted message!\n"
                "💡 Make sure you copied both EXACTLY as shown."
            )
            logging.warning(
                f"{interaction.user} failed to decrypt - invalid key or message"
            )
        except Exception as e:
            await interaction.user.send(
                "❌ Decryption failed! Check your key and message."
            )
            logging.warning(f"{interaction.user} failed to decrypt: {e}")
