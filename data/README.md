# Data Layout

실제 데이터와 대용량 산출물은 Git에 포함하지 않습니다.

## Directories

- `raw/`: 원본 이미지, 평면도, 메타데이터
- `interim/`: 분할 결과, 중간 manifest, 정렬 전 결과
- `processed/`: 학습 완료 Block 및 Space 자산
- `exports/`: 시각화, 리포트, 성능 측정 결과

## Notes

- 실제 데이터 파일은 `.gitignore`로 제외됩니다.
- 각 하위 디렉터리의 `.gitkeep`은 구조 유지를 위한 placeholder입니다.
