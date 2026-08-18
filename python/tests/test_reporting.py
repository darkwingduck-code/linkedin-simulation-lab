import json
import tempfile
import unittest
from pathlib import Path

from reliability_lab.reporting import compare_scenarios, render_html, write_comparison_json

CSV_HEADER = "run_id,uptime_hours,downtime_hours,failures,availability\n"


class ReportingTests(unittest.TestCase):
    def test_comparison_outputs_versioned_json_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline.csv"
            stressed = root / "stressed.csv"
            baseline.write_text(CSV_HEADER + "1,710,10,1,0.986111\n", encoding="utf-8")
            stressed.write_text(CSV_HEADER + "1,680,40,4,0.944444\n", encoding="utf-8")
            rows = compare_scenarios({"baseline": baseline, "stressed": stressed})
            json_path = root / "comparison.json"
            html_path = root / "comparison.html"
            write_comparison_json(rows, json_path)
            render_html(rows, html_path)

            payload = json.loads(json_path.read_text(encoding="utf-8"))
            report = html_path.read_text(encoding="utf-8")
            self.assertEqual(payload["schema_version"], "1.0")
            self.assertEqual(len(payload["scenarios"]), 2)
            self.assertIn("baseline", report)
            self.assertIn("stressed", report)
            self.assertGreaterEqual(report.count("<svg"), 2)

    def test_at_least_two_scenarios_are_required(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least two"):
            compare_scenarios({"only": "unused.csv"})


if __name__ == "__main__":
    unittest.main()
