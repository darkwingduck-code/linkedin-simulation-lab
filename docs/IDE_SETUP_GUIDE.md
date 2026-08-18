# Level 1 IDE Setup and Debugging Guide

이 가이드는 저장소를 CLion과 PyCharm에서 처음부터 실행하고 디버깅하는 절차를 클릭 단위로 설명한다.

## 준비 및 기준 검증

- 로컬 경로: C:\Users\sadva\linkedin-simulation-lab
- GitHub: https://github.com/darkwingduck-code/linkedin-simulation-lab
- CLion/PyCharm 2026.2.1, Python 3.10 이상

PowerShell에서 다음을 실행한다.

~~~powershell
cd C:\Users\sadva\linkedin-simulation-lab
git pull
.\scripts\run-level1.ps1
~~~

마지막 줄은 LEVEL1_VERIFICATION=PASS여야 한다.

## CLion 설정

1. File → Open에서 저장소 루트를 선택한다.
2. CMake project로 열겠다는 안내를 승인한다.
3. Settings → Build, Execution, Deployment → CMake로 이동한다.
4. CMakePresets.json의 debug와 release profile을 활성화한다.
5. 우측 target에서 reliability_simulator를 선택하고 Build Project를 실행한다.
6. reliability_tests target도 실행해 모든 테스트가 통과하는지 확인한다.

## CLion 디버깅

1. cpp/src/reliability.cpp를 연다.
2. run loop 시작 줄에 breakpoint를 건다.
3. reliability_simulator의 Program arguments를 다음으로 설정한다.

~~~text
artifacts/clion-debug.csv 3 42
~~~

4. Debug로 실행한다.
5. Variables에서 run, clock, downtime, failures를 관찰한다.
6. Step Over로 고장 시간과 수리 시간이 누적되는 과정을 확인한다.
7. Watches에 config.hours - downtime과 downtime / config.hours를 추가한다.
8. 종료 후 artifacts/clion-debug.csv를 확인한다.

관찰할 불변조건:

- clock은 감소하지 않는다.
- downtime은 음수가 아니다.
- uptime + downtime은 configured hours와 같다.
- availability는 0과 1 사이이다.
- 같은 설정과 seed는 같은 결과를 만든다.

## PyCharm 설정

1. File → Open에서 같은 저장소 루트를 연다.
2. Settings → Project → Python Interpreter에서 Python 3.10+ virtual environment를 만든다.
3. python 폴더를 우클릭해 Mark Directory as → Sources Root를 선택한다.
4. Run → Edit Configurations에서 Python configuration을 만든다.
5. Module name은 reliability_lab.cli로 설정한다.
6. Parameters는 다음과 같이 입력한다.

~~~text
artifacts/simulation.csv --output artifacts/summary.json
~~~

7. Working directory는 저장소 루트다.
8. 환경변수 PYTHONPATH는 $PROJECT_DIR$/python으로 설정한다.
9. 실행해 평균 availability와 JSON 생성 메시지를 확인한다.

## PyCharm 테스트와 디버깅

1. Python tests → Unittests configuration을 만든다.
2. Target은 python/tests, Working directory는 저장소 루트다.
3. PYTHONPATH를 $PROJECT_DIR$/python으로 설정하고 테스트한다.
4. python/reliability_lab/analytics.py를 연다.
5. rows를 읽는 줄과 return 줄에 breakpoint를 건다.
6. CLI configuration을 Debug로 실행한다.
7. rows, availability, failures, ordered, p05_index를 관찰한다.
8. Evaluate Expression에서 다음을 평가한다.

~~~python
min(availability), max(availability), sum(availability) / len(availability)
~~~

9. artifacts/summary.json과 console 결과가 일치하는지 확인한다.

## 문제 해결

- cmake를 찾지 못함: scripts/run-level1.ps1을 사용한다. CLion bundled toolchain을 자동 탐색한다.
- No module named reliability_lab: python을 Sources Root로 지정하고 PYTHONPATH를 확인한다.
- CSV가 없음: Python 분석 전에 C++ simulator를 실행한다.
- 결과가 다름: seed, runs, hours, failure/repair rate가 같은지 확인한다.

## 제출 증거

- docs/evidence/level1-clion-debug.png
- docs/evidence/level1-pycharm-debug.png
- docs/level-1-notes.md
- 성공한 PR 또는 commit 링크

스크린샷에는 토큰, 이메일 등 민감정보가 노출되지 않도록 한다.
