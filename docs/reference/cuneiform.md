# Cuneiform Signs Reference

DUB.SAR uses Unicode cuneiform signs from the Unicode standard blocks:
- **Cuneiform**: `U+12000` to `U+123FF`
- **Cuneiform Numbers and Punctuation**: `U+12400` to `U+1247F`
- **Early Dynastic Cuneiform**: `U+12480` to `U+1254F`

### Historical Inspiration vs Ancient Language Reconstruction

DUB.SAR is an executable programming language designed for modern computational safety and verified sexagesimal mathematics. It draws symbolic, conceptual, and grammatical inspiration from Old Babylonian and Seleucid mathematical tablets, scribal administrative systems, and sexagesimal place-value arithmetic. It is **not** an ancient language reconstruction or natural language translation engine. Instead, authentic cuneiform ideograms and syllabograms are mapped to strict deterministic grammar rules, formal typing constraints, and runtime operations.

---

## 1. Historically Attested Mathematical and Scribal Vocabulary

These signs possess authentic historical attestation in Mesopotamian mathematical tablets (such as Plimpton 322, BM 13901, and YBC 4652) and administrative archives:

| Cuneiform Sign | Codepoint | Transliteration | Historical / Scribal Meaning | Scholar Equivalent |
| :---: | :--- | :--- | :--- | :--- |
| `𒂊𒁹` | `U+1208A U+12079` | e-diš | Single problem header formula | `problem` / `given` |
| `𒁾𒊬` | `U+1207E U+122AC` | dub-sar | Tablet writer / scribe (recipe definition) | `recipe` / `procedure` |
| `𒅗𒁹` | `U+12157 U+12079` | ka-diš | Stated result header formula | `result` |
| `𒍣` | `U+12363` | zi | To raise / heap (addition) | `add` / `+` |
| `𒋫` | `U+122EB` | ta | Out of / from (subtraction, range origin) | `subtract` / `-` / `from` / `than` |
| `𒊭` | `U+122AD` | ša | Of (multiplication, genitive relationship) | `multiply` / `*` / `of` |
| `𒉌` | `U+1224C` | ni | By / per (division) | `divide` / `/` |
| `𒅁` | `U+12141` | íb | Equal side / flank (square) | `square` |
| `𒁀𒋛` | `U+12040 U+122DB` | ba-si | Equal proportion (square root) | `square-root` / `sqrt` |
| `𒅆` | `U+12146` | igi | Reciprocal / eye (examine / consult) | `consult` |
| `𒁾` | `U+1207E` | dub | Inscribed clay tablet entity | `tablet` |
| `𒃻` | `U+120FB` | gar | To place / deposit an entry | `put` |
| `𒈭` | `U+1222D` | dah | To add onto / append | `append` |
| `𒉻` | `U+1227B` | pad | To break off a portion / retrieve entry | `take entry` / `pad` |
| `𒈦` | `U+12226` | maš | Half constant ($1/2 = 0;30$) | `half` / `0;30` |
| `𒌓` | `U+12313` | ud | Day unit ($1\text{ ud} = 24\text{ hr}$) | `day` / `ud` |
| `𒌗` | `U+12317` | iti | Month unit ($1\text{ iti} = 30\text{ ud}$) | `month` / `iti` |
| `𒈬` | `U+1222C` | mu | Year unit ($1\text{ mu} = 360\text{ ud}$) | `year` / `mu` |
| `𒄘` | `U+12118` | gun | Talent weight unit ($1\text{ gun} = 60\text{ ma-na}$) | `talent` / `gun` |
| `𒈠𒈾` | `U+12220 U+1223E` | ma-na | Mina weight unit ($1\text{ ma-na} = 60\text{ gin}$) | `mina` / `ma-na` |
| `𒄀` | `U+12100` | gi | Reed measure ($1\text{ gi} = 6\text{ cubits}$) / repetition | `gi` / `reed` / `consider` |

---

## 2. Reconstructed and Interpretive Scribal Operators

To build a complete, deterministic, and expressive computational grammar, DUB.SAR interprets related Sumerian and Akkadian lexical roots into modern programming constructs:

