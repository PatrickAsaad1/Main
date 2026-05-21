import asyncio
import discord
from Utils.Logger import setup_logging
from datetime import datetime
from Utils.Helpers import return_to_menu, returnx

logging = setup_logging()


def setup(bot):

    @bot.tree.command(
        name="cafe",
        description="Order food and drinks from Pat Cafe with a fun interactive system.",
    )
    async def cafe(interaction: discord.Interaction):
        """Cafe ordering system."""
        logging.info(f"{interaction.user} selected cafe system")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        max_quantities = {
            "pizza": 10,
            "burger": 15,
            "tea": 50,
            "coffee": 50,
            "latte": 50,
        }
        DEFAULT_MAX_QTY = 50
        menu_prices = {
            "pizza": 8,
            "burger": 7,
            "tea": 2,
            "coffee": 3,
            "latte": 4,
        }
        menu_items = ", ".join(menu_prices.keys())

        await interaction.response.send_message("Welcome to Pat Cafe!")

        orders = []
        total_price = 0

        while True:
            try:
                await interaction.channel.send(
                    f"{interaction.user.mention}, what do you want today? Here's what we are serving:\n{menu_items}"
                )
                order_msg = await bot.wait_for("message", timeout=30.0, check=check)

                if returnx(order_msg.content):
                    return

                order = order_msg.content.lower().strip()

                if order not in menu_prices:
                    await interaction.channel.send(
                        f"Sorry, we don't have '{order}' on the menu. Try again."
                    )
                    logging.warning(
                        f"{interaction.user} requested invalid item: {order}"
                    )
                    continue

                max_qty = max_quantities.get(order, DEFAULT_MAX_QTY)
                if order == "pizza":
                    await interaction.channel.send(
                        "🍕 Great choice! Pizza is delicious!"
                    )
                elif order == "burger":
                    await interaction.channel.send(
                        "🍔 Yummy! Burgers are always a good idea!"
                    )
                else:
                    await interaction.channel.send(
                        f"☕ {order.title()} is a perfect pick-me-up!"
                    )

            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ Time's up! Order cancelled.")
                return

            while True:
                try:
                    await interaction.channel.send(f"How many {order} would you like?")
                    qty_msg = await bot.wait_for("message", timeout=30.0, check=check)

                    if returnx(qty_msg.content):
                        return

                    qty_input = qty_msg.content.strip()

                    if not qty_input.isdigit():
                        await interaction.channel.send("Please enter a valid number!")
                        logging.warning("User put a non-number input")
                        continue

                    qty = int(qty_input)
                    if qty <= 0:
                        logging.warning("User put a negative number")
                        await interaction.channel.send(
                            "Please enter a positive number!"
                        )
                    elif qty > max_qty:
                        await interaction.channel.send(
                            f"Sorry, we can only serve up to {max_qty} {order}s at a time."
                        )
                        logging.warning(
                            f"User wanted to order {qty} {order} (max {max_qty})"
                        )
                    else:
                        break

                except asyncio.TimeoutError:
                    await interaction.channel.send("⏰ Time's up! Order cancelled.")
                    return

            orders.append(
                {
                    "item": order,
                    "quantity": qty,
                    "price": menu_prices[order],
                }
            )
            total_price += qty * menu_prices[order]

            if qty > 1:
                if order.endswith("y"):
                    item_word = order[:-1] + "ies"
                elif order in ["tea", "coffee", "latte"]:
                    item_word = order
                else:
                    item_word = order + "s"
            else:
                item_word = order

            await interaction.channel.send(f"✓ Added {qty} {item_word} to your order.")
            logging.info(
                f"Added {qty} x {order} to order. Current total: ${total_price:.2f}"
            )

            try:
                await interaction.channel.send(
                    "Would you like to order something else? (y/n):"
                )
                more_msg = await bot.wait_for("message", timeout=30.0, check=check)

                if returnx(more_msg.content):
                    return

                more = more_msg.content.lower().strip()
                if more not in ["y", "yes"]:
                    break
            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ Time's up! Finishing your order.")
                break

        if orders:
            summary_lines = [
                "\n" + "=" * 40,
                "     Your Order Summary",
                "=" * 40,
            ]
            for item in orders:
                summary_lines.append(
                    f"• {item['quantity']} x {item['item']}: ${item['quantity'] * item['price']:.2f}"
                )
            summary_lines.extend(
                [
                    "-" * 40,
                    f"Total: ${total_price:.2f}",
                    "=" * 40,
                    "Thank you for visiting Pat Cafe! ☕",
                ]
            )
            await interaction.channel.send("\n".join(summary_lines))
            logging.info(
                f"{interaction.user} completed order. Total: ${total_price:.2f}"
            )
        else:
            await interaction.channel.send("No items ordered. Come back soon!")
