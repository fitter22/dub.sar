# Source Modes

DUB.SAR features a three-mode source model designed to unite authentic visual scribal culture with practical programming and learning ergonomics:

- **Scholar Mode**: The readable, practical mode for learning, authoring, and everyday programming.
- **Tablet Mode**: The genuine cuneiform program notation and visual representation of the language.
- **Mixed Mode**: The seamless bridge between Scholar and Tablet notations.

All three source modes compile into the exact same Abstract Syntax Tree (AST), execute identically across both the reference AST interpreter and bytecode VM, and preserve equivalent semantics.

---

## The Three-Mode Model

### 1. Scholar Mode (Readable Authoring)

Scholar Mode is designed for human authoring, teaching, and clean code review. It uses readable Latin keywords (`problem`, `recipe`, `result`, `consider`, `retain`, `when`), descriptive variable identifiers (`solar-year`, `candidate-year`), and standard algebraic notation:

```dubsar
problem

    solar-year :
        ask "solar year in days"

    limit :
        1000

result

    solar-year
```

Scholar Mode is the primary recommended form for learning the language and developing new algorithms.

### 2. Tablet Mode (Genuine Cuneiform Notation)

Tablet Mode represents program structure, keywords, operators, and identifiers using authentic Unicode cuneiform signs (`U+12000` through `U+1254F`). In canonical Tablet Mode, programs contain zero Latin identifiers outside of string data and comments:

```dubsar
𒂊𒁹

    𒈬 :
        𒀀𒁹 "solar year in days"

    𒍠 :
        1000

𒅗𒁹

    𒈬
```

In this representation:
- Program keywords are cuneiform wedges (`𒂊𒁹` for `problem`, `𒀀𒁹` for `ask`, `𒅗𒁹` for `result`).
- Variables and procedure names are represented by single or compound cuneiform signs (`𒈬` for year, `𒍠` for limit).

Tablet Mode is the distinctive cultural and visual notation of DUB.SAR, used for canonical clay tablet inscriptions, terminal artwork, and ceremonial programs.

### 3. Mixed Mode (The Interoperability Bridge)

DUB.SAR does not enforce an all-or-nothing dichotomy. Mixed Mode is a first-class language capability:
- A Scholar Mode file may freely use cuneiform numerals (`𒁹`, `𒈫`, `𒌋`), mathematical signs (`𒁀𒋛`), or unit signs (`𒌓`, `𒌗`, `𒈬`).
- A Tablet Mode program may use Latin identifiers or custom formulas during prototyping.
- The lexer, parser, and semantic analyzer natively accept both sets of tokens interchangeably.

---

## The Unicode String Literal Exception

A foundational principle of DUB.SAR is that **strings are data, not program syntax**.

DUB.SAR deliberately does not attempt to transcribe or encode arbitrary modern Unicode strings into cuneiform phonetic approximations. Strings represent user prompts, dataset keys, exported labels, or runtime inputs. 

Consequently, Tablet Mode allows normal Unicode string literals, including modern languages, numbers, and cuneiform text:

```dubsar
    𒀀𒁹 "solar year in days"
    𒁹𒀀 "Babylonian sqrt(2) approximation:"
    𒁹𒀀 "𒀭𒂗𒆠"
    𒁹𒀀 "こんにちは"
```

During source normalization and transliteration (`dubsar transliterate` and `dubsar cuneiform`):
- Program syntax, keywords, operators, and identifiers are converted according to the target mode.
- String literals preserve their exact Unicode byte contents with 100% round-trip fidelity.

---

## Cuneiform Identifier Conventions

In Tablet Mode, identifiers are constructed from Unicode cuneiform signs:

1. **Sign Run Scanning**: An unbroken run of cuneiform signs (`U+12000` to `U+1254F`), excluding word divider signs (`𒑰` and `𒑱`), is scanned as a discrete cuneiform word.
2. **Keyword Recognition**: If the word matches a reserved language keyword (`𒂊𒁹`, `𒁾𒊬`, `𒅗𒁹`, `𒂊𒀀`, `𒉡𒂊𒀀`, `𒁀𒋛`, etc.), it is treated as a language token.
3. **Pure Numerals**: If the word consists entirely of cuneiform numeral signs, it is evaluated as a numeric literal.
4. **Identifiers**: Any other cuneiform sign or compound word is recognized as a valid identifier.

### Symbolic Sign Conventions

