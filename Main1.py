# just to make the user know it's just a practice
import time
import os
import logging
import random
from datetime import datetime

try:
    try:
        import json

        json = True
    except ImportError:
        print("json is not installed. Please install it using 'pip install json'")
        json = False
        quotes = False
    try:
        import requests

        requests = True
    except ImportError:
        requests = False
        quotes = False
    if json and requests == True:
        quotes = True
except ImportError:
    print()
try:
    import cryptography.fernet as fernet

    fernet_available = True
except ImportError:
    print(
        "cryptography.fernet is not installed. Please install it using 'pip install cryptography'"
    )
    print("Or with 'python -m pip install cryptography' if 'pip' is not recognized.")
    print("Without cryptography.fernet, the encrypt/decrypt feature will be disabled.")
    fernet_available = False
try:
    import cowsay

    cowsay_available = True
except ImportError:
    print("cowsay is not installed. Please install it using 'pip install cowsay'")
    print("Or with 'python -m pip install cowsay' if 'pip' is not recognized.")
    print("without cowsay, the cow feature will be disabled.")
    cowsay_available = False
    cowsay = None
    time.sleep(2)

script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "game.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_path)],
)


def return_to_menu():
    """Handle returning to main menu with logging and delay."""
    print("Returning to main menu...")
    logging.info("User returned to main menu")
    time.sleep(1)


def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def get_name():
    """Prompt user for their name and display a welcome message."""
    print("=" * 40)
    print("Welcome! (This is just practice)")
    print("=" * 40)
    time.sleep(2)
    while True:
        name = input("What is your name? ").strip()
        if name:
            name = name.title()
            logging.info("User entered their name")
            logging.info(f"User's name is: {name}")
            break
        else:
            print("Please enter a valid name!")
            logging.error("User didn't put a name")
            time.sleep(2)
            continue
    clear()
    print(
        f"Welcome {name}, thank you for trying this :) I hope you have fun playing with it!"
    )
    time.sleep(2)
    return name


def returnx(x):
    if x == "return":
        return_to_menu()
        return True
    return False


def mainmenu(name):
    """Display the main menu and return user's choice."""
    clear()
    print(f"{name}, choose something!")
    print()
    print("1. Age checker")
    print("2. Calculator")
    print("3. Cafe system")
    print("4. Guessing game")
    print("5. Big text search")
    print("6. Rock-Paper-Scissors Game")
    print("7. Encrypt / Decrypt messages")
    print("8. Random picker wheel")
    print("9. Number guessing game")
    print("10. Password generator")
    print("11. Exit")
    return input("Enter your choice: ")


