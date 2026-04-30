"""
tableau.py — Shared utilities for the Vigenère cipher.

Both encrypt.py and decrypt.py import from this module, so the alphabet
and helper logic stay consistent across the project.

Owner: Role 2 (decryption module owner) maintains this file, since the
shared tableau is most closely tied to the encrypt/decrypt math.
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def char_to_index(letter: str) -> int:
    """
    Return the 0-based position of `letter` in the alphabet.
    'A' -> 0, 'B' -> 1, ..., 'Z' -> 25.
    Assumes the input is a single uppercase letter.
    """
    return ord(letter.upper()) - ord("A")


def index_to_char(index: int) -> str:
    """
    Return the uppercase letter at position `index` in the alphabet.
    Wraps around mod 26 so negative or large indices still return a letter.
    """
    return ALPHABET[index % 26]


def normalize_key(key: str) -> str:
    """
    Strip non-alphabetic characters from the key and uppercase it.
    Raises ValueError if the resulting key is empty.
    """
    cleaned = "".join(ch for ch in key if ch.isalpha()).upper()
    if not cleaned:
        raise ValueError("Key must contain at least one letter.")
    return cleaned


def repeat_key(key: str, length: int) -> str:
    """
    Repeat `key` cyclically until it is at least `length` characters long,
    then truncate to exactly `length`.

    Example: repeat_key("LEMON", 12) -> "LEMONLEMONLE"
    """
    if length <= 0:
        return ""
    repeats = (length // len(key)) + 1
    return (key * repeats)[:length]