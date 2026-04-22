import logging
import os


def setup_logging():
    """Setup logging configuration."""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(script_dir, "data", "game.log")

    # Create data folder if it doesn't exist
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_path)],
    )
    return logging.getLogger()


# Create a default logger instance
logger = logging.getLogger(__name__)
