import csv
import random
import tempfile
import unittest
from pathlib import Path

from reliability_lab.analytics import summarize
from reliability_lab.reporting import compare_scenarios, render_html


class PropertyTests(unittest.TestCase):
    def test_generated_valid_rows_preserve_summary_invariants(self) -> None:
        generator = random.Random(42)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "generated.csv"
            rows = []
            for run_id in range(1, 201):
                downtime = generator.uniform(0.0, 720.0)
                uptime = 720.0 - downtime
                rows.append(
                    {
                        "run_id": run_id,
                        "uptime_hours": uptime,
                        "downtime_hours": downtime,
                        "failures": generator.randint(0, 20),
                        "availability": uptime / 720.0,
                    }
                )
            with path.open("w", newline="", encoding="utf-8") as target:
                writer = csv.DictWriter(target, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

            result = summarize(path)
            self.assertEqual(result["runs"], 200)
            self.assertGreaterEqual(result["mean_availability"], 0.0)
            self.assertLessEqual(result["mean_availability"], 1.0)
            self.assertGreaterEqual(result["availability_stddev"], 0.0)
            self.assertGreaterEqual(result["p95_downtime_hours"], 0.0)
            self.assertLessEqual(result["p95_downtime_hours"], 720.0)

    def test_scenario_names_are_html_escaped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            csv_path = root / "valid.csv"
            csv_path.write_text(
                "run_id,uptime_hours,downtime_hours,failures,availability\n1,700,20,1,0.972222\n",
                encoding="utf-8",
            )
            rows = compare_scenarios({"<script>alert(1)</script>": csv_path, "safe": csv_path})
            report = root / "report.html"
            render_html(rows, report)
            content = report.read_text(encoding="utf-8")
            self.assertNotIn("<script>alert(1)</script>", content)
            self.assertIn("&lt;script&gt;", content)


if __name__ == "__main__":
    unittest.main()
