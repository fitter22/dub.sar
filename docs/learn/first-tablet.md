# 1. Your First Tablet

This chapter introduces the fundamental concepts of DUB.SAR, guides you through installing the toolchain, and walks through your first executable computational tablet.

---

## What is a Computational Tablet?

In Mesopotamia, mathematical tablets (`IM.GID.DA`) were not passive notebooks; they were structured instruments of calculation. Scribes recorded known parameters, executed procedural algorithms (*epēšu*, "to do / calculate"), and inscribed permanent conclusions.

DUB.SAR translates this physical paradigm directly into code. In canonical scribal practice, a complete tablet is organized into three sections:

1. **Problem Statement** (`problem` / `𒂊𒁹`): Establishes known physical parameters, initial quantities, and boundary conditions.
2. **Computational Prescriptions** (`recipe` / `𒁾𒊬`, optional): Reusable procedures and auxiliary recipes.
3. **Inscribed Result** (`result` / `𒅗𒁹`): The verified mathematical outputs baked permanently into clay.

While the DUB.SAR parser permits minimal or single-section tablets (providing empty defaults if either problem or result is omitted), complete computational tablets canonically begin with `problem` / `𒂊𒁹` and conclude with `result` / `𒅗𒁹`. Neither section header takes a trailing colon.

Unlike conventional imperative languages, DUB.SAR tablets have no unbounded loops, no null pointers, and no floating-point rounding errors. At the language level, execution is deterministic, dimensional, and exact (with arbitrary precision in the reference interpreter/VM and 64-bit rational bounds in native/WASM compilation).

---

## Installation and Setup

Before writing your first tablet, install the DUB.SAR toolchain:

### Prerequisites

- **Python 3.9+** (the core compiler and virtual machine have zero external dependencies).
- A C compiler (`clang` or `gcc`) for compiling ahead-of-time (AOT) to native machine binaries.

### Installing from Source

```bash
git clone https://github.com/fitter22/dub.sar.git
cd dub.sar
pip install -e .
```

Verify that the CLI is installed and accessible on your path:

```bash
dubsar --version
```

---

## Scholar Mode and Tablet Mode

DUB.SAR programs can be written in three interoperable source modes:

- **Scholar Mode**: Clean Latin-script keywords, ASCII identifiers, and readable intermediate bindings.
- **Tablet Mode**: Authentic Unicode cuneiform signs, cuneiform identifiers, and compact postfix prescriptions.
- **Mixed Mode**: A hybrid allowing cuneiform identifiers alongside Latin keywords or vice versa.

All modes share the exact same computational semantics, execution runtime, and compilation pipeline.

To see how DUB.SAR operates, consider computing the hypotenuse of a right triangle with base $3\text{ meter}$ and altitude $4\text{ meter}$ using the Pythagorean relation ($\sqrt{3^2 + 4^2} = 5\text{ meter}$):

### Scholar Mode

In Scholar Mode, the computation makes each intermediate quantity explicit with named bindings:

<!-- test-id: learn-first-tablet-scholar -->
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

### Tablet Mode (Cuneiform)

In authentic cuneiform Tablet Mode (using cuneiform identifiers and the standard length unit `meter`), the same computation is expressed as a compact postfix mathematical prescription:

<!-- test-id: learn-first-tablet-cuneiform -->
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

Both programs execute the same calculation and produce the exact dimensional output:

```text
5 length
```

---

## Semantic Equivalence vs. Structural Differences

The Scholar and Tablet implementations above illustrate an important design distinction in DUB.SAR:

- **Scholar Mode** is optimized for conventional programming readability. It breaks multi-step operations into explicit, named intermediate assignments (`w_sq`, `h_sq`, `hyp_sq`, `hyp`), allowing easy inspection and debugging.
- **Tablet Mode** expresses the calculation as a unified postfix mathematical prescription (`𒁇 : ...`), reflecting the terse, worked-calculation style of historical scribal clay tablets.

These two styles are **semantically equivalent**, but they are **not structurally identical**:

