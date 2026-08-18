$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$build = Join-Path $projectRoot 'build\release'
$release = Join-Path $projectRoot 'release'
$cmake = 'C:\Program Files\JetBrains\CLion 2026.2.1\bin\cmake\win\x64\bin\cmake.exe'

& $cmake --install $build --prefix $release
if ($LASTEXITCODE -ne 0) { throw 'C++ install failed' }
& (Join-Path $projectRoot '.venv\Scripts\python.exe') -m build
if ($LASTEXITCODE -ne 0) { throw 'Python package build failed' }
Write-Output 'PACKAGE_BUILD=PASS'
