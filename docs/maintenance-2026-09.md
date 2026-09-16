# Keep context cards current (v0.2.0)

```bash
repo-context-card . --output CONTEXT_CARD.md
repo-context-card . --output CONTEXT_CARD.md --check
```

The second command returns 0 for a current card, 1 for a missing/stale card, or 2 for
invalid input/I/O. It never writes. The output file is excluded from the scan, so
generation does not change its own input. Saved cards use "." as their root so they
can be checked in another checkout. Keep the same format and scan limits when checking.

```yaml
repos:
  - repo: https://github.com/Uky0Yang/repo-context-card
    rev: v0.2.0
    hooks:
      - id: repo-context-card
```

Refresh and commit the card after changing the repository. The default 200-file limit
is still a bounded summary, not a full repository index.
