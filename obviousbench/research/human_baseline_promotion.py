"""Guard promotion of scored human-baseline rows into the paper baseline CSV."""

from __future__ import annotations

import csv
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from obviousbench.research.human_baseline_scoring import (
    RESPONSE_COLUMNS,
    SCORED_COLUMNS,
)
from obviousbench.research.human_baseline_thresholds import ITEM_THRESHOLD_COLUMNS

PromotionStatus = Literal["pass", "blocked"]


@dataclass(frozen=True)
class HumanBaselinePromotionInputs:
    output_path: Path
    scored_path: Path = Path("data/human_baseline/paper_v1_scored_draft.csv")
    promoted_path: Path = Path("data/human_baseline/paper_v1.csv")
    collection_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md"
    )
    scoring_report_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md"
    )
    threshold_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md"
    )
    threshold_items_path: Path = Path(
        "data/human_baseline/paper_v1_threshold_items.csv"
    )
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class HumanBaselinePromotionCheck:
    name: str
    status: PromotionStatus
    evidence: str
    next_action: str


@dataclass(frozen=True)
class HumanBaselinePromotionResult:
    output_path: Path
    promoted_path: Path
    checks: tuple[HumanBaselinePromotionCheck, ...]
    source_rows: int
    promoted_rows: int
    target_rows_before: int
    threshold_status_counts: Counter[str]
    apply_requested: bool
    applied: bool

    @property
    def ok(self) -> bool:
        return all(check.status == "pass" for check in self.checks)

    @property
    def status(self) -> PromotionStatus:
        return "pass" if self.ok else "blocked"

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    @property
    def blocked_count(self) -> int:
        return sum(check.status == "blocked" for check in self.checks)

    def check_by_name(self, name: str) -> HumanBaselinePromotionCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


def build_human_baseline_promotion_report(
    inputs: HumanBaselinePromotionInputs,
    *,
    apply: bool = False,
) -> HumanBaselinePromotionResult:
    """Write a promotion report and optionally copy scored rows into paper_v1.csv."""
    scored_rows, scored_issues = _load_scored_rows(inputs.scored_path)
    threshold_counts, threshold_issues = _load_threshold_status_counts(
        inputs.threshold_items_path
    )
    checks = (
        _report_status_check("collection audit", inputs.collection_audit_path),
        _report_status_check("scoring report", inputs.scoring_report_path),
        _report_status_check("threshold audit", inputs.threshold_audit_path),
        _threshold_items_check(threshold_counts, threshold_issues),
        _scored_rows_check(scored_rows, scored_issues),
    )
    ready = all(check.status == "pass" for check in checks)
    target_rows_before = _count_csv_rows(inputs.promoted_path)
    applied = False
    promoted_rows = target_rows_before
    if ready and apply:
        _write_promoted_rows(inputs.promoted_path, scored_rows)
        applied = True
        promoted_rows = len(scored_rows)

    result = HumanBaselinePromotionResult(
        output_path=inputs.output_path,
        promoted_path=inputs.promoted_path,
        checks=checks,
        source_rows=len(scored_rows),
        promoted_rows=promoted_rows,
        target_rows_before=target_rows_before,
        threshold_status_counts=threshold_counts,
        apply_requested=apply,
        applied=applied,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _report_status_check(
    name: str,
    path: Path,
) -> HumanBaselinePromotionCheck:
    status = _overall_status(path)
    if status == "PASS":
        return HumanBaselinePromotionCheck(
            name=name,
            status="pass",
            evidence=f"{path} reports PASS.",
            next_action="None.",
        )
    return HumanBaselinePromotionCheck(
        name=name,
        status="blocked",
        evidence=f"{path} reports {status}.",
        next_action=f"Regenerate and review `{path}` until it reports PASS.",
    )


def _threshold_items_check(
    counts: Counter[str],
    issues: Sequence[str],
) -> HumanBaselinePromotionCheck:
    if issues:
        return HumanBaselinePromotionCheck(
            name="threshold item states",
            status="blocked",
            evidence="; ".join(issues[:5]),
            next_action="Rerun `make -C paper human-baseline-thresholds`.",
        )
    if not counts:
        return HumanBaselinePromotionCheck(
            name="threshold item states",
            status="blocked",
            evidence="No item threshold rows are available.",
            next_action="Rerun `make -C paper human-baseline-thresholds`.",
        )
    if counts["no_data"]:
        return HumanBaselinePromotionCheck(
            name="threshold item states",
            status="blocked",
            evidence=f"{counts['no_data']} item(s) still have no scored human data.",
            next_action="Collect, score, and threshold all paper item rows first.",
        )
    return HumanBaselinePromotionCheck(
        name="threshold item states",
        status="pass",
        evidence=_threshold_counts_evidence(counts),
        next_action="None.",
    )


def _scored_rows_check(
    rows: Sequence[dict[str, str]],
    issues: Sequence[str],
) -> HumanBaselinePromotionCheck:
    if issues:
        return HumanBaselinePromotionCheck(
            name="scored rows",
            status="blocked",
            evidence="; ".join(issues[:5]),
            next_action="Rerun `make -C paper human-baseline-score` after fixing rows.",
        )
    if not rows:
        return HumanBaselinePromotionCheck(
            name="scored rows",
            status="blocked",
            evidence="No scored rows are available.",
            next_action="Collect real responses, then rerun scoring.",
        )
    return HumanBaselinePromotionCheck(
        name="scored rows",
        status="pass",
        evidence=f"{len(rows)} scored row(s) are promotion-ready.",
        next_action="None.",
    )


def _overall_status(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Overall status:"):
            return line.split(":", 1)[1].strip()
    return "MISSING"


def _load_scored_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        return [], [f"scored CSV missing: {path}"]
    issues: list[str] = []
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(SCORED_COLUMNS) - set(reader.fieldnames or ()))
        if missing:
            return [], [f"{path} missing columns: {', '.join(missing)}"]
        for row_number, row in enumerate(reader, start=2):
            normalized = {column: (row.get(column) or "").strip() for column in SCORED_COLUMNS}
            rows.append(normalized)
            _validate_scored_row(path, row_number, normalized, issues)
    return rows, issues


def _validate_scored_row(
    path: Path,
    row_number: int,
    row: dict[str, str],
    issues: list[str],
) -> None:
    for column in ("item_id", "participant_id", "answer", "seconds", "correct"):
        if not row[column]:
            issues.append(f"{path}:{row_number} missing {column}")
    if row["correct"].lower() not in {"true", "false"}:
        issues.append(f"{path}:{row_number} correct must be true/false")
    try:
        if float(row["seconds"]) < 0:
            issues.append(f"{path}:{row_number} seconds must be non-negative")
    except ValueError:
        issues.append(f"{path}:{row_number} invalid seconds: {row['seconds']!r}")


def _load_threshold_status_counts(path: Path) -> tuple[Counter[str], list[str]]:
    if not path.exists():
        return Counter(), [f"threshold item CSV missing: {path}"]
    issues: list[str] = []
    counts: Counter[str] = Counter()
    allowed = {"core_h0", "borderline", "exclude", "no_data"}
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(ITEM_THRESHOLD_COLUMNS) - set(reader.fieldnames or ()))
        if missing:
            return counts, [f"{path} missing columns: {', '.join(missing)}"]
        for row_number, row in enumerate(reader, start=2):
            status = (row.get("status") or "").strip()
            if status not in allowed:
                issues.append(f"{path}:{row_number} invalid status {status!r}")
                continue
            counts[status] += 1
    return counts, issues


