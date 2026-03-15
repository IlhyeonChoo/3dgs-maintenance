# 연구 계획서: 대형 공간의 효율적 유지보수를 위한 확장 가능한 적응형 3DGS 프레임워크

## 1. 연구 개요

### 1.1 연구 목표

대규모 실내 공간(대학 건물 등)을 3D Gaussian Splatting(3DGS)으로 재구성하되, **타겟 디바이스의 VRAM 및 연산 자원 제약** 하에서도 실시간 렌더링이 가능한 파이프라인을 설계한다.

핵심 전략은 **렌더링 시 필요한 Gaussian의 수를 줄이는 것**이며, 이를 위해 공간을 구조적으로 분할·학습하고, 시점에 따라 필요한 범위만 메모리에 적재하는 Space-based Streaming 방식을 제안한다.

### 1.2 문제 정의

| 문제 | 설명 |
|------|------|
| VRAM 한계 | 대규모 공간의 전체 Gaussian을 동시에 메모리에 올리기 어려움 |
| 연산 부하 | 불필요한 Gaussian까지 렌더링 파이프라인에 포함되어 연산량 증가 |
| 경계면 단절 | 분할 학습 시 구역 경계에서 시각적 seam 발생 |
| 확장성 부재 | 기존 방식은 공간이 커질수록 리소스 요구량이 선형적으로 증가 |

### 1.3 제안 방법 요약

```
대규모 공간 → [공간 분할] → Block들 → [Block별 학습] → 학습된 Block들
    → [Block → Space 통합·최적화] → Overlapping Spaces
    → [시점 기반 Space Streaming] → 실시간 렌더링
```

---

## 2. 핵심 개념 정의

### 2.1 Block

- 공간 분할의 기본 단위
- 건물의 구조적 특성(방, 복도 등)을 반영하여 정의
- 각 Block은 독립적으로 3DGS 학습이 수행되는 단위

### 2.2 Space

- 하나 이상의 Block이 통합·최적화된 렌더링 로딩 단위
- **Space 간 영역 중첩(Overlap)이 가능** — 이를 통해 시점 전환 시 끊김 없는 렌더링 보장
- 인덱싱, Pruning, LoD 등의 최적화가 Space 수준에서 수행됨

### 2.3 Block vs Space 비교

| | Block | Space |
|---|---|---|
| 역할 | 학습 단위 | 렌더링 로딩 단위 |
| 정의 기준 | 물리적 공간 구조 | 렌더링 효율 + 시점 커버리지 |
| 중첩 여부 | 비중첩 (분할) | 중첩 가능 |
| 최적화 | 학습 시 기본 최적화 | 통합 후 인덱싱·Pruning·LoD |

---

## 3. 파이프라인 상세

### Phase 1: 공간 분할 (Spatial Partitioning)

**목표:** 대규모 공간을 학습 가능한 Block 단위로 나눈다.

**방법:**
- 건물 평면도 또는 식별 가능한 공간 구분(방, 복도 등)을 활용
- 각 Block의 경계와 데이터 취득 범위 정의
- Block 간 오버랩 촬영 영역을 설정하여 이후 통합 시 활용

**미결 사항:**
- 구체적인 분할 알고리즘 및 규칙은 추후 확정
- 자동화 수준 (수동 정의 vs. 알고리즘 기반) 결정 필요

**산출물:**
- Block 정의 목록 (경계 좌표, 포함 영역)
- Block별 데이터 취득 프로토콜

---

### Phase 2: Block별 3DGS 학습 (Per-Block Training)

**목표:** 각 Block에 대해 독립적으로 3DGS 모델을 학습한다.

**방법:**
- Block별 이미지 데이터로 SfM(Structure from Motion) 수행
- SfM 결과를 초기값으로 3DGS 학습
- 전역 좌표계 정렬을 통해 Block 간 기하학적 일관성 확보

**고려사항:**
- 전역 좌표계 정렬 전략: 전체 SfM 후 분할 vs. Block별 SfM 후 정합
- Block 경계 영역의 학습 품질 확보 (오버랩 촬영 데이터 활용)

**산출물:**
- Block별 학습된 3DGS 모델 (point cloud + Gaussian attributes)
- 전역 좌표계 기준 Block 위치 정보

---

### Phase 3: Block → Space 통합 및 최적화 (Consolidation)

**목표:** 학습된 Block들을 적절한 범위로 묶어 Space를 구성하고, 렌더링 효율을 위한 최적화를 수행한다.

