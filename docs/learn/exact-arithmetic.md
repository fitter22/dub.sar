# 3. Exact Sexagesimal Arithmetic

Mesopotamian mathematics relied on base-60 place-value notation. DUB.SAR implements an exact rational arithmetic model to mirror authentic scribal calculations without floating-point drift.

---

## The Sexagesimal Semicolon

Sexagesimal notation uses semicolons (`;`) to separate the integer portion from fractional sexagesimal places, with commas (`,`) separating successive sexagesimal places:

- `1;30` denotes $1 + \frac{30}{60} = 1.5$.
- `0;20` denotes $\frac{20}{60} = \frac{1}{3}$.
- `0;15` denotes $\frac{15}{60} = \frac{1}{4}$.
- `1;24,51,10` denotes the famous Babylonian approximation of $\sqrt{2}$ from tablet YBC 7289:

    $$1 + \frac{24}{60} + \frac{51}{3600} + \frac{10}{216000} \approx 1.41421296\dots$$

---

## Exact Rational Model vs. Backend Limits

At the language level, DUB.SAR models all numbers as exact rationals ($p/q$) with automatic Euclidean GCD reduction, completely avoiding IEEE floating-point approximation errors.

However, the execution targets have different representation characteristics:

- **Reference Interpreter & Stack VM**: Implemented in Python with arbitrary-precision integers, supporting unbounded numerator and denominator expansion.
- **Native AOT Compiler (C99) & WebAssembly**: High-performance compiled targets store exact rationals in fixed-width signed 64-bit integer pairs (`int64_t num, den` / `i64`) using 128-bit intermediate arithmetic (`__int128_t`). While mathematically exact, calculations on these targets are bounded by 64-bit integer limits.

---

## Runnable Sexagesimal Arithmetic

Here is a runnable tablet demonstrating sexagesimal fraction addition and exact division via reciprocal multiplication:

<!-- test-id: learn-exact-arithmetic-runnable -->
```dubsar
problem
    # 1. Sexagesimal fractions
    half : 0;30        # 30/60 = 1/2
    third : 0;20       # 20/60 = 1/3

    # 2. Exact sum of fractions: 1/2 + 1/3 = 5/6 = 50/60
    sum : half + third

    # 3. Exact division by 4 via reciprocal multiplication (0;15)
    dividend : 100
    recip_four : 0;15
    quarter : dividend * recip_four
result
    sum
    quarter
```

Output:
```text
0;50
25
```

---

## Regular Numbers & Reciprocals

In Mesopotamian mathematics, numbers whose prime factors are limited to 2, 3, and 5 are known as **regular numbers** (*igi-bi*). Regular numbers have finite sexagesimal reciprocal expansions without repeating fractions:

- $2 \to 0;30$
- $3 \to 0;20$
- $4 \to 0;15$
- $5 \to 0;12$
- $6 \to 0;10$
- $8 \to 0;07,30$
- $9 \to 0;06,40$
- $10 \to 0;06$

Because Mesopotamian mathematics lacked floating-point division, scribes performed division by multiplying by the pre-computed exact reciprocal from archival tables.

---

## Further Reading & Reference

- **[Language Reference: Numbers & Sexagesimal Notation](../reference/numbers.md)**: Full syntax for positional sexagesimal representation.
- **[Core Concepts: Exact Arithmetic](../concepts/exact-arithmetic.md)**: Mathematical theory of base-60 sexagesimal fractions and regular numbers.
- **[Examples: Babylonian Square Root of 2](../examples/index.md#historical-mesopotamian-archaeology)**: Runnable calculation of $\sqrt{2}$ from tablet YBC 7289.
