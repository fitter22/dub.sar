# DUB.SAR 1.0 — Language Specification

**Status:** 1.0 (first fully specified, implementation-ready version)  
**Style:** executable mathematical tablet language  
**Reference target:** exact-rational VM, with optional WebAssembly/native backends

## 1. Purpose

DUB.SAR is a modern executable language deliberately designed **from the perspective of a Mesopotamian mathematical tablet**, rather than as a modern programming language translated into Sumerian.

Its core ideas are:

- a source file is a **tablet/problem**;
- the fundamental objects are **named quantities**, not generic variables;
- calculations are expressed as **mathematical prescriptions**;
- procedures are reusable mathematical recipes;
- control flow is expressed as **conditions and bounded repetitions**;
- numbers are **exact rationals**, written canonically in sexagesimal notation;
- units are first-class and checked by the compiler;
- source may be written in cuneiform, Sumerian transliteration, or a mixture;
- every valid program has deterministic executable semantics.

DUB.SAR is **historically inspired, not historically reconstructed**. Sumerian vocabulary, cuneiform signs, sexagesimal mathematics, and the organization of mathematical texts provide the cultural substrate; the grammar, type system, compiler, VM, and programming meanings of signs are modern DUB.SAR inventions.

Sumerian is typically left-headed inside noun phrases, while clauses are typically right-headed, with the verb at the end. Sumerian also uses phrase-final case markers. DUB.SAR borrows the *shape* of this organization—quantity/operand material followed by an operation—without claiming to reproduce Sumerian grammar. Mesopotamian mathematical texts are likewise strongly procedural, often presenting quantities and then prescribing operations.

Unicode defines dedicated Cuneiform and Cuneiform Numbers and Punctuation blocks, while also noting that historical numeral interpretation depends on metrological system. DUB.SAR therefore defines its own canonical computational number semantics.

---

## 2. Source modes

### 2.1 Tablet mode

The canonical visual form uses Unicode cuneiform signs.

Example:

```text
𒂊𒁹

    𒈬 : 365;14,31,55 𒌓
```

### 2.2 Scholar mode

The same program can be written using Latin transliteration / ASCII identifiers:

```text
PROBLEM

    mu : 365;14,31,55 day
```

### 2.3 Mixed mode

Cuneiform and transliterated tokens may be mixed:

```text
𒂊𒁹

    𒈬 : 365;14,31,55 𒌓
    best-cycle :
        100
        nearest
```

All three modes MUST normalize to the same token stream and AST when semantically equivalent.

---

## 3. Lexical rules

### 3.1 Unicode

Source is Unicode text. Cuneiform signs are interpreted as distinct code points/sign tokens; a parser MUST NOT replace one sign with another solely because the signs have related scholarly readings.

### 3.2 Whitespace and indentation

Spaces separate tokens. Indentation is significant.

A block begins after `:` and consists of following lines indented one level further than the header.

Two-space and four-space indentation are both valid. A project SHOULD standardize on four spaces.

### 3.3 Comments

Scholar-mode comments begin with `#`.

Tablet-mode comments may begin with `𒑰`.

A comment continues to end of line.

### 3.4 Identifiers

ASCII technical identifiers use:

```text
[A-Za-z_][A-Za-z0-9_-]*
```

Cuneiform identifiers consist of one or more cuneiform signs that are not reserved syntax tokens.

Identifiers are case-sensitive in Scholar mode.

---

## 4. Canonical vocabulary

The following tokens are part of DUB.SAR 1.0. Their programming meanings are **DUB.SAR conventions** unless explicitly identified as historical.

| Token | Scholarly value | DUB.SAR role |
|---|---|---|
| `𒂊𒁹` | e-diš | problem/tablet start |
| `𒁾𒊬` | dub-sar | procedure / recipe declaration |
| `𒅗𒁹` | ka-diš | result section |
| `𒈬` | mu | year/unit symbol |
| `𒌓` | ud | day/unit symbol |
| `𒌗` | iti | month/unit symbol / through |
| `𒍣` | zi | addition verb / postfix add |
| `𒋫` | ta | subtraction verb / postfix subtract / from |
| `𒊭` | ša | multiplication verb / postfix multiply |
| `𒉌` | ni | division verb / postfix divide |
| `𒄥` | gur | floor / integer part |
| `𒉏` | nim | ceiling |
| `𒊑` | ri | nearest rounding |
| `𒋼` | te | absolute value / retain selection |
| `𒌉` | tur | lesser than (`<`) |
| `𒃲` | gal | greater than (`>`) |
| `𒊓` | sa | equal (`==`) |
| `𒈨` | me | copula is |
| `nu` / `𒉡` | nu | empty sentinel / negation |
| `shu` / `𒋗` | šu | take operand |
| `nam` / `𒉆` | nam | determine record |
| `𒄀` | gi | bounded repetition / domain |
| `𒂊𒀀` | e-a | conditional / when |
| `𒉡𒂊𒀀` | nu-e-a | alternative branch / else |
| `𒄑` | ĝeš | return |
| `𒁹𒀀` | diš-a | output / inscribe |
| `𒀀𒁹` | a-diš | input / ask |
| `𒅆` | igi | consult persistent tablet |
| `𒁾` | dub | tablet keyword |
| `𒆥` | kin | working mutable tablet |
| `𒃻` | gar | put entry into tablet |
| `𒁕` | da | with |
| `𒃮𒊑` | gaba-ri | copy tablet |
| `𒁶` | gim | as |
| `pad` | pad | entry |
| `𒑰` | — | comment marker |

