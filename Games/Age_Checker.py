# games/age_checker.py
from Utils.Logger import setup_logging
from datetime import datetime
from Utils.Helpers import return_to_menu, returnx

logging = setup_logging()


def run(name=None):
    """Calculate user's age from their birth year."""
    logging.info("User selected age checker")
    while True:
        birth = (
            input("What is your birth year? (type 'Return' to return to main menu) ")
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
