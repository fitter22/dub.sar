# Deploying the website

The site is static output from `website/`. Cloudflare Pages project `dub-sar` serves it. Production comes from the `main` branch. This repository does not deploy the site yet: the workflow builds it, and a later change can upload `website/dist`.

The documentation site stays on GitHub Pages at <https://fitter22.github.io/dub.sar/>, published by `.github/workflows/deploy-docs.yml`. Do not point that Pages source at this website, and do not turn on Cloudflare's Git integration for `dub-sar`. A connected Cloudflare build would compile on Cloudflare's side and fight the GitHub Actions build.

## Project contract

- Pages project name: `dub-sar`
- Production branch: `main`
- Free hostname: the `pages.dev` name assigned to that project (intended `dub-sar.pages.dev`, plus any suffix Cloudflare adds)
- GitHub environment: `cloudflare-pages`
- Secrets on that environment: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`
- Variable on that environment: `CLOUDFLARE_PAGES_PROJECT=dub-sar`
- No Worker, D1 database, or KV namespace

Build locally or in CI:

```bash
cd website
npm ci
npm run build
```

The publish directory is `website/dist`. It contains `index.html`, `catalog.json`, and `runtime/` (wheel, runner, sample WAT, and sample WASM when `wat2wasm` is installed).

A manual upload, after the API token and account id are exported in the shell and not written into the repo, is:

```bash
npx wrangler pages deploy website/dist --project-name=dub-sar
```

Run that from the repository root. Preview deployments stay enabled in the Pages project. Production deploys should use the `cloudflare-pages` environment and only `main`.

## Future GitHub Actions deploy

Add this job to `.github/workflows/website.yml` when deployment is wanted. It is not part of the current workflow.

```yaml
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: cloudflare-pages
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.9"
      - run: python -m pip install --upgrade pip setuptools wheel
      - run: sudo apt-get update && sudo apt-get install -y wabt
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: npm
          cache-dependency-path: website/package-lock.json
      - working-directory: website
        run: npm ci
      - working-directory: website
        run: npm run build
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy website/dist --project-name=${{ vars.CLOUDFLARE_PAGES_PROJECT }}
```

Pull-request previews can use the same upload with `--branch=${{ github.head_ref }}` from a workflow that has access to the environment. Keep production limited to `main`.
