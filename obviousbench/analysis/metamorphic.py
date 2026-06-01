"""Metamorphic group consistency analysis."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

from obviousbench.analysis.metrics import EvalRecord


@dataclass(frozen=True)
class MetamorphicConsistencyRow:
    run_variant: str
    model: str
    family: str
    metamorphic_group_id: str
    metamorphic_relation: str
    samples: int
    scored_samples: int
    assessable: bool
    all_correct: bool
    all_incorrect: bool
    mixed_outcomes: bool
    consistent: bool


def compute_metamorphic_consistency(
    records: list[EvalRecord],
) -> list[MetamorphicConsistencyRow]:
    grouped: dict[tuple[str, str, str, str, str], list[EvalRecord]] = defaultdict(list)
    for record in records:
        if not record.metamorphic_group_id:
            continue
        key = (
            record.run_variant,
            record.model,
            record.family,
            record.metamorphic_group_id,
            record.metamorphic_relation,
        )
        grouped[key].append(record)

    rows: list[MetamorphicConsistencyRow] = []
    for key, group_records in sorted(grouped.items()):
        run_variant, model, family, group_id, relation = key
        scored = [
            record
            for record in group_records
            if not record.provider_error and not record.timeout
        ]
        scored_outcomes = {record.correct for record in scored}
        assessable = len(scored) >= 2
        all_correct = bool(scored) and scored_outcomes == {True}
        all_incorrect = bool(scored) and scored_outcomes == {False}
        mixed_outcomes = len(scored_outcomes) > 1
        rows.append(
            MetamorphicConsistencyRow(
                run_variant=run_variant,
                model=model,
                family=family,
                metamorphic_group_id=group_id,
                metamorphic_relation=relation,
                samples=len(group_records),
                scored_samples=len(scored),
                assessable=assessable,
                all_correct=all_correct,
                all_incorrect=all_incorrect,
                mixed_outcomes=mixed_outcomes,
                consistent=assessable and not mixed_outcomes,
            )
        )
    return rows


def export_metamorphic_consistency_csv(
    rows: list[MetamorphicConsistencyRow],
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_variant",
        "model",
        "family",
        "metamorphic_group_id",
        "metamorphic_relation",
        "samples",
        "scored_samples",
        "assessable",
        "all_correct",
        "all_incorrect",
        "mixed_outcomes",
        "consistent",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
