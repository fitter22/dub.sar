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

## Conformance Verification

DUB.SAR includes a comprehensive conformance test suite located in `tests/`. Conforming implementations must pass all normative test cases across:

- Lexer and parser conformance for both Tablet and Scholar modes.
- Exact rational arithmetic and sexagesimal notation parsing and formatting.
- Compile-time dimensional type-checking.
- Reference interpreter and native compiler backend equivalence.
