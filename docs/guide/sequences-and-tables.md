# Sequences & Tables

Tablets frequently contain tabular accounts, lists of measurements, and coefficient sequences.

---

## Working Sequences

Create a mutable working sequence with `working name of length 0`:

```dubsar
problem
    working sig of length 0
    append 10 to sig
    append 20 to sig
    append 30 to sig
    append 40 to sig
```

---

## Operations on Sequences

- `length of seq`: Returns the integer count of elements.
- `first from seq`: Extracts the initial element at index 0.
- `last from seq`: Extracts the final element at index $N-1$.
- `take entry i from seq`: Fetches the element at 0-based index `i` (or postfix `i seq take` / `i seq 𒋗`).
