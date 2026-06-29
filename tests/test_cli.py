from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from repo_context_card.cli import main


class CliTests(unittest.TestCase):
    def test_writes_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "CONTEXT_CARD.md"
            (root / "README.md").write_text("# Demo", encoding="utf-8")

            self.assertEqual(main([str(root), "--output", str(output)]), 0)

            self.assertTrue(output.exists())
            self.assertIn("# Context Card:", output.read_text(encoding="utf-8"))

    def test_writes_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "context-card.json"
            (root / "main.py").write_text("print('ok')", encoding="utf-8")

            self.assertEqual(main([str(root), "--format", "json", "--output", str(output)]), 0)

            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["files_scanned"], 1)
            self.assertEqual(data["languages"]["Python"], 1)


if __name__ == "__main__":
    unittest.main()
