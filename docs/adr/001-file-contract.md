# ADR-001: File contracts between C++ and Python

Status: Accepted  
Date: 2026-08-18

## Context

The system needs a clear boundary between a high-throughput C++ simulation engine and a Python analysis/reporting layer. The boundary must be inspectable in CLion and PyCharm, reproducible, portable, and simple enough for a learning project.

## Decision

Use versioned files:

- CSV version 1 for tabular analytics and interoperability.
- JSON version 1 for self-describing configuration, provenance, and complete results.

The C++ process owns simulation and serialization. Python owns validation, aggregation, scenario comparison, and presentation.

## Alternatives considered

### pybind11

Rejected for the current stage because it couples build systems, Python ABI, packaging, and process memory. Reconsider when interactive calls or zero-copy transfer becomes more valuable than process isolation.

### HTTP API

Rejected because deployment, networking, authentication, and service operations do not improve the current local experiment workflow. Reconsider when multiple remote consumers need concurrent access.

### Message queue

Rejected because asynchronous delivery and operational complexity are unnecessary for deterministic batch experiments. Reconsider for distributed high-volume simulation jobs.

## Consequences

Benefits:

- artifacts can be inspected, versioned, reproduced, and passed between IDEs;
- failures are isolated by process;
- no runtime integration dependency is required.

Costs:

- duplicate CSV and JSON serialization;
- disk I/O and parsing overhead;
- schema evolution must be explicit;
- very large experiments will require streaming or a binary columnar format.
