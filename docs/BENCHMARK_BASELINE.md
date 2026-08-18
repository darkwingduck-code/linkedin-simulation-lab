# Benchmark Baseline

Date: 2026-08-18  
OS: Microsoft Windows NT 10.0.26200.0  
Logical processors: 24  
Toolchain: GNU 15.2.0 bundled with CLion 2026.2.1  
Build: Release  
Command: scripts/benchmark.ps1

## C++ simulation

- Runs: 100,000
- Seed: 42
- Elapsed: 0.1717865 seconds
- Throughput: 582,117.92 runs/second

## Python CSV analytics

Input: the 100,000-row C++ benchmark CSV  
Repeats: 20

- Mean: 0.2089791 seconds
- Minimum: 0.1810511 seconds
- Maximum: 0.3519209 seconds

## Interpretation

On this machine the simulation itself is faster than one Python parse-and-summary pass for the resulting CSV. This suggests that file serialization/parsing is already a meaningful part of end-to-end latency. It does not yet justify replacing the file contract: inspectability and reproducibility remain more valuable at the current scale.

Future measurements must use the same build type, machine power mode, run count, seed, and input artifact. Compare medians or multiple benchmark sessions before claiming a regression or improvement.
