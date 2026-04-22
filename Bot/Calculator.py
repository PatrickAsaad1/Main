# Bot_games/calculator.py (Upgraded)
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="calc", aliases=["Calc", "CALC", "calculate", "Calculate"])
    async def calc(ctx, *, expression: str = None):
        """Calculator: $calc 5+3 or $calc 5 + 3 + 2"""
        logging.info(f"Calc by {ctx.author}: {expression}")

        if not expression:
            await ctx.send("❌ Usage: `$calc 5 + 3` or `$calc 5+3`")
            return

        # Replace symbols
        expression = expression.replace("x", "*").replace("×", "*").replace("÷", "/")

        # Check if it's a simple no-space expression like "5+3"
        if " " not in expression:
            # Find the operator
            for op in ["+", "-", "*", "/"]:
                if op in expression:
                    parts = expression.split(op)
                    if len(parts) == 2:
                        try:
                            num1 = float(parts[0])
                            num2 = float(parts[1])
                        except ValueError:
                            await ctx.send("❌ Invalid numbers!")
                            return

                        if op == "+":
                            result = num1 + num2
                        elif op == "-":
                            result = num1 - num2
                        elif op == "*":
                            result = num1 * num2
                        elif op == "/":
                            if num2 == 0:
                                await ctx.send("❌ Can't divide by zero!")
                                return
                            result = num1 / num2

                        await ctx.send(f"🧮 {expression} = {result}")
                        return
            await ctx.send("❌ Invalid format! Use `$calc 5+3` or `$calc 5 + 3 + 2`")
            return

        # Multiple operations with spaces: "5 + 3 + 2"
        parts = expression.split()

        # Validate alternating number-operator-number pattern
        if len(parts) < 3 or len(parts) % 2 == 0:
            await ctx.send("❌ Invalid format! Example: `$calc 5 + 3 + 2`")
            return

        # Check all odd indices are operators
        for i in range(1, len(parts), 2):
            if parts[i] not in ["+", "-", "*", "/"]:
                await ctx.send(f"❌ Invalid operator: {parts[i]}")
                return

        # Calculate left-to-right
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
                        await ctx.send("❌ Can't divide by zero!")
                        return
                    result /= num

            await ctx.send(f"🧮 {expression} = {result}")

        except ValueError:
            await ctx.send("❌ Invalid numbers!")
