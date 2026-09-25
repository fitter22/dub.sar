# 9. Tablet Archive

Tablets in Mesopotamian administration were stored in formal archives and consulted across generations. DUB.SAR provides a persistent, immutable tablet archive backed by SQLite (`.tablets.db`).

---

## Consulting Reference Tablets

DUB.SAR embeds standard mathematical reference tablets, including:

- `reciprocals`: Standard sexagesimal reciprocal table ($1/2 = 0;30$, $1/4 = 0;15$, etc.).
- `right-triangles`: Pythagorean triplets such as 3-4-5 and 5-12-13.
- `inclinations`: Historical ramp inclinations and feeds.
- `turn-divisions`: Sexagesimal subdivisions of full rotations.

To consult a persistent tablet and retrieve records:

```dubsar
problem
    consult tablet "reciprocals"

    reciprocal-of-four :
        4
        take entry from reciprocals
result
    reciprocal-of-four
```

In authentic cuneiform Tablet Mode:

```dubsar
𒂊𒁹
    𒅆 𒁾 "reciprocals"

    𒁇 :
        4
        𒉻 𒋫 reciprocals
𒅗𒁹
    𒁇
```

---

## Working Tablets and Archival Inscription

Computational workflows often use temporary scratchpads before committing records permanently to clay. In DUB.SAR, scratchpads are declared as **working tablets**:

```dubsar
problem
    working observations

    put 42 into observations at 10

    inscribe observations as tablet "observations"

    recorded-entry :
        10
        take entry from observations
result
    recorded-entry
```

In cuneiform Tablet Mode:

```dubsar
𒂊𒁹
    𒆥 𒅎

    𒃻 42 𒀀 𒅎 𒀀 10

    𒁹𒀀 𒅎 𒁶 𒁾 "observations"

    𒁇 :
        10
        𒉻 𒋫 𒅎
𒅗𒁹
    𒁇
```

### Inscription Semantics and Immutability

Once inscribed with `inscribe ... as tablet ...` (or `𒁹𒀀 ... 𒁶 𒁾 ...`), the target tablet is permanently written to the backing SQLite database:
- **Immutability**: Persistent tablets cannot be mutated in place.
- **Provenance & Lineage**: Every tablet version receives a cryptographic SHA-256 hash verifying its contents and schema.
- **Revisions**: Further modifications derive a new version or child tablet with parent tracking.
