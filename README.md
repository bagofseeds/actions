# bagofseeds/actions

Reusable GitHub Actions workflows adapted from [`neuroscales/abczarr`](https://github.com/neuroscales/abczarr).

## Reusable workflows

### `/.github/workflows/test.yaml` (pytest)

Runs pytest in a target repository.

- **workflow_call** inputs:
  - `requirements-file`: path to a requirements file (can be any name/path)
  - `python-version`, `tag`, `pytest-args`, `working-directory`
- **workflow_dispatch** extras:
  - `pip-dependencies`: comma-separated list (`pkg1,pkg2,./localpkg`)

Notes:
- Installs `pytest`
- Installs the current project (`pip install -e <working-directory>`)
- Installs dependencies from `requirements-file` when provided

Example (`workflow_call`):

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test.yaml@main
    with:
      python-version: "3.12"
      requirements-file: "requirements-test.txt"
      pytest-args: "-q"
```

### `/.github/workflows/test-matrix.yaml` (pytest matrix)

Runs `test.yaml` for Python `3.8` and latest (`3.x`).

Example (`workflow_call`):

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test-matrix.yaml@main
    with:
      requirements-file: "requirements-test.txt"
```

### `/.github/workflows/lint.yaml`

Generic lint runner with configurable command.

- **workflow_call**: pass `requirements-file`
- **workflow_dispatch**: optional `pip-dependencies` (comma-separated)

### `/.github/workflows/coverage.yaml`

Runs `pytest --cov=...` and uploads `coverage.xml`.

- **workflow_call**: pass `requirements-file`
- **workflow_dispatch**: optional `pip-dependencies` (comma-separated)

## Publish workflows (repository-specific)

Added from the reference repo:

- `/.github/workflows/publish-pypi.yaml`
- `/.github/workflows/test-and-publish.yaml`
- `/.github/workflows/publish-on-release.yaml`

These can be called, but are usually **repo-specific** because they depend on:
- package metadata/build layout
- repository secrets/tokens
- release policy

To adapt in another repo:
1. Create repository secrets for `PYPI_TOKEN` and `TEST_PYPI_TOKEN`.
2. Ensure package build works with `python -m build`.
3. Call `test-and-publish.yaml` from your repo and pass the right `requirements-file` for tests.
4. Prefer pinning this repo by tag/SHA in `uses:`.

## Zensical docs workflow

Added:

- `/.github/workflows/doc.yaml`

This workflow builds docs (`zensical build --clean` by default) and deploys to GitHub Pages.

Can it be called from another repo?
- **Yes**, via `workflow_call`.
- But the caller repository must have Pages enabled and allow `pages: write` + `id-token: write` permissions.
- The caller must also provide a valid docs requirements file and build command/path if defaults do not match.

Example (`workflow_call`):

```yaml
jobs:
  docs:
    uses: bagofseeds/actions/.github/workflows/doc.yaml@main
    with:
      docs-requirements-file: "docs/requirements.txt"
      build-command: "zensical build --clean"
      site-path: "site"
```
