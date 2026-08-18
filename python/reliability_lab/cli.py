from __future__ import annotations

import argparse

from .analytics import summarize, write_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze C++ reliability simulation output")
    parser.add_argument("csv", nargs="?", default="artifacts/simulation.csv")
    parser.add_argument("--output", default="artifacts/summary.json")
    args = parser.parse_args()
    summary = summarize(args.csv)
    write_report(summary, args.output)
    print(f"Mean availability: {summary['mean_availability']:.3%}")
    print(f"5th percentile availability: {summary['p05_availability']:.3%}")
    print(f"Report written to {args.output}")


if __name__ == "__main__":
    main()

