# games/text_search.py
from Utils.Logger import setup_logging
import time
from Utils.Helpers import return_to_menu, returnx
from Utils.Screen import clear

logging = setup_logging()


def run(name=None):
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

        if len(fat_text_input) > 50000:
            print(
                "⚠️ Warning: Very large text detected. This might slow down the search."
            )
            confirm = input("Continue anyway? (y/n): ").strip().lower()
            if confirm != "y":
                return_to_menu()
                return

        if returnx(search_word):
            return
        elif fat_text_input == "":
            print("You didn't enter any text! Returning to main menu...")
            logging.warning("User entered empty text for search")
            time.sleep(2)
            return

        search_word = (
            input(
                "What word do you want to search for? (type 'Return' to return to main menu) "
            )
            .strip()
            .lower()
        )

        if search_word == "return":
            return_to_menu()
            return
        elif search_word == "":
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
                input("\nDo you wanna see a secret word reverser? (y/n): ")
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
