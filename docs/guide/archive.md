# Tablet Archive (é-dub-ba-a)

The DUB.SAR Tablet Archive (`é-dub-ba-a` / *tablet house*) provides persistent, versioned, cryptographic storage for mathematical tablets. DUB.SAR programs execute alongside this local archive, which contains inherited scholarly knowledge, tables of constants, metrological standards, and program-inscribed computational results.

---

## Architecture & Conceptual Paradigm

The Tablet Archive is fundamentally **not** SQL, CRUD, or conventional database programming:

```text
Conventional Programming:              DUB.SAR Architecture:
┌─────────────────────────┐            ┌─────────────────────────┐
│       Source Code       │            │  Mathematical Tablet    │
└────────────┬────────────┘            └────────────┬────────────┘
             │ SQL queries                          │ consult / inscribe
             ▼                                      ▼
┌─────────────────────────┐            ┌─────────────────────────┐
│     Relational DB       │            │   House of Tablets      │
│  (Tables, Rows, CRUD)   │            │ (Immutable Clay Tablets)│
└─────────────────────────┘            └─────────────────────────┘
```

The language exposes **no** tables, rows, `SELECT`, `FROM`, `WHERE`, `INSERT`, `UPDATE`, or `DELETE` statements. Instead, a DUB.SAR scholar works within an authentic tablet room:

- **Storage Engine**: SQLite embedded storage (`.tablets.db`).
- **Cryptographic Provenance**: Every inscribed tablet computes a canonical SHA-256 hash of its serialized payload and metadata.
- **Consulting Knowledge**: Read-only examination of existing reference tablets.
- **Working Scratchpads**: Temporary in-memory tablets for rapid computation.
- **Explicit Inscription**: Baking a working tablet into a permanent, immutable clay record.
- **Lineage and Provenance**: Tracking which earlier tablets were consulted, copied, or derived.

---

## 1. Consulting Scholarly Knowledge

To retrieve a value from a persistent tablet in the archive, consult the tablet and take the entry:

### Scholar Mode
```dubsar
problem
    consult tablet "reciprocals"

    reciprocal-of-four :
        4
        take entry from reciprocals
result
    reciprocal-of-four
```

### Canonical Cuneiform Mode
```dubsar
𒂊𒁹
    𒅆 𒁾 "reciprocals" 𒁶 𒅎

    𒈦 :
        𒅎 4 𒋗
𒅗𒁹
    𒈦
```

---

## 2. Working Tablets & Inscription

Computational scratchpads are declared as working tablets (`kin` / `𒆥`). They are fast, mutable in-memory key-value mappings that disappear upon program termination unless explicitly inscribed:

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

Inscription is strictly atomic: the new tablet version is either committed to the archive in its entirety with a cryptographic SHA-256 checksum, or the transaction fails leaving existing records completely intact.

---

## 3. Immutability, Monotonic Versioning & Lineage

Persistent tablets are strictly **immutable**. Once inscribed, a version cannot be overwritten or altered in place:

- **Derivation & Copying**: Creating a revision is performed via `copy tablet "T" as working W` or `derive tablet "T" as working W`.
- **Monotonic Versioning**: Re-inscribing creates version $N+1$ (`v1` -> `v2` -> `v3`), retaining complete historical lineage.
- **Version Pinning**: Programs can pin an exact historical version (`consult tablet "reciprocals" version 1`) to guarantee mathematical reproducibility across decades.

---

## 4. Standard Scholarly Archive ("Scribal Archive 1")

Every new DUB.SAR archive automatically initializes with 13 standard scholarly reference tablets:

- `reciprocals`: Authentic Old Babylonian reciprocal pairs ($2 \to 0;30$, $3 \to 0;20$, $4 \to 0;15$, $5 \to 0;12$, $6 \to 0;10$, $8 \to 0;07,30$, etc.).
- `common-fractions`: Exact sexagesimal representations of fundamental fractions ($1/2, 1/3, 2/3, 1/4, 3/4, 1/5, 5/6$).
- `squares`: Exact integer squares for numbers $1$ through $60$.
- `cubes`: Exact integer cubes for numbers $1$ through $30$.
- `square-roots`: Verified rational approximations and exact integer roots.
- `powers`: Powers of fundamental bases ($2$ and $60$).
- `basic-metrology`: Attested conversion factors for length, area, and capacity.
- `basic-geometry`: Attested geometric coefficients.
- `ea-nasir-shipment`: Structured shipment record of copper ingots from Dilmun inspired by tablet UET V 72, recording promised/delivered weights, quality standards, and transaction metadata.
- `right-triangles`: Verified integer right triangles (Pythagorean triples) such as $(3, 4, 5)$, $(5, 12, 13)$, $(8, 15, 17)$, $(7, 24, 25)$, $(20, 21, 29)$, $(12, 35, 37)$, $(9, 40, 41)$, $(28, 45, 53)$, $(11, 60, 61)$, $(16, 63, 65)$, $(33, 56, 65)$, $(48, 55, 73)$, $(13, 84, 85)$, $(36, 77, 85)$, $(39, 80, 89)$, and $(65, 72, 97)$, connecting directly to Plimpton 322 scribal traditions.
- `inclinations`: Standard scribal slopes, ratios, inclinations (rise/run), and feeds (run/rise) for embankments, ramps, and canal construction.
- `powers-of-two`: Exact integer powers $2^0$ through $2^{12}$ alongside exact reciprocal fractions, validating sequence lengths for Radix-2 FFT algorithms.
- `turn-divisions`: Sexagesimal subdivisions of a full cycle ($1/1, 1/2, 1/3, 1/4, 1/5, 1/6, 1/8, 1/10, 1/12, 1/60, 1/360$), bridging historical Babylonian circular divisions (post-450 BCE zodiac) and modern harmonic analysis.

