"""
tests.py — Test cases for the Vigenère cipher.

Owner: Role 3.

Run with:  python3 tests.py

Each test prints PASS or FAIL. The runner exits with a non-zero status
if any test fails, which makes it easy to wire into a GitHub Action later.
"""

import sys

from encrypt import encrypt
from decrypt import decrypt


# (description, function-to-test, args, expected_output)
TEST_CASES = [
    # ---------- Core correctness ----------

    # Classic textbook example.
    ("encrypt: ATTACKATDAWN / LEMON",
     encrypt, ("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR"),
    ("decrypt: LXFOPVEFRNHR / LEMON",
     decrypt, ("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN"),

    # Case preservation.
    ("encrypt: mixed case",
     encrypt, ("Attack at dawn", "LEMON"), "Lxfopv ef rnhr"),
    ("decrypt: mixed case",
     decrypt, ("Lxfopv ef rnhr", "LEMON"), "Attack at dawn"),

    # Non-alphabetic passthrough — punctuation and spaces.
    ("encrypt: punctuation passes through",
     encrypt, ("HELLO, WORLD!", "KEY"), "RIJVS, UYVJN!"),
    ("decrypt: punctuation passes through",
     decrypt, ("RIJVS, UYVJN!", "KEY"), "HELLO, WORLD!"),

    # ---------- Edge cases ----------

    # Empty input — encrypting nothing should produce nothing.
    ("encrypt: empty plaintext",
     encrypt, ("", "KEY"), ""),
    ("decrypt: empty ciphertext",
     decrypt, ("", "KEY"), ""),

    # Single character — A shifted by B should land on B.
    ("encrypt: single letter (A + B = B)",
     encrypt, ("A", "B"), "B"),
    ("decrypt: single letter (B - B = A)",
     decrypt, ("B", "B"), "A"),

    # Key longer than plaintext — only first len(plaintext) letters of key are used.
    # H(7) + L(11) = 18 -> S.  I(8) + O(14) = 22 -> W.
    ("encrypt: key longer than plaintext",
     encrypt, ("HI", "LONGKEY"), "SW"),

    # Plaintext with no letters — should pass through completely unchanged.
    ("encrypt: no letters in plaintext",
     encrypt, ("12345 !@#", "KEY"), "12345 !@#"),

    # ---------- Key normalization ----------

    # Lowercase key should produce the same result as uppercase key.
    ("encrypt: lowercase key equals uppercase key",
     lambda msg, k: encrypt(msg, k) == encrypt(msg, k.upper()),
     ("HELLO", "key"), True),

    # Non-letter characters in the key should be ignored ("K-E-Y" == "KEY").
    ("encrypt: dashes in key are ignored",
     lambda msg, k: encrypt(msg, k) == encrypt(msg, "KEY"),
     ("HELLO", "K-E-Y"), True),

    # ---------- Key cycling ----------

    # With key "AB", shifts cycle 0,1,0,1 — so "AAAA" -> "ABAB".
    ("encrypt: short key cycles across longer plaintext",
     encrypt, ("AAAA", "AB"), "ABAB"),

    # ---------- Round trips ----------

    # Round trip on a longer message.
    ("round trip: long message",
     lambda msg, k: decrypt(encrypt(msg, k), k),
     ("The quick brown fox jumps over the lazy dog.", "SECURITY"),
     "The quick brown fox jumps over the lazy dog."),

    # Round trip on a message that mixes letters, digits, and punctuation.
    ("round trip: mixed alphanumeric and punctuation",
     lambda msg, k: decrypt(encrypt(msg, k), k),
     ("Pass: 1234! It's working.", "PYTHON"),
     "Pass: 1234! It's working."),
]


def run_tests() -> int:
    passed = 0
    failed = 0
    for description, fn, args, expected in TEST_CASES:
        try:
            actual = fn(*args)
            if actual == expected:
                print(f"PASS  {description}")
                passed += 1
            else:
                print(f"FAIL  {description}")
                print(f"      expected: {expected!r}")
                print(f"      got:      {actual!r}")
                failed += 1
        except NotImplementedError as e:
            print(f"SKIP  {description}  ({e})")
        except Exception as e:
            print(f"ERROR {description}  ({type(e).__name__}: {e})")
            failed += 1

    print()
    print(f"{passed} passed, {failed} failed, {len(TEST_CASES) - passed - failed} skipped")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())