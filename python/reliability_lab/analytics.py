from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path


def summarize(csv_path: str | Path) -> dict[str, float | int]:
    with Path(csv_path).open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError("simulation data is empty")

    availability = [float(row["availability"]) for row in rows]
    failures = [int(row["failures"]) for row in rows]
    ordered = sorted(availability)
    p05_index = max(0, int(len(ordered) * 0.05) - 1)
    return {
        "runs": len(rows),
        "mean_availability": statistics.fmean(availability),
        "p05_availability": ordered[p05_index],
        "mean_failures": statistics.fmean(failures),
        "max_failures": max(failures),
    }


def write_report(summary: dict[str, float | int], output_path: str | Path) -> None:
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(summary, indent=2), encoding="utf-8")