The vocabulary is intentionally small. Where a modern programming concept has no defensible historical Sumerian equivalent, DUB.SAR assigns a transparent technical convention instead of pretending the term is ancient.

---

## 5. Program model

A DUB.SAR source file is a **tablet**.

Its structure is:

```text
TABLET
  PROBLEM
  PROCEDURES*
  RESULT
```

The problem section establishes initial quantities and calls procedures. Procedures are declared at tablet level between the problem and result sections and are registered before execution of the problem section. The result section emits final results.

There is no class/object system in 1.0.

---

## 6. Grammar

The normative grammar is:

```ebnf
tablet           ::= problem-section recipe-section* result-section ;

problem-section  ::= ("𒂊𒁹" | "problem" | "given") block ;
result-section   ::= ("𒅗𒁹" | "result") block ;
recipe-section   ::= recipe ;

recipe           ::= ("𒁾𒊬" | "recipe" | "procedure") identifier parameter* ":" block ;
parameter        ::= identifier ;

block            ::= NEWLINE INDENT statement+ DEDENT ;

statement        ::= declaration
                   | determination
                   | retain-statement
                   | repetition
                   | determine-statement
                   | return-statement
                   | output-statement
                   | consult-statement
                   | working-statement
                   | copy-statement
                   | derive-statement
                   | inscribe-statement
                   | put-statement
                   | replace-statement
                   | remove-statement
                   | expression-statement
                   | expression ;

declaration      ::= identifier ":" expression unit?
                   | identifier ":" NEWLINE INDENT postfix-step+ DEDENT
                   | identifier ":" ("𒉡" | "empty") ;

determination    ::= identifier ":" identifier ("," identifier)+
                   | identifier ":" NEWLINE INDENT identifier+ DEDENT ;

retain-statement ::= ("𒋼" | "retain") identifier (NEWLINE INDENT)? (("𒂊𒀀" | "when") expression)? ;

conditional      ::= ("𒂊𒀀" | "when" | "if") expression ":" block alternative? ;
alternative      ::= ("𒉡𒂊𒀀" | "else") ":" block ;

repetition       ::= ("𒄀" | "consider" | "repeat") identifier range ":" block ;
range            ::= (("𒋫" | "from")? expression)? ("𒂗" | "through" | "to" | "..") expression
                   | expression ;

determine-statement ::= ("𒉆" | "nam" | "determine") expression ;
return-statement ::= ("𒄑" | "return") expression ("," expression)* ;
output-statement ::= ("𒁹𒀀" | "output" | "inscribe") expression ;
input-expression ::= ("𒀀𒁹" | "ask" | "input") ("(" string ")" | string) ;

consult-statement   ::= ("𒅆" | "consult" | "examine") expression (("version" | "mu" | "𒈬") expression)? (("𒁶" | "as") identifier)? ;
working-statement   ::= ("create")? ("𒆥" | "working") ("𒁾" | "tablet")? identifier ;
copy-statement      ::= ("𒃮𒊑" | "copy") (expression)? (("version" | "mu" | "𒈬") expression)? ("𒁶" | "as") ("𒆥" | "working")? identifier ;
derive-statement    ::= "derive" ("𒋫" | "from") expression (("version" | "mu" | "𒈬") expression)? ("𒁶" | "as") ("𒆥" | "working")? identifier ;
inscribe-statement  ::= ("𒁹𒀀" | "output" | "inscribe" | "𒊬") identifier ("𒁶" | "as") expression ;
put-statement       ::= ("𒃻" | "put" | "insert" | "set") expression ("into" | "in" | "𒀀") identifier ("at" | "𒀀") expression ;
replace-statement   ::= (identifier)? ("replace" | "update") ("entry" | "pad")? expression ("𒁕" | "with") expression ("into" identifier)? ;
remove-statement    ::= ("remove" | "delete") ("entry" | "pad")? expression ("𒋫" | "from") identifier ;

expression       ::= comparison ;
comparison       ::= sum (comparison-op sum)*
                   | sum "is" ("lesser" | "greater" | "equal") ("than")? sum
                   | sum "is" ("empty" | "not" "empty") ;
comparison-op    ::= "==" | "!=" | "<" | "<=" | ">" | ">=" | "𒌉" | "𒃲" | "𒊓" ;

sum              ::= product (("+"|"-"|"𒍣"|"𒋫"|"add"|"subtract") product)* ;
product          ::= power (("*"|"/"|"%"|"𒊭"|"𒉌"|"multiply"|"divide") power)* ;
power            ::= unary ("**" unary)? ;
unary            ::= ("-" | "𒉡" | "not")? primary ;

postfix-step     ::= primary | postfix-op | apply-recipe ;
apply-recipe     ::= ("𒀝" | "apply") identifier ;
postfix-op       ::= "floor" | "ceil" | "nearest" | "absolute"
                   | "add" | "subtract" | "multiply" | "divide" | "take"
                   | "𒄥" | "𒉏" | "𒊑" | "𒋼" | "𒍣" | "𒋫" | "𒊭" | "𒉌" | "𒋗" ;

primary          ::= number quantity-unit?
                   | field-access
                   | identifier
                   | string
                   | ("𒉡" | "empty")
                   | call
                   | input-expression
                   | take-entry
                   | seek-entry
                   | history-expression
                   | "(" expression ")" ;

take-entry       ::= ("𒋗" | "take") ("entry" | "pad")? expression ("𒋫" | "from") primary
                   | expression ("𒋗" | "take") ("entry" | "pad")? ("𒋫" | "from") primary ;
seek-entry       ::= ("seek" | "find") ("entry" | "pad")? ("nearest" | "round" | "ri" | "𒊑")? expression ("in" | "into" | "𒋫" | "from") primary ;
history-expression ::= ("history" | "igi-kar") ("of" | "𒊭") primary ;

field-access     ::= primary "." identifier
                   | identifier ("of" | "𒊭") primary ;

quantity-unit    ::= unit ;
unit             ::= identifier | cuneiform-unit ;
call             ::= identifier "(" arguments? ")" ;
arguments        ::= expression ("," expression)* ;
identifier       ::= cuneiform-identifier | ascii-identifier ;
```

