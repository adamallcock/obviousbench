"""Audit human-baseline items against predeclared paper thresholds."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from statistics import median

ANSWER_KEY_COLUMNS = (
    "item_id",
    "family",
    "subfamily",
    "target",
    "answer_type",
    "scorer",
)
SCORED_COLUMNS = (
    "item_id",
    "participant_id",
    "answer",
    "seconds",
    "correct",
    "notes",
    "scorer",
    "target",
    "extracted",
    "failure_type",
    "format_correct",
    "strict_correct",
)
ITEM_THRESHOLD_COLUMNS = (
    "item_id",
    "family",
    "subfamily",
    "scorer",
    "response_count",
    "correct_count",
    "accuracy",
    "median_seconds",
    "confusion_note_count",
    "status",
    "reason",
)
FAMILY_THRESHOLD_COLUMNS = (
    "family",
    "item_count",
    "core_h0_count",
    "borderline_count",
    "exclude_count",
    "no_data_count",
    "response_count",
    "median_accuracy",
    "median_seconds",
)
CONFUSION_TERMS = ("ambiguous", "confusing", "confusion", "unclear")
ThresholdStatus = str


@dataclass(frozen=True)
class AnswerKeyEntry:
    item_id: str
    family: str
    subfamily: str
    target: str
    answer_type: str
    scorer: str


@dataclass(frozen=True)
class ScoredHumanResponse:
    item_id: str
    correct: bool
    seconds: float
    notes: str


@dataclass(frozen=True)
class HumanBaselineThresholdInputs:
    scored_path: Path
    answer_key_path: Path
    item_output_path: Path
    family_output_path: Path
    report_path: Path
    generated_on: str = "2026-06-01"
    core_accuracy_threshold: float = 0.95
    core_seconds_threshold: float = 10.0
    exclude_accuracy_threshold: float = 0.80
    exclude_seconds_threshold: float = 30.0
    confusion_note_threshold: int = 2


@dataclass(frozen=True)
class ItemThresholdSummary:
    item_id: str
    family: str
    subfamily: str
    scorer: str
    response_count: int
    correct_count: int
    accuracy: float | None
    median_seconds: float | None
    confusion_note_count: int
    status: ThresholdStatus
    reason: str


@dataclass(frozen=True)
class FamilyThresholdSummary:
    family: str
    item_count: int
    core_h0_count: int
    borderline_count: int
    exclude_count: int
    no_data_count: int
    response_count: int
    median_accuracy: float | None
    median_seconds: float | None


@dataclass(frozen=True)
class HumanBaselineThresholdResult:
    item_output_path: Path
    family_output_path: Path
    report_path: Path
    items: tuple[ItemThresholdSummary, ...]
    families: tuple[FamilyThresholdSummary, ...]
    ignored_row_count: int
    unknown_item_count: int
    issue_count: int

    @property
    def ok(self) -> bool:
        return (
            self.item_count > 0
            and self.no_data_count == 0
            and self.ignored_row_count == 0
            and self.issue_count == 0
        )

    @property
    def item_count(self) -> int:
        return len(self.items)

    @property
    def core_h0_count(self) -> int:
        return sum(item.status == "core_h0" for item in self.items)

    @property
    def borderline_count(self) -> int:
        return sum(item.status == "borderline" for item in self.items)

    @property
    def exclude_count(self) -> int:
        return sum(item.status == "exclude" for item in self.items)

    @property
    def no_data_count(self) -> int:
        return sum(item.status == "no_data" for item in self.items)

    @property
    def response_count(self) -> int:
        return sum(item.response_count for item in self.items)


def audit_human_baseline_thresholds(
    inputs: HumanBaselineThresholdInputs,
) -> HumanBaselineThresholdResult:
    """Classify scored human-baseline rows by the paper's threshold policy."""
    issues: list[str] = []
    answer_key = _load_answer_key(inputs.answer_key_path, issues)
    responses, ignored_row_count, unknown_item_count = _load_scored_responses(
        inputs.scored_path,
        answer_key,
        issues,
    )

    item_summaries = tuple(
        _summarize_item(entry, responses[entry.item_id], inputs)
        for entry in answer_key
    )
    family_summaries = tuple(_summarize_families(item_summaries))
    result = HumanBaselineThresholdResult(
        item_output_path=inputs.item_output_path,
        family_output_path=inputs.family_output_path,
        report_path=inputs.report_path,
        items=item_summaries,
        families=family_summaries,
        ignored_row_count=ignored_row_count,
        unknown_item_count=unknown_item_count,
        issue_count=len(issues),
    )
    inputs.item_output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.family_output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.report_path.parent.mkdir(parents=True, exist_ok=True)
    _write_item_csv(inputs.item_output_path, item_summaries)
    _write_family_csv(inputs.family_output_path, family_summaries)
    inputs.report_path.write_text(
        _render_report(result, inputs, issues),
        encoding="utf-8",
    )
    return result


