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
    best-cycle := nearest(100)
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
| `𒁾𒊬` | dub-sar | procedure declaration |
| `𒅗𒁹` | ka-diš | result section |
| `𒈬` | mu | year/unit symbol |
| `𒌓` | ud | day/unit symbol |
| `𒌗` | iti | month/unit symbol |
| `𒍣` | zi | addition verb |
| `𒋫` | ta | subtraction verb |
| `𒊭` | ša | multiplication verb |
| `𒉌` | ni | division verb |
| `𒄀` | gi | bounded repetition |
| `𒂊𒀀` | e-a | conditional |
| `𒉡𒂊𒀀` | nu-e-a | alternative branch |
| `𒄑` | ĝeš | return |
| `𒁹𒀀` | diš-a | output |
| `𒀀𒁹` | a-diš | input |
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
tablet           ::= problem-section procedure-section* result-section ;

problem-section  ::= "𒂊𒁹" block ;
result-section   ::= "𒅗𒁹" block ;
procedure-section ::= procedure ;

procedure        ::= "𒁾𒊬" identifier "(" parameters? ")" ":" block ;
parameters       ::= parameter ("," parameter)* ;
parameter        ::= identifier ;

block            ::= NEWLINE INDENT statement+ DEDENT ;

statement        ::= declaration
                   | assignment
                   | expression-statement
                   | conditional
                   | repetition
                   | return-statement
                   | output-statement
                   | input-expression
                   | expression ;

declaration      ::= identifier ":" expression unit? ;
assignment       ::= identifier ":=" expression
                   | identifier ("," identifier)+ ":=" expression-list ;
expression-list  ::= expression ("," expression)+ ;

conditional      ::= "𒂊𒀀" expression ":" block alternative? ;
alternative      ::= "𒉡𒂊𒀀" ":" block ;

repetition       ::= "𒄀" identifier range ":" block ;
range            ::= expression
                   | expression "𒌗" expression ;

return-statement ::= "𒄑" expression ("," expression)* ;
output-statement ::= "𒁹𒀀" expression ;
input-expression ::= "𒀀𒁹" "(" string ")" ;

expression       ::= comparison ;
comparison       ::= sum (comparison-op sum)* ;
sum              ::= product (("+"|"-"|"𒍣"|"𒋫") product)* ;
product          ::= power (("*"|"/"|"%"|"𒊭"|"𒉌") power)* ;
power            ::= unary ("**" unary)? ;
unary            ::= ("-"|"𒉡")? primary ;
primary          ::= number quantity-unit?
                   | identifier
                   | string
                   | call
                   | "(" expression ")" ;
quantity-unit    ::= unit ;
unit             ::= identifier | cuneiform-unit ;
call             ::= identifier "(" arguments? ")" ;
arguments        ::= expression ("," expression)* ;
comparison-op    ::= "=="|"!="|"<"|"<="|">"|">=" ;
identifier       ::= cuneiform-identifier|ascii-identifier ;
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

### 7.2 Derived quantities

```text
fraction := 𒈬 - 365 𒌓
```

uses `:=` to establish a derived quantity.

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

Compared quantities MUST be dimensionally compatible.

Comparisons yield an internal Boolean value used for control flow.

---

## 11. Conditions

Native form:

```text
𒂊𒀀 error < best:
    best := error
```

Scholar/ASCII alias:

```text
if error < best:
    best := error
```

Alternative branch:

```text
𒉡𒂊𒀀:
    ...
```

or ASCII `else:`.

Booleans are primarily control values. DUB.SAR 1.0 does not require Boolean variables as a core mathematical abstraction.

---

## 12. Repetition

DUB.SAR uses **bounded mathematical repetition**, not an unrestricted `while` loop.

Single-bound form:

```text
𒄀 cycle 1000:
    ...
```

means `cycle = 1, 2, ..., 1000`.

Explicit-range form:

```text
𒄀 cycle 1 𒌗 1000:
    ...
```

The upper bound is inclusive.

A repetition MUST be finite. Implementations MUST reject a statically negative count where it cannot be given a meaningful range interpretation.

---

## 13. Procedures

A procedure is a reusable mathematical recipe.

Canonical form:

```text
𒁾𒊬 leap-rule(solar, limit):
    ...
    𒄑 result
```

A procedure may return one or more values. Multiple values form a finite **tablet-result tuple**.

Return syntax:

```text
𒄑 a, b, c
```

Call syntax:

```text
a, b, c := leap-rule(solar, 1000)
```

All returned elements MUST be explicit and ordered.

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

### Input

```text
𒈬 := 𒀀𒁹("solar year in days")
```

The runtime accepts an exact integer, sexagesimal value, or decimal input and immediately converts it to the exact rational representation.

### Output

```text
𒁹𒀀 "cycle:"
𒁹𒀀 cycle
```

Strings are Unicode strings.

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
candidate := whole + leaps / cycle
```

may lower to:

```text
LOAD whole
LOAD leaps
LOAD cycle
DIV
ADD
STORE candidate
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

Reference command:

```text
dubsar run tablet.dub
dubsar check tablet.dub
dubsar compile tablet.dub --target=bytecode
dubsar compile tablet.dub --target=wasm
dubsar compile tablet.dub --target=native
dubsar transliterate tablet.dub
dubsar cuneiform tablet.dub
dubsar render tablet.dub --style=tablet
```

`render` is a presentation feature; case lines, tablet borders and similar visual features do not affect program semantics.

Unicode documents cuneiform case ruling and similar lines as formatting rather than syntax, supporting this separation.

---

## 25. Tablet rendering

A DUB.SAR implementation SHOULD be able to render source as:

- Unicode text;
- transliterated scholar text;
- SVG;
- PNG;
- PDF;
- clay-tablet-style artwork.

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
𒁾𒊬 next-leap(accumulator, cycle, leaps):

    new-accumulator := accumulator + leaps

    𒂊𒀀 new-accumulator >= cycle:

        new-accumulator := new-accumulator - cycle
        𒄑 new-accumulator, 1

    𒄑 new-accumulator, 0
```

A caller can invoke this once per calendar year. This distributes leap days as evenly as possible over the cycle.

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

- `:=`;
- indentation-sensitive blocks;
- procedures with tuple returns;
- compiler IR;
- arbitrary-precision runtime representation;
- module system and CLI.

A DUB.SAR implementation or manual MUST never present category-C syntax as evidence about ancient Sumerian programming.

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
