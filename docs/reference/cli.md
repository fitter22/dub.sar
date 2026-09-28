# CLI Reference

The `dubsar` command-line utility provides commands to run, check, compile, format, transliterate, and render DUB.SAR tablets, as well as administer persistent tablet archives.

---

## 1. `dubsar run`

Executes a DUB.SAR tablet source file using the specified execution engine.

### Syntax

```bash
dubsar run <file.dub> [options]
```

### Semantics

- Parses and semantically checks the source tablet before execution.
- Evaluates the tablet using one of three execution backends:
    - `vm`: Stack-oriented bytecode virtual machine (default, recommended).
    - `ast`: Recursive AST tree-walking interpreter (reference implementation).
    - `native`: Ahead-of-time compiled native machine binary linked against the C99 rational runtime.
- Automatically connects to an adjacent SQLite tablet archive database (`<stem>.tablets.db`) unless an explicit database path is provided via `--archive`.
- Formats numeric results according to `--format` (`canonical`, `sexagesimal`, or `decimal`).

### Exit Codes

| Exit Code | Meaning |
| :---: | :--- |
| `0` | Execution completed successfully. |
| `1` | Source file not found, syntax error, semantic type error, or runtime exception. |
| `2` | Unexpected internal interpreter or system error. |

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--backend` | `vm`, `ast`, `native` | `vm` | Execution engine backend. |
| `--input` | `<string>` | `None` | Preset numeric or string input value to supply to interactive `ask` / `𒀀𒁹` expressions. |
| `--format` | `canonical`, `sexagesimal`, `decimal` | `canonical` | Number presentation style for inscribed results. |
| `--mode` | `auto`, `tablet`, `scholar`, `mixed` | `auto` | Enforces or auto-detects source language mode. |
| `--archive` | `<path>` | `None` | Path to persistent SQLite tablet archive database (`.db`). Defaults to `<stem>.tablets.db`. |

### Practical Examples

Execute a tablet using the default stack VM backend:

```bash
dubsar run tablet.dub
```

Execute using the AST reference interpreter with decimal number formatting:

```bash
dubsar run tablet.dub --backend=ast --format=decimal
```

Supply a preset input value to an interactive tablet:

```bash
dubsar run survey.dub --input="45"
```

Execute a tablet connected to a shared archive database:

```bash
dubsar run tablet.dub --archive=central_records.db
```

Compile and execute ahead-of-time with the native backend:

```bash
dubsar run tablet.dub --backend=native
```

### Links

- [Language Reference](language.md)
- [Execution Model Specification](../specification/index.md)
- [Diagnostics & Errors](diagnostics.md)

---

## 2. `dubsar check`

Performs static lexical analysis, grammar parsing, and semantic validation without executing the tablet.

### Syntax

```bash
dubsar check <file.dub> [options]
```

### Semantics

- Verifies tablet structure, problem blocks, calculation pipelines, and result assertions.
- Enforces static type safety, dimensional consistency of metrological units, and scope rules.
- Validates persistent archive references against available schemas.
- Produces no side effects and does not modify archive databases or files.

### Exit Codes

| Exit Code | Meaning |
| :---: | :--- |
| `0` | Tablet parsed and verified successfully with no errors. |
| `1` | Syntax error, dimensional unit conflict, undefined variable, or semantic validation failure. |

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--mode` | `auto`, `tablet`, `scholar`, `mixed` | `auto` | Enforces specific source mode during parsing and validation. |

### Practical Examples

Validate a tablet file:

```bash
dubsar check tablet.dub
```

Output on success:

```text
[OK] Tablet 'tablet.dub' parsed and verified successfully (Mode: scholar).
```

Enforce authentic cuneiform Tablet Mode during validation:

```bash
dubsar check tablet.dub --mode=tablet
```

### Links

- [Diagnostics & Errors](diagnostics.md)
- [DUB.SAR 1.0 Specification](../specification/index.md)
- [Units & Metrology](../guide/units.md)

---

## 3. `dubsar compile`

Compiles a DUB.SAR tablet into intermediate representation, bytecode, WebAssembly, C99 source, or native machine binaries.

### Syntax

```bash
dubsar compile <file.dub> [options]
```

### Semantics

