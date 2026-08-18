# Incident Drill: Release tests silently disabled

Date: 2026-08-18  
Severity: High for test reliability; no production deployment occurred.

## Scenario

The C++ unit executable originally used the standard assert macro. Release builds define NDEBUG, which removes assert expressions. The test executable could therefore exit successfully without checking invariants.

The PowerShell workflow also used ErrorActionPreference alone. Native executables can return non-zero without producing a terminating PowerShell error, allowing later commands to continue.

## Detection

Expanding warning-as-error to the Release test target produced unused-variable warnings. Those warnings revealed that assertions had been compiled away. A deliberately failing build also showed the workflow continuing to later commands.

## Root cause

- Test correctness depended on a build-mode-sensitive macro.
- The orchestration script assumed PowerShell exception behavior covered native exit codes.
- Earlier validation checked final output but did not inject a known failure into the workflow.

## Remediation

- Replaced assertions with explicit runtime require checks.
- Wrapped the test main body and returned non-zero on failures.
- Checked LASTEXITCODE after configure, build, CTest, simulation, unittest, mypy, and analytics.
- Added Debug and Release test execution.
- Added randomized invariants across 50 generated C++ configurations.

## Verification

- Debug and Release CTest both execute the invariant checks.
- Warning-as-error builds pass.
- A non-zero native command now terminates the workflow.
- CI repeats the checks on Windows and Linux.

## Prevention

- Never use build-disabled assertions as the only test oracle.
- Every workflow command must have an explicit failure contract.
- Run at least one deliberate-failure drill when changing orchestration.
- Review Release output independently from Debug output.