Scholar/ASCII aliases MAY be provided by an implementation, but they MUST normalize to the same AST as their canonical DUB.SAR counterparts.

---

## 7. Quantities

A quantity is a pair:

```text
(value, unit)
```

where `value` is an exact rational and `unit` is a dimension/unit expression.

Examples:

```text
365 𒌓
24 𒌗
3
```

The first has a day unit, the second a month unit, and the third is dimensionless.

### 7.1 Establishing a quantity

```text
𒈬 : 365;14,31,55 𒌓
```

establishes the named quantity `𒈬` with value `365;14,31,55` days.

### 7.2 Postfix calculation pipelines

A quantity may be established via an indented postfix calculation block:

```text
whole-days :
    solar-year
    𒄥

fraction :
    solar-year
    whole-days
    𒋫
```

In Scholar Mode:

```text
whole-days :
    solar-year
    floor

fraction :
    solar-year
    whole-days
    subtract
```

Operands and intermediate values are pushed to the calculation stack; trailing postfix operators reduce the stack.

### 7.3 Mathematical determinations and empty sentinels

A **determination** is a typed record combining multiple named quantities:

```text
candidate : cycle, leaps, error
```

A record may be initialized to the **empty sentinel** before searching:

```text
best : 𒉡
```

or in Scholar Mode:

```text
best : empty
```

### 7.4 Field access

Fields of a determination record are accessed via dot notation or prepositional syntax:

```text
best.error
error of best
```

### 7.5 Derived quantities
 
```text
fraction :
    solar-year
    whole-days
    subtract
```

uses `:` to establish a derived quantity via mathematical prescription.

A name established in a procedure is local to that procedure.

---

## 8. Numbers

### 8.1 Integer literals

Decimal integers are allowed for interoperability:

```text
0
1
365
1000
```

### 8.2 Canonical sexagesimal literals

The canonical fractional syntax is:

```text
integer ; digit , digit , ...
```

Example:

```text
365;14,31,55
```

means:

\[
365 + \frac{14}{60} + \frac{31}{60^2} + \frac{55}{60^3}.
\]

It is represented exactly.

### 8.3 Digit rules

Every sexagesimal fractional digit MUST satisfy:

```text
0 <= digit < 60
```

Thus `1;59,59` is valid and `1;60,0` is invalid.

### 8.4 Negative values

A leading `-` applies to the complete rational value.

```text
-1;30
```

means:

\[
-(1 + 30/60).
\]

### 8.5 Cuneiform numeral input

Unicode encodes dedicated Cuneiform numeric signs, but historical cuneiform numeral interpretation is metrologically dependent. A DUB.SAR implementation MUST resolve cuneiform numerals through the DUB.SAR numeral table before converting them to an internal value. It MUST NOT treat Unicode's `Numeric_Value` property as a universal historical absolute value.

### 8.6 Internal representation

All ordinary DUB.SAR numeric values MUST be stored semantically as:

```text
Rational(numerator, denominator)
```

with positive denominator and normalized numerator/denominator.

Arbitrary-precision integers SHOULD be used.

---

## 9. Arithmetic semantics

Supported arithmetic:

```text
+
-
*
/
%
**
```

The cuneiform mathematical verbs are also supported:

```text
𒍣   add
𒋫   subtract
𒊭   multiply
𒉌   divide
```

### 9.1 Addition/subtraction

Operands MUST be dimensionally compatible.

```text
3 𒌓 + 2 𒌓
```

is valid.

```text
3 𒌓 + 2 𒌗
```

is rejected unless the programmer explicitly converts the units.

### 9.2 Multiplication

Dimensions multiply algebraically.

```text
2 𒌓 * 3 𒌓
```

has unit `day^2`.

### 9.3 Division

Dimensions divide algebraically.

```text
10 𒌓 / 2
```

has unit `day`.

### 9.4 Exact division

`/` always means exact rational division. Truncation is never implicit.

---

## 10. Comparison

Valid comparison operators:

```text
== != < <= > >=
```

Cuneiform comparative operators:

```text
𒌉   lesser than (<)
𒃲   greater than (>)
𒊓   equal to (==)
```

Scholar Mode also supports verbal comparative expressions:

```text
error is lesser than best.error
error is greater than best.error
error is equal to target
target is empty
target is not empty
```

Compared quantities MUST be dimensionally compatible.

Comparisons yield an internal Boolean value used for control flow.

---

## 11. Conditions and atomic selection

### 11.1 Block conditions

Native form:

```text
𒂊𒀀 error < best:
    best : error
```

Scholar/ASCII alias:

```text
when error < best:
    best : error
```

Alternative branch:

```text
𒉡𒂊𒀀:
    ...
```

or ASCII `else:`.

Booleans are primarily control values. DUB.SAR 1.0 does not require Boolean variables as a core mathematical abstraction.

### 11.2 Atomic retain selection

Rather than branching imperatively with mutable assignments, mathematical optimization uses atomic retention:

```text
𒋼 candidate 𒂊𒀀 error 𒌉 best.error
```

