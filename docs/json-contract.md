# JSON Data Contract

Version: 1.0

The JSON artifact preserves the simulation configuration and every result row.

~~~json
{
  "schema_version": "1.0",
  "config": {
    "runs": 1000,
    "seed": 42,
    "hours": 720.0,
    "failure_rate_per_hour": 0.0015,
    "repair_rate_per_hour": 0.08
  },
  "results": [
    {
      "run_id": 1,
      "uptime_hours": 720.0,
      "downtime_hours": 0.0,
      "failures": 0,
      "availability": 1.0
    }
  ]
}
~~~

Compatibility rules:

- Consumers must check schema_version before interpretation.
- New optional fields may be added in a backward-compatible 1.x release.
- Removing, renaming, or changing the meaning/type of a field requires 2.0.
- config is the provenance required to reproduce a run.
- results follows the same numeric constraints as the CSV contract.
