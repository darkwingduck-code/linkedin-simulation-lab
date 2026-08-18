# C++/CLion + Python/PyCharm Level 5 Roadmap

## Level 5의 정의

이 문서의 Level 5는 JetBrains의 공식 등급이 아니다. 혼자서 문제 정의, 설계, 구현, 테스트, 자동화, 측정, 배포를 수행하고 선택의 근거를 설명할 수 있는 포트폴리오 역량 등급이다. 강의 시청이나 코드 복사는 완료로 인정하지 않으며 코드, 테스트, 문서, 실행 증거가 Git에 남아야 한다.

권장 기간은 10주, 주당 6~8시간이다. 모든 작업은 `level/<단계>-<주제>` 브랜치와 PR로 진행한다.

## Level 1 — 실행하고 설명하기

목표: 기존 파이프라인을 이해하고 두 IDE에서 도움 없이 실행·디버깅한다.

### CLion / C++

1. 저장소 루트를 CMake 프로젝트로 연다.
2. Debug와 Release에서 `reliability_simulator`, `reliability_tests`를 빌드한다.
3. `simulate`에 중단점을 걸고 `clock`, `downtime`, `failures`를 관찰한다.
4. 지수분포 기반 고장·복구 모델을 자기 말로 설명한다.
5. 코드를 수정하지 않고 실행 인자로 seed와 runs를 바꾼다.

### PyCharm / Python

1. Python 3.10+ 인터프리터를 만들고 `python`을 Sources Root로 지정한다.
2. `reliability_lab.cli`와 unittest를 PyCharm에서 실행한다.
3. `summarize`를 디버깅하며 CSV rows와 percentile 계산을 관찰한다.
4. C++와 Python 사이의 CSV 계약을 설명한다.
5. 같은 seed로 같은 결과가 재현되는지 확인한다.

통과 기준:

- 두 IDE의 디버거 화면 또는 짧은 녹화
- `docs/level-1-notes.md`에 데이터 흐름과 핵심 함수 5개 설명
- CTest와 unittest 성공 로그

## Level 2 — 안전하게 확장하기

목표: 기존 동작을 깨뜨리지 않고 기능을 추가한다.

필수 구현:

1. C++ 위치 인자를 `--runs`, `--seed`, `--hours`, `--failure-rate`, `--repair-rate` 옵션으로 교체
2. 범위 검증과 이해하기 쉬운 오류 메시지
3. Python에 중앙값, 표준편차, downtime 95분위수 추가
4. 빈 파일, 잘못된 행, 0 rate, 극단값 테스트
5. `docs/data-contract.md`에 CSV 스키마 문서화
6. C++에 `-Wall -Wextra -Wpedantic`, Python에 타입 검사 적용

통과 기준:

- 두 언어 합계 10개 이상의 집중된 테스트
- 컴파일러 경고 0개
- Python 타입 검사 통과
- PR에 채택하지 않은 대안 하나와 이유 기록

## Level 3 — 시스템으로 설계하기

목표: 단순 스크립트를 모듈화된 애플리케이션으로 발전시킨다.

필수 구현:

1. configuration, event, result를 명시적 도메인 타입으로 분리
2. simulation, validation, serialization, CLI 책임 분리
3. 버전이 명시된 JSON 출력 추가
4. 여러 시나리오를 비교하는 Python 명령 추가
5. 표와 차트 2개 이상이 포함된 HTML 보고서 생성
6. C++ 처리량과 Python 분석 지연시간 benchmark
7. end-to-end 테스트로 실행 파일부터 보고서까지 검증

답해야 할 질문:

- 파일 계약이 적합한 이유와 pybind11/API/message queue가 더 나은 시점은?
- seed와 표본 수가 재현성과 신뢰도에 어떤 영향을 주는가?
- 사용자 입력, 인프라, 프로그래머 오류를 어떻게 구분하는가?
- 언어 경계와 도메인 경계는 어떻게 다른가?

통과 기준:

- `docs/adr/`의 Architecture Decision Record
- 장비·컴파일러 정보가 포함된 benchmark baseline
- 자동 end-to-end 테스트
- 2분 분량 전체 파이프라인 데모

