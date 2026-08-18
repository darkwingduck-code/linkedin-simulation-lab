import csv
import tempfile
import unittest
from pathlib import Path

from reliability_lab.analytics import summarize


class AnalyticsTests(unittest.TestCase):
    fieldnames = ["run_id", "uptime_hours", "downtime_hours", "failures", "availability"]

    def write_rows(self, directory: str, rows: list[dict[str, object]], fieldnames=None) -> Path:
        path = Path(directory) / "simulation.csv"
        with path.open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=fieldnames or self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_summary_includes_level_2_statistics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_rows(directory, [
                {"run_id": 1, "uptime_hours": 700, "downtime_hours": 20, "failures": 2, "availability": 0.97},
                {"run_id": 2, "uptime_hours": 710, "downtime_hours": 10, "failures": 1, "availability": 0.99},
            ])
            result = summarize(path)
            self.assertEqual(result["runs"], 2)
            self.assertAlmostEqual(result["mean_availability"], 0.98)
            self.assertAlmostEqual(result["median_availability"], 0.98)
            self.assertAlmostEqual(result["availability_stddev"], 0.01)
            self.assertEqual(result["p95_downtime_hours"], 20)
            self.assertEqual(result["max_failures"], 2)

    def test_empty_data_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_rows(directory, [])
            with self.assertRaisesRegex(ValueError, "empty"):
                summarize(path)

    def test_missing_field_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fields = ["run_id", "downtime_hours", "failures", "availability"]
            path = self.write_rows(directory, [], fields)
            with self.assertRaisesRegex(ValueError, "uptime_hours"):
                summarize(path)

    def test_malformed_number_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_rows(directory, [
                {"run_id": 1, "uptime_hours": 700, "downtime_hours": 20, "failures": "many", "availability": 0.97},
            ])
            with self.assertRaisesRegex(ValueError, "row 2"):
                summarize(path)

    def test_availability_range_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_rows(directory, [
                {"run_id": 1, "uptime_hours": 700, "downtime_hours": 20, "failures": 1, "availability": 1.2},
            ])
            with self.assertRaisesRegex(ValueError, "out of range"):
                summarize(path)

    def test_non_finite_metric_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_rows(directory, [
                {"run_id": 1, "uptime_hours": "nan", "downtime_hours": 1, "failures": 1, "availability": 0.97},
            ])
            with self.assertRaisesRegex(ValueError, "non-finite"):
                summarize(path)

    def test_non_positive_run_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_rows(directory, [
                {"run_id": 0, "uptime_hours": 700, "downtime_hours": 20, "failures": 1, "availability": 0.97},
            ])
            with self.assertRaisesRegex(ValueError, "run_id"):
                summarize(path)
    def test_negative_metrics_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_rows(directory, [
                {"run_id": 1, "uptime_hours": 700, "downtime_hours": -1, "failures": 1, "availability": 0.97},
            ])
            with self.assertRaisesRegex(ValueError, "negative"):
                summarize(path)


if __name__ == "__main__":
    unittest.main()
