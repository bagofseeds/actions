# `test.yaml`

Run pytest in a target repository.

## Highlights

- installs `pytest`
- installs the project with `pip install -e .`
- supports extra requirements and pytest arguments

## Example

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test.yaml@main
    with:
      requirements-file: "requirements-test.txt"
      pytest-args: "-q"
```
