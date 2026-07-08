# `doc.yaml`

Build docs with Zensical and publish them to GitHub Pages.

For push-triggered deploys, use [`docs-on-push.yaml`](docs-on-push.md).

## Highlights

- installs docs dependencies from `docs/requirements.txt`
- builds the site with `zensical build --clean`
- uploads the generated `site/` directory to Pages

## Example

```yaml
jobs:
  docs:
    uses: bagofseeds/actions/.github/workflows/doc.yaml@main
    with:
      docs-requirements-file: "docs/requirements.txt"
      build-command: "zensical build --clean"
      site-path: "site"
```
