from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import os
from typing import Iterable


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "target",
    ".next",
    ".turbo",
    "coverage",
}

IMPORTANT_FILES = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "Dockerfile",
    "docker-compose.yml",
    ".github/workflows",
)

LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".h": "C/C++",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".md": "Markdown",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".json": "JSON",
}


@dataclass
class FileEntry:
    path: str
    size: int

    def to_dict(self) -> dict:
        return {"path": self.path, "size": self.size}


@dataclass
class RepoContext:
    root: str
    name: str
    files_scanned: int
    total_bytes: int
    languages: dict[str, int] = field(default_factory=dict)
    important_files: list[str] = field(default_factory=list)
    suggested_commands: list[str] = field(default_factory=list)
    tree: list[str] = field(default_factory=list)
    largest_files: list[FileEntry] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "root": self.root,
            "name": self.name,
            "files_scanned": self.files_scanned,
            "total_bytes": self.total_bytes,
            "languages": self.languages,
            "important_files": self.important_files,
            "suggested_commands": self.suggested_commands,
            "tree": self.tree,
            "largest_files": [entry.to_dict() for entry in self.largest_files],
        }


def scan_repo(root: Path, max_files: int = 200, max_tree_entries: int = 80) -> RepoContext:
    root = root.resolve()
    files = list(iter_files(root, max_files=max_files))
    language_counts: dict[str, int] = {}
    important = find_important_files(root, files)
    total_bytes = 0
    largest: list[FileEntry] = []

    for file in files:
        relative = file.relative_to(root).as_posix()
        size = safe_size(file)
        total_bytes += size
        largest.append(FileEntry(relative, size))
        language = LANGUAGE_EXTENSIONS.get(file.suffix.lower())
        if language:
            language_counts[language] = language_counts.get(language, 0) + 1

    largest = sorted(largest, key=lambda item: (-item.size, item.path))[:10]

    return RepoContext(
        root=str(root),
        name=root.name,
        files_scanned=len(files),
        total_bytes=total_bytes,
        languages=dict(sorted(language_counts.items(), key=lambda item: (-item[1], item[0]))),
        important_files=important,
        suggested_commands=suggest_commands(root),
        tree=build_tree(root, files, max_entries=max_tree_entries),
        largest_files=largest,
    )


def iter_files(root: Path, max_files: int) -> Iterable[Path]:
    count = 0
    for current_root, dirs, files in os.walk(root):
        dirs[:] = sorted(directory for directory in dirs if directory not in IGNORE_DIRS)
        for name in sorted(files):
            path = Path(current_root) / name
            if should_ignore_file(path):
                continue
            yield path
            count += 1
            if count >= max_files:
                return


def should_ignore_file(path: Path) -> bool:
    name = path.name
    if name.endswith((".pyc", ".pyo", ".log", ".tmp")):
        return True
    if name in {".DS_Store", "Thumbs.db"}:
        return True
    return False


def safe_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def find_important_files(root: Path, files: list[Path]) -> list[str]:
    relatives = {file.relative_to(root).as_posix() for file in files}
    important: list[str] = []
    for item in IMPORTANT_FILES:
        if item.endswith("/workflows"):
            if any(path.startswith(".github/workflows/") for path in relatives):
                important.append(item)
        elif item in relatives:
            important.append(item)
    return important


def suggest_commands(root: Path) -> list[str]:
    commands: list[str] = []
    if (root / "package.json").exists():
        commands.extend(read_package_scripts(root / "package.json"))
    if (root / "pyproject.toml").exists():
        commands.append("python -m pip install -e .")
        commands.append("python -m unittest discover -s tests")
    elif (root / "requirements.txt").exists():
        commands.append("python -m pip install -r requirements.txt")
    if (root / "Cargo.toml").exists():
        commands.extend(["cargo test", "cargo clippy"])
    if (root / "go.mod").exists():
        commands.extend(["go test ./...", "go vet ./..."])
    return dedupe(commands)[:10]


def read_package_scripts(package_json: Path) -> list[str]:
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["npm install"]
    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return ["npm install"]

    commands = ["npm install"]
    for name in ("lint", "test", "typecheck", "build", "dev"):
        if name in scripts:
            commands.append(f"npm run {name}")
    return commands


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output


def build_tree(root: Path, files: list[Path], max_entries: int) -> list[str]:
    entries = sorted(file.relative_to(root).as_posix() for file in files)
    if len(entries) <= max_entries:
        return entries
    return entries[:max_entries] + [f"... {len(entries) - max_entries} more files"]