Every scholarly entry retains exact rational representations—no IEEE floating-point approximation or decimal truncation occurs.

---

## 5. Archive CLI Tooling

Manage and inspect the local archive using dedicated CLI subcommands:

```bash
# List all tablets in the archive
dubsar archive list

# Display tablet contents and metadata
dubsar archive show "reciprocals"

# Trace version history and provenance
dubsar archive history "reciprocals"

# Export the archive to canonical JSON
dubsar archive export -o archive.json

# Import tablets from canonical JSON
dubsar archive import archive.json

# Render a tablet in ASCII/Unicode clay-style grid or vector SVG
dubsar archive render "reciprocals"
dubsar archive render "reciprocals" --style svg -o reciprocals.svg
```

---

## 6. End-to-End Archive Workflow: The Ea-nāṣir Copper Dispute

To demonstrate the full lifecycle of persistent archive consultation, exact rational calculation, mathematical determination, working tablet inscription, and monotonic revision with provenance tracking, DUB.SAR provides an end-to-end accounting workflow inspired by the world's oldest preserved customer complaint tablet (**UET V 72 / British Museum BM 131236**, c. 1750 BCE from Ur).

### Historical Context vs. Computational Model

> **Historical Disclaimer**:
> This example is an illustrative computational demonstration of ancient administrative dispute settlement adapted to the DUB.SAR Tablet Archive.
>
> Historically, tablet UET V 72 records Nanni's passionate personal complaint to the merchant Ea-nāṣir concerning subpar copper ingots delivered after arduous transit through hostile territory ("What do you take me for, that you treat somebody like me with such contempt?"). The original clay tablet does not preserve modern tabular balance sheets or structured numerical matrices.
>
> In DUB.SAR, this historical dispute is formalized as an executable scribal audit workflow: structured delivery records are consulted from the persistent archive, quality deficiency is calculated using exact sexagesimal arithmetic, and an audit assessment tablet is inscribed into the archive with complete version lineage.

### Conceptual Workflow

```text
┌─────────────────────────┐
│   ea-nasir-shipment     │ (Persistent archival record: 10 talent promised/delivered, quality 0;45)
└────────────┬────────────┘
             │ consult tablet & take entries
             ▼
┌─────────────────────────┐
│   ea-nasir.dub          │ (Calculates exact deficiency: 1 - 0;45 = 0;15; builds assessment)
└────────────┬────────────┘
             │ inscribe working complaint-assessment
             ▼
┌─────────────────────────┐
│  ea-nasir-assessment v1 │ (Immutable assessment tablet committed to archive)
└────────────┬────────────┘
             │ derive tablet as working revised-assessment
             ▼
┌─────────────────────────┐
│  ea-nasir_revision.dub  │ (Appends verdict: "rejected"; updates archive)
└────────────┬────────────┘
             │ inscribe revised-assessment
             ▼
┌─────────────────────────┐
│  ea-nasir-assessment v2 │ (Version 2 with complete provenance: derived from v1)
└─────────────────────────┘
```

### Step 1: Inscribing the Assessment Tablet (v1)

The audit program consults `ea-nasir-shipment`, extracts the promised and delivered quantities (each 10 talent), retrieves the required quality (`1`) and delivered ingot quality (`0;45`, or $3/4$), computes the exact quality deficiency ($1 - 0;45 = 0;15$), forms a mathematical determination, transfers it into a working tablet, and inscribes `ea-nasir-assessment` into the persistent archive.

#### Scholar Mode (`examples/ea_nasir_scholar.dub`)
```text
problem
    consult tablet "ea-nasir-shipment"

    merchant :
        "merchant"
        take entry from ea-nasir-shipment

    promised :
        "promised-quantity"
        take entry from ea-nasir-shipment

    delivered :
        "delivered-quantity"
        take entry from ea-nasir-shipment

    required-quality :
        "required-quality"
        take entry from ea-nasir-shipment

    actual-quality :
        "actual-quality"
        take entry from ea-nasir-shipment

    deficiency :
        required-quality
        actual-quality
        subtract

    assessment :
        merchant
        promised
        delivered
        required-quality
        actual-quality
        deficiency

    working complaint-assessment

    put assessment into complaint-assessment

    inscribe complaint-assessment as tablet "ea-nasir-assessment"
result
    assessment
```

