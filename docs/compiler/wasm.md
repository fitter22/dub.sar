# WebAssembly Compilation

DUB.SAR can compile mathematical tablets directly to WebAssembly Text (`.wat`) and standard binary `.wasm` modules with zero external dependencies.

---

## Architecture

- **Stack Operations**: Maps DUB.SAR stack expressions directly to Wasm value stack operations.
- **Embedded Rational Arithmetic**: Emits internal Wasm functions for arbitrary precision 64-bit integer rational addition, multiplication, division, and GCD reduction.
- **Pure Zero-Dependency Modules**: Generated Wasm modules run in standard web browsers or serverless Wasm runtimes (Wasmer, Wasmtime).

---

## Compiling to Wasm

```bash
dubsar compile tablet.dub -o tablet.wat --target=wasm
```
