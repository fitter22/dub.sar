# 5. Postfix Calculation Pipelines

Authentic Mesopotamian calculation descriptions often proceed procedurally: *“take the width, multiply by itself, take the length, multiply by itself, accumulate, take the square root.”*

DUB.SAR captures this calculation style through postfix operation pipelines.

---

## Postfix Syntax

Expressions can be written using postfix pipelines:

<!-- test-id: learn-pipelines-scholar -->
```dubsar
problem
    hyp : 3 meter 3 meter multiply 4 meter 4 meter multiply add square-root
result
    hyp
```

Using cuneiform verbs:

<!-- test-id: learn-pipelines-cuneiform -->
```dubsar
𒂊𒁹
    𒁇 : 3 meter 3 meter 𒊭 4 meter 4 meter 𒊭 𒍣 𒁀𒋛
𒅗𒁹
    𒁇
```

Both produce the exact dimensional output:

```text
5 length
```

---

## Common Postfix Verbs

| Verb (Scholar) | Cuneiform Sign | Pronunciation | Semantics |
| :--- | :--- | :--- | :--- |
| `add` | `𒍣` | *zi* | Pops two values and pushes their sum |
| `subtract` | `𒋫` | *ta* | Pops two values and pushes their difference |
| `multiply` | `𒊭` | *ša* | Pops two values and pushes their product |
| `divide` | `𒉌` | *ni* | Pops two values and pushes their quotient |
| `square` | `𒅁` | *íb* | Squares the top value in place |
| `square-root` | `𒁀𒋛` | *ba-si* | Computes the square root |
| `floor` | `𒄥` | *gur* | Rounds down to the nearest integer |
| `ceil` | `𒉏` | *nim* | Rounds up to the nearest integer |
| `nearest` | `𒊑` | *ri* | Rounds to the nearest integer |

---

## Further Reading & Reference

- **[Language Guide: Calculations & Prescriptions](../guide/calculations.md)**: Detailed postfix rules, multi-line blocks, and stack dynamics.
- **[Language Reference: Core Vocabulary](../reference/language.md)**: Normative list of mathematical verbs and keywords.
- **[Language Reference: Cuneiform Signs](../reference/cuneiform.md)**: Authentic cuneiform glyphs for mathematical operators.
