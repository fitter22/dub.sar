# Quantities & Expressions

Expressions in DUB.SAR can be written in either standard infix algebraic notation or postfix stack notation.

---

## Identifiers and Bindings

Identifiers may contain letters, digits, underscores, and hyphens (e.g., `solar-year`, `hyp_sq`, `total_1`).

Two assignment operators are supported:
- `:` **Establishment**: Declares or establishes a known binding.
- `:=` **Prescription Assignment**: Calculates an expression and assigns it to a variable.

```dubsar
problem:
    limit : 100
    counter := limit + 1
```

---

## Binary Operators

| Operator | Meaning | Precedence |
| :--- | :--- | :--- |
| `**` | Power (exponent must be integer) | 4 |
| `*`, `/`, `%` | Multiplication, Division, Modulo | 3 |
| `+`, `-` | Addition, Subtraction | 2 |
| `==`, `!=`, `<`, `<=`, `>`, `>=` | Comparison | 1 |