**CityGaussian과의 차이:** CityGaussian은 모든 Block을 하나의 통합 모델로 합치는 반면, 본 연구는 **렌더링 시 필요한 범위 단위(Space)**로 선택적 통합을 수행한다.

**주요 작업:**
1. **Space 범위 결정**: 어떤 Block들을 하나의 Space로 묶을 것인지 결정
2. **경계면 처리**: Space 내부에서 Block 간 경계의 시각적 단절 해소
3. **공간 인덱싱**: Octree 등의 자료구조로 Gaussian의 공간적 검색 효율화
4. **Gaussian Pruning**: 불필요하거나 중복되는 Gaussian 제거
5. **LoD 생성**: 거리에 따른 상세도 레벨 구성

**Space 구성 원칙:**
- Space는 서로 겹칠 수 있음 (Overlap)
- 겹치는 영역은 시점 전환 시 seamless transition의 핵심
- Space의 크기는 타겟 디바이스의 메모리 제약에 맞춰 조절

**산출물:**
- Space 정의 (포함 Block 목록, 경계, 오버랩 영역)
- 최적화된 Space별 Gaussian 데이터
- 공간 인덱스 자료구조

---

### Phase 4: 시점 기반 Space Streaming (Viewpoint-based Rendering)

**목표:** 렌더링 시점에 따라 필요한 Space만 메모리에 로드하여 실시간 렌더링을 수행한다.

**동작 원리:**

```
[유저 시점 변경]
      │
      ▼
[현재 시점이 속한 Space 판별]
      │
      ▼
[필요 Space 로드 / 불필요 Space 언로드]
      │
      ▼
[로드된 Space의 Gaussian만으로 렌더링]
```

**핵심 메커니즘:**
- 유저의 카메라 위치·방향 정보로 필요 Space를 판별
- 현재 로드된 Space와 비교하여 로드/언로드 결정
- Space 간 오버랩 영역 덕분에 전환 시 빈 영역 없이 렌더링
- 전체 Gaussian이 아닌 Space 단위 Gaussian만 렌더링하여 연산량 절감

**기대 효과:**
- VRAM 사용량: 전체 모델 대비 대폭 감소 (활성 Space 크기에 비례)
- 렌더링 속도: 연산 대상 Gaussian 수 감소로 프레임 레이트 향상
- 확장성: 공간 규모가 커져도 동시 로드 Space 수는 제한적

---

## 4. 기존 연구와의 비교

### 4.1 CityGaussian (Liu et al., ECCV 2024)

- 균일 그리드 기반 분할 + 전체 통합 렌더링
- 모든 Block의 Gaussian을 한 번에 메모리에 적재
- 대규모 야외 씬 대상, 고성능 GPU 환경 전제
- **차이점:** 본 연구는 구조 기반 분할 + Space 단위 선택적 로딩으로 저사양 환경 지원

### 4.2 기존 LoD/Streaming 접근

- Octree 기반 LoD, frustum culling 등은 렌더링 단계에서의 최적화
- **차이점:** 본 연구는 학습 단계부터 구조적 분할을 수행하고, 학습-통합-렌더링 전 과정을 아우르는 통합 파이프라인 제안

---

## 5. 연구 일정 (예상)

| 단계 | 내용 | 기간 |
|------|------|------|
| Phase 1 | 공간 분석, Block 정의, 데이터 취득 | TBD |
| Phase 2 | Block별 SfM + 3DGS 학습 | TBD |
| Phase 3 | Space 통합, 인덱싱, Pruning, LoD | TBD |
| Phase 4 | Streaming 렌더러 구현 및 검증 | TBD |
| 최종 | 논문 작성 및 발표 | TBD |

---

## 6. 미결 사항 및 향후 결정 필요 항목

- [ ] 공간 분할 알고리즘/규칙 확정
- [ ] Space 구성 기준 구체화 (크기, 오버랩 비율 등)
- [ ] 전역 좌표계 정렬 전략 결정
- [ ] 경계면 블렌딩 방법 선정
- [ ] 타겟 디바이스 스펙 및 성능 목표 설정
- [ ] 평가 지표 정의 (PSNR, SSIM, FPS, VRAM 사용량 등)

---

## 7. 참고 문헌

- Kerbl, B., et al. "3D Gaussian Splatting for Real-Time Radiance Field Rendering." SIGGRAPH 2023.
- Liu, Y., et al. "CityGaussian: Real-time High-quality Large-Scale Scene Rendering with Gaussians." ECCV 2024.
