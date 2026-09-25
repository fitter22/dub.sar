# 1. Your First Tablet

In DUB.SAR, every program models an ancient clay tablet (`IM.GID.DA`). A tablet is structured into distinct scribal sections representing the problem setup, procedure algorithms, and the final inscribed result.

DUB.SAR programs can be written in three interoperable source modes:
- **Scholar Mode**: Clean Latin-script keywords and alphanumeric identifiers.
- **Tablet Mode**: Authentic Unicode cuneiform ideograms and syllabograms.
- **Mixed Mode**: A hybrid allowing cuneiform identifiers alongside Latin keywords or vice versa.

DUB.SAR is historically inspired by Old Babylonian and Seleucid scribal practices, but designed as an executable, statically verifiable programming language.

---

## Symmetrical Implementations: Scholar & Tablet Modes

Every tablet begins with a **Problem Statement** section (`problem` / `𒂊𒁹`) and concludes with a **Result** section (`result` / `𒅗𒁹`).

Notice that neither section header takes a trailing colon.

### Scholar Mode

```dubsar
problem
    x : 40
    y : 2
    sum := x + y
result
    sum
```

Alternatively, written using postfix scribal verb evaluation:

```dubsar
problem
    x : 40
    y : 2
    sum :
        x
        y
        add
result
    sum
```

### Tablet Mode (Cuneiform)

Here is the structurally identical tablet inscribed in genuine Unicode cuneiform:

```dubsar
𒂊𒁹
    𒊕 : 40
    𒅎 : 2
    𒁇 := 𒊕 𒍣 𒅎
𒅗𒁹
    𒁇
```

Or using authentic postfix cuneiform verb invocation:

```dubsar
𒂊𒁹
    𒊕 : 40
    𒅎 : 2
    𒁇 :
        𒊕
        𒅎
        𒍣
𒅗𒁹
    𒁇
```

Both forms compile to identical intermediate representations and bytecode, producing the exact result `42`.

---

## Sections Explained

- `problem` (`𒂊𒁹` / `e-diš`): Declares known input quantities, bindings, and initial conditions.
- `result` (`𒅗𒁹` / `ka-diš`): Specifies the values inscribed onto the tablet as final outputs.
- `recipe` / `procedure` (`𒁾𒊬` / `dub-sar`): Defines reusable subroutines and mathematical algorithms.

Bindings declared with `:` establish initial values or structured blocks. Expressions assigned with `:=` compute intermediate quantities.
