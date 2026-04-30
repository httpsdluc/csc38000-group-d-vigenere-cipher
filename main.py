"""
main.py — Command-line interface for the Vigenère cipher.

Owner: Role 3.

Responsibilities:
- Provide a simple, friendly CLI that lets the user pick encrypt or decrypt,
  enter a message and a key, and see the result.
- Validate input (non-empty key, valid menu choice) and print clear errors.
- Keep this file thin — all real logic lives in encrypt.py and decrypt.py.
"""

from encrypt import encrypt
from decrypt import decrypt


MENU = """
Vigenère Cipher
---------------
1) Encrypt
2) Decrypt
3) Quit
"""


def prompt_choice() -> str:
    """Ask the user to pick a menu option. Return '1', '2', or '3'."""
    while True:
        choice = input("> ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Please enter 1, 2, or 3.")


def run_encrypt() -> None:
    message = input("Message: ")
    key = input("Key: ").strip()
    if not key:
        print("Error: key cannot be empty.")
        return
    print(f"Ciphertext: {encrypt(message, key)}")


def run_decrypt() -> None:
    message = input("Ciphertext: ")
    key = input("Key: ").strip()
    if not key:
        print("Error: key cannot be empty.")
        return
    print(f"Plaintext: {decrypt(message, key)}")


def main() -> None:
    while True:
        print(MENU)
        choice = prompt_choice()
        if choice == "1":
            run_encrypt()
        elif choice == "2":
            run_decrypt()
        else:
            print("Goodbye.")
            return


if __name__ == "__main__":
    main()