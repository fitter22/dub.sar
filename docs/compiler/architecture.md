# Compiler Architecture

The DUB.SAR compilation pipeline bridges high-level Mesopotamian mathematical statements and hardware-level execution.

---

## Pipeline Overview

```text
               .dub source (Tablet / Scholar / Mixed)
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │     Unicode Lexer     │ (Significant Indentation,
                     │  (dubsar/lexer.py)    │  Cuneiform Signs, Numerals)
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Recursive-Descent AST │ (Normative EBNF Grammar,
                     │  (dubsar/parser.py)   │  Unified AST Nodes)
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   Semantic Analyzer   │ (Lexical Scopes, Compile-Time Units,
                     │ (dubsar/semantic.py)  │  Determinations & Range Checks)
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │  DUB.SAR Semantic IR  │ (Mathematical Verbs: ESTABLISH,
                     │ (dubsar/semantic_ir.py)│  TAKE, POSTFIX, RETAIN, DETERMINE)
                     └───────────┬───────────┘
                                 │
                 ┌───────────────┼───────────────┬───────────────┐
                 │               │               │               │
                 ▼               ▼               ▼               ▼
        ┌────────────────┐┌─────────────┐┌───────────────┐┌───────────────┐
        │  AST Evaluator ││ Bytecode IR ││ WASM Compiler ││Native Compiler│
        │ (Interpreter)  ││ Compiler    ││ (dubsar/      ││ (dubsar/      │
        │                ││ (dubsar/    ││   wasm.py)    ││   native/)    │
        │                ││   ir.py)    ││               ││               │
        └────────────────┘└──────┬──────┘└───────────────┘└───────┬───────┘
                                 │                                │
                                 ▼                                ▼
                        ┌─────────────────┐              ┌─────────────────┐
                        │ Virtual Machine │              │Host C99/LLVM CC │
                        │ (dubsar/vm.py)  │              │ (clang / gcc)   │
                        └─────────────────┘              └────────┬────────┘
                                                                  │
                                               ┌──────────────────┼──────────────────┐
                                               ▼                  ▼                  ▼
                                       ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
                                       │Native Binary  │  │Textual LLVM IR│  │Shared Library │
                                       │(Mach-O / ELF) │  │    (.ll)      │  │(.dylib / .so) │
                                       └───────────────┘  └───────────────┘  └───────────────┘
```

---

## Compiler Targets

| Target | Status | Description |
| :--- | :--- | :--- |
| **Native Compiler** | **Complete** | AOT compilation to standalone binaries, textual LLVM IR, C99, and shared libraries with 128-bit hardware rational acceleration |
| **Reference AST Interpreter** | **Complete** | Full language support, exact arbitrary-precision rationals |
| **Stack Bytecode VM** | **Complete** | Stack IR, constant table, activation frames, determination ops |
| **Semantic IR** | **Complete** | Mathematical verbs layer (`ESTABLISH`, `TAKE`, `POSTFIX`, `RETAIN`, etc.) |
| **WebAssembly (.wat)** | **Complete** | Scalar-replaced determinations, bounded loops, 64-bit rational runtime |

---

## Pipeline Layers

1. **Frontend**: Unicode lexical tokenizer and recursive-descent parser producing a unified Abstract Syntax Tree across Tablet, Scholar, and Mixed modes.
2. **Semantic Analysis**: Lexical scope validation, compile-time unit dimensional checking, determinations, and domain range validation.
3. **Semantic IR**: Lowers language structures into canonical mathematical verbs (`ESTABLISH`, `TAKE`, `POSTFIX`, `RETAIN`, `DETERMINE`).
4. **Code Generation**: Emits target-specific representations (C99, LLVM, WebAssembly, or Stack Bytecode).
