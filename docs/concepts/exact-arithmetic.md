# Exact Arithmetic in DUB.SAR

Modern computer architectures rely on binary floating-point numbers (IEEE 754), which inevitably introduce roundoff errors ($0.1 + 0.2 \ne 0.3$).

---

## Rational Precision

DUB.SAR treats all numbers as exact rational values:
$$r = \frac{p}{q}, \quad p, q \in \mathbb{Z}, \quad q > 0$$

All arithmetic operations compute exact sums, differences, products, and quotients:

$$\frac{p_1}{q_1} + \frac{p_2}{q_2} = \frac{p_1 q_2 + p_2 q_1}{q_1 q_2}$$

GCD reduction is performed automatically, maintaining canonical reduced forms across both Python and native compiled C99 runtimes.
