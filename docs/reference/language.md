# Language Reference

This reference manual documents the syntax, operational semantics, and lexical vocabulary of the DUB.SAR programming language. It is organized by language mechanism, followed by a complete lexical and cuneiform glossary.

---

## 1. Program & Tablet Structure

In DUB.SAR, every source file models a Mesopotamian computational clay tablet (`IM.GID.DA`). A tablet is canonically organized into three sections:

```syntax
problem
    # Section 1: Known parameters, inputs, and preconditions

recipe my_procedure
    # Section 2 (optional): Auxiliary procedures and recipes

result
    # Section 3: Inscribed outputs and final conclusions
```

### Syntax

| Mode | Problem Header | Recipe Header | Result Header |
| :--- | :--- | :--- | :--- |
| **Scholar** | `problem` (or `given`) | `recipe <name>` (or `procedure <name>`) | `result` |
| **Tablet** | `𒂊𒁹` | `𒁾𒊬 <name>` | `𒅗𒁹` |

A trailing colon after `problem` or `result` is optional and ignored. Statements within a section are indented by 4 spaces.

### Semantics

- **Canonical Structure**: Scribes typically declare parameters in `problem` / `𒂊𒁹`, optional reusable algorithms in `recipe` / `𒁾𒊬`, and output bindings in `result` / `𒅗𒁹`.
- **Parser Defaults**: The parser permits minimal tablets; if `problem` or `result` is omitted, an empty default section is supplied automatically.
- **Scoping**: Variables established in `problem` are visible throughout the tablet. Variables inside a `recipe` are lexically scoped to that recipe.

### Minimal Example

<!-- test-id: ref-language-structure -->
```dubsar
problem
    side : 6 cubit
    area : side * side
result
    area
```

Output:
```text
36 length^2
```

### Related Documentation

- **Tutorial**: [Chapter 1: Your First Tablet](../learn/first-tablet.md)
- **Guide**: [Language Guide: Tablet Structure](../guide/tablet-structure.md)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

---

## 2. Problem & Result Sections

### Syntax

Scholar Mode:
```syntax
problem
    <establishments and statements>
result
    <expressions or variables to inscribe>
```

Tablet Mode:
```syntax
𒂊𒁹
    <establishments and statements>
𒅗𒁹
    <expressions or variables to inscribe>
```

### Semantics

- **`problem` / `𒂊𒁹`**: Establishes initial conditions, reads input values via `ask` / `𒀀𒁹`, mounts persistent archive tables, and executes preparatory calculations.
- **`result` / `𒅗𒁹`**: Evaluates final quantities and bakes them permanently into the tablet output stream. Expressions listed in `result` are printed in declaration order.

### Minimal Example

<!-- test-id: ref-language-sections -->
```dubsar
problem
    base : 10
    factor : 3
    total : base * factor
result
    total
```

Output:
```text
30
```

### Related Documentation

- **Tutorial**: [Chapter 1: Your First Tablet](../learn/first-tablet.md)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

---

## 3. Quantity Establishment

Quantities, dimensions, and expressions are bound to identifiers using the colon `:` operator.

### Syntax

Single-line establishment:
```syntax
<identifier> : <expression>
```

Multi-line stack prescription:
```syntax
<identifier> :
    <operand_1>
    <operand_2>
    <postfix_verb>
```

### Semantics

- **Re-establishment**: Establishing a name again with `:` replaces the previous quantity. `name := expression` updates that name the same way. Neither form is a syntax error.
- **Establishment**: The colon `:` establishes a quantity. `:=` assigns to a name that already exists or creates one.
- **Identifiers**:
  - Scholar Mode: ASCII alphanumeric identifiers and underscores (`total_area`, `side1`).
  - Tablet Mode: Valid non-reserved Unicode cuneiform sequences (`𒂼`, `𒊕`, `𒁇`). Reserved cuneiform keywords and numerals cannot be used as variable names.

### Minimal Example

<!-- test-id: ref-language-establishment -->
```dubsar
problem
    width : 5 meter
    height : 12 meter
    diagonal :
        width width multiply
        height height multiply
        add
        square-root
result
    diagonal
```

Output:
```text
13 meter
```

### Related Documentation

- **Tutorial**: [Chapter 2: Quantities & Expressions](../learn/quantities.md)
- **Guide**: [Language Guide: Quantities & Expressions](../guide/quantities-and-expressions.md)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

---

## 4. Expressions & Operators

