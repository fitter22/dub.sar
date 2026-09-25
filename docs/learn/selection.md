# 7. Determinations & Selection

Approximation and search algorithms generate multiple candidate evaluations. DUB.SAR provides structured determination records and the `retain` statement to select optimal candidates.

---

## Determination Records

A determination packages named variables into a coherent compound record:

```dubsar
problem:
    width : 3 meter
    length : 4 meter
    area := width * length
    sample : width, length, area
result:
    sample.area
```

---

## The `retain` Statement

Within search loops, `retain candidate when ...` keeps the best candidate according to an explicit condition:

```dubsar
problem:
    best : empty
    consider i from 1 through 5:
        c : i * i
        retain c when c is greater than best
result:
    best
```

If `best` is initially `empty`, the first candidate is retained unconditionally. Subsequent candidates replace `best` only if the condition evaluates to true.