## Level 4 — 프로덕션 엔지니어링

목표: 다른 개발자와 자동화 시스템이 신뢰할 수 있게 만든다.

필수 구현:

1. Windows/Linux GitHub Actions
2. CTest, unittest, lint, type check, static analysis
3. 지원되는 컴파일러에서 sanitizer 실행
4. Python CLI 패키징과 버전이 있는 C++ release artifact
5. 구조화 로그, exit code, 장애 진단 문서
6. property/invariant 기반 무작위 테스트
7. 성능 회귀 기준
8. 신뢰하지 않는 파일, 경로 처리, 자원 고갈, 의존성 위험 문서화

통과 기준:

- 운영체제 2개 이상에서 CI 성공
- 재현 절차가 있는 tagged release
- 의도적으로 결함을 주입하고 탐지·진단·수정한 incident drill
- 커밋 목록이 아니라 사용자 효과를 설명하는 release note

## Level 5 — 시스템을 소유하고 가르치기

목표: 실제 의사결정을 지원하는 capstone과 기술 리더십 증거를 만든다.

Capstone 후보: 데이터센터 냉각계통, 수소 배관 구성요소 또는 분산 서비스.

필수 구현:

1. 문제 정의와 측정 가능한 성공 기준
2. 공개 자료 또는 보정된 parameter와 출처
3. 병렬 C++ simulation, 정확성 비교, 측정된 speedup
4. Python sensitivity analysis와 uncertainty visualization
5. 안정적이고 버전이 있는 교환 계약
6. CI, release, 문서, 재현 가능한 실험
7. 모델을 신뢰하면 안 되는 범위
8. 단순 데모가 아닌 결과 기반 엔지니어링 권고

10분 발표에서 답할 내용:

- 어떤 의사결정을 지원하는가?
- 결과를 지배하는 가정은 무엇인가?
- 구현이 충분히 정확함을 어떻게 증명했는가?
- 어떤 병목을 측정하고 개선했는가?
- 100배 규모에서 무엇이 먼저 실패하는가?
- 시간이 더 있다면 무엇을 다시 설계할 것인가?

통과 기준:

- 외부 리뷰 PR 3개 또는 문서화된 self-review 3회
- 공개 tagged release와 완전한 재현 가이드
- README에서 test/static analysis/benchmark 증거 연결
- 기술 글 1개, 데모 1개, LinkedIn 프로젝트 업데이트 1개
- Level 1과 capstone 설계를 비교한 retrospective

## 10주 실행 계획

| 주 | 결과 | 단계 |
|---|---|---|
| 1 | IDE 설정, 디버깅, 구조 설명 | L1 |
| 2 | CLI 옵션과 입력 검증 | L2 |
| 3 | 분석 지표와 edge-case 테스트 | L2 |
| 4 | 도메인 리팩터링과 JSON 계약 | L3 |
| 5 | 시나리오 비교와 HTML 보고서 | L3 |
| 6 | benchmark와 ADR | L3 |
| 7 | cross-platform CI와 품질 검사 | L4 |
| 8 | 패키징, release, incident drill | L4 |
| 9 | capstone, 병렬화, 민감도 분석 | L5 |
| 10 | 재현성 감사, 기술 글, 데모 | L5 |

## 매주 반복할 루프

1. tracker에서 미완료 항목 하나를 선택한다.
2. acceptance criteria가 있는 GitHub issue를 만든다.
3. 전용 branch에서 CLion 또는 PyCharm으로 구현한다.
4. 테스트를 추가하고 `scripts/run.ps1`을 실행한다.
5. PR에 무엇을 바꿨고 무엇을 측정했으며 무엇을 배웠는지 기록한다.
6. diff를 correctness, readability, scope 관점으로 검토한다.
7. merge 후 tracker와 증거 링크를 갱신한다.

LinkedIn에는 저장소로 입증 가능한 주장만 쓴다. “고급 C++를 학습했다”보다 “100,000회 실행 시간을 X에서 Y로 줄였고 N개 불변조건으로 검증했다”처럼 측정 가능한 표현을 사용한다.
