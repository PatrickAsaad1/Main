# utils/screen.py
import os


def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")