Scholar Mode:

```text
retain candidate when error is lesser than best.error
```

If the target determination (`best`) holds the empty sentinel (`𒉡` / `empty`), the candidate is retained immediately without evaluating the comparison.

---

## 12. Repetition

DUB.SAR uses **bounded mathematical repetition**, not an unrestricted `while` loop.

### 12.1 Bounded search domains

The canonical mathematical search domain specifies an inclusive lower and upper bound:

```text
𒄀 cycle 𒋫 1 𒌗 limit:
    ...
```

Scholar Mode:

```text
consider cycle from 1 through limit:
    ...
```

The bound marker `𒋫` (`from`) and separator `𒌗` (`through`, `to`, `..`) delineate the finite search range.

### 12.2 Single-bound and range variants

Single-bound form:

```text
𒄀 cycle 1000:
    ...
```

means `cycle = 1, 2, ..., 1000`.

Explicit range without lower marker:

```text
𒄀 cycle 1 𒌗 1000:
    ...
```

Scholar Mode alias:

```text
repeat cycle 1 to 1000:
    ...
```

The upper bound is inclusive.

A repetition MUST be finite. Implementations MUST reject a statically negative count where it cannot be given a meaningful range interpretation.

---

## 13. Procedures

A procedure is a reusable mathematical recipe.

Canonical form:

```text
𒁾𒊬 leap-rule solar limit:
    ...
    𒉆 result
```

In Scholar Mode:

```text
recipe leap-rule solar limit:
    ...
    determine result
```

A recipe produces a quantity or determination result.

Recipe application uses postfix notation:

```text
res :
    solar
    1000
    𒀝 leap-rule
```

or in Scholar Mode:

```text
res :
    solar
    1000
    apply leap-rule
```

---

## 14. Built-in mathematical procedures

The standard implementation MUST provide:

```text
abs(x)
floor(x)
ceil(x)
nearest(x)
min(a,b)
max(a,b)
gcd(a,b)
lcm(a,b)
```

### 14.1 `nearest`

Returns the nearest integer. If the argument is dimensionless, the result is a dimensionless integer. If the argument is a quantity, the result is the corresponding integer count and is dimensionless.

Exact half-way cases round away from zero.

```text
nearest(2.49) = 2
nearest(2.5)  = 3
nearest(-2.5) = -3
```

Decimal examples here are explanatory; canonical DUB.SAR source uses exact rationals.

### 14.2 `floor`

Returns mathematical floor. For a quantity, the result retains the same unit and has an integer-valued magnitude.

### 14.3 `ceil`

Returns mathematical ceiling. For a quantity, the result retains the same unit and has an integer-valued magnitude.

### 14.4 Dual syntax: prefix procedures and postfix verbs

All primary mathematical operations can be written either as prefix functional calls or as postfix reduction verbs within calculation pipelines:

| Operation | Prefix form | Scholar postfix | Tablet postfix |
|---|---|---|---|
| Floor | `floor(x)` | `floor` | `𒄥` |
| Ceiling | `ceil(x)` | `ceil` | `𒉏` |
| Round to nearest | `nearest(x)` | `nearest` | `𒊑` |
| Absolute value | `abs(x)` | `absolute` | `𒋼` |
| Addition | `a + b` | `add` | `𒍣` |
| Subtraction | `a - b` | `subtract` | `𒋫` |
| Multiplication | `a * b` | `multiply` | `𒊭` |
| Division | `a / b` | `divide` | `𒉌` |

---

## 15. Units

The reference unit set contains:

```text
second
minute
hour
day
year
month
```

with:

```text
minute = 60 second
hour   = 60 minute
day    = 24 hour
```

`year` is intentionally a separate abstract calendar/astronomical unit and is NOT automatically defined as 365 days.

The cuneiform aliases are:

```text
𒌓 = day
𒈬 = year
𒌗 = month
```

The language MUST reject accidental mixing of incompatible units.

---

## 16. Conversion

Explicit conversion uses:

```text
convert(value, target-unit)
```

The standard library MUST refuse conversions that are not defined.

No implicit conversion from `year` to `day` exists in core DUB.SAR.

This is essential for planetary-calendar programs because the unknown solar year is the very quantity being modeled.

---

## 17. Input and output

### 17.1 Input

Prompted input establishes a quantity:

```text
solar-year : 𒀀𒁹 "solar year in days"
```

Scholar Mode:

```text
solar-year : ask "solar year in days"
```

The runtime accepts an exact integer, sexagesimal value, or decimal input and immediately converts it to the exact rational representation.

### 17.2 Output and inscription

#### Explicit inscription

```text
𒁹𒀀 "cycle:"
𒁹𒀀 cycle
```

Scholar Mode: `output "cycle:"`.

#### Implicit result inscription

Listing a quantity, determination record, or expression on its own line within the `result` (`𒅗𒁹`) section automatically inscribes and emits its values in order:

```text
𒅗𒁹

    best
```

If `best` is a determination `candidate : cycle, leaps, error`, its constituent values are emitted sequentially. Strings are Unicode strings.

---

## 18. Scope

DUB.SAR uses lexical/static scope.

A name established inside a procedure is local to that procedure.

Procedure parameters shadow names in outer scopes.

There is no dynamic scope.

---

## 19. Errors

A conforming implementation MUST distinguish at least:

- `SyntaxError` — malformed source;
- `NameError` — unknown name;
- `UnitError` — incompatible dimensions;
- `DivisionByZero` — zero divisor;
- `RangeError` — invalid repetition range;
- `InputError` — invalid numeric input;
- `ReturnError` — procedure does not return the declared result shape.

