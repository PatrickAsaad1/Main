# games/encrypt_decrypt.py
from Utils.Logger import setup_logging
import time
import os

# Try to import cryptography
try:
    from cryptography import fernet

    fernet_available = True
except ImportError:
    fernet_available = False
    fernet = None

from Utils.Helpers import return_to_menu

logging = setup_logging()


def run(name=None):
    """Encrypt or decrypt messages using Fernet."""
    logging.info("User selected encrypt/decrypt")

    if not fernet_available:
        print("\nSorry, the encrypt/decrypt feature is not available.")
        print("Please install cryptography: pip install cryptography")
        logging.warning("User attempted to use encrypt/decrypt without cryptography")
        time.sleep(2)
        return

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
                script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                data_dir = os.path.join(script_dir, "data")
                os.makedirs(data_dir, exist_ok=True)
                file_path = os.path.join(data_dir, "encrypted_data.txt")

                file_exists = os.path.exists(file_path)
                with open(file_path, "a", encoding="utf-8") as f:
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

                print(f"\n✅ Saved to: data/encrypted_data.txt")
                logging.info("User saved key and encrypted message to file")
            elif yes_no in ["n", "no"]:
                print(
                    "\n⚠️ Remember, without saving the key and encrypted message, you won't be able to decrypt it later!"
                )
                logging.warning("User chose not to save the key and encrypted message")
        except (IOError, OSError) as e:
            print(f"\n❌ Error saving the key and message: {e}")
            logging.error(f"Error saving the key and message: {e}")

    elif choice == "2":
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
