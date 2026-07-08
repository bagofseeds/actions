# `coverage.yaml`

Run pytest with coverage and upload `coverage.xml`.

## Highlights

- runs `pytest --cov`
- supports custom coverage targets and pytest args

## Example

```yaml
jobs:
  coverage:
    uses: bagofseeds/actions/.github/workflows/coverage.yaml@main
    with:
      requirements-file: "requirements-test.txt"
      coverage-target: "mypackage"
```
