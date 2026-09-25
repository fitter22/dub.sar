# 6. Bounded Mathematical Search

Mesopotamian scribes solved problems through systematic iterative searches over finite domains rather than unconstrained while-loops.

---

## Domain Repetition (`consider`)

Use `consider ... from ... through ...:` to iterate through a bounded mathematical range:

```dubsar
problem:
    total : 0
    consider n from 1 through 10:
        total := total + n
result:
    total
```

In cuneiform script:

```dubsar
𒂊𒁹
    total : 0
    𒄀 n 𒋫 1 𒌗 10:
        total := total + n
𒅗𒁹
    total
```

Loops in DUB.SAR are always statically bounded, guaranteeing termination and algorithmic determinism.
