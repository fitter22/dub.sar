# DUB.SAR 1.0

**DUB.SAR** (`𒁾𒊬`, Sumerian: *tablet writer / scribe*) is an executable Mesopotamian mathematical tablet language. It synthesizes authentic scribal mathematical traditions from the Old Babylonian period (c. 1900–1600 BCE) with modern programming language theory, exact arithmetic, dimensional unit safety, and multi-target compilation.

---

## Key Pillars

- **The Tablet Paradigm**: Programs are structured as computational tablets (`IM.GID.DA`) with clear scribal sections: a **Problem Statement** (`𒂊𒁹` / `problem`), reusable **Prescription Recipes** (`𒁾𒊬` / `recipe`), and an **Inscribed Result** (`𒅗𒁹` / `result`).
- **Three-Mode Source Model**: Write tablets in **Scholar Mode** (clean Latin-script keywords), **Tablet Mode** (authentic Unicode cuneiform signs), or **Mixed Mode** (combining cuneiform identifiers with Latin keywords). All modes share the same computational semantics, execution runtime, and compilation pipeline.
- **Historically Inspired Modern Language**: Inspired by Mesopotamian mathematics, scribal accounting, and sexagesimal computation, DUB.SAR is an executable programming system, not an ancient language reconstruction.
- **Exact Rational Arithmetic**: Fractions and sexagesimal places are preserved as exact rational numbers ($p/q$), eliminating floating-point drift. The Python reference engine provides arbitrary precision, while the native C99 runtime utilizes 64-bit rational structures with 128-bit intermediate arithmetic.
- **First-Class Metrological Dimensionality**: Quantities carry physical units enforced at parse and compile time with explicit unit conversions supported across defined metrological dimensions using standard conversion factors.
- **Persistent Tablet Archive**: Working tablets can be inscribed into SQLite-backed archives with cryptographic SHA-256 content addressing, immutable version history, and lineage tracking.
- **Multi-Target Compilation**: Run tablets on the default virtual machine (`vm`), reference AST interpreter (`ast`), or compile ahead-of-time to standalone C99 binaries, native executables, LLVM IR, shared libraries, and WebAssembly Text (`.wat`).

---

## Quickstart

### Installation

DUB.SAR requires Python 3.9 or higher and has zero external dependencies for its core interpreter and compiler.

```bash
git clone https://github.com/fitter22/dub.sar.git
cd dub.sar
pip install -e .
```

To compile to native machine binaries or shared libraries, ensure a C compiler (`clang` or `gcc`) is installed on your system.

### Your First Tablet

Create a file named `hypotenuse.dub`:

<!-- test-id: home-first-tablet-scholar -->
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

The same computation can be expressed in authentic cuneiform Tablet Mode as a compact postfix mathematical prescription:

<!-- test-id: home-first-tablet-cuneiform -->
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

### Running the Tablet

Execute on the virtual machine (default):

```bash
dubsar run hypotenuse.dub
```

Execute with the reference AST interpreter:

```bash
dubsar run hypotenuse.dub --backend=ast
```

Compile and run directly as a native executable:

```bash
dubsar run hypotenuse.dub --backend=native
```

Render an authentic SVG clay tablet illustration:

```bash
dubsar render hypotenuse.dub -o tablet.svg
```

---

## Documentation Map

- **[Learn](learn/index.md)**: A step-by-step tutorial series from basic syntax to advanced algorithms.
- **[Language Guide](guide/index.md)**: Comprehensive, topic-by-topic documentation of language mechanics.
- **[Reference](reference/index.md)**: Lexical grammar, cuneiform signs, standard units, CLI commands, and diagnostics.
- **[Examples](examples/index.md)**: Curated mathematical problems from Babylonian archaeology and modern numerical algorithms.
- **[Compiler](compiler/index.md)**: Pipeline architecture, bytecode VM, C99 codegen, LLVM IR, and WebAssembly.
- **[Concepts](concepts/index.md)**: Deeper background on Mesopotamian mathematics, exact sexagesimal numbers, and tablet archives.
- **[Specification](specification/index.md)**: The normative DUB.SAR 1.0 Language Specification.

---

## Local Documentation Workflow

To contribute to or preview this documentation site locally:

```bash
pip install mkdocs mkdocs-material
mkdocs serve
```

Visit `http://127.0.0.1:8000` to preview changes in real time. Validate all links and strict formatting prior to committing:

```bash
mkdocs build --strict
```
