# 6. Bounded Mathematical Search

Mesopotamian scribes solved problems through systematic iterative searches over finite domains rather than unconstrained while-loops.

---

## Domain Repetition (`consider`)

Use `consider ... from ... through ...:` to iterate through a bounded mathematical range:

```dubsar
problem
    total : 0
    consider n from 1 through 10:
        total := total + n
result
    total
```

In cuneiform script:

```dubsar
𒂊𒁹
    𒊕 : 0
    𒄀 𒁄 𒋫 1 𒂗 10:
        𒊕 := 𒊕 + 𒁄
𒅗𒁹
    𒊕
```

Loops in DUB.SAR are always statically bounded, guaranteeing termination and algorithmic determinism.
