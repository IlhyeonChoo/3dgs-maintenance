# Phase 1: Spatial Partitioning

이 디렉터리는 대규모 실내 공간을 학습 가능한 Block 단위로 분할하는 코드를 담습니다.

## Expected Inputs

- 건물 평면도
- 방/복도/계단 등의 구조 정보
- 촬영 이미지 또는 촬영 계획 메타데이터

## Expected Outputs

- Block 정의 manifest
- Block별 overlap 구간 정보
- Block별 데이터 취득 계획

## Initial Implementation Targets

- 수동 정의 기반 Block manifest 생성기
- 구조 기반 분할 규칙 실험 코드
- 분할 결과 시각화 도구
