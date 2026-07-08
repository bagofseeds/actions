# bagofseeds/actions

Reusable GitHub Actions workflows for testing, linting, docs, and publishing.

## Included workflows

- [`test.yaml`](test.md) — run pytest
- [`test-matrix.yaml`](test-matrix.md) — run pytest across Python versions
- [`lint.yaml`](lint.md) — run a configurable lint command
- [`coverage.yaml`](coverage.md) — run pytest with coverage
- [`doc.yaml`](doc.md) — build and deploy docs
- [`publish-pypi.yaml`](publish-pypi.md) — publish to PyPI or TestPyPI
- [`test-and-publish.yaml`](test-and-publish.md) — test first, then publish
- [`publish-on-release.yaml`](publish-on-release.md) — release-driven publish flow
