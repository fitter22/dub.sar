# Guided Examples Catalog

Welcome to the DUB.SAR Examples Catalog. This catalog organizes 21 curated computational tablets (42 source files) into a guided pedagogical progression from initial language fundamentals through advanced archival systems and astronomical algorithms.

Every example is provided in two paired implementations:

- **Scholar Mode** (`examples/<name>_scholar.dub`): Formatted with clean Latin-script keywords, descriptive variable bindings, and modern identifier conventions for readability.
- **Tablet / Mixed Mode** (`examples/<name>.dub`): Written with authentic cuneiform syntax, postfix prescriptions, and mathematical verbs. Fully authentic **Tablet Mode** (`babylonian_sqrt2.dub`, `even_distribution.dub`, `planetary_leap.dub`, `reciprocal_lookup.dub`) pairs cuneiform keywords with authentic cuneiform identifiers, while **Mixed Mode** pairs cuneiform keywords and verbs with readable Latin identifiers, allowing learners to focus on operators and pipelines.

All examples are fully executable and verified for exact semantic parity across both the reference AST interpreter and the stack-based virtual machine via automated test coverage in `tests/test_examples.py`.

---

## Pedagogical Progression

The catalog follows a five-level pedagogical progression designed to take scribes from basic syntax to full mastery:

```mermaid
flowchart LR
    L1["Level 1: Beginner<br>Language Fundamentals"] --> L2["Level 2: Intermediate<br>Control Flow & Pipelines"]
    L2 --> L3["Level 3: Advanced<br>Sequences & Geometry"]
    L3 --> L4["Level 4: Mastery<br>Archives & Advanced Math"]
    L4 --> L5["Level 5: Exemplars<br>Historical Tablets & Systems"]
```

1. **Level 1: Beginner — Fundamentals**: Clay tablet structure, base-60 sexagesimal notation, dimensional types, and metrological unit conversions.
2. **Level 2: Intermediate — Control Flow & Pipelines**: Stack-oriented postfix pipelines, mathematical verbs, finite bounded iteration, atomic selection, and structured determination tuples.
3. **Level 3: Advanced — Data Structures & Geometry**: Dynamic sequence tablets, iterative series transformations, right-triangle geometry, inclination slopes, and directed turn vectors.
4. **Level 4: Mastery — Archives & Advanced Math**: Embedded reciprocal reference tables, multi-tablet archival persistence, immutable sequences, and discrete Fourier spectral analysis.
5. **Level 5: Exemplars — Historical Tablets & Systems**: Authentic archaeological calculations (YBC 7289, Plimpton 322, UET V 72), astronomical calendar intercalation, versioned audit tablets, and core conformance smoke tests.

---

## Master Catalog Table