- Generates target code based on `--target`:
    - `bytecode` / `ir`: Intermediate stack bytecode disassembly for the DUB.SAR VM.
    - `wasm` / `wat`: WebAssembly Text format (`.wat`) with 64-bit integer rational runtime.
    - `json`: Structured JSON serialization of the parsed AST and tablet metadata.
    - `c`: Standalone ANSI C99 source code with exact 64-bit rational arithmetic.
    - `native`: Standalone ahead-of-time compiled native machine executable binary.
    - `llvm` / `ll`: LLVM intermediate representation emitted via the C compiler backend.
    - `shared` / `dylib` / `so`: Dynamically linked shared object library.
- Textual targets (`bytecode`, `ir`, `wat`, `json`) print to stdout unless `-o` is specified.
- Native/C targets write to `<file_stem>.<ext>` or `<file_stem>` binary by default.

### Exit Codes

| Exit Code | Meaning |
| :---: | :--- |
| `0` | Compilation completed successfully. |
| `1` | Lexical, parsing, semantic, or compiler backend error. |

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--target` | `bytecode`, `wasm`, `wat`, `ir`, `json`, `native`, `c`, `llvm`, `ll`, `shared`, `dylib`, `so` | `bytecode` | Target compilation artifact format. |
| `-o`, `--output` | `<file>` | `None` | Output destination file path. |
| `--opt-level` | `-O0`, `-O1`, `-O2`, `-O3`, `-Os` | `-O3` | Optimization level passed to the native backend C compiler. |
| `--mode` | `auto`, `tablet`, `scholar`, `mixed` | `auto` | Enforces source language mode. |

### Practical Examples

Disassemble bytecode instructions to stdout:

```bash
dubsar compile tablet.dub
```

Compile to WebAssembly Text format:

```bash
dubsar compile tablet.dub --target=wat -o tablet.wat
```

Emit standalone ANSI C99 source code:

```bash
dubsar compile tablet.dub --target=c -o tablet.c
```

Compile directly to an optimized native machine binary:

```bash
dubsar compile tablet.dub --target=native -o tablet_bin
```

Export parsed AST to JSON:

```bash
dubsar compile tablet.dub --target=json -o ast.json
```

### Links

- [Compiler Overview](../compiler/index.md)
- [WebAssembly Guide](../compiler/wasm.md)
- [Compiler Architecture](../compiler/architecture.md)

---

## 4. `dubsar format`

Formats and canonicalizes tablet source code according to scribal layout and indentation rules.

### Syntax

```bash
dubsar format <file.dub> [options]
```

### Semantics

- Normalizes indentation, line spacing, and operator padding across problem, recipe, and result sections.
- Supports canonical target style transformation: convert between Latin Scholar Mode and authentic cuneiform Tablet Mode formatting.
- Can emit to stdout, save to a new file, or update the file in-place.

### Exit Codes

| Exit Code | Meaning |
| :---: | :--- |
| `0` | Source formatted successfully. |
| `1` | Parsing error encountered in source file. |

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--mode` | `auto`, `tablet`, `scholar` | `auto` | Canonical target style: Tablet cuneiform, Scholar Latin, or auto-detected. |
| `-i`, `--inplace` | flag | `false` | Overwrites the input source file in-place with formatted output. |
| `-o`, `--output` | `<file>` | `None` | Destination output file path. Defaults to printing to stdout. |

### Practical Examples

Format and print canonical code to stdout:

```bash
dubsar format tablet.dub
```

Format a tablet file in-place:

```bash
dubsar format tablet.dub -i
```

Canonicalize and save formatted output to a separate file:

```bash
dubsar format tablet.dub -o formatted_tablet.dub
```

Convert layout to Scholar Mode style during formatting:

```bash
dubsar format tablet.dub --mode=scholar -o tablet_scholar.dub
```

### Links

