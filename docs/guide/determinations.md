# Determinations

A **Determination** is a structured record that groups related mathematical properties and intermediate candidate values into a single entity.

---

## Declaring Determinations

```dubsar
problem
    width : 30 meter
    height : 12 meter
    area := width * height
    lot : width, height, area
result
    lot.area
```

Field values can be accessed using dot notation (`lot.area`, `lot.width`) or using English prepositional phrases (`area of lot`).

---

## Historical Context

In Sumerian cuneiform lexicography, determinatives (semantic classifiers) placed before or after a word indicated its conceptual category (e.g., wooden objects `GIŠ`, stone objects `NA4`, towns `URU`). DUB.SAR adopts this concept to give structured mathematical objects explicit geometric and conceptual typing.
