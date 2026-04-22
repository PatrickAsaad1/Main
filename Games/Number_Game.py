# games/number_game.py
from Utils.Logger import setup_logging
import time
import random
from Utils.Helpers import returnx

logging = setup_logging()


def run(name=None):
    """Number guessing game - guess a number between 1-20 with 5 attempts."""
    logging.info("User selected number game")
    number = random.randint(1, 20)
    print("I will think of a number from 1 - 20 and you try to guess it")
    time.sleep(1)
    print("Type 'Return' to return to main menu | Note: You have only 5 attempts")
    print()
    time.sleep(0.5)

    attempts = 0
    while attempts < 5:
        print(f"Attempt {attempts+1}/5")
        uguess = input("What is the num im guessing? ").strip().lower()

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
