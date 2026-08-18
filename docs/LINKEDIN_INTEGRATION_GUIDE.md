# LinkedIn 연결 실전 가이드 — 퇴근 후 혼자 따라 하기

최종 확인일: 2026-08-18. LinkedIn과 ChatGPT/Codex 화면은 계정, 요금제, 지역, 배포 시점에 따라 다를 수 있다. 이 문서는 게시글 작성을 요구하지 않고 프로젝트 증거를 프로필에 연결하는 절차만 다룬다.

## 먼저 알아야 할 핵심

CLion과 PyCharm은 LinkedIn에 연결되는 앱이 아니다. 두 IDE에서 프로젝트를 개발했다는 증거는 GitHub commit, CI, release, 문서로 남기고 LinkedIn 프로필에는 그 GitHub URL을 연결한다. ChatGPT/Codex의 Connect apps는 외부 서비스의 데이터와 작업을 연결하는 connector 목록이다. JetBrains IDE 통합은 IDE 안의 AI Chat에서 Codex를 선택하는 별도 로컬 개발 통합이므로 Connect apps에 `CLion`이나 `PyCharm`이 표시되지 않아도 정상이다.

공식 근거:

- OpenAI Codex IDE: https://learn.chatgpt.com/docs/codex/ide
- OpenAI 용어집의 IDE extension/connector 구분: https://learn.chatgpt.com/docs/glossary
- LinkedIn 프로필 섹션 추가: https://www.linkedin.com/help/linkedin/answer/a540837/add-sections-to-your-profile
- LinkedIn Featured 작업 샘플: https://www.linkedin.com/help/linkedin/answer/a550399/feature-samples-of-your-work-on-your-linkedin-profile
- LinkedIn 웹사이트 연결: https://www.linkedin.com/help/linkedin/answer/a548010/adding-a-website-to-your-profile

## 0. 시작 전 5분 점검

1. GitHub에서 저장소가 로그아웃 상태로 열리는지 확인한다: https://github.com/darkwingduck-code/linkedin-simulation-lab
2. Release가 공개인지 확인한다: https://github.com/darkwingduck-code/linkedin-simulation-lab/releases
3. Actions에서 최근 CI가 초록색인지 확인한다.
4. 저장소에 실명, 이메일, API key, 회사 기밀 데이터가 없는지 다시 확인한다.
5. LinkedIn 프로필 수정 전에 현재 소개/About 내용을 메모장에 백업한다.

주의: 이 저장소의 parameter는 교육용 가정이다. 실제 설비나 서비스의 안전성 인증 결과처럼 표현하면 안 된다.

## 1. CLion에서 증거 재현

1. CLion에서 `File > Open`으로 저장소 루트를 연다.
2. CMake profile을 Release로 선택하고 Reload CMake Project를 실행한다.
3. `reliability_tests`를 실행해 통과를 확인한다.
4. `reliability_simulator` Run configuration에 다음 인자를 넣는다.

```text
--output artifacts/clion-level5.csv --runs 100000 --seed 20260818 --hours 8760 --failure-rate 0.0015 --repair-rate 0.08 --threads 4
```

5. 같은 명령을 `--threads 1`로도 실행한다. 두 CSV가 동일해야 한다.
6. `simulate_one`에 breakpoint를 걸고 한 run의 고장/복구 흐름을 관찰한다.

막히면 확인할 것:

- CMake 3.20 이상, C++17 toolchain인지 확인한다.
- `--threads 0`은 의도적으로 실패한다.
- 빌드 폴더가 꼬이면 CLion의 Reset Cache and Reload Project를 먼저 사용한다. 저장소 전체를 삭제하지 않는다.

## 2. PyCharm에서 증거 재현

1. 같은 저장소를 PyCharm으로 연다.
2. Project Interpreter를 `.venv\Scripts\python.exe`로 지정한다.
3. Terminal에서 `python -m pip install -e ".[dev]"`를 실행한다.
4. `python` 폴더를 Sources Root로 지정한다.
5. unittest configuration을 만들고 `python/tests` 전체를 실행한다.
6. Python module configuration을 만든다.

```text
Module: reliability_lab.capstone
Arguments: --simulator build/reliability_simulator.exe --output-dir artifacts/capstone --runs 100000 --threads 4
Working directory: 저장소 루트
```

7. `artifacts/capstone/capstone-report.html`을 브라우저로 열어 민감도 결과를 확인한다.

주의: interpreter가 다른 Python을 가리키면 `reliability_lab`을 못 찾을 수 있다. 문제의 대부분은 코드가 아니라 interpreter/working directory 불일치다.

## 3. LinkedIn Projects에 연결 — 기본 권장 경로

