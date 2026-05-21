import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="calc",
        description="Calculate a simple math expression. Example: /calc expression:5 + 3",
    )
    async def calc(interaction: discord.Interaction, expression: str):
        """Calculator: /calc expression:5+3 or /calc expression:5 + 3 + 2"""
        logging.info(f"Calc by {interaction.user}: {expression}")

        # Clean operators
        cleaned_expression = (
            expression.replace("x", "*").replace("×", "*").replace("÷", "/").strip()
        )

        if " " not in cleaned_expression:
            for op in ["+", "-", "*", "/"]:
                if op in cleaned_expression:
                    parts = cleaned_expression.split(op)
                    if len(parts) == 2:
                        try:
                            num1 = float(parts[0])
                            num2 = float(parts[1])
                        except ValueError:
                            await interaction.response.send_message(
                                "❌ Invalid numbers!"
                            )
                            return

                        if op == "+":
                            result = num1 + num2
                        elif op == "-":
                            result = num1 - num2
                        elif op == "*":
                            result = num1 * num2
                        elif op == "/":
                            if num2 == 0:
                                await interaction.response.send_message(
                                    "❌ Can't divide by zero!"
                                )
                                return
                            result = num1 / num2

                        await interaction.response.send_message(
                            f"🧮 {cleaned_expression} = {result}"
                        )
                        return

            await interaction.response.send_message(
                "❌ Invalid format! Use `/calc expression:5+3` or `/calc expression:5 + 3 + 2`"
            )
            return

        parts = cleaned_expression.split()

        if len(parts) < 3 or len(parts) % 2 == 0:
            await interaction.response.send_message(
                "❌ Invalid format! Example: `/calc expression:5 + 3 + 2`"
            )
            return

        for i in range(1, len(parts), 2):
            if parts[i] not in ["+", "-", "*", "/"]:
                await interaction.response.send_message(
                    f"❌ Invalid operator: {parts[i]}"
                )
                return

        try:
            result = float(parts[0])

            for i in range(1, len(parts), 2):
                op = parts[i]
                num = float(parts[i + 1])

                if op == "+":
                    result += num
                elif op == "-":
                    result -= num
                elif op == "*":
                    result *= num
                elif op == "/":
                    if num == 0:
                        await interaction.response.send_message(
                            "❌ Can't divide by zero!"
                        )
                        return
                    result /= num

            await interaction.response.send_message(
                f"🧮 {cleaned_expression} = {result}"
            )

        except ValueError:
            await interaction.response.send_message("❌ Invalid numbers!")
