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

    reciprocal-of-four :
        4
        pad 𒋫 reciprocals
𒅗𒁹
    reciprocal-of-four
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
    𒆥 observations

    𒃻 42 𒀀 observations 𒀀 10

    𒁹𒀀 observations 𒁶 𒁾 "observations"

    recorded-entry :
        10
        pad 𒋫 observations
𒅗𒁹
    recorded-entry
```

### Inscription Semantics and Immutability

Once inscribed with `inscribe ... as tablet ...` (or `𒁹𒀀 ... 𒁶 𒁾 ...`), the target tablet is permanently written to the backing SQLite database:
- **Immutability**: Persistent tablets cannot be mutated in place.
- **Provenance & Lineage**: Every tablet version receives a cryptographic SHA-256 hash verifying its contents and schema.
- **Revisions**: Further modifications derive a new version or child tablet with parent tracking.
