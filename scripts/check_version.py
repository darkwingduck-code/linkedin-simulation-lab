from __future__ import annotations

import re
from pathlib import Path


def extract(pattern: str, text: str, source: str) -> str:
    match = re.search(pattern, text)
    if not match:
        raise SystemExit(f"could not find version in {source}")
    return match.group(1)


root = Path(__file__).resolve().parent.parent
expected = (root / "VERSION").read_text(encoding="utf-8").strip()
python_version = extract(
    r'(?m)^version = "([^"]+)"',
    (root / "pyproject.toml").read_text(encoding="utf-8"),
    "pyproject.toml",
)
cmake_version = extract(
    r"project\(reliability_simulator VERSION ([0-9.]+)",
    (root / "CMakeLists.txt").read_text(encoding="utf-8"),
    "CMakeLists.txt",
)
versions = {"VERSION": expected, "Python": python_version, "CMake": cmake_version}
if len(set(versions.values())) != 1:
    raise SystemExit(f"version mismatch: {versions}")
print(f"VERSION_CHECK=PASS ({expected})")
