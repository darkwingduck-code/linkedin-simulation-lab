# Project Session Log

이 문서는 계정 자격 증명이나 대화 원문 전체를 저장하지 않고, 프로젝트 구성 과정에서 나온 유용한 의사결정과 검증 결과를 보존한다.

## 2026-08-18 — Initial setup

### 사용자 목표

- CLion과 PyCharm에서 연결되는 toy project 구축
- 학습 진행과 LinkedIn portfolio에 사용할 수 있는 증거 생성
- GitHub에 코드와 과정을 보존

### 주요 결정

- C++ simulation과 Python analytics를 결합한 reliability engineering 프로젝트 선택
- 기존 `CLionProjects/untitled`와 `PycharmProjects/WelcomeScreen`은 변경하지 않음
- 두 IDE에서 하나의 Git 저장소를 열어 중복을 피함
- 초기 언어 경계는 안정적인 CSV 계약으로 정의
- baseline은 표준 라이브러리만 사용해 실행 장벽을 낮춤

### 구현

- deterministic C++17 Monte Carlo failure/repair simulator
- seed 재현성과 accounting invariant를 검증하는 CTest
- availability/failure metrics를 계산하는 Python package와 CLI
- Python unittest
- CLion bundled CMake를 탐색하고 build, test, simulation, analysis를 실행하는 PowerShell workflow
- README와 portfolio 설명

### 검증

- CLion 2026.2.1 bundled GNU 15.2.0 toolchain으로 C++ build 성공
- CTest 1/1 통과
- Python unittest 1/1 통과
- 1,000회 simulation 실행
- 평균 availability 98.233%
- 5th-percentile availability 93.286%

### GitHub 전달

- Initial commit: `f6da7d3 feat: add cross-language reliability simulation lab`
- Repository: https://github.com/darkwingduck-code/linkedin-simulation-lab
- Default branch: `main`

### 정정된 이해

- 처음에는 “Connect Apps”를 LinkedIn 글 게시 요청으로 잘못 해석했다.
- 정확한 의미: Connect Apps는 외부 서비스 connector이며 로컬 PyCharm/CLion은 그 목록에 나타나지 않는다.
- JetBrains IDE 연동은 별도 경로다. JetBrains AI Chat에서 Codex를 선택한다.
- 설정 과정에서 LinkedIn 게시물은 자동 공개되지 않았다.

### 다음 목표

`LEVEL5_ROADMAP.md`와 `PROGRESS_TRACKER.md`를 따라 진행한다. 첫 작업은 Level 1 debugger 증거와 `docs/level-1-notes.md` 작성이다.

## 2026-08-18 — Level 1 execution

### 추가된 재현성 도구

- CMakePresets.json에 Debug/Release configure, build, test preset 추가
- scripts/run-level1.ps1에 CLion bundled CMake/Ninja/compiler 탐색 추가
- Debug/Release를 독립 build directory에서 구성·빌드·테스트
- Python unittest와 1,000-run 통합 분석 포함

### 실행 결과

- Debug build 및 CTest 통과
- Release build 및 CTest 통과
- Python unittest 통과
- 1,000-run simulation과 summary 생성
- 최종 marker: LEVEL1_VERIFICATION=PASS

### 문서화

- IDE_SETUP_GUIDE.md: 두 IDE의 설정, 실행, debugger, 문제 해결, 증거 제출 절차
- level-1-notes.md: 데이터 흐름, 핵심 함수, 모델 가정, 언어 경계, 불변조건
- CONVERSATION_HISTORY.md: 지금까지의 사용자 요청, 수행, 정정 이력

### 의도적으로 미완료 처리한 사항

IDE에서 사용자가 직접 breakpoint와 variable inspector를 조작하고 screenshot을 남기는 단계는 자동 build와 다르다. 실제 screenshot이 없으므로 CLion/PyCharm debugger walkthrough는 tracker에서 미완료 상태다.

