# Level 5 Progress Tracker

완료 체크는 같은 PR 안의 commit, test report, benchmark, 글 또는 demo 링크를 근거로 한다.

## Level 1

- [x] CLion Debug/Release 빌드
- [ ] C++ debugger walkthrough
- [ ] PyCharm CLI 및 테스트 실행
- [ ] Python debugger walkthrough
- [x] 데이터 흐름 설명 문서
- [x] Baseline CTest와 unittest 통과

## Level 2

- [x] Named C++ CLI options
- [x] 입력 검증과 오류 테스트
- [x] 확장된 Python 통계
- [x] 집중 테스트 10개 이상
- [x] C++ warning-clean build
- [x] Python type-checking gate
- [x] 데이터 계약 문서

## Level 3

- [x] 도메인 중심 모듈 경계
- [x] Versioned JSON output
- [x] Multi-scenario comparison
- [x] HTML report와 charts
- [x] End-to-end process test
- [x] Benchmark baseline
- [x] Architecture Decision Records

## Level 4

- [ ] Windows/Linux CI
- [ ] Lint/type/static analysis
- [ ] Sanitizer
- [ ] Packaged Python CLI
- [ ] Versioned C++ artifacts
- [ ] Property/invariant tests
- [ ] Performance regression gate
- [ ] Security/failure-mode 문서
- [ ] Tagged release와 incident drill

## Level 5

- [ ] Capstone 문제와 성공 기준
- [ ] Parameter provenance
- [ ] 병렬 simulator와 측정된 speedup
- [ ] Sensitivity/uncertainty analysis
- [ ] 재현 가능한 실험 workflow
- [ ] Limitations/trust-boundary 분석
- [ ] Engineering recommendation
- [ ] 리뷰 PR 또는 self-review 3회
- [ ] Public release와 reproduction audit
- [ ] 기술 글, demo, LinkedIn 업데이트
- [ ] Final retrospective

## Evidence log

| 날짜 | 단계 | 증거 | 링크 |
|---|---:|---|---|
| 2026-08-18 | Baseline | C++/Python 테스트와 1,000회 통합 실행 | Commit f6da7d3 |
| 2026-08-18 | L1 | Debug/Release build, tests, data-flow notes | scripts/run-level1.ps1 |
| 2026-08-18 | L2 | Named CLI, validation, 12 automated tests, warning/type gates, data contract | Level 2 delivery commit |
| 2026-08-18 | L3 | JSON contract, scenario comparison, HTML/SVG, E2E, benchmark, ADR | Level 3 delivery commit |
