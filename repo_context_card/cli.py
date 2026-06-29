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
    parser.add_argument("--max-files", type=int, default=200, help="Maximum number of files to scan.")
    parser.add_argument("--max-tree-entries", type=int, default=80, help="Maximum file map entries to include.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    context = scan_repo(Path(args.path), max_files=args.max_files, max_tree_entries=args.max_tree_entries)
    output = render_json(context) if args.format == "json" else render_markdown(context)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8", newline="\n")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
