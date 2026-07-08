# `test-and-publish.yaml`

Run tests before publishing.

## Highlights

- can skip testing or publishing independently
- supports PyPI and TestPyPI targets

## Example

```yaml
jobs:
  release:
    uses: bagofseeds/actions/.github/workflows/test-and-publish.yaml@main
    with:
      test: true
      publish: "test+pypi"
      requirements-file: "requirements-test.txt"
```
