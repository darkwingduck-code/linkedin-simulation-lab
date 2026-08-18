# Level 3 Guide

## Outcomes

Level 3 transforms the baseline into a modular experiment system:

- C++ simulation and serialization are separate responsibilities.
- CSV remains the analytics contract.
- versioned JSON preserves configuration and full results.
- Python compares multiple scenarios.
- HTML reports contain tables and two inline SVG charts.
- end-to-end tests cross the process and language boundary.
- benchmark commands establish a performance baseline.

## Generate a scenario

~~~powershell
.\build\release\reliability_simulator.exe --output artifacts\baseline.csv --json-output artifacts\baseline.json --runs 1000 --seed 42 --failure-rate 0.0015
~~~

Generate a stressed scenario:

~~~powershell
.\build\release\reliability_simulator.exe --output artifacts\stressed.csv --json-output artifacts\stressed.json --runs 1000 --seed 42 --failure-rate 0.004
~~~

## Compare scenarios

~~~powershell
$env:PYTHONPATH='python'
python -m reliability_lab.compare --scenario baseline=artifacts\baseline.csv --scenario stressed=artifacts\stressed.csv --json-output artifacts\comparison.json --html-output artifacts\comparison.html
~~~

Open artifacts/comparison.html in a browser. Check that the table, mean availability chart, and p95 downtime chart agree with comparison.json.

## Run the end-to-end test

scripts/run-level1.ps1 sets RELIABILITY_SIMULATOR and discovers all Python tests. The end-to-end test launches C++ twice, validates JSON schema version 1.0, summarizes both CSV files, and renders HTML.

## Benchmark

~~~powershell
.\scripts\benchmark.ps1
~~~

The benchmark records:

- machine OS and logical processor count;
- C++ toolchain;
- 100,000-run simulator elapsed time and runs/second;
- repeated Python CSV summary mean/min/max latency.

Benchmark numbers describe this machine and are not universal claims. Compare changes on the same machine, power mode, build type, run count, and seed.

## Architecture questions

1. Why do CSV and JSON coexist?
2. Which contract is authoritative for analytics?
3. Where should schema migration occur?
4. When does file I/O become the bottleneck?
5. Which alternative in ADR-001 should be selected at 100x scale?
6. Which assumptions in the reliability model dominate scenario differences?

## Measured scenario result

Using 1,000 runs and seed 42:

| Metric | Baseline failure rate 0.0015 | Stressed failure rate 0.004 |
|---|---:|---:|
| Mean availability | 98.233% | 95.263% |
| P05 availability | 93.286% | 87.896% |
| P95 downtime | 47.937 h | 86.685 h |
| Mean failures | 1.051 | 2.781 |

This is a deterministic demonstration for the configured seed, not a calibrated real-world prediction.