DUB.SAR supports standard infix arithmetic expressions, relational comparisons, and logical guards.

### Syntax & Precedence

| Operator / Keyword | Cuneiform Sign | Precedence | Associativity | Description |
| :--- | :---: | :---: | :---: | :--- |
| `**`, `pow` | - | 5 | Right | Exponentiation |
| `*`, `/`, `%`, `mod`, `of` | `𒊭`, `𒉌` | 4 | Left | Multiplication, division, remainder, scaling |
| `+`, `-` | `𒍣`, `𒋫` | 3 | Left | Addition, subtraction |
| `==`, `!=`, `<`, `<=`, `>`, `>=` | `𒊓`, `𒌉`, `𒃲` | 2 | None | Relational comparisons |
| `not` | `𒉡` | 2 | Prefix | Logical negation |
| `when` ... `else` | `𒂊𒀀` ... `𒉡𒂊𒀀` | 1 | Right | Ternary conditional guard |

### Comparison Predicates

In addition to mathematical symbols, DUB.SAR supports natural English comparison predicates:
- `x is greater than y`
- `x is lesser than y`
- `x is equal to y`
- `x is not y`

### Semantics

- **Exact Rational Evaluation**: Infix arithmetic evaluates with exact rational values ($p/q$). Automatic Euclidean GCD reduction keeps fractions in canonical form.
- **Dimensional Safety**: Addition and subtraction require identical metrological dimensions. Multiplication and division form compound or quotient units.

### Minimal Example

<!-- test-id: ref-language-operators -->
```dubsar
problem
    a : 20
    b : 6
    quot : a / b
    rem : a % b
result
    quot
    rem
```

Output:
```text
3;20
2
```

### Related Documentation

- **Tutorial**: [Chapter 2: Quantities & Expressions](../learn/quantities.md)
- **Guide**: [Language Guide: Calculations](../guide/calculations.md)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

---

## 5. Postfix Calculation Verbs

DUB.SAR features stack-oriented postfix evaluation, reflecting the procedural instructions of historical clay tablets (*"take the width, square it, take the height, square it, heap them together, take the root"*).

### Syntax

Single-line pipeline:
```syntax
target : <val1> <val2> <verb> ...
```

Indented prescription block:
```syntax
target :
    <statement_1>
    <statement_2>
    <verb>
```

### Built-in Postfix Verbs

| Scholar Verb | Cuneiform Sign | Transliteration | Arity | Semantics |
| :--- | :---: | :--- | :---: | :--- |
| `add` | `𒍣` | *zi* | 2 | Pops $b, a$, pushes $a + b$ |
| `subtract` | `𒋫` | *ta* | 2 | Pops $b, a$, pushes $a - b$ |
| `multiply` | `𒊭` | *ša* | 2 | Pops $b, a$, pushes $a \times b$ |
| `divide` | `𒉌` | *ni* | 2 | Pops $b, a$, pushes $a / b$ |
| `square` | `𒅁` | *íb* | 1 | Pops $a$, pushes $a^2$ |
| `square-root` | `𒁀𒋛` | *ba-si* | 1 | Pops $a$, pushes $\sqrt{a}$ |
| `floor` | `𒄥` | *gur* | 1 | Pops $a$, pushes $\lfloor a \rfloor$ |
| `ceil` | `𒉏` | *nim* | 1 | Pops $a$, pushes $\lceil a \rceil$ |
| `nearest` | `𒊑` | *ri* | 1 | Pops $a$, pushes nearest integer $[a]$ |
| `absolute` | `𒋼` | *te* | 1 | Pops $a$, pushes $\|a\|$ |

### Minimal Example

<!-- test-id: ref-language-verbs -->
```dubsar
problem
    calc : 15 4 multiply 10 add 2 divide
result
    calc
```

Output:
```text
35
```

### Related Documentation

- **Tutorial**: [Chapter 5: Postfix Calculation Pipelines](../learn/pipelines.md)
- **Guide**: [Language Guide: Calculations](../guide/calculations.md)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

---

## 6. Mathematical Determinations

Determinations group related values into structured mathematical records, corresponding to compound measurements on cadastral tablets.

### Syntax

Record construction:
```syntax
<record_name> : <val_1>, <val_2>, <val_3>
```

Field access (dot notation or postfix phrasing):
```syntax
<record_name>.<field_name>
<field_name> of <record_name>
```

### Semantics

