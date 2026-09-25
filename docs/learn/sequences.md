# 8. Sequences & Structured Data

Scribes maintained lists and inventory tablets. DUB.SAR supports mutable working sequences and tables, enabling collections of quantities to be accumulated, transformed, and queried.

---

## Working Sequences

Create a temporary working sequence with `working name of length 0` (or in Tablet Mode `𒆥 name of length 0`):

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

In authentic cuneiform Tablet Mode, entries are retrieved using the `𒋗` (*šu*, take) or `pad 𒋫` operator:

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

---

## Indexing and Retrieving Entries

Entries in sequences are 0-indexed. Scribes retrieve specific entries using inline or multiline `take entry`:

```dubsar
problem
    working sig of length 0
    append 10 to sig
    append 20 to sig
    item : take entry 1 from sig
result
    item
```

In cuneiform Tablet Mode:

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
