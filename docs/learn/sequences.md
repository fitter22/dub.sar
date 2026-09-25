# 8. Sequences & Structured Data

Scribes maintained lists and inventory tablets. DUB.SAR supports mutable working sequences and tables.

---

## Working Sequences

Create a temporary working sequence with `working name of length 0`:

```dubsar
problem:
    working measurements of length 0
    append 12 to measurements
    append 18 to measurements
    append 25 to measurements

    total_count : length of measurements
    first_val : first from measurements
    last_val : last from measurements
result:
    total_count
    first_val
    last_val
```

---

## Indexing and Slicing

Entries in sequences are indexed starting from 0:

```dubsar
problem:
    working sig of length 0
    append 10 to sig
    append 20 to sig
    item := sig 1 take
result:
    item
```