def password():
    manypass = input("How many passwords do you want to generate? ")
    while True:
        if returnx(manypass):
            return
        if not manypass.isdigit():
            print("Please enter a number!")
            manypass = input("How many passwords? ")
            continue
        manypass = int(manypass)
        break
    manychar = input("How many characters? ")
    while True:
        if returnx(manychar):
            return
        if not manychar.isdigit():
            print("Please enter a number!")
            manychar = input("How many characters? ")
            continue
        manychar = int(manychar)
        break
    characters = (
        "!@#$%&*_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    )
    for i in range(manypass):
        password = ""
        for j in range(manychar):
            password += random.choice(characters)
        print(f"Password {i+1}: {password}")


def age_checker():
    """Calculate user's age from their birth year."""
    logging.info("User selected age checker")
    while True:
        birth = (
            input("What is your birth year? (type 'return' to return to main menu) ")
            .strip()
            .lower()
        )
        if returnx(birth):
            return
        try:
            birth_year = int(birth)
            current_year = datetime.now().year
            age = current_year - birth_year
            if age < 0:
                print("You haven't been born yet? ")
                logging.warning(
                    f"User entered a birth year in the future: {birth_year}"
                )
                continue
            elif age > 150:
                print(f"{age} years old? You must be a record holder!")
                logging.warning(f"User entered an age over 150: {age}")
                continue
            else:
                print(f"Your age is {age}")
                logging.info(f"User's age calculated: {age}")
            break
        except ValueError:
            print("Please enter a valid year (numbers only)!")
            logging.error(f"User entered invalid birth year: {birth}")
            continue


def calculator():
    """Simple calculator that performs basic operations on two numbers."""
    logging.info("User selected calculator")
    while True:
        try:
            raw_input = (
                input(
                    "What is the first number? (type 'return' to return to main menu) "
                )
                .strip()
                .lower()
            )
            if returnx(raw_input):
                return
            num1 = float(raw_input)
            op = input("What is the operation (+ - x * /)? ").strip().lower()
            # Get second number based on operation
            if op == "/":
                while True:
                    raw_num2 = input("What is the second number? ").strip().lower()
                    if returnx(raw_num2):
                        return
                    try:
                        num2 = float(raw_num2)
                        if num2 == 0:
                            print("Can't divide by zero! Try again.")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid number!")
            elif op in ["+", "-", "x", "*"]:
                raw_num2 = input("What is the second number? ").strip().lower()
                if returnx(raw_num2):
                    return
                num2 = float(raw_num2)
            else:
                print("Please enter a valid operator (+, -, x, *, /)!")
                logging.error(f"User entered invalid operator: {op}")
                time.sleep(2)
                continue
            # Calculate result
            if op == "+":
                result = num1 + num2
            elif op == "-":
                result = num1 - num2
            elif op in ["x", "*"]:
                result = num1 * num2
            elif op == "/":
                result = num1 / num2
            print(f"\nThe answer is {result:<10.2f}")
            logging.info(f"Calculated result: {num1} {op} {num2} = {result}")
            choice = input("Wanna try it again (y/n)? ").strip().lower()
            if choice in ["yes", "y"]:
                clear()
                continue
            break
        except ValueError:
            print("Please enter valid numbers!")
            logging.error("User entered invalid numbers for calculation")
            continue


def cafe_system(name):
    """Cafe ordering system where users can order items and see the total price."""
    logging.info("User selected cafe system")
    max_quantities = {"pizza": 10, "burger": 15, "tea": 50, "coffee": 50, "latte": 50}
    DEFAULT_MAX_QTY = 50
    menu_prices = {"pizza": 8, "burger": 7, "tea": 2, "coffee": 3, "latte": 4}
    menu_items = ", ".join(menu_prices.keys())
    print("\n" + "=" * 40)
    print("     Welcome to Pat Cafe!")
    print("=" * 40)
    time.sleep(2)
    print(f"\nWelcome {name} to Pat Cafe, thanks for coming in!\n")
    time.sleep(2)
    orders = []
    total_price = 0
    while True:
        print(
            f"\n{name}, what do you want today? That's what we are serving:\n{menu_items}\n"
        )
        order = (
            input("Your order: (type 'return' to return to main menu) ").lower().strip()
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
        # Special message and max quantity
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
        # Add to orders
        orders.append({"item": order, "quantity": qty, "price": menu_prices[order]})
        total_price += qty * menu_prices[order]
        # Pluralisation fix: drinks usually don't need an 's' even if you have more than one
        if qty > 1 and order not in ["tea", "coffee", "latte"]:
            item_word = order + "s"
        else:
            item_word = order
        print(f"\n✓ Added {qty} {item_word} to your order.")
        logging.info(
            f"Added {qty} x {order} to order. Current total: ${total_price:.2f}"
        )
        # Ask if they want more
        more = (
            input("\nWould you like to order something else? (y/n): ").strip().lower()
        )
        if more not in ["y", "yes"]:
            break
    # After showing summary and saving (only once here)
    if orders:
        show_order_summary(orders, total_price)
        save_success = save_order_summary(orders, total_price, name)
        # Only ask to view history if save actually worked
        if save_success:
            see_history = (
                input("\n📜 Would you like to see ALL past orders? (y/n): ")
                .strip()
                .lower()
            )
            if see_history in ["y", "yes"]:
                file_path = "cafe_orders.txt"
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
    """Save order to file for company records. Returns True if successful, False if failed."""
    try:
        with open("cafe_orders.txt", "a") as f:
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
        print("\n✅ Order saved to cafe_orders.txt")
        logging.info(f"Order saved: {len(orders)} items, total ${total_price:.2f}")
        return True
    except (IOError, OSError) as e:
        logging.error(f"Failed to save order: {e}")
        print(f"\n❌ Could not save order: {e}")
        print("Your order was NOT saved. Please try again or contact staff.")
        return False


def number_game():
    number = random.randint(1, 20)
    print("I will think of a number from 1 - 20 and you try to guess it")
    time.sleep(1)
    print("Type 'return' to return to main menu | Note: You have only 5 attempts")
    print()
    time.sleep(0.5)
    attempts = 0
    while attempts < 5:
        print(f"Attempt {attempts+1}/5")
        uguess = input("What is the number I'm guessing? ").strip().lower()
        if returnx(uguess):
            return
        if not uguess.isdigit():
            print("Please enter a number between 1 - 20")
            logging.warning(f"User entered invalid guess: {uguess}")
            time.sleep(2)
            continue
        uguess = int(uguess)
        if uguess < 1 or uguess > 20:
            print("Please enter a number between 1 - 20")
            logging.warning(f"User entered out of range guess: {uguess}")
            time.sleep(2)
            continue
        attempts += 1
        if uguess < number:
            print("Too low, try again")
            print()
            logging.info(f"User guessed {uguess}, which is too low")
        elif uguess > number:
            print("Too high, try again")
            print()
            logging.info(f"User guessed {uguess}, which is too high")
        else:
            print("You got it right!")
            logging.info(f"User guessed the number correctly: {number}")
            break
    else:
        print(f"You lost! The number was {number}")
        logging.info(f"User lost the number guessing game. The number was {number}")


def guessing_game():
    """Number guessing game - guess correctly to reach 3 points."""
    logging.info("User selected guessing game")
    score = 0
    difficulty_ranges = {
        "easy": (1, 3),
        "med": (1, 5),
        "medium": (1, 5),
        "hard": (1, 10),
    }
    print(
        "\nEvery time you guess right, you get +1 point! Wrong guess loses a point (if you have any)."
    )
    time.sleep(1)
    while True:
        game = input("Choose difficulty (easy / med / hard): ").strip().lower()
        if game in difficulty_ranges:
            low, high = difficulty_ranges[game]
            print(f"\nGreat! I'll pick a number between {low} and {high}")
            break
        elif returnx(game):
            return
        else:
            print("Please choose easy, med, or hard")
    print(f"\nTry to reach 3 points to win! (type 'return' to return to main menu)")
    while score < 3:
        rnum = random.randint(low, high)
        user_input = input(f"\nGuess the number ({low}-{high}): ").strip().lower()
        if returnx(user_input):
            return
        try:
            unum = int(user_input)
        except ValueError:
            print("Please enter a number!")
            continue
        if unum < low or unum > high:
            print(f"Please enter a number from {low} to {high}!")
            continue
        print(f"\nThe number was: {rnum}")
        if unum == rnum:
            print("You got it right :)")
            score += 1
            logging.info(f"User guessed correctly. Score: {score}/3")
        else:
            print("Wrong guess, try again!")
            if score > 0:
                score -= 1
            logging.info(f"User guessed incorrectly. Score: {score}/3")
        print(f"Your score is {score}/3")
    print("\n🎉 You won! Reached 3 points!")
    logging.info("User won the guessing game.")


def text_search():
    """Search for a word in a large text block."""
    logging.info("User selected text search")
    while True:
        print(
            "Drop a big chunk of text below, then tell me a word and I'll hunt it down for you!"
        )
        print()
        time.sleep(2)
        fat_text_input = (
            input("Paste your text here: (type 'return' to go back) ").strip().lower()
        )
        if returnx(fat_text_input):
            return
        if len(fat_text_input) > 50000:
            print(
                "⚠️ Warning: Very large text detected. This might slow down the search."
            )
            confirm = input("Continue anyway? (y/n): ").strip().lower()
            if confirm != "y":
                return_to_menu()
                return
        if fat_text_input == "":
            print("You didn't enter any text! Returning to main menu...")
            logging.warning("User entered empty text for search")
            time.sleep(2)
            return
        search_word = (
            input(
                "What word do you want to search for? (type 'return' to return to main menu) "
            )
            .strip()
            .lower()
        )
        if returnx(search_word):
            return
        if search_word == "":
            print("You didn't enter any word! Returning to main menu...")
            logging.warning("User entered empty word for search")
            time.sleep(2)
            return
        if search_word in fat_text_input:
            print(f"\n✅ Found '{search_word}' in the text!")
            logging.info(f"User found the word '{search_word}' in the text")
            time.sleep(2)
        else:
            print(f"❌ '{search_word}' not found in the text.")
            logging.info(f"User did not find the word '{search_word}' in the text")
            time.sleep(2)
        while True:
            secret = (
                input("\nDo you want to see a secret word reverser? (y/n): ")
                .strip()
                .lower()
            )
            if secret in ["y", "yes"]:
                print("\nSo you will need to put a word and it will be reversed :)")
                word = input("Enter a word to reverse: ").strip()
                if word:
                    print(f"\nThe reversed word is: {word[::-1]}")
                    logging.info(f"User reversed the word '{word}'")
                else:
                    print("No word entered.")
                break
            elif secret in ["n", "no"]:
                break
            else:
                print("Please enter y or n")
                continue
        again = (
            input("\nDo you want to search for another word? (y/n): ").strip().lower()
        )
        if again in ["y", "yes"]:
            clear()
            continue
        else:
            return_to_menu()
            return


def rock_paper_scissors():
    """Rock-Paper-Scissors game against the computer, first to 3 points wins."""
    logging.info("User selected rock-paper-scissors")
    gchoices = ["rock", "paper", "scissors"]

    def play_again_prompt():
        """Ask user if they want to play again. Returns True if yes."""
        while True:
            again = input("Play again? (y/n): ").strip().lower()
            if again in ["y", "yes"]:
                logging.info("User chose to play again")
                return True
            elif again in ["n", "no"]:
                logging.info("User chose not to play again")
                return False
            else:
                print("Please enter y or n")

    while True:
        player_score = 0
        computer_score = 0
        print("Rock-Paper-Scissors Game!")
        print("First to 3 points wins. Type 'return' to return to main menu\n")
        while player_score < 3 and computer_score < 3:
            player = input("Rock, paper, or scissors? ").lower()
            if returnx(player):
                return
            if player not in gchoices:
                print("Invalid choice. Please choose rock, paper, or scissors.\n")
                continue
            computer = random.choice(gchoices)
            print(f"Computer chose: {computer}")
            if player == computer:
                print("Tie!")
            elif (
                (player == "rock" and computer == "scissors")
                or (player == "paper" and computer == "rock")
                or (player == "scissors" and computer == "paper")
            ):
                print("You won this round!")
                player_score += 1
            else:
                print("You lost this round!")
                computer_score += 1
            print(f"Score - You: {player_score} | Computer: {computer_score}\n")
            time.sleep(1)
            clear()
        if player_score == 3:
            print("🎉 Congratulations! You won the game!")
        else:
            print("💻 Computer wins the game!")
        if not play_again_prompt():
            print("\nThanks for playing!")
            return


def random_picker():
    """Create a list of items and randomly pick from it."""
    logging.info("User selected random picker")
    choices = []
    print("===== RANDOM PICKER WHEEL =====")
    print("Commands: 'done' = finish list, 'return' to return to main menu\n")
    while True:
        user_input = input(f"Enter item #{len(choices)+1}: ").strip()
        if returnx(user_input):
            return
        if user_input.lower() == "done":
            logging.info("User finished building the list for random picker")
            break
        if user_input:
            choices.append(user_input)
        else:
            print("Please enter a valid item!")
            logging.warning(
                f"User entered invalid item for random picker: {user_input}"
            )
            time.sleep(2)
    if not choices:
        print("\nYou didn't enter any items!")
        logging.warning("User tried to use random picker without entering any items")
        time.sleep(2)
        return
    print(f"\nYour list: {', '.join(choices)}")
    while True:
        winner = random.choice(choices)
        print(f"\n🎲 The computer picks: --- {winner} ---")
        pick_another = (
            input("\nPick again? (y/n or 'return' to return to main menu): ")
            .strip()
            .lower()
        )
        if returnx(pick_another):
            return
        elif pick_another in ["n", "no"]:
            print("\nThanks for using the random picker!")
            logging.info("User finished using the random picker")
            time.sleep(2)
            return
        elif pick_another not in ["y", "yes"]:
            print("Please enter y, n, or return.")
            logging.warning(
                f"User entered invalid input for random picker: {pick_another}"
            )
            time.sleep(2)
            continue


def encrypt_decrypt(name):
    """Encrypt or decrypt messages using Fernet."""
    logging.info("User selected encrypt/decrypt")
    print("\n1. Encrypt a message")
    print()
    print("2. Decrypt a message")
    print()
    print("3. Return to main menu")
    choice = input("Choose: ")
    while choice not in ["1", "2", "3"]:
        print("Invalid choice. Please enter 1, 2, or 3.")
        choice = input("Choose: ")
    if choice == "1":
        if not fernet_available:
            print(
                "\nSorry, the encryption feature is not available because cryptography.fernet is not installed."
            )
            logging.warning(
                "User attempted to use encrypt/decrypt feature without cryptography.fernet"
            )
            time.sleep(2)
            return
        key = fernet.Fernet.generate_key()
        cipher = fernet.Fernet(key)
        msg = input("\nEnter message to encrypt: ")
        encrypted = cipher.encrypt(msg.encode())
        print(f"\n🔒 Encrypted: {encrypted.decode()}")
        print("\n🔑 SAVE THIS KEY (without it, the message is lost forever):")
        print(key.decode())
        yes_no = (
            input("\nDo you want to save the key and the encrypted message? (y/n): ")
            .strip()
            .lower()
        )
        try:
            if yes_no in ["y", "yes"]:
                file_path = os.path.join(script_dir, "encrypted_data.txt")
                file_exists = os.path.exists(file_path)
                with open(file_path, "a") as f:
                    if not file_exists:
                        f.write("=" * 50 + "\n")
                        f.write("ENCRYPTED MESSAGE DATA\n")
                        f.write("=" * 50 + "\n\n")
                    else:
                        f.write("\n\n" + "-" * 50 + "\n")
                    f.write(
                        "⚠️ WARNING: Key stored with message - store key separately for real security!\n"
                    )
                    f.write(f"KEY:\n{key.decode()}\n\n")
                    f.write(f"MESSAGE:\n{encrypted.decode()}\n\n")
                print(f"\n✅ Saved to: {file_path}")
                logging.info("User saved key and encrypted message to file")
            elif yes_no in ["n", "no"]:
                print(
                    "\n⚠️ Remember, without saving the key and encrypted message, you won't be able to decrypt it later!"
                )
                logging.warning("User chose not to save the key and encrypted message")
            else:
                logging.info(
                    f"User entered invalid input for saving key and message: {yes_no}"
                )
            logging.info("User encrypted a message")
        except (IOError, OSError) as e:
            print(f"\n❌ Error saving the key and message: {e}")
            logging.error(f"Error saving the key and message: {e}")
    elif choice == "2":
        if not fernet_available:
            print(
                "\nSorry, the decryption feature is not available because cryptography.fernet is not installed."
            )
            logging.warning(
                "User attempted to use decrypt feature without cryptography.fernet"
            )
            time.sleep(2)
            return
        key_input = input(
            "\nEnter the key (paste exactly as shown during encryption): "
        ).strip()
        key = key_input.encode()
        encrypted_msg = input("Enter encrypted message: ").strip().encode()
        try:
            cipher = fernet.Fernet(key)
            decrypted = cipher.decrypt(encrypted_msg)
            print(f"\n🔓 Decrypted: {decrypted.decode()}")
            logging.info("User decrypted a message")
        except fernet.InvalidToken:
            print("\n❌ Invalid key or message. Decryption impossible.")
            logging.warning("User failed to decrypt - invalid key or message")
        except Exception as e:
            print("\n❌ Invalid key or message. Decryption impossible.")
            logging.warning(f"User failed to decrypt: {e}")
    elif choice == "3":
        return_to_menu()
        return


def main():
    """Main game loop that displays menu and runs selected mini-games."""
    try:
        name = get_name()
        while True:
            choice = mainmenu(name)
            if choice == "1":
                age_checker()
            elif choice == "2":
                calculator()
            elif choice == "3":
                cafe_system(name)
            elif choice == "4":
                guessing_game()
            elif choice == "5":
                text_search()
            elif choice == "6":
                rock_paper_scissors()
            elif choice == "7":
                encrypt_decrypt(name)
            elif choice == "8":
                random_picker()
            elif choice == "9":
                number_game()
            elif choice == "10":
                password()
            elif choice == "11":
                print("Goodbye!")
                logging.info("User exited the game")
                time.sleep(2)
                break
            else:
                print("Please choose a number from 1 to 10!")
            input("\nPress Enter to return to main menu... ")
        # Quote at the end
        if quotes:
            print("Here is a quote for you")
            try:
                response = requests.get("https://zenquotes.io/api/random")
                json_data = response.json()
                quote = f"💬 {json_data[0]['q']} — *{json_data[0]['a']}*"
                print(quote)
            except Exception as e:
                logging.error(f"Quote API error: {e}")
                print("❌ Could not fetch a quote right now. Try again later!")
        time.sleep(1)
        print("\n" + "=" * 40)
        print("I really hope you enjoyed that")
        print("=" * 40)
        print(
            "\nIf you want to see more of my projects or just wanna chat, find me on Discord! :)"
        )
        print("\nMy Discord user: just_pat123")
        print("Our server: https://discord.gg/vzYwPADbuj")
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! (Interrupted by user)")
        logging.info("User interrupted the program with KeyboardInterrupt")
        time.sleep(1)
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}", exc_info=True)
        print("\n⚠️  An unexpected error occurred. Check game.log for details.")
        time.sleep(3)


if __name__ == "__main__":
    main()
