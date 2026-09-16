from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__
from .render import render_json, render_markdown
from .scanner import scan_repo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repo-context-card",
        description="Generate compact repository context cards for AI coding agents.",
    )
    parser.add_argument("path", nargs="?", default=".", help="Repository or directory to scan.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format.")
    parser.add_argument("--output", "-o", help="Write output to a file instead of stdout.")
    parser.add_argument("--check", action="store_true", help="Exit 1 if --output is missing or stale; never write.")
    parser.add_argument("--max-files", type=int, default=200, help="Maximum number of files to scan.")
    parser.add_argument("--max-tree-entries", type=int, default=80, help="Maximum file map entries to include.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.check and not args.output:
        parser.error("--check requires --output")
    try:
        root = Path(args.path)
        if not root.is_dir():
            raise ValueError(f"not a directory: {root}")
        target = Path(args.output) if args.output else None
        context = scan_repo(root, max_files=args.max_files, max_tree_entries=args.max_tree_entries, exclude=target)
        if target:
            context.root = "."  # Committed cards must be portable across checkouts.
        output = render_json(context) if args.format == "json" else render_markdown(context)
        if args.check:
            current = target.read_text(encoding="utf-8") if target.exists() else None
            if current != output:
                print(f"Context card is missing or stale: {target}")
                return 1
        elif target:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8", newline="\n")
        else:
            print(output, end="")
    except (OSError, ValueError) as exc:
        print(f"repo-context-card: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
