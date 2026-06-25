"""Canonical dataset path resolution helpers."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SPLIT_DIR_ALIASES: dict[str, Path] = {
    "calibration_v0": Path("benchmark/calibration/v0"),
    "dev_regression": Path("benchmark/regression"),
    "public_examples": Path("public_examples"),
    "public_v0": Path("public_examples"),
}


def data_root(data_dir: Path | str | None = None) -> Path:
    """Return the configured data root."""
    return Path(data_dir) if data_dir is not None else PROJECT_ROOT / "data"


def split_dir_path(split: str, *, data_dir: Path | str | None = None) -> Path:
    """Resolve a split name while preserving legacy tmpdir fallbacks."""
    root = data_root(data_dir)
    canonical_path = root / SPLIT_DIR_ALIASES.get(split, Path(split))
    legacy_path = root / split
    if canonical_path.exists() or not legacy_path.exists():
        return canonical_path
    return legacy_path


def split_file_path(
    split: str,
    family_file: str,
    *,
    data_dir: Path | str | None = None,
) -> Path:
    """Resolve a family JSONL file within a split directory."""
    return split_dir_path(split, data_dir=data_dir) / family_file