---

## 20. Program execution

Execution proceeds:

1. initialize the standard library;
2. parse and semantically validate the complete tablet;
3. register all procedures;
4. execute the problem section in source order;
5. execute the result section;
6. terminate with the final observable output.

For deterministic programs, identical input and source MUST produce identical output.

---

## 21. Intermediate representation

DUB.SAR's natural IR is **stack-oriented**, because the source language is designed around worked calculations.

Example source:

```text
candidate-year :
    whole
    leaps
    cycle
    divide
    add
```

may lower to:

```text
LOAD whole
LOAD leaps
LOAD cycle
DIV
ADD
STORE candidate-year
```

A semantic IR node retains both value and unit information.

---

## 22. Virtual machine

A reference DUB.SAR VM SHOULD expose:

```text
operand stack
environment stack
call stack
unit table
constant table
I/O interface
```

Recommended bytecode instructions:

```text
CONST
LOAD
STORE
ADD
SUB
MUL
DIV
REM
POW_INT
CMP
JUMP
JUMP_IF_FALSE
RANGE
CALL
RETURN
FLOOR
CEIL
NEAREST
ABS
INPUT
OUTPUT
```

The bytecode is an implementation detail, not part of the source language.

---

## 23. Compiler architecture

A practical compiler can be:

```text
        .dub source
             |
             v
      +--------------+
      | Unicode lexer|
      +------+-------+
             |
             v
      +--------------+
      | parser / AST  |
      +------+-------+
             |
             v
      +--------------+
      | semantic pass |
      | names + units |
      +------+-------+
             |
             v
      +--------------+
      | DUB.SAR IR    |
      +------+-------+
         /          \
        v            v
   +---------+   +-----------+
   | DUB VM  |   | WASM/LLVM |
   +---------+   +-----------+
```

### Recommended implementation

Python 3 is a good reference implementation language because it has Unicode strings and arbitrary-size integers. The compiler front end can be implemented using a hand-written lexer/parser or a small parser generator.

The first release SHOULD be an interpreter. Once the interpreter passes the language test suite, add bytecode compilation, then WebAssembly, then native LLVM output.

---

## 24. CLI

Reference commands:

```text
dubsar run tablet.dub [--backend=vm|ast] [--input=...]
dubsar check tablet.dub
dubsar format tablet.dub [--mode=tablet|scholar]
dubsar compile tablet.dub --target=bytecode
dubsar compile tablet.dub --target=wasm
dubsar compile tablet.dub --target=wat
dubsar compile tablet.dub --target=ir
dubsar compile tablet.dub --target=json
dubsar transliterate tablet.dub
dubsar cuneiform tablet.dub
dubsar render tablet.dub --style=tablet
dubsar render tablet.dub --style=text
dubsar render tablet.dub --style=tablet --strip-comments
```

Supported compilation targets:
- `bytecode` — Stack bytecode chunk for the DUB.SAR VM;
- `wasm` / `wat` — WebAssembly text format with 64-bit rational runtime;
- `ir` — High-level mathematical Semantic IR;
- `json` — Abstract syntax tree serialized as JSON;
- `native` — Native LLVM machine code (planned Stage 4).

`render` is a presentation feature; case lines, tablet borders and similar visual features do not affect program semantics.

Unicode documents cuneiform case ruling and similar lines as formatting rather than syntax, supporting this separation.

---

## 25. Tablet rendering

A DUB.SAR implementation SHOULD be able to render source as:

- Unicode text (terminal double-line border box);
- transliterated scholar text;
- SVG (authentic Mesopotamian clay tablet artwork with bevels, texture gradients, case rulings, and drop shadows);
- PNG;
- PDF;
- clay-tablet-style artwork.

The renderer MAY provide an option (`--strip-comments`) to omit transliteration annotations and comments for pure museum-grade cuneiform presentation.

The renderer consumes the canonical AST/sign stream. It does not reinterpret program semantics.

---

## 26. Full example: planetary leap-year rule

### 26.1 Problem

Given a planet's solar year `Y` in fractional days, find a repeating calendar cycle with at most `N` years such that inserting one extra day in `L` of those years minimizes:

\[
\left|Y - \left(\lfloor Y \rfloor + L/C\right)\right|.
\]

For each candidate cycle `C`, choose:

\[
L = \operatorname{nearest}(C(Y-\lfloor Y\rfloor)).
\]

### 26.2 Valid DUB.SAR 1.0 source

#### Tablet Mode (Cuneiform)

```text
𒂊𒁹

    solar-year : 𒀀𒁹 "solar year in days"
    limit : 1000

    whole-days :
        solar-year
        𒄥

    fraction :
        solar-year
        whole-days
        𒋫

    best : 𒉡

    𒄀 cycle 𒋫 1 𒌗 limit:

        leaps :
            cycle
            fraction
            𒊭
            𒊑

        error :
            whole-days
            leaps
            cycle
            𒉌
            𒍣
            solar-year
            𒋫
            𒋼

        candidate :
            cycle
            leaps
            error

        𒋼 candidate 𒂊𒀀 error 𒌉 best.error

𒅗𒁹

    best
```

#### Scholar Mode (Latin Transliteration)

```text
problem

    solar-year : ask "solar year in days"
    limit : 1000

    whole-days :
        solar-year
        floor

    fraction :
        solar-year
        whole-days
        subtract

    best : empty

    consider cycle from 1 through limit:

        leaps :
            cycle
            fraction
            multiply
            nearest

        error :
            whole-days
            leaps
            cycle
            divide
            add
            solar-year
            subtract
            absolute

        candidate :
            cycle
            leaps
            error

        retain candidate when error is lesser than best.error

result

    best
```