def _load_answer_key(path: Path, issues: list[str]) -> tuple[AnswerKeyEntry, ...]:
    if not path.exists():
        issues.append(f"answer key missing: {path}")
        return ()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(ANSWER_KEY_COLUMNS) - set(reader.fieldnames or ()))
        if missing:
            issues.append(f"{path} missing columns: {', '.join(missing)}")
            return ()
        return tuple(
            AnswerKeyEntry(
                item_id=(row.get("item_id") or "").strip(),
                family=(row.get("family") or "").strip(),
                subfamily=(row.get("subfamily") or "").strip(),
                target=(row.get("target") or "").strip(),
                answer_type=(row.get("answer_type") or "").strip(),
                scorer=(row.get("scorer") or "").strip(),
            )
            for row in reader
            if (row.get("item_id") or "").strip()
        )


def _load_scored_responses(
    path: Path,
    answer_key: Sequence[AnswerKeyEntry],
    issues: list[str],
) -> tuple[dict[str, list[ScoredHumanResponse]], int, int]:
    responses: dict[str, list[ScoredHumanResponse]] = defaultdict(list)
    if not path.exists():
        issues.append(f"scored response file missing: {path}")
        return responses, 0, 0
    known_item_ids = {entry.item_id for entry in answer_key}
    ignored_row_count = 0
    unknown_item_count = 0
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(SCORED_COLUMNS) - set(reader.fieldnames or ()))
        if missing:
            issues.append(f"{path} missing columns: {', '.join(missing)}")
            return responses, 0, 0
        for row in reader:
            item_id = (row.get("item_id") or "").strip()
            if item_id not in known_item_ids:
                unknown_item_count += 1
                ignored_row_count += 1
                continue
            correct = _parse_bool(row.get("correct") or "")
            seconds = _parse_seconds(row.get("seconds") or "")
            if correct is None or seconds is None:
                ignored_row_count += 1
                continue
            responses[item_id].append(
                ScoredHumanResponse(
                    item_id=item_id,
                    correct=correct,
                    seconds=seconds,
                    notes=row.get("notes") or "",
                )
            )
    if unknown_item_count:
        issues.append(f"{unknown_item_count} scored row(s) use unknown item_id values")
    return responses, ignored_row_count, unknown_item_count


def _summarize_item(
    entry: AnswerKeyEntry,
    responses: Sequence[ScoredHumanResponse],
    inputs: HumanBaselineThresholdInputs,
) -> ItemThresholdSummary:
    response_count = len(responses)
    if response_count == 0:
        return ItemThresholdSummary(
            item_id=entry.item_id,
            family=entry.family,
            subfamily=entry.subfamily,
            scorer=entry.scorer,
            response_count=0,
            correct_count=0,
            accuracy=None,
            median_seconds=None,
            confusion_note_count=0,
            status="no_data",
            reason="No scored human response rows are available.",
        )

    correct_count = sum(response.correct for response in responses)
    accuracy = correct_count / response_count
    median_seconds = median(response.seconds for response in responses)
    confusion_note_count = sum(
        _has_confusion_note(response.notes) for response in responses
    )
    status, reason = _classify_item(
        accuracy,
        median_seconds,
        confusion_note_count,
        inputs,
    )
    return ItemThresholdSummary(
        item_id=entry.item_id,
        family=entry.family,
        subfamily=entry.subfamily,
        scorer=entry.scorer,
        response_count=response_count,
        correct_count=correct_count,
        accuracy=accuracy,
        median_seconds=median_seconds,
        confusion_note_count=confusion_note_count,
        status=status,
        reason=reason,
    )


