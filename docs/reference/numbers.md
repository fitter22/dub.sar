# Numeric Notation Reference

DUB.SAR parses, evaluates, and outputs numbers in multiple exact formats, rooted in Mesopotamian sexagesimal place-value mathematics and rational arithmetic.

---

## 1. Supported Number Formats

DUB.SAR supports five numerical formats in source code:

| Format | Syntax Example | Mathematical Value | Description |
| :--- | :--- | :--- | :--- |
| **Decimal Integer** | `42`, `1000` | $42$, $1000$ | Standard base-10 digits. |
| **Rational Fraction** | `3/4`, `355/113` | $3/4$, $355/113$ | Exact integer ratio $p/q$. |
| **Sexagesimal Fraction** | `0;30`, `1;24,51,10` | $1/2$, $\approx \sqrt{2}$ | Positional base-60 with semicolon and comma separators. |
| **Regular Sexagesimal Integer** | `1,20`, `2,0` | $80$, $120$ | Multi-place sexagesimal whole numbers ($1 \times 60 + 20 = 80$). |
| **Cuneiform Numerals** | `𒁹`, `𒌋`, `𒐏𒈫` | $1$, $10$, $42$ | Authentic Unicode cuneiform numeral glyphs (values 1–59). |

---

## 2. Positional Sexagesimal System

In Mesopotamian mathematics, numbers are expressed in base 60. DUB.SAR adopts the standard Assyriological transcription convention:

- The **semicolon** (`;`) marks the sexagesimal radix point separating the integer part from the fractional part.
- The **comma** (`,`) separates consecutive base-60 sexagesimal places, each taking a value from 0 to 59.

### Place-Value Weighting

$$
d_k \dots d_1, d_0 ; f_1, f_2, f_3 = \sum_{i=0}^{k} d_i \cdot 60^i + \sum_{j=1}^{3} f_j \cdot 60^{-j}
$$

### Common Sexagesimal Equivalences

| Sexagesimal | Exact Fraction | Decimal Equivalent | Notes |
| :--- | :---: | :---: | :--- |
| `0;30` | $1/2$ | $0.5$ | Half (`maš` / `𒈦`) |
| `0;20` | $1/3$ | $0.333\dots$ | One third |
| `0;15` | $1/4$ | $0.25$ | One quarter |
| `0;12` | $1/5$ | $0.2$ | One fifth |
| `0;10` | $1/6$ | $0.166\dots$ | One sixth |
| `0;7,30` | $1/8$ | $0.125$ | One eighth ($7/60 + 30/3600$) |
| `0;6,40` | $1/9$ | $0.111\dots$ | One ninth ($6/60 + 40/3600$) |
| `0;5` | $1/12$ | $0.0833\dots$ | One twelfth |
| `1;24,51,10` | $\approx \sqrt{2}$ | $1.41421296\dots$ | YBC 7289 diagonal approximation |

---

## 3. Regular vs Irregular Numbers

Mesopotamian reciprocal tables emphasize **regular sexagesimal numbers** (5-smooth / Hamming numbers):

- **Regular Numbers**: Numbers whose only prime factors are $2$, $3$, and $5$ ($2^a \cdot 3^b \cdot 5^c$). Their reciprocals terminate in finite sexagesimal places.
- **Irregular Numbers**: Numbers containing any prime factor $\ge 7$ (such as $7$, $11$, $13$, $17$). Their reciprocals produce non-terminating, repeating sexagesimal sequences. DUB.SAR maintains exact integer ratios $p/q$ for all numbers, ensuring zero loss of precision even for irregular values.

---

## 4. Computational Precision Model

Calculations are evaluated using exact rational arithmetic ($p/q$), completely eliminating IEEE-754 binary floating-point rounding drift:

- **Reference Interpreter & VM**: Arbitrary-precision exact integer numerators and denominators normalized via Euclidean GCD.
- **Native AOT Compiler (C99 Runtime)**: Exact 64-bit rational storage (`int64_t num, den`) using 128-bit intermediate products (`__int128_t`) with canonical Euclidean GCD normalization.
- **Format Modes**: The CLI `--format` option controls output presentation:
    - `canonical` (default): Terminating regular numbers print in sexagesimal notation; integers print in decimal; irregular ratios print as fractions.
    - `sexagesimal`: Enforces sexagesimal formatting across results.
    - `decimal`: Prints exact decimal or fraction representations.

---

## 5. Minimal Example

<!-- test-id: ref-numbers-formats -->
```dubsar
problem
    half : 0;30
    ratio : 3/4
    combined : half + ratio
result
    combined
```

Output:
```text
1;15
```

---

## 6. Related Documentation

- **Tutorial**: [Chapter 3: Exact Sexagesimal Arithmetic](../learn/exact-arithmetic.md)
- **Language Guide**: [Numbers & Sexagesimal](../guide/numbers.md)
- **Language Reference**: [Numeric & Sexagesimal Notation](language.md#12-numeric-sexagesimal-notation)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)
