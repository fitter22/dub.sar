# 9. Tablet Archive

Tablets in Mesopotamian administration were stored in formal archives and consulted across generations. DUB.SAR provides a persistent, immutable tablet archive backed by SQLite.

---

## Standard Reference Tablets

DUB.SAR embeds standard mathematical reference tablets, including:

- `reciprocals`: Standard sexagesimal reciprocal table.
- `right-triangles`: Pythagorean triplets such as 3-4-5 and 5-12-13.
- `inclinations`: Historical ramp inclinations and feeds.
- `turn-divisions`: Sexagesimal subdivisions of full rotations.

```dubsar
problem:
    tri : take "3-4-5" from "right-triangles"
    diag : tri.diagonal
result:
    diag
```

---

## Inscribing Persistent Tablets

Working tablets can be permanently inscribed into an archive:

```dubsar
problem:
    working report of length 0
    append 100 to report
    inscribe report as "annual-tribute"
result:
    "inscribed"
```

Once inscribed, persistent tablets are immutable and content-hashed with SHA-256 for provenance tracking.
