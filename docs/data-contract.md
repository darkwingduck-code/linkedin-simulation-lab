# CSV Data Contract

## Contract version

Version: 1.0

Producer: C++ reliability_simulator  
Consumer: Python reliability_lab.analytics

The first line must be the header. Additional columns may be added in a future backward-compatible version, but the five required columns cannot be renamed or removed within version 1.

## Required columns

| Column | Type | Unit | Constraint | Meaning |
|---|---|---|---|---|
| run_id | positive integer | none | unique within file | Monte Carlo run identifier |
| uptime_hours | finite number | hours | >= 0 | observed operating time |
| downtime_hours | finite number | hours | >= 0 | observed repair/down time |
| failures | integer | count | >= 0 | failures observed during the run |
| availability | finite number | ratio | 0 <= value <= 1 | uptime divided by observation hours |

## Example

~~~csv
run_id,uptime_hours,downtime_hours,failures,availability
1,706.200000,13.800000,1,0.980833
~~~

## Invariants

- uptime_hours + downtime_hours equals the configured observation window within tolerance.
- availability equals uptime_hours / observation window within serialization tolerance.
- numeric values must not be NaN or infinity.
- a file must contain at least one data row.

## Failure behavior

The Python consumer fails fast for a missing header, empty data, invalid numeric value, out-of-range availability, or negative downtime/failures. Additional columns are ignored. Breaking changes require a new contract version.

## Producer command

~~~powershell
.\build\debug\reliability_simulator.exe --output artifacts\simulation.csv --runs 1000 --seed 42 --hours 720 --failure-rate 0.0015 --repair-rate 0.08
~~~