def _classify_item(
    accuracy: float,
    median_seconds: float,
    confusion_note_count: int,
    inputs: HumanBaselineThresholdInputs,
) -> tuple[ThresholdStatus, str]:
    if accuracy < inputs.exclude_accuracy_threshold:
        return (
            "exclude",
            (
                "Human accuracy is below "
                f"{_format_percent(inputs.exclude_accuracy_threshold)}."
            ),
        )
    if median_seconds > inputs.exclude_seconds_threshold:
        return (
            "exclude",
            (
                "Median response time is above "
                f"{_format_number(inputs.exclude_seconds_threshold)} seconds."
            ),
        )
    if confusion_note_count >= inputs.confusion_note_threshold:
        return (
            "exclude",
            (
                "Repeated participant notes indicate confusion or ambiguity "
                f"({confusion_note_count} note(s))."
            ),
        )
    if (
        accuracy >= inputs.core_accuracy_threshold
        and median_seconds < inputs.core_seconds_threshold
    ):
        return (
            "core_h0",
            (
                "Meets core H0 threshold: accuracy at or above "
                f"{_format_percent(inputs.core_accuracy_threshold)} and median "
                f"time below {_format_number(inputs.core_seconds_threshold)} seconds."
            ),
        )
    return (
        "borderline",
        "Meets minimum human-baseline floor but not the core H0 threshold.",
    )


def _summarize_families(
    items: Sequence[ItemThresholdSummary],
) -> list[FamilyThresholdSummary]:
    by_family: dict[str, list[ItemThresholdSummary]] = defaultdict(list)
    for item in items:
        by_family[item.family].append(item)

    summaries: list[FamilyThresholdSummary] = []
    for family, family_items in sorted(by_family.items()):
        status_counts = Counter(item.status for item in family_items)
        accuracies = [
            item.accuracy for item in family_items if item.accuracy is not None
        ]
        medians = [
            item.median_seconds
            for item in family_items
            if item.median_seconds is not None
        ]
        summaries.append(
            FamilyThresholdSummary(
                family=family,
                item_count=len(family_items),
                core_h0_count=status_counts["core_h0"],
                borderline_count=status_counts["borderline"],
                exclude_count=status_counts["exclude"],
                no_data_count=status_counts["no_data"],
                response_count=sum(item.response_count for item in family_items),
                median_accuracy=median(accuracies) if accuracies else None,
                median_seconds=median(medians) if medians else None,
            )
        )
    return summaries


def _parse_bool(value: str) -> bool | None:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    return None


def _parse_seconds(value: str) -> float | None:
    try:
        seconds = float(value)
    except ValueError:
        return None
    return seconds if seconds >= 0 else None


def _has_confusion_note(notes: str) -> bool:
    lowered = notes.lower()
    return any(term in lowered for term in CONFUSION_TERMS)


def _write_item_csv(path: Path, items: Sequence[ItemThresholdSummary]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ITEM_THRESHOLD_COLUMNS)
        writer.writeheader()
        for item in items:
            writer.writerow(
                {
                    "item_id": item.item_id,
                    "family": item.family,
                    "subfamily": item.subfamily,
                    "scorer": item.scorer,
                    "response_count": item.response_count,
                    "correct_count": item.correct_count,
                    "accuracy": _format_optional(item.accuracy),
                    "median_seconds": _format_optional(item.median_seconds),
                    "confusion_note_count": item.confusion_note_count,
                    "status": item.status,
                    "reason": item.reason,
                }
            )


def _write_family_csv(
    path: Path,
    families: Sequence[FamilyThresholdSummary],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FAMILY_THRESHOLD_COLUMNS)
        writer.writeheader()
        for family in families:
            writer.writerow(
                {
                    "family": family.family,
                    "item_count": family.item_count,
                    "core_h0_count": family.core_h0_count,
                    "borderline_count": family.borderline_count,
                    "exclude_count": family.exclude_count,
                    "no_data_count": family.no_data_count,
                    "response_count": family.response_count,
                    "median_accuracy": _format_optional(family.median_accuracy),
                    "median_seconds": _format_optional(family.median_seconds),
                }
            )


