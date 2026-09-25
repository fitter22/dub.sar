# DUB.SAR 1.0

**DUB.SAR** (`𒁾𒊬`, Sumerian: *tablet writer / scribe*) is an executable Mesopotamian mathematical tablet language. It synthesizes authentic scribal mathematical traditions from the Old Babylonian period (c. 1900–1600 BCE) with modern programming language theory, exact arithmetic, dimensional unit safety, and multi-target compilation.

---

## Key Pillars

- **The Tablet Paradigm**: Programs are structured as computational tablets (`IM.GID.DA`) with clear scribal sections: a **Problem Statement** (`𒂊𒁹` / `problem`), reusable **Prescription Recipes** (`𒁾𒊬` / `recipe`), and an **Inscribed Result** (`𒅗𒁹` / `result`).
- **Authentic Dual-Layer Syntax**: Write tablets using Unicode cuneiform signs (Tablet Mode) or transliterated Latin keywords (Scholar Mode). Both forms parse into the identical abstract syntax tree.
- **Exact Rational Arithmetic**: Fractions and sexagesimal places are preserved exactly as arbitrary-precision rational values ($p/q$), preventing floating-point rounding errors.
- **First-Class Metrological Dimensionality**: Quantities carry physical units (length, area, volume, mass, time) enforced at parse and compile time with automatic unit conversions.
- **Persistent Tablet Archive**: Working tablets can be inscribed into SQLite-backed archives with cryptographic SHA-256 content addressing, immutable version history, and lineage tracking.
- **Multi-Target Compilation**: Run tablets through the reference AST interpreter, execute stack bytecode on the register VM, or compile ahead-of-time to standalone C99 binaries, native executables, LLVM IR, shared libraries, and WebAssembly (`.wasm`).

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

```dubsar
problem:
    width : 3 meter
    length : 4 meter
    w_sq := width width multiply
    l_sq := length length multiply
    hyp_sq := w_sq l_sq add
    hyp := hyp_sq square-root
result:
    hyp
```

Or write the identical tablet using authentic cuneiform signs:

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

Execute with the reference interpreter:

```bash
dubsar run hypotenuse.dub
```

Execute on the register virtual machine:

```bash
dubsar run hypotenuse.dub --backend=vm
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
