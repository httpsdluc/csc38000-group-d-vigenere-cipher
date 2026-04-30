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

    # Non-alphabetic passthrough.
    ("encrypt: punctuation passes through",
     encrypt, ("HELLO, WORLD!", "KEY"), "RIJVS, UYVJN!"),
    ("decrypt: punctuation passes through",
     decrypt, ("RIJVS, UYVJN!", "KEY"), "HELLO, WORLD!"),

    # Round trip on a longer message.
    ("round trip: long message",
     lambda msg, k: decrypt(encrypt(msg, k), k),
     ("The quick brown fox jumps over the lazy dog.", "SECURITY"),
     "The quick brown fox jumps over the lazy dog."),
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