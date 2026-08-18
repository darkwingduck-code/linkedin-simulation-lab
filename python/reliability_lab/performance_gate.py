from __future__ import annotations

import argparse
import subprocess
import tempfile
import time
from pathlib import Path

from .analytics import summarize


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail on major performance regressions")
    parser.add_argument("--simulator", required=True)
    parser.add_argument("--runs", type=int, default=50_000)
    parser.add_argument("--max-simulation-seconds", type=float, default=2.0)
    parser.add_argument("--max-analysis-seconds", type=float, default=1.0)
    args = parser.parse_args()
    if args.runs <= 0:
        parser.error("--runs must be positive")

    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "performance.csv"
        started = time.perf_counter()
        subprocess.run(
            [
                args.simulator,
                "--output",
                str(output),
                "--runs",
                str(args.runs),
                "--seed",
                "42",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        simulation_seconds = time.perf_counter() - started

        started = time.perf_counter()
        summarize(output)
        analysis_seconds = time.perf_counter() - started

    print(f"simulation_seconds={simulation_seconds:.6f}")
    print(f"analysis_seconds={analysis_seconds:.6f}")
    if simulation_seconds > args.max_simulation_seconds:
        raise SystemExit(
            f"simulation regression: {simulation_seconds:.3f}s > {args.max_simulation_seconds:.3f}s"
        )
    if analysis_seconds > args.max_analysis_seconds:
        raise SystemExit(
            f"analysis regression: {analysis_seconds:.3f}s > {args.max_analysis_seconds:.3f}s"
        )
    print("PERFORMANCE_GATE=PASS")


if __name__ == "__main__":
    main()
