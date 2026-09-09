<div align="center">

# 𒁾𒊬 — DUB.SAR 1.0

### The Executable Mesopotamian Mathematical Tablet Language

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Spec: 1.0](https://img.shields.io/badge/Specification-DUB.SAR%201.0-orange.svg)](DUB_SAR_1.0_Language_Specification.md)
[![Tests: 79 Passing](https://img.shields.io/badge/Tests-79%2F79%20Passing-brightgreen.svg)](tests/)
[![Architecture: VM + WASM](https://img.shields.io/badge/Architecture-Interpreter%20%7C%20VM%20%7C%20WASM-purple.svg)](dubsar/)
[![Vibe Coded](https://img.shields.io/badge/Built%20With-100%25%20Vibe%20Coding-ff69b4.svg)](#-vibe-coded-to-perfection)

<p align="center">
  <b>What if ancient Babylonian scribes had designed a modern programming language?</b><br>
  DUB.SAR is not a Python dialect in cuneiform costume. It is an executable Mesopotamian mathematical tablet language engineered from first principles — featuring exact arbitrary-precision rational arithmetic, algebraic dimensional unit safety, bounded mathematical search domains, postfix calculation pipelines, atomic selections, a high-level Semantic IR, a stack bytecode virtual machine, and a WebAssembly compiler.
</p>

[Specification](DUB_SAR_1.0_Language_Specification.md) • [Architecture](#-compiler--runtime-architecture) • [Quickstart](#-quickstart) • [Examples](examples/) • [Clay Tablet Rendering](#-clay-tablet-rendering)

---

</div>

## 🏺 Why DUB.SAR?

Modern programming languages are encumbered with Von Neumann memory mutations, uncontrolled `while` loops, assignment operators (`=`, `:=`), subroutine returns (`def`, `return`), and IEEE 754 binary floating-point roundoff errors.

**DUB.SAR (Sumerian: *dub-sar*, "scribe") reimagines computation as an excavated mathematical clay tablet:**

- 📜 **The Tablet Paradigm**: Programs are computational tablets (`IM.GID.DA`) structured in authentic scribal sections: a **Problem Statement** (`𒂊𒁹` / `problem`), reusable **Prescription Recipes** (`𒁾𒊬` / `recipe`), and an **Inscribed Result** (`𒅗𒁹` / `result`).
- 🚫 **No Imperative Gimmicks**: Say goodbye to `:=`, `=`, `def`, `return`, `for`, `while`, `if`, `else`, and `class`. DUB.SAR expresses computation purely through **Quantity Establishment** (`name : expression`), **Mathematical Determinations** (`candidate : cycle, leaps, error`), **Finite Search Domains** (`consider cycle from 1 through limit:`), and **Atomic Selection** (`retain candidate when error is lesser than best.error`).
- 🧮 **Exact Sexagesimal Rational Engine**: Every numeric value is an exact arbitrary-precision rational fraction, natively written, computed, and displayed in canonical Mesopotamian sexagesimal notation (`365;14,31,55`). Floating-point inaccuracies simply do not exist.
- 📐 **Algebraic Dimensional Safety**: Units are first-class mathematical entities. Quantities multiply and divide algebraically (`2 day * 3 day = 6 day^2`). Incompatible dimensional operations (`1 day + 2 year`) are statically rejected at compile time.
- 🔄 **Postfix Calculation Pipelines**: Calculations unfold through clear mathematical reductions:
  ```text
  whole-days : solar-year floor
  fraction : solar-year whole-days subtract
  ```
- 🪶 **Trimodal Source Flexibility**: Write in authentic Unicode cuneiform (**Tablet Mode**), academic Latin transliteration (**Scholar Mode**), or intermix both (**Mixed Mode**). All three representations normalize into an identical abstract syntax tree and Semantic IR.
- 🎨 **Clay Artwork Generator**: Compile any tablet directly to a vector SVG rendering of an inscribed, case-ruled Mesopotamian clay tablet with bevels, drop shadows, and wedge impressions.

---

## ⚡ Vibe Coded to Perfection

> **This entire repository was 100% vibe coded.**
>
> From deciphering historical cuneiform numeral tables and designing an exact-rational sexagesimal arithmetic core to implementing an indentation-sensitive Unicode lexer, recursive-descent parser, compile-time unit type checker, high-level mathematical Semantic IR, stack-based bytecode virtual machine, complete WebAssembly backend, and SVG clay tablet renderer — every single line of code, specification, and test suite was built in an uninterrupted flow of specification-driven vibe coding.

---

## 🏛️ Trimodal Source Experience

DUB.SAR provides dual canonical representations of the same mathematical tablet:

### Tablet Mode (Canonical Cuneiform)
```text
𒑰 DUB.SAR 1.0 — Planetary Leap-Year Rule (Tablet Mode)

𒂊𒁹

    solar-year : 𒀀𒁹 "solar year in days"
    limit : 1000

    whole-days :
        solar-year
        𒄥

    fraction :
        solar-year
        whole-days
        𒋫

    best : 𒉡

    𒄀 cycle 𒋫 1 𒌗 limit:

        leaps :
            cycle
            fraction
            𒊭
            𒊑

        error :
            whole-days
            leaps
            cycle
            𒉌
            𒍣
            solar-year
            𒋫
            𒋼

        candidate :
            cycle
            leaps
            error

        𒋼 candidate 𒂊𒀀 error 𒌉 best.error

𒅗𒁹

    best
```

### Scholar Mode (Academic Latin Transliteration)
```text
# DUB.SAR 1.0 — Planetary Leap-Year Rule (Scholar Mode)

problem

    solar-year : ask "solar year in days"
    limit : 1000

    whole-days :
        solar-year
        floor

    fraction :
        solar-year
        whole-days
        subtract

    best : empty

    consider cycle from 1 through limit:

        leaps :
            cycle
            fraction
            multiply
            nearest

        error :
            whole-days
            leaps
            cycle
            divide
            add
            solar-year
            subtract
            absolute

        candidate :
            cycle
            leaps
            error

        retain candidate when error is lesser than best.error

result

    best
```

---

## 🚀 Quickstart

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

## 🛠️ CLI Toolkit

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
```

---

## 🏗️ Compiler & Runtime Architecture

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

## 📜 Historical Foundations vs. Modern Inventions

DUB.SAR bridges genuine ancient scribal traditions with 21st-century compiler construction:

### 1. Historically Grounded
- **Cuneiform Inscriptions**: Authentic Unicode cuneiform signs ($U+12000 \dots U+1247F$) and punctuation marks ($U+12480 \dots U+1254F$).
- **Sumerian Mathematical Vocabulary**: Keywords (`𒂊𒁹` *e-diš*, `𒁾𒊬` *dub-sar*, `𒅗𒁹` *ka-diš*, `𒄀` *gi*, `𒋫` *ta*, `𒌗` *iti*, `𒋼` *te*, `𒂊𒀀` *e-a*, `𒌉` *tur*, `𒃲` *gal*, `𒊓` *sa*, `𒉡` *nu*, `gur`, `nim`, `ri`, `zi`, `sha`, `ni`) reflect genuine Old Babylonian mathematical phrasing.
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

## 🎨 Clay Tablet Rendering

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
║      solar-year : 𒀀𒁹 "solar year in days"                    ║
║      limit : 1000                                              ║
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
║      best : 𒉡                                                 ║
║                                                                ║
║      𒄀 cycle 𒋫 1 𒌗 limit:                                   ║
║                                                                ║
║          leaps :                                               ║
║              cycle                                             ║
║              fraction                                          ║
║              𒊭                                                ║
║              𒊑                                                ║
║                                                                ║
║          error :                                               ║
║              whole-days                                        ║
║              leaps                                             ║
║              cycle                                             ║
║              𒉌                                                ║
║              𒍣                                                ║
║              solar-year                                        ║
║              𒋫                                                ║
║              𒋼                                                ║
║                                                                ║
║          candidate :                                           ║
║              cycle                                             ║
║              leaps                                             ║
║              error                                             ║
║                                                                ║
║          𒋼 candidate 𒂊𒀀 error 𒌉 best.error                 ║
║                                                                ║
║  𒅗𒁹                                                          ║
║                                                                ║
║      best                                                      ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 📚 Included Examples

Explore the [`examples/`](examples/) directory for complete, verified tablets:

- 🪐 **[`planetary_leap.dub`](examples/planetary_leap.dub)**: The canonical planetary leap-year rule in full cuneiform Tablet Mode.
- 📜 **[`planetary_leap_scholar.dub`](examples/planetary_leap_scholar.dub)**: The planetary leap-year rule in Scholar Mode Latin transliteration.
- ⚖️ **[`even_distribution.dub`](examples/even_distribution.dub)**: Section 27 Bresenham leap-year accumulator distributing leap days evenly over a calendar cycle.
- 📐 **[`babylonian_sqrt2.dub`](examples/babylonian_sqrt2.dub)**: Tablet YBC 7289 calculation of the diagonal of a square ($\sqrt{2} pprox 1;24,51,10$).
- ⏱️ **[`unit_conversion.dub`](examples/unit_conversion.dub)**: Explicit unit conversions across `second`, `minute`, `hour`, and `day`.
- ✅ **[`conformance.dub`](examples/conformance.dub)**: Formal language conformance test suite.

---

## 🧪 Comprehensive Conformance & Testing

Run the full automated test suite:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

**79 unit, integration, and mathematical conformance test cases** cover:
- **Exhaustive Numeric Conformance**: Values `0`, `1`, `2`, `59`, `60`, `1;0`, `1;30`, `1;59,59`, `365;14,31,55`, `-1;30`, round-trip normalization, and exact arithmetic.
- **Static Unit Type Checking**: Compile-time detection of incompatible units (`1 day + 2 year`), dimensional products, cancellations, and explicit conversions.
- **Semantic IR & Verbs**: Verification of high-level mathematical verbs (`ESTABLISH`, `TAKE`, `POSTFIX`, `REPEAT`, `RETAIN`, `DETERMINE`).
- **Mathematical Redesign Conformance**: Quantities, multiline postfix pipelines, bounded domains, determinations, field lookups, atomic selections, and implicit result inscriptions.
- **Trimodal Source Equivalence**: Tablet, Scholar, and Mixed mode equivalence.
- **Independent Algorithm Validation**: Continued-fraction best rational approximations verified against bounded mathematical brute force.
- **Deterministic Leap Distribution**: Bresenham accumulator distribution.
- **AST Evaluator & VM Equivalence**: Exact rational parity between interpreter and VM.
- **Full WASM Lowering**: Determinations, procedures, loops, conditionals, and 64-bit rational runtime.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

The DUB.SAR 1.0 language specification and its historical inspirations are documented in [`DUB_SAR_1.0_Language_Specification.md`](DUB_SAR_1.0_Language_Specification.md).