## 2026-08-18 — Level 2 implementation

### C++ changes

- Positional arguments replaced with named options for output, runs, seed, hours, failure rate, and repair rate.
- Rejects missing values, unknown options, negative integers, trailing characters, non-finite doubles, non-positive rates/hours, and seed/runs range violations.
- GNU/Clang warning flags enabled and warnings promoted to errors.
- CTest now covers model invariants, named CLI success, zero-run rejection, and unknown-option rejection.

### Python changes

- Added median availability, population standard deviation, and p95 downtime.
- Added required-header, empty-file, numeric parsing, range, and negative-value validation.
- Replaced a broad dictionary alias with a TypedDict summary contract.
- Added strict mypy configuration and verified all package sources.

### Verification

- Debug CTest: 4/4 pass.
- Release CTest: 4/4 pass.
- Python unittest: 8/8 pass.
- Strict mypy: 3 source files, no issues.
- Warning-as-error C++ builds pass.
- Integrated 1,000-run analysis remains reproducible at 98.233% mean availability.

### Documentation

- docs/LEVEL2_GUIDE.md
- docs/data-contract.md
- progress and conversation logs updated

### Verification hardening discovered during review

When warning-as-error was expanded to the Release test target, the build revealed that standard assert checks disappear under NDEBUG. The test executable was rewritten to use explicit runtime checks that remain active in Release. Both PowerShell workflows now inspect every native exit code and stop immediately on configure, build, test, simulation, type-check, or analytics failure.

## 2026-08-18 — Level 3 implementation

### Architecture

- Split C++ simulation from CSV/JSON serialization.
- Added JSON schema version 1.0 with configuration provenance and complete results.
- Documented the file-boundary decision and rejected pybind11, API, and queue alternatives in ADR-001.

### Python system

- Added sorted multi-scenario comparison.
- Added versioned comparison JSON.
- Added self-contained HTML with a metrics table and two inline SVG bar charts.
- Added a CLI for scenario comparison.
- Added a cross-process end-to-end test that launches C++, validates JSON, reads CSV, and renders HTML.

### Verification

- Debug CTest 4/4 and Release CTest 4/4.
- Python unittest 11/11 including end-to-end.
- strict mypy: 6 package source files, no issues.
- Total automated cases: 15.
- Real baseline and stressed scenario pipeline generated successfully.

### Benchmark

- C++ 100,000 runs: 0.1717865 seconds, 582,117.92 runs/second.
- Python 100,000-row analysis mean: 0.2089791 seconds over 20 repeats.
- Full environment and interpretation recorded in BENCHMARK_BASELINE.md.

## 2026-08-18 — Level 4 implementation

### Delivery automation

- Added Windows and Linux GitHub Actions with read-only repository permissions.
- Added Release C++ build/test, Python lint/type/test, E2E, performance gate, packaging, and artifacts.
- Added Linux AddressSanitizer/UndefinedBehaviorSanitizer and clang-tidy jobs.
- Added official checkout v6, setup-python v6, and upload-artifact v7 actions.
- Added VERSION/CMake/Python version consistency check.

### Local quality evidence

- ruff format and lint pass.
- strict mypy passes for 7 package source files.
- clang-tidy bugprone/performance/portability build passes with two documented targeted exclusions.
- C++ property checks cover 50 generated configurations.
- Python property checks cover 200 deterministic generated rows and HTML escaping.
- Local performance gate passes: 50,000 runs in 0.098625 s; analysis in 0.105198 s.
- Python wheel, source distribution, and C++ installed binary produced successfully.
- Installed console commands and wheel contents verified.

### Reliability and security

- Added explicit trust boundaries, resource exhaustion analysis, secret guidance, and vulnerability reporting.
- Added an incident drill documenting Release assertions compiled out and native exit-code handling.
- CI and sanitizer items remain unchecked in the tracker until GitHub reports successful runs.
