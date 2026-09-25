# CLI Reference

The `dubsar` command-line tool executes, compiles, formats, and renders DUB.SAR tablets.

---

## Commands

### `dubsar run`
Executes a tablet file:

```bash
dubsar run <file.dub> [--backend={ast,vm,native}] [--input=<val>] [--archive=<db_path>]
```

- `--backend=ast`: Reference AST interpreter (default).
- `--backend=vm`: Stack-oriented bytecode virtual machine.
- `--backend=native`: Ahead-of-time compiled native machine binary.
- `--input=<val>`: Preset input value for interactive `ask` expressions.
- `--archive=<db_path>`: Path to SQLite archive file.

### `dubsar compile`
Compiles a tablet to target output:

```bash
dubsar compile <file.dub> -o <output_file> --target={c,native,shared,llvm,wasm}
```

- `--target=c`: Generates standalone C99 source.
- `--target=native`: Compiles native executable.
- `--target=shared`: Compiles dynamic shared library (`.so` / `.dylib`).
- `--target=llvm`: Emits textual LLVM IR (`.ll`).
- `--target=wasm`: Emits WebAssembly Text format (`.wat`).

### `dubsar fmt`
Formats tablet source code cleanly according to scribal indentation conventions.

### `dubsar render`
Renders an authentic visual representation of a clay tablet as an SVG image or terminal frame:

```bash
dubsar render <file.dub> -o tablet.svg
```
