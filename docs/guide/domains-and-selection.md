# Domains & Selection

DUB.SAR provides bounded domain repetition and candidate selection.

---

## Bounded Domains (`consider`)

To iterate over a finite mathematical domain:

```dubsar
problem:
    sum : 0
    consider k from 1 through 100:
        sum := sum + k
result:
    sum
```

Bounds must be non-negative integers or exact expressions evaluating to positive integers. Loop variables are locally scoped to the block.

---

## Atomic Selection (`retain`)

The `retain` statement selects and updates the current optimal candidate:

```dubsar
problem:
    best : empty
    consider x from 1 through 10:
        error := (x * x - 50) absolute
        candidate : x, error
        retain candidate when candidate.error < best.error
result:
    best.x
```

When `best` is `empty`, the candidate is retained automatically on the first iteration.
