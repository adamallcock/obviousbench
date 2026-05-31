"""Generator helpers."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from obviousbench.datasets.schemas import BenchmarkItem


def write_jsonl(items: Iterable[BenchmarkItem], path: Path, *, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        json.dumps(item.model_dump(mode="json"), ensure_ascii=False, sort_keys=True)
        for item in items
    ]
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
