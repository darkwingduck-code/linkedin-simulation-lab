import csv
import tempfile
import unittest
from pathlib import Path

from reliability_lab.analytics import summarize


class AnalyticsTests(unittest.TestCase):
    def test_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "simulation.csv"
            with path.open("w", newline="", encoding="utf-8") as target:
                writer = csv.DictWriter(
                    target,
                    fieldnames=["run_id", "uptime_hours", "downtime_hours", "failures", "availability"],
                )
                writer.writeheader()
                writer.writerows([
                    {"run_id": 1, "uptime_hours": 700, "downtime_hours": 20, "failures": 2, "availability": 0.97},
                    {"run_id": 2, "uptime_hours": 710, "downtime_hours": 10, "failures": 1, "availability": 0.99},
                ])
            result = summarize(path)
            self.assertEqual(result["runs"], 2)
            self.assertAlmostEqual(result["mean_availability"], 0.98)
            self.assertEqual(result["max_failures"], 2)


if __name__ == "__main__":
    unittest.main()

