# bagofseeds/actions

---

## Reusable workflows

### `test.yaml` — Run pytest

Runs pytest in a target repository. Automatically installs `pytest` and, when
present, the current project (`pip install -e .`). Missing requirements files
are skipped with a warning.

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tag` | `string` | No | `""` | Commit / Branch / Tag / SHA to checkout |
| `python-version` | `string` | No | `"3.x"` | Python version to use |
| `requirements-file` | `string` | No | `""` | Path to a requirements file to install (any filename) |
| `pytest-args` | `string` | No | `""` | Extra arguments passed to pytest |
| `working-directory` | `string` | No | `"."` | Directory where pytest should run |
| `pip-dependencies` | `string` | No | `""` | Comma-separated pip packages (**workflow_dispatch only**) |

#### Example

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test.yaml@main
    with:
      python-version: "3.12"
      requirements-file: "requirements-test.txt"
      pytest-args: "-q"
```

---

### `test-matrix.yaml` — Run pytest on multiple Python versions

Calls `test.yaml` across a matrix of Python `3.8` and latest (`3.x`).

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tag` | `string` | No | `""` | Commit / Branch / Tag / SHA to checkout |
| `requirements-file` | `string` | No | `""` | Path to a requirements file to install (any filename) |
| `pytest-args` | `string` | No | `""` | Extra arguments passed to pytest |
| `working-directory` | `string` | No | `"."` | Directory where pytest should run |

#### Example

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test-matrix.yaml@main
    with:
      requirements-file: "requirements-test.txt"
```

---

### `lint.yaml` — Run a lint command

Generic lint runner with a configurable command. Default command: `ruff check .`.
Missing requirements files are skipped with a warning.

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tag` | `string` | No | `""` | Commit / Branch / Tag / SHA to checkout |
| `python-version` | `string` | No | `"3.x"` | Python version to use |
| `requirements-file` | `string` | No | `""` | Path to a requirements file to install |
| `lint-command` | `string` | No | `"ruff check ."` | Command to execute for linting |
| `working-directory` | `string` | No | `"."` | Directory where lint command should run |
| `pip-dependencies` | `string` | No | `""` | Comma-separated pip packages (**workflow_dispatch only**) |

#### Example

```yaml
jobs:
  lint:
    uses: bagofseeds/actions/.github/workflows/lint.yaml@main
    with:
      requirements-file: "requirements-lint.txt"
      lint-command: "ruff check --select=E,W ."
```

---

### `coverage.yaml` — Run pytest with coverage

Runs `pytest --cov` and uploads `coverage.xml` as an artifact. Missing
requirements files are skipped with a warning.

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tag` | `string` | No | `""` | Commit / Branch / Tag / SHA to checkout |
| `python-version` | `string` | No | `"3.x"` | Python version to use |
| `requirements-file` | `string` | No | `""` | Path to a requirements file to install |
| `coverage-target` | `string` | No | `"."` | Package/path passed to `--cov` |
| `pytest-args` | `string` | No | `""` | Extra arguments passed to pytest |
| `working-directory` | `string` | No | `"."` | Directory where pytest should run |
| `pip-dependencies` | `string` | No | `""` | Comma-separated pip packages (**workflow_dispatch only**) |

#### Example

```yaml
jobs:
  coverage:
    uses: bagofseeds/actions/.github/workflows/coverage.yaml@main
    with:
      requirements-file: "requirements-test.txt"
      coverage-target: "mypackage"
```

---

### `doc.yaml` — Build and deploy docs

Builds documentation (default: `zensical build --clean`) and deploys to
GitHub Pages. Use `docs-on-push.yaml` for automatic push-triggered deploys.

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tag` | `string` | No | `""` | Commit / Branch / Tag / SHA to checkout |
| `python-version` | `string` | No | `"3.x"` | Python version to use |
| `docs-requirements-file` | `string` | No | `"docs/requirements.txt"` | Path to docs requirements file |
| `build-command` | `string` | No | `"zensical build --clean"` | Command that builds docs |
| `site-path` | `string` | No | `"site"` | Path of generated static site to publish |

#### Permissions required by caller

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

#### Cross-repo callability

This workflow **can** be called from another repo via `workflow_call`. The
caller must have GitHub Pages enabled and grant the permissions listed above.

#### Example

```yaml
jobs:
  docs:
    uses: bagofseeds/actions/.github/workflows/doc.yaml@main
    with:
      docs-requirements-file: "docs/requirements.txt"
      build-command: "zensical build --clean"
      site-path: "site"
```

### `docs-on-push.yaml` — Trigger docs deploys on push

Wraps `doc.yaml` for `push` events on `main` and `master`.

#### Example

No inputs; add it as a workflow in the target repository:

```yaml
jobs:
  docs:
    uses: bagofseeds/actions/.github/workflows/docs-on-push.yaml@main
```

---

## Publish workflows

These workflows handle PyPI publishing. They can be called cross-repo but are
typically **repository-specific** because they depend on package build layout
and repository secrets.

### `publish-pypi.yaml` — Publish to PyPI

Builds and publishes a Python package to PyPI or TestPyPI.

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `python-version` | `string` | No | `"3.x"` | Python version to use |
| `tag` | `string` | No | `""` | Commit / Branch / Tag / SHA to checkout |
| `test` | `boolean` | No | `false` | Publish to TestPyPI instead of PyPI |

#### Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `password` | Yes | PyPI or TestPyPI API token |

---

### `test-and-publish.yaml` — Test then publish

Optionally runs the test matrix, then publishes to TestPyPI and/or PyPI.

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tag` | `string` | No | `""` | Commit / Branch / Tag / SHA to checkout |
| `test` | `boolean` | No | `true` | Run tests before publishing |
| `publish` | `string` / `choice` | No | `"none"` | Publish target: `"none"`, `"pypi"`, `"test"`, or `"test+pypi"` |
| `python-version` | `string` | No | `"3.x"` | Python version for publish job |
| `requirements-file` | `string` | No | `""` | Path to requirements file used by the test workflow |

#### Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `PYPI_TOKEN` | Yes | PyPI API token |
| `TEST_PYPI_TOKEN` | Yes | TestPyPI API token |

---

### `publish-on-release.yaml` — Publish on GitHub release

Triggered automatically when a GitHub release is published. Runs the full
test suite then publishes to both TestPyPI and PyPI.

No inputs — uses `secrets: inherit` to pass tokens from the repository.

---

## Adapting publish workflows for another repository

1. Copy or call the publish workflows from this repo.
2. Create repository secrets: `PYPI_TOKEN` and `TEST_PYPI_TOKEN`.
3. Ensure `python -m build` works for your package.
4. Pin this repo by tag or SHA in `uses:`.

```yaml
jobs:
  release:
    uses: bagofseeds/actions/.github/workflows/test-and-publish.yaml@main
    with:
      test: true
      publish: "test+pypi"
      requirements-file: "requirements-test.txt"
    secrets:
      PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
      TEST_PYPI_TOKEN: ${{ secrets.TEST_PYPI_TOKEN }}
```
