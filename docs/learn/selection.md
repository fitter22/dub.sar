# 7. Determinations & Selection

Approximation and search algorithms generate multiple candidate evaluations. DUB.SAR provides structured determination records and the `retain` statement to select optimal candidates.

---

## Determination Records

A determination packages named variables into a coherent compound mathematical record:

<!-- test-id: learn-selection-records -->
```dubsar
problem
    width : 3 meter
    height : 4 meter
    area : width * height
    sample : width, height, area
result
    sample.area
```

Output:
```text
12 length^2
```

Fields within a determination can be accessed using dot notation (`sample.area`) or postfix English phrasing (`area of sample`).

---

## The `retain` Statement

Within search loops, `retain candidate when ...` maintains the optimal candidate across iterations according to an explicit condition:

<!-- test-id: learn-selection-retain -->
```dubsar
problem
    best : empty
    consider i from 1 through 5:
        c : i * i
        retain c when c is greater than best
result
    best
```

Output:
```text
25
```

### Sentinel Semantics (`empty` / `nu` / `𒉡`)

- When `best` is initialized to `empty` (`𒉡`), the first candidate produced in the loop is retained unconditionally.
- On subsequent iterations, `retain` evaluates the `when` condition. Only if the candidate improves upon the current `best` is the state atomically updated.
- If no candidate ever satisfies the condition, `best` remains `empty`.

---

## Further Reading & Reference

- **[Language Guide: Determinations](../guide/determinations.md)**: Formal syntax for determination records and field access.
- **[Language Guide: Domains & Selection](../guide/domains-and-selection.md)**: Selection conditions, ordering, and sentinels.
- **[Language Reference: Core Vocabulary](../reference/language.md)**: Keywords `retain`, `when`, `empty`, `is greater than`, `is lesser than`.