- **Tuple Construction**: Combines multiple named quantities into an immutable record.
- **Field Lookup**: Fields can be queried by identifier name (e.g. `record.width` or `width of record`) or by zero-based index (`record[0]`).
- **Use in Optimization**: Determinations are canonically paired with `retain` to track multiple parameters of an optimal candidate during bounded search.

### Minimal Example

<!-- test-id: ref-language-determinations -->
```dubsar
problem
    width : 15 cubit
    depth : 24 cubit
    parcel : width, depth
    area : parcel.width * parcel.depth
result
    area
```

Output:
```text
360 length^2
```

### Related Documentation

- **Tutorial**: [Chapter 7: Determinations & Selection](../learn/selection.md)
- **Guide**: [Language Guide: Determinations](../guide/determinations.md)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

---

## 7. Bounded Domains & Search Loops

DUB.SAR eliminates unconstrained while-loops in favor of strictly bounded integer domains, guaranteeing algorithmic termination.

### Syntax

Scholar Mode:
```syntax
consider <variable> from <lower_bound> through <upper_bound>:
    <body_statements>
```

Tablet Mode:
```syntax
𒄀 <variable> 𒋫 <lower_bound> 𒂗 <upper_bound>:
    <body_statements>
```

### Semantics

- **Finite Range**: Iterates over closed integer intervals $[lower, upper]$. Both bounds must evaluate to finite integer quantities.
- **Reversed or Non-Positive Bounds**: Attempting an inverted range ($lower > upper$) or invalid domain raises a `DubSarRangeError`.
- **Termination Guarantee**: Because loop ranges are strictly finite and cannot be modified inside the loop body, all DUB.SAR loops are guaranteed to terminate.

### Minimal Example

<!-- test-id: ref-language-domains -->
```dubsar
problem
    total : 0
    consider k from 1 through 100:
        total : total + k
result
    total
```

Output:
```text
5050
```

### Related Documentation

- **Tutorial**: [Chapter 6: Bounded Mathematical Search](../learn/search.md)
- **Guide**: [Language Guide: Domains & Selection](../guide/domains-and-selection.md)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

---

## 8. Atomic Selection

Within search loops, optimal values are retained across iterations using the `retain` statement and the `empty` sentinel.

### Syntax

Scholar Mode:
```syntax
retain <candidate> when <condition>
```

Tablet Mode:
```syntax
𒋼 <candidate> 𒂊𒀀 <condition>
```

### Sentinel Syntax

| Mode | Sentinel Keyword |
| :--- | :--- |
| **Scholar** | `empty` (or `none`) |
| **Tablet** | `𒉡` (or `nu`) |

### Semantics

- **Sentinel Initialization**: When an accumulator variable is initialized to `empty` (`𒉡`), the first candidate produced in the domain loop is retained unconditionally.
- **Conditional Update**: On subsequent iterations, the `when` condition is evaluated. If true, the candidate atomically replaces the current accumulator value.
- **Purity**: Retention is atomic; if the condition evaluates to false, the accumulator is unchanged.

### Minimal Example

<!-- test-id: ref-language-selection -->
```dubsar
problem
    best : empty
    consider x from 1 through 10:
        c : x * x
        retain x when c <= 50
result
    best
```

Output:
```text
7
```

### Related Documentation

- **Tutorial**: [Chapter 7: Determinations & Selection](../learn/selection.md)
- **Guide**: [Language Guide: Domains & Selection](../guide/domains-and-selection.md)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

---

## 9. Sequences and Tables

DUB.SAR provides in-memory working sequences and tables for list accumulation and tabular data processing.

### Syntax

| Operation | Scholar Mode Syntax | Tablet Mode Syntax |
| :--- | :--- | :--- |
| **Allocate** | `working <name> of length 0` | `𒆥 <name> of length 0` |
| **Append** | `append <value> to <name>` | `𒈭 <value> 𒀀 <name>` |
| **Retrieve** | `take entry <index> from <name>` | `<index> <name> 𒋗` |
| **Deposit** | `put <value> into <name> at <index>` | `𒃻 <value> 𒀀 <name> 𒀀 <index>` |
| **Length** | `length of <name>` | `<name> 𒁍` |

### Semantics

- **Indexing**: Sequences are 0-indexed.
- **Bounds Checking**: Accessing an index outside $[0, \text{length}-1]$ raises a runtime error.
- **Mutable Working State**: Working sequences exist in memory during tablet execution and can be committed to permanent storage using `inscribe`.

