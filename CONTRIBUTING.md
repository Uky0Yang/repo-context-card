# Contributing

Thanks for helping improve `repo-context-card`.

## Good Contributions

- Better command detection for common project types
- More useful summaries without making output noisy
- Tests for real-world repository layouts
- Documentation examples for agent workflows
- CI and pre-commit examples

## Before Opening a PR

Run:

```bash
python -m unittest discover -s tests
python -m repo_context_card . --output CONTEXT_CARD.md
```

If your change updates scanner behavior, add tests.

## Rule of Thumb

This tool should stay small, deterministic, and safe to run in CI. Avoid model calls, network calls, or project-specific assumptions in the default path.
