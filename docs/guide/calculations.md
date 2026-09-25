# Calculations & Postfix Pipelines

In addition to traditional algebraic expressions, DUB.SAR supports authentic Mesopotamian postfix calculation pipelines.

---

## Postfix Pipeline Mechanics

In a postfix pipeline, values are pushed onto a temporary evaluation stack and verbs operate on the topmost items:

```dubsar
problem
    result_val := 15 4 multiply 10 add 2 divide
result
    result_val
```

Evaluation steps:
1. Push `15`.
2. Push `4`.
3. `multiply` pops 4 and 15, pushing 60.
4. Push `10`.
5. `add` pops 10 and 60, pushing 70.
6. Push `2`.
7. `divide` pops 2 and 70, pushing 35.

---

## Built-in Mathematical Procedures

- `abs(x)`: Absolute value.
- `floor(x)`: Greatest integer less than or equal to $x$.
- `ceil(x)`: Smallest integer greater than or equal to $x$.
- `nearest(x)`: Rounds half-way cases away from zero.
- `gcd(a, b)`: Greatest common divisor.
- `lcm(a, b)`: Least common multiple.
- `min(a, b)`, `max(a, b)`: Minimum and maximum of two values.
