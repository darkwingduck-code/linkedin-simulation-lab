# Security and Failure Modes

## Trust boundaries

### CLI arguments

Risk: unbounded runs can exhaust CPU, memory, and disk.  
Current control: values must be positive and type/range valid.  
Remaining limitation: no configurable maximum run count. Operators must set resource limits for untrusted callers.

### Output paths

Risk: a caller can overwrite writable files by selecting an output path.  
Current control: the program only writes explicitly requested CSV/JSON paths and reports open failures.  
Remaining limitation: paths are not sandboxed. Never expose the CLI directly to untrusted remote users.

### CSV input

Risk: malformed, oversized, non-finite, or adversarial rows.  
Controls: required schema, numeric parsing, finite/range checks, non-empty input, fail-fast errors.  
Remaining limitation: the current analyzer loads the full file into memory. Use file-size limits or streaming for untrusted large files.

### HTML output

Risk: scenario names could inject markup or script.  
Control: scenario names and chart titles are HTML escaped; a regression test covers script-shaped input.  
Remaining limitation: generated reports have inline CSS/SVG. Serve with a restrictive Content-Security-Policy if hosted.

### JSON output

Risk: downstream consumers may interpret incompatible schemas.  
Control: schema_version is mandatory and documented.  
Remaining limitation: no JSON Schema file or cryptographic artifact signing yet.

### Dependencies and CI

Risk: compromised package or GitHub Action.  
Controls: minimal Python dependencies, read-only CI token permission, official actions, reproducible version metadata.  
Remaining limitation: actions use major tags rather than immutable commit SHAs; Python development dependencies use lower bounds.

## Resource exhaustion

- Keep run counts bounded in automation.
- Store artifacts outside source control.
- Monitor artifact retention and storage.
- Run performance gates using Release builds.
- Prefer streaming or columnar storage before processing multi-gigabyte files.

## Secret handling

The project requires no runtime secrets. Never place GitHub tokens, API keys, credentials, or private datasets in CLI arguments, CSV/JSON artifacts, screenshots, or committed logs.

## Reporting a vulnerability

Do not publish credentials or exploit details in a public issue. Revoke exposed credentials first, preserve minimal evidence, and use the repository owner's private contact channel.
