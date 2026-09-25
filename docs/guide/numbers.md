# Numbers & Sexagesimal Notation

DUB.SAR accurately represents base-60 sexagesimal notation and supports exact rational calculations.

---

## Sexagesimal Digit Notation

In historical Mesopotamian mathematics and standard modern Assyriological convention (Neugebauer-Sachs convention):

- **Semicolon `;` Separates Whole Numbers and Fractions**: A semicolon marks the boundary between the integer places ($60^0$) and the sexagesimal fractional places ($60^{-1}, 60^{-2}, \dots$).
  - `1;30` represents $1 + \frac{30}{60} = 1.5 = \frac{3}{2}$.
  - `0;20` represents $0 + \frac{20}{60} = \frac{1}{3}$.
  - `0;15` represents $0 + \frac{15}{60} = \frac{1}{4}$.
  - `1;24,51,10` represents the YBC 7289 approximation of $\sqrt{2}$:
    $$1 + \frac{24}{60} + \frac{51}{3600} + \frac{10}{216000} = \frac{30547}{21600} \approx 1.41421296$$
- **Comma `,` Separates Successive Fractional Places**:
  - Following a semicolon separator, commas delimit successive negative powers of 60 ($60^{-1}, 60^{-2}, \dots$): `0;7,30` represents $\frac{7}{60} + \frac{30}{3600} = \frac{1}{8}$.
  - Whole numbers are expressed using standard decimal notation (`90`) or cuneiform numerals (`𒐏𒈫` = 42, `𒌍` = 30).

---

## Regular Numbers

A number $n$ is regular in base 60 if its prime factorization contains only 2, 3, and 5 ($n = 2^a 3^b 5^c$). Regular numbers possess terminating reciprocal expansions in base 60.

DUB.SAR tests for regularity and uses exact rational reduction to ensure that arithmetic over regular numbers never introduces recurring approximations.

---

## Computational Precision Model

DUB.SAR avoids binary floating-point drift (IEEE-754) by evaluating all numeric operations over exact rational values ($p/q$ where $p, q \in \mathbb{Z}, q > 0$):

- **Python Reference Interpreter & Bytecode VM**: Evaluates numbers with arbitrary-precision integers, supporting unbounded numerator and denominator growth without overflow.
- **Native C99 / AOT Runtime**: Stores exact rational numbers in 64-bit signed integer pairs (`int64_t num, den`), computing cross-multiplication, additions, and subtractions using 128-bit intermediate arithmetic (`__int128_t`) with automated Euclidean GCD reduction after each operation.
