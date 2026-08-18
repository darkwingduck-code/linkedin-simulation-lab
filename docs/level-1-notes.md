# Level 1 Notes

## 한 문장 설명

C++ 엔진이 고장·수리 사건을 Monte Carlo 방식으로 생성해 CSV로 내보내고, Python 계층이 결과 분포를 요약해 JSON 지표를 만든다.

## 데이터 흐름

~~~text
SimulationConfig → simulate → SimulationResult 목록 → write_csv
→ artifacts CSV → summarize → metrics → write_report → artifacts JSON
~~~

## 핵심 함수

1. simulate: 입력 검증 후 seed가 고정된 난수 생성기로 run별 고장과 복구를 계산한다.
2. write_csv: 결과를 언어 중립 CSV 계약으로 직렬화한다.
3. C++ main: 실행 인자, simulation, serialization, 오류 exit code를 연결한다.
4. summarize: CSV에서 availability와 failure 통계를 계산한다.
5. write_report: 분석 결과를 자동화 도구도 읽을 수 있는 JSON으로 저장한다.

## 모델 설명

고장까지의 시간과 수리 시간은 exponential distribution에서 표본을 얻는다. 고장률과 수리율이 일정하다는 memoryless 가정을 사용한다. availability는 uptime_hours / total_hours이며 uptime은 total hours - downtime이다.

## CSV 경계의 선택

장점은 추가 의존성이 없고 두 IDE에서 직접 검사하기 쉽다는 것이다. 단점은 schema와 타입 검증이 약하고 대용량 parsing 비용이 있다는 것이다. in-process 연동은 pybind11, 원격 호출은 API, 비동기 대규모 처리는 message queue를 검토한다.

## 자동 검증되는 불변조건

- 결과 수는 config.runs와 같다.
- 같은 seed는 같은 결과를 만든다.
- uptime과 downtime은 음수가 아니다.
- uptime + downtime은 관찰 시간과 같다.
- availability는 0과 1 사이다.

## Baseline

- 1,000 runs, seed 42
- Mean availability: 98.233%
- Fifth percentile availability: 93.286%
- Debug/Release CTest: pass
- Python unittest: pass

## 사람의 IDE 조작이 필요한 증거

- [ ] CLion debugger screenshot
- [ ] PyCharm debugger screenshot
- [ ] screenshots를 docs/evidence에 추가
- [ ] tracker에 링크 기록

자동 빌드는 debugger 조작 완료를 의미하지 않으므로 위 항목은 미완료로 유지한다.
