# Phase 4: Viewpoint-based Space Streaming

이 디렉터리는 현재 시점에 필요한 Space만 메모리에 유지하기 위한 로직을 다룹니다.

## Expected Inputs

- Space manifest
- Space별 bounding metadata
- 카메라 pose 및 시야 정보

## Expected Outputs

- 현재 프레임에서 필요한 Space 목록
- 로드 / 언로드 결정
- 스트리밍 성능 측정 결과

## Initial Implementation Targets

- 시점 기반 활성 Space 판별기
- prefetch 및 eviction 정책 실험
- VRAM / FPS 측정용 시뮬레이터
