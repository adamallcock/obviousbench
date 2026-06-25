"""Dataset loading and Inspect sample conversion."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from inspect_ai.dataset import Sample

from obviousbench.datasets.schemas import BenchmarkItem


def load_benchmark_jsonl(path: Path | str, *, allow_empty: bool = False) -> list[BenchmarkItem]:
    """Load benchmark items from a local JSONL file."""
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file does not exist: {dataset_path}")

    items = [
        BenchmarkItem.model_validate(json.loads(line))
        for line in dataset_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not items and not allow_empty:
        raise ValueError(f"Dataset file is empty: {dataset_path}")
    return items


def to_sample(item: BenchmarkItem) -> Sample:
    """Convert a benchmark item into an Inspect sample."""
    return Sample(
        id=item.id,
        input=item.prompt,
        target=item.target,
        metadata={
            "family": item.family,
            "subfamily": item.subfamily,
            "answer_type": item.answer_type,
            "scorer": item.scorer,
            "split": item.split,
            "source_type": item.source_type,
            "source_refs": item.source_refs,
            "human_triviality": item.human_triviality,
            "review_status": item.review_status,
            "benchmark_metadata": item.metadata.model_dump(mode="json"),
        },
    )


def to_samples(items: Iterable[BenchmarkItem]) -> list[Sample]:
    return [to_sample(item) for item in items]
