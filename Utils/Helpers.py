# utils/helpers.py
import time
from Utils.Logger import setup_logging
from Utils.Screen import clear

logging = setup_logging()


def return_to_menu():
    """Handle returning to main menu with logging and delay."""
    print("Returning to main menu...")
    logging.info("User returned to main menu")
    time.sleep(1)


def returnx(x):
    """Check if user typed 'return'."""
    if x == "return":
        return_to_menu()
        return True
    return False


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
        f"Welcome {name}, Thank you for trying this :) I hope you have fun playing with it!"
    )
    time.sleep(2)
    return name