### 26.3 Semantic result for Earth-like input

For `Y = 365.2422`, with `maximum-cycle = 1000`, the bounded search selects:

```text
cycle = 673
leaps = 163
common = 510
```

so the mean calendar year is:

```text
365 + 163/673
```

The computation remains exact internally; decimal output is only presentation formatting.

---

## 27. Even distribution of leap years

A cycle `(C,L)` specifies the average year but not which years receive an extra day.

DUB.SAR 1.0 therefore recommends the following exact accumulator procedure:

```text
𒁾𒊬 leap-for-year year cycle leaps:

    prev-year :
        year
        1
        -

    cur-count :
        year
        leaps
        *
        cycle
        /
        𒄥

    prev-count :
        prev-year
        leaps
        *
        cycle
        /
        𒄥

    is-leap :
        cur-count
        prev-count
        -

    𒉆 is-leap
```

A caller can invoke this for every year in a cycle. This distributes leap days with mathematical uniformity over the cycle without imperative state mutations.

---

## 28. Exactness and optimization

Compiler optimizations MUST preserve exact rational semantics.

Allowed examples:

- constant folding;
- rational reduction;
- common-subexpression elimination;
- dead-code elimination;
- fixed-range unrolling;
- replacing the leap-year bounded search with an equivalent continued-fraction algorithm.

A compiler MUST NOT silently replace exact arithmetic with binary floating point when that can change observable semantics.

---

## 29. Conformance tests

A DUB.SAR 1.0 implementation MUST test at least:

### Numbers

```text
1
60
1;0
1;30
365;14,31,55
```

### Arithmetic

```text
1;30 + 0;30 = 2
2 * 0;30 = 1
3 / 2 = 1;30
```

### Unit safety

```text
1 day + 2 day       valid
1 day + 2 year      invalid
```

### Control flow

```text
repeat 1..1
repeat 1..1000
```

### Exactness

Equivalent rational values MUST compare equal regardless of their input spelling.

---

## 30. Historical authenticity policy

Every feature belongs to one of three categories.

### A. Historically grounded

Examples:

- cuneiform writing;
- Sumerian lexical material;
- sexagesimal mathematical inspiration;
- quantity/measurement orientation;
- procedural mathematical presentation.

### B. Historically inspired but modernized

Examples:

- tablet/problem organization;
- quantity-first declarations;
- operation-at-end mathematical style;
- bounded mathematical repetition.

### C. Modern invention

Examples:

- compiler grammar and mathematical AST;
- `retain` and atomic selection;
- high-level Semantic IR;
- stack bytecode VM and WebAssembly backend;
- arbitrary-precision rational runtime representation;
- command-line interface, automated formatter, and SVG renderer.

A DUB.SAR implementation or manual MUST never present category-C syntax as evidence about ancient Sumerian programming. Never say "ancient Sumerians used `𒍣` as a programming addition operator." Say instead: "DUB.SAR assigns this sign the programming semantic `ADD`, inspired by its lexical and historical associations."

---

## 31. Why the language is deliberately not Python-like

The following is intentionally *not* the fundamental model:

```text
variable = value
for i in range(...):
    ...
```

Instead, DUB.SAR's conceptual model is:

```text
establish quantity
prescribe mathematical operation
repeat a bounded calculation
compare determinations
retain the best determination
write the result
```

The surface syntax therefore resembles an executable mathematical exercise more than a modern software language.

The stack-oriented IR reinforces this: a calculation is naturally represented as a stream of operands and operations, which can be displayed as a worked computational trace.

---

## 32. Reference implementation plan

A complete implementation can be built in four stages.

### Stage 1 — interpreter

Implement:

- lexer;
- source-mode normalization;
- parser;
- AST;
- exact rational values;
- units;
- procedures;
- conditions;
- bounded repetition;
- input/output;
- standard math library.

### Stage 2 — bytecode VM

Lower AST to the stack-oriented instruction set in §22.

### Stage 3 — WebAssembly

Compile bytecode or IR to WASM. Use a small exact-rational runtime represented with arbitrary-precision integers, or a verified integer/rational library where necessary.

### Stage 4 — native compiler

Lower the same IR to LLVM and produce native executables.

The language definition is independent of the backend, so all four execution modes share one semantic test suite.

---

## 33. Versioning

DUB.SAR 1.0 is the first stable language version.

Future 1.x releases MAY add:

- standard-library procedures;
- diagnostics;
- new output/rendering targets;
- performance optimizations;
- additional historically attested vocabulary where semantics are unambiguous.

They MUST NOT change the meaning of existing valid 1.0 programs.

Breaking semantic changes require DUB.SAR 2.0.

---

## 34. Design principle

The defining test for DUB.SAR is:

> **If written on clay, it should look primarily like a mathematical procedure. If fed to a compiler, every statement must have a precise machine meaning.**

That is the boundary DUB.SAR 1.0 is designed to occupy.

---

## 35. References

1. Electronic Text Corpus of Sumerian Literature, **Sumerian language** — grammar, noun phrases, case markers, clause structure.  
   https://etcsl.orinst.ox.ac.uk/edition2/language.php

2. Unicode Standard 17.0, **Chapter 11 — Cuneiform and Sumero-Akkadian** — Unicode encoding, cuneiform numerals, metrological context.  
   https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-11/

3. Unicode, **Cuneiform Numbers and Punctuation** — Unicode names and code points.  
   https://www.unicode.org/charts/nameslist/c_12400.html

