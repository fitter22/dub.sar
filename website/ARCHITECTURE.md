# Website architecture

The public site is a static page plus one in-browser runtime. A visitor can read the landing page, edit a tablet, and execute it locally. Normal execution does not call a backend.

## What runs a tablet

The playground uses one stable runtime: CPython compiled to WebAssembly, loaded through [Pyodide 0.26.4](https://cdn.jsdelivr.net/pyodide/v0.26.4/full/) from jsDelivr. After that runtime is up, the page installs a wheel built from this repository and evaluates `website/runtime/runner.py`.

`execute(source, backend, stdin)` parses the tablet and runs either:

- the reference interpreter (`Interpreter.run`)
- the bytecode machine (`Compiler` then `VirtualMachine.execute`)

Both engines are the ones shipped in the `dubsar` package. The page does not reimplement the language in JavaScript, and it does not compile a fresh WebAssembly module for every tablet.

This is the stable-runtime approach. A second approach already exists in the language: `dubsar compile --target=wasm` emits WebAssembly text, and `wat2wasm` turns that text into a binary. The website build still produces that artifact for the 3-4-5 meter tablet (`sample.wat` and, when `wat2wasm` is on `PATH`, `sample.wasm`). That module demonstrates the compiler backend. The playground does not use it to run arbitrary source, because a per-program module would not cover the interpreter's full behavior (archive lookup, input, diagnostics) without a second implementation.

The native C backend is not available in the browser.

## Loading

Pyodide, the wheel, and the runner stay unloaded during the first paint. The page starts the download when the playground scrolls into view, when Try a tablet is used, or when a comparison tablet is opened. The worker keeps the runtime after the first load.

`website/scripts/prepare_assets.py` writes the files the worker fetches:

- `catalog.json`, parsed from `examples/*.dub` (one catalog, the repository examples)
- `runtime/dubsar-<version>-*.whl`
- `runtime/runner.py`
- `runtime/manifest.json`, including the package version shown in the UI
- `runtime/sample.wat` and `runtime/sample.wasm`

## Editor

CodeMirror 6 provides the editor: line numbers, four-space indentation, bracket and quote closing, undo, and a small highlighter for scholar keywords, comments (`#` and `𒑰`), strings, sexagesimal numerals, and cuneiform runs. The typeface stack is Noto Sans, then Noto Sans Cuneiform, so Latin stays Latin and signs still have a font.

## Limits and diagnostics

The page thread abandons a run after 8 seconds by terminating the worker and creating a new one on the next attempt. That bound is what stops a tablet that does not return. Syntax, name, unit, and other `DubSarError` failures come back as the same diagnostic text the command-line tool prints, with a line and a column. The editor moves the cursor there.

Examples in the catalog are the repository tablets. Their results are the language's own results for that source and version. The version string in the status line is `dubsar.__version__` from the wheel that was just installed.

## What this deploy does not include

There is no application server, Worker, database, or key-value store for a normal run. The archive inside the runtime is the in-memory school archive the package already seeds. Pyodide is loaded from a public CDN; a build that must run without that network would need those files mirrored. The documentation site on GitHub Pages is a separate origin and is not produced by this project.
