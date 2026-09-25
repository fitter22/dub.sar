# Numeric Notation Reference

DUB.SAR parses, evaluates, and outputs numbers in multiple exact formats.

---

## Formats

1. **Decimal Integers**: Standard digits (`0`, `42`, `1000`).
2. **Rational Fractions**: Exact integer ratios (`3/4`, `355/113`).
3. **Sexagesimal Fractions**: Semicolon-delimited base-60 places (`0;30` = $1/2$, `0;20` = $1/3$, `1;24,51,10` $\approx \sqrt{2}$).
4. **Positional Sexagesimal Integers**: Comma-delimited powers of 60 (`1,30` = $1 \times 60 + 30 = 90$).
5. **Cuneiform Numerals**: Authentic cuneiform numeric signs (`𒁹` = 1, `𒌋` = 10, `𒐕` = 60).

---

## Computational Precision Model

Calculations are evaluated using exact rational arithmetic ($p/q$), completely eliminating IEEE-754 binary floating-point rounding drift:

- **Reference Interpreter & VM**: Arbitrary-precision exact integer numerators and denominators.
- **Native AOT Compiler (C99 Runtime)**: Exact 64-bit rational storage (`int64_t num, den`) using 128-bit intermediate products (`__int128_t`) with canonical Euclidean GCD normalization.
