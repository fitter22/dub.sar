# Compiler Architecture

The DUB.SAR compilation pipeline bridges high-level Mesopotamian mathematical statements and hardware-level execution.

---

## Pipeline Overview

```
Source Code (.dub)
       │
       ▼
 [Lexer & Parser]
       │
       ▼
   Typed AST
       │
       ▼
[Semantic Analyzer]
       │
       ├──► Reference AST Interpreter (Stage 1)
       │
       ▼
  Semantic IR (CR-011 / CR-024)
       │
       ├──► Stack Bytecode IR & VM (Stage 2)
       │
       ├──► WebAssembly Text Codegen (Stage 3)
       │
       ▼
 Native C99 & LLVM IR Codegen (Stage 4)
       │
       ▼
 Host Compiler (clang / gcc)
       │
       ▼
 Machine Executable / Shared Library
```

---

## Layers

1. **Frontend**: Lexical tokenizer and recursive-descent parser producing a unified Abstract Syntax Tree.
2. **Semantic Analysis**: Scope validation, compile-time unit dimensional checking, and procedure arity validation.
3. **Semantic IR**: Lowers language structures into canonical mathematical verbs (`ESTABLISH`, `TAKE`, `ADD`, `RETAIN`, `DETERMINE`).
4. **Code Generation**: Emits target-specific representations (C99, LLVM, WebAssembly, or Stack Bytecode).
