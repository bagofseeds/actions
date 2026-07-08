# `lint.yaml`

Run a configurable lint command.

## Highlights

- defaults to `ruff check .`
- supports custom requirements and extra pip dependencies
- skips missing requirements files with a warning

## Example

```yaml
jobs:
  lint:
    uses: bagofseeds/actions/.github/workflows/lint.yaml@main
    with:
      requirements-file: "requirements-lint.txt"
      lint-command: "ruff check --select=E,W ."
```
