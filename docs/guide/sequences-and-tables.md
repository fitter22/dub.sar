# The Tablet-Oriented Data Model (Sequences, Tables, and Structured Records)

DUB.SAR provides a unified, first-class mathematical data model:

> **A tablet is an inscribed mathematical data object containing identifiable entries.**

Instead of borrowing modern concepts like generic arrays, vectors, Python lists, or SQL tables, DUB.SAR grounds all data collections in the physical and mathematical reality of the clay tablet.

---

## 1. The Three Tablet Shapes

### 1. Sequence (`shape: sequence`)
- Sequential, ordered entries keyed by contiguous non-negative integers ($0, 1, 2, \dots, N-1$).
- Models numerical series, coefficients, polynomials, coordinate vectors, and observation streams.
- Declared with an optional pre-allocated length: `working signal of length 1024`.
- Supports auto-indexing append: `append 42 to signal` (or `signal 42 𒈭`).

### 2. Mathematical Table (`shape: table`)
- Associative mappings with arbitrary exact mathematical keys (integers, sexagesimal rationals, strings, or dimensioned quantities).
- Models reciprocal tables, tables of squares and square roots, astronomical ephemerides, and metrological standards.
- Entries set at specific exact keys: `put 0;30 into recips at 2` (or `recips 2 0;30 𒃻`).

### 3. Structured Tablet (`shape: structured`)
- Named fields representing compound physical or administrative entities.
- Models celestial observations, shipment bills of lading, and multi-parameter problem states.
- Initialized with inline field declarations:
  ```dubsar
  working planet:
      mass : 100
      radius : 20
  ```

---

## 2. First-Class Tablet Operations

All operations are natively available in both **Scholar Mode** (prefix phrasing) and **Canonical Cuneiform Mode** (postfix operand-verb order):

| Operation | Scholar Mode (Prefix) | Canonical Cuneiform (Postfix) | Semantics |
| :--- | :--- | :--- | :--- |
| **Creation** | `working W [of length N] [:]` | `working W [of length N] [:]` | Allocates a mutable working tablet |
| **Retrieval** | `take entry K from T` | `T K 𒋗` | Looks up entry $K$. Raises `DubSarEntryNotFoundError` if absent |
| **Insertion** | `put V into W at K` | `W K V 𒃻` | Inserts or overwrites entry $K$ in working tablet $W$ |
| **Append** | `append V to W` | `W V 𒈭` | Appends value $V$ at the next sequential integer index |
| **Length** | `length of T` | `T 𒁍` | Evaluates to the exact dimensionless integer count of entries |
| **Removal** | `remove entry K from W` | `W K remove` | Deletes entry $K$ from working tablet $W$ |
| **First Entry** | `first from T` | `T first` | Retrieves the value of the earliest entry by key sort |
| **Last Entry** | `last from T` | `T last` | Retrieves the value of the latest entry by key sort |
| **Nearest Entry** | `seek entry nearest X in T` | `T X 𒊑` | Retrieves the entry whose key is closest to $X$ |
| **Iteration** | `consider entries of T:` | `consider entries of T:` | Iterates each entry value (bound to `entry` or `v`) |
| **Keyed Iteration** | `consider K, V of T:` | `consider K, V of T:` | Iterates each key and value pair |
| **Inscription** | `inscribe tablet W [as T]` | `𒁹𒀀 W [as T]` | Persists working tablet $W$ into the archive |

---

## 3. Safety Guarantees: Immutability and Exactness

- **Strict Immutability**: Modifying, appending to, or removing entries from a persistent archive tablet raises `DubSarImmutableTabletError` (alias `ImmutableTablet`). Persistent records can only be revised by deriving a working tablet and inscribing a new version.
- **Missing Entry Protection**: Attempting to take a non-existent entry raises `DubSarEntryNotFoundError` (alias `EntryNotFound`).
- **Exact Rational Guarantee**: Sequence indices, table keys, and values are preserved as exact rationals and quantities. No decimal or floating-point distortion can occur.

---

## 4. Canonical Tablet Model Examples

The repository includes four end-to-end runnable examples demonstrating the tablet-oriented data model:

- **Reciprocal Table Lookup** (`examples/reciprocal_lookup_scholar.dub` / `examples/reciprocal_lookup.dub`): Consults standard mathematical tablet `reciprocals` and performs exact division by multiplying by the reciprocal.
- **Sequence Generation** (`examples/sequence_generation_scholar.dub` / `examples/sequence_generation.dub`): Builds a Fibonacci-style sequence, inspects `length`, and queries `first` and `last`.
- **Sequence Transformation** (`examples/sequence_transformation_scholar.dub` / `examples/sequence_transformation.dub`): Iterates entries of an observation sequence with `consider entries of ...:` and creates a scaled working sequence.
- **Persistent Tablet Sequences** (`examples/persistent_sequence_scholar.dub` / `examples/persistent_sequence.dub`): Inscribes a working sequence tablet and queries persistent versioned entries.
