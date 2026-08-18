# ADR-002: clang-tidy policy and targeted exclusions

Status: Accepted  
Date: 2026-08-18

## Decision

Enable bugprone, performance, and portability clang-tidy families. Treat bugprone and performance findings as errors.

Exclude:

- bugprone-exception-escape: command-line main functions already convert domain exceptions to exit codes; the checker also follows standard stream operations that can theoretically throw.
- bugprone-easily-swappable-parameters: the two local parsing helpers accept value and option label strings. Their narrow scope and named call sites make strong wrapper types disproportionate.

These exclusions are explicit rather than disabling all bugprone checks. Re-evaluate if the helpers become public APIs or new uncaught exception paths are introduced.
