#!/usr/bin/env python3

from pathlib import Path
import sys


REQUIRED_PATHS = [
    "README.md",
    ".gitignore",
    "docs/README.md",
    "docs/research_plan.md",
    "src/README.md",
    "src/partition/README.md",
    "src/train/README.md",
    "src/consolidation/README.md",
    "src/streaming/README.md",
    "configs/README.md",
    "configs/partition.template.yaml",
    "configs/train.template.yaml",
    "configs/consolidation.template.yaml",
    "configs/streaming.template.yaml",
    "scripts/README.md",
    "data/README.md",
    "data/raw/.gitkeep",
    "data/interim/.gitkeep",
    "data/processed/.gitkeep",
    "data/exports/.gitkeep",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_PATHS if not (repo_root / path).exists()]

    if missing:
        print("Missing repository paths:", file=sys.stderr)
        for path in missing:
            print(f" - {path}", file=sys.stderr)
        return 1

    print("Repository scaffold is complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