Where historically attested lexical terminology is unavailable, DUB.SAR treats cuneiform signs as symbolic program identifiers:

| Symbolic Sign | Codepoint | Transliteration | Symbolic Role in Examples |
| :--- | :--- | :--- | :--- |
| `𒈬` | `U+1222C` | MU | Year / solar cycle / primary parameter |
| `𒍠` | `U+12361` | ZAG | Boundary / limit |
| `𒌓` | `U+12313` | UD | Whole days / base unit |
| `𒁇` | `U+12047` | BAR | Remainder / fraction / diagonal measure |
| `𒊕` | `U+122A0` | SAG | Head / best candidate / prime record |
| `𒁄` | `U+12044` | BAL | Cycle / iteration turn |
| `𒋛` | `U+122DB` | SI | Leap / surplus count / extent |
| `𒈬𒁶` | `U+1222C U+12111` | MU.GIM | Candidate year ("like-year") |
| `𒇲` | `U+121B7` | LAL | Deficit / error difference |
| `𒊮` | `U+122AE` | SHA3 | Candidate record tuple |
| `𒅎` | `U+1214E` | IM | Count / step / tablet reference |
| `𒃷` | `U+120F7` | GAN | Calculated approximation |
| `𒅆𒁀` | `U+12146 U+12040` | IGI.BA | Root recipe ("root examination") |
| `𒈠` | `U+12222` | MA | Start argument |
| `𒋰` | `U+122EB` | TAB | Double / pair / iterations |
| `𒄿` | `U+1213E` | I | Current iteration state |
| `𒈦` | `U+12226` | MASZ | Half-factor / reciprocal value |
| `𒈠𒁶` | `U+12222 U+12111` | MA.GIM | Next iteration state |
| `𒈬𒁹` .. `𒈬𒐉` | `U+1222C ...` | MU.1 .. MU.4 | Indexed sequence values |
| `𒋛𒈬` | `U+122DB U+1222C` | SI.MU | Leap distribution calculation |

---

## Canonical Sign Mapping Table

| Concept | Scholar Mode | Tablet Mode (Cuneiform) | Scribal Pronunciation |
| :--- | :--- | :--- | :--- |
| Problem Section | `problem` | `𒂊𒁹` | `e-diš` |
| Recipe (Procedure) | `recipe` / `procedure` | `𒁾𒊬` | `dub-sar` |
| Result Section | `result` | `𒅗𒁹` | `ka-diš` |
| Addition | `add` / `+` | `𒍣` | `zi` |
| Subtraction | `subtract` / `-` | `𒋫` | `ta` |
| Multiplication | `multiply` / `*` | `𒊭` | `ša` |
| Division | `divide` / `/` | `𒉌` | `ni` |
| Square | `square` | `𒅁` | `íb` |
| Square Root | `square-root` / `sqrt` | `𒁀𒋛` | `ba-si` |
| Loop / Domain | `consider ... through` | `𒄀 ... 𒂗` | `gi ... en` |
| Conditional When | `when` / `if` | `𒂊𒀀` | `e-a` |
| Conditional Else | `else` | `𒉡𒂊𒀀` | `nu-e-a` |
| Retain Candidate | `retain` | `𒋼` | `te` |
| Comparison (Lesser) | `is lesser than` / `<` | `𒌉` | `tur` |
| Comparison (Greater) | `is greater than` / `>` | `𒃲` | `gal` |
| Equality | `is equal` / `==` | `𒊓` | `sa` |
| Inscribe (Output) | `output` / `inscribe` | `𒁹𒀀` | `diš-a` |
| Ask (Input) | `ask` / `input` | `𒀀𒁹` | `a-diš` |
| Consult Tablet | `consult tablet` | `𒅆 𒁾` | `igi dub` |
| Working Tablet | `working` | `𒆥` | `kin` |
| Put Entry | `put ... into` | `𒃻 ... 𒀀` | `gar ... a` |
| Take Entry | `take ... from` | `... 𒋗` | `... šu` |

---

## Transliteration and Normalization CLI

The DUB.SAR toolchain provides bidirectional normalization between modes:

### Converting Tablet to Scholar Mode
```bash
dubsar transliterate examples/planetary_leap.dub
```

### Converting Scholar to Tablet Mode
```bash
dubsar cuneiform examples/planetary_leap_scholar.dub
```

Both tools preserve indentation, whitespace, comment semantics, and exact string literal contents.
