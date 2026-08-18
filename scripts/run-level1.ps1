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
    & $cmake --build $buildDirectory
    & $ctest --test-dir $buildDirectory --output-on-failure
}
$env:PYTHONPATH = Join-Path $projectRoot 'python'
python -m unittest discover -s (Join-Path $projectRoot 'python\tests') -v
& (Join-Path $projectRoot 'build\debug\reliability_simulator.exe') (Join-Path $projectRoot 'artifacts\level1-debug.csv') 1000 42
python -m reliability_lab.cli (Join-Path $projectRoot 'artifacts\level1-debug.csv') --output (Join-Path $projectRoot 'artifacts\level1-summary.json')
Write-Output 'LEVEL1_VERIFICATION=PASS'