### Minimal Example

<!-- test-id: ref-language-sequences -->
```dubsar
problem
    working seq of length 0
    append 10 to seq
    append 20 to seq
    append 30 to seq
    count : length of seq
    mid : take entry 1 from seq
result
    count
    mid
```

Output:
```text
3
20
```

### Related Documentation

- **Tutorial**: [Chapter 8: Sequences & Structured Data](../learn/sequences.md)
- **Guide**: [Language Guide: Sequences & Tables](../guide/sequences-and-tables.md)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

---

## 10. Tablet Archive Operations

DUB.SAR embeds a persistent, immutable tablet archive backed by SQLite (`.tablets.db`).

### Syntax

| Operation | Scholar Mode | Tablet Mode |
| :--- | :--- | :--- |
| **Consult Tablet** | `consult tablet "<name>"` | `𒅆 𒁾 "<name>"` |
| **Working Scratchpad** | `working <name>` | `𒆥 <name>` |
| **Inscribe Archive** | `inscribe <source> as tablet "<target>"` | `𒁹𒀀 <source> 𒁶 𒁾 "<target>"` |
| **Read Archive Row** | `<key> take entry from <tablet>` | `<key> 𒉻 𒋫 <tablet>` |
| **Write Working Row** | `put <value> into <tablet> at <key>` | `𒃻 <value> 𒀀 <tablet> 𒀀 <key>` |

### Semantics

- **Embedded Standards**: Standard mathematical reference tables (`reciprocals`, `right-triangles`, `inclinations`, `turn-divisions`) are embedded directly in the engine and can be consulted without external setup.
- **Immutability**: Once written with `inscribe ... as tablet`, an archived tablet version is frozen clay; it cannot be modified in place.
- **Cryptographic Provenance**: Every inscribed version receives a deterministic SHA-256 fingerprint tracking schema, content, and parent lineage.

### Minimal Example

<!-- test-id: ref-language-archive -->
```dubsar
problem
    consult tablet "reciprocals"
    recip_5 :
        5
        take entry from reciprocals
result
    recip_5
```

Output:
```text
0;12
```

### Related Documentation

- **Tutorial**: [Chapter 9: The Tablet Archive](../learn/archive.md)
- **Guide**: [Language Guide: Tablet Archive](../guide/archive.md)
- **Concepts**: [Core Concepts: Archive & Provenance](../concepts/archive-and-provenance.md)

---

## 11. Units & Metrological Conversions

Quantities carry physical metrological dimensions that are statically checked at compile time.

### Syntax

Literal dimensioning:
```syntax
<number> <unit>
```

Explicit unit conversion:
```syntax
<quantity> <target_unit> apply convert
```

In cuneiform Tablet Mode:
```syntax
<quantity> <target_unit> 𒀝 convert
```

### Standard Base Dimensions

- **Length** (`length`): `cubit` (base unit), `finger` ($1/30\text{ cubit}$), `reed` ($6\text{ cubits}$), `nindan` ($12\text{ cubits}$). `meter` is a separate uncalibrated dimension and does not add to the cubit.
- **Time** (`time`): `second` (base unit), `minute` ($60\text{ s}$), `hour` ($3600\text{ s}$), `day` ($86400\text{ s}$).
- **Mass** (`mass`): `mina` (base unit), `talent` ($60\text{ minas}$).
- **Calendar Dimensions**: `month` and `year` represent independent abstract calendar and astronomical cycles; each has its own distinct base dimension and scale 1, and neither converts to days or to each other.
- **Dynamic Units**: Any unrecognized unit (e.g. `copper`, `grain`) dynamically forms an independent base dimension. `shekel` is the standard mass base.

### Semantics

- **Dimensional Homogeneity**: Quantities can only be added or subtracted if they share the exact identical dimension exponents.
- **Conversions**: Explicit conversion applies exact rational scale factors within the same dimension (e.g., converting 1 day to hours produces $24\text{ hours}$). Converting across incompatible dimensions raises a compile-time `DubSarUnitError`.

### Minimal Example

<!-- test-id: ref-language-units -->
```dubsar
problem
    duration : 1 day
    in_hours :
        duration
        hour
        apply convert
result
    in_hours
```

Output:
```text
24 hour
```

### Related Documentation

- **Tutorial**: [Chapter 4: Units & Dimensional Safety](../learn/units.md)
- **Guide**: [Language Guide: Units & Metrology](../guide/units.md)
- **Reference**: [Units Reference](units.md)

