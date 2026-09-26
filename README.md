# 𒁾𒊬 — DUB.SAR 1.0
### The Executable Mesopotamian Mathematical Tablet Language

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-fitter22.github.io%2Fdub.sar-orange.svg)](https://fitter22.github.io/dub.sar/)
[![Conformance Tests](https://img.shields.io/badge/Test%20Suite-Passing-success.svg)](tests/)
[![Targets: C99 / VM / WAT](https://img.shields.io/badge/Targets-C99%20%7C%20VM%20%7C%20WAT-purple.svg)](https://fitter22.github.io/dub.sar/compiler/)

> **What if ancient Babylonian scribes had designed a modern programming language?**

**DUB.SAR** (Sumerian: *dub-sar*, "tablet writer" or "scribe") is an executable mathematical tablet language. It synthesizes authentic scribal traditions from Old Babylonian mathematics (c. 1900–1600 BCE) with modern programming language theory, exact arithmetic, dimensional unit safety, and multi-target compilation.

Instead of dimensionless bit-vectors, non-terminating loops, and lossy IEEE floating-point approximations, DUB.SAR treats computation as physical clay tablet inscriptions: exact sexagesimal rational arithmetic, compile-time metrological unit safety, bounded mathematical search, and persistent archival provenance.

---

## The Tablet Paradigm

In DUB.SAR, every program is a computational clay tablet (`IM.GID.DA`) organized into three scribal sections:

- **Problem Statement** (`problem` / `𒂊𒁹`): Given quantities, metrological dimensions, and initial assumptions.
- **Computational Prescriptions** (`recipe` / `𒁾𒊬`): Constructive mathematical algorithms and reusable formulas.
- **Inscribed Result** (`result` / `𒅗𒁹`): The verified mathematical conclusions baked permanently into clay.

### Trimodal Source Model

Tablets can be authored in three interchangeable notations:
- **Scholar Mode**: Clean Latin-script mathematical vocabulary for modern readability.
- **Tablet Mode**: Authentic Unicode cuneiform signs ($U+12000 \dots U+1254F$).
- **Mixed Mode**: Interleaving cuneiform identifiers with Latin keywords.

All modes share the same computational semantics, execution runtime, and compilation pipeline, with automated translation via `dubsar transliterate` and `dubsar cuneiform`.

---

## First Tablet: The 3-4-5 Right Triangle

Here is a side-by-side comparison calculating the hypotenuse of a right triangle with width 3 meters and height 4 meters:

#### Scholar Mode (`hypotenuse_scholar.dub`)
```dubsar
problem
    width : 3 meter
    height : 4 meter
    w_sq : width width multiply
    h_sq : height height multiply
    hyp_sq : w_sq h_sq add
    hyp : hyp_sq square-root
result
    hyp
```

#### Tablet Mode (`hypotenuse.dub`)
```dubsar
𒂊𒁹
    𒂼 : 3 meter
    𒊕 : 4 meter
    𒁇 :
        𒂼 𒅁
        𒊕 𒅁
        𒍣
        𒁀𒋛
𒅗𒁹
    𒁇
```

Both produce the exact dimensioned output:
```text
5 length
```

---

## Quickstart

### Prerequisites

- **Python 3.9+** (zero external dependencies for core compiler and VM).
- A C compiler (`clang` or `gcc`) for compiling to native machine binaries.

### Installation

```bash
git clone https://github.com/fitter22/dub.sar.git
cd dub.sar
pip install -e .
```

### Running Tablets

Execute on the default Stack Virtual Machine:
```bash
dubsar run examples/geometry_triangle_scholar.dub
```

Execute with the reference AST interpreter:
```bash
dubsar run examples/geometry_triangle_scholar.dub --backend=ast
```

Compile and run directly as a native machine executable:
```bash
dubsar run examples/geometry_triangle_scholar.dub --backend=native
```

Render an authentic clay tablet vector illustration:
```bash
dubsar render examples/geometry_triangle.dub --style=tablet -o triangle.svg
```

---

## Key Pillars

- **Exact Sexagesimal Rational Arithmetic**: Numbers are preserved as exact rationals ($p/q$), eliminating floating-point drift. Native sexagesimal notation (`0;30 = 1/2`, `1;24,51,10 \approx \sqrt{2}`) reflects authentic Old Babylonian base-60 mathematics.
- **Algebraic Dimensional Metrology**: Quantities carry physical units (such as length, mass, and time) checked statically at compile time. Incompatible operations (such as adding meters to seconds) are caught before execution, with explicit conversions supported across defined metrological dimensions.
- **Bounded Determinism**: Eliminates unbounded loops (`while`) in favor of bounded mathematical domains and atomic selections, guaranteeing program termination.
- **Persistent Tablet Archive (*é-dub-ba-a*)**: SQLite-backed embedded house of tablets featuring SHA-256 cryptographic content addressing, immutable version lineages, and 13 standard scholarly reference tablets.
- **Geometric & Fourier Mathematics**: 8-layer progression extending scribal ratios, right triangles, and canal inclinations into Discrete and Radix-2 Fast Fourier Transforms without complex numbers.
- **Clay Tablet Vector Art**: Built-in rendering engine producing SVG clay tablet artwork with wedge impressions, case rulings, drop shadows, and clay gradients.

---

## Implementation Status

| Component | Status | Description |
| :--- | :--- | :--- |
| **Native C99 / LLVM AOT** | Complete | Ahead-of-time compilation to standalone binaries, LLVM IR, and shared libraries |
| **Stack Bytecode VM** | Complete | Stack IR, constant table, activation frames, and determination operations |
| **Reference AST Interpreter** | Complete | Full language support with arbitrary-precision exact rationals |
| **WebAssembly Backend (WAT)** | Complete | Textual WebAssembly (`.wat`) code generator with 64-bit rational runtime, assembleable to `.wasm` via standard tools |
| **Trimodal Unicode Parser** | Complete | Lexer and recursive-descent parser for Tablet, Scholar, and Mixed modes |
| **Persistent Archive Engine** | Complete | SQLite-backed *é-dub-ba-a* with immutable monotonic versioning and SHA-256 provenance |
| **Clay Tablet SVG Renderer** | Complete | Vector artwork generator producing textured clay tablet illustrations |
| **Conformance Test Suite** | Complete | Exhaustive unit, integration, and mathematical conformance test suite |

---

## Documentation

Full documentation, tutorials, and language references are available at the documentation site:
**[https://fitter22.github.io/dub.sar/](https://fitter22.github.io/dub.sar/)**

- **[Learn Tutorial](https://fitter22.github.io/dub.sar/learn/)**: Step-by-step tutorial series from your first tablet to advanced algorithms.
- **[Language Guide](https://fitter22.github.io/dub.sar/guide/)**: Comprehensive guide covering tablet structure, source modes, units, calculations, and the archive.
- **[Concepts](https://fitter22.github.io/dub.sar/concepts/)**: Deep dives into the tablet paradigm, exact arithmetic, dimensional metrology, and Fourier mathematics.
- **[Language Reference](https://fitter22.github.io/dub.sar/reference/)**: Core vocabulary, cuneiform signs, units of measurement, CLI commands, and error diagnostics.
- **[Compiler Architecture](https://fitter22.github.io/dub.sar/compiler/)**: Compilation pipeline, native C99 emission, bytecode VM, and WebAssembly lowering.
- **[Examples Catalog](https://fitter22.github.io/dub.sar/examples/)**: Runnable tablets from Babylonian archaeology and modern numerical algorithms.
- **[Normative Specification](https://fitter22.github.io/dub.sar/specification/)**: The authoritative DUB.SAR 1.0 Language Specification.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

The normative language specification is documented in [`DUB_SAR_1.0_Language_Specification.md`](DUB_SAR_1.0_Language_Specification.md).
