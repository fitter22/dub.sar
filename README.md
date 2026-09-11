<div align="center">

# 𒁾𒊬 — DUB.SAR 1.0

### The Executable Mesopotamian Mathematical Tablet Language

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Spec: 1.0](https://img.shields.io/badge/Specification-DUB.SAR%201.0-orange.svg)](DUB_SAR_1.0_Language_Specification.md)
[![Tests: 184 Passing](https://img.shields.io/badge/Tests-184%2F184%20Passing-brightgreen.svg)](tests/)
[![Architecture: VM + WASM](https://img.shields.io/badge/Architecture-Interpreter%20%7C%20VM%20%7C%20WASM-purple.svg)](dubsar/)
[![Vibe Coded](https://img.shields.io/badge/Built%20With-100%25%20Vibe%20Coding-ff69b4.svg)](#vibe-coded-to-perfection)

<p align="center">
  <b>What if ancient Babylonian scribes had designed a modern programming language?</b><br>
  DUB.SAR is not a Python dialect in cuneiform costume. It is an executable Mesopotamian mathematical tablet language engineered from first principles — featuring exact arbitrary-precision rational arithmetic, algebraic dimensional unit safety, bounded mathematical search domains, postfix calculation pipelines, atomic selections, a high-level Semantic IR, a stack bytecode virtual machine, and a WebAssembly compiler.
</p>

[Specification](DUB_SAR_1.0_Language_Specification.md) • [Architecture](#compiler--runtime-architecture) • [Quickstart](#quickstart) • [Tablet Archive](#the-tablet-archive) • [Tablet Data Model](#the-tablet-oriented-data-model-sequences-tables-and-structured-records) • [Geometric & Fourier Mathematics](#geometric-mathematics-foundation--coherent-path-to-fourier-mathematics) • [Examples](examples/) • [Clay Tablet Rendering](#clay-tablet-rendering)

---

</div>

## Why DUB.SAR?

Modern programming languages are encumbered with Von Neumann memory mutations, uncontrolled `while` loops, assignment operators (`=`, `:=`), subroutine returns (`def`, `return`), and IEEE 754 binary floating-point roundoff errors.

**DUB.SAR (Sumerian: *dub-sar*, "scribe") reimagines computation as an excavated mathematical clay tablet:**

- **The Tablet Paradigm**: Programs are computational tablets (`IM.GID.DA`) structured in authentic scribal sections: a **Problem Statement** (`𒂊𒁹` / `problem`), reusable **Prescription Recipes** (`𒁾𒊬` / `recipe`), and an **Inscribed Result** (`𒅗𒁹` / `result`).
- **No Imperative Gimmicks**: Say goodbye to `:=`, `=`, `def`, `return`, `for`, `while`, `if`, `else`, and `class`. DUB.SAR expresses computation purely through **Quantity Establishment** (`name : expression`), **Mathematical Determinations** (`candidate : cycle, leaps, error`), **Finite Search Domains** (`consider cycle from 1 through limit:`), and **Atomic Selection** (`retain candidate when error is lesser than best.error`).
- **Exact Sexagesimal Rational Engine**: Every numeric value is an exact arbitrary-precision rational fraction, natively written, computed, and displayed in canonical Mesopotamian sexagesimal notation (`365;14,31,55`). Floating-point inaccuracies simply do not exist.
- **Algebraic Dimensional Safety**: Units are first-class mathematical entities. Quantities multiply and divide algebraically (`2 day * 3 day = 6 day^2`). Incompatible dimensional operations (`1 day + 2 year`) are statically rejected at compile time.
- **Postfix Calculation Pipelines**: Calculations unfold through clear mathematical reductions:
  ```text
  whole-days : solar-year floor
  fraction : solar-year whole-days subtract
  ```
- **Trimodal Source Flexibility**: Write in authentic Unicode cuneiform (**Tablet Mode**), academic Latin transliteration (**Scholar Mode**), or intermix both (**Mixed Mode**). All three representations normalize into an identical abstract syntax tree and Semantic IR.
- **Clay Artwork Generator**: Compile any tablet directly to a vector SVG rendering of an inscribed, case-ruled Mesopotamian clay tablet with bevels, drop shadows, and wedge impressions.

---

## Vibe Coded to Perfection

> **This entire repository was 100% vibe coded.**
>
> From deciphering historical cuneiform numeral tables and designing an exact-rational sexagesimal arithmetic core to implementing an indentation-sensitive Unicode lexer, recursive-descent parser, compile-time unit type checker, high-level mathematical Semantic IR, stack-based bytecode virtual machine, complete WebAssembly backend, and SVG clay tablet renderer — every single line of code, specification, and test suite was built in an uninterrupted flow of specification-driven vibe coding.

---

## Trimodal Source Experience

DUB.SAR provides dual canonical representations of the same mathematical tablet:

### Tablet Mode (Canonical Cuneiform)
```text
𒑰 DUB.SAR 1.0 — Planetary Leap-Year Rule (Tablet Mode)

𒂊𒁹

    solar-year :
        𒀀𒁹 "solar year in days"

    limit :
        1000

    whole-days :
        solar-year
        𒄥

    fraction :
        solar-year
        whole-days
        𒋫

    best :
        𒉡

    𒄀 cycle 𒋫 1 𒂗 limit:

        leaps :
            cycle
            fraction
            𒊭
            𒊑

        candidate-year :
            whole-days
            leaps
            cycle
            𒉌
            𒍣

        error :
            solar-year
            candidate-year
            𒋫
            𒋼

        candidate :
            cycle
            leaps
            error

        𒋼 candidate
            𒂊𒀀 error 𒊭 candidate
            𒈨 𒌉 𒋫 error 𒊭 best

𒅗𒁹

    best
```

### Scholar Mode (Academic Latin Transliteration)
```text
# DUB.SAR 1.0 — Planetary Leap-Year Rule (Scholar Mode)

problem

    solar-year :
        ask "solar year in days"

    limit :
        1000

    whole-days :
        solar-year
        floor

    fraction :
        solar-year
        whole-days
        subtract

    best :
        empty

    consider cycle from 1 through limit:

        leaps :
            cycle
            fraction
            multiply
            nearest

        candidate-year :
            whole-days
            leaps
            cycle
            divide
            add

        error :
            solar-year
            candidate-year
            subtract
            absolute

        candidate :
            cycle
            leaps
            error

        retain candidate
            when error of candidate
            is lesser than error of best

result

    best
```

---

## Quickstart

### Prerequisites
- Python 3.9 or higher (zero external dependencies required for the compiler, VM, and interpreter).

### Installation
Clone the repository:
```bash
git clone https://github.com/fitter22/dub.sar.git
cd dub.sar
chmod +x bin/dubsar
```

### Running Your First Tablet
Execute the Earth-like planetary leap-year calendar solver ($Y = 365.2422$ days):
```bash
bin/dubsar run examples/planetary_leap.dub --input="365.2422"
```

**Output:**
```text
673
163 day
3/3365000 day
```

*DUB.SAR deterministically discovers the optimal 673-year calendar cycle with 163 leap days and an error of just $3/3365000$ days/year (less than one day in a million years), matching independent continued-fraction analysis.*

---

## CLI Toolkit

The `dubsar` command-line tool provides end-to-end capabilities:

```bash
# 1. Execute via Virtual Machine (default) or AST Interpreter
bin/dubsar run examples/planetary_leap.dub --input="365.2422"
bin/dubsar run examples/planetary_leap.dub --backend=ast --input="365.2422"

# 2. Verify syntax and static dimensional safety
bin/dubsar check examples/planetary_leap.dub

# 3. Canonical code formatter (Tablet or Scholar layout)
bin/dubsar format examples/planetary_leap.dub --mode=tablet
bin/dubsar format examples/planetary_leap.dub --mode=scholar

# 4. Disassemble to stack bytecode
bin/dubsar compile examples/planetary_leap.dub --target=bytecode

# 5. Compile to WebAssembly Text (.wat)
bin/dubsar compile examples/planetary_leap.dub --target=wasm -o tablet.wat

# 6. Export AST to JSON
bin/dubsar compile examples/planetary_leap.dub --target=json

# 7. Bidirectional Transliteration
bin/dubsar transliterate examples/planetary_leap.dub
bin/dubsar cuneiform examples/planetary_leap_scholar.dub

# 8. Render Clay Tablet Artwork (SVG or Text Terminal)
bin/dubsar render examples/planetary_leap.dub --style=tablet -o tablet.svg
bin/dubsar render examples/planetary_leap.dub --style=text
bin/dubsar render examples/planetary_leap.dub --style=tablet --strip-comments -o tablet_clean.svg

# 9. Tablet Archive Management (é-dub-ba-a)
bin/dubsar archive list
bin/dubsar archive show "reciprocals"
bin/dubsar archive history "reciprocals"
bin/dubsar archive export -o archive.json
bin/dubsar archive import archive.json
bin/dubsar archive render "reciprocals"
bin/dubsar run examples/tablet_archive.dub --archive=project_archive.db
```

---

## The Tablet Archive (*é-dub-ba-a*)

DUB.SAR programs execute alongside a persistent, local **Tablet Archive** (*é-dub-ba-a*, the Sumerian "house of tablets") containing inherited scholarly knowledge, tables of constants, metrological standards, and program-inscribed computational results.

### Conceptual Paradigm: House of Tablets, Not a Database

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
- **Consulting Knowledge**: Read-only examination of existing reference tablets.
- **Working Scratchpads**: Temporary in-memory tablets for rapid computation.
- **Explicit Inscription**: Baking a working tablet into a permanent, immutable clay record.
- **Lineage and Provenance**: Tracking which earlier tablets were consulted, copied, or derived.

### 1. Consulting Scholarly Knowledge

To retrieve a value from a persistent tablet in the archive, consult the tablet and take the entry:

#### Scholar Mode
```text
problem

    consult tablet "reciprocals"

    reciprocal-of-four :
        4
        take entry from reciprocals

result

    reciprocal-of-four
```

#### Canonical Cuneiform Mode
```text
𒂊𒁹

    𒅆 𒁾 "reciprocals"

    reciprocal-of-four :
        4
        pad 𒋫 reciprocals

𒅗𒁹

    reciprocal-of-four
```

### 2. Working Tablets & Inscription

Computational scratchpads are declared as working tablets (`kin` / `𒆥`). They are fast, mutable in-memory key-value mappings that disappear upon program termination unless explicitly inscribed:

```text
problem

    working observations

    put 42 into observations at 10

    inscribe observations as tablet "observations"

result

    observations
```

Inscription is strictly atomic: the new tablet version is either committed to the archive in its entirety with a cryptographic SHA-256 checksum, or the transaction fails leaving existing records completely intact.

### 3. Immutability, Monotonic Versioning & Lineage

Persistent tablets are strictly **immutable**. Once inscribed, a version cannot be overwritten or altered in place:
- **Derivation & Copying**: Creating a revision is performed via `copy tablet "T" as working W` or `derive tablet "T" as working W`.
- **Monotonic Versioning**: Re-inscribing creates version $N+1$ (`v1` -> `v2` -> `v3`), retaining complete historical lineage.
- **Version Pinning**: Programs can pin an exact historical version (`consult tablet "reciprocals" version 1`) to guarantee mathematical reproducibility across decades.

### 4. Standard Scholarly Archive ("Scribal Archive 1")

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

### 5. Archive CLI Tooling

Developers and scholars can manage and inspect the local archive using dedicated CLI subcommands:

```bash
# List all tablets in the archive
bin/dubsar archive list

# Display tablet contents and metadata
bin/dubsar archive show "reciprocals"

# Trace version history and provenance
bin/dubsar archive history "reciprocals"

# Export the archive to canonical JSON
bin/dubsar archive export -o archive.json

# Import tablets from canonical JSON
bin/dubsar archive import archive.json

# Render a tablet in ASCII/Unicode clay-style grid or vector SVG
bin/dubsar archive render "reciprocals"
bin/dubsar archive render "reciprocals" --style svg -o reciprocals.svg
```

### 6. End-to-End Archive Workflow: The Ea-nāṣir Copper Dispute

To demonstrate the full lifecycle of persistent archive consultation, exact rational calculation, mathematical determination, working tablet inscription, and monotonic revision with provenance tracking, DUB.SAR provides an end-to-end accounting workflow inspired by the world's oldest preserved customer complaint tablet (**UET V 72 / British Museum BM 131236**, c. 1750 BCE from Ur).

#### Historical Context vs. Computational Model

> **Historical Disclaimer**:
> This example is an illustrative computational demonstration of ancient administrative dispute settlement adapted to the DUB.SAR Tablet Archive.
>
> Historically, tablet UET V 72 records Nanni's passionate personal complaint to the merchant Ea-nāṣir concerning subpar copper ingots delivered after arduous transit through hostile territory ("What do you take me for, that you treat somebody like me with such contempt?"). The original clay tablet does not preserve modern tabular balance sheets or structured numerical matrices.
>
> In DUB.SAR, this historical dispute is formalized as an executable scribal audit workflow: structured delivery records are consulted from the persistent archive, quality deficiency is calculated using exact sexagesimal arithmetic, and an audit assessment tablet is inscribed into the archive with complete version lineage.

#### Conceptual Workflow

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

#### Step 1: Inscribing the Assessment Tablet (v1)

The audit program consults `ea-nasir-shipment`, extracts the promised and delivered quantities (each 10 talent), retrieves the required quality (`1`) and delivered ingot quality (`0;45`, or $3/4$), computes the exact quality deficiency ($1 - 0;45 = 0;15$), forms a mathematical determination, transfers it into a working tablet, and inscribes `ea-nasir-assessment` into the persistent archive.

##### Scholar Mode (`examples/ea_nasir_scholar.dub`)
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

##### Canonical Cuneiform Mode (`examples/ea_nasir.dub`)
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

#### Step 2: Monotonic Derivation & Verdict (v2)

When an official ruling is pronounced on the dispute, a subsequent program derives a working scratchpad directly from version 1 of `ea-nasir-assessment`, sets a `verdict` entry ("rejected"), and inscribes the revised tablet back to `ea-nasir-assessment`.

Because DUB.SAR tablets are strictly immutable:
- `ea-nasir-assessment` version 1 remains unaltered in the archive for historical auditability.
- `ea-nasir-assessment` version 2 is created with cryptographic checksum and provenance metadata: `derived_from: ea-nasir-assessment:v1`.

##### Scholar Mode (`examples/ea_nasir_revision_scholar.dub`)
```text
problem

    consult tablet "ea-nasir-assessment"

    derive from "ea-nasir-assessment" as working revised-assessment

    put "rejected" into revised-assessment at "verdict"

    inscribe revised-assessment as tablet "ea-nasir-assessment"

result

    "ea-nasir-assessment"
```

##### Canonical Cuneiform Mode (`examples/ea_nasir_revision.dub`)
```text
𒂊𒁹

    𒅆 𒁾 "ea-nasir-assessment"

    𒁴 𒋫 "ea-nasir-assessment" 𒁶 𒆥 revised-assessment

    𒃻 "rejected" 𒀀 revised-assessment 𒀀 "verdict"

    𒁹𒀀 revised-assessment 𒁶 𒁾 "ea-nasir-assessment"

𒅗𒁹

    "ea-nasir-assessment"
```

#### Persistent Tablet Entries and Metadata

| Tablet | Version | Key | Value | Metadata / Notes |
| :--- | :--- | :--- | :--- | :--- |
| `ea-nasir-shipment` | `1` | `merchant` | `"Ea-nāṣir"` | `origin`: `"Dilmun"`, `destination`: `"Ur"` |
| | | `promised-quantity` | `10 talent` | Metrological standard: 1 talent = 60 mina = 3600 shekels |
| | | `delivered-quantity` | `10 talent` | Full weight delivered |
| | | `required-quality` | `1` | Grade 1 (pure standard copper) |
| | | `actual-quality` | `0;45` | Grade 3/4 (substandard ingots) |
| `ea-nasir-assessment` | `1` | `deficiency` | `0;15` | Exact rational: $1 - 0;45 = 0;15$ ($1/4$ deficit) |
| `ea-nasir-assessment` | `2` | `verdict` | `"rejected"` | `derived_from`: `"ea-nasir-assessment:v1"` |

#### Inspecting and Rendering via CLI

Manage and inspect the audit workflow directly from the terminal:

```bash
# 1. View the original shipment record in the persistent archive
bin/dubsar archive show "ea-nasir-shipment"

# 2. Execute the assessment program (inscribes ea-nasir-assessment v1)
bin/dubsar run examples/ea_nasir_scholar.dub

# 3. View the newly inscribed assessment tablet
bin/dubsar archive show "ea-nasir-assessment"

# 4. Execute the revision program (derives and inscribes ea-nasir-assessment v2)
bin/dubsar run examples/ea_nasir_revision_scholar.dub

# 5. Trace the complete immutable version lineage and parent links
bin/dubsar archive history "ea-nasir-assessment"

# 6. Render the assessment tablet to terminal clay grid or vector SVG artwork
bin/dubsar archive render "ea-nasir-assessment"
bin/dubsar archive render "ea-nasir-assessment" --style svg -o examples/ea_nasir_assessment.svg
```

Pre-rendered clay tablet artwork artifacts for both tablets are available in the repository:
- [`examples/ea_nasir_shipment.svg`](examples/ea_nasir_shipment.svg) (Original shipment tablet)
- [`examples/ea_nasir_assessment.svg`](examples/ea_nasir_assessment.svg) (Inscribed assessment tablet)

---

## The Tablet-Oriented Data Model (Sequences, Tables, and Structured Records)

DUB.SAR provides a unified, first-class mathematical data model:

> **A tablet is an inscribed mathematical data object containing identifiable entries.**

Instead of borrowing modern concepts like generic arrays, vectors, Python lists, or SQL tables, DUB.SAR grounds all data collections in the physical and mathematical reality of the clay tablet.

### 1. The Three Tablet Shapes

1. **Sequence (`shape: sequence`)**:
   - Sequential, ordered entries keyed by contiguous non-negative integers ($0, 1, 2, \dots, N-1$).
   - Models numerical series, coefficients, polynomials, coordinate vectors, and observation streams.
   - Declared with an optional pre-allocated length: `working signal of length 1024`.
   - Supports auto-indexing append: `append 42 to signal` (or `signal 42 𒈭`).

2. **Mathematical Table (`shape: table`)**:
   - Associative mappings with arbitrary exact mathematical keys (integers, sexagesimal rationals, strings, or dimensioned quantities).
   - Models reciprocal tables, tables of squares and square roots, astronomical ephemerides, and metrological standards.
   - Entries set at specific exact keys: `put 0;30 into recips at 2` (or `recips 2 0;30 𒃻`).

3. **Structured Tablet (`shape: structured`)**:
   - Named fields representing compound physical or administrative entities.
   - Models celestial observations, shipment bills of lading, and multi-parameter problem states.
   - Initialized with inline field declarations:
     ```text
     working planet:
         mass : 100
         radius : 20
     ```

### 2. First-Class Tablet Operations

All operations are natively available in both **Scholar Mode** (prefix phrasing) and **Canonical Cuneiform Mode** (postfix operand-verb order):

| Operation | Scholar Mode (Prefix) | Canonical Cuneiform (Postfix) | Semantics |
| :--- | :--- | :--- | :--- |
| **Creation** | `working W [of length N] [:]` | `working W [of length N] [:]` | Allocates a mutable working tablet |
| **Retrieval** | `take entry K from T` | `T K 𒋗` | Looks up entry $K$. Raises `DubSarEntryNotFoundError` if absent |
| **Insertion** | `put V into W at K` | `W K V 𒃻` | Inserts or overwrites entry $K$ in working tablet $W$ |
| **Append** | `append V to W` | `W V 𒈭` | Appends value $V$ at the next sequential integer index |
| **Length** | `length of T` | `T 𒁍` | Evaluates to the exact dimensionless integer count of entries |
| **Removal** | `remove entry K from W` | `W K remove` | Deletes entry $K$ from working tablet $W$ |
| **First Entry** | `first from T` | `T first` | Retrieves the value of the earliest entry by key sort |
| **Last Entry** | `last from T` | `T last` | Retrieves the value of the latest entry by key sort |
| **Nearest Entry** | `seek entry nearest X in T` | `T X 𒊑` | Retrieves the entry whose key is closest to $X$ |
| **Iteration** | `consider entries of T:` | `consider entries of T:` | Iterates each entry value (bound to `entry` or `v`) |
| **Keyed Iteration** | `consider K, V of T:` | `consider K, V of T:` | Iterates each key and value pair |
| **Inscription** | `inscribe tablet W [as T]` | `𒁹𒀀 W [as T]` | Persists working tablet $W$ into the archive |

### 3. Safety Guarantees: Immutability and Exactness

- **Strict Immutability**: Modifying, appending to, or removing entries from a persistent archive tablet raises `DubSarImmutableTabletError` (alias `ImmutableTablet`). Persistent records can only be revised by deriving a working tablet and inscribing a new version.
- **Missing Entry Protection**: Attempting to take a non-existent entry raises `DubSarEntryNotFoundError` (alias `EntryNotFound`).
- **Exact Rational Guarantee**: Sequence indices, table keys, and values are preserved as exact rationals and quantities. No decimal or floating-point distortion can occur.

### 4. Canonical Tablet Model Examples

The repository includes four end-to-end runnable examples demonstrating the tablet-oriented data model:

- **Reciprocal Table Lookup** ([`examples/reciprocal_lookup_scholar.dub`](examples/reciprocal_lookup_scholar.dub) / [`examples/reciprocal_lookup.dub`](examples/reciprocal_lookup.dub)): Consults standard mathematical tablet `reciprocals` and performs exact division by multiplying by the reciprocal.
- **Sequence Generation** ([`examples/sequence_generation_scholar.dub`](examples/sequence_generation_scholar.dub) / [`examples/sequence_generation.dub`](examples/sequence_generation.dub)): Builds a Fibonacci-style sequence, inspects `length`, and queries `first` and `last`.
- **Sequence Transformation** ([`examples/sequence_transformation_scholar.dub`](examples/sequence_transformation_scholar.dub) / [`examples/sequence_transformation.dub`](examples/sequence_transformation.dub)): Iterates entries of an observation sequence with `consider entries of ...:` and creates a scaled working sequence.
- **Persistent Tablet Sequences** ([`examples/persistent_sequence_scholar.dub`](examples/persistent_sequence_scholar.dub) / [`examples/persistent_sequence.dub`](examples/persistent_sequence.dub)): Inscribes a working sequence tablet and queries persistent versioned entries.

---

## Geometric Mathematics Foundation & Coherent Path to Fourier Mathematics

DUB.SAR extends its mathematical model toward advanced numerical mathematics and harmonic analysis through an 8-layer progression grounded in ancient Mesopotamian scribal geometry:

```text
Exact Quantity (Universal Bedrock)
      │
      ▼
Ratio & Reciprocal
      │
      ▼
Geometric Determination (Right Triangles)
      │
      ▼
Inclination & Feed (Proportional Geometry)
      │
      ▼
Direction Abstraction (Ray Orientations)
      │
      ▼
The Turn System (Equal Circular Divisions)
      │
      ▼
Directed Quantities (Magnitude + Direction)
      │
      ▼
Tablet Fourier Mathematics (DFT & Radix-2 FFT)
```

Rather than bolting on modern floating-point primitives (`sin`, `cos`, `tan`, `exp(iθ)`, `complex`), DUB.SAR builds harmonic analysis organically from exact ratios, tablet sequences, and directed quantities.

### 1. The 8 Geometric & Fourier Layers

#### Layer A: Exact Quantity and Ratio (Universal Bedrock) `[attested]`
Every mathematical calculation in DUB.SAR operates on arbitrary-precision exact rationals ($p/q$) with compile-time algebraic dimensional safety. Quantities multiply, divide, and invert without silent floating-point conversions. Ratios and reciprocals are exact scribal pairings.

#### Layer B: Geometric Determinations and Right Triangles `[attested]`
Mesopotamian mathematics calculated with squares, square roots, and right triangles centuries before Pythagoras:
- **Exact Squares & Roots**: `square` and `square-root` compute exact integer squares and roots.
- **Right Triangle Determination**: `right-triangle` constructs a structured determination with fields `width`, `length`, `diagonal`, and boolean `is_valid` ($w^2 + l^2 = d^2$).
- **Missing Side Solver**: Given any two sides, `right-triangle` solves for the exact missing third side (or errors if non-integer).
- **Pythagorean Validation**: `validate-triangle` verifies whether three sides form a true integer right triangle.

```text
# Solving missing hypotenuse for base 3, height 4:
tri : 3 4 empty right-triangle
hypotenuse : tri.diagonal       # 5
valid : tri.is_valid            # 1
```

> **Scholarly Note on Plimpton 322**:
> Tablet Plimpton 322 (c. 1820–1762 BCE, Larsa) contains 15 rows of right triangle parameters. DUB.SAR maintains scholarly neutrality between:
> 1. **Eleanor Robson's scribal/pedagogical analysis**: Reciprocal pairs $(x, 1/x)$ generated within Old Babylonian scribal schooling.
> 2. **Mansfield & Wildberger's ratio-based trigonometry**: Exact ratio-based right-triangle geometry without circular angles.
> Both perspectives validate DUB.SAR's ratio-based geometric model.

#### Layer C: Inclination, Feed, and Proportional Geometry `[attested]`
Ancient canal, ramp, and ziggurat construction relied on proportional slopes rather than modern angles:
- **Inclination (*mūlû*)**: $\text{rise} / \text{run}$ — vertical rise per unit horizontal run.
- **Feed (*mūrqītu* / *šikittum*)**: $\text{run} / \text{rise}$ — horizontal setback per unit vertical rise.
- The `inclination` operator consumes `run` and `rise` to produce a determination with fields `rise`, `run`, `inclination`, and `feed`.
- The `feed` operator computes the reciprocal ratio directly.

#### Layer D: Direction Abstraction `[reconstructed]`
Direction in DUB.SAR represents an invariant ray orientation:
- Constructed from orthogonal components: `(run, rise) direction`.
- Constructed from circular fractions: `T direction` (where $T$ is a turn).
- Normalizes to unit components without exposing transcendental functions (`horizontal` and `vertical` coordinates).

#### Layer E: The Turn System `[attested / reconstructed]`
A turn represents a fraction of a full revolution $p/q \in [0, 1)$:
- Declared as `(p, q) turn`, capturing quarter-turns ($1/4$), half-turns ($1/2$), and sexagesimal steps ($1/60$, $1/360$).
- Addition, subtraction, and scaling wrap cyclically modulo $1$.

> **Historical Dating of the 360-Degree Division**:
> The 360-degree division of the circle was **not** a Sumerian invention. It was developed in **5th-century BCE Babylonian astronomy** (Achaemenid period, post-450 BCE) for the mathematical zodiac, dividing the ecliptic into 12 equal signs of 30 degrees.

#### Layer F: Directed Quantities `[reconstructed]`
A directed quantity binds a physical magnitude to an invariant direction:
- Constructed via `(magnitude, direction) directed`.
- Supports vector addition, scalar scaling, and rotation: `Q T rotate`.
- Rotation composes directions by adding turn fractions: $\text{Turn}_A + \text{Turn}_B \pmod 1$.

#### Layer G: Explicit Approximate Determinations `[reconstructed]`
When irrationals arise (such as the diagonal of a unit square, $\sqrt{2}$ on tablet YBC 7289):
- DUB.SAR never silently converts to IEEE float.
- Explicit approximation via `X approximate` executes bounded Babylonian Heron iterations:
  $$x_{n+1} = \frac{1}{2}\left(x_n + \frac{S}{x_n}\right)$$
- Yields a determination with fields `value` (rational estimate), `iterations`, and `error_bound`.

#### Layer H: Fourier Mathematics on Tablets (DFT & FFT) `[modern]`
DUB.SAR synthesizes ancient tablet sequences and directed rotations into modern harmonic analysis:
- **Sequence Tablet as Signal**: Time-domain and frequency-domain signals are represented purely as sequence tablets of directed quantities.
- **Harmonic Roots of Unity**: Rotations by $W_N^k = \text{turn}(-k/N)$ replace complex exponentials $e^{-2\pi i k / N}$.
- **Reference Discrete Fourier Transform (`dft`)**:
  $$X[k] = \sum_{n=0}^{N-1} x[n] \cdot \text{turn}\left(-\frac{k \cdot n}{N}\right)$$
- **Radix-2 Fast Fourier Transform (`fft`)**: Recursive Cooley-Tukey decimation-in-time algorithm for sequences of length $N = 2^m$.
- **Inverse Transforms (`inverse-dft`, `inverse-fft`)**: Normalized exact reconstruction ($1/N$ factor) satisfying energy conservation (Parseval's theorem).

### 2. First-Class Geometric & Fourier Operations

| Operation | Scholar Mode (Prefix / Postfix) | Canonical Cuneiform | Semantics |
| :--- | :--- | :--- | :--- |
| **Square** | `X square` | `X 𒉏` | Computes $X \cdot X$ |
| **Square Root** | `X square-root` | `X square-root` | Computes exact integer $\sqrt{X}$ (errors if non-square) |
| **Right Triangle** | `w l d right-triangle` | `w l d right-triangle` | Constructs right triangle determination; solves missing side |
| **Validate Triangle** | `w l d validate-triangle` | `w l d validate-triangle` | Validates if $w^2 + l^2 = d^2$ (returns 1 or 0) |
| **Inclination** | `run rise inclination` | `run rise inclination` | Constructs determination with `rise`, `run`, `inclination`, `feed` |
| **Feed** | `run rise feed` | `run rise feed` | Computes horizontal feed ratio ($\text{run} / \text{rise}$) |
| **Direction** | `dx dy direction` | `dx dy direction` | Constructs direction from orthogonal run/rise components |
| **Turn** | `p q turn` | `p q turn` | Constructs turn fraction $p/q \pmod 1$ |
| **Directed Quantity** | `mag dir directed` | `mag dir directed` | Binds scalar magnitude to directional ray |
| **Rotation** | `Q T rotate` | `Q T rotate` | Rotates directed quantity $Q$ by turn $T$ |
| **Approximation** | `X approximate` | `X approximate` | Computes bounded Heron-method rational approximation |
| **Discrete Fourier Transform** | `S dft` | `S dft` | Computes reference $O(N^2)$ DFT on sequence tablet $S$ |
| **Fast Fourier Transform** | `S fft` | `S fft` | Computes Cooley-Tukey $O(N \log N)$ FFT for length $2^m$ |
| **Inverse DFT** | `S inverse-dft` | `S inverse-dft` | Computes normalized inverse DFT reconstruction |
| **Inverse FFT** | `S inverse-fft` | `S inverse-fft` | Computes normalized inverse Radix-2 FFT reconstruction |

### 3. Historical Provenance Framework

To maintain scientific and historical integrity, DUB.SAR categorizes all mathematical constructs into explicit provenance tiers:

- **`[attested]`**: Directly verified in excavated cuneiform tablets.
  - Reciprocal tables, multiplication tables, squares, cubes.
  - Right triangle relationships (Plimpton 322, BM 85196, BM 34568).
  - Inclinations and feeds for embankments and ramps (*mūlû*, *mūrqītu*).
  - 360-degree circular division in 5th-century BCE Babylonian astronomy.
- **`[reconstructed]`**: Historically plausible scribal formalizations.
  - Direction abstraction based on run/rise ratios.
  - Rational turn arithmetic.
  - Bounded approximation determinations.
- **`[modern]`**: 20th-century computational mathematics synthesized into Mesopotamian paradigm.
  - Discrete Fourier Transform (DFT).
  - Radix-2 Cooley-Tukey Fast Fourier Transform (FFT).
  - Sequence-tablet harmonic decomposition without complex numbers.

### 4. Canonical Examples

The repository includes complete, runnable examples of geometric and Fourier computation:
- **Right Triangles & Pythagorean Geometry** ([`examples/geometry_triangle_scholar.dub`](examples/geometry_triangle_scholar.dub) / [`examples/geometry_triangle.dub`](examples/geometry_triangle.dub)): Solves missing hypotenuse, validates triangle triples, and consults the `right-triangles` archival tablet.
- **Slopes, Feeds & Directed Quantities** ([`examples/geometric_inclination_scholar.dub`](examples/geometric_inclination_scholar.dub) / [`examples/geometric_inclination.dub`](examples/geometric_inclination.dub)): Computes canal ramp inclination, feed, constructs directed vectors, and performs quarter-turn rotations.
- **Fourier Transform & Harmonic Analysis** ([`examples/fourier_dft_scholar.dub`](examples/fourier_dft_scholar.dub) / [`examples/fourier_dft.dub`](examples/fourier_dft.dub)): Verifies sequence length against `powers-of-two`, generates harmonic signal, executes both reference DFT and recursive Radix-2 FFT, and reconstructs signal via inverse DFT.

---

## Compiler & Runtime Architecture

```text
               .dub source (Tablet / Scholar / Mixed)
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │     Unicode Lexer     │ (Significant Indentation,
                     │  (dubsar/lexer.py)    │  Cuneiform Signs, Numerals)
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Recursive-Descent AST │ (Section 6 EBNF Grammar,
                     │  (dubsar/parser.py)   │  Redesign AST Nodes)
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   Semantic Analyzer   │ (Lexical Scopes, Compile-Time Units,
                     │ (dubsar/semantic.py)  │  Determinations & Range Checks)
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │  DUB.SAR Semantic IR  │ (Mathematical Verbs: ESTABLISH,
                     │ (dubsar/semantic_ir.py)│  TAKE, POSTFIX, RETAIN, DETERMINE)
                     └───────────┬───────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
                 ▼               ▼               ▼
        ┌────────────────┐┌─────────────┐┌───────────────┐
        │  AST Evaluator ││ Bytecode IR ││ WASM Compiler │
        │ (Interpreter)  ││ Compiler    ││ (dubsar/      │
        │                ││ (dubsar/    ││   wasm.py)    │
        │                ││   ir.py)    ││               │
        └────────────────┘└──────┬──────┘└───────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Virtual Machine │ (Operand Stack, Call Frames,
                        │ (dubsar/vm.py)  │  Exact Rational Engine)
                        └─────────────────┘
```

### Compiler Targets
| Target | Status | Description |
| :--- | :--- | :--- |
| **Reference AST Interpreter** | **Complete** | Full language support, exact arbitrary-precision rationals |
| **Stack Bytecode VM** | **Complete** | Stack IR, constant table, activation frames, determination ops |
| **Semantic IR** | **Complete** | Mathematical verbs layer (ESTABLISH, TAKE, POSTFIX, RETAIN, etc.) |
| **WebAssembly (.wat)** | **Complete** | Scalar-replaced determinations, bounded loops, 64-bit rational runtime |
| **Native Compiler** | *Planned* | LLVM / Cranelift native code generation backend |

---

## Historical Foundations vs. Modern Inventions

DUB.SAR bridges genuine ancient scribal traditions with 21st-century compiler construction:

### 1. Historically Grounded
- **Cuneiform Inscriptions**: Authentic Unicode cuneiform signs ($U+12000 \dots U+1247F$) and punctuation marks ($U+12480 \dots U+1254F$).
- **Sumerian Mathematical Vocabulary**: Keywords (`𒂊𒁹` *e-diš*, `𒁾𒊬` *dub-sar*, `𒅗𒁹` *ka-diš*, `𒄀` *gi*, `𒋫` *ta*, `𒂗` *en*, `𒌗` *iti*, `𒋼` *te*, `𒂊𒀀` *e-a*, `𒌉` *tur*, `𒃲` *gal*, `𒊓` *sa*, `𒈨` *me*, `𒉡` *nu*, `𒄥` *gur*, `𒉏` *nim*, `𒊑` *ri*, `𒍣` *zi*, `𒊭` *ša*, `𒉌` *ni*, `𒀝` *ak*, `𒉆` *nam*, `𒁹𒀀` *diš-a*, `𒀀𒁹` *a-diš*) reflect genuine Old Babylonian mathematical phrasing and scribal conventions.
- **Sexagesimal Positional System**: Positional base-60 representation for fractions and integers (`365;14,31,55`).
- **Tablet Organization**: The tripartite division of Problem Statement, Computational Prescriptions, and Inscribed Results mirrors Old Babylonian tablets (such as BM 13901 and YBC 7289).

### 2. Historically Inspired
- **Quantity-First Mathematics**: Numbers are not dimensionless bit-vectors, but named physical quantities (`(value, unit)`).
- **Mathematical Prescriptions**: Algorithms framed as constructive step-by-step recipes on clay rather than abstract procedures.
- **Bounded Determinism**: Absence of non-terminating loops, reflecting the finite, constructive nature of clay tablet mathematics.

### 3. Modern DUB.SAR Innovations
- **Syntactic Redesign**: Complete elimination of imperative keywords (`:=`, `=`, `def`, `return`, `if`, `else`, `while`) in favor of mathematical establishments, determinations, bounded domains, and atomic selections.
- **Exact Arbitrary-Precision Rational Runtime**: Arbitrary-precision integer arithmetic eliminating floating-point roundoff errors.
- **Compiler Architecture**: Lexer, recursive-descent AST, compile-time unit type checker, Semantic IR, stack VM bytecode, and WebAssembly backend.
- **Tooling**: Command-line interface, automated formatter, transliterator, and SVG vector renderer.

---

## Clay Tablet Rendering

DUB.SAR transforms your mathematical tablet code into an authentic Mesopotamian clay tablet SVG artwork complete with clay texture gradients, bevels, drop shadows, horizontal case rulings, and wedge impressions:

```bash
bin/dubsar render examples/planetary_leap.dub --style=tablet -o tablet.svg
```

You can also render directly to your terminal:
```text
╔════════════════════════════════════════════════════════════════╗
║                     TABLET: PLANETARY_LEAP                     ║
╠════════════════════════════════════════════════════════════════╣
║  𒑰 DUB.SAR 1.0 — Planetary Leap-Year Rule (Tablet Mode)       ║
║                                                                ║
║  𒂊𒁹                                                          ║
║                                                                ║
║      solar-year :                                              ║
║          𒀀𒁹 "solar year in days"                              ║
║                                                                ║
║      limit :                                                   ║
║          1000                                                  ║
║                                                                ║
║      whole-days :                                              ║
║          solar-year                                            ║
║          𒄥                                                    ║
║                                                                ║
║      fraction :                                                ║
║          solar-year                                            ║
║          whole-days                                            ║
║          𒋫                                                    ║
║                                                                ║
║      best :                                                    ║
║          𒉡                                                     ║
║                                                                ║
║      𒄀 cycle 𒋫 1 𒂗 limit:                                   ║
║                                                                ║
║          leaps :                                               ║
║              cycle                                             ║
║              fraction                                          ║
║              𒊭                                                ║
║              𒊑                                                ║
║                                                                ║
║          candidate-year :                                      ║
║              whole-days                                        ║
║              leaps                                             ║
║              cycle                                             ║
║              𒉌                                                ║
║              𒍣                                                ║
║                                                                ║
║          error :                                               ║
║              solar-year                                        ║
║              candidate-year                                    ║
║              𒋫                                                ║
║              𒋼                                                ║
║                                                                ║
║          candidate :                                           ║
║              cycle                                             ║
║              leaps                                             ║
║              error                                             ║
║                                                                ║
║          𒋼 candidate                                           ║
║              𒂊𒀀 error 𒊭 candidate                            ║
║              𒈨 𒌉 𒋫 error 𒊭 best                            ║
║                                                                ║
║  𒅗𒁹                                                          ║
║                                                                ║
║      best                                                      ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Included Examples

Explore the [`examples/`](examples/) directory for complete, verified tablets available in both **Canonical Cuneiform (Tablet Mode)** and **Scholar Mode (Latin Transliteration)**:

- **Planetary Leap-Year Rule**:
  - [`planetary_leap.dub`](examples/planetary_leap.dub) (Canonical Cuneiform)
  - [`planetary_leap_scholar.dub`](examples/planetary_leap_scholar.dub) (Scholar Mode)
- **Babylonian Square Diagonal ($\sqrt{2} \approx 1;24,51,10$ / Tablet YBC 7289)**:
  - [`babylonian_sqrt2.dub`](examples/babylonian_sqrt2.dub) (Canonical Cuneiform)
  - [`babylonian_sqrt2_scholar.dub`](examples/babylonian_sqrt2_scholar.dub) (Scholar Mode)
- **Tablet Archive & Persistent Knowledge**:
  - [`tablet_archive.dub`](examples/tablet_archive.dub) (Canonical Cuneiform)
  - [`tablet_archive_scholar.dub`](examples/tablet_archive_scholar.dub) (Scholar Mode)
- **Even Distribution of Leap Years**:
  - [`even_distribution.dub`](examples/even_distribution.dub) (Canonical Cuneiform)
  - [`even_distribution_scholar.dub`](examples/even_distribution_scholar.dub) (Scholar Mode)
- **Unit Conversions & Dimensional Safety**:
  - [`unit_conversion.dub`](examples/unit_conversion.dub) (Canonical Cuneiform)
  - [`unit_conversion_scholar.dub`](examples/unit_conversion_scholar.dub) (Scholar Mode)
- **The Ea-nāṣir Copper Dispute (Tablet Archive & Provenance)**:
  - [`ea_nasir.dub`](examples/ea_nasir.dub) (Canonical Cuneiform Assessment)
  - [`ea_nasir_scholar.dub`](examples/ea_nasir_scholar.dub) (Scholar Mode Assessment)
  - [`ea_nasir_revision.dub`](examples/ea_nasir_revision.dub) (Canonical Cuneiform Revision v2)
  - [`ea_nasir_revision_scholar.dub`](examples/ea_nasir_revision_scholar.dub) (Scholar Mode Revision v2)
  - [`ea_nasir_shipment.svg`](examples/ea_nasir_shipment.svg) (Clay Tablet Artwork: Shipment)
  - [`ea_nasir_assessment.svg`](examples/ea_nasir_assessment.svg) (Clay Tablet Artwork: Assessment)
- **Tablet Data Model (Sequences, Tables & Persistent Records)**:
  - [`reciprocal_lookup.dub`](examples/reciprocal_lookup.dub) / [`reciprocal_lookup_scholar.dub`](examples/reciprocal_lookup_scholar.dub) (Mathematical Table Lookup)
  - [`sequence_generation.dub`](examples/sequence_generation.dub) / [`sequence_generation_scholar.dub`](examples/sequence_generation_scholar.dub) (Sequence Generation)
  - [`sequence_transformation.dub`](examples/sequence_transformation.dub) / [`sequence_transformation_scholar.dub`](examples/sequence_transformation_scholar.dub) (Sequence Transformation)
  - [`persistent_sequence.dub`](examples/persistent_sequence.dub) / [`persistent_sequence_scholar.dub`](examples/persistent_sequence_scholar.dub) (Persistent Inscribed Sequence)
- **Right Triangles & Pythagorean Geometry**:
  - [`geometry_triangle.dub`](examples/geometry_triangle.dub) (Canonical Cuneiform)
  - [`geometry_triangle_scholar.dub`](examples/geometry_triangle_scholar.dub) (Scholar Mode)
- **Geometric Inclinations, Feeds & Directed Quantities**:
  - [`geometric_inclination.dub`](examples/geometric_inclination.dub) (Canonical Cuneiform)
  - [`geometric_inclination_scholar.dub`](examples/geometric_inclination_scholar.dub) (Scholar Mode)
- **Discrete & Fast Fourier Transform (DFT / Radix-2 FFT)**:
  - [`fourier_dft.dub`](examples/fourier_dft.dub) (Canonical Cuneiform)
  - [`fourier_dft_scholar.dub`](examples/fourier_dft_scholar.dub) (Scholar Mode)
- **Language Conformance Suite**:
  - [`conformance.dub`](examples/conformance.dub) (Canonical Cuneiform)
  - [`conformance_scholar.dub`](examples/conformance_scholar.dub) (Scholar Mode)

---

## Comprehensive Conformance & Testing

Run the full automated test suite:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

**184 unit, integration, and mathematical conformance test cases** cover:
- **Exhaustive Numeric Conformance**: Values `0`, `1`, `2`, `59`, `60`, `1;0`, `1;30`, `1;59,59`, `365;14,31,55`, `-1;30`, round-trip normalization, and exact arithmetic.
- **Static Unit Type Checking**: Compile-time detection of incompatible units (`1 day + 2 year`), dimensional products, cancellations, and explicit conversions.
- **Semantic IR & Verbs**: Verification of high-level mathematical verbs (`ESTABLISH`, `TAKE`, `POSTFIX`, `REPEAT`, `RETAIN`, `DETERMINE`).
- **Mathematical Redesign Conformance**: Quantities, multiline postfix pipelines, bounded domains, determinations, field lookups, atomic selections, and implicit result inscriptions.
- **Tablet Archive & Persistent Memory**: SQLite-backed embedded house of tablets, Scribal Archive 1 seeding, version pinning, provenance tracking, working tablet mutations, atomic inscriptions, and exact rational preservation.
- **Tablet Data Model**: Sequence allocation, indexed append, associative tables, nearest-key lookup, entry removal, and iteration.
- **Geometric Mathematics & Triangles**: Verification of exact squares, integer square roots, right-triangle determinations, Pythagorean validation, missing-side solving, and Plimpton 322 archival table lookup.
- **Inclinations, Directions & Turns**: Exact calculation of slope (rise/run) and feed (run/rise), directional ray normalization, modular turn arithmetic ($p/q \pmod 1$), directed quantities, vector additions, and quarter-turn rotations.
- **Fourier Transforms & Harmonic Reconstruction**: Exact sequence tablet processing, reference DFT ($O(N^2)$), recursive Cooley-Tukey Radix-2 FFT ($O(N \log N)$), normalized inverse transforms ($1/N$), and Parseval energy conservation.
- **Trimodal Source Equivalence**: Tablet, Scholar, and Mixed mode equivalence.
- **Independent Algorithm Validation**: Continued-fraction best rational approximations verified against bounded mathematical brute force.
- **Deterministic Leap Distribution**: Bresenham accumulator distribution.
- **AST Evaluator & VM Equivalence**: Exact rational parity between interpreter and VM.
- **Full WASM Lowering**: Determinations, procedures, loops, conditionals, and 64-bit rational runtime.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

The DUB.SAR 1.0 language specification and its historical inspirations are documented in [`DUB_SAR_1.0_Language_Specification.md`](DUB_SAR_1.0_Language_Specification.md).
