<div align="center">

# 𒁾𒊬 — DUB.SAR 1.0

### The Executable Mesopotamian Mathematical Tablet Language

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Spec: 1.0](https://img.shields.io/badge/Specification-DUB.SAR%201.0-orange.svg)](DUB_SAR_1.0_Language_Specification.md)
[![Tests: 50 Passing](https://img.shields.io/badge/Tests-50%2F50%20Passing-brightgreen.svg)](tests/)
[![Architecture: VM + WASM](https://img.shields.io/badge/Architecture-Interpreter%20%7C%20VM%20%7C%20WASM-purple.svg)](dubsar/)
[![Vibe Coded](https://img.shields.io/badge/Built%20With-100%25%20Vibe%20Coding-ff69b4.svg)](#-vibe-coded-to-perfection)

<p align="center">
  <b>What if ancient Babylonian scribes had access to modern compiler technology?</b><br>
  DUB.SAR is an executable programming language designed from the perspective of an ancient Mesopotamian mathematical tablet, powered by arbitrary-precision rational mathematics, strict dimensional unit checking, a stack bytecode virtual machine, and a WebAssembly compiler.
</p>

[Specification](DUB_SAR_1.0_Language_Specification.md) • [Architecture](#-compiler--runtime-architecture) • [Quickstart](#-quickstart) • [Examples](examples/) • [Clay Tablet Rendering](#-clay-tablet-rendering)

---

</div>

## 🏺 Why DUB.SAR?

Modern programming languages are built upon Von Neumann variables, arbitrary loops, and binary floating-point approximations.

**DUB.SAR (Sumerian: *dub-sar*, "scribe") reimagines computation from first principles:**

- 📜 **The Tablet Paradigm**: A source file is not a script; it is an **excavated tablet** (`IM.GID.DA`) composed of an initial **problem statement** (`𒂊𒁹`), reusable mathematical **prescriptions** (`𒁾𒊬`), and an inscribed **result section** (`𒅗𒁹`).
- 🧮 **Exact Sexagesimal Arithmetic**: Say goodbye to IEEE 754 floating-point inaccuracies. Every number is an **exact rational**, natively written and displayed in canonical Mesopotamian sexagesimal notation (`365;14,31,55`).
- 📐 **Algebraic Dimensional Safety**: Units are first-class citizens. `3 𒌓 + 2 𒌓` equals `5 𒌓`. Dimensions multiply algebraically (`2 𒌓 * 3 𒌓 = 6 day^2`). Adding `1 day + 2 year` without explicit astronomical conversion is rejected by the compiler.
- 🔁 **Bounded Mathematical Repetition**: No infinite, non-deterministic `while` loops. Control flow is built around verifiable, bounded mathematical search over finite ranges (`𒄀 cycle 1 𒌗 limit:`).
- 🪶 **Trimodal Source Flexibility**: Write in authentic Unicode cuneiform (**Tablet Mode**), academic Latin transliteration (**Scholar Mode**), or seamlessly intermix both (**Mixed Mode**). All three normalize to identical abstract syntax trees.
- 🎨 **Clay Artwork Generator**: Compile your computational tablet directly to a vector SVG rendering of an inscribed, case-ruled Mesopotamian clay tablet.

---

## ⚡ Vibe Coded to Perfection

> **This entire repository was 100% vibe coded.**
>
> From deciphering cuneiform numeral tables and designing an exact-rational sexagesimal arithmetic core to implementing an indentation-sensitive Unicode lexer, recursive-descent parser, semantic scope validator, stack-based bytecode virtual machine, WebAssembly backend, and SVG clay tablet renderer — every single line of code, documentation, and test suite was created in a flow of autonomous, specification-driven vibe coding.

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
*Notice: DUB.SAR deterministically discovers the optimal 673-year cycle with 163 leap years, exactly matching Section 26.3 of the specification.*

---

## 🛠️ CLI Toolkit

The `dubsar` command line interface provides end-to-end tooling:

```bash
# 1. Execute via Virtual Machine (default) or AST Interpreter
python3 -m dubsar run examples/planetary_leap.dub --input="365.2422"
python3 -m dubsar run examples/planetary_leap.dub --backend=ast --input="365.2422"

# 2. Verify syntax and static semantic safety
python3 -m dubsar check examples/planetary_leap.dub

# 3. Disassemble to stack bytecode
python3 -m dubsar compile examples/planetary_leap.dub --target=bytecode

# 4. Compile to WebAssembly Text (.wat)
python3 -m dubsar compile examples/planetary_leap.dub --target=wasm -o tablet.wat

# 5. Export AST as JSON
python3 -m dubsar compile examples/planetary_leap.dub --target=json

# 6. Bidirectional Transliteration
python3 -m dubsar transliterate examples/planetary_leap.dub
python3 -m dubsar cuneiform examples/planetary_leap_scholar.dub

# 7. Render Clay Tablet Artwork
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
                     │   Semantic Analyzer   │ (Lexical Scopes, 7 Error Types,
                     │ (dubsar/semantic.py)  │  Dimensional Compatibility)
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

### Core Architecture Components
1. **[`dubsar/numbers.py`](dubsar/numbers.py)**: Exact arbitrary-precision rational number core (`Rational`), sexagesimal literal parser (`integer;d1,d2,...`), cuneiform numeral resolution table (`DUB_SAR_NUMERAL_TABLE`), and round-away-from-zero logic.
2. **[`dubsar/units.py`](dubsar/units.py)**: Algebraic dimensional analysis system (`Unit`, `Quantity`). Enforces compatibility on addition/subtraction and computes products/quotients of physical dimensions.
3. **[`dubsar/lexer.py`](dubsar/lexer.py)**: State-aware Unicode lexer handling cuneiform multi-sign tokens, scholar aliases, comments (`#` and `𒑰`), and significant indentation blocks.
4. **[`dubsar/parser.py`](dubsar/parser.py)**: Hand-written recursive descent parser strictly implementing the normative EBNF grammar.
5. **[`dubsar/semantic.py`](dubsar/semantic.py)**: Static semantic validator verifying identifier resolution, procedure signatures, and range boundaries.
6. **[`dubsar/builtins.py`](dubsar/builtins.py)**: Standard mathematical recipes: `abs`, `floor`, `ceil`, `nearest`, `min`, `max`, `gcd`, `lcm`, and `convert`.
7. **[`dubsar/interpreter.py`](dubsar/interpreter.py)**: Stage 1 tree-walking reference interpreter.
8. **[`dubsar/ir.py`](dubsar/ir.py)** & **[`dubsar/vm.py`](dubsar/vm.py)**: Stage 2 stack-oriented bytecode compiler and virtual machine.
9. **[`dubsar/wasm.py`](dubsar/wasm.py)**: Stage 3 WebAssembly code generator emitting standard `.wat`.
10. **[`dubsar/normalizer.py`](dubsar/normalizer.py)**: Bidirectional transliteration engine.
11. **[`dubsar/renderer.py`](dubsar/renderer.py)**: Vector graphics tablet renderer creating realistic clay tablet artifacts.

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
║  𒂊𒁹                                                                  ║
║                                                                        ║
║      𒈬 := 𒀀𒁹("solar year in days")                                  ║
║      maximum-cycle : 1000                                              ║
║      cycle, leaps, error := leap-rule(𒈬, maximum-cycle)               ║
║                                                                        ║
║  𒁾𒊬 leap-rule(solar, limit):                                         ║
║                                                                        ║
║      whole := floor(solar)                                             ║
║      fraction := solar - whole                                         ║
║      fraction-count := fraction / 1 𒌓                                 ║
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
- ⚖️ **[`even_distribution.dub`](examples/even_distribution.dub)**: Section 27 leap-year accumulator distributing leap days evenly over a calendar cycle.
- 📐 **[`babylonian_sqrt2.dub`](examples/babylonian_sqrt2.dub)**: Tablet YBC 7289 calculation of the diagonal of a square ($\sqrt{2} \approx 1;24,51,10$).
- ⏱️ **[`unit_conversion.dub`](examples/unit_conversion.dub)**: Explicit conversions across `second`, `minute`, `hour`, and `day`.
- ✅ **[`conformance.dub`](examples/conformance.dub)**: Section 29 formal language conformance test suite.

---

## 🧪 Comprehensive Conformance & Testing

Run the full automated test suite:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

**50 unit and integration test cases** cover:
- **Sexagesimal Literal Engine**: Digit boundary assertions ($0 \le d < 60$), regular vs. irregular rationals, cuneiform numeral translation.
- **Dimensional Safety**: Strict unit error propagation, dimensional cancellations, conversion refusals.
- **Lexical Indentation**: Indentation stack, dedents, multi-line blocks, comment handling.
- **Language Conformance (§29)**: Numbers (`1`, `60`, `1;0`, `1;30`, `365;14,31,55`), arithmetic (`1;30 + 0;30 = 2`, `2 * 0;30 = 1`, `3 / 2 = 1;30`), unit safety, repetition bounds, and exact comparison.
- **Section 26 Leap-Year Proof**: Complete verification of Earth solar year search yielding $C = 673, L = 163$.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

The DUB.SAR 1.0 language specification and its historical inspirations are documented in [`DUB_SAR_1.0_Language_Specification.md`](DUB_SAR_1.0_Language_Specification.md).