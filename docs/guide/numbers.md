# Numbers & Sexagesimal Notation

DUB.SAR accurately represents base-60 sexagesimal notation and supports exact arbitrary-precision calculations.

---

## Sexagesimal Digit Notation

Digits within a sexagesimal place range from 0 to 59:

- Comma `,` separates places of the same power of 60.
- Semicolon `;` separates the integer part from fractional places ($60^{-1}, 60^{-2}, \dots$).

Example:

$$1,24;51,10 = 1 \cdot 60^1 + 24 \cdot 60^0 + 51 \cdot 60^{-1} + 10 \cdot 60^{-2} = 84 + \frac{51}{60} + \frac{10}{3600}$$

---

## Regular Numbers

A number $n$ is regular in base 60 if its prime factorization is of the form $2^a 3^b 5^c$. Only regular numbers possess terminating reciprocal expansions in base 60.

DUB.SAR tests for regularity and uses exact rational reduction to ensure that arithmetic over regular numbers never introduces recurring approximations.
