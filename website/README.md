# DUB.SAR website

Landing page and in-browser playground for DUB.SAR. The page is static. Tablets run in the visitor's browser through Pyodide and a wheel built from this repository.

The site is not deployed yet. See [DEPLOYMENT.md](DEPLOYMENT.md) for the Cloudflare Pages project and [ARCHITECTURE.md](ARCHITECTURE.md) for how execution works. The documentation site at <https://fitter22.github.io/dub.sar/> is separate.

## Requirements

- Python 3.9+
- `setuptools` and `wheel` (the asset script builds with `--no-build-isolation`)
- Node.js 20 or newer
- `wat2wasm` from [WABT](https://github.com/WebAssembly/wabt) if the build should emit `sample.wasm`

## Commands

From `website/`:

```bash
python3 -m pip install setuptools wheel
npm install
npm run dev
```

`npm run dev` refreshes the example catalog and the wheel, then starts Vite. `npm run build` typechecks and writes `dist/`.

Generated files under `public/catalog.json` and `public/runtime/` are local build output. Do not commit them.