def _render_report(
    result: HumanBaselineThresholdResult,
    inputs: HumanBaselineThresholdInputs,
    issues: Sequence[str],
) -> str:
    lines = [
        "---",
        "title: Paper V1 Human Baseline Threshold Audit",
        f"date: {inputs.generated_on}",
        "type: research",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# Paper V1 Human Baseline Threshold Audit",
        "",
        "This report classifies scored human-baseline rows against the",
        "predeclared ObviousBench paper thresholds. It does not collect",
        "participant data, adjudicate ambiguous answers, or run model providers.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"- Scored responses: `{inputs.scored_path}`",
        f"- Answer key: `{inputs.answer_key_path}`",
        f"- Item output: `{inputs.item_output_path}`",
        f"- Family output: `{inputs.family_output_path}`",
        f"- Items: {result.item_count}",
        f"- Scored response rows used: {result.response_count}",
        f"- Ignored scored rows: {result.ignored_row_count}",
        f"- Unknown-item rows: {result.unknown_item_count}",
        f"- Core H0 items: {result.core_h0_count}",
        f"- Borderline items: {result.borderline_count}",
        f"- Excluded items: {result.exclude_count}",
        f"- Items with no scored data: {result.no_data_count}",
        f"- Structural issues: {result.issue_count}",
        "",
        "## Threshold Rules",
        "",
        (
            "- `core_h0`: accuracy at or above "
            f"{_format_percent(inputs.core_accuracy_threshold)} and median "
            f"time below {_format_number(inputs.core_seconds_threshold)} seconds."
        ),
        (
            "- `borderline`: at least "
            f"{_format_percent(inputs.exclude_accuracy_threshold)} accuracy and "
            "no exclusion trigger, but not core H0."
        ),
        (
            "- `exclude`: accuracy below "
            f"{_format_percent(inputs.exclude_accuracy_threshold)}, median time "
            f"above {_format_number(inputs.exclude_seconds_threshold)} seconds, "
            "or repeated confusion or ambiguity notes."
        ),
        "- `no_data`: no scored human response rows are available for the item.",
        "",
    ]
    lines.extend(_family_markdown(result.families))
    if result.no_data_count:
        lines.extend(_no_data_lines(result.items))
    if issues:
        lines.extend(["## Issues", ""])
        for issue in issues[:40]:
            lines.append(f"- {issue}")
        if len(issues) > 40:
            lines.append(f"- {len(issues) - 40} additional issue(s) omitted.")
        lines.append("")
    lines.extend(
        [
            "## Use In Paper",
            "",
            "Use only `core_h0` rows for headline human-trivial claims. Keep",
            "`borderline` and `exclude` rows out of headline claims unless the",
            "paper explicitly labels them as appendix or diagnostic material.",
            "Do not promote this audit to final evidence while `no_data` rows",
            "remain.",
            "",
        ]
    )
    return "\n".join(lines)


def _family_markdown(families: Sequence[FamilyThresholdSummary]) -> list[str]:
    lines = [
        "## Family Summary",
        "",
        (
            "| Family | Items | Core H0 | Borderline | Exclude | No Data | "
            "Responses | Median Accuracy | Median Seconds |"
        ),
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    if not families:
        lines.append("| n/a | 0 | 0 | 0 | 0 | 0 | 0 |  |  |")
    for family in families:
        lines.append(
            "| "
            + " | ".join(
                [
                    family.family,
                    str(family.item_count),
                    str(family.core_h0_count),
                    str(family.borderline_count),
                    str(family.exclude_count),
                    str(family.no_data_count),
                    str(family.response_count),
                    _format_optional(family.median_accuracy),
                    _format_optional(family.median_seconds),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _no_data_lines(items: Sequence[ItemThresholdSummary]) -> list[str]:
    no_data_items = [item.item_id for item in items if item.status == "no_data"]
    lines = ["## No-Data Items", ""]
    for item_id in no_data_items[:40]:
        lines.append(f"- `{item_id}`")
    if len(no_data_items) > 40:
        lines.append(f"- {len(no_data_items) - 40} additional item(s) omitted.")
    lines.append("")
    return lines


def _format_optional(value: float | None) -> str:
    if value is None:
        return ""
    return _format_number(value)


def _format_number(value: float) -> str:
    formatted = f"{value:.3f}".rstrip("0").rstrip(".")
    return formatted if formatted else "0"


def _format_percent(value: float) -> str:
    return f"{value * 100:.0f}%"
