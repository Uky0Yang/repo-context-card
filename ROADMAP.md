# Roadmap

## Near Term

Implemented in v0.2.0: read-only `--check`, portable saved cards and a pre-commit hook.

- Add TOML configuration
- Add richer command detection for uv, poetry, pnpm, bun, make, just, and task
- Published to [PyPI](https://pypi.org/project/repo-context-card/0.2.0/) as v0.2.0

## Mid Term

- Add optional Git metadata summary
- Add safe README excerpt support
- Add monorepo package detection
- Add Mermaid architecture summary from directory structure

## Long Term

- Add context budget profiles for Codex, Claude Code, Cursor, Copilot, and Gemini CLI
- Add generated `AGENTS.md` starter mode
- Add GitHub Action wrapper

## Non-Goals

- No default model calls
- No default network calls
- No indexing database
- No hidden background daemon
