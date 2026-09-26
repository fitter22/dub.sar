# 8. Sequences & Structured Data

Scribes maintained lists and inventory tablets. DUB.SAR supports mutable working sequences and tables, enabling collections of quantities to be accumulated, transformed, and queried.

---

## Working Sequences

Create a temporary working sequence with `working name of length 0` (or in Tablet Mode `𒆥 name of length 0`):

<!-- test-id: learn-sequences-working-scholar -->
```dubsar
problem
    working measurements of length 0
    append 12 to measurements
    append 18 to measurements
    append 25 to measurements

    total_count : length of measurements
    val0 :
        0
        take entry from measurements
    val1 :
        1
        take entry from measurements
result
    total_count
    val0
    val1
```

Output:
```text
3
12
18
```

### Mixed Mode (Cuneiform Verbs with Latin Identifiers)

In Mixed Mode, scribes can employ authentic cuneiform operational verbs (`𒈭` for append, `𒋗` for take) alongside descriptive Latin variable identifiers (`measurements`, `total_count`):

<!-- test-id: learn-sequences-working-mixed -->
```dubsar
𒂊𒁹
    𒆥 measurements of length 0
    𒈭 12 𒀀 measurements
    𒈭 18 𒀀 measurements
    𒈭 25 𒀀 measurements

    total_count : length of measurements
    val0 :
        0
        measurements 𒋗
    val1 :
        1
        measurements 𒋗
𒅗𒁹
    total_count
    val0
    val1
```

Output:
```text
3
12
18
```

---

## Indexing and Retrieving Entries

Entries in sequences are 0-indexed. Scribes retrieve specific entries using inline or multiline `take entry`:

<!-- test-id: learn-sequences-indexing-scholar -->
```dubsar
problem
    working sig of length 0
    append 10 to sig
    append 20 to sig
    item : take entry 1 from sig
result
    item
```

Output:
```text
20
```

### Mixed Mode

In Mixed Mode, indexing uses the postfix `𒋗` (*šu*, take) verb:

<!-- test-id: learn-sequences-indexing-mixed -->
```dubsar
𒂊𒁹
    𒆥 sig of length 0
    𒈭 10 𒀀 sig
    𒈭 20 𒀀 sig
    item :
        1
        sig 𒋗
𒅗𒁹
    item
```

Output:
```text
20
```

---

## Further Reading & Reference

- **[Language Guide: Sequences & Tables](../guide/sequences-and-tables.md)**: Full coverage of the 3 tablet shapes (sequence, table, structured) and first-class tablet operations.
- **[Language Reference: Core Vocabulary](../reference/language.md)**: Keywords `working`, `append`, `take`, `length of`, and `put`.
- **[Examples Catalog: Tablet Data Model](../examples/index.md#tablet-data-model-sequences)**: Runnable examples of sequence generation and transformation.
