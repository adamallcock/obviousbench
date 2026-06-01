"""Typed scorer gold fixture loading."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, StrictStr, ValidationError

from obviousbench.datasets.schemas import ScorerName


class ExpectedGoldDecision(BaseModel):
    """Expected deterministic scoring decision for a gold example."""

    model_config = ConfigDict(extra="forbid")

    answer_correct: bool
    format_correct: bool
    strict_correct: bool
    failure_type: StrictStr
    extracted: StrictStr | None = None


class ScorerGoldExample(BaseModel):
    """One hand-authored scorer gold contract example."""

    model_config = ConfigDict(extra="forbid")

    id: StrictStr
    scorer: StrictStr
    target: StrictStr
    output: StrictStr
    expected: ExpectedGoldDecision
    notes: StrictStr = ""


class ScorerGoldFixture(BaseModel):
    """Top-level YAML fixture document."""

    model_config = ConfigDict(extra="forbid")

    examples: list[ScorerGoldExample]


def load_gold_examples(paths: Iterable[Path]) -> list[ScorerGoldExample]:
    """Load and validate scorer gold examples from YAML fixture paths."""
    examples: list[ScorerGoldExample] = []
    seen_ids: set[str] = set()
    valid_scorers = {scorer.value for scorer in ScorerName}

    for path in paths:
        try:
            raw_fixture = yaml.safe_load(path.read_text(encoding="utf-8"))
            fixture = ScorerGoldFixture.model_validate(raw_fixture)
        except ValidationError as exc:
            raise ValueError(f"Invalid scorer gold fixture {path}: {exc}") from exc
        for example in fixture.examples:
            if example.id in seen_ids:
                raise ValueError(f"Duplicate scorer gold example id: {example.id}")
            if example.scorer not in valid_scorers:
                raise ValueError(
                    f"Unknown scorer in scorer gold example {example.id}: "
                    f"{example.scorer}"
                )
            seen_ids.add(example.id)
            examples.append(example)

    return examples
