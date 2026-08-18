# Level 2 Guide

## Objective

Extend the baseline without breaking reproducibility or the C++/Python boundary.

## Named C++ CLI

~~~powershell
.\build\debug\reliability_simulator.exe --output artifacts\simulation.csv --runs 1000 --seed 42 --hours 720 --failure-rate 0.0015 --repair-rate 0.08
~~~

Run help with reliability_simulator.exe --help. Invalid values such as --runs 0 and unknown options return a non-zero exit code and show usage.

## Python Level 2 metrics

- mean_availability
- median_availability
- availability_stddev using population standard deviation
- p05_availability using nearest rank
- p95_downtime_hours using nearest rank
- mean_failures
- max_failures

Nearest rank is deterministic, easy to explain, and works for small samples. Production work must document whether interpolation is required.

## Validation exercises

1. Run with --runs 0 and confirm failure.
2. Run with --seed 4294967296 and confirm range failure.
3. Remove one required CSV header and confirm Python rejects the file.
4. Set availability to 1.2 and confirm range failure.
5. Compare Debug and Release summaries with seed 42.
6. Explain why malformed source data must fail before metrics are reported.

## Test inventory

C++/CTest covers deterministic seeds, accounting, bounds, invalid model configuration, named CLI success, zero-run rejection, and unknown-option rejection.

Python/unittest covers expanded statistics, empty data, missing headers, malformed numbers, availability range, and negative metrics, non-finite values, and invalid run identifiers.

## Remaining Level 2 work

- Install and configure a Python static type checker.
- Capture one PR explanation of a rejected design alternative.