4. Cuneiform Digital Library Initiative (CDLI).  
   https://cdli.earth/

Historical claims in this specification should be read as references to the cited sources; DUB.SAR's programming semantics remain an original design.

---

## 36. The Tablet Archive (*é-dub-ba-a*)

### 36.1 Conceptual Model

DUB.SAR programs operate within a computational environment coupled with a local, persistent **Tablet Archive** (the scribal house of tablets, *é-dub-ba-a*). 

The archive is **not** a relational SQL database or generic CRUD key-value store exposed to the source language. Rather, it models persistent, versioned mathematical clay tablets carrying recorded scholarly knowledge, tables of constants, metrological lists, and program-inscribed experimental results.

The distinction is foundational:
- **Procedures and Recipes** contain executable algorithms.
- **Tablets** contain recorded mathematical knowledge and persistent data.

### 36.2 Persistent Tablets and Immutability

Persistent tablets stored in the archive are strictly **immutable**. Once inscribed, a tablet version can never be modified in place.

Every persistent tablet possesses:
- **Tablet Identity**: A unique identifier or name (e.g. `"reciprocals"`, `"solar-observations"`).
- **Monotonic Versioning**: An integer version (`v1`, `v2`, `...`) incremented automatically upon each new inscription.
- **Content Checksum**: A deterministic SHA-256 digest computed from canonical key-value serialization.
- **Colophon and Provenance Metadata**: Recording the tablet title, kind, historical tags, lineage (`copied-from`, `derived-from`), timestamp, and inscribing agent.

When a program consults a tablet without an explicit version:
```text
consult tablet "reciprocals"
```
the runtime resolves the highest available version. Pinning an exact historical version guarantees bit-for-bit computational reproducibility:
```text
consult tablet "reciprocals" version 1
```

### 36.3 Provenance and Lineage

Modifications to existing knowledge occur through derivation or copying, never in-place mutation. When a tablet is copied or derived:
- `copy tablet "T" as working W`: Creates a mutable working tablet pre-populated with all entries of `T`, recording `T` as its parent.
- `derive tablet "T" as working W`: Establishes a formal mathematical derivation lineage, recording source tablet identity and version.

When `W` is subsequently inscribed:
```text
inscribe W as tablet "T"
```
the archive creates version $N+1$ whose provenance points directly to version $N$.

### 36.4 Working Tablets (*kin* / 𒆥)

Working tablets (`kin` / `𒆥`) are mutable, temporary in-memory scratchpads. They allow high-performance computational modifications without disk I/O or database transaction overhead:
- `working W`: Declares an empty working tablet named `W`.
- `put V into W at K`: Inserts or sets key $K$ to value $V$.
- `replace entry K in W with V`: Replaces the value at key $K$.
- `remove entry K from W`: Deletes key $K$ from the working tablet.
- `K take entry from W`: Retrieves entry for key $K$.
- `seek entry in W nearest K`: Finds entry whose key is closest to $K$.

Working tablets that are not explicitly inscribed before execution ends evaporate upon program termination.

### 36.5 Inscription (*sar* / 𒁾𒊬)

Explicit inscription is the sole mechanism by which working tablets become persistent:
```text
inscribe W as tablet "target-name"
```
Inscription is strictly atomic: either the new tablet version and its entries are committed in full to the archive, or the operation fails completely, leaving existing versions unmodified.

### 36.6 Exact Value Preservation

All tablet entries preserve DUB.SAR's exact arithmetic guarantees. Entries are serialized using canonical exact representations:
- **Rationals**: Stored as exact numerator and denominator integers without decimal or floating-point rounding.
- **Quantities**: Preserved as exact rational value and dimension vector / canonical unit.
- **Strings and Determinations**: Serialized preserving field order, typing, and precision.

### 36.7 Standard Scholarly Archive ("Scribal Archive 1")

Every new DUB.SAR archive automatically initializes with standard scholarly reference tablets:
1. `reciprocals`: Standard Old Babylonian reciprocal pairs ($2 \to 0;30$, $3 \to 0;20$, $4 \to 0;15$, $5 \to 0;12$, $6 \to 0;10$, $8 \to 0;07,30$, etc.).
2. `common-fractions`: Exact sexagesimal representations of fundamental fractions ($1/2, 1/3, 2/3, 1/4, 3/4, 1/5, 5/6$).
3. `squares`: Exact integer squares for integers $1$ through $60$.
4. `cubes`: Exact integer cubes for integers $1$ through $30$.
5. `square-roots`: Documented rational approximations and exact integer roots.
6. `powers`: Powers of fundamental bases (powers of $2$ and $60$).
7. `basic-metrology`: Attested conversion factors for length, area, and capacity.
8. `basic-geometry`: Geometric coefficients (e.g. circle constant approximations).
9. `ea-nasir-shipment`: Structured shipment record of copper ingots inspired by tablet UET V 72 (British Museum BM 131236), recording promised and delivered quantities, quality ratings, and transaction metadata.

Each tablet carries explicit historical provenance tags: `attested` (historically attested in cuneiform corpus), `reconstructed`, or `modern`.

### 36.8 Dual-Mode Syntax Examples

#### Canonical Cuneiform Mode

```text
𒂊𒁹

    𒅆 𒁾 "reciprocals"

    reciprocal-of-7 :
        7
        pad 𒋫 reciprocals

    𒆥 observations

    observations
        10
        42
        𒃻

    𒁾 observations 𒁶 "observations"

𒅗𒁹

    reciprocal-of-7
```

#### Scholar Mode

