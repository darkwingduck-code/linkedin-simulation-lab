from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from .analytics import summarize


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark Python reliability analytics")
    parser.add_argument("csv")
    parser.add_argument("--repeat", type=int, default=20)
    parser.add_argument("--output", default="artifacts/python-benchmark.json")
    args = parser.parse_args()
    if args.repeat <= 0:
        parser.error("--repeat must be positive")

    durations: list[float] = []
    for _ in range(args.repeat):
        start = time.perf_counter()
        summarize(args.csv)
        durations.append(time.perf_counter() - start)

    result = {
        "schema_version": "1.0",
        "operation": "python_csv_summary",
        "repeat": args.repeat,
        "mean_seconds": sum(durations) / len(durations),
        "min_seconds": min(durations),
        "max_seconds": max(durations),
    }
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
