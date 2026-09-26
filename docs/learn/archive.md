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

<!-- test-id: learn-archive-reciprocals-scholar -->
```dubsar
problem
    consult tablet "reciprocals"

    reciprocal-of-four :
        4
        take entry from reciprocals
result
    reciprocal-of-four
```

### Mixed Mode (Cuneiform Keywords with Archive Identifier)

In Mixed Mode, scribes can mount persistent reference tablets using cuneiform operators (`𒅆 𒁾`) while retaining the named table identifier (`reciprocals`):

<!-- test-id: learn-archive-reciprocals-mixed -->
```dubsar
𒂊𒁹
    𒅆 𒁾 "reciprocals"

    𒁇 :
        4
        𒉻 𒋫 reciprocals
𒅗𒁹
    𒁇
```

Both Scholar and Mixed modes produce the exact sexagesimal reciprocal of 4 ($1/4 = 15/60$):

```text
0;15
```

In the pipeline above:
1. `consult tablet "reciprocals"` (`𒅆 𒁾 "reciprocals"`) mounts the embedded reference table from the archive.
2. The key `4` is pushed onto the evaluation stack.
3. `take entry from reciprocals` (`𒉻 𒋫 reciprocals`) pops key `4`, looks up its entry in the archive, and pushes the stored reciprocal value (`0;15`).

---

## Working Tablets and Archival Inscription

Computational workflows often use temporary scratchpads before committing records permanently to clay. In DUB.SAR, scratchpads are declared as **working tablets**:

<!-- test-id: learn-archive-working-scholar -->
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

In authentic cuneiform Tablet Mode (using cuneiform working tablet `𒅎` and identifier `𒁇`):

<!-- test-id: learn-archive-working-cuneiform -->
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

Both produce the inscribed value:

```text
42
```

### Inscription Semantics and Immutability

Once inscribed with `inscribe ... as tablet ...` (or `𒁹𒀀 ... 𒁶 𒁾 ...`), the working tablet is baked permanently into the backing SQLite database (`.tablets.db`):

- **Immutability**: Persistent tablets cannot be mutated in place. Once inscribed, the clay dries and the records are permanent.
- **Cryptographic Provenance**: Every inscribed tablet version receives a deterministic SHA-256 hash computed across its schema and rows, ensuring cryptographic integrity.
- **Version Lineage**: Further modifications derive a new version or child tablet with parent tracking, preserving an unbroken audit trail of calculations.

---

## Further Reading & Reference

- **[Language Guide: Tablet Archive](../guide/archive.md)**: Querying, inscribing, and managing tablets.
- **[Core Concepts: Archive & Provenance](../concepts/archive-and-provenance.md)**: Content addressing, version lineage, and cryptographic immutability.
- **[CLI Reference: Dubsar CLI](../reference/cli.md)**: Command-line inspection and archival management tools.

