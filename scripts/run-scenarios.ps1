$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$simulator = Join-Path $projectRoot 'build\release\reliability_simulator.exe'
if (-not (Test-Path $simulator)) { throw 'Run scripts\run-level1.ps1 first.' }
$artifacts = Join-Path $projectRoot 'artifacts'

& $simulator --output (Join-Path $artifacts 'baseline.csv') --json-output (Join-Path $artifacts 'baseline.json') --runs 1000 --seed 42 --failure-rate 0.0015
if ($LASTEXITCODE -ne 0) { throw 'Baseline scenario failed' }
& $simulator --output (Join-Path $artifacts 'stressed.csv') --json-output (Join-Path $artifacts 'stressed.json') --runs 1000 --seed 42 --failure-rate 0.004
if ($LASTEXITCODE -ne 0) { throw 'Stressed scenario failed' }

$env:PYTHONPATH = Join-Path $projectRoot 'python'
python -m reliability_lab.compare --scenario "baseline=$artifacts\baseline.csv" --scenario "stressed=$artifacts\stressed.csv" --json-output (Join-Path $artifacts 'comparison.json') --html-output (Join-Path $artifacts 'comparison.html')
if ($LASTEXITCODE -ne 0) { throw 'Scenario comparison failed' }
Write-Output 'SCENARIO_PIPELINE=PASS'
