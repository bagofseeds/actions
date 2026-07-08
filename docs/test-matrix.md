# `test-matrix.yaml`

Run pytest on multiple Python versions.

## Highlights

- runs the shared test workflow
- currently targets Python `3.8` and latest `3.x`

## Example

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test-matrix.yaml@main
    with:
      requirements-file: "requirements-test.txt"
```
