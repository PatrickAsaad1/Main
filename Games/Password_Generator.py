# games/password_generator.py
from Utils.Logger import setup_logging
import random
from Utils.Helpers import return_to_menu, returnx

logging = setup_logging()


def run(name=None):
    """Generate random passwords."""
    logging.info("User selected password generator")

    manypass = input("How many passwords you wanna generate? ")
    while True:
        if returnx(manypass):
            return
        if not manypass.isdigit():
            print("Please enter a number!")
            manypass = input("How many passwords? ")
            continue
        manypass = int(manypass)
        break
    logging.info(f"User wants to generate {manypass} passwords")

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
    logging.info(f"User wants each password to be {manychar} characters long")
    characters = (
        "!@#$%&*_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    )

    for i in range(manypass):
        password = ""
        for j in range(manychar):
            password += random.choice(characters)
        print(f"Password {i+1}: {password}")
