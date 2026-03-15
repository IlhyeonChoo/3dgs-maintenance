# Phase 2: Per-Block Training

이 디렉터리는 Block 단위의 SfM 및 3DGS 학습 파이프라인을 다룹니다.

## Expected Inputs

- Block별 이미지 집합
- 카메라 메타데이터
- Phase 1에서 생성한 Block manifest

## Expected Outputs

- SfM 결과
- Block별 학습된 Gaussian 자산
- 전역 좌표계 기준 정렬 정보

## Initial Implementation Targets

- Block별 학습 실행 wrapper
- 학습 결과 표준 디렉터리 구조 정의
- Block 모델 품질 점검 유틸리티