- [Source Modes](language.md#13-source-modes-scholar-tablet-and-mixed)
- [Source Modes Guide](../guide/source-modes.md)

---

## 5. `dubsar transliterate`

Converts authentic cuneiform Tablet Mode source into canonical Latin Scholar Mode text.

### Syntax

```bash
dubsar transliterate <file.dub> [options]
```

### Semantics

- Replaces Unicode cuneiform ideograms and syllabograms (`𒂊𒁹`, `𒅗𒁹`, `𒍣`, `𒋫`, `𒊭`, `𒉌`, etc.) with their canonical Latin equivalents (`problem`, `result`, `add`, `subtract`, `multiply`, `divide`, etc.).
- Converts cuneiform numeric signs (`𒁹`, `𒌋`, `𒌍`, etc.) into decimal or sexagesimal numbers.
- Preserves string literals exactly without transliterating their internal characters.

### Exit Codes

| Exit Code | Meaning |
| :---: | :--- |
| `0` | Transliteration completed successfully. |
| `1` | File read or processing error. |

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `-o`, `--output` | `<file>` | `None` | Output destination file path. Prints to stdout when omitted. |

### Practical Examples

Transliterate cuneiform tablet to stdout:

```bash
dubsar transliterate tablet_cuneiform.dub
```

Save transliterated Scholar Mode source to a new file:

```bash
dubsar transliterate tablet_cuneiform.dub -o tablet_scholar.dub
```

### Links

- [Source Modes](language.md#13-source-modes-scholar-tablet-and-mixed)
- [Cuneiform Signs Reference](cuneiform.md)
- [Lexical Vocabulary](language.md#14-lexical-vocabulary-sign-catalog)

---

## 6. `dubsar cuneiform`

Converts Latin Scholar Mode source code into authentic Mesopotamian cuneiform Tablet Mode inscriptions.

### Syntax

```bash
dubsar cuneiform <file.dub> [options]
```

### Semantics

- Maps Scholar Mode keywords (`problem`, `result`, `recipe`, `working`, `add`, `multiply`, etc.) to their canonical Unicode cuneiform signs (`𒂊𒁹`, `𒅗𒁹`, `𒁾𒊬`, `𒆥`, `𒍣`, `𒊭`, etc.).
- Converts integer numbers 1 through 59 into authentic cuneiform numeral glyphs (`𒁹`, `𒈫`, `𒌋`, `𒌍`, `𒐏`, `𒐐`, etc.).
- Preserves string literals and modern identifiers without corruption.

### Exit Codes

| Exit Code | Meaning |
| :---: | :--- |
| `0` | Cuneiform conversion completed successfully. |
| `1` | File read or processing error. |

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `-o`, `--output` | `<file>` | `None` | Output destination file path. Prints to stdout when omitted. |

### Practical Examples

Convert Scholar Mode code to cuneiform on stdout:

```bash
dubsar cuneiform tablet_scholar.dub
```

Write cuneiform output to a tablet file:

```bash
dubsar cuneiform tablet_scholar.dub -o tablet_cuneiform.dub
```

### Links

- [Cuneiform Signs Reference](cuneiform.md)
- [Source Modes](language.md#13-source-modes-scholar-tablet-and-mixed)

---

## 7. `dubsar render`

Generates an authentic visual presentation of the clay tablet as an SVG vector graphic or terminal text display.

### Syntax

```bash
dubsar render <file.dub> [options]
```

### Semantics

- In `tablet` or `svg` mode (default), generates a high-resolution Scalable Vector Graphics (`.svg`) rendering featuring warm clay gradients, realistic tablet bevels, surface fissures, and cuneiform typography.
- In `text` mode, generates a formatted monospace Unicode box frame suitable for terminal output or ASCII documentation.
- Comments (`#` and `𒑰`) can be stripped using `--strip-comments` to present a pristine inscribed tablet face.

### Exit Codes

| Exit Code | Meaning |
| :---: | :--- |
| `0` | Rendering completed successfully. |
| `1` | Source file or rendering error. |

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--style` | `tablet`, `svg`, `text` | `tablet` | Rendering presentation style: clay tablet SVG (`tablet` or `svg`) or monospace terminal box (`text`). |
| `--strip-comments` | flag | `false` | Omits comment lines (`#` and `𒑰`) from the rendered tablet artwork. |
| `-o`, `--output` | `<file>` | `None` | Destination output file path. Defaults to `<stem>_tablet.svg` for SVG style, or stdout for text style. |

### Practical Examples

Render a clay tablet SVG vector image:

```bash
dubsar render tablet.dub --style=svg -o tablet.svg
```

Display a terminal clay tablet box:

```bash
dubsar render tablet.dub --style=text
```

Render an SVG tablet without comments:

```bash
dubsar render tablet.dub --style=svg --strip-comments -o clean_tablet.svg
```

### Links

- [Language Reference](language.md)
- [Cuneiform Signs Reference](cuneiform.md)

---

## 8. `dubsar archive`

Inspects, queries, exports, and administers persistent clay tablet archives backed by SQLite.

### Syntax

```bash
dubsar archive <subcommand> [options]
```

### Exit Codes

| Exit Code | Meaning |
| :---: | :--- |
| `0` | Archive operation completed successfully. |
| `1` | Archive database error, tablet not found, or invalid schema. |

### Subcommands

#### `list`

Lists all tablets registered in the archive database, showing namespace, latest version, kind, and clay shape.

```bash
dubsar archive list [--namespace=<ns>] [--archive=<db_path>]
```

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--namespace` | `<string>` | `None` | Filter listed tablets by namespace prefix. |
| `--archive` | `<path>` | `archive.db` | Path to persistent SQLite archive database (`.db`). |

Example:

```bash
dubsar archive list --archive=treasury.db
```

Output:

```text
NAME                 NAMESPACE    VER   KIND           SHAPE     
-----------------------------------------------------------------
survey_2026          survey       2     administrative rectangular
lunar_cycle          astronomy    1     reference      pillow    
```

#### `show`

Displays the full metadata, classification tags, and inscribed key-value dictionary entries for a given tablet.

```bash
dubsar archive show <tablet_name> [--version=<ver>] [--archive=<db_path>]
```

| Argument / Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `<tablet_name>` | `<string>` | (required) | Identifier name of the tablet to inspect. |
| `--version` | `<int>` | `None` | Specific historical version number. When omitted, inspects the latest version. |
| `--archive` | `<path>` | `archive.db` | Path to SQLite archive database. |

Example:

```bash
dubsar archive show survey_2026 --archive=treasury.db
```

#### `history`

Displays the provenance and revision audit trail for a tablet across all saved versions.

```bash
dubsar archive history <tablet_name> [--archive=<db_path>]
```

| Argument / Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `<tablet_name>` | `<string>` | (required) | Identifier name of the tablet to trace. |
| `--archive` | `<path>` | `archive.db` | Path to SQLite archive database. |

Example:

```bash
dubsar archive history survey_2026 --archive=treasury.db
```

Output:

```text
History of 'survey_2026':
  v1 | root      | a1b2c3d4e5f6 | 2026-09-28T10:00:00 | dubsar
  v2 | parent v1 | f6e5d4c3b2a1 | 2026-09-28T11:30:00 | dubsar
```

#### `export`

Exports the entire archive or selected records to a JSON interchange format.

```bash
dubsar archive export [-o <output.json>] [--archive=<db_path>]
```

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `-o`, `--output` | `<file>` | `None` | Destination JSON file path. Prints to stdout when omitted. |
| `--archive` | `<path>` | `archive.db` | Path to SQLite archive database. |

Example:

```bash
dubsar archive export -o treasury_backup.json --archive=treasury.db
```

#### `import`

Imports tablet versions and entries from a JSON archive interchange file into the archive database.

```bash
dubsar archive import <file.json> [--archive=<db_path>]
```

| Argument / Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `<file.json>` | `<path>` | (required) | Path to JSON interchange file to import. |
| `--archive` | `<path>` | `archive.db` | Path to destination SQLite archive database. |

Example:

```bash
dubsar archive import treasury_backup.json --archive=treasury.db
```

#### `render`

Renders an archived tablet version in monospace text format or as high-resolution SVG clay tablet artwork.

```bash
dubsar archive render <tablet_name> [--version=<ver>] [--style=text|tablet|svg] [-o <output_file>] [--archive=<db_path>]
```

| Argument / Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `<tablet_name>` | `<string>` | (required) | Name of tablet to render. |
| `--version` | `<int>` | `None` | Tablet version to render. Defaults to latest version. |
| `--style` | `text`, `tablet`, `svg` | `text` | Presentation format: text table (`text`) or clay SVG (`tablet`/`svg`). |
| `-o`, `--output` | `<file>` | `None` | Destination output file path. Prints to stdout when omitted. |
| `--archive` | `<path>` | `archive.db` | Path to SQLite archive database. |

Example:

```bash
dubsar archive render survey_2026 --style=svg -o survey_tablet.svg --archive=treasury.db
```

### Links

- [Tablet Archive Operations](language.md#10-tablet-archive-operations)
- [DUB.SAR 1.0 Specification](../specification/index.md)
- [Tablet Archive Tutorial](../learn/archive.md)
