# Phase 3: Block to Space Consolidation

이 디렉터리는 Block 결과를 Space 단위로 묶고, 렌더링 효율을 높이기 위한 최적화를 담당합니다.

## Expected Inputs

- Block별 Gaussian 자산
- Block 위치 및 정렬 정보
- Space 구성 정책

## Expected Outputs

- Space 정의 manifest
- Space별 최적화된 Gaussian 자산
- 검색 및 로딩을 위한 인덱스 데이터

## Initial Implementation Targets

- Block 묶음 규칙 설계
- overlap 경계 처리 실험
- pruning / LoD / indexing 파이프라인 골격
