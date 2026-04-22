# games/guessing_game.py
from Utils.Logger import setup_logging
import time
import random
from Utils.Helpers import returnx

logging = setup_logging()


def run(name=None):
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

    print(f"\nTry to reach 3 points to win! (type 'Return' to return to main menu)")

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
