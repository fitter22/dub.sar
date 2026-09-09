<div align="center">

# 𒁾𒊬 — DUB.SAR 1.0

### The Executable Mesopotamian Mathematical Tablet Language

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Spec: 1.0](https://img.shields.io/badge/Specification-DUB.SAR%201.0-orange.svg)](DUB_SAR_1.0_Language_Specification.md)
[![Tests: 68 Passing](https://img.shields.io/badge/Tests-68%2F68%20Passing-brightgreen.svg)](tests/)
[![Architecture: VM + WASM](https://img.shields.io/badge/Architecture-Interpreter%20%7C%20VM%20%7C%20WASM-purple.svg)](dubsar/)
[![Vibe Coded](https://img.shields.io/badge/Built%20With-100%25%20Vibe%20Coding-ff69b4.svg)](#-vibe-coded-to-perfection)

<p align="center">
  <b>What if ancient Babylonian scribes had access to modern compiler technology?</b><br>
  DUB.SAR is an executable programming language designed from the perspective of an ancient Mesopotamian mathematical tablet, powered by arbitrary-precision rational mathematics, strict dimensional unit checking, a high-level mathematical Semantic IR, a stack bytecode virtual machine, and a WebAssembly compiler.
</p>

[Specification](DUB_SAR_1.0_Language_Specification.md) • [Architecture](#-compiler--runtime-architecture) • [Quickstart](#-quickstart) • [Examples](examples/) • [Clay Tablet Rendering](#-clay-tablet-rendering)

---

</div>

## 🏺 Why DUB.SAR?

Modern programming languages are built upon Von Neumann variables, arbitrary loops, and binary floating-point approximations.

**DUB.SAR (Sumerian: *dub-sar*, "scribe") reimagines computation from first principles:**

- 📜 **The Tablet Paradigm**: A source file is not a script; it is an **excavated tablet** (`IM.GID.DA`) composed of an initial **problem statement** (`𒂊𒁹`), reusable mathematical **prescriptions** (`𒁾𒊬`), and an inscribed **result section** (`𒅗𒁹`).
- 🧮 **Exact Sexagesimal Arithmetic**: Say goodbye to IEEE 754 floating-point inaccuracies. Every number is an **exact rational**, natively written and displayed in canonical Mesopotamian sexagesimal notation (`365;14,31,55`).
- 📐 **Algebraic Dimensional Safety**: Units are first-class citizens. `3 𒌓 + 2 𒌓` equals `5 𒌓`. Dimensions multiply algebraically (`2 𒌓 * 3 𒌓 = 6 day^2`). Incompatible dimensional operations (`1 day + 2 year`) are rejected statically at compile time before execution.
- 🔁 **Bounded Mathematical Repetition**: No infinite, non-deterministic `while` loops. Control flow is built around verifiable, bounded mathematical search over finite ranges (`𒄀 cycle 1 𒌗 limit:`).
- 🪶 **Trimodal Source Flexibility**: Write in authentic Unicode cuneiform (**Tablet Mode**), academic Latin transliteration (**Scholar Mode**), or seamlessly intermix both (**Mixed Mode**). All three normalize to identical abstract syntax trees and Semantic IR.
- 🎨 **Clay Artwork Generator**: Compile your computational tablet directly to a vector SVG rendering of an inscribed, case-ruled Mesopotamian clay tablet.

---

## ⚡ Vibe Coded to Perfection

> **This entire repository was 100% vibe coded.**
>
> From deciphering cuneiform numeral tables and designing an exact-rational sexagesimal arithmetic core to implementing an indentation-sensitive Unicode lexer, recursive-descent parser, compile-time unit type checker, high-level mathematical Semantic IR, stack-based bytecode virtual machine, complete WebAssembly backend, and SVG clay tablet renderer — every single line of code, documentation, and test suite was created in a flow of autonomous, specification-driven vibe coding.

---

## 🏛️ Trimodal Source Experience

### Tablet Mode (Canonical Cuneiform)
```text
𒂊𒁹

    𒈬 := 𒀀𒁹("solar year in days")
    maximum-cycle : 1000
    cycle, leaps, error := leap-rule(𒈬, maximum-cycle)

𒁾𒊬 leap-rule(solar, limit):

    whole := floor(solar)
    fraction := solar - whole
    fraction-count := fraction / 1 𒌓

    best-cycle := 1
    best-leaps := 0
    best-error := abs(solar - whole)

    𒄀 cycle 1 𒌗 limit:

        estimated-leaps := nearest(cycle * fraction-count)
        candidate := whole + (estimated-leaps / cycle) * 1 𒌓
        error := abs(solar - candidate)

        𒂊𒀀 error < best-error:

            best-error := error
            best-cycle := cycle
            best-leaps := estimated-leaps

    𒄑 best-cycle, best-leaps, best-error

𒅗𒁹

    𒁹𒀀 "normal days:"
    𒁹𒀀 floor(𒈬)
    𒁹𒀀 "cycle years:"
    𒁹𒀀 cycle
    𒁹𒀀 "leap years:"
    𒁹𒀀 leaps
    𒁹𒀀 "common years:"
    𒁹𒀀 cycle - leaps
    𒁹𒀀 "mean calendar year:"
    𒁹𒀀 floor(𒈬) + (leaps / cycle) * 1 𒌓
    𒁹𒀀 "error in days/year:"
    𒁹𒀀 error
```

### Scholar Mode (Latin Transliteration)
```text
PROBLEM

    mu := input("solar year in days")
    maximum-cycle : 1000
    cycle, leaps, error := leap-rule(mu, maximum-cycle)

procedure leap-rule(solar, limit):

    whole := floor(solar)
    fraction := solar - whole
    fraction-count := fraction / 1 day

    best-cycle := 1
    best-leaps := 0
    best-error := abs(solar - whole)

    repeat cycle 1 to limit:

        estimated-leaps := nearest(cycle * fraction-count)
        candidate := whole + (estimated-leaps / cycle) * 1 day
        error := abs(solar - candidate)

        if error < best-error:

            best-error := error
            best-cycle := cycle
            best-leaps := estimated-leaps

    return best-cycle, best-leaps, best-error

RESULT

    output "normal days:"
    output floor(mu)
    output "cycle years:"
    output cycle
    output "leap years:"
    output leaps
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.9 or higher (zero external runtime dependencies).

### Installation
Run directly from source or install via pip:
```bash
# Clone the repository
git clone https://github.com/fitter22/dub.sar.git
cd dub.sar

# Make launcher executable
chmod +x bin/dubsar
```

### Running Your First Tablet
Execute the Earth-like planetary leap-year calendar solver ($Y = 365.2422$ days):
```bash
python3 -m dubsar run examples/planetary_leap.dub --input="365.2422"
```

**Output:**
```text
normal days:
365 day
cycle years:
673
leap years:
163
common years:
510
mean calendar year:
365 + 163/673 day
error in days/year:
3/3365000 day
```
*Notice: DUB.SAR deterministically discovers the optimal 673-year cycle with 163 leap years, exactly matching Section 26.3 of the specification and confirmed by independent continued fraction expansion.*

---

## 🛠️ CLI Toolkit

The `dubsar` command line interface provides end-to-end tooling:

```bash
# 1. Execute via Virtual Machine (default) or AST Interpreter
python3 -m dubsar run examples/planetary_leap.dub --input="365.2422"
python3 -m dubsar run examples/planetary_leap.dub --backend=ast --input="365.2422"

# 2. Verify syntax and static dimensional safety (CR-003)
python3 -m dubsar check examples/planetary_leap.dub

# 3. Format and canonicalize tablet code (CR-040, CR-041)
python3 -m dubsar format examples/planetary_leap.dub --mode=tablet
python3 -m dubsar format examples/planetary_leap.dub --mode=scholar

# 4. Disassemble to stack bytecode
python3 -m dubsar compile examples/planetary_leap.dub --target=bytecode

# 5. Compile to WebAssembly Text (.wat) (CR-001)
python3 -m dubsar compile examples/planetary_leap.dub --target=wasm -o tablet.wat

# 6. Export AST as JSON
python3 -m dubsar compile examples/planetary_leap.dub --target=json

# 7. Bidirectional Transliteration (CR-039)
python3 -m dubsar transliterate examples/planetary_leap.dub
python3 -m dubsar cuneiform examples/planetary_leap_scholar.dub

# 8. Render Clay Tablet Artwork (CR-036)
python3 -m dubsar render examples/planetary_leap.dub --style=tablet -o tablet.svg
python3 -m dubsar render examples/planetary_leap.dub --style=text
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
                     │  (dubsar/parser.py)   │  Typed Expressions)
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   Semantic Analyzer   │ (Lexical Scopes, Compile-Time Units,
                     │ (dubsar/semantic.py)  │  Return Arity, Range Verification)
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │  DUB.SAR Semantic IR  │ (Mathematical Verbs: ESTABLISH,
                     │ (dubsar/semantic_ir.py)│  TAKE, ADD, REPEAT, DETERMINE)
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

### Compiler Target Status (CR-044)
| Target | Status | Notes |
| :--- | :--- | :--- |
| **Reference AST Interpreter** | **Complete** | Full 1.0 language, exact arbitrary-precision rationals |
| **Stack Bytecode VM** | **Complete** | Stack IR, constant table, frames, full 1.0 language |
| **Semantic IR** | **Complete** | Mathematical verbs layer (ESTABLISH, TAKE, ADD, REPEAT, etc.) |
| **WebAssembly (.wat)** | **Complete** | Full lowering of procedures, loops, conditionals, and 64-bit rational runtime |
| **Native Compiler** | *Planned* | LLVM / Cranelift native code generation backend |

---

## 📜 Historical Foundations vs. Modern Inventions (CR-043)

DUB.SAR is designed to remain true to historical mathematical practice while functioning as a modern programming language:

### 1. Historically Grounded
- **Cuneiform Script**: Written using Unicode cuneiform signs ($U+12000 \dots U+1247F$) and punctuation marks ($U+12480 \dots U+1254F$).
- **Sumerian Mathematical Vocabulary**: Keywords (`𒂊𒁹` *e-diš*, `𒁾𒊬` *dub-sar*, `𒅗𒁹` *ka-diš*, `𒍣` *zi*, `𒋫` *ta*, `𒊭` *ša*, `𒉌` *ni*) reflect genuine administrative and scribal mathematics.
- **Sexagesimal System**: Positional base-60 representation for fractions and integers (`integer;digit,digit,...`).
- **Tablet Organization**: The tripartite division of Problem Statement, Computational Prescriptions, and Inscribed Results directly mirrors Old Babylonian worked problem tablets (such as BM 13901).

### 2. Historically Inspired
- **Quantity-First Mathematics**: Treating numbers not as dimensionless bit-vectors, but as named physical/abstract quantities (`(value, unit)`).
- **Prescriptive Recipe Procedures**: Mathematical algorithms framed as concrete recipes and step-by-step tablets rather than generic abstract subroutines.
- **Bounded Determinism**: Absence of non-terminating loops, reflecting the finite, constructive nature of clay tablet computations.

### 3. Modern DUB.SAR Inventions
- **Syntactic Constructs**: Block indentation, modern assignment (`:=`), procedure declarations, and comma-separated parameter lists.
- **Exact Arbitrary-Precision Rational Runtime**: Seamless arbitrary-precision integer arithmetic eliminating floating-point errors.
- **Compiler Architecture**: Lexer, recursive-descent AST, compile-time unit type checker, Semantic IR, stack VM bytecode, and WebAssembly backend.
- **Tooling**: Command-line interface, automated formatter, transliterator, and SVG vector renderer.

---

## 🎨 Clay Tablet Rendering

DUB.SAR can transform any tablet source into an authentic Mesopotamian clay tablet SVG artwork with drop shadows, clay texture gradients, bevels, horizontal case rulings, and wedge impressions:

```bash
python3 -m dubsar render examples/planetary_leap.dub --style=tablet -o tablet.svg
```

You can also render directly to your terminal:
```text
╔════════════════════════════════════════════════════════════════════════╗
║                         TABLET: PLANETARY_LEAP                         ║
╠════════════════════════════════════════════════════════════════════════╣
║  # DUB.SAR 1.0 — Planetary Leap-Year Rule (Tablet Mode)                ║
║  # As specified in Section 26 of DUB.SAR 1.0 Language Specification    ║
║                                                                        ║
║  𒂊𒁹                                                                    ║
║                                                                        ║
║      𒈬 := 𒀀𒁹("solar year in days")                                    ║
║      maximum-cycle : 1000                                              ║
║      cycle, leaps, error := leap-rule(𒈬, maximum-cycle)                 ║
║                                                                        ║
║  𒁾𒊬 leap-rule(solar, limit):                                           ║
║                                                                        ║
║      whole := floor(solar)                                             ║
║      fraction := solar - whole                                         ║
║      fraction-count := fraction / 1 𒌓                                  ║
║                                                                        ║
║      best-cycle := 1                                                   ║
║      best-leaps := 0                                                   ║
║      best-error := abs(solar - whole)                                  ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## 📚 Included Examples

Explore the [`examples/`](examples/) directory for complete, verified tablets:

- 🪐 **[`planetary_leap.dub`](examples/planetary_leap.dub)**: The canonical Section 26 planetary leap-year rule in full cuneiform.
- 📜 **[`planetary_leap_scholar.dub`](examples/planetary_leap_scholar.dub)**: The same planetary problem in Scholar Latin transliteration.
- ⚖️ **[`even_distribution.dub`](examples/even_distribution.dub)**: Section 27 Bresenham leap-year accumulator distributing leap days evenly over a calendar cycle.
- 📐 **[`babylonian_sqrt2.dub`](examples/babylonian_sqrt2.dub)**: Tablet YBC 7289 calculation of the diagonal of a square ($\sqrt{2} \approx 1;24,51,10$).
- ⏱️ **[`unit_conversion.dub`](examples/unit_conversion.dub)**: Explicit conversions across `second`, `minute`, `hour`, and `day`.
- ✅ **[`conformance.dub`](examples/conformance.dub)**: Section 29 formal language conformance test suite.

---

## 🧪 Comprehensive Conformance & Testing

Run the full automated test suite:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

**68 unit and integration test cases** cover:
- **Exhaustive Numeric Conformance (CR-016)**: Values `0`, `1`, `2`, `59`, `60`, `1;0`, `1;30`, `1;59,59`, `365;14,31,55`, `-1;30`, round-trip normalization, and exact arithmetic.
- **Static Unit Type Checking (CR-003)**: Compile-time detection of incompatible units (`1 day + 2 year`), dimensional products, cancellations, and explicit conversions.
- **Semantic IR & Verbs (CR-011, CR-024)**: Verification of high-level mathematical verbs (`ESTABLISH`, `TAKE`, `ADD`, `REPEAT`, `DETERMINE`, etc.).
- **Trimodal Source Equivalence (CR-006)**: Tablet, Scholar, and Mixed mode equivalence.
- **Independent Algorithm Validation (CR-034)**: Continued fraction best rational approximations verified against bounded brute force.
- **Deterministic Leap Distribution (CR-035)**: Bresenham accumulator distribution.
- **AST Evaluator & VM Equivalence (CR-046)**: Exact rational comparison between interpreter and VM.
- **Full WASM Lowering (CR-001, CR-002)**: Procedures, parameters, locals, loops, conditionals, and rational runtime.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

The DUB.SAR 1.0 language specification and its historical inspirations are documented in [`DUB_SAR_1.0_Language_Specification.md`](DUB_SAR_1.0_Language_Specification.md).