| Level | Example Name | Primary Concept | Scholar Tablet | Tablet / Mixed Tablet | Mode | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Beginner** | [First Tablet](#first-tablet-dimensions) | Problem/Result, Dimensions | [`first_tablet_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/first_tablet_scholar.dub) | [`first_tablet.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/first_tablet.dub) | Mixed | `1200 length^2` |
| **1. Beginner** | [Exact Arithmetic](#exact-sexagesimal-arithmetic) | Sexagesimal Radix Arithmetic | [`arithmetic_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/arithmetic_scholar.dub) | [`arithmetic.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/arithmetic.dub) | Mixed | `0;50`, `0;45`, `0;10`, `3` |
| **1. Beginner** | [Unit Conversions](#unit-conversions-dimensional-safety) | Metrology & Unit Safety | [`unit_conversion_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/unit_conversion_scholar.dub) | [`unit_conversion.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/unit_conversion.dub) | Mixed | `2 hour`, `1;30 day`, `2160 minute` |
| **2. Intermediate** | [Postfix Pipelines](#postfix-pipelines-mathematical-verbs) | Verbs (`zi`, `ba-si`, `gur`, `nim`, `ri`) | [`postfix_pipelines_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/postfix_pipelines_scholar.dub) | [`postfix_pipelines.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/postfix_pipelines.dub) | Mixed | `49`, `24;30`, `24`, `25`, `25` |
| **2. Intermediate** | [Bounded Search](#bounded-mathematical-search) | Domains (`consider ... through`) | [`bounded_search_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/bounded_search_scholar.dub) | [`bounded_search.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/bounded_search.dub) | Mixed | `55` |
| **2. Intermediate** | [Atomic Selection](#atomic-selection-sentinel-retention) | `retain ... when`, Sentinel `empty` | [`atomic_selection_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/atomic_selection_scholar.dub) | [`atomic_selection.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/atomic_selection.dub) | Mixed | `Largest integer whose square <= 50:`, `7` |
| **2. Intermediate** | [Determinations](#determinations-structured-records) | Tuples, Field Extractions | [`determinations_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/determinations_scholar.dub) | [`determinations.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/determinations.dub) | Mixed | `360 length^2`, `15 kus`, `24 kus` |
| **3. Advanced** | [Sequence Generation](#sequence-generation) | Dynamic Sequences, First/Last | [`sequence_generation_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/sequence_generation_scholar.dub) | [`sequence_generation.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/sequence_generation.dub) | Mixed | `6`, `1`, `8` |
| **3. Advanced** | [Sequence Transformation](#sequence-transformation) | Series Mapping & Bounded Iteration | [`sequence_transformation_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/sequence_transformation_scholar.dub) | [`sequence_transformation.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/sequence_transformation.dub) | Mixed | `120`, `4`, `96` |
| **3. Advanced** | [Right Triangles](#right-triangles-plimpton-322) | Pythagorean Triples, Slopes | [`geometry_triangle_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/geometry_triangle_scholar.dub) | [`geometry_triangle.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/geometry_triangle.dub) | Mixed | `1`, `13`, `2;24`, `0;25`, `30`, `1` |
| **3. Advanced** | [Geometric Inclinations](#geometric-inclinations-feeds-turns) | Slopes, Feeds, Directed Turns | [`geometric_inclination_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/geometric_inclination_scholar.dub) | [`geometric_inclination.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/geometric_inclination.dub) | Mixed | `0;20`, `3`, `direction(...)` |
| **4. Mastery** | [Reciprocal Lookup](#reciprocal-table-lookup) | Reference Tablet Division | [`reciprocal_lookup_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/reciprocal_lookup_scholar.dub) | [`reciprocal_lookup.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/reciprocal_lookup.dub) | Tablet | `0;7,30`, `3;45` |
| **4. Mastery** | [Tablet Archive Persistence](#tablet-archive-persistence-lineage) | Multi-tablet Storage, Working Copy | [`tablet_archive_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/tablet_archive_scholar.dub) | [`tablet_archive.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/tablet_archive.dub) | Mixed | `0;15` |
| **4. Mastery** | [Persistent Sequences](#persistent-inscribed-sequences) | Inscribing Structured Sequences | [`persistent_sequence_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/persistent_sequence_scholar.dub) | [`persistent_sequence.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/persistent_sequence.dub) | Mixed | `5`, `1`, `16` |
| **4. Mastery** | [Fourier Transforms](#discrete-fourier-transform-dft-fft) | DFT/FFT Spectral Analysis | [`fourier_dft_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/fourier_dft_scholar.dub) | [`fourier_dft.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/fourier_dft.dub) | Mixed | `2`, `4`, `4`, `1`, `1`, `1` |
| **5. Exemplar** | [Babylonian Sqrt(2)](#babylonian-square-root-of-2-ybc-7289) | YBC 7289 Diagonal Approximation | [`babylonian_sqrt2_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/babylonian_sqrt2_scholar.dub) | [`babylonian_sqrt2.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/babylonian_sqrt2.dub) | Tablet | `1 + 195025/470832`, `42 + 33461/78472` |
| **5. Exemplar** | [Planetary Leap Cycles](#planetary-leap-year-cycle-search) | Astronomical Period Search | [`planetary_leap_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/planetary_leap_scholar.dub) | [`planetary_leap.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/planetary_leap.dub) | Tablet | `673`, `163 day`, `1/29073600 day` |
| **5. Exemplar** | [Even Intercalation](#even-distribution-of-leap-years) | Bresenham Leap Year Distribution | [`even_distribution_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/even_distribution_scholar.dub) | [`even_distribution.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/even_distribution.dub) | Tablet | `0`, `0`, `0`, `1` |
| **5. Exemplar** | [Ea-Nasir Dispute v1](#ea-nasir-copper-trade-dispute-uet-v-72) | UET V 72 Audit & Archive | [`ea_nasir_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/ea_nasir_scholar.dub) | [`ea_nasir.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/ea_nasir.dub) | Mixed | `Ea-nasir`, `10 talent`, `0;15` |
| **5. Exemplar** | [Ea-Nasir Revision v2](#ea-nasir-assessment-revision-v1-v2) | Working Derivation & Versioning | [`ea_nasir_revision_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/ea_nasir_revision_scholar.dub) | [`ea_nasir_revision.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/ea_nasir_revision.dub) | Mixed | `ea-nasir-assessment` |
| **5. Exemplar** | [Core Conformance](#core-conformance-smoke-test) | Core Language Smoke Test | [`conformance_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/conformance_scholar.dub) | [`conformance.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/conformance.dub) | Mixed | Multi-part mathematical verification |

---

## Level 1: Beginner — Language Fundamentals

Beginner examples introduce core DUB.SAR primitives: the two-part tablet structure (`problem` / `result`), exact sexagesimal numbers, and dimensional physical quantities.

### First Tablet: Dimensions

- **Files**: [`examples/first_tablet_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/first_tablet_scholar.dub) / [`examples/first_tablet.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/first_tablet.dub)
- **Concept**: Tablet structure, dimensional establishments, and unit exponent multiplication.
- **Tutorial Guide**: [Chapter 1: Your First Tablet](../learn/first-tablet.md)

Demonstrates calculating the area of a rectangular field from width and length measurements, enforcing that multiplying two quantities of dimension `length` produces `length^2`.

```bash
# Execute in Scholar Mode
python3 -m dubsar run examples/first_tablet_scholar.dub

# Execute in Cuneiform Tablet Mode
python3 -m dubsar run examples/first_tablet.dub
```

**Expected Output**:
```text
1200 length^2
```

---

### Exact Sexagesimal Arithmetic

- **Files**: [`examples/arithmetic_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/arithmetic_scholar.dub) / [`examples/arithmetic.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/arithmetic.dub)
- **Concept**: Exact sexagesimal positional notation, rational evaluation, and basic operations.
- **Tutorial Guide**: [Chapter 3: Exact Sexagesimal Arithmetic](../learn/exact-arithmetic.md)

Validates exact base-60 sexagesimal arithmetic without floating-point rounding errors:
- Sum: $0;30 + 0;20 = 0;50$ ($1/2 + 1/3 = 5/6$)
- Difference: $1 - 0;15 = 0;45$ ($1 - 1/4 = 3/4$)
- Product: $0;30 \times 0;20 = 0;10$ ($1/2 \times 1/3 = 1/6$)
- Division: $1 / 0;20 = 3$ ($1 / (1/3) = 3$)

```bash
python3 -m dubsar run examples/arithmetic_scholar.dub
```

**Expected Output**:
```text
Sum (0;30 + 0;20):
0;50
Difference (1 - 0;15):
0;45
Product (0;30 * 0;20):
0;10
Division (1 / 0;20):
3
```

---

### Unit Conversions & Dimensional Safety

- **Files**: [`examples/unit_conversion_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/unit_conversion_scholar.dub) / [`examples/unit_conversion.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/unit_conversion.dub)
- **Concept**: Physical units, conversion ratios, and dimensional checking.
- **Tutorial Guide**: [Chapter 4: Units & Dimensional Safety](../learn/units.md)

Demonstrates converting between time units (`second` $\to$ `hour`, `hour` $\to$ `day`, `day` $\to$ `minute`) and adding quantities with compatible dimensions. Adding incompatible dimensions (e.g. `meter` and `second`) causes a static compile-time error.

```bash
python3 -m dubsar run examples/unit_conversion_scholar.dub
```

**Expected Output**:
```text
7200 seconds converted to hours (expected 2 hour):
2 hour
36 hours converted to days (expected 1;30 day):
1;30 day
1;30 day converted to minutes (expected 2160 minute):
2160 minute
36 hour + 12 hour:
48 hour
```

---

## Level 2: Intermediate — Control Flow, Pipelines & Records

Intermediate examples showcase stack-oriented evaluation, finite iteration, condition-based filtering, and structured tuples.

### Postfix Pipelines & Mathematical Verbs

- **Files**: [`examples/postfix_pipelines_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/postfix_pipelines_scholar.dub) / [`examples/postfix_pipelines.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/postfix_pipelines.dub)
- **Concept**: Stack-oriented evaluation and mathematical verbs (`zi`, `ba-si`, `gur`, `nim`, `ri`).
- **Tutorial Guide**: [Chapter 5: Postfix Calculation Pipelines](../learn/pipelines.md)

Illustrates how DUB.SAR evaluates multi-step postfix expressions using historical scribal verbs:
- `square` (`íb`): Squares the operand ($7^2 = 49$)
- `half` (`ba-si`): Halves the operand ($49 / 2 = 24;30$)
- `floor` (`gur`): Truncates toward zero ($24;30 \to 24$)
- `ceiling` (`nim`): Rounds upward ($24;30 \to 25$)
- `nearest` (`ri`): Rounds to nearest integer ($24;30 \to 25$)

```bash
python3 -m dubsar run examples/postfix_pipelines_scholar.dub
```

**Expected Output**:
```text
Square of 7:
49
Half of 49:
24;30
Floor of 24;30:
24
Ceiling of 24;30:
25
Nearest to 24;30:
25
```

---

### Bounded Mathematical Search

- **Files**: [`examples/bounded_search_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/bounded_search_scholar.dub) / [`examples/bounded_search.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/bounded_search.dub)
- **Concept**: Bounded domains (`consider ... from ... through ...`), accumulator variables, and termination guarantees.
- **Tutorial Guide**: [Chapter 6: Bounded Mathematical Search](../learn/search.md)

Demonstrates guaranteed termination: DUB.SAR prohibits unbounded `while` loops. All iteration is strictly bounded over finite numeric domains. In this example, the integers 1 through 10 are accumulated to yield 55.

```bash
python3 -m dubsar run examples/bounded_search_scholar.dub
```

**Expected Output**:
```text
Sum of 1 through 10:
55
```

---

### Atomic Selection & Sentinel Retention

- **Files**: [`examples/atomic_selection_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/atomic_selection_scholar.dub) / [`examples/atomic_selection.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/atomic_selection.dub)
- **Concept**: Atomic `retain` with criteria (`when`), sentinel `empty` (`nu`), and bound filtering.
- **Tutorial Guide**: [Chapter 7: Determinations & Selection](../learn/selection.md)

Finds the largest integer $n \in [1, 10]$ whose square does not exceed $50$, updating the retained candidate only when the condition is satisfied:

```bash
python3 -m dubsar run examples/atomic_selection_scholar.dub
```

**Expected Output**:
```text
Largest integer whose square <= 50:
7
```

---

### Determinations & Structured Records

- **Files**: [`examples/determinations_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/determinations_scholar.dub) / [`examples/determinations.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/determinations.dub)
- **Concept**: Compound tuples (`determine`), named field projections, and record metrology.
- **Tutorial Guide**: [Chapter 7: Determinations & Selection](../learn/selection.md)

Constructs an agricultural parcel record with named fields (`width`, `depth`, `area`), extracts properties via `take entry from`, and verifies rectangular dimensional consistency:

```bash
python3 -m dubsar run examples/determinations_scholar.dub
```

**Expected Output**:
```text
Parcel area:
360 length^2
Parcel width:
15 kus
Parcel depth:
24 kus
```

---

## Level 3: Advanced — Data Structures & Geometry

Advanced examples introduce mutable scratchpad sequences, iterative observation processing, and Mesopotamian surveying mathematics.

### Sequence Generation

- **Files**: [`examples/sequence_generation_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/sequence_generation_scholar.dub) / [`examples/sequence_generation.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/sequence_generation.dub)
- **Concept**: Working sequence tablets, sequential accumulation (`append`), and boundary inspection (`first of`, `last of`, `length of`).
- **Tutorial Guide**: [Chapter 8: Sequences & Structured Data](../learn/sequences.md)

Allocates a working sequence tablet in memory, computes a 6-term Fibonacci sequence ($1, 1, 2, 3, 5, 8$), and inspects the length, initial element, and final element.

```bash
python3 -m dubsar run examples/sequence_generation_scholar.dub
```

**Expected Output**:
```text
6
1
8
```

---

### Sequence Transformation

- **Files**: [`examples/sequence_transformation_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/sequence_transformation_scholar.dub) / [`examples/sequence_transformation.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/sequence_transformation.dub)
- **Concept**: Iterating over observations, map/reduce transformations, and sequence statistics.
- **Tutorial Guide**: [Chapter 8: Sequences & Structured Data](../learn/sequences.md)

Loads an observation series of disbursements (12, 24, 36, 48), iterates through entries using bounded loops to compute the cumulative total (120), transforms each entry by doubling, and inspects the resulting transformed sequence length (4) and final entry (96).

```bash
python3 -m dubsar run examples/sequence_transformation_scholar.dub
```

**Expected Output**:
```text
120
4
96
```

---

### Right Triangles & Plimpton 322

- **Files**: [`examples/geometry_triangle_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/geometry_triangle_scholar.dub) / [`examples/geometry_triangle.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/geometry_triangle.dub)
- **Concept**: Pythagorean triples, diagonal relations, slope ratios, and exact triangle area.
- **Tutorial Guide**: [Concepts: Geometric & Fourier](../concepts/geometric-and-fourier.md)

Solves a right triangle with base $5$ and height $12$, verifying the hypotenuse ($13$), computing the inclination slope ($12/5 = 2;24$), reciprocal feed ($5/12 = 0;25$), and enclosed area ($30$).

```bash
python3 -m dubsar run examples/geometry_triangle_scholar.dub
```

**Expected Output**:
```text
1
13
2;24
0;25
30
1
```

---

### Geometric Inclinations, Feeds & Turns

- **Files**: [`examples/geometric_inclination_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/geometric_inclination_scholar.dub) / [`examples/geometric_inclination.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/geometric_inclination.dub)
- **Concept**: Canal ramp slope ($rise/run$), feed ($run/rise$), directed vectors, and angular turn fractions.
- **Tutorial Guide**: [Concepts: Geometric & Fourier](../concepts/geometric-and-fourier.md)

Calculates earthwork ramp profiles for canal embankments and manipulates directed spatial quantities along quarter-turn angles:

```bash
python3 -m dubsar run examples/geometric_inclination_scholar.dub
```

**Expected Output**:
```text
0;20
3
0;30
2
direction(quarter-turn)
direction(0;22,30-turn)
10 meter along direction(quarter-turn)
```

---

## Level 4: Mastery — Archives & Advanced Mathematics

Mastery examples demonstrate standard mathematical reference tables, immutable archive operations, persistent sequence storage, and harmonic spectral analysis.

### Reciprocal Table Lookup

- **Files**: [`examples/reciprocal_lookup_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/reciprocal_lookup_scholar.dub) / [`examples/reciprocal_lookup.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/reciprocal_lookup.dub)
- **Concept**: Standard reference tables (`reciprocals`), table consultation, and division by reciprocal multiplication.
- **Tutorial Guide**: [Chapter 9: The Tablet Archive](../learn/archive.md)

In Mesopotamian mathematics, division is achieved by consulting a standard reciprocal table and multiplying by the reciprocal ($igi$). This example looks up the reciprocal of $8$ ($0;7,30$) and multiplies it by $30$ to compute $30 / 8 = 3;45$.

```bash
python3 -m dubsar run examples/reciprocal_lookup_scholar.dub
```

**Expected Output**:
```text
0;7,30
3;45
```

---

### Tablet Archive Persistence & Lineage

- **Files**: [`examples/tablet_archive_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/tablet_archive_scholar.dub) / [`examples/tablet_archive.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/tablet_archive.dub)
- **Concept**: Persistent archives, scratchpad allocation (`as working`), in-place mutation, and SHA-256 provenance.
- **Tutorial Guide**: [Chapter 9: The Tablet Archive](../learn/archive.md)

Demonstrates the lifecycle of archival data: consulting an immutable tablet, deriving a mutable working copy, updating fields, and writing the result.

```bash
python3 -m dubsar run examples/tablet_archive_scholar.dub
```

**Expected Output**:
```text
0;15
```

---

### Persistent Inscribed Sequences

- **Files**: [`examples/persistent_sequence_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/persistent_sequence_scholar.dub) / [`examples/persistent_sequence.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/persistent_sequence.dub)
- **Concept**: Inscribing dynamic sequence tablets into the immutable archive.
- **Tutorial Guide**: [Chapter 9: The Tablet Archive](../learn/archive.md)

Constructs a geometric sequence of powers of 2 ($1, 2, 4, 8, 16$), commits the complete sequence tablet to the archive under name `powers`, consults the archived tablet, and queries sequence length ($5$), initial element ($1$), and final element ($16$).

```bash
python3 -m dubsar run examples/persistent_sequence_scholar.dub
```

**Expected Output**:
```text
5
1
16
```

---

### Discrete Fourier Transform (DFT / FFT)

- **Files**: [`examples/fourier_dft_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/fourier_dft_scholar.dub) / [`examples/fourier_dft.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/fourier_dft.dub)
- **Concept**: Spectral analysis on directed sequences, reference $O(N^2)$ DFT, and Cooley-Tukey Radix-2 FFT ($O(N \log N)$).
- **Tutorial Guide**: [Concepts: Geometric & Fourier](../concepts/geometric-and-fourier.md)

Transforms a 4-point discrete impulse sequence $[1, 0, 0, 0]$ into the frequency domain, verifies harmonic bin magnitudes, Parseval energy conservation, and inverts back to the original time domain with exact rational arithmetic:

```bash
python3 -m dubsar run examples/fourier_dft_scholar.dub
```

**Expected Output**:
```text
2
4
4
1
1
1
```

---

## Level 5: Exemplars — Historical Tablets & Systems

Exemplar programs integrate all language capabilities to solve real-world problems from archaeological tablets, astronomical calendars, and commercial audits.

### Babylonian Square Root of 2 (YBC 7289)

- **Files**: [`examples/babylonian_sqrt2_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/babylonian_sqrt2_scholar.dub) / [`examples/babylonian_sqrt2.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/babylonian_sqrt2.dub)
- **Concept**: Tablet YBC 7289 reciprocal iteration, diagonal scaling, and arbitrary rational precision.
- **Archaeological Source**: Yale Babylonian Collection tablet YBC 7289 (c. 1800–1600 BCE).

Calculates the sexagesimal approximation inscribed on tablet YBC 7289 ($1;24,51,10 \approx 1.41421296$), and evaluates the diagonal of a square with side $30$:

```bash
python3 -m dubsar run examples/babylonian_sqrt2_scholar.dub
```

**Expected Output**:
```text
Babylonian sqrt(2) approximation:
1 + 195025/470832
Square with side 30 has diagonal:
42 + 33461/78472
```

---

### Planetary Leap-Year Cycle Search

- **Files**: [`examples/planetary_leap_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/planetary_leap_scholar.dub) / [`examples/planetary_leap.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/planetary_leap.dub)
- **Concept**: Interactive input (`ask`), bounded astronomical search, and calendar cycle optimization.
- **Tutorial Guide**: [Chapter 10: Complete Example](../learn/complete-example.md)

Takes a precise astronomical solar year measurement ($365;14,31,55\text{ days}$) and evaluates candidate intercalation cycles (up to 1000 years) to find the period that minimizes cumulative calendar drift:

```bash
# Provide solar year measurement via stdin:
echo "365;14,31,55" | python3 -m dubsar run examples/planetary_leap_scholar.dub
```

**Expected Output**:
```text
673
163 day
1/29073600 day
```

---

### Even Distribution of Leap Years

- **Files**: [`examples/even_distribution_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/even_distribution_scholar.dub) / [`examples/even_distribution.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/even_distribution.dub)
- **Concept**: Bresenham accumulator arithmetic and uniform intercalation distribution.

Distributes leap days uniformly across a multi-year calendar cycle using exact integer accumulator arithmetic without floating-point error:

```bash
python3 -m dubsar run examples/even_distribution_scholar.dub
```

**Expected Output**:
```text
year 1 extra day:
0
year 2 extra day:
0
year 3 extra day:
0
year 4 extra day:
1
```

---

### Ea-Nasir Copper Trade Dispute (UET V 72)

- **Files**: [`examples/ea_nasir_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/ea_nasir_scholar.dub) / [`examples/ea_nasir.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/ea_nasir.dub)
- **Concept**: Archival assessment, merchant purity audits, and version 1 inscription.
- **Archaeological Source**: British Museum tablet UET V 72 (Ur, c. 1750 BCE).

Formalizes the historic dispute between customer Nanni and merchant Ea-nasir: extracts promised vs. delivered quantities, computes the purity deficit ($1 - 0;45 = 0;15$), and inscribes the official assessment tablet into the archive.

```bash
python3 -m dubsar run examples/ea_nasir_scholar.dub
```

**Expected Output**:
```text
Ea-nāṣir
10 talent
10 talent
1
0;45
0;15
```

---

### Ea-Nasir Assessment Revision (v1 -> v2)

- **Files**: [`examples/ea_nasir_revision_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/ea_nasir_revision_scholar.dub) / [`examples/ea_nasir_revision.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/ea_nasir_revision.dub)
- **Concept**: Deriving working drafts from existing tablets, updating fields, and versioned re-inscription.

Loads the existing `ea-nasir-assessment` tablet, creates a working draft, records a final `rejected` verdict, and inscribes version 2:

```bash
# Run examples/ea_nasir_scholar.dub first. It inscribes ea-nasir-assessment v1.
python3 -m dubsar run examples/ea_nasir_revision_scholar.dub
```

**Expected Output**:
```text
ea-nasir-assessment
```

---

### Core Conformance Smoke Test

- **Files**: [`examples/conformance_scholar.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/conformance_scholar.dub) / [`examples/conformance.dub`](https://github.com/fitter22/dub.sar/blob/main/examples/conformance.dub)
- **Concept**: Core language smoke test exercising numbers, arithmetic, unit safety, and bounded loops.

A smoke-test example exercising a representative subset of core language features:
- Number formats: integers, base-60 fractions, astronomical constants
- Arithmetic: addition, subtraction, multiplication, division
- Dimensional safety: unit arithmetic consistency
- Exact equality: rational equivalence checks
- Finite domains: bounded loop accumulation

The emitted values are verified for exactness and Interpreter/VM parity in `tests/test_examples.py`.

```bash
python3 -m dubsar run examples/conformance_scholar.dub
```

**Expected Output**:
```text
sum 1;30 + 0;30 (expected 2):
2
mul 2 * 0;30 (expected 1):
1
div 3 / 2 (expected 1;30):
1;30
unit sum 1 day + 2 day (expected 3 day):
3 day
exactness checks:
1
1
bounded repetition 1..5 sum (expected 15):
15
```

---

## Running the Automated Test Suite

All 42 example tablets are tested continuously by the project test suite. You can verify that every example compiles, runs cleanly, and matches its expected output on both the Interpreter and VM:

```bash
# Run example suite
python3 -m unittest tests/test_examples.py

# Run documentation snippet suite
python3 -m unittest tests/test_docs_examples.py

# Run entire repository test suite
python3 -m unittest discover -s tests -p "test_*.py"
```

For more in-depth exploration:
- Start learning with the [Tutorial Series](../learn/index.md).
- Consult the [Language Reference](../reference/language.md) for formal syntax rules.
- Review [Cuneiform Signs](../reference/cuneiform.md) for authentic paleographic glyphs.
