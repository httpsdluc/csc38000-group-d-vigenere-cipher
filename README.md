# csc38000-group-d-vigenere-cipher

CSC 38000 Group D Project

# Vigenère Cipher

An encryption and decryption algorithm based on the Vigenère polyalphabetic cipher, implemented in Python.

**Course:** CSC 38000 — Computer Security (City College of New York)
**Instructor:** Dr. Oluwaseyi Ajayi
**Group:** D
**Members:** Khan Abdur (Group Leader), Cai Rong Li, Diana Lucero, Md Mamum

## About the Cipher

The Vigenère cipher is a polyalphabetic substitution cipher invented in the 16th century. Unlike the Caesar cipher, which shifts every letter by the same amount, the Vigenère cipher uses a keyword to determine a different shift for each position in the message. Each letter of the keyword corresponds to a row of the Vigenère tableau (a 26×26 grid of shifted alphabets), and the keyword is repeated cyclically to match the length of the plaintext.

For example, encrypting `ATTACKATDAWN` with the key `LEMON`:

```
Plaintext:  A T T A C K A T D A W N
Key:        L E M O N L E M O N L E
Ciphertext: L X F O P V E F R N H R
```

For each letter, you find the row in the Vigenère tableau corresponding to the key letter and the column corresponding to the plaintext letter — the intersection is the ciphertext letter. Decryption reverses the process.

## Project Structure

```
vigenere-cipher/
├── .gitignore
├── README.md
├── main.py              # CLI entry point — Role 3
├── encrypt.py           # Encryption module — Role 1
├── decrypt.py           # Decryption module — Role 2
├── tableau.py           # Shared Vigenère tableau utility
├── tests.py             # Test cases and verification — Role 3
└── docs/
    └── cryptanalysis.md # Writeup on attacks against the cipher — Role 4
```

## Roles

| Role | Owner | Responsibility                                                                                                                                                                        |
| ---- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | _TBD_ | Build `encrypt(plaintext, key)` in `encrypt.py`. Handle key cycling, case preservation, and non-alphabetic characters.                                                                |
| 2    | _TBD_ | Build `decrypt(ciphertext, key)` in `decrypt.py`. Maintain the shared `tableau.py` utility used by both modules.                                                                      |
| 3    | _TBD_ | Build `main.py` (the user-facing CLI) and write test cases in `tests.py`. Owns the README updates as the project evolves.                                                             |
| 4    | _TBD_ | Build the presentation slides and write `docs/cryptanalysis.md` covering the cipher's history, strengths, and known attacks (Kasiski examination, Friedman test, frequency analysis). |

Fill in the names once the group decides who takes which role.

## Setup

This project uses only the Python standard library — no installation needed beyond Python 3.8 or newer.

```bash
git clone https://github.com/<your-username>/vigenere-cipher.git
cd vigenere-cipher
python3 main.py
```

## Usage

Once `main.py` is implemented, the CLI will let you choose between encrypt and decrypt, then prompt for a message and a key:

```
$ python3 main.py
Vigenère Cipher
1) Encrypt
2) Decrypt
> 1
Message: ATTACK AT DAWN
Key: LEMON
Ciphertext: LXFOPV EF RNHR
```

## Running Tests

```bash
python3 tests.py
```

Tests use the classic `ATTACKATDAWN` / `LEMON` / `LXFOPVEFRNHR` vector and a few additional cases.

## Workflow

1. Each owner works on a feature branch named after their module (e.g. `feature/encrypt`).
2. Open a pull request to `main` when your piece is ready.
3. At least one other group member should review and approve before merging.
4. Keep `main` in a working, runnable state at all times.

## License

This project is for academic use as part of CSC 38000 at CCNY.
