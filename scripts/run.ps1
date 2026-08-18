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
& $cmake --build $buildDirectory --config Release
& $ctest --test-dir $buildDirectory -C Release --output-on-failure

$executable = Join-Path $buildDirectory 'Release\reliability_simulator.exe'
if (-not (Test-Path $executable)) {
    $executable = Join-Path $buildDirectory 'reliability_simulator.exe'
}
& $executable (Join-Path $artifactDirectory 'simulation.csv') 1000 42

$env:PYTHONPATH = Join-Path $projectRoot 'python'
python -m unittest discover -s (Join-Path $projectRoot 'python\tests') -v
python -m reliability_lab.cli (Join-Path $artifactDirectory 'simulation.csv') --output (Join-Path $artifactDirectory 'summary.json')


