from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from reliability_lab.capstone import _write_html


class CapstoneTests(unittest.TestCase):
    def test_html_escapes_scenario_names(self) -> None:
        report: dict[str, object] = {
            "parallel_exact_match": True,
            "speedup": 2.0,
            "scenarios": [
                {
                    "name": "<unsafe>",
                    "mean_availability": 0.99,
                    "p05_availability": 0.98,
                    "ci95_low": 0.98,
                    "ci95_high": 1.0,
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.html"
            _write_html(report, output)
            text = output.read_text(encoding="utf-8")
        self.assertIn("&lt;unsafe&gt;", text)
        self.assertNotIn("<unsafe>", text)

    def test_capstone_cli_rejects_nonpositive_runs(self) -> None:
        from reliability_lab import capstone

        with patch("sys.argv", ["capstone", "--simulator", "fake", "--runs", "0"]):
            with self.assertRaises(SystemExit):
                capstone.main()


if __name__ == "__main__":
    unittest.main()
