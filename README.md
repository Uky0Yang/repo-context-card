# repo-context-card

Generate a compact repository context card for AI coding agents.

`repo-context-card` is a dependency-free Python CLI that scans a repository and emits a deterministic Markdown or JSON summary: important files, language mix, likely validation commands, a compact file map, and largest scanned files.

## Why

AI coding agents work better when they get the right context early. Recent high-growth developer tools are converging on context engineering, token reduction, agent skills, and repo memory. Many solutions are powerful but heavy.

This project is intentionally small: create a readable `CONTEXT_CARD.md` that any agent or human can inspect before editing a codebase.

## Install

From this repository:

```bash
python -m pip install -e .
```

Or run without installing:

```bash
python -m repo_context_card .
```

## Usage

Print Markdown to stdout:

```bash
repo-context-card .
```

Write a context card:

```bash
repo-context-card . --output CONTEXT_CARD.md
```

Write JSON:

```bash
repo-context-card . --format json --output context-card.json
```

Limit scanning:

```bash
repo-context-card . --max-files 150 --max-tree-entries 60
```

## What It Detects

- Important files such as `README.md`, `AGENTS.md`, `CLAUDE.md`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, and GitHub workflows
- Language counts by file extension
- Suggested commands for Python, Node, Rust, and Go projects
- Compact file map
- Largest scanned files
- Total scanned bytes

## Example

```text
# Context Card: my-project

## Summary

- Root: `/path/to/my-project`
- Files scanned: `42`
- Total scanned bytes: `118420`

## Languages

- Python: 12 file(s)
- Markdown: 4 file(s)

## Suggested Commands

- `python -m pip install -e .`
- `python -m unittest discover -s tests`
```

## CI Example

```yaml
name: Context card

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  context-card:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install -e .
      - run: repo-context-card . --output CONTEXT_CARD.md
      - run: test -s CONTEXT_CARD.md
```

## Design Principles

- No dependencies
- No model calls
- No network calls
- Deterministic output
- Safe for CI
- Useful to humans and agents

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests
python -m repo_context_card . --output CONTEXT_CARD.md
```

## Agent OSS Toolkit

This project is part of a small toolkit for building and launching agent-ready open-source repositories:

- [agent-repo-kit](https://github.com/Uky0Yang/agent-repo-kit): scaffold launch-ready, AI-agent-friendly repositories
- [oss-launch-check](https://github.com/Uky0Yang/oss-launch-check): audit whether a repository is ready to launch as open source
- [repo-context-card](https://github.com/Uky0Yang/repo-context-card): generate compact repository context cards for coding agents
- [agent-rules-lint](https://github.com/Uky0Yang/agent-rules-lint): lint AGENTS.md, CLAUDE.md, Cursor rules, and Copilot instructions
- [awesome-ai-agents-zh](https://github.com/Uky0Yang/awesome-ai-agents-zh): Chinese AI Agents / MCP / AI DevTools directory

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
