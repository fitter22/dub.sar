# Core Language Vocabulary

This document catalogs the complete keyword, verb, operator, and scribal vocabulary for DUB.SAR across Scholar Mode, Tablet Mode (authentic cuneiform ideograms), and Transliteration Mode.

---

## 1. Structural Keywords & Section Delimiters

| Scholar Keyword | Transliteration | Tablet Mode (Cuneiform) | Category | Description |
| :--- | :--- | :---: | :--- | :--- |
| `problem` / `given` | `e-diš` / `e-dis` | `𒂊𒁹` | Section | Marks the beginning of the problem statement and input declaration. |
| `recipe` / `procedure` | `dub-sar` | `𒁾𒊬` | Section | Defines a named sub-computation, procedure, or transformation. |
| `result` | `ka-diš` / `ka-dis` | `𒅗𒁹` | Section | Marks the result section specifying final outputs inscribed to tablet. |

---

## 2. Control Flow & Search Operations

| Scholar Keyword | Transliteration | Tablet Mode (Cuneiform) | Category | Description |
| :--- | :--- | :---: | :--- | :--- |
| `when` / `if` | `e-a` | `𒂊𒀀` | Conditional | Conditional guard evaluating a boolean predicate. |
| `else` | `nu-e-a` | `𒉡𒂊𒀀` | Conditional | Fallback execution branch when prior guards evaluate to false. |
| `consider` / `repeat` / `for` | `gi` | `𒄀` | Loop / Search | Bounded domain iteration or candidate generation. |
| `from` | `ta` | `𒋫` | Range | Range origin lower boundary. |
| `through` / `to` / `..` | `en` | `𒂗` | Range | Canonical range upper boundary (*adi*). |
| `through` / `to` (calendar alias) | `iti` | `𒌗` | Range | Astronomical and calendar alias for range upper boundary. |
| `retain` / `keep` | `te` / `tu` | `𒋼` | Search | Retains candidate meeting optimization criteria (*ṭehû*). |
| `determine` | `nam` | `𒉆` / `𒉇` | Control | Terminates recipe and produces determined return quantity. |
| `return` | `ĝeš` / `ges` | `𒄑` | Control | Returns control and values from procedure block. |
| `apply` | `ak` / `dù` | `𒀝` / `𒆕` | Invocation | Applies recipe or sub-procedure to provided arguments. |

---

## 3. Mathematical Operations & Postfix Verbs

| Scholar Verb / Operator | Transliteration | Tablet Mode (Cuneiform) | Operation | Mathematical Formula |
| :--- | :--- | :---: | :--- | :--- |
| `add` / `+` | `zi` | `𒍣` | Addition | $a + b$ |
| `subtract` / `sub` / `-` | `ta` | `𒋫` | Subtraction | $a - b$ |
| `multiply` / `mul` / `*` / `of` | `ša` / `sha` | `𒊭` | Multiplication / Scaling | $a \times b$ |
| `divide` / `div` / `/` | `ni` | `𒉌` | Division | $a / b$ |
| `%` / `mod` | - | - | Sexagesimal Remainder | $a \pmod b$ |
| `**` / `pow` | - | - | Power / Exponentiation | $a^b$ |
| `square` | `íb` | `𒅁` | Geometric Square | $a^2$ |
| `square-root` / `sqrt` | `ba-si` | `𒁀𒋛` | Proportion / Square Root | $\sqrt{a}$ |
| `floor` | `gur` | `𒄥` | Floor Rounding | $\lfloor a \rfloor$ |
| `ceil` | `nim` | `𒉏` | Ceiling Rounding | $\lceil a \rceil$ |
| `nearest` / `round` | `ri` | `𒊑` | Nearest Integer Rounding | $[a]$ |
| `absolute` / `abs` | `te` | `𒋼` | Absolute Value | $|a|$ |

---

## 4. Persistent Clay Tablet Archive & Records

| Scholar Operation | Transliteration | Tablet Mode (Cuneiform) | Category | Description |
| :--- | :--- | :---: | :--- | :--- |
| `consult tablet` | `igi dub` | `𒅆 𒁾` | Archive | Inspects or loads an external or persistent tablet record. |
| `tablet` | `dub` | `𒁾` | Archive | Declares a named persistent tablet entity. |
| `working` | `kin` | `𒆥` | Archive | Declares a mutable in-memory scratchpad tablet. |
| `put` | `gar` | `𒃻` | Inscription | Deposits an entry or record into a tablet. |
| `append` | `dah` | `𒈭` | Inscription | Appends an entry onto an existing tablet sequence. |
| `take entry` / `pad` | `pad ... šu` | `𒉻 ... 𒋗` | Retrieval | Retrieves an indexed entry from a tablet entity. |
| `inscribe ... as tablet` | `... gim dub` | `... 𒁶 𒁾` | Inscription | Finalizes an in-memory collection as an immutable tablet. |
| `into` / `to` | `a` | `𒀀` | Target | Destination preposition for tablet entries. |
| `length` | `gíd` / `gid` / `uš` | `𒁍` / `𒍑` | Query | Returns entry count of a sequence or tablet. |
| `with` | `da` | `𒁕` | Join | Merges or joins candidate records. |
| `copy` | `gaba-ri` | `𒃮𒊑` | Archive | Produces duplicate tablet copy (*gaba-ri*). |
| `derive` | `dim` | `𒁴` | Archive | Derives child tablet with provenance record. |

---

## 5. Logical, Relational, and Assertion Terms

| Scholar Keyword | Transliteration | Tablet Mode (Cuneiform) | Meaning |
| :--- | :--- | :---: | :--- |
| `equal` / `==` | `sa` / `sá` | `𒊓` | Equality comparison |
| `not-equal` / `!=` | - | - | Inequality comparison |
| `lesser` / `<` | `tur` | `𒌉` | Strict less-than comparison |
| `greater` / `>` | `gal` | `𒃲` | Strict greater-than comparison |
| `not` | `nu` | `𒉡` | Logical negation |
| `is` | `me` | `𒈨` | Copula assertion / predicate test |
| `empty` / `none` | `nu` | `𒉡` | Null / empty sequence literal |
| `than` | `ta` | `𒋫` | Comparison ablative preposition |

---

## 6. Interactive I/O & Scribal Comments

| Scholar Keyword | Transliteration | Tablet Mode (Cuneiform) | Description |
| :--- | :--- | :---: | :--- |
| `inscribe` / `output` / `print` | `diš-a` / `sar` | `𒁹𒀀` / `𒊬` | Inscribes expression value to the output stream. |
| `ask` / `input` | `a-diš` | `𒀀𒁹` | Prompts for interactive external input during execution. |
| `#` | `𒑰` | `𒑰` | Old Assyrian word divider used for scribal comments. |
