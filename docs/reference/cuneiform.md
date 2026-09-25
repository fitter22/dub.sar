# Cuneiform Signs Reference

DUB.SAR uses Unicode cuneiform signs from the Unicode standard blocks:
- **Cuneiform**: `U+12000` to `U+123FF`
- **Cuneiform Numbers and Punctuation**: `U+12400` to `U+1247F`
- **Cuneiform Signs Extension**: `U+12480` to `U+1254F`

---

## 1. Structural Keywords

| Cuneiform Sign | Codepoint | Transliteration | Scribal Role | Scholar Equivalent |
| :---: | :--- | :--- | :--- | :--- |
| `𒂊𒁹` | `U+1208A U+12079` | e-diš | Problem section header | `problem` / `given` |
| `𒁾𒊬` | `U+12081 U+122AC` | dub-sar | Procedure / recipe definition | `recipe` / `procedure` |
| `𒅗𒁹` | `U+12157 U+12079` | ka-diš | Result section header | `result` |
| `𒂊𒀀` | `U+1208A U+12000` | e-a | Conditional guard | `when` / `if` |
| `𒉡𒂊𒀀` | `U+12261 U+1208A U+12000` | nu-e-a | Alternative conditional branch | `else` |
| `𒄀` | `U+12100` | gi | Repetition / loop header | `consider` / `repeat` |
| `𒂗` | `U+12097` | en | Range upper boundary | `through` / `to` |
| `𒋼` | `U+122F0` | te | Retain candidate statement | `retain` |
| `ナム` / `𒉆` | `U+12246` / `U+12247` | nam | Recipe return statement | `determine` / `return` |
| `𒄑` | `U+12117` | ĝeš | Procedure return | `return` |
| `𒁹𒀀` | `U+12079 U+12000` | diš-a | Output / inscription | `output` / `inscribe` |
| `𒀀𒁹` | `U+12000 U+12079` | a-diš | Interactive input request | `ask` / `input` |
| `𒑰` | `U+12470` | - | Scribal comment delimiter | `#` |

---

## 2. Mathematical and Relational Signs

| Cuneiform Sign | Codepoint | Transliteration | Mathematical Operation | Scholar Equivalent |
| :---: | :--- | :--- | :--- | :--- |
| `𒍣` | `U+12363` | zi | Addition | `add` / `+` |
| `𒋫` | `U+122EB` | ta | Subtraction / range start | `subtract` / `-` / `from` / `than` |
| `𒊭` | `U+122AD` | ša | Multiplication / of | `multiply` / `*` / `of` |
| `𒉌` | `U+1224C` | ni | Division | `divide` / `/` |
| `𒅁` | `U+12140` | íb | Square | `square` |
| `𒁀𒋛` | `U+12040 U+122DB` | ba-si | Square root | `square-root` / `sqrt` |
| `𒄥` | `U+12125` | gur | Floor rounding | `floor` |
| `𒉏` | `U+12258` | nim | Ceil rounding | `ceil` |
| `𒊑` | `U+12291` | ri | Nearest integer rounding | `nearest` |
| `𒋼` | `U+122F0` | te | Absolute value (postfix) | `absolute` |
| `𒌉` | `U+12309` | tur | Less than comparison | `lesser than` / `<` |
| `𒃲` | `U+120F2` | gal | Greater than comparison | `greater than` / `>` |
| `𒊓` | `U+12293` | sa | Equality comparison | `equal` / `==` |
| `𒉡` | `U+12261` | nu | Logical negation / empty literal | `not` / `empty` |
| `𒈨` | `U+12228` | me | Copula is | `is` |
| `𒀝` / `𒆕` | `U+1201D` / `U+12068` | ak / dù | Recipe invocation | `apply` |

---

## 3. Persistent Tablet Archive Signs

| Cuneiform Sign | Codepoint | Transliteration | Scribal Operation | Scholar Equivalent |
| :---: | :--- | :--- | :--- | :--- |
| `𒅆` | `U+12146` | igi | Consult / examine | `consult` |
| `𒁾` | `U+12081` | dub | Clay tablet entity | `tablet` |
| `𒆥` | `U+121A0` | kin | Working tablet declaration | `working` |
| `𒃻` | `U+120FB` | gar | Place entry into tablet | `put` |
| `𒈭` | `U+12076` | dah | Append entry to tablet | `append` |
| `𒉻` | `U+1227B` | pad | Take / retrieve entry | `take entry` / `pad` |
| `𒁶` | `U+12111` | gim | Inscribe as tablet / alias | `as` / `gim` |
| `𒀀` | `U+12000` | a | Target preposition | `into` / `to` |
| `𒁍` / `𒍑` | `U+12053` / `U+1234D` | gíd / uš | Sequence / tablet length | `length` |

---

## 4. Standard Symbolic Identifier Signs

Where attested domain-specific terms are not established in historical tablets, DUB.SAR adopts symbolic cuneiform signs for variables and record fields:

| Sign | Codepoint | Transliteration | Symbolic Meaning in Examples |
| :---: | :--- | :--- | :--- |
| `𒈬` | `U+1222C` | MU | Year / solar cycle / iteration index |
| `𒍠` | `U+12361` | ZAG | Boundary limit / loop maximum |
| `𒌓` | `U+12313` | UD | Whole-day value / time quantity |
| `𒁇` | `U+12047` | BAR | Fractional remainder / side measurement |
| `𒊕` | `U+122A0` | SAG | Head record / best candidate |
| `𒁄` | `U+12044` | BAL | Cycle index / iteration counter |
| `𒋛` | `U+122DB` | SI | Leap counter / diagonal extent |
| `𒈬𒁶` | `U+1222C U+12111` | MU.GIM | Candidate year quantity |
| `𒇲` | `U+121B7` | LAL | Error / deficit |
| `𒊮` | `U+122AE` | SHA3 | Candidate candidate tuple |
| `𒅎` | `U+1214E` | IM | Tablet reference / iteration count |
| `𒃷` | `U+120F7` | GAN | Approximated root result |
| `𒅆𒁀` | `U+12146 U+12040` | IGI.BA | Square root calculation recipe |
| `𒈠` | `U+12222` | MA | Initial argument parameter |
| `𒋰` | `U+122EB` | TAB | Companion / factor 2 / steps |
| `𒄿` | `U+1213E` | I | Variable step state |
| `𒈦` | `U+12226` | MASZ | Half constant / reciprocal entry |
| `𒈠𒁶` | `U+12222 U+12111` | MA.GIM | Updated iteration value |
| `𒈬𒁹` .. `𒈬𒐉` | `U+1222C ...` | MU.1 .. MU.4 | Year index variables 1 through 4 |
| `𒋛𒈬` | `U+122DB U+1222C` | SI.MU | Leap distribution calculation recipe |
| `𒋛𒀀` | `U+122DB U+12000` | SI.A | Boolean leap day indicator |

---

## 5. String Literal Policy

String literals (enclosed in double `"` or single `'` quotes) represent **data**, not language syntax. 

Arbitrary strings are not translated into cuneiform characters. Instead, strings preserve their exact Unicode content (Latin text, cuneiform, punctuation, or other human languages) across all source modes and transliteration passes.
