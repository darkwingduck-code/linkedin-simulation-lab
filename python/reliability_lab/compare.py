from __future__ import annotations

import argparse
from pathlib import Path

from .reporting import compare_scenarios, render_html, write_comparison_json


def _scenario(value: str) -> tuple[str, Path]:
    name, separator, path = value.partition("=")
    if not separator or not name or not path:
        raise argparse.ArgumentTypeError("scenario must use NAME=CSV_PATH")
    return name, Path(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare reliability simulation scenarios")
    parser.add_argument(
        "--scenario",
        action="append",
        type=_scenario,
        required=True,
        help="Scenario in NAME=CSV_PATH form; provide at least twice",
    )
    parser.add_argument("--json-output", default="artifacts/comparison.json")
    parser.add_argument("--html-output", default="artifacts/comparison.html")
    args = parser.parse_args()
    scenarios = dict(args.scenario)
    rows = compare_scenarios(scenarios)
    write_comparison_json(rows, args.json_output)
    render_html(rows, args.html_output)
    print(f"Compared {len(rows)} scenarios")
    print(f"JSON report written to {args.json_output}")
    print(f"HTML report written to {args.html_output}")


if __name__ == "__main__":
    main()
