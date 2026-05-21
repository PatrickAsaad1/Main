import discord
from Utils.Logger import setup_logging

logging = setup_logging()

MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    " ": "/",
}


def setup(bot):

    @bot.tree.command(name="morse", description="Convert text to Morse code.")
    async def morse(interaction: discord.Interaction, msg: str):
        logging.info(
            f"{interaction.user} used /morse command"
        )  # FIXED: added / for consistency

        encrypted_msg = ""
        for letter in msg.upper():
            if letter in MORSE_CODE_DICT:
                encrypted_msg += MORSE_CODE_DICT[letter] + " "
            else:
                encrypted_msg += " "

        if not encrypted_msg.strip():
            return await interaction.response.send_message(
                "Could not convert that text to morse code.", ephemeral=True
            )

        await interaction.response.send_message(f"`{encrypted_msg.strip()}`")
