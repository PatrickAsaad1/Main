# games/cafe.py
import time
import os
from Utils.Logger import setup_logging
from datetime import datetime
from Utils.Helpers import return_to_menu, returnx
from Utils.Screen import clear

logging = setup_logging()


def show_order_summary(orders, total_price):
    """Display order summary."""
    print("\n" + "=" * 40)
    print("📋 YOUR ORDER SUMMARY")
    print("=" * 40)
    for item in orders:
        item_total = item["quantity"] * item["price"]
        print(f"  {item['quantity']} x {item['item']}: ${item_total:.2f}")
    print("-" * 40)
    print(f"💰 TOTAL: ${total_price:.2f}")
    print("=" * 40)


def save_order_summary(orders, total_price, name):
    """Save order to file for company records."""
    try:
        # Get the script directory and create data folder path
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(script_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, "cafe_orders.txt")

        with open(file_path, "a") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"ORDER FROM: {name}\n")
            f.write(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'-'*30}\n")
            for item in orders:
                f.write(
                    f"{item['quantity']} x {item['item']}: ${item['quantity'] * item['price']:.2f}\n"
                )
            f.write(f"TOTAL: ${total_price:.2f}\n")
            f.write(f"{'='*50}\n")
        print("\n✅ Order saved to data/cafe_orders.txt")
        logging.info(f"Order saved: {len(orders)} items, total ${total_price:.2f}")
        return True
    except (IOError, OSError) as e:
        logging.error(f"Failed to save order: {e}")
        print(f"\n❌ Could not save order: {e}")
        return False


def run(name):
    """Cafe ordering system."""
    logging.info("User selected cafe system")
    max_quantities = {"pizza": 10, "burger": 15, "tea": 50, "coffee": 50, "latte": 50}
    DEFAULT_MAX_QTY = 50
    menu_prices = {"pizza": 8, "burger": 7, "tea": 2, "coffee": 3, "latte": 4}
    menu_items = ", ".join(menu_prices.keys())

    print("\n" + "=" * 40)
    print("     Welcome to Pat Cafe!")
    print("=" * 40)
    time.sleep(2)
    print(f"\nWelcome {name} to Pat Cafe, Thanks for coming in!\n")
    time.sleep(2)

    orders = []
    total_price = 0

    while True:
        print(
            f"\n{name}, what do you want today? That's what we are serving:\n{menu_items}\n"
        )
        order = (
            input("Your order: (type 'Return' to return to main menu) ").lower().strip()
        )
        if order == "return":
            if orders:
                save_choice = (
                    input(
                        "\nYou have items in your order. Save before leaving? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if save_choice in ["y", "yes"]:
                    show_order_summary(orders, total_price)
                    save_order_summary(orders, total_price, name)
            return_to_menu()
            return
        if order not in menu_prices:
            print(f"\nSorry, we don't have '{order}' on the menu. Try again.\n")
            logging.warning(f"User requested invalid item: {order}")
            continue

        max_qty = max_quantities.get(order, DEFAULT_MAX_QTY)
        if order == "pizza":
            print("\n🍕 Great choice! Pizza is delicious!")
        elif order == "burger":
            print("\n🍔 Yummy! Burgers are always a good idea!")
        else:
            print(f"\n☕ {order.title()} is a perfect pick-me-up!")

        while True:
            qty_input = input(f"How many {order} would you like? ").strip().lower()
            if qty_input == "return":
                if orders:
                    save_choice = (
                        input(
                            "\nYou have items in your order. Save before leaving? (y/n): "
                        )
                        .strip()
                        .lower()
                    )
                    if save_choice in ["y", "yes"]:
                        show_order_summary(orders, total_price)
                        save_order_summary(orders, total_price, name)
                return_to_menu()
                return
            if not qty_input.isdigit():
                print("Please enter a valid number!")
                continue
            qty = int(qty_input)
            if qty <= 0:
                print("Please enter a positive number!")
            elif qty > max_qty:
                print(f"Sorry, we can only serve up to {max_qty} {order}s at a time.")
            else:
                break

        orders.append({"item": order, "quantity": qty, "price": menu_prices[order]})
        total_price += qty * menu_prices[order]

        if qty > 1 and order not in ["tea", "coffee", "latte"]:
            item_word = order + "s"
        else:
            item_word = order
        print(f"\n✓ Added {qty} {item_word} to your order.")
        logging.info(
            f"Added {qty} x {order} to order. Current total: ${total_price:.2f}"
        )

        more = (
            input("\nWould you like to order something else? (y/n): ").strip().lower()
        )
        if more not in ["y", "yes"]:
            break

    if orders:
        show_order_summary(orders, total_price)
        save_success = save_order_summary(orders, total_price, name)
        if save_success:
            see_history = (
                input("\n📜 Would you like to see ALL past orders? (y/n): ")
                .strip()
                .lower()
            )
            if see_history in ["y", "yes"]:
                script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                file_path = os.path.join(script_dir, "data", "cafe_orders.txt")
                try:
                    with open(file_path, "r") as f:
                        content = f.read()
                    if not content.strip():
                        print("\n📭 No past orders found.")
                    else:
                        print("\n" + "=" * 50)
                        print("📜 ORDER HISTORY")
                        print("=" * 50)
                        print(content)
                        print("=" * 50)
                except FileNotFoundError:
                    print("\n📭 No past orders found.")
                except Exception as e:
                    print(f"\n❌ Error reading order history: {e}")
                    logging.error(f"Error reading order history: {e}")
