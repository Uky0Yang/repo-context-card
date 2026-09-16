import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from repo_context_card.cli import main


class CheckTests(unittest.TestCase):
    def test_generated_card_is_stable_and_check_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            root = Path(directory)
            (root / 'README.md').write_text('# Demo\n', encoding='utf-8')
            card = root / 'CONTEXT_CARD.md'
            args = [str(root), '--output', str(card)]
            self.assertEqual(main(args), 0)
            original = card.read_bytes()
            self.assertEqual(main(args + ['--check']), 0)
            (root / 'new.py').write_text('print(1)\n', encoding='utf-8')
            self.assertEqual(main(args + ['--check']), 1)
            self.assertEqual(card.read_bytes(), original)

    def test_missing_card_is_stale_without_creation(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            card = Path(directory) / 'card.json'
            self.assertEqual(main([directory, '--format', 'json', '--output', str(card), '--check']), 1)
            self.assertFalse(card.exists())

    def test_json_card_is_portable_and_stable(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            root = Path(directory)
            (root / 'README.md').write_text('# Portable\n', encoding='utf-8')
            card = root / 'card.json'
            args = [directory, '--format', 'json', '--output', str(card)]
            self.assertEqual(main(args), 0)
            self.assertEqual(json.loads(card.read_text(encoding='utf-8'))['root'], '.')
            self.assertEqual(main(args + ['--check']), 0)
