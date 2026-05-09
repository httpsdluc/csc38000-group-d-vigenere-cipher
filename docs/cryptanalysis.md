# Cryptanalysis of the Vigenère Cipher

Owner: Role 4.

This document supports the project presentation. It covers the cipher's history, why it was once considered unbreakable, and how it can be broken in practice.

## 1. History


Vigenère did not actually invent the Vigenère cipher. It was originally created by Giovan Battista Bellaso in 1553. Vigenère's actual contribution was a stronger autokey cipher. 
Vigenère cipher was also known as "the indecipherable cipher" which came from the fact that it defeated all known frequency analysis of the time. Essentially the cipher resisted attempts to break in for three centuries. 
It was eventually broken by Charles Babbage around 1854 (unpublished) and independently by Friedrich Kasiski in 1863, who published the method. It was broken by exploiting the weakness of a repeating keyword, which allowed analysts to determine the key length and reduce it to simple Caesar ciphers.

## 2. How the Cipher Works


The Vigenère cipher is built around a 26×26 grid of letters called the **Vigenère tableau**.
Each row is a Caesar-shifted alphabet: row A starts at A, row B starts at B, and so on.
To encrypt, you pick the row named by your key letter and the column named by your plaintext
letter — the cell at their intersection is the ciphertext letter.

A **monoalphabetic** cipher like Caesar maps every letter to exactly one other letter using a single fixed shift. If you shift by 3, then every 'A' becomes 'D', every 'E' becomes 'H', and so on throughout the entire message. This makes it trivially vulnerable to frequency analysis:
'E' is the most common letter in English, so whatever letter appears most often in the ciphertext is almost certainly 'E', and the shift falls out immediately.

The Vigenère cipher is **polyalphabetic** — it uses a different shift for each position in the message, determined by the keyword. The same plaintext letter maps to a different ciphertext
letter depending on where it falls relative to the key. The word "AT" appearing twice in a message will encrypt to two completely different pairs of letters if the key is at a different
phase each time. This breaks the one-to-one relationship that frequency analysis depends on.

- Walk through the canonical example: encrypting `ATTACKATDAWN` with key `LEMON`.

The key `LEMON` is repeated cyclically to match the length of the plaintext:

Plaintext:  A  T  T  A  C  K  A  T  D  A  W  N
Key:        L  E  M  O  N  L  E  M  O  N  L  E

Each key letter determines a row in the tableau, and each plaintext letter determines a column. The shift for each position is simply the alphabetic index of the key letter (A=0, B=1, …, Z=25). 
The final ciphertext is `LXFOPVEFRNHR`


## 3. Strengths

The cipher's primary strength is its resistance to frequency analysis. Because the key cycles through multiple shifts so a common letter like 'E' can encrypt to a different letter at every
occurrence — an attacker counting letter frequencies in the ciphertext sees a flattened, near-uniform distribution rather than the peaked curve of normal English.

This is a direct consequence of polyalphabetic substitution: the same plaintext letter maps to a different ciphertext letter depending on its position relative to the key. In the worked
example above, 'A' appears four times in `ATTACKATDAWN` and encrypts to four different letters — L, O, E, and N — making it invisible to simple pattern matching.

Finally, the cipher requires no special tools. Given the tableau and a key, anyone can encrypt or decrypt a message by hand with pencil and paper, which made it practical for military and
diplomatic use long before computers existed.

## 4. Known Attacks

### 4.1 Kasiski Examination (Friedrich Kasiski, 1863)

Repeated sequences in the plaintext encrypted under the same key phase produce identical sequences in the ciphertext. By finding these repeated sequences and measuring the distances between them, an attacker can determine the key length — it is likely a factor of those distances. For example, if "VTK" appears at positions 10 and 40, the distance is 30, suggesting a key length of 2, 3, 5, 6, 10, or 15. Taking the GCD across multiple such pairs narrows it
down quickly.
Once the key length is known, split the ciphertext into that many columns and run frequency analysis on each column independently — each column is a Caesar cipher.

### 4.2 Friedman Test / Index of Coincidence (William Friedman, 1920s)

The index of coincidence (IC) measures how unevenly letter frequencies are distributed in a text. English plaintext has IC ≈ 0.067; purely random text has IC ≈ 0.038. Vigenère ciphertext
falls somewhere in between — the longer the key, the closer the IC drops toward random. By computing the IC of the ciphertext, an attacker gets a statistical estimate of the key length without needing any repeated sequences.

### 4.3 Frequency Analysis on Each Caesar Column

Once the key length *k* is known, the ciphertext can be split into *k* columns, where every character in a column was shifted by the same key letter. Each column is therefore a simple Caesar cipher and can be broken independently by matching its letter frequencies against the known English distribution. The most frequent letter in each column is most likely an encryption of 'E'. Recovering one shift per column yields the full key.

## 5. Modern Relevance

The Vigenère cipher is cryptographically broken and has no place in modern security. The attacks in Section 4 can recover the key from a few hundred characters of ciphertext in minutes.

Its historical significance, however, is real. The idea of cycling through multiple substitution alphabets directly influenced the design of rotor machines like the Enigma, which
automated the same principle mechanically — and whose breaking by Turing and the team at Bletchley Park relied on evolved versions of the same statistical techniques.

At the other extreme, pushing the Vigenère cipher to its logical limit produces something unbreakable: if the key is truly random, never reused, and exactly as long as the message, it
becomes a one-time pad — which Claude Shannon proved in 1949 offers perfect secrecy. The Vigenère cipher sits at the conceptual midpoint between the Caesar cipher and the OTP, making
it a useful lens for understanding both the history and the theory of cryptography.

## 6. References

- Stallings, W., & Brown, L. _Computer Security: Principles and Practice_, 2nd ed. (course textbook).
- Singh, S. _The Code Book_. (popular but accurate history.)
- Kasiski, F. W. _Die Geheimschriften und die Dechiffrir-Kunst_ (1863).
