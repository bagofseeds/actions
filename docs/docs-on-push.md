# `docs-on-push.yaml`

Trigger docs deployment on push and delegate to `docs.yaml`.

## Highlights

- triggered by pushes to `main` and `master`
- calls the reusable docs workflow

## Example

```yaml
jobs:
  docs:
    uses: bagofseeds/actions/.github/workflows/docs-on-push.yaml@main
```