---

## 12. Numeric & Sexagesimal Notation

DUB.SAR parses and computes numbers as exact arbitrary-precision rationals ($p/q$).

### Notation Formats

1. **Decimal Integers**: Standard decimal digits (`0`, `42`, `1000`).
2. **Rational Fractions**: Exact integer fractions (`3/4`, `22/7`).
3. **Sexagesimal Fractions**: Base-60 positional notation where semicolons separate the whole integer from sexagesimal places, and commas separate successive places:
   - `0;30` $= 30/60 = 1/2$
   - `0;20` $= 20/60 = 1/3$
   - `0;15` $= 15/60 = 1/4$
   - `1;24,51,10` $\approx 1.41421296\dots$ (Babylonian approximation of $\sqrt{2}$)
4. **Cuneiform Numerals**: Additive sequences of cuneiform digits (`𒁹` = 1, `𒈫` = 2, `𒌋` = 10, `𒐏` = 40, `𒐏𒈫` = 42).

### Backend Representation Limits

- **Reference Interpreter & VM**: Uses Python arbitrary-precision integers with unbounded rational growth.
- **Native AOT Compiler (C99) & WebAssembly**: Uses fixed-width signed 64-bit integer pairs (`int64_t num, den` / `i64`) with 128-bit intermediate arithmetic. Calculations on compiled backends are bounded by 64-bit limits.

### Minimal Example

<!-- test-id: ref-language-numbers -->
```dubsar
problem
    quarter : 0;15
    factor : 4
    product : quarter * factor
result
    product
```

Output:
```text
1
```

### Related Documentation

- **Tutorial**: [Chapter 3: Exact Sexagesimal Arithmetic](../learn/exact-arithmetic.md)
- **Reference**: [Numeric Notation Reference](numbers.md)
- **Concepts**: [Core Concepts: Exact Arithmetic](../concepts/exact-arithmetic.md)

---

## 13. Source Modes: Scholar, Tablet, and Mixed

DUB.SAR programs can be authored in three interchangeable notations that share the identical computational semantics and execution runtime:

### Mode Descriptions

- **Scholar Mode**: Clean Latin-script mathematical vocabulary and readable ASCII identifiers (`width`, `height`, `problem`, `result`).
- **Tablet Mode**: Authentic Unicode cuneiform signs ($U+12000 \dots U+1254F$), non-reserved cuneiform variable names, and compact postfix prescriptions.
- **Mixed Mode**: Interleaving cuneiform section delimiters (`𒂊𒁹`, `𒅗𒁹`) or verbs (`𒍣`, `ta`) with descriptive Latin identifiers (`speed`, `measurements`).

### Automatic Transliteration

The CLI provides automated bidirectional conversion between source modes:
- `dubsar transliterate <file.dub>`: Converts cuneiform Tablet Mode into Latin Scholar Mode.
- `dubsar cuneiform <file.dub>`: Converts Latin Scholar Mode into authentic cuneiform Tablet Mode.

### Comparison Examples

Scholar Mode:
<!-- test-id: ref-language-modes-scholar -->
```dubsar
problem
    side : 4 cubit
    area : side * side
result
    area
```

Tablet Mode:
<!-- test-id: ref-language-modes-tablet -->
```dubsar
𒂊𒁹
    𒊕 : 4 cubit
    𒁇 : 𒊕 𒅁
𒅗𒁹
    𒁇
```

Mixed Mode:
<!-- test-id: ref-language-modes-mixed -->
```dubsar
𒂊𒁹
    side : 4 cubit
    𒁇 : side 𒅁
𒅗𒁹
    𒁇
```

All three modes evaluate to identical outputs:
```text
16 length^2
```

### Related Documentation

