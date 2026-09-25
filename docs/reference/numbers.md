# Numeric Notation Reference

DUB.SAR parses and prints numbers in multiple exact formats.

---

## Formats

1. **Decimal Integers**: Standard digits (`0`, `42`, `1000`).
2. **Rational Fractions**: Exact integer ratios (`3/4`, `355/113`).
3. **Sexagesimal Fractions**: Semicolon-delimited base-60 places (`0;30`, `1;24,51,10`).
4. **Mixed Sexagesimal Integers**: Comma-delimited powers of 60 (`1,30` = 90).

---

## Precision Guarantee

Calculations are evaluated using arbitrary-precision rational arithmetic. Numbers are never cast to floating-point representation during evaluation, eliminating IEEE-754 precision loss.
