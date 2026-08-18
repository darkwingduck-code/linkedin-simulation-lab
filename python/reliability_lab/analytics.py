from __future__ import annotations

import csv
import json
import math
import statistics
from pathlib import Path
from typing import TypedDict

class Summary(TypedDict):
    runs: int
    mean_availability: float
    median_availability: float
    availability_stddev: float
    p05_availability: float
    p95_downtime_hours: float
    mean_failures: float
    max_failures: int
_REQUIRED_FIELDS = {
    "run_id",
    "uptime_hours",
    "downtime_hours",
    "failures",
    "availability",
}


def _nearest_rank(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    rank = max(1, math.ceil(percentile * len(ordered)))
    return ordered[rank - 1]


def _read_rows(csv_path: str | Path) -> list[dict[str, str]]:
    with Path(csv_path).open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        fields = set(reader.fieldnames or ())
        missing = _REQUIRED_FIELDS - fields
        if missing:
            raise ValueError(f"missing CSV fields: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise ValueError("simulation data is empty")
    return rows


def summarize(csv_path: str | Path) -> Summary:
    rows = _read_rows(csv_path)
    availability: list[float] = []
    failures: list[int] = []
    downtime: list[float] = []

    for number, row in enumerate(rows, start=2):
        try:
            row_id = int(row["run_id"])
            row_uptime = float(row["uptime_hours"])
            row_downtime = float(row["downtime_hours"])
            row_failures = int(row["failures"])
            row_availability = float(row["availability"])
        except (TypeError, ValueError) as error:
            raise ValueError(f"invalid numeric value on CSV row {number}") from error
        finite_values = (row_uptime, row_downtime, row_availability)
        if not all(math.isfinite(value) for value in finite_values):
            raise ValueError(f"non-finite metric on CSV row {number}")
        if not 0.0 <= row_availability <= 1.0:
            raise ValueError(f"availability out of range on CSV row {number}")
        if row_id <= 0:
            raise ValueError(f"run_id must be positive on CSV row {number}")
        if row_failures < 0 or row_uptime < 0.0 or row_downtime < 0.0:
            raise ValueError(f"negative metric on CSV row {number}")
        availability.append(row_availability)
        failures.append(row_failures)
        downtime.append(row_downtime)

    return {
        "runs": len(rows),
        "mean_availability": statistics.fmean(availability),
        "median_availability": statistics.median(availability),
        "availability_stddev": statistics.pstdev(availability),
        "p05_availability": _nearest_rank(availability, 0.05),
        "p95_downtime_hours": _nearest_rank(downtime, 0.95),
        "mean_failures": statistics.fmean(failures),
        "max_failures": max(failures),
    }


def write_report(summary: Summary, output_path: str | Path) -> None:
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(summary, indent=2), encoding="utf-8")
