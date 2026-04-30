# Cryptanalysis of the Vigenère Cipher

Owner: Role 4.

This document supports the project presentation. It covers the cipher's history, why it was once considered unbreakable, and how it can be broken in practice. Fill in each section with your own writing — the headings and prompts below are scaffolding.

## 1. History

- Who is Vigenère, and what was actually his contribution versus what is misattributed?
- The cipher was called _le chiffre indéchiffrable_ ("the indecipherable cipher") for ~300 years. Why?
- When and how was it eventually broken?

## 2. How the Cipher Works

- The Vigenère tableau (26×26 grid).
- Polyalphabetic substitution vs. monoalphabetic substitution (Caesar).
- Walk through the canonical example: encrypting `ATTACKATDAWN` with key `LEMON`.

## 3. Strengths

- Resists simple frequency analysis when the key is unknown.
- Same plaintext letter maps to different ciphertext letters depending on key position.
- Easy to compute by hand using the tableau.

## 4. Known Attacks

### 4.1 Kasiski Examination (Friedrich Kasiski, 1863)

- Find repeated sequences of characters in the ciphertext.
- Measure the distances between repetitions.
- The greatest common divisor (GCD) of those distances is likely the key length.
- Once the key length is known, split the ciphertext into that many columns and run frequency analysis on each column independently — each column is a Caesar cipher.

### 4.2 Friedman Test / Index of Coincidence (William Friedman, 1920s)

- Compute the index of coincidence (IC) of the ciphertext.
- English plaintext has IC ≈ 0.0667; uniformly random text has IC ≈ 0.0385.
- The IC of Vigenère ciphertext drops as key length grows; this gives a statistical estimate of key length.

### 4.3 Frequency Analysis on Each Caesar Column

- Once the key length is known, each column corresponds to one Caesar shift.
- Match each column's letter-frequency distribution against the known English frequency distribution to recover the shift.
- Concatenating the recovered shifts gives the key.

## 5. Modern Relevance

- Vigenère by itself is broken and is not used to protect anything sensitive today.
- However, the _idea_ of polyalphabetic substitution influenced the design of more sophisticated ciphers, including rotor machines like the Enigma.
- One-time pads (which are unbreakable) can be viewed as a Vigenère cipher with a truly random, never-repeated key as long as the message.

## 6. References

- Stallings, W., & Brown, L. _Computer Security: Principles and Practice_, 2nd ed. (course textbook).
- Singh, S. _The Code Book_. (popular but accurate history.)
- Kasiski, F. W. _Die Geheimschriften und die Dechiffrir-Kunst_ (1863).
