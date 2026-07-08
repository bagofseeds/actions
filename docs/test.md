# `test.yaml`

Run pytest in a target repository.

## Highlights

- installs `pytest`
- installs the project with `pip install -e .` when project metadata exists
- supports extra requirements and pytest arguments
- skips missing requirements files with a warning

## Example

```yaml
jobs:
  tests:
    uses: bagofseeds/actions/.github/workflows/test.yaml@main
    with:
      requirements-file: "requirements-test.txt"
      pytest-args: "-q"
```