1. **Different AST Structures**: The Scholar version declares four separate intermediate assignments (`Assignment` AST nodes), whereas the Tablet version defines a single prescription block (`Prescription` AST node) containing a sequence of stack operations.
2. **Semantic Invariant**: Despite the structural difference, both forms encode identical mathematical semantics and respect identical dimensional rules ($3\text{ m} \times 3\text{ m} \to 9\text{ m}^2$, $4\text{ m} \times 4\text{ m} \to 16\text{ m}^2$, $9\text{ m}^2 + 16\text{ m}^2 \to 25\text{ m}^2$, $\sqrt{25\text{ m}^2} \to 5\text{ m}$).
3. **Execution Guarantee**: Rather than requiring statement-by-statement bytecode equality, DUB.SAR guarantees semantic invariance: equivalent inputs evaluate to identical computational outputs across the virtual machine, reference interpreter, and native compiler backends.

---

## How the Postfix Tablet Pipeline Executes

In Tablet Mode, the indented block introduced by the colon `:` after `𒁇` is a **postfix prescription**. Operations within this block evaluate over an internal operand stack:

```dubsar
    𒁇 :
        𒂼 𒅁
        𒊕 𒅁
        𒍣
        𒁀𒋛
```

The stack transitions proceed step-by-step:

1. **`𒂼 𒅁` (Square Width)**: The value of variable `𒂼` ($3\text{ meter}$) is pushed onto the stack. The postfix verb `𒅁` (*íb*, square) squares it in place.
   - *Stack:* `[9 meter^2]`
2. **`𒊕 𒅁` (Square Height)**: The value of variable `𒊕` ($4\text{ meter}$) is pushed onto the stack. The postfix verb `𒅁` squares it in place.
   - *Stack:* `[9 meter^2, 16 meter^2]`
3. **`𒍣` (Sum of Squares)**: The binary verb `𒍣` (*zi*, raise / heap / add) pops the top two values, computes their dimensional sum ($9\text{ meter}^2 + 16\text{ meter}^2$), and pushes the result.
   - *Stack:* `[25 meter^2]`
4. **`𒁀𒋛` (Equal Proportion / Root)**: The unary verb `𒁀𒋛` (*ba-si*, square root) pops the sum, computes the root, and pushes the resulting quantity.
   - *Stack:* `[5 meter]`
5. **Assignment**: Upon exiting the prescription block, the final value remaining on the stack ($5\text{ meter}$) is bound to the target identifier `𒁇`.

---

## Identifier Semantics: Language Vocabulary vs. User Variables

When inspecting the Tablet Mode example, it is essential to distinguish between **fixed language vocabulary** and **user-defined variable identifiers**:

| Symbol in Example | Role | Nature | Specification Status |
| :--- | :--- | :--- | :--- |
| `𒂊𒁹` (*e-diš*) | Problem section header | Language Keyword | Fixed grammar delimiter (`problem`) |
| `𒅗𒁹` (*ka-diš*) | Result section header | Language Keyword | Fixed grammar delimiter (`result`) |
| `𒍣` (*zi*) | Addition operator | Mathematical Verb | Fixed built-in verb (`add` / `+`) |
| `𒅁` (*íb*) | Square operator | Mathematical Verb | Fixed built-in verb (`square`) |
| `𒁀𒋛` (*ba-si*) | Square-root operator | Mathematical Verb | Fixed built-in verb (`square-root` / `sqrt`) |
| `meter` | Physical unit | Metrological Unit | Standard length unit |
| `𒂼` (*dagal*) | Horizontal leg variable | **User Identifier** | Arbitrary variable chosen by programmer |
| `𒊕` (*sag*) | Vertical leg variable | **User Identifier** | Arbitrary variable chosen by programmer |
| `𒁇` (*bar*) | Hypotenuse variable | **User Identifier** | Arbitrary variable chosen by programmer |

### Why Were `𒂼`, `𒊕`, and `𒁇` Chosen?

