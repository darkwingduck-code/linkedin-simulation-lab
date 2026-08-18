# 기술 글: 재현 가능한 병렬 Monte Carlo 신뢰성 실험 만들기

단순한 병렬화는 빠르지만 thread scheduling에 따라 난수 소비 순서가 바뀌면 같은 seed에서도 결과가 달라진다. 이 프로젝트는 각 Monte Carlo run에 `base seed + run identity`로 구성한 독립 seed sequence를 부여했다. worker는 서로 다른 result slot만 기록하며, 최종 vector 순서는 run id 순서로 고정된다. 따라서 worker 수는 실행 시간만 바꾸고 결과는 바꾸지 않는다.

정확성은 “평균이 비슷하다”로 판정하지 않았다. C++ test에서 1-thread와 4-thread의 각 run 결과를 비교하고, capstone workflow에서는 생성 CSV 전체의 byte equality를 검사한다. 2026-08-18 개발 장비의 100,000회 실행은 0.6768초에서 0.2828초로 줄어 2.39x를 기록했다. 연속 측정에서는 2.39x~3.50x로 변동했다. 문서에는 최신 재현값을 고정했으며 이 값은 환경 의존 측정이지 보장 수치가 아니다.

Python 단계는 failure rate와 repair rate를 각각 변화시킨 다섯 scenario를 실행한다. 평균 가용성, 하위 5% 가용성, 평균의 95% 신뢰구간을 versioned JSON과 dependency-free HTML/SVG로 남긴다. 교육용 가정에서는 복구 속도가 느려질 때 손실이 크게 나타났지만 실제 권고 전에는 조직의 incident data로 rate를 보정해야 한다.

Level 1에서는 “코드가 실행된다”가 목표였다. Level 5에서는 문제, provenance, deterministic concurrency, uncertainty, CI, release, 한계, 의사결정 권고를 하나의 감사 가능한 경로로 연결했다. 성숙도의 차이는 코드 줄 수가 아니라 결과를 어디까지 신뢰할 수 있는지 설명하는 능력에 있다.