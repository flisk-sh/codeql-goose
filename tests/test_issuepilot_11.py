import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "goose_analyze.py"


def run_cli(root, output):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), "--output", str(output)],
        capture_output=True,
        text=True,
    )


class ScanRootTests(unittest.TestCase):
    def test_missing_or_non_directory_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            regular_file = parent / "regular-file"
            regular_file.touch()
            for root in (parent / "missing", regular_file):
                with self.subTest(root=root):
                    output = parent / "report.sarif"
                    result = run_cli(root, output)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn(str(root), result.stderr)
                    self.assertFalse(output.exists())

    def test_empty_directory_warns_and_writes_sarif(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "report.sarif"
            result = run_cli(root, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("warning: no files matched", result.stderr.lower())
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["runs"][0]["results"], [])
