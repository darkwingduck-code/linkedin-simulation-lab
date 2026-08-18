import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from reliability_lab.reporting import compare_scenarios, render_html


class EndToEndTests(unittest.TestCase):
    def test_simulator_to_html_report(self) -> None:
        executable = os.environ.get("RELIABILITY_SIMULATOR")
        if not executable:
            self.skipTest("RELIABILITY_SIMULATOR is not configured")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scenarios: dict[str, Path] = {}
            for name, failure_rate in (("baseline", "0.0015"), ("stressed", "0.004")):
                csv_path = root / f"{name}.csv"
                json_path = root / f"{name}.json"
                subprocess.run(
                    [
                        executable,
                        "--output",
                        str(csv_path),
                        "--json-output",
                        str(json_path),
                        "--runs",
                        "100",
                        "--seed",
                        "42",
                        "--failure-rate",
                        failure_rate,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                payload = json.loads(json_path.read_text(encoding="utf-8"))
                self.assertEqual(payload["schema_version"], "1.0")
                self.assertEqual(len(payload["results"]), 100)
                scenarios[name] = csv_path

            rows = compare_scenarios(scenarios)
            report_path = root / "comparison.html"
            render_html(rows, report_path)
            report = report_path.read_text(encoding="utf-8")
            self.assertIn("Reliability Scenario Comparison", report)
            self.assertIn("baseline", report)
            self.assertIn("stressed", report)


if __name__ == "__main__":
    unittest.main()
