$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$simulator = Join-Path $projectRoot 'build\release\reliability_simulator.exe'
if (-not (Test-Path $simulator)) {
    throw 'Release simulator not found. Run scripts\run-level1.ps1 first.'
}
$csv = Join-Path $projectRoot 'artifacts\benchmark-100k.csv'
$watch = [Diagnostics.Stopwatch]::StartNew()
& $simulator --output $csv --runs 100000 --seed 42
if ($LASTEXITCODE -ne 0) { throw 'C++ benchmark failed' }
$watch.Stop()

$env:PYTHONPATH = Join-Path $projectRoot 'python'
$pythonOutput = Join-Path $projectRoot 'artifacts\python-benchmark.json'
python -m reliability_lab.benchmark $csv --repeat 20 --output $pythonOutput
if ($LASTEXITCODE -ne 0) { throw 'Python benchmark failed' }
$pythonResult = Get-Content $pythonOutput -Raw | ConvertFrom-Json

$result = [ordered]@{
    schema_version = '1.0'
    machine = [ordered]@{
        os = [Environment]::OSVersion.VersionString
        processor_count = [Environment]::ProcessorCount
        clion_toolchain = 'GNU 15.2.0 bundled with CLion 2026.2.1'
    }
    cpp_simulation = [ordered]@{
        runs = 100000
        seed = 42
        elapsed_seconds = $watch.Elapsed.TotalSeconds
        runs_per_second = 100000 / $watch.Elapsed.TotalSeconds
    }
    python_analysis = $pythonResult
}
$result | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $projectRoot 'artifacts\benchmark.json') -Encoding utf8
$result | ConvertTo-Json -Depth 5
