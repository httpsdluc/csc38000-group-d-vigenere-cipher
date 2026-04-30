"""
decrypt.py — Vigenère cipher decryption.

Owner: Role 2.

Responsibilities:
- Implement decrypt(ciphertext, key) so that:
    decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"
- Mirror the behavior of encrypt(): preserve case, pass non-alphabetic
  characters through unchanged, and only advance the key on letters.
- Maintain tableau.py (the shared utility module) so both encrypt and
  decrypt agree on the alphabet and key handling.
"""

from tableau import char_to_index, index_to_char, normalize_key


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt `ciphertext` using the Vigenère cipher with `key`.

    Args:
        ciphertext: The encrypted message.
        key: The same keyword used to encrypt.

    Returns:
        The recovered plaintext, with case and non-alphabetic characters preserved.

    Example:
        >>> decrypt("Lxfopv ef rnhr!", "LEMON")
        'Attack at dawn!'
    """
    # TODO (Role 2): implement decryption.
    #
    # Suggested approach:
    #   1. Call normalize_key(key) to get a clean uppercase key.
    #   2. Walk through ciphertext one character at a time.
    #   3. Track a separate `key_index` that only advances when the current
    #      ciphertext character is a letter.
    #   4. For each letter:
    #        shift = char_to_index(normalized_key[key_index % len(key)])
    #        new_index = (char_to_index(letter) - shift) % 26
    #        plaintext_letter = index_to_char(new_index)
    #      then restore the original case.
    #   5. For non-letters, append the character unchanged.
    raise NotImplementedError("decrypt() needs to be implemented by Role 2.")


if __name__ == "__main__":
    # Quick smoke test — replace once implementation is done.
    sample_cipher = "Lxfopv ef rnhr!"
    sample_key = "LEMON"
    print(f"Ciphertext: {sample_cipher}")
    print(f"Key       : {sample_key}")
    print(f"Plaintext : {decrypt(sample_cipher, sample_key)}")