$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$clion = Get-ChildItem 'C:\Program Files\JetBrains' -Directory -Filter 'CLion*' | Sort-Object Name -Descending | Select-Object -First 1
if (-not $clion) { throw 'CLion installation not found.' }
$cmake = Join-Path $clion.FullName 'bin\cmake\win\x64\bin\cmake.exe'
$ctest = Join-Path $clion.FullName 'bin\cmake\win\x64\bin\ctest.exe'
$compiler = Join-Path $clion.FullName 'bin\mingw\bin\c++.exe'
$ninja = Join-Path $clion.FullName 'bin\ninja\win\x64\ninja.exe'
foreach ($configuration in @('Debug','Release')) {
    $name = $configuration.ToLowerInvariant()
    $buildDirectory = Join-Path $projectRoot "build\$name"
    & $cmake -S $projectRoot -B $buildDirectory -G Ninja "-DCMAKE_CXX_COMPILER=$compiler" "-DCMAKE_MAKE_PROGRAM=$ninja" "-DCMAKE_BUILD_TYPE=$configuration"
    if ($LASTEXITCODE -ne 0) { throw "$configuration configure failed" }
    & $cmake --build $buildDirectory
    if ($LASTEXITCODE -ne 0) { throw "$configuration build failed" }
    & $ctest --test-dir $buildDirectory --output-on-failure
    if ($LASTEXITCODE -ne 0) { throw "$configuration tests failed" }
}
$env:PYTHONPATH = Join-Path $projectRoot 'python'
python -m unittest discover -s (Join-Path $projectRoot 'python\tests') -v
if ($LASTEXITCODE -ne 0) { throw 'Python tests failed' }
$mypy = Join-Path $projectRoot '.venv\Scripts\mypy.exe'
if (-not (Test-Path $mypy)) {
    throw 'mypy is required. Run: .\.venv\Scripts\python.exe -m pip install -e ".[dev]"'
}
& $mypy python/reliability_lab
if ($LASTEXITCODE -ne 0) { throw 'mypy failed' }
& (Join-Path $projectRoot 'build\debug\reliability_simulator.exe') --output (Join-Path $projectRoot 'artifacts\level1-debug.csv') --runs 1000 --seed 42
if ($LASTEXITCODE -ne 0) { throw 'Simulation failed' }
python -m reliability_lab.cli (Join-Path $projectRoot 'artifacts\level1-debug.csv') --output (Join-Path $projectRoot 'artifacts\level1-summary.json')
if ($LASTEXITCODE -ne 0) { throw 'Analytics failed' }
Write-Output 'LEVEL1_VERIFICATION=PASS'
