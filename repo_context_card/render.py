from __future__ import annotations

import json

from .scanner import RepoContext


def render_markdown(context: RepoContext) -> str:
    lines = [
        f"# Context Card: {context.name}",
        "",
        "A compact, deterministic repository summary for AI coding agents.",
        "",
        "## Summary",
        "",
        f"- Root: `{context.root}`",
        f"- Files scanned: `{context.files_scanned}`",
        f"- Total scanned bytes: `{context.total_bytes}`",
        "",
    ]

    if context.languages:
        lines.extend(["## Languages", ""])
        for language, count in context.languages.items():
            lines.append(f"- {language}: {count} file(s)")
        lines.append("")

    if context.important_files:
        lines.extend(["## Important Files", ""])
        for file in context.important_files:
            lines.append(f"- `{file}`")
        lines.append("")

    if context.suggested_commands:
        lines.extend(["## Suggested Commands", ""])
        for command in context.suggested_commands:
            lines.append(f"- `{command}`")
        lines.append("")

    if context.tree:
        lines.extend(["## File Map", ""])
        for entry in context.tree:
            lines.append(f"- `{entry}`")
        lines.append("")

    if context.largest_files:
        lines.extend(["## Largest Scanned Files", ""])
        for entry in context.largest_files:
            lines.append(f"- `{entry.path}` ({entry.size} bytes)")
        lines.append("")

    lines.extend(
        [
            "## Agent Notes",
            "",
            "- Read the project README and any agent instruction files before editing.",
            "- Prefer the suggested commands when validating changes.",
            "- Treat this file as a generated summary; refresh it after meaningful structural changes.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_json(context: RepoContext) -> str:
    return json.dumps(context.to_dict(), indent=2, ensure_ascii=False) + "\n"
