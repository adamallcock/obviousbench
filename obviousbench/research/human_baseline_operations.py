"""Build an operations packet for collecting the ObviousBench human baseline."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

OperationStatus = Literal["pass", "blocked"]


@dataclass(frozen=True)
class HumanBaselineOperationsInputs:
    output_path: Path
    collection_packet_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md"
    )
    collection_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md"
    )
    scoring_report_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md"
    )
    threshold_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md"
    )
    promotion_report_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-promotion-report.md"
    )
    readiness_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-readiness-audit.md"
    )
    response_template_path: Path = Path(
        "data/human_baseline/paper_v1_response_template.csv"
    )
    promoted_baseline_path: Path = Path("data/human_baseline/paper_v1.csv")
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class HumanBaselineOperationCheck:
    name: str
    status: OperationStatus
    evidence: str
    next_action: str


@dataclass(frozen=True)
class HumanBaselineOperationsResult:
    output_path: Path
    checks: tuple[HumanBaselineOperationCheck, ...]

    @property
    def ok(self) -> bool:
        return all(check.status == "pass" for check in self.checks)

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    @property
    def blocked_count(self) -> int:
        return sum(check.status == "blocked" for check in self.checks)

    def check_by_name(self, name: str) -> HumanBaselineOperationCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


def build_human_baseline_operations_packet(
    inputs: HumanBaselineOperationsInputs,
) -> HumanBaselineOperationsResult:
    """Write the human-baseline operations handoff without collecting data."""
    checks = (
        _collection_packet_check(inputs),
        _response_collection_check(inputs),
        _scoring_check(inputs),
        _threshold_check(inputs),
        _promotion_report_check(inputs),
        _promotion_target_check(inputs),
        _readiness_check(inputs),
    )
    result = HumanBaselineOperationsResult(
        output_path=inputs.output_path,
        checks=checks,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _collection_packet_check(
    inputs: HumanBaselineOperationsInputs,
) -> HumanBaselineOperationCheck:
    text = _read(inputs.collection_packet_path)
    status = _line_value(text, "Overall status:")
    participants = _bullet_value(text, "Participants")
    rows = _bullet_value(text, "Preallocated response rows")
    if status == "PASS" and inputs.response_template_path.exists():
        return HumanBaselineOperationCheck(
            name="collection packet",
            status="pass",
            evidence=(
                f"{participants or 'unknown'} participant(s); "
                f"{rows or 'unknown'} response row(s)."
            ),
            next_action="None.",
        )
    return HumanBaselineOperationCheck(
        name="collection packet",
        status="blocked",
        evidence="Collection packet or response template is missing or not passing.",
        next_action="Run `make -C paper human-baseline-packet`.",
    )


def _response_collection_check(
    inputs: HumanBaselineOperationsInputs,
) -> HumanBaselineOperationCheck:
    text = _read(inputs.collection_audit_path)
    status = _line_value(text, "Overall status:")
    expected = _bullet_value(text, "Expected response rows")
    complete = _bullet_value(text, "Completed answer+timing rows")
    missing_answers = _bullet_value(text, "Missing answers")
    invalid_timings = _bullet_value(text, "Invalid timings")
    if status == "PASS":
        return HumanBaselineOperationCheck(
            name="response collection",
            status="pass",
            evidence=f"{complete}/{expected} answer+timing rows complete.",
            next_action="None.",
        )
    return HumanBaselineOperationCheck(
        name="response collection",
        status="blocked",
        evidence=(
            f"{complete or '0'}/{expected or '0'} answer+timing rows complete; "
            f"{missing_answers or 'unknown'} missing answer(s); "
            f"{invalid_timings or 'unknown'} invalid timing(s)."
        ),
        next_action=(
            "Collect real answers and non-negative elapsed seconds in "
            "`data/human_baseline/paper_v1_response_template.csv`, then rerun "
            "`make -C paper human-baseline-audit`."
        ),
    )


def _scoring_check(inputs: HumanBaselineOperationsInputs) -> HumanBaselineOperationCheck:
    text = _read(inputs.scoring_report_path)
    status = _line_value(text, "Overall status:")
    rows = _bullet_value(text, "Response rows")
    scored = _bullet_value(text, "Scored rows")
    issues = _bullet_value(text, "Issues")
    if status == "PASS":
        return HumanBaselineOperationCheck(
            name="scoring",
            status="pass",
            evidence=f"{scored}/{rows} rows scored; {issues or '0'} issue(s).",
            next_action="None.",
        )
    return HumanBaselineOperationCheck(
        name="scoring",
        status="blocked",
        evidence=f"{scored or '0'}/{rows or '0'} rows scored; {issues or 'unknown'} issue(s).",
        next_action=(
            "Run `make -C paper human-baseline-score` only after collection "
            "audit passes."
        ),
    )


def _threshold_check(inputs: HumanBaselineOperationsInputs) -> HumanBaselineOperationCheck:
    text = _read(inputs.threshold_audit_path)
    status = _line_value(text, "Overall status:")
    core = _bullet_value(text, "Core H0 items")
    no_data = _bullet_value(text, "Items with no scored data")
    ignored = _bullet_value(text, "Ignored scored rows")
    if status == "PASS":
        return HumanBaselineOperationCheck(
            name="threshold classification",
            status="pass",
            evidence=f"{core or '0'} core H0 item(s); {no_data or '0'} no-data item(s).",
            next_action="None.",
        )
    return HumanBaselineOperationCheck(
        name="threshold classification",
        status="blocked",
        evidence=(
            f"{core or '0'} core H0 item(s); {no_data or 'unknown'} no-data item(s); "
            f"{ignored or 'unknown'} ignored scored row(s)."
        ),
        next_action=(
            "Run `make -C paper human-baseline-thresholds` after scoring passes "
            "and use only `core_h0` items for headline claims."
        ),
    )


def _readiness_check(inputs: HumanBaselineOperationsInputs) -> HumanBaselineOperationCheck:
    text = _read(inputs.readiness_audit_path)
    status = _extract_readiness_status(text)
    if status == "PASS":
        return HumanBaselineOperationCheck(
            name="paper readiness",
            status="pass",
            evidence="Readiness audit reports PASS.",
            next_action="None.",
        )
    return HumanBaselineOperationCheck(
        name="paper readiness",
        status="blocked",
        evidence="Readiness audit is not passing; current blocker is human-baseline evidence.",
        next_action=(
            "Promote only audited scored rows to `data/human_baseline/paper_v1.csv`, "
            "then rerun `make -C paper readiness`."
        ),
    )


def _promotion_report_check(
    inputs: HumanBaselineOperationsInputs,
) -> HumanBaselineOperationCheck:
    text = _read(inputs.promotion_report_path)
    status = _line_value(text, "Overall status:")
    source_rows = _bullet_value(text, "Source scored rows")
    target_rows = _bullet_value(text, "Target rows after run")
    if status == "PASS":
        return HumanBaselineOperationCheck(
            name="promotion preflight",
            status="pass",
            evidence=(
                f"{source_rows or 'unknown'} source row(s); "
                f"{target_rows or 'unknown'} current target row(s)."
            ),
            next_action="Apply promotion only after reviewing the report.",
        )
    return HumanBaselineOperationCheck(
        name="promotion preflight",
        status="blocked",
        evidence=f"Promotion report status is {status or 'missing'}.",
        next_action="Run `make -C paper human-baseline-promotion`.",
    )


def _promotion_target_check(
    inputs: HumanBaselineOperationsInputs,
) -> HumanBaselineOperationCheck:
    if inputs.promoted_baseline_path.exists() and inputs.promoted_baseline_path.stat().st_size > 0:
        rows = max(inputs.promoted_baseline_path.read_text(encoding="utf-8").count("\n") - 1, 0)
    else:
        rows = 0
    status: OperationStatus = "pass" if rows > 0 else "blocked"
    return HumanBaselineOperationCheck(
        name="promotion target",
        status=status,
        evidence=f"{inputs.promoted_baseline_path} has {rows} response row(s).",
        next_action=(
            "Copy checked scored baseline rows into `data/human_baseline/paper_v1.csv` "
            "only after collection, scoring, and threshold audits pass."
            if status != "pass"
            else "None."
        ),
    )


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _line_value(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip().rstrip(".")
    return ""


def _bullet_value(text: str, label: str) -> str:
    pattern = re.compile(rf"^-\s+{re.escape(label)}:\s+(.+?)\.?\s*$")
    for line in text.splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return ""


def _extract_readiness_status(text: str) -> str:
    if "Overall status: PASS" in text or "## Overall Status\n\nPASS" in text:
        return "PASS"
    return "FAIL"


def _render_markdown(
    result: HumanBaselineOperationsResult,
    inputs: HumanBaselineOperationsInputs,
) -> str:
    lines = [
        "---",
        "title: Paper V1 Human Baseline Operations Packet",
        f"date: {inputs.generated_on}",
        "type: runbook",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# Paper V1 Human Baseline Operations Packet",
        "",
        "This packet coordinates the collection, audit, scoring, thresholding,",
        "promotion, and readiness gates for the paper human baseline. It does",
        "not create participant data, score blank rows, run providers, or",
        "authorize final model arrays.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        (
            "Summary: "
            f"{result.passed_count} passed, {result.blocked_count} blocked."
        ),
        "",
        "## Operation Matrix",
        "",
        "| Step | Status | Evidence | Next action |",
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
            "make -C paper human-baseline-packet",
            "make -C paper human-baseline-audit",
            "# Fill every answer and seconds field in the response template.",
            "make -C paper human-baseline-audit",
        "make -C paper human-baseline-score",
        "make -C paper human-baseline-thresholds",
        "make -C paper human-baseline-promotion",
        "# After the promotion report says PASS and rows are reviewed:",
        ".venv/bin/python scripts/promote_human_baseline.py --apply",
        "make -C paper assets",
            "make -C paper readiness",
            "make -C paper sweep-plan",
            "```",
            "",
            "## Stop Rules",
            "",
            "- Do not show `data/human_baseline/paper_v1_answer_key.csv` to participants.",
            "- Do not store participant names, emails, demographics, payment details, or notes "
            "outside pseudonymous IDs.",
            "- Do not run final model arrays until `make -C paper readiness` passes and "
            "the sweep handoff says `Run allowed: YES`.",
            "",
        ]
    )
    return "\n".join(lines)


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
