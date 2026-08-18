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
