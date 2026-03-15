# 3dgs-maintenance

**대형 공간의 효율적 유지보수를 위한 확장 가능한 적응형 3D Gaussian Splatting 프레임워크**

Scalable Adaptive 3D Gaussian Splatting Framework for Efficient Maintenance of Large-Scale Spaces

---

## Overview

본 프로젝트는 대규모 실내 공간(예: 대학 건물)의 디지털 트윈을 3D Gaussian Splatting(3DGS) 기반으로 구축·유지보수하기 위한 파이프라인을 제안합니다.

핵심 아이디어는 **Block 단위 분할 학습 → Space 단위 통합·최적화 → 시점 기반 동적 로딩**의 3단계 전략으로, 타겟 디바이스의 VRAM과 연산 자원 제약 하에서도 끊김 없는 실시간 렌더링을 달성하는 것입니다.

### Key Contributions

- **Space-level Streaming**: 전체 Block의 Gaussian을 메모리에 올리지 않고, 유저 시점에 해당하는 Space만 동적으로 로드하여 렌더링
- **Overlapping Spaces**: Space 간 영역 중첩을 허용하여 시점 이동 시 seam 없는 자연스러운 전환 보장
- **Block → Space Consolidation**: 개별 Block 학습 결과를 적절한 범위로 묶어 인덱싱·Pruning 등 최적화를 수행하는 통합 파이프라인

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Pipeline Overview                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────────┐  │
│  │  Phase 1  │    │   Phase 2    │    │     Phase 3       │  │
│  │  Spatial  │───▶│  Per-Block   │───▶│  Block → Space    │  │
│  │ Partition │    │  3DGS Train  │    │  Consolidation    │  │
│  └──────────┘    └──────────────┘    └───────────────────┘  │
│                                              │               │
│                                              ▼               │
│                                      ┌───────────────┐      │
│                                      │    Phase 4     │      │
│                                      │  Viewpoint-    │      │
│                                      │  based Space   │      │
│                                      │  Streaming     │      │
│                                      └───────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Pipeline Details

### Phase 1 — Spatial Partitioning

건물의 구조적 정보(평면도, 방·복도 구분 등)를 활용하여 대규모 공간을 학습 가능한 Block 단위로 분할합니다.

- 평면도 또는 공간 경계 정보 기반 분할
- Block별 데이터 취득 경로 및 프로토콜 설계
- 분할 알고리즘 및 규칙은 연구 진행 중 확정 예정

### Phase 2 — Per-Block 3DGS Training

분할된 각 Block에 대해 독립적으로 3DGS 학습을 수행합니다.

- Block별 SfM → 3DGS 학습
- 전역 좌표계(Global Coordinate System) 정렬

### Phase 3 — Block → Space Consolidation

학습된 Block들을 적절한 범위로 묶어 **Space**를 구성합니다. Space는 렌더링 시 메모리 로딩의 기본 단위이며, Space 간 영역 중첩이 가능합니다.

- 인접 Block 통합 및 경계면 처리
- Octree 기반 공간 인덱싱
- Gaussian Pruning 및 압축
- LoD(Level of Detail) 구조 생성

### Phase 4 — Viewpoint-based Space Streaming

렌더링 시점에서 필요한 Space만 메모리에 로드하여 실시간 렌더링을 수행합니다.

- 유저 시점(카메라 위치·방향) → 필요 Space 판별
- Space 단위 동적 로드/언로드
- 중첩 영역을 통한 seamless transition

## Comparison with CityGaussian

| | CityGaussian | Ours |
|---|---|---|
| **분할 기준** | 균일 그리드 | 건물 구조 기반 (방·복도) |
| **통합 방식** | 전체 Block 동시 통합 | Block → Space 선택적 통합 |
| **렌더링 단위** | 전체 모델 | Space 단위 (동적 로딩) |
| **영역 중첩** | N/A | Space 간 중첩 허용 |
| **타겟 환경** | 고성능 GPU | 제한된 자원 환경 (웹 등) |

## Project Structure

```
3dgs-maintenance/
├── .gitignore
├── README.md
├── docs/
│   ├── README.md
│   └── research_plan.md        # 연구 계획서
├── src/
│   ├── README.md
│   ├── partition/              # Phase 1: 공간 분할
│   ├── train/                  # Phase 2: Block별 학습
│   ├── consolidation/          # Phase 3: Space 통합·최적화
│   └── streaming/              # Phase 4: 시점 기반 스트리밍
├── configs/                     # 실험 설정 파일
├── scripts/                     # 유틸리티 스크립트
└── data/                        # 데이터 (gitignored, scaffold tracked)
```

## Getting Started

> 🚧 본 프로젝트는 현재 초기 개발 단계입니다.

### Prerequisites

- All experiments were conducted on a single NVIDIA RTX PRO 4500 GPU (32GB VRAM)
- Python 3.10+
- CUDA 12.8
- PyTorch 2.7+

### Installation

```bash
git clone https://github.com/CNU26-3DGS/3dgs-maintenance.git
cd 3dgs-maintenance
python3 scripts/check_structure.py
```

## Team

**CNU26-3DGS** — 충남대학교 2026 졸업연구 팀

## References

- [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) (Kerbl et al., SIGGRAPH 2023)
- [CityGaussian: Real-time High-quality Large-Scale Scene Rendering with Gaussians](https://dekuliutesla.github.io/citygs/) (Liu et al., ECCV 2024)

## License

TBD