- **Tutorial**: [Chapter 1: Your First Tablet](../learn/first-tablet.md)
- **Guide**: [Language Guide: Source Modes](../guide/source-modes.md)
- **Reference**: [CLI Reference: Transliterate & Cuneiform](cli.md#5-dubsar-transliterate)

---

## 14. Lexical Vocabulary & Sign Catalog

### Section Delimiters

| Scholar Keyword | Transliteration | Tablet Sign | Codepoint | Description |
| :--- | :--- | :---: | :--- | :--- |
| `problem` / `given` | *e-diš* | `𒂊𒁹` | `U+1208A U+12079` | Problem section header |
| `recipe` / `procedure` | *dub-sar* | `𒁾𒊬` | `U+1207E U+122AC` | Auxiliary procedure definition |
| `result` | *ka-diš* | `𒅗𒁹` | `U+12157 U+12079` | Result inscription section |

### Mathematical Verbs & Operators

| Scholar Keyword | Transliteration | Tablet Sign | Codepoint | Operation |
| :--- | :--- | :---: | :--- | :--- |
| `add` / `+` | *zi* | `𒍣` | `U+12363` | Addition ($a + b$) |
| `subtract` / `-` | *ta* | `𒋫` | `U+122EB` | Subtraction ($a - b$) |
| `multiply` / `*` / `of` | *ša* | `𒊭` | `U+122AD` | Multiplication ($a \times b$) |
| `divide` / `/` | *ni* | `𒉌` | `U+1224C` | Division ($a / b$) |
| `square` | *íb* | `𒅁` | `U+12141` | Square ($a^2$) |
| `square-root` / `sqrt` | *ba-si* | `𒁀𒋛` | `U+12040 U+122DB` | Square root ($\sqrt{a}$) |
| `floor` | *gur* | `𒄥` | `U+12125` | Floor rounding ($\lfloor a \rfloor$) |
| `ceil` | *nim* | `𒉏` | `U+1224F` | Ceiling rounding ($\lceil a \rceil$) |
| `nearest` / `round` | *ri* | `𒊑` | `U+12291` | Nearest integer rounding |
| `absolute` / `abs` | *te* | `𒋼` | `U+122FC` | Absolute value ($\|a\|$) |

### Search, Selection, and Control

| Scholar Keyword | Transliteration | Tablet Sign | Codepoint | Description |
| :--- | :--- | :---: | :--- | :--- |
| `consider` / `for` | *gi* | `𒄀` | `U+12100` | Bounded iteration header |
| `from` | *ta* | `𒋫` | `U+122EB` | Domain lower bound |
| `through` / `to` | *en* | `𒂗` | `U+12097` | Canonical domain upper bound |
| `through` (alias) | *iti* | `𒌗` | `U+12317` | Astronomical upper bound alias |
| `retain` / `keep` | *te* | `𒋼` | `U+122FC` | Atomic candidate retention |
| `when` / `if` | *e-a* | `𒂊𒀀` | `U+1208A U+12000` | Conditional guard |
| `else` | *nu-e-a* | `𒉡𒂊𒀀` | `U+12261 U+1208A U+12000` | Alternative branch |
| `empty` / `none` | *nu* | `𒉡` | `U+12261` | Empty sentinel literal |
| `determine` / `return`| *nam* | `𒉆` | `U+12246` | Recipe return statement |

### Archive & Collection Vocabulary

| Scholar Keyword | Transliteration | Tablet Sign | Codepoint | Description |
| :--- | :--- | :---: | :--- | :--- |
| `consult tablet` | *igi dub* | `𒅆 𒁾` | `U+12146 U+1207E` | Mount archive reference tablet |
| `working` | *kin* | `𒆥` | `U+121A5` | Allocate working scratchpad |
| `put` | *gar* | `𒃻` | `U+120FB` | Store value at tablet key/index |
| `append` | *dah* | `𒈭` | `U+1222D` | Append entry to sequence |
| `take entry` / `pad` | *pad ... šu* | `𒉻 ... 𒋗` | `U+1227B ... U+122D7` | Retrieve entry from tablet |
| `inscribe ... as tablet` | *... gim dub* | `... 𒁶 𒁾` | `... U+12076 U+1207E` | Finalize immutable tablet |
| `into` / `to` | *a* | `𒀀` | `U+12000` | Target preposition |
| `length` | *gíd* / *uš* | `𒁍` / `𒍑` | `U+1204D` / `U+12351` | Sequence entry count |

### Punctuation & I/O

| Symbol | Cuneiform Sign | Codepoint | Description |
| :--- | :---: | :--- | :--- |
| `:` | `:` | - | Quantity establishment delimiter |
| `,` | `,` | - | Determination record element separator |
| `.` | `.` | - | Determination field access operator |
| `#` | `𒑰` | `U+12470` | Comment marker (Old Assyrian word divider) |
| `ask` / `input` | `𒀀𒁹` | `U+12000 U+12079` | Interactive external input request |
| `inscribe` / `output`| `𒁹𒀀` | `U+12079 U+12000` | Inscribe value to output stream |
