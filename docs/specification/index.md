# DUB.SAR 1.0 Specification

The normative definition of the DUB.SAR mathematical tablet language is maintained in the repository specification document.

---

## Normative Specification

The authoritative standard is defined in:

- **Repository Specification**: [`DUB_SAR_1.0_Language_Specification.md`](https://github.com/fitter22/dub.sar/blob/main/DUB_SAR_1.0_Language_Specification.md)

This specification governs all conforming implementations, interpreters, virtual machines, and ahead-of-time compiler backends.

---

## Core Specification Sections

The DUB.SAR 1.0 specification defines:

1. **Purpose and Design Philosophy**: Historical inspiration from Mesopotamian mathematics, exact rational semantics, and tablet-oriented execution.
2. **Source Modes**: Dual-layer syntax supporting cuneiform Tablet Mode, Latin transliteration Scholar Mode, and mixed notations.
3. **Lexical Grammar**: Tokens, identifiers, number literals (decimal, rational, sexagesimal), delimiters, and comments.
4. **Tablet Structure**: Section divisions including Problem Statement (`problem` / `𒂊𒁹`), Prescription Recipes (`recipe` / `𒁾𒊬`), and Inscribed Results (`result` / `𒅗𒁹`).
5. **Types and Metrology**: Dimension system, standard physical dimensions (length, area, volume, mass, time, count), and exact rational scaling factors.
6. **Execution Semantics**: Exact rational evaluation, stack operations, bounded iteration, and determination conditions.
7. **Archive Semantics**: Content addressing, immutable storage schemas, and provenance tracking.
8. **Compiler Conformance**: Requirements for reference interpreters, bytecode VMs, native C99 emission, and WebAssembly targets.

---

## Conformance Verification & Test Suite

Run the full automated test suite:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

The conformance test suite verifies normative implementation correctness across:

- **Exhaustive Numeric Conformance**: Values `0`, `1`, `2`, `59`, `60`, `1;0`, `1;30`, `1;59,59`, `365;14,31,55`, `-1;30`, round-trip normalization, and exact rational arithmetic.
- **Static Unit Type Checking**: Compile-time detection of incompatible units (`1 day + 2 year`), dimensional products, cancellations, and explicit conversions.
- **Semantic IR & Verbs**: Verification of high-level mathematical verbs (`ESTABLISH`, `TAKE`, `POSTFIX`, `REPEAT`, `RETAIN`, `DETERMINE`).
- **Mathematical Redesign Conformance**: Quantities, multiline postfix pipelines, bounded domains, determinations, field lookups, atomic selections, and implicit result inscriptions.
- **Tablet Archive & Persistent Memory**: SQLite-backed embedded house of tablets, Scribal Archive 1 seeding, version pinning, provenance tracking, working tablet mutations, atomic inscriptions, and exact rational preservation.
- **Tablet Data Model**: Sequence allocation, indexed append, associative tables, nearest-key lookup, entry removal, and iteration.
- **Geometric Mathematics & Triangles**: Exact squares, integer square roots, right-triangle determinations, Pythagorean validation, missing-side solving, and Plimpton 322 archival table lookup.
- **Inclinations, Directions & Turns**: Exact calculation of slope (rise/run) and feed (run/rise), directional ray normalization, modular turn arithmetic ($p/q \pmod 1$), directed quantities, vector additions, and quarter-turn rotations.
- **Fourier Transforms & Harmonic Reconstruction**: Exact sequence tablet processing, reference DFT ($O(N^2)$), recursive Cooley-Tukey Radix-2 FFT ($O(N \log N)$), normalized inverse transforms ($1/N$), and Parseval energy conservation.
- **Trimodal Source Equivalence**: Tablet, Scholar, and Mixed mode equivalence.
- **Independent Algorithm Validation**: Continued-fraction best rational approximations verified against bounded mathematical brute force.
- **Deterministic Leap Distribution**: Bresenham accumulator distribution.
- **AST Evaluator & VM Equivalence**: Exact rational parity between interpreter and VM.
- **Full WASM Lowering**: Determinations, procedures, loops, conditionals, and 64-bit rational runtime.

