# `test-matrix.yaml`

Run pytest on multiple Python versions.

## Highlights

- runs the shared test workflow
- targets Python `3.8` (the floor), `3.10` and the latest `3.x`
- runs `3.8` on `ubuntu-24.04`, the newest runner image with a 3.8 build;
  the others run on `ubuntu-latest`
- one failing version does not cancel the others (`fail-fast: false`)

## Example

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test-matrix.yaml@main
    with:
      requirements-file: "requirements-test.txt"
```
