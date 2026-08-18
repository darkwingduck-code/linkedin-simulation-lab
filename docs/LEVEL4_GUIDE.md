# Level 4 Guide

## Quality and CI

Local quality gate:

~~~powershell
.\.venv\Scripts\ruff.exe format --check python
.\.venv\Scripts\ruff.exe check python
.\.venv\Scripts\mypy.exe
.\scripts\run-level1.ps1
~~~

GitHub Actions repeats Release builds, CTest, Python unit/E2E tests, lint, typing, packaging, artifacts, sanitizers, static analysis, and the performance gate on supported jobs.

Official action majors were selected from their current repositories on 2026-08-18: checkout v6, setup-python v6, upload-artifact v7.

## Package

~~~powershell
.\scripts\package.ps1
~~~

Outputs:

- release/bin/reliability_simulator.exe
- dist/reliability_lab-0.4.0-py3-none-any.whl
- dist/reliability_lab-0.4.0.tar.gz

Installed Python commands:

- reliability-analyze
- reliability-compare
- reliability-performance-gate

## Static analysis

Enable clang-tidy with ENABLE_CLANG_TIDY=ON. The policy and two targeted exclusions are documented in ADR-002.

## Sanitizers

Linux CI configures ENABLE_SANITIZERS=ON and runs AddressSanitizer plus UndefinedBehaviorSanitizer in Debug. Windows uses warning-as-error and normal tests because the selected MinGW workflow does not provide the same sanitizer support.

## Performance gate

The gate runs 50,000 simulations and one Python analysis pass. Default limits are 2.0 seconds for simulation and 1.0 second for analysis. These intentionally broad thresholds catch major regressions rather than benchmark noise.

## Release checklist

1. All local quality gates pass.
2. CI passes on Windows and Linux.
3. Package contents and console commands are verified.
4. CHANGELOG and VERSION agree.
5. Security review and incident drill are current.
6. Tag v0.4.0 is created only after the commit is pushed.
7. GitHub release contains C++ and Python artifacts.
