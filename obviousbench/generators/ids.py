"""Stable item ID helpers."""

from obviousbench.datasets.schemas import FAMILY_SHORT_NAMES, SPLIT_SHORT_NAMES


def make_id(family: str, split: str, index: int) -> str:
    try:
        family_short = FAMILY_SHORT_NAMES[family]
    except KeyError as exc:
        raise ValueError(f"Unknown family: {family}") from exc
    try:
        split_short = SPLIT_SHORT_NAMES[split]
    except KeyError as exc:
        raise ValueError(f"Unknown split: {split}") from exc
    if index < 1:
        raise ValueError("index must be positive")
    return f"obviousbench.{family_short}.en.v0.{split_short}.{index:06d}"

