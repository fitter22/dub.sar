# WebAssembly Compilation

DUB.SAR can compile mathematical tablets directly to WebAssembly Text (`.wat`), which can be assembled into standard binary `.wasm` modules using standard toolchains (such as `wat2wasm`) with zero external runtime dependencies.

---

## Architecture

- **Stack Operations**: Maps DUB.SAR stack expressions directly to Wasm value stack operations.
- **Embedded Rational Arithmetic**: Emits internal Wasm functions for 64-bit integer rational addition, subtraction, multiplication, division, and GCD reduction.
- **Pure Zero-Dependency Modules**: Generated Wasm modules run in standard web browsers or serverless Wasm runtimes (Wasmer, Wasmtime).

---

## Compiling to WebAssembly Text

```bash
dubsar compile tablet.dub -o tablet.wat --target=wasm

# Assemble into binary .wasm using WABT wat2wasm:
wat2wasm tablet.wat -o tablet.wasm
```
