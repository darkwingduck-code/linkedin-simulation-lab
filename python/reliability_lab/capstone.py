from __future__ import annotations

import argparse
import html
import json
import math
import subprocess
import time
from pathlib import Path
from typing import TypedDict, cast

from .analytics import summarize


class ScenarioResult(TypedDict):
    name: str
    failure_rate: float
    repair_rate: float
    mean_availability: float
    p05_availability: float
    ci95_low: float
    ci95_high: float


def _run(
    simulator: Path, output: Path, runs: int, seed: int, failure: float, repair: float, threads: int
) -> float:
    command = [
        str(simulator),
        "--output",
        str(output),
        "--runs",
        str(runs),
        "--seed",
        str(seed),
        "--hours",
        "8760",
        "--failure-rate",
        str(failure),
        "--repair-rate",
        str(repair),
        "--threads",
        str(threads),
    ]
    started = time.perf_counter()
    subprocess.run(command, check=True, capture_output=True, text=True)
    return time.perf_counter() - started


def run_capstone(
    simulator: Path, output_dir: Path, runs: int, seed: int, threads: int
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    serial_csv = output_dir / "parallel-check-serial.csv"
    parallel_csv = output_dir / "parallel-check-parallel.csv"
    serial_seconds = _run(simulator, serial_csv, runs, seed, 0.0015, 0.08, 1)
    parallel_seconds = _run(simulator, parallel_csv, runs, seed, 0.0015, 0.08, threads)
    if serial_csv.read_bytes() != parallel_csv.read_bytes():
        raise RuntimeError("serial and parallel outputs differ for the same seed")

    definitions = [
        ("failure-low", 0.0010, 0.08),
        ("baseline", 0.0015, 0.08),
        ("failure-high", 0.0020, 0.08),
        ("repair-slow", 0.0015, 0.05),
        ("repair-fast", 0.0015, 0.12),
    ]
    scenarios: list[ScenarioResult] = []
    for index, (name, failure, repair) in enumerate(definitions):
        csv_path = output_dir / f"{name}.csv"
        _run(simulator, csv_path, runs, seed + index, failure, repair, threads)
        summary = summarize(csv_path)
        margin = 1.96 * summary["availability_stddev"] / math.sqrt(summary["runs"])
        scenarios.append(
            {
                "name": name,
                "failure_rate": failure,
                "repair_rate": repair,
                "mean_availability": summary["mean_availability"],
                "p05_availability": summary["p05_availability"],
                "ci95_low": summary["mean_availability"] - margin,
                "ci95_high": summary["mean_availability"] + margin,
            }
        )
    report: dict[str, object] = {
        "contract_version": "1.0",
        "runs_per_scenario": runs,
        "seed": seed,
        "threads": threads,
        "serial_seconds": serial_seconds,
        "parallel_seconds": parallel_seconds,
        "speedup": serial_seconds / parallel_seconds if parallel_seconds else 0.0,
        "parallel_exact_match": True,
        "scenarios": scenarios,
    }
    (output_dir / "capstone-results.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    _write_html(report, output_dir / "capstone-report.html")
    return report


def _write_html(report: dict[str, object], output: Path) -> None:
    scenarios = report["scenarios"]
    assert isinstance(scenarios, list)
    rows = []
    bars = []
    for index, item in enumerate(scenarios):
        assert isinstance(item, dict)
        name = html.escape(str(item["name"]))
        availability = float(item["mean_availability"])
        rows.append(
            f"<tr><td>{name}</td><td>{availability:.6f}</td><td>{float(item['p05_availability']):.6f}</td><td>[{float(item['ci95_low']):.6f}, {float(item['ci95_high']):.6f}]</td></tr>"
        )
        width = max(0.0, min(600.0, availability * 600.0))
        bars.append(
            f'<text x="0" y="{25 + index * 32}">{name}</text><rect x="110" y="{8 + index * 32}" width="{width:.2f}" height="20"/><text x="720" y="{25 + index * 32}">{availability:.6f}</text>'
        )
    document = f"""<!doctype html><html><head><meta charset="utf-8"><title>Level 5 capstone</title><style>body{{font-family:system-ui;max-width:1000px;margin:auto}}table{{border-collapse:collapse;width:100%}}td,th{{padding:.5rem;border:1px solid #ccc}}rect{{fill:#0a66c2}}</style></head><body><h1>Level 5 Reliability Capstone</h1><p>Exact parallel match: {report["parallel_exact_match"]}; measured speedup: {cast(float, report["speedup"]):.2f}x.</p><svg viewBox="0 0 850 180" role="img" aria-label="Scenario mean availability">{"".join(bars)}</svg><table><thead><tr><th>Scenario</th><th>Mean availability</th><th>P05</th><th>95% CI of mean</th></tr></thead><tbody>{"".join(rows)}</tbody></table></body></html>"""
    output.write_text(document, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Level 5 reliability capstone")
    parser.add_argument("--simulator", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/capstone"))
    parser.add_argument("--runs", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260818)
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()
    if args.runs <= 0 or args.threads <= 0:
        parser.error("runs and threads must be positive")
    report = run_capstone(args.simulator, args.output_dir, args.runs, args.seed, args.threads)
    print(f"Capstone complete: {args.output_dir}")
    print(f"Measured speedup: {cast(float, report['speedup']):.2f}x")


if __name__ == "__main__":
    main()