LinkedIn 공식 도움말 기준으로 새 Project에는 별도 Project URL 필드가 없을 수 있다. 이때 `Add media > Add a link`를 사용한다.

1. LinkedIn 로그인 > `Me` > `View Profile`.
2. 소개 카드의 `Add profile section`.
3. `Recommended` > `Add projects`.
4. Project name: `C++/Python Reliability Simulation Lab`.
5. 시작일과 종료일은 실제 작업 기간만 입력한다.
6. Description에는 검증 가능한 사실만 넣는다. 예: C++17 Monte Carlo, Python 분석, Windows/Linux CI, deterministic parallel execution.
7. `Add media` > `Add a link`.
8. URL에 저장소 주소를 넣는다.
9. 미리보기 제목과 설명을 확인한 뒤 Save.
10. 로그아웃 창 또는 시크릿 창에서 프로필 노출을 확인한다.

## 4. Featured에 연결 — 보이는 계정만

1. `Add profile section` > `Recommended` > `Add Featured`.
2. Add 아이콘 > `Add a link`가 있으면 GitHub Release 또는 저장소 URL을 넣는다.
3. Featured가 없거나 링크 옵션이 제한되면 오류가 아니다. 계정/요금제/UI 차이일 수 있으므로 Projects 경로를 사용한다.
4. 공개 게시물을 만들지 않아도 외부 링크 작업 샘플을 지원하는 화면에서는 저장소를 연결할 수 있다.

## 5. Contact info에 연결 — 보조 경로

1. Profile 소개 카드 > `Contact info` > Edit.
2. `Add website`를 선택한다.
3. GitHub 저장소 URL을 입력하고 적절한 website type을 선택한다.
4. LinkedIn 공식 도움말은 최대 3개 웹사이트를 설명하지만 현재 계정 화면에서 제공되는 범위를 따른다.

## 6. 연결 성공 판정

다음 네 항목을 모두 만족해야 완료다.

- 프로필의 Projects 또는 Featured에서 링크를 클릭하면 공개 GitHub 저장소가 열린다.
- GitHub Actions 최신 실행이 성공이다.
- `v0.5.0` Release와 재현 가이드가 보인다.
- 설명의 모든 숫자가 저장소의 결과 JSON 또는 CI로 검증된다.

`Connect apps`에 CLion/PyCharm이 보이는지는 판정 항목이 아니다.

## 7. 절대 하지 말 것

- 회사 코드, 사내 장애 수치, 고객 데이터, token을 공개 저장소에 올리지 않는다.
- 2.39x는 이 PC에서 100,000회 실행을 한 한 번의 측정값이다. 모든 환경에서 보장한다고 쓰지 않는다.
- 교육용 rate를 실제 산업 고장률이라고 표현하지 않는다.
- LinkedIn 비밀번호나 session cookie를 IDE plugin 또는 스크립트에 넣지 않는다.
- 자동화가 LinkedIn 약관이나 UI를 우회하도록 만들지 않는다.
- 링크가 작동하는지 확인하지 않고 완료로 체크하지 않는다.

## 8. 문제 해결표

| 증상 | 의미 | 조치 |
|---|---|---|
| Connect apps에 CLion/PyCharm 없음 | 정상적인 제품 경계 | IDE는 JetBrains AI Chat에서 확인하고 LinkedIn에는 GitHub URL 연결 |
| Projects에 URL 칸 없음 | 현재 LinkedIn UI 동작 | `Add media > Add a link` 사용 |
| Featured 없음 | 계정/UI/요금제 차이 가능 | Projects와 Contact info 사용 |
| 링크가 404 | 저장소 비공개/URL 오타 | 로그아웃 상태에서 URL 재확인 |
| Python module not found | interpreter 또는 Sources Root 오류 | `.venv`와 `python` Sources Root 재설정 |
| 직렬/병렬 CSV 다름 | correctness regression | 공개 연결을 멈추고 CTest/CI부터 수정 |

## 9. 퇴근 후 완료 체크리스트

- [ ] CLion Release 빌드와 CTest 통과 화면 캡처
- [ ] PyCharm unittest 통과 화면 캡처
- [ ] capstone HTML 확인
- [ ] GitHub 저장소/Release/Actions 로그아웃 상태 확인
- [ ] LinkedIn Projects에 Add media 링크 연결
- [ ] 가능한 경우 Featured 또는 Contact info에 추가 연결
- [ ] 프로필에서 링크를 다시 클릭해 확인
- [ ] 공개 설명과 저장소 수치 대조

개인 화면 캡처는 계정 정보가 포함될 수 있으므로 Git에 commit하지 말고 본인 기기에만 보관한다.