# 2. Quantities & Expressions

DUB.SAR treats values as either dimensionless exact rationals or dimensioned quantities.

---

## Numbers and Literals

Numbers can be specified in standard decimal notation or sexagesimal base-60 notation:

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

All calculations preserve exact fractions without floating-point truncation.

---

## Metrological Quantities

Attach physical units directly to numeric values:

```dubsar
problem
    distance : 15 meter
    speed : 3 meter / second
    travel_time := distance / speed
result
    travel_time
```

The runtime verifies unit compatibility automatically. Adding incompatible units (such as meters and days) raises a compile-time diagnostic.
