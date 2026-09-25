# Compiler & Toolchain

DUB.SAR features an extensible multi-tier compiler pipeline translating mathematical tablets into machine-executable formats.

---

## Compiler Topics

- **[Using the Native Compiler](using-native.md)**: Ahead-of-time compilation to C99, native machine binaries, shared libraries, and LLVM IR.
- **[Architecture & Pipeline](architecture.md)**: Frontend lexical analysis, AST lowering, Semantic IR, and codegen.
- **[Virtual Machine](vm.md)**: Bytecode design, stack instructions, environment frames, and VM interpreter.
- **[WebAssembly](wasm.md)**: Compiling tablets to standard `.wasm` modules with zero external dependencies.
