# 6. Bounded Mathematical Search

Mesopotamian scribes solved problems through systematic iterative searches over finite domains rather than unconstrained while-loops.

---

## Domain Repetition (`consider`)

Use `consider ... from ... through ...:` to iterate through a bounded mathematical range:

<!-- test-id: learn-search-scholar -->
```dubsar
problem
    total : 0
    consider n from 1 through 10:
        total : total + n
result
    total
```

Output:
```text
55
```

This calculates the 10th triangular number:

$$\sum_{n=1}^{10} n = \frac{10 \times 11}{2} = 55$$

In authentic cuneiform Tablet Mode:

<!-- test-id: learn-search-cuneiform -->
```dubsar
𒂊𒁹
    𒊕 : 0
    𒄀 𒁄 𒋫 1 𒂗 10:
        𒊕 : 𒊕 + 𒁄
𒅗𒁹
    𒊕
```

Output:
```text
55
```

In Tablet Mode:
- `𒄀` (*gi*): Begins the bounded iteration block (`consider`).
- `𒁄` (*bal*): The loop variable (cycle / turn).
- `𒋫` (*ta*): Specifies the lower bound ("from").
- `𒂗` (*en*): Specifies the upper bound ("through").

Loops in DUB.SAR are always statically bounded over finite integer ranges. This design guarantees algorithmic termination and mathematical determinism, preventing non-terminating loops.

---

## Further Reading & Reference

- **[Language Guide: Domains & Selection](../guide/domains-and-selection.md)**: Detailed semantics of bounded iteration and candidate selection.
- **[Language Reference: Core Vocabulary](../reference/language.md)**: Grammar for `consider`, `from`, `through`, and domain iteration.
- **[Language Reference: Cuneiform Signs](../reference/cuneiform.md)**: Signs `𒄀` (*gi*), `𒁄` (*bal*), `𒋫` (*ta*), and `𒂗` (*en*).
