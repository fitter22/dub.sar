# 3. Exact Sexagesimal Arithmetic

Mesopotamian mathematics relied on base-60 place-value notation. DUB.SAR implements arbitrary-precision rational arithmetic to mirror authentic scribal calculations.

---

## The Sexagesimal Semicolon

Sexagesimal notation uses semicolons (`;`) to separate the integer portion from fractional sexagesimal places:

- `1;30` denotes $1 + \frac{30}{60} = 1.5$.
- `0;20` denotes $\frac{20}{60} = \frac{1}{3}$.
- `1;24,51,10` denotes the famous Babylonian approximation of $\sqrt{2}$ from tablet YBC 7289:

    $$1 + \frac{24}{60} + \frac{51}{3600} + \frac{10}{216000} \approx 1.41421296\dots$$

---

## Regular Numbers & Reciprocals

In Mesopotamian mathematics, numbers whose prime factors are limited to 2, 3, and 5 have finite sexagesimal reciprocal expansions. DUB.SAR can test whether a rational is regular and compute exact reciprocal values without repeating decimals.
