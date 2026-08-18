$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    & (Join-Path $PSScriptRoot 'run.ps1')
    if ($LASTEXITCODE -ne 0) { throw 'Baseline validation failed' }
    $simulator = Join-Path $root 'build\reliability_simulator.exe'
    $env:PYTHONPATH = Join-Path $root 'python'
    & (Join-Path $root '.venv\Scripts\python.exe') -m reliability_lab.capstone --simulator $simulator --output-dir (Join-Path $root 'artifacts\capstone') --runs 100000 --threads 4
    if ($LASTEXITCODE -ne 0) { throw 'Capstone failed' }
} finally {
    Pop-Location
}