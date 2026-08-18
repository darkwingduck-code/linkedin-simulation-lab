# Conversation History

이 문서는 프로젝트와 관련된 대화를 시간순으로 요약한다. 대화 원문 전체를 복제하지 않고, 요청·응답·실행 결과·정정 사항을 보존한다. 인증 토큰과 개인 자격 증명은 기록하지 않는다.

## 1. 최초 요청

사용자는 CLion과 PyCharm에서 toy project를 연동해 LinkedIn 경력 성장을 지원해 달라고 요청했다. “Likedin”이 LinkedIn인지 LeetCode인지 확인한 뒤 LinkedIn임을 확정했다.

## 2. Connect Apps 언급

사용자는 LinkedIn이 plugin/Connect Apps로 연결돼 있다고 설명했다. 처음에는 이를 프로젝트 결과를 LinkedIn에 게시하는 흐름으로 해석했다. 로컬 상태를 조사해 기존 CLion과 PyCharm 프로젝트가 기본 예제 수준임을 확인했다.

## 3. 프로젝트 방향 결정

사용자가 “진행”을 요청했다. 별도의 직무 선택 답변 없이 기존 workspace의 simulation, AI, engineering 성격을 근거로 C++ simulation + Python analytics 방향을 선택했다. 기존 IDE 예제는 변경하지 않고 새 저장소 linkedin-simulation-lab을 만들었다.

## 4. 최초 구현

다음 항목을 구현했다.

- C++17 Monte Carlo reliability simulator
- failure/repair exponential distributions
- deterministic seed
- CSV output
- Python availability/failure analytics
- JSON summary
- CTest와 Python unittest
- PowerShell end-to-end workflow
- README와 LinkedIn 문안 초안

시스템 PATH에 CMake가 없었기 때문에 CLion 2026.2.1 bundled CMake, Ninja, GNU compiler를 자동 탐색하도록 스크립트를 보완했다.

## 5. 최초 검증과 GitHub

1,000 runs에서 mean availability 98.233%, fifth percentile 93.286%를 확인했다. CTest와 unittest가 통과했다. 초기 commit f6da7d3을 만들고 공개 GitHub 저장소에 main branch로 push했다.

Repository: https://github.com/darkwingduck-code/linkedin-simulation-lab

## 6. LinkedIn 게시 관련 정정

사용자가 “글을 올리라는 것이 아니라 Connect Apps”라고 정정했다. 이에 공개 게시를 전제로 한 해석이 잘못됐음을 인정했다. LinkedIn에는 자동 게시하지 않았고 LINKEDIN_POST.md는 참고 초안일 뿐임을 명확히 했다.

이후 사용자가 명시적으로 LinkedIn 게시를 요청했을 때는 연결된 쓰기 도구와 인앱 browser가 세션에 노출되지 않아 자동 게시를 완료할 수 없었다. 기본 browser의 게시 URL을 열고 정리된 문안을 clipboard에 준비했지만 게시 완료라고 주장하지 않았다.

## 7. PyCharm/CLion이 Connect Apps에 보이지 않는 문제

사용자는 Connect Apps 목록에 PyCharm과 CLion이 나타나지 않는다고 설명했다. 공식 OpenAI 문서를 확인해 다음을 정정했다.

- Connect Apps는 외부 서비스 connector 목록이다.
- 로컬 JetBrains IDE는 그 목록에 나타나는 대상이 아니다.
- JetBrains 연동은 IDE 안의 AI Chat에서 Codex를 선택하는 별도 방식이다.
- LinkedIn connector와 IDE integration은 서로 다른 경계다.

공식 안내: https://learn.chatgpt.com/docs/codex/ide

## 8. Level 5 로드맵 요청

사용자는 CLion과 PyCharm 모두 Level 5까지 성장할 수 있는 상세 가이드와 대화 기록의 Git 보존을 요청했다. Level 5를 공식 JetBrains 등급이 아니라 독립적으로 설계·구현·테스트·자동화·배포·설명할 수 있는 project competency로 정의했다.

다음을 추가하고 commit 51b2224로 push했다.

- docs/LEVEL5_ROADMAP.md
- docs/PROGRESS_TRACKER.md
- docs/SESSION_LOG.md
- README learning links

## 9. Level 1 실제 진행

사용자가 계속 진행하고 가이드와 대화 내용을 더 자세히 Git에 남기도록 요청했다. 다음을 추가했다.

- CMakePresets.json의 Debug/Release workflow
- scripts/run-level1.ps1
- docs/IDE_SETUP_GUIDE.md
- docs/level-1-notes.md
- 현재 문서

실제 실행에서 Debug/Release C++ build와 CTest, Python unittest, 1,000-run 분석이 통과했다. 다만 IDE에서 사람이 breakpoint를 조작하고 screenshot을 남기는 작업은 자동 검증과 구분해 아직 완료로 표시하지 않았다.

## 기록 원칙

- 수행하지 않은 작업을 완료로 표시하지 않는다.
- LinkedIn 공개 게시 여부처럼 외부 상태는 실제 증거 없이 주장하지 않는다.
- 대화 기록에는 비밀정보를 넣지 않는다.
- 학습 주장은 commit, test, benchmark, screenshot 또는 글로 입증한다.

## 10. Level 2 구현

사용자가 다음 단계 진행을 요청해 named C++ CLI, 강한 입력 검증, 확장된 Python 통계, edge-case tests, warning-as-error compiler gate, strict mypy gate와 CSV data contract를 구현했다.

Debug와 Release에서 CTest 4개씩 통과했고 Python unittest 8개와 mypy source 3개가 통과했다. 자동 test case 수는 CTest 4 + Python 8로 12개다. 기존 1,000-run baseline 결과도 유지됐다.

설계상 positional CLI를 제거해 호출 의미를 명확하게 했고, percentile은 작은 표본에서도 결정적으로 동작하는 nearest-rank를 선택했다. CSV는 초기 학습 경계로 유지하되 schema 한계와 pybind11/API/message queue 대안을 문서화했다.

### Level 2 review correction

Pre-push verification found that C++ standard assert is compiled out in Release and that PowerShell ErrorActionPreference alone does not stop on every native executable failure. Tests were changed to explicit runtime checks, and both workflow scripts now validate LASTEXITCODE after each native command. Fresh Debug and Release runs passed afterward.

## 11. Level 3 구현

사용자가 이어서 진행을 요청했다. C++ simulation과 serialization을 분리하고 schema version 1.0 JSON을 추가했다. Python에는 다중 scenario 비교, versioned comparison JSON, table과 inline SVG charts를 포함한 HTML report를 구현했다.

end-to-end test는 C++ executable을 두 번 실행해 baseline/stressed artifacts를 만들고 JSON version과 result 수를 검증한 뒤 Python으로 HTML까지 생성한다. Debug/Release CTest 4개, Python tests 11개, strict mypy source 6개가 통과했다.

실제 benchmark는 Release 100,000 runs에서 약 582,118 runs/second, Python 100,000-row summary 평균 약 0.209초였다. 수치는 같은 머신과 조건에서만 비교해야 한다는 제한도 함께 기록했다.
