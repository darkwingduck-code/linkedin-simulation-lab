$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$buildDirectory = Join-Path $projectRoot 'build'
$artifactDirectory = Join-Path $projectRoot 'artifacts'

$cmakeCommand = Get-Command cmake -ErrorAction SilentlyContinue
if ($cmakeCommand) {
    $cmake = $cmakeCommand.Source
    $ctest = Join-Path (Split-Path $cmake) 'ctest.exe'
    $configureArgs = @('-S', $projectRoot, '-B', $buildDirectory)
} else {
    $clion = Get-ChildItem 'C:\Program Files\JetBrains' -Directory -Filter 'CLion*' |
        Sort-Object Name -Descending | Select-Object -First 1
    if (-not $clion) { throw 'CMake was not found in PATH and no CLion installation was found.' }
    $cmake = Join-Path $clion.FullName 'bin\cmake\win\x64\bin\cmake.exe'
    $ctest = Join-Path $clion.FullName 'bin\cmake\win\x64\bin\ctest.exe'
    $compiler = Join-Path $clion.FullName 'bin\mingw\bin\c++.exe'
    $ninja = Join-Path $clion.FullName 'bin\ninja\win\x64\ninja.exe'
    $configureArgs = @('-S', $projectRoot, '-B', $buildDirectory, '-G', 'Ninja',
        "-DCMAKE_CXX_COMPILER=$compiler", "-DCMAKE_MAKE_PROGRAM=$ninja", '-DCMAKE_BUILD_TYPE=Release')
}

& $cmake @configureArgs
if ($LASTEXITCODE -ne 0) { throw 'CMake configure failed' }
& $cmake --build $buildDirectory --config Release
if ($LASTEXITCODE -ne 0) { throw 'C++ build failed' }
& $ctest --test-dir $buildDirectory -C Release --output-on-failure
if ($LASTEXITCODE -ne 0) { throw 'C++ tests failed' }

$executable = Join-Path $buildDirectory 'Release\reliability_simulator.exe'
if (-not (Test-Path $executable)) {
    $executable = Join-Path $buildDirectory 'reliability_simulator.exe'
}
& $executable --output (Join-Path $artifactDirectory 'simulation.csv') --json-output (Join-Path $artifactDirectory 'simulation.json') --runs 1000 --seed 42
if ($LASTEXITCODE -ne 0) { throw 'Simulation failed' }

$env:PYTHONPATH = Join-Path $projectRoot 'python'
$env:RELIABILITY_SIMULATOR = $executable
python -m unittest discover -s (Join-Path $projectRoot 'python\tests') -v
if ($LASTEXITCODE -ne 0) { throw 'Python tests failed' }
$mypy = Join-Path $projectRoot '.venv\Scripts\mypy.exe'
if (-not (Test-Path $mypy)) { throw 'Install dev dependencies with: .\.venv\Scripts\python.exe -m pip install -e ".[dev]"' }
& $mypy python/reliability_lab
if ($LASTEXITCODE -ne 0) { throw 'mypy failed' }
python -m reliability_lab.cli (Join-Path $artifactDirectory 'simulation.csv') --output (Join-Path $artifactDirectory 'summary.json')
if ($LASTEXITCODE -ne 0) { throw 'Analytics failed' }