```text
problem

    consult tablet "reciprocals"

    reciprocal-of-7 :
        7
        take entry from reciprocals

    working observations

    put 42 into observations at 10

    inscribe observations as tablet "observations"

result

    reciprocal-of-7
```

### 36.9 Developer Tooling and Inspection

Outside source execution, the `dubsar archive` CLI suite allows scholars and developers to inspect and manage the archive:
- `dubsar archive list`: Enumerate all tablets with current version, entry count, and metadata.
- `dubsar archive show <name> [--version V]`: Display tablet contents and colophon.
- `dubsar archive history <name>`: Trace complete version lineage and parent links.
- `dubsar archive export [--out file.json]`: Export archive to a deterministic canonical JSON bundle.
- `dubsar archive import <file.json>`: Safely import tablets into an archive.
- `dubsar archive render <name> [--style text|tablet|svg] [-o output]`: Render tablet layout as an ASCII/Unicode clay-style grid or vector SVG artwork.

---

## 37. Tablet-Oriented Data Model (Sequences, Tables, and Structured Data)

### 37.1 The Fundamental Abstraction

In DUB.SAR, structured mathematical data is represented through a unified **tablet-oriented data model**:

> **A tablet is an inscribed mathematical data object containing identifiable entries.**

The language does not introduce generic arrays, vectors, hashes, or relational tables under borrowed names. Instead, whether persistent in the archive or mutable in active working memory, data objects are conceptualized as clay tablets carrying inscribed mathematical entries.

### 37.2 The Three Shapes of Tablets

Every tablet belongs to one of three mathematical shapes:

1. **Sequence (`shape: sequence`)**:
   - Ordered, contiguous mathematical entries keyed by non-negative integers ($0, 1, 2, \dots, N-1$).
   - Models numerical sequences, polynomials, coefficients, time-series observations, and vector coordinate tuples.
   - Initialized with an optional allocated length: `working signal of length 1024`.
   - Supports auto-indexing append operations: `append val to signal` / `signal val 𒈭`.

2. **Mathematical Table (`shape: table`)**:
   - Sparse or discrete associative mappings keyed by arbitrary exact mathematical keys (integers, sexagesimal rationals, strings, or dimensioned quantities).
   - Models reciprocal tables, multiplication tables, squares, square roots, astronomical ephemerides, and metrological lookup tables.
   - Entries are placed at exact keys: `put 0;30 into recips at 2` / `recips 2 0;30 𒃻`.

3. **Structured Tablet (`shape: structured`)**:
   - Named fields or record-like structured entries.
   - Models physical entity records, administrative shipments, astronomical bodies, and compound problem parameters.
   - Initialized with inline field definitions:
     ```text
     working planet:
         mass : 100
         radius : 20
     ```

### 37.3 First-Class Tablet Operations

DUB.SAR provides first-class tablet operations in both prefix (Scholar Mode) and postfix (Canonical Cuneiform Mode) styles:

| Operation | Scholar Mode (Prefix) | Canonical Cuneiform (Postfix) | Description |
| :--- | :--- | :--- | :--- |
| **Creation** | `working W [of length N] [:]` | `working W [of length N] [:]` | Declares a mutable working tablet. |
| **Retrieval** | `take entry K from T` | `T K 𒋗` | Retrieves entry with key $K$. Raises `DubSarEntryNotFoundError` if absent. |
| **Insertion** | `put V into W at K` | `W K V 𒃻` | Inserts or overwrites entry $K$ in working tablet $W$. |
| **Append** | `append V to W` | `W V 𒈭` | Appends $V$ at the next sequential non-negative integer key. |
| **Length** | `length of T` | `T 𒁍` | Evaluates to the exact integer count of entries in tablet $T$. |
| **Removal** | `remove entry K from W` | `W K remove` | Deletes entry $K$ from working tablet $W$. |
| **Seek First** | `first from T` | `T first` | Retrieves the value of the earliest entry by sorted key order. |
| **Seek Last** | `last from T` | `T last` | Retrieves the value of the latest entry by sorted key order. |
| **Seek Nearest**| `seek entry nearest X in T` | `T X 𒊑` | Finds the entry whose numeric key is closest to target $X$. |
| **Iteration** | `consider entries of T:` | `consider entries of T:` | Iterates each entry, binding the entry value to `entry` (or `v`). |
| **Keyed Iter** | `consider K, V of T:` | `consider K, V of T:` | Iterates each key-value pair in tablet $T$. |
| **Inscription**| `inscribe tablet W [as T]` | `𒁹𒀀 W [as T]` | Persists working tablet $W$ as an immutable archive tablet version. |

### 37.4 Immutability Guarantee

Persistent archive tablets are strictly immutable. Any attempt to modify, append to, or remove entries from a persistent tablet raises `DubSarImmutableTabletError` (error alias `ImmutableTablet`):
```text
consult tablet "reciprocals"
append 5 to reciprocals   # ERROR: DubSarImmutableTabletError: persistent tablets are immutable
```
To modify existing data, a program must create a mutable working copy using `derive tablet "reciprocals" as working my_recips` or `copy tablet "reciprocals" as working my_recips`.

### 37.5 Entry Lookup Semantics

Looking up an entry with `take entry K from T` (or `T K 𒋗`) requires the entry to exist. If the key is not present in the tablet, evaluation halts with `DubSarEntryNotFoundError` (error alias `EntryNotFound`):
```text
consult tablet "reciprocals"
v : take entry 99 from reciprocals   # ERROR: DubSarEntryNotFoundError: Entry 99 not found
```
For approximate mathematical tables, programs use `seek entry nearest target in T` to locate the closest entry without raising an error.
