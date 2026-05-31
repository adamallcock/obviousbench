"""Balanced barrage profile selection."""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from obviousbench.datasets.load import load_benchmark_jsonl
from obviousbench.datasets.schemas import BenchmarkItem, Family

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROFILE_RE = re.compile(
    r"^(?P<strategy>balanced|hard_obvious)_(?P<families>\d+)x(?P<per_family>\d+)$"
)
FAMILY_ORDER = tuple(family.value for family in Family)
HARD_SUBFAMILY_ORDER = {
    "arithmetic": (
        "numeric_comparison",
        "unit_conversion_and_small_calc",
        "small_integer_arithmetic",
    ),
    "character_count": ("single_letter_count",),
    "constraint_awareness": ("object_must_be_present",),
    "format_compliance": (
        "exact_json_schema",
        "json_field",
        "instruction_conflict",
        "only_yes_no",
    ),
    "negation": ("without_constraint", "not_choice"),
    "ordering": ("numeric_sort", "alphabetical_sort"),
    "spelling_transform": ("remove_letter", "replace_letter", "reverse_word"),
    "word_count": ("comma_list_count", "sentence_word_count"),
}


@dataclass(frozen=True)
class BarrageProfile:
    """A family-balanced benchmark barrage recipe."""

    name: str
    family_count: int
    per_family: int
    strategy: str = "balanced"

    @classmethod
    def parse(cls, value: str) -> BarrageProfile:
        match = PROFILE_RE.fullmatch(value)
        if not match:
            raise ValueError(
                "Unknown barrage profile. Expected a name like balanced_8x10 "
                "or hard_obvious_8x10."
            )
        strategy = match.group("strategy")
        family_count = int(match.group("families"))
        per_family = int(match.group("per_family"))
        if family_count < 1 or per_family < 1:
            raise ValueError("Barrage profile counts must be positive.")
        return cls(
            name=value,
            family_count=family_count,
            per_family=per_family,
            strategy=strategy,
        )

    @property
    def sample_count(self) -> int:
        return self.family_count * self.per_family


def load_split_items(split: str, *, data_dir: Path | str | None = None) -> list[BenchmarkItem]:
    """Load every JSONL dataset file in a split directory."""
    root = Path(data_dir) if data_dir is not None else PROJECT_ROOT / "data"
    split_dir = root / split
    if not split_dir.exists():
        raise FileNotFoundError(f"Split directory does not exist: {split_dir}")

    items: list[BenchmarkItem] = []
    for path in sorted(split_dir.glob("*.jsonl")):
        items.extend(load_benchmark_jsonl(path))
    if not items:
        raise ValueError(f"No benchmark items found in split directory: {split_dir}")
    return items


def build_barrage(
    items: list[BenchmarkItem],
    profile: BarrageProfile,
    *,
    seed: int,
) -> list[BenchmarkItem]:
    """Select a deterministic family-balanced, subfamily-diverse barrage."""
    by_family: dict[str, list[BenchmarkItem]] = defaultdict(list)
    for item in items:
        by_family[item.family].append(item)

    selected_families = _select_families(by_family, profile)
    family_picks = {}
    for family in selected_families:
        if profile.strategy == "hard_obvious":
            family_picks[family] = _select_hard_family_items(
                by_family[family],
                profile.per_family,
                seed=seed,
            )
        else:
            family_picks[family] = _select_family_items(
                by_family[family],
                profile.per_family,
                seed=seed,
            )
    return _interleave_family_picks(family_picks, selected_families, profile.per_family)


def write_barrage_jsonl(items: list[BenchmarkItem], path: Path | str) -> Path:
    """Write selected barrage rows as canonical JSONL."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        json.dumps(item.model_dump(mode="json"), sort_keys=True)
        for item in items
    ]
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return output


def _select_families(
    by_family: dict[str, list[BenchmarkItem]],
    profile: BarrageProfile,
) -> list[str]:
    eligible = [
        family
        for family in FAMILY_ORDER
        if family in by_family and len(by_family[family]) >= profile.per_family
    ]
    if len(eligible) < profile.family_count:
        raise ValueError(
            f"Profile {profile.name} requires {profile.family_count} families with "
            f"at least {profile.per_family} items each; found {len(eligible)}."
        )
    return eligible[: profile.family_count]


def _select_family_items(
    items: list[BenchmarkItem],
    quota: int,
    *,
    seed: int,
) -> list[BenchmarkItem]:
    by_subfamily: dict[str, list[BenchmarkItem]] = defaultdict(list)
    for item in items:
        by_subfamily[item.subfamily].append(item)

    subfamilies = sorted(by_subfamily)
    queues = {
        subfamily: sorted(
            subfamily_items,
            key=lambda item: _stable_sort_key(seed, item.family, subfamily, item.id),
        )
        for subfamily, subfamily_items in by_subfamily.items()
    }

    selected: list[BenchmarkItem] = []
    while len(selected) < quota:
        made_progress = False
        for subfamily in subfamilies:
            queue = queues[subfamily]
            if not queue:
                continue
            selected.append(queue.pop(0))
            made_progress = True
            if len(selected) == quota:
                break
        if not made_progress:
            raise ValueError(
                f"Family {items[0].family} has fewer than {quota} selectable items."
            )
    return selected


def _select_hard_family_items(
    items: list[BenchmarkItem],
    quota: int,
    *,
    seed: int,
) -> list[BenchmarkItem]:
    priority = {
        subfamily: index
        for index, subfamily in enumerate(HARD_SUBFAMILY_ORDER.get(items[0].family, ()))
    }
    ranked = sorted(
        items,
        key=lambda item: (
            priority.get(item.subfamily, len(priority)),
            _stable_sort_key(seed, item.family, item.subfamily, item.id),
        ),
    )
    if len(ranked) < quota:
        raise ValueError(
            f"Family {items[0].family} has fewer than {quota} selectable items."
        )
    return ranked[:quota]


def _interleave_family_picks(
    family_picks: dict[str, list[BenchmarkItem]],
    family_order: list[str],
    per_family: int,
) -> list[BenchmarkItem]:
    selected: list[BenchmarkItem] = []
    for index in range(per_family):
        for family in family_order:
            selected.append(family_picks[family][index])
    return selected


def _stable_sort_key(seed: int, *parts: str) -> str:
    payload = "\0".join([str(seed), *parts])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
