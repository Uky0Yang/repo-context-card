from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from repo_context_card.render import render_json, render_markdown
from repo_context_card.scanner import scan_repo


class ScannerTests(unittest.TestCase):
    def test_scans_languages_and_important_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Agent", encoding="utf-8")
            (root / "app.py").write_text("print('hi')", encoding="utf-8")
            (root / "web.ts").write_text("export const ok = true", encoding="utf-8")

            context = scan_repo(root)

            self.assertEqual(context.languages["Markdown"], 2)
            self.assertEqual(context.languages["Python"], 1)
            self.assertEqual(context.languages["TypeScript"], 1)
            self.assertIn("README.md", context.important_files)
            self.assertIn("AGENTS.md", context.important_files)

    def test_suggests_package_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                json.dumps({"scripts": {"test": "vitest", "build": "tsc", "lint": "eslint ."}}),
                encoding="utf-8",
            )

            context = scan_repo(root)

            self.assertEqual(context.suggested_commands[:4], ["npm install", "npm run lint", "npm run test", "npm run build"])

    def test_render_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
            (root / "demo.py").write_text("x = 1", encoding="utf-8")

            context = scan_repo(root)
            markdown = render_markdown(context)
            data = json.loads(render_json(context))

            self.assertIn("# Context Card:", markdown)
            self.assertEqual(data["files_scanned"], 2)
            self.assertIn("python -m pip install -e .", data["suggested_commands"])
