# Agent Instructions

## Purpose

Maintain `repo-context-card`, a dependency-free Python CLI that generates compact repository context cards for AI coding agents.

## Scope

These instructions apply to code, tests, documentation, and GitHub workflow files in this repository.

## Commands

Run these checks before publishing:

```bash
python -m unittest discover -s tests
python -m repo_context_card . --output CONTEXT_CARD.md
```

## Safety

- Do not add model calls to the default scanning path.
- Do not add network calls to the default scanning path.
- Do not include secrets, environment values, or file contents in generated output by default.
- Keep output deterministic so CI diffs are meaningful.

## Style

- Prefer standard-library Python.
- Keep summaries compact and easy to scan.
- Add tests for scanner behavior changes.
