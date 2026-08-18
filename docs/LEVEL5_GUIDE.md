# Level 5 Capstone Guide

## 문제와 의사결정

이 capstone은 1년(8,760시간) 동안 repairable service 하나의 가용성을 추정하고, failure 발생 빈도를 줄이는 투자와 repair 시간을 줄이는 투자 중 어느 쪽을 우선 검토할지 지원한다. 성공 기준은 100,000회 Monte Carlo 실험을 재현하고, 4-thread 결과가 1-thread 결과와 정확히 같으며, 민감도와 95% 평균 신뢰구간을 versioned JSON/HTML로 남기는 것이다.

이 결과는 실제 운영 SLO나 안전 인증이 아니다. 공개 실측 데이터가 아니라 교육용 가정으로 model behavior와 engineering workflow를 검증한다.

## Parameter provenance

| Parameter | Baseline | 범위 | 출처/성격 |
|---|---:|---:|---|
| horizon | 8,760 h | 고정 | 1 calendar year 정의 |
| failure rate | 0.0015/h | 0.0010–0.0020 | 교육용 calibrated assumption; Level 1 baseline에서 계승 |
| repair rate | 0.08/h | 0.05–0.12 | 교육용 calibrated assumption; 평균 repair time `1/rate` 비교용 |
| runs | 100,000 | 고정 | Monte Carlo sampling error와 실행 시간의 실용적 절충 |
| seed | 20260818 | 고정 | 재현용, 현재 실험일 기반 |
| threads | 4 | 1과 비교 | 현재 개발 장비의 bounded worker 수 |

Rate는 외부 설비의 관측값이 아니다. 실제 의사결정에는 incident/maintenance data로 calibration하고 독립적인 validation을 해야 한다.

## 실행

```powershell
.\scripts\run-capstone.ps1
```

또는 이미 빌드했다면:

```powershell
$env:PYTHONPATH = "$PWD\python"
python -m reliability_lab.capstone --simulator .\build\reliability_simulator.exe --output-dir artifacts\capstone --runs 100000 --threads 4
```

산출물:

- `capstone-results.json`: contract version, timing, exact-match flag, scenario metrics
- `capstone-report.html`: sensitivity/uncertainty visualization
- scenario CSV: 재실행 시 생성되는 중간 자료이며 Git에는 넣지 않음

## 2026-08-18 측정 결과

- serial: 0.6768 s
- 4-thread: 0.2828 s
- measured speedup: 2.39x
- serial/parallel CSV: byte-for-byte exact match
- baseline mean availability: 0.981640
- slow repair mean availability: 0.970935
- fast repair mean availability: 0.987665

연속 측정에서 speedup이 2.39x~3.50x로 변동했으므로 최신 재현값 2.39x를 증거로 고정했으며 일반화는 금지한다. CI는 정확성과 실행 성공을 검사하고, hardware-specific 성능 주장은 각 장비에서 다시 측정한다.

## Engineering recommendation

이 교육용 범위에서는 baseline 대비 repair-fast 시나리오의 mean availability 상승 폭이 failure-low와 거의 비슷하고, repair-slow의 하락 폭이 더 크다. 따라서 실제 조직에서는 먼저 MTTR 분포와 복구 병목의 실측 데이터를 수집하고, repair 자동화의 비용 대비 효과를 failure prevention 투자와 함께 비교하는 것을 권고한다. simulator 결과만으로 투자 결정을 확정하지 않는다.

## 신뢰하면 안 되는 범위

- 고장과 복구 시간이 독립적인 지수분포가 아닌 시스템
- common-cause failure, load dependency, maintenance window, redundancy가 중요한 시스템
- non-stationary rate 또는 계절성이 있는 데이터
- 인명/환경 안전 판단과 규제 인증
- parameter calibration 없이 실제 SLA 비용을 산출하는 용도
- 평균 가용성만으로 tail risk를 충분히 설명한다고 보는 경우

100배 규모에서는 CSV I/O와 결과 메모리, scenario orchestration이 먼저 병목이 될 가능성이 높다. 다음 설계는 streaming aggregation, chunked output, process-level scenario parallelism을 검토한다.

## Self-review 3회

1. Correctness review: run별 deterministic seed로 thread scheduling과 결과를 분리하고 C++ test 및 byte comparison으로 검증했다.
2. Statistical review: mean만 제시하지 않고 p05와 mean의 95% CI를 함께 기록했다. scenario 간 seed 차이는 독립 sample을 위한 선택이다.
3. Communication/safety review: parameter를 실제 관측값으로 오인하지 않게 provenance와 trust boundary를 명시하고 recommendation을 조건부로 작성했다.

## 재현 감사

- [x] clean checkout에서 CMake build 가능
- [x] Windows/Linux CI
- [x] CTest/unittest/lint/mypy/clang-tidy/sanitizer
- [x] fixed seed와 versioned exchange contract
- [x] serial/parallel exact equality gate
- [x] one-command capstone workflow
- [x] 공개 입력 가정과 한계
- [ ] 다른 사람이 독립 장비에서 실행 후 결과 링크 제출
- [ ] LinkedIn Projects 링크를 사용자가 직접 확인

마지막 두 항목은 외부 사람/사용자 계정 작업이므로 자동 완료로 표시하지 않는다.