#### Canonical Cuneiform Mode (`examples/ea_nasir.dub`)
```text
𒂊𒁹
    𒅆 𒁾 "ea-nasir-shipment"

    merchant :
        "merchant"
        pad 𒋫 ea-nasir-shipment

    promised :
        "promised-quantity"
        pad 𒋫 ea-nasir-shipment

    delivered :
        "delivered-quantity"
        pad 𒋫 ea-nasir-shipment

    required-quality :
        "required-quality"
        pad 𒋫 ea-nasir-shipment

    actual-quality :
        "actual-quality"
        pad 𒋫 ea-nasir-shipment

    deficiency :
        required-quality
        actual-quality
        𒋫

    assessment :
        merchant
        promised
        delivered
        required-quality
        actual-quality
        deficiency

    𒆥 complaint-assessment

    𒃻 assessment 𒀀 complaint-assessment

    𒁹𒀀 complaint-assessment 𒁶 𒁾 "ea-nasir-assessment"
𒅗𒁹
    assessment
```

### Step 2: Monotonic Derivation & Verdict (v2)

When an official ruling is pronounced on the dispute, a subsequent program derives a working scratchpad directly from version 1 of `ea-nasir-assessment`, sets a `verdict` entry ("rejected"), and inscribes the revised tablet back to `ea-nasir-assessment`.

Because DUB.SAR tablets are strictly immutable:
- `ea-nasir-assessment` version 1 remains unaltered in the archive for historical auditability.
- `ea-nasir-assessment` version 2 is created with cryptographic checksum and provenance metadata: `derived_from: ea-nasir-assessment:v1`.

#### Scholar Mode (`examples/ea_nasir_revision_scholar.dub`)
```text
problem
    consult tablet "ea-nasir-assessment"

    derive from "ea-nasir-assessment" as working revised-assessment

    put "rejected" into revised-assessment at "verdict"

    inscribe revised-assessment as tablet "ea-nasir-assessment"
result
    "ea-nasir-assessment"
```

#### Canonical Cuneiform Mode (`examples/ea_nasir_revision.dub`)
```text
𒂊𒁹
    𒅆 𒁾 "ea-nasir-assessment"

    𒁴 𒋫 "ea-nasir-assessment" 𒁶 𒆥 revised-assessment

    𒃻 "rejected" 𒀀 revised-assessment 𒀀 "verdict"

    𒁹𒀀 revised-assessment 𒁶 𒁾 "ea-nasir-assessment"
𒅗𒁹
    "ea-nasir-assessment"
```

### Persistent Tablet Entries and Metadata

| Tablet | Version | Key | Value | Metadata / Notes |
| :--- | :--- | :--- | :--- | :--- |
| `ea-nasir-shipment` | `1` | `merchant` | `"Ea-nāṣir"` | `origin`: `"Dilmun"`, `destination`: `"Ur"` |
| | | `promised-quantity` | `10 talent` | Metrological standard: 1 talent = 60 mina = 3600 shekels |
| | | `delivered-quantity` | `10 talent` | Full weight delivered |
| | | `required-quality` | `1` | Grade 1 (pure standard copper) |
| | | `actual-quality` | `0;45` | Grade 3/4 (substandard ingots) |
| `ea-nasir-assessment` | `1` | `deficiency` | `0;15` | Exact rational: $1 - 0;45 = 0;15$ ($1/4$ deficit) |
| `ea-nasir-assessment` | `2` | `verdict` | `"rejected"` | `derived_from`: `"ea-nasir-assessment:v1"` |

### Inspecting and Rendering via CLI

Manage and inspect the audit workflow directly from the terminal:

```bash
# 1. View the original shipment record in the persistent archive
dubsar archive show "ea-nasir-shipment"

# 2. Execute the assessment program (inscribes ea-nasir-assessment v1)
dubsar run examples/ea_nasir_scholar.dub

# 3. View the newly inscribed assessment tablet
dubsar archive show "ea-nasir-assessment"

# 4. Execute the revision program (derives and inscribes ea-nasir-assessment v2)
dubsar run examples/ea_nasir_revision_scholar.dub

# 5. Trace the complete immutable version lineage and parent links
dubsar archive history "ea-nasir-assessment"

# 6. Render the assessment tablet to terminal clay grid or vector SVG artwork
dubsar archive render "ea-nasir-assessment"
dubsar archive render "ea-nasir-assessment" --style svg -o examples/ea_nasir_assessment.svg
```
