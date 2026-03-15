# Source Layout

소스 코드는 파이프라인 단계 기준으로 분리합니다.

## Directories

- `partition/`: 공간 구조를 바탕으로 Block을 정의하는 로직
- `train/`: Block별 SfM/3DGS 학습 실행과 결과 정리
- `consolidation/`: Block 결과를 Space 단위로 묶고 최적화하는 로직
- `streaming/`: 시점 기반 Space 로딩/언로딩 및 렌더링 의사결정 로직

## Design Rule

- 각 디렉터리는 `입력 포맷`, `핵심 처리`, `산출물 포맷`을 먼저 정의한 뒤 구현합니다.
- 초기 단계에서는 스크립트보다 메타데이터 스키마와 실행 계약을 먼저 고정하는 것이 좋습니다.
- 구현이 시작되면 공통 타입과 유틸리티는 별도 공용 모듈로 분리하는 것을 권장합니다.