def _write_promoted_rows(path: Path, scored_rows: Sequence[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESPONSE_COLUMNS)
        writer.writeheader()
        for row in scored_rows:
            writer.writerow({column: row.get(column, "") for column in RESPONSE_COLUMNS})


def _count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return sum(1 for _ in reader)


def _threshold_counts_evidence(counts: Counter[str]) -> str:
    parts = [
        f"{counts['core_h0']} core_h0",
        f"{counts['borderline']} borderline",
        f"{counts['exclude']} exclude",
        f"{counts['no_data']} no_data",
    ]
    return "; ".join(parts) + " item state(s)."


def _render_markdown(
    result: HumanBaselinePromotionResult,
    inputs: HumanBaselinePromotionInputs,
) -> str:
    lines = [
        "---",
        "title: Paper V1 Human Baseline Promotion Report",
        f"date: {inputs.generated_on}",
        "type: runbook",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# Paper V1 Human Baseline Promotion Report",
        "",
        "This generated report validates whether scored human-baseline rows can",
        "be promoted into the paper baseline CSV used by the arXiv readiness",
        "gate. It is dry-run by default and does not run model providers.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"- Apply requested: {'yes' if result.apply_requested else 'no'}",
        f"- Promotion applied: {'yes' if result.applied else 'no'}",
        f"- Source scored rows: {result.source_rows}",
        f"- Target rows before run: {result.target_rows_before}",
        f"- Target rows after run: {result.promoted_rows}",
        f"- Target CSV: `{result.promoted_path}`",
        f"- Threshold states: {_threshold_counts_evidence(result.threshold_status_counts)}",
        "",
        "## Promotion Checks",
        "",
        "| Check | Status | Evidence | Next action |",
        "| --- | --- | --- | --- |",
    ]
    for check in result.checks:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(check.name),
                    check.status.upper(),
                    _cell(check.evidence),
                    _cell(check.next_action),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Command Ladder",
            "",
            "```bash",
            "make -C paper human-baseline-audit",
            "make -C paper human-baseline-score",
            "make -C paper human-baseline-thresholds",
            "make -C paper human-baseline-promotion",
            "# After this report says PASS and the rows have been reviewed:",
            ".venv/bin/python scripts/promote_human_baseline.py --apply",
            "make -C paper assets",
            "make -C paper readiness",
            "make -C paper sweep-plan",
            "```",
            "",
            "## Stop Rules",
            "",
            "- Do not use `--apply` while this report is blocked.",
            "- Do not edit `correct` values by hand to force readiness.",
            "- Do not promote rows before the collection, scoring, and threshold",
            "  audits all report PASS.",
            "- Do not run final model arrays until `make -C paper readiness` passes",
            "  and the final-sweep handoff says `Run allowed: YES`.",
            "",
        ]
    )
    return "\n".join(lines)


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
