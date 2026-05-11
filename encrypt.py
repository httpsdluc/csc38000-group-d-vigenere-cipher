"""
encrypt.py — Vigenère cipher encryption.

Owner: Role 1.

Responsibilities:
- Implement encrypt(plaintext, key) so that:
    encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
- Preserve the case of the original plaintext (uppercase stays uppercase,
  lowercase stays lowercase).
- Pass non-alphabetic characters through unchanged (spaces, punctuation,
  digits should appear in the ciphertext exactly as in the plaintext).
- The key only advances on alphabetic characters — spaces in the
  plaintext should NOT consume a position in the key.
"""

from tableau import char_to_index, index_to_char, normalize_key


def encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt `plaintext` using the Vigenère cipher with `key`.

    Args:
        plaintext: The message to encrypt. May contain any characters.
        key: The keyword. Non-alphabetic characters in the key are ignored.

    Returns:
        The ciphertext, with case and non-alphabetic characters preserved.

    Example:
        >>> encrypt("Attack at dawn!", "LEMON")
        'Lxfopv ef rnhr!'
    """
    # TODO (Role 1): implement encryption.
    #
    # Suggested approach:
    #   1. Call normalize_key(key) to get a clean uppercase key.
    #   2. Walk through plaintext one character at a time.
    #   3. Track a separate `key_index` that only advances when the current
    #      plaintext character is a letter.
    #   4. For each letter:
    #        shift = char_to_index(normalized_key[key_index % len(key)])
    #        new_index = (char_to_index(letter) + shift) % 26
    #        ciphertext_letter = index_to_char(new_index)
    #      then restore the original case.
    #   5. For non-letters, append the character unchanged.
    # raise NotImplementedError("encrypt() needs to be implemented by Role 1.")

    normalized_key = normalize_key(key)
    result_chars = []
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            key_letter = normalized_key[key_index % len(normalized_key)]
            shift = char_to_index(key_letter)
            cipher_index = (char_to_index(char) + shift) % 26
            cipher_letter = index_to_char(cipher_index)
            if char.islower():
                cipher_letter = cipher_letter.lower()
            result_chars.append(cipher_letter)
            key_index += 1
        else:
            result_chars.append(char)

    return "".join(result_chars)


if __name__ == "__main__":
    # Quick smoke test — replace once implementation is done.
    sample_plain = "Attack at dawn!"
    sample_key = "LEMON"
    print(f"Plaintext : {sample_plain}")
    print(f"Key       : {sample_key}")
    print(f"Ciphertext: {encrypt(sample_plain, sample_key)}")