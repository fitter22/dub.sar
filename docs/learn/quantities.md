# 2. Quantities & Expressions

DUB.SAR treats values as either dimensionless exact rationals or dimensioned quantities.

---

## Numbers and Literals

Numbers can be specified in standard decimal notation, rational fractions, or sexagesimal base-60 notation:

```dubsar
problem
    a : 12
    b : 3/4
    c : 1;30           # 1 + 30/60 = 1.5
    d : 0;20           # 20/60 = 1/3
result
    a
    b
    c
    d
```

Output:
```text
12
0;45
1;30
0;20
```

Notice that rational `3/4` is automatically presented in canonical sexagesimal notation as `0;45` ($45/60$). All calculations preserve exact arbitrary-precision rationals without floating-point truncation or drift.

---

## Metrological Quantities

Attach physical units directly to numeric values to form dimensioned physical quantities:

```dubsar
problem
    distance : 15 meter
    speed : 3 meter / second
    travel_time : distance / speed
result
    travel_time
```

Output:
```text
5 time
```

When dividing distance by speed, the length units cancel ($15\text{ m} / (3\text{ m/s}) = 5\text{ s}$), yielding an exact time quantity.

In authentic cuneiform Tablet Mode:

```dubsar
𒂊𒁹
    dist : 15 meter
    vel : 3 meter / second
    𒌓 : dist / vel
𒅗𒁹
    𒌓
```

Output:
```text
5 time
```

The runtime enforces dimensional compatibility statically. Incompatible operations (such as attempting `10 meter + 2 day`) are rejected at compile time before execution.

---

## Further Reading & Reference

- **[Language Guide: Quantities & Expressions](../guide/quantities-and-expressions.md)**: Formal syntax for quantities and mathematical expressions.
- **[Language Reference: Numbers & Sexagesimal Notation](../reference/numbers.md)**: Number parsing, regular numbers, and base-60 place value.
- **[Language Reference: Units of Measurement](../reference/units.md)**: Supported length, mass, area, capacity, and time units.
- **[Core Concepts: Dimensional Mathematics](../concepts/dimensional-mathematics.md)**: Compile-time dimensional analysis and metrological safety.
