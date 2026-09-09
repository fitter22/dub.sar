<div align="center">

# 𒁾𒊬 — DUB.SAR 1.0

### The Executable Mesopotamian Mathematical Tablet Language

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Spec: 1.0](https://img.shields.io/badge/Specification-DUB.SAR%201.0-orange.svg)](DUB_SAR_1.0_Language_Specification.md)
[![Tests: 131 Passing](https://img.shields.io/badge/Tests-131%2F131%20Passing-brightgreen.svg)](tests/)
[![Architecture: VM + WASM](https://img.shields.io/badge/Architecture-Interpreter%20%7C%20VM%20%7C%20WASM-purple.svg)](dubsar/)
[![Vibe Coded](https://img.shields.io/badge/Built%20With-100%25%20Vibe%20Coding-ff69b4.svg)](#vibe-coded-to-perfection)

<p align="center">
  <b>What if ancient Babylonian scribes had designed a modern programming language?</b><br>
  DUB.SAR is not a Python dialect in cuneiform costume. It is an executable Mesopotamian mathematical tablet language engineered from first principles — featuring exact arbitrary-precision rational arithmetic, algebraic dimensional unit safety, bounded mathematical search domains, postfix calculation pipelines, atomic selections, a high-level Semantic IR, a stack bytecode virtual machine, and a WebAssembly compiler.
</p>

[Specification](DUB_SAR_1.0_Language_Specification.md) • [Architecture](#compiler--runtime-architecture) • [Quickstart](#quickstart) • [Tablet Archive](#the-tablet-archive) • [Examples](examples/) • [Clay Tablet Rendering](#clay-tablet-rendering)

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

Every new DUB.SAR archive automatically initializes with standard scholarly reference tablets:
- `reciprocals`: Authentic Old Babylonian reciprocal pairs ($2 \to 0;30$, $3 \to 0;20$, $4 \to 0;15$, $5 \to 0;12$, $6 \to 0;10$, $8 \to 0;07,30$, etc.).
- `common-fractions`: Exact sexagesimal representations of fundamental fractions ($1/2, 1/3, 2/3, 1/4, 3/4, 1/5, 5/6$).
- `squares`: Exact integer squares for numbers $1$ through $60$.
- `cubes`: Exact integer cubes for numbers $1$ through $30$.
- `square-roots`: Verified rational approximations and exact integer roots.
- `powers`: Powers of fundamental bases ($2$ and $60$).
- `basic-metrology`: Attested conversion factors for length, area, and capacity.
- `basic-geometry`: Attested geometric coefficients.

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

# Render a tablet in ASCII/Unicode clay-style grid
bin/dubsar archive render "reciprocals"
```

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
- **Language Conformance Suite**:
  - [`conformance.dub`](examples/conformance.dub) (Canonical Cuneiform)
  - [`conformance_scholar.dub`](examples/conformance_scholar.dub) (Scholar Mode)

---

## Comprehensive Conformance & Testing

Run the full automated test suite:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

**131 unit, integration, and mathematical conformance test cases** cover:
- **Exhaustive Numeric Conformance**: Values `0`, `1`, `2`, `59`, `60`, `1;0`, `1;30`, `1;59,59`, `365;14,31,55`, `-1;30`, round-trip normalization, and exact arithmetic.
- **Static Unit Type Checking**: Compile-time detection of incompatible units (`1 day + 2 year`), dimensional products, cancellations, and explicit conversions.
- **Semantic IR & Verbs**: Verification of high-level mathematical verbs (`ESTABLISH`, `TAKE`, `POSTFIX`, `REPEAT`, `RETAIN`, `DETERMINE`).
- **Mathematical Redesign Conformance**: Quantities, multiline postfix pipelines, bounded domains, determinations, field lookups, atomic selections, and implicit result inscriptions.
- **Tablet Archive & Persistent Memory**: SQLite-backed embedded house of tablets, Scribal Archive 1 seeding, version pinning, provenance tracking, working tablet mutations, atomic inscriptions, and exact rational preservation.
- **Trimodal Source Equivalence**: Tablet, Scholar, and Mixed mode equivalence.
- **Independent Algorithm Validation**: Continued-fraction best rational approximations verified against bounded mathematical brute force.
- **Deterministic Leap Distribution**: Bresenham accumulator distribution.
- **AST Evaluator & VM Equivalence**: Exact rational parity between interpreter and VM.
- **Full WASM Lowering**: Determinations, procedures, loops, conditionals, and 64-bit rational runtime.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

The DUB.SAR 1.0 language specification and its historical inspirations are documented in [`DUB_SAR_1.0_Language_Specification.md`](DUB_SAR_1.0_Language_Specification.md).
