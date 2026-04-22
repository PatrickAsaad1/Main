# games/rock_paper_scissors.py
from Utils.Logger import setup_logging
import time
import random
from Utils.Helpers import returnx
from Utils.Screen import clear

logging = setup_logging()


def run(name=None):
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
        print("First to 3 points wins. Type 'Return' to return to main menu\n")

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
