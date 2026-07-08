# bagofseeds/actions

Reusable, **generic** GitHub Actions workflows that can be called from other repositories.

This repository adapts reusable workflows from [`neuroscales/abczarr`](https://github.com/neuroscales/abczarr) and keeps only workflows that are broadly reusable across projects.

## Available reusable workflows

### 1) `test.yaml` — run pytest

Path: `/.github/workflows/test.yaml`

Key inputs:
- `python-version` (default: `3.x`)
- `tag` (optional ref to checkout)
- `pip-dependencies` (**newline-separated**, optional; supports any number of dependencies)
- `pytest-args` (optional)
- `working-directory` (default: `.`)

Example:

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test.yaml@main
    with:
      python-version: "3.12"
      pip-dependencies: |
        -e .
        .[test]
        numpy>=1.26
      pytest-args: "-q"
```

### 2) `test-matrix.yaml` — pytest on Python 3.8 + latest

Path: `/.github/workflows/test-matrix.yaml`

Runs the same test workflow on:
- `3.8`
- `3.x` (latest available stable Python on the runner)

Example:

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test-matrix.yaml@main
    with:
      pip-dependencies: |
        -e .
        .[test]
```

### 3) `lint.yaml` — run project-defined lint command

Path: `/.github/workflows/lint.yaml`

You provide dependencies and the lint command, so this stays project-agnostic.

Example:

```yaml
jobs:
  lint:
    uses: bagofseeds/actions/.github/workflows/lint.yaml@main
    with:
      pip-dependencies: |
        ruff
        codespell
      lint-command: "ruff check . && codespell ."
```

### 4) `coverage.yaml` — pytest coverage + upload artifact

Path: `/.github/workflows/coverage.yaml`

Runs `pytest --cov=...` and uploads `coverage.xml` as a workflow artifact.

Example:

```yaml
jobs:
  coverage:
    uses: bagofseeds/actions/.github/workflows/coverage.yaml@main
    with:
      pip-dependencies: |
        -e .
        .[test]
      coverage-target: "your_package"
```

## Workflows intentionally not adapted (and why)

Some workflows in `abczarr` are intentionally project/repository constrained:

- **PyPI publish workflows** (`publish-pypi.yaml`, `publish-on-release.yaml`, `test-and-publish.yaml`)
  - Restriction: require repository-specific secrets, package metadata, and release policy.
  - Workaround: keep publishing workflows in each target repository, and optionally call the reusable `test`/`coverage` workflows from this repo before publishing.

- **Docs deploy workflow** (`doc.yaml`)
  - Restriction: depends on project-specific documentation toolchain and site layout.
  - Workaround: define a repository-level docs workflow that installs project docs dependencies and optionally reuses generic setup/testing workflows from this repo.

## Notes

- These are **reusable workflows** (`workflow_call`), invoked via:
  `uses: bagofseeds/actions/.github/workflows/<workflow>.yaml@<ref>`
- Pin to tags/SHAs in production for better supply-chain safety.
