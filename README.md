# Reliability Simulation Lab

A portfolio-ready toy project connecting a high-performance C++17 Monte Carlo engine with a lightweight Python analytics pipeline.

## Architecture

```text
CLion / C++ simulator -> artifacts/simulation.csv -> PyCharm / Python analyzer
                                                        |
                                                        v
                                              artifacts/summary.json
```

The simulator models alternating failure and repair events over a 720-hour operating window. The Python layer calculates mean availability, fifth-percentile availability, and failure statistics.

## Run everything

From PowerShell:

```powershell
.\scripts\run.ps1
```

No third-party runtime dependencies are required. You need CMake, a C++17 compiler, and Python 3.10+.

## CLion

Open the repository root as a CMake project. Build `reliability_simulator` or run `reliability_tests`. The executable accepts:

```text
reliability_simulator [output.csv] [runs] [seed]
```

## PyCharm

Open the repository root, create a Python 3.10+ interpreter, then mark `python` as a Sources Root. Run:

```powershell
$env:PYTHONPATH='python'
python -m reliability_lab.cli artifacts/simulation.csv
python -m unittest discover -s python/tests -v
```

## Portfolio talking points

- Clear language boundary through a stable CSV contract
- Deterministic simulations for reproducible engineering results
- Separate unit tests for the computational and analytics layers
- One-command end-to-end workflow suitable for CI

See [LINKEDIN_POST.md](LINKEDIN_POST.md) for a ready-to-edit launch post.

## Learning path

- [Level 5 roadmap](docs/LEVEL5_ROADMAP.md): C++/CLion과 Python/PyCharm의 5단계 실전 커리큘럼
- [Progress tracker](docs/PROGRESS_TRACKER.md): 완료 항목과 포트폴리오 증거 기록
- [Project session log](docs/SESSION_LOG.md): 프로젝트 결정, 실행, 검증 및 정정 내역

### Level 1 execution

- [IDE setup and debugging guide](docs/IDE_SETUP_GUIDE.md)
- [Level 1 technical notes](docs/level-1-notes.md)
- [Conversation history](docs/CONVERSATION_HISTORY.md)
- Run all Level 1 automated checks with .\scripts\run-level1.ps1.
