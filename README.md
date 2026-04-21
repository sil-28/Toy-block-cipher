# Toy Block Cipher — SPN Implementation in Magma

A from-scratch implementation of a **Substitution-Permutation Network (SPN)** toy block cipher, written in [Magma](http://magma.maths.usyd.edu.au/magma/). This project was developed as part of a cryptography course in the MSc Mathematics program and demonstrates the core building blocks of modern symmetric ciphers like AES.

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
    └── toyblock.m      # Full implementation in Magma
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

Open Magma and load the file:

```magma
load "magma/toyblock.m";

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

The file includes a `test()` procedure that verifies both encryption and decryption against known-good outputs:

| Key | Plaintext | Expected Ciphertext |
|-----|-----------|-------------------|
| `0000000000000000` | `0000000000000000` | `0011001000011011` |
| `0000000000000000` | `1111111111111111` | `0010001010111101` |
| `1111111111111111` | `0000000000000000` | `0110110111100101` |
| `1111111111111111` | `1111111111111111` | `0000110001110101` |

The procedure also verifies that decryption correctly inverts encryption for all four cases. Run it with:

```magma
load "magma/toyblock.m";
load "magma/test.m";
test();
// Expected output:
// Correct!
// Correct!
```

---

## Requirements

- [Magma Computational Algebra System](http://magma.maths.usyd.edu.au/magma/) (v2.20 or later recommended)
- Alternatively, a free online Magma calculator is available at [magma.maths.usyd.edu.au/calc](http://magma.maths.usyd.edu.au/calc/)
