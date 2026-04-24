# Toy Block Cipher — SPN Implementation in Magma & Pyhton

A from-scratch implementation of a **Substitution-Permutation Network (SPN)** toy block cipher, written in both [Magma](http://magma.maths.usyd.edu.au/magma/) and **Python**. This project was developed as part of a cryptography course in the MSc Mathematics program and demonstrates the core building blocks of modern symmetric ciphers like AES.

---

## Overview

A Substitution-Permutation Network is a series of mathematical operations used in modern block ciphers. This implementation operates on **16-bit blocks** with a **16-bit key** and runs for **4 rounds**, combining:

- **Substitution** — non-linear confusion via an S-box over GF(2)⁴
- **Permutation** — linear diffusion of bits across the block
- **Key mixing** — XOR with round keys derived from a key schedule

The structure mirrors the design principles behind AES, making this a useful pedagogical tool for understanding how real-world ciphers work.

---

## Structure

```
toy-block-cipher/
├── README.md
└── magma/
│   ├── ToyBlockCipher.mag      # Full implementation in Magma
│   └── test.txt                # Magma test suite
└── python/
    ├── ToyBlockCipher.py       # Full implementation in Python
    └── test.py                 # Python test suite
```

---

## Components

### S-box (`Substitution`)

Takes a 4-bit input vector over GF(2)⁴ and maps it to a 4-bit output via a fixed lookup table. Provides **confusion** — making the relationship between key and ciphertext as complex as possible.

The cipher also includes `InverseSubstitution` for decryption, which applies the inverse S-box mapping.

### Permutation (`Permutation`)

Operates on 16-bit blocks. Rearranges bits according to a fixed permutation table, spreading the influence of each input bit across the block. Provides **diffusion** — ensuring that a change in one bit of the plaintext affects many bits of the ciphertext.

```
Bit positions (1-indexed):
1  → 1    2  → 5    3  → 9    4  → 13
5  → 2    6  → 6    7  → 10   8  → 14
9  → 3    10 → 7    11 → 11   12 → 15
13 → 4    14 → 8    15 → 12   16 → 16
```

The permutation is its own inverse, so `InversePermutation` simply calls `Permutation`.

### Key Schedule (`KSchedule`)

Derives 5 round keys from the original 16-bit key using two permutations `s1` and `s2` defined on GF(2)⁴. Returns a sequence `Ks` of 5 subkeys, each of length 16 bits.

### Encryption (`ToyBlock`)

Runs 4 rounds of the SPN:

1. XOR with round key
2. Apply S-box to each 4-bit nibble
3. Apply permutation (skipped in the last round)

Final step: XOR with the last round key.

### Decryption (`ToyBlockDecipher`)

Inverts the encryption process using inverse S-box and the same permutation (which is its own inverse), applying round keys in reverse order.

---

## Usage

### Magma

Open Magma and load the file:

```magma
load "magma/ToyBlockCipher.mag";

// Define a 16-bit key and plaintext as sequences over GF(2)
K := [0,0,0,0, 1,1,1,1, 0,0,0,0, 1,1,1,1];
M := [1,0,1,0, 0,1,0,1, 1,1,0,0, 0,0,1,1];

// Encrypt
C := ToyBlock(K, M);
print C;

// Decrypt
M2 := ToyBlockDecipher(K, C);
print M2;

// Verify correctness
print M eq M2;  // should print: true
```

### Python

No external dependencies required — uses only the Python standard library. Key and plaintext are passed as plain **16-bit integers**.

```python
import ToyBlockCipher as TBC

K = 0x0F0F   # 16-bit key
M = 0xA5C3   # 16-bit plaintext

# Encrypt
C = TBC.ToyBlock(K, M)
print(hex(C))

# Decrypt
M2 = TBC.ToyBlockDecipher(K, C)
print(hex(M2))

# Verify correctness
print(M == M2)  # should print: True
```

---

## Mathematical Background

This cipher is built on the theory of **finite fields**, specifically the field GF(2) (integers modulo 2). Key concepts used:

- **GF(2)⁴** — the 4-dimensional vector space over GF(2), used to represent 4-bit words
- **XOR as addition** — addition in GF(2) corresponds to bitwise XOR
- **S-box as a bijection** — the substitution function is a permutation of GF(2)⁴, ensuring invertibility
- **Key schedule via symmetric group** — round key derivation uses permutations `s1`, `s2` acting on GF(2)⁴ as elements of the symmetric group S₁₆

This algebraic structure is the same theoretical foundation underlying **AES**, which operates over GF(2⁸).

---

## Why This Matters

Understanding toy ciphers like this one is the first step toward analyzing and breaking real ciphers. The SPN structure introduced here is directly relevant to:

- **Differential cryptanalysis** — studying how differences in plaintext propagate through rounds
- **Linear cryptanalysis** — finding linear approximations of the S-box
- **AES internals** — AES is a more sophisticated SPN over a larger field

---

## Test Vectors

Both implementations are verified against the same known-good outputs (values in decimal for python, in binary for magma):

| Key | Plaintext | Expected Ciphertext |
| --- | --- | --- |
| `0` | `0` | `12827` |
| `0` | `65535` | `8893` |
| `65535` | `0` | `28133` |
| `65535` | `65535` | `3189` |

Each test also verifies that decryption correctly inverts encryption.

**Magma:**
```magma
load "magma/ToyBlockCipher.mag";
load "magma/test.txt";
test();
// Expected output:
// Correct!
// Correct!
```

**Python:**
```bash
python python/test.py
# Expected output:
# Correct!
# Correct!
```

---

## Requirements

### Magma
- [Magma Computational Algebra System](http://magma.maths.usyd.edu.au/magma/) (v2.20 or later recommended)
- Alternatively, a free online Magma calculator is available at [magma.maths.usyd.edu.au/calc](http://magma.maths.usyd.edu.au/calc/)

### Python
* Python 3.7 or later
* No external libraries required