In Mesopotamian field surveys and geometric problem tablets (such as BM 13901 and Plimpton 322), scribes routinely used specific technical terms:
- `𒂼` (*dagal*): "width" or "breadth" (contrasted with length, *uš*).
- `𒊕` (*sag*): "front", "head", or "short/vertical side" of a triangle or field.
- `𒁇` (*bar*): "outside", "remainder", or the unknown target quantity.

In DUB.SAR, these signs are used in the example as an authentic, historically grounded naming convention.

### Crucial Distinction for Scribes

The language specification **does not** bind `𒂼` as a keyword meaning "width", nor is `𒊕` a keyword meaning "height". They are standard user identifiers, exactly like `width`, `height`, `x`, or `y` in Scholar Mode.

When writing your own tablets:
- You can use cuneiform sequences accepted by the lexer that are not reserved keywords or cuneiform numerals as variable names (for example `𒀀` [*a*], `𒁉` [*bi*], `𒌨` [*ur*]).
- You can also use ASCII identifiers (`width`, `height`) inside Tablet Mode or Mixed Mode.
- Reserved cuneiform signs cannot be used as variable identifiers:
  - **Section Delimiters**: `𒂊𒁹` (*problem*), `𒅗𒁹` (*result*), `𒁾𒊬` (*recipe*).
  - **Mathematical Verbs**: `𒍣` (*add*), `ta` / `𒋫` (*subtract*), `ša` / `𒊭` (*multiply*), `ni` / `𒉌` (*divide*), `𒅁` (*square*), `𒁀𒋛` (*square-root*), `𒄥` (*floor*), `𒉏` (*ceil*), `𒊑` (*nearest*).
  - **Search & Selection**: `𒄀` (*consider*), `𒂗` (*through*), `𒋼` (*retain*), `nu` / `𒉡` (*empty*).
  - **Tablet Archive**: `𒅆` (*consult*), `𒆥` (*working*), `𒁹𒀀` (*inscribe*), `𒈭` (*append*), `𒉻` / `𒋗` (*take*), `𒃻` (*put*).
  - **Cuneiform Numerals**: sequences composed purely of cuneiform digits (such as `𒁹` [1], `𒈫` [2], `𒐈` [3]) are lexed as numeric literals.

---

## How to Write Your Own Tablet Mode Program

To create a new tablet from scratch:

1. **Open the Problem Section**: Begin the tablet with `𒂊𒁹` on its own line (no trailing colon).
2. **Establish Known Quantities**: Indent lines by 4 spaces and declare known values using the colon `:` operator:
   ```dubsar
   𒊕 : 12 cubit
   ```
3. **Prescribe Calculations**: Compute unknown values using either single-line expressions (`:`) or multi-line postfix prescription blocks (`:`):
   ```dubsar
   𒁇 : 𒊕 * 2
   ```
4. **Close with the Result Section**: Add `𒅗𒁹` on its own line and list the variables to inscribe as outputs:
   ```dubsar
   𒅗𒁹
       𒁇
   ```

---

## Running the Tablet

Save the code above to `hypotenuse.dub` and execute it with the `dubsar` CLI:

Execute on the virtual machine (default backend):
```bash
dubsar run hypotenuse.dub
```

Execute with the reference AST interpreter:
```bash
dubsar run hypotenuse.dub --backend=ast
```

Compile and run directly as an AOT-compiled native binary:
```bash
dubsar run hypotenuse.dub --backend=native
```

Render an authentic clay tablet illustration as an SVG image:
```bash
dubsar render hypotenuse.dub -o hypotenuse.svg
```

---

## Further Reading & Reference

- **[Language Guide: Tablet Structure](../guide/tablet-structure.md)**: Tripartite structure, problem setup, and result inscription.
- **[Language Guide: Source Modes](../guide/source-modes.md)**: Deep dive into Scholar, Tablet, and Mixed modes.
- **[Core Concepts: The Tablet Paradigm](../concepts/tablet-paradigm.md)**: The physical and mathematical model of clay tablets.
- **[Reference: Core Vocabulary](../reference/language.md)**: Full normative keywords and symbols.
- **[Reference: Cuneiform Signs](../reference/cuneiform.md)**: Complete sign catalog with Unicode code points and pronunciations.
