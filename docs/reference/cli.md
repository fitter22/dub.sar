# CLI Reference

The `dubsar` command-line utility provides commands to run, check, compile, format, transliterate, and render DUB.SAR tablets, as well as administer persistent tablet archives.

---

## 1. `dubsar run`

Executes a DUB.SAR tablet source file:

```bash
dubsar run <file.dub> [options]
```

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--backend` | `vm`, `ast`, `native` | `vm` | Execution backend: stack-oriented bytecode virtual machine (`vm`), reference AST interpreter (`ast`), or ahead-of-time compiled binary (`native`). |
| `--input` | `<val>` | `None` | Preset numeric or string input value to supply to interactive `ask` / `𒀀𒁹` expressions. |
| `--format` | `canonical`, `sexagesimal`, `decimal` | `canonical` | Number presentation style for inscribed results. |
| `--mode` | `auto`, `tablet`, `scholar`, `mixed` | `auto` | Enforces or auto-detects source language mode. |
| `--archive` | `<path>` | `None` | Path to persistent SQLite tablet archive database (`.db`). |

---

## 2. `dubsar check`

Performs lexical, grammatical, and semantic type/dimensional validation without execution:

```bash
dubsar check <file.dub> [--mode={auto,tablet,scholar,mixed}]
```

---

## 3. `dubsar compile`

Compiles a tablet into intermediate representation, bytecode, WebAssembly, C99, or native binary:

```bash
dubsar compile <file.dub> [options]
```

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--target` | `bytecode`, `wasm`, `wat`, `ir`, `json`, `native`, `c`, `llvm` (or `ll`), `shared` (or `dylib`, `so`) | `bytecode` | Target artifact output format. |
| `-o`, `--output` | `<file>` | `None` | Destination output file path (defaults to stdout if omitted). |
| `--opt-level` | `-O0`, `-O1`, `-O2`, `-O3`, `-Os` | `-O3` | Optimization level passed to the native backend C compiler. |
| `--mode` | `auto`, `tablet`, `scholar`, `mixed` | `auto` | Source language mode. |

### Compilation Targets

- `bytecode`: Serialized DUB.SAR bytecode stream for the virtual machine.
- `wasm` / `wat`: WebAssembly binary (`.wasm`) or WebAssembly Text format (`.wat`).
- `ir`: DUB.SAR Intermediate Representation text.
- `json`: JSON representation of tablet AST and metadata.
- `c`: Standalone ANSI C99 source code with exact 64-bit rational runtime arithmetic.
- `native`: AOT-compiled native machine binary linked against the C99 runtime.
- `shared` / `dylib` / `so`: Dynamically linked shared library.
- `llvm` / `ll`: LLVM textual Intermediate Representation.

---

## 4. `dubsar format`

Formats and canonicalizes tablet source code according to scribal layout and indentation rules:

```bash
dubsar format <file.dub> [options]
```

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--mode` | `auto`, `tablet`, `scholar` | `auto` | Target formatting style: authentic cuneiform Tablet Mode, Latin Scholar Mode, or auto-detected. |
| `-i`, `--inplace` | flag | `false` | Overwrites the input source file in-place with formatted output. |
| `-o`, `--output` | `<file>` | `None` | Writes formatted code to a target file rather than stdout. |

---

## 5. `dubsar transliterate`

Converts authentic cuneiform Tablet Mode source into readable Latin Scholar Mode source:

```bash
dubsar transliterate <file.dub> [-o <output_file>]
```

---

## 6. `dubsar cuneiform`

Converts Latin Scholar Mode source code into canonical cuneiform Tablet Mode inscriptions:

```bash
dubsar cuneiform <file.dub> [-o <output_file>]
```

---

## 7. `dubsar render`

Generates an authentic visual rendering of the clay tablet as an SVG image or terminal frame:

```bash
dubsar render <file.dub> [options]
```

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--style` | `tablet`, `svg`, `text` | `tablet` | Rendering style: high-resolution clay tablet SVG (`tablet` or `svg`) or monospace terminal clay box (`text`). |
| `--strip-comments` | flag | `false` | Omits comment lines (`#` and `𒑰`) from the rendered tablet artwork. |
| `-o`, `--output` | `<file>` | `None` | Output destination file path. |

---

## 8. `dubsar archive`

Inspects and administers persistent clay tablet archives:

```bash
dubsar archive list [--namespace=<ns>] [--archive=<db_path>]
dubsar archive show <tablet_name> [--version=<ver>] [--archive=<db_path>]
dubsar archive history <tablet_name> [--archive=<db_path>]
dubsar archive export [-o <output.json>] [--archive=<db_path>]
```