| Cuneiform Sign | Codepoint | Transliteration | Scribal Operational Role | Scholar Equivalent |
| :---: | :--- | :--- | :--- | :--- |
| `𒂊𒀀` | `U+1208A U+12000` | e-a | Conditional guard clause | `when` / `if` |
| `𒉡𒂊𒀀` | `U+12261 U+1208A U+12000` | nu-e-a | Alternative conditional branch | `else` |
| `𒂗` | `U+12097` | en | Canonical range upper boundary (*adi*) | `through` / `to` / `en` |
| `𒌗` | `U+12317` | iti | Calendar alias for range upper boundary | `through` / `iti` |
| `𒋼` | `U+122FC` | te | Retain candidate in search (*ṭehû*) / absolute | `retain` / `absolute` |
| `𒉆` | `U+12246` | nam | Recipe determination return statement | `determine` / `return` |
| `𒉇` | `U+12247` | nam2 | Recipe return statement (orthographic variant) | `determine` / `return` |
| `𒄑` | `U+12111` | ĝeš | Procedure return statement | `return` |
| `𒁹𒀀` | `U+12079 U+12000` | diš-a | Output / inscribe to tablet stream | `output` / `inscribe` |
| `𒀀𒁹` | `U+12000 U+12079` | a-diš | Interactive input request | `ask` / `input` |
| `𒋗` | `U+122D7` | šu | Retrieval target marker (*pad ... šu*) | `take` / `šu` |
| `𒄥` | `U+12125` | gur | Floor rounding (truncate downward) | `floor` |
| `𒉏` | `U+1224F` | nim | Ceiling rounding (truncate upward) | `ceil` |
| `𒊑` | `U+12291` | ri | Nearest integer rounding | `nearest` / `round` |
| `𒌉` | `U+12309` | tur | Less than comparison ($<$) | `lesser` / `<` |
| `𒃲` | `U+120F2` | gal | Greater than comparison ($>$) | `greater` / `>` |
| `𒊓` | `U+12293` | sa | Equality comparison ($==$) | `equal` / `==` |
| `𒉡` | `U+12261` | nu | Logical negation / empty literal | `not` / `empty` / `none` |
| `𒈨` | `U+12228` | me | Copula assertion | `is` / `me` |
| `𒀝` | `U+1201D` | ak | Recipe invocation | `apply` |
| `𒆕` | `U+12195` | dù | Recipe invocation (variant) | `apply` |
| `𒆥` | `U+121A5` | kin | Working tablet declaration | `working` |
| `𒁶` | `U+12076` | gim | Inscribe as tablet / record equivalence | `as` / `gim` |
| `𒀀` | `U+12000` | a | Target preposition | `into` / `to` |
| `𒁍` | `U+1204D` | gíd | Sequence length measurement | `length` |
| `𒍑` | `U+12351` | uš | Tablet length measurement (variant) | `length` |
| `𒁕` | `U+12055` | da | Companion preposition | `with` / `da` |
| `𒃮𒊑` | `U+120EE U+12291` | gaba-ri | Copy tablet archive | `copy` |
| `𒁴` | `U+12074` | dim | Derive tablet archive | `derive` |

> [!NOTE]
> In range iterations (`consider ... through ...`), `𒂗` (`en`, `U+12097`) is the canonical, normative range terminator. The calendar sign `𒌗` (`iti`, `U+12317`) is supported as an attested astronomical and calendrical alias.

---

## 3. Standard Symbolic Identifier Signs

Where attested domain-specific terms are not established in historical tablets, DUB.SAR adopts symbolic cuneiform signs for variables, counters, and record fields:

| Sign | Codepoint | Transliteration | Symbolic Meaning in Examples |
| :---: | :--- | :--- | :--- |
| `𒈬` | `U+1222C` | MU | Year / solar cycle / iteration index |
| `𒍠` | `U+12360` | ZAG | Boundary limit / loop maximum |
| `𒁇` | `U+12047` | BAR | Fractional remainder / side measurement |
| `𒊕` | `U+12295` | SAG | Head record / optimal candidate |
| `𒁄` | `U+12044` | BAL | Cycle index / alternation counter |
| `𒋛` | `U+122DB` | SI | Leap counter / diagonal extent |
| `𒈬𒁶` | `U+1222C U+12076` | MU.GIM | Candidate year quantity |
| `𒇲` | `U+121F2` | LAL | Error / deficit / discrepancy |
| `𒊮` | `U+122AE` | SHA3 | Candidate record tuple / inner state |
| `𒅎` | `U+1214E` | IM | Tablet index / iteration count |
| `𒃷` | `U+120F7` | GAN | Approximated root result |
| `𒅆𒁀` | `U+12146 U+12040` | IGI.BA | Square root approximation recipe |
| `𒈠` | `U+12220` | MA | Initial parameter / bound |
| `𒋰` | `U+122F0` | TAB | Companion / factor 2 / steps |
| `𒄿` | `U+1213F` | I | Step state variable |
| `𒈠𒁶` | `U+12220 U+12076` | MA.GIM | Updated iteration value |
| `𒈬𒁹` .. `𒈬𒐉` | `U+1222C U+12079` .. `U+1222C U+12409` | MU.1 .. MU.4 | Year index variables 1 through 4 |
| `𒋛𒈬` | `U+122DB U+1222C` | SI.MU | Leap distribution calculation recipe |
| `𒋛𒀀` | `U+122DB U+12000` | SI.A | Boolean leap day indicator |

---

## 4. Punctuation and Formatting

| Cuneiform Sign | Codepoint | Transliteration | Scribal Role | Scholar Equivalent |
| :---: | :--- | :--- | :--- | :--- |
| `𒑰` | `U+12470` | - | Old Assyrian word divider / comment marker | `#` |

---

## 5. String Literal Policy

String literals (enclosed in double `"` or single `'` quotes) represent **data**, not language syntax:

- Arbitrary text strings are not translated into cuneiform signs.
- Strings preserve their exact Unicode content (Latin text, cuneiform, punctuation, or any modern character set) across all source modes and transliteration passes.
