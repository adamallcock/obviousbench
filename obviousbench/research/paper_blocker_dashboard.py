"""Build a consolidated blocker dashboard for the ObviousBench paper."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

BlockerStatus = Literal["pass", "blocked", "waiting"]
PublicationMode = Literal["strict", "preprint"]


@dataclass(frozen=True)
class PaperBlockerDashboardInputs:
    output_path: Path
    collection_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md"
    )
    threshold_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md"
    )
    final_sweep_plan_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-final-sweep-plan.md"
    )
    result_artifact_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md"
    )
    claim_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-claim-blocker-audit.md"
    )
    section_tracker_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-report-section-tracker.md"
    )
    source_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-paper-source-audit.md"
    )
    pdf_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md"
    )
    preflight_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md"
    )
    internal_review_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-internal-review.md"
    )
    manuscript_completeness_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md"
    )
    release_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md"
    )
    metadata_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md"
    )
    generated_on: str = "2026-06-01"
    publication_mode: PublicationMode = "preprint"


@dataclass(frozen=True)
class PaperBlocker:
    area: str
    status: BlockerStatus
    dependency: str
    evidence: str
    next_action: str
    source: Path


@dataclass(frozen=True)
class PaperBlockerDashboardResult:
    output_path: Path
    blockers: tuple[PaperBlocker, ...]

    @property
    def ok(self) -> bool:
        return self.blocked_count == 0 and self.waiting_count == 0

    @property
    def pass_count(self) -> int:
        return sum(blocker.status == "pass" for blocker in self.blockers)

    @property
    def blocked_count(self) -> int:
        return sum(blocker.status == "blocked" for blocker in self.blockers)

    @property
    def waiting_count(self) -> int:
        return sum(blocker.status == "waiting" for blocker in self.blockers)

    def blocker_by_area(self, area: str) -> PaperBlocker:
        for blocker in self.blockers:
            if blocker.area == area:
                return blocker
        raise KeyError(area)


def build_paper_blocker_dashboard(
    inputs: PaperBlockerDashboardInputs,
) -> PaperBlockerDashboardResult:
    """Aggregate current paper audits into one action dashboard."""
    blockers = (
        _human_collection_blocker(inputs),
        _human_threshold_blocker(inputs),
        _final_sweep_blocker(inputs),
        _result_artifact_blocker(inputs),
        _claim_and_section_blocker(inputs),
        _source_and_pdf_blocker(inputs),
        _submission_preflight_blocker(inputs),
        _internal_review_blocker(inputs),
        _manuscript_completeness_blocker(inputs),
        _release_blocker(inputs),
        _metadata_blocker(inputs),
    )
    result = PaperBlockerDashboardResult(
        output_path=inputs.output_path,
        blockers=blockers,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _human_collection_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    if inputs.publication_mode == "preprint":
        return PaperBlocker(
            area="human-baseline validation",
            status="pass",
            dependency="deferred validation",
            evidence=(
                "Deferred under the fast-preprint path; empirical human-baseline "
                "claims must be omitted or labeled as future validation."
            ),
            next_action="Collect only after `paper_v1` is frozen for a strict benchmark version.",
            source=inputs.collection_audit_path,
        )

    text = _read(inputs.collection_audit_path)
    status = _status_from_overall(text)
    expected = _int(text, r"Expected response rows:\s+(\d+)")
    complete = _int(text, r"Completed answer\+timing rows:\s+(\d+)")
    missing_answers = _int(text, r"Missing answers:\s+(\d+)")
    invalid_timings = _int(text, r"Invalid timings:\s+(\d+)")
    evidence = (
        f"{complete or 0}/{expected or 0} answer+timing rows complete; "
        f"{missing_answers or 0} missing answer(s); "
        f"{invalid_timings or 0} invalid timing(s)."
    )
    return PaperBlocker(
        area="human-baseline collection",
        status=status,
        dependency="human data collection",
        evidence=evidence,
        next_action=(
            "Collect real participant answers/timings and rerun "
            "`make -C paper human-baseline-audit`."
            if status != "pass"
            else "None."
        ),
        source=inputs.collection_audit_path,
    )


def _human_threshold_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    if inputs.publication_mode == "preprint":
        return PaperBlocker(
            area="human-triviality thresholds",
            status="pass",
            dependency="deferred validation",
            evidence=(
                "No core-H0 set is required for the fast-preprint path; "
                "human-trivial wording is a design target, not a measured result."
            ),
            next_action="Run thresholding later only after audited human rows exist.",
            source=inputs.threshold_audit_path,
        )

    text = _read(inputs.threshold_audit_path)
    status = _status_from_overall(text)
    core = _int(text, r"Core H0 items:\s+(\d+)")
    no_data = _int(text, r"Items with no scored data:\s+(\d+)")
    ignored = _int(text, r"Ignored scored rows:\s+(\d+)")
    evidence = (
        f"{core or 0} core H0 item(s); {no_data or 0} no-data item(s); "
        f"{ignored or 0} ignored scored row(s)."
    )
    return PaperBlocker(
        area="human-triviality thresholds",
        status=status,
        dependency="human data collection",
        evidence=evidence,
        next_action=(
            "Score completed responses, rerun thresholds, and use only "
            "`core_h0` items for headline human-trivial claims."
            if status != "pass"
            else "None."
        ),
        source=inputs.threshold_audit_path,
    )


def _final_sweep_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    artifact_text = _read(inputs.result_artifact_audit_path)
    artifact_status = _status_from_overall(artifact_text)
    planned = _int(artifact_text, r"Planned models:\s+(\d+)") or _int(
        artifact_text,
        r"Planned model rows:\s+(\d+)",
    )
    if artifact_status == "pass":
        return PaperBlocker(
            area="final model sweep",
            status="pass",
            dependency="provider run after readiness",
            evidence=(
                "Evidence-run artifacts are present"
                + (f" for {planned} planned model row(s)." if planned else ".")
            ),
            next_action="None.",
            source=inputs.result_artifact_audit_path,
        )
    text = _read(inputs.final_sweep_plan_path)
    run_allowed = _line_value(text, "Run allowed:") or "unknown"
    blockers = _bullet_block(text, "## Current Blockers")
    status: BlockerStatus = "pass" if run_allowed == "YES" else "waiting"
    evidence = f"Run allowed: {run_allowed}."
    if blockers:
        evidence += " Current blocker(s): " + "; ".join(blockers) + "."
    return PaperBlocker(
        area="final model sweep",
        status=status,
        dependency="provider run after readiness",
        evidence=evidence,
        next_action=(
            "Do not run provider/model arrays until readiness passes and the "
            "sweep plan says `Run allowed: YES`."
            if status != "pass"
            else (
                "Confirm explicit run approval and cost ceiling, then execute "
                "the frozen sweep commands model by model."
            )
        ),
        source=inputs.final_sweep_plan_path,
    )


def _result_artifact_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    text = _read(inputs.result_artifact_audit_path)
    status = _status_from_overall(text)
    summary = _line_value(text, "Summary:") or _line_value(text, "Overall status:")
    planned = _int(text, r"Planned model rows:\s+(\d+)") or _int(
        text,
        r"Planned models:\s+(\d+)",
    )
    evidence = _join_nonempty(
        [
            summary,
            f"planned model rows: {planned}" if planned is not None else "",
        ]
    )
    return PaperBlocker(
        area="final result artifacts",
        status=status,
        dependency="provider run after readiness",
        evidence=evidence or "Final result audit did not expose a summary line.",
        next_action=(
            "Run the authorized final sweep, summarize/rescore logs, and "
            "generate comparison/report artifacts."
            if status != "pass"
            else "None."
        ),
        source=inputs.result_artifact_audit_path,
    )


def _claim_and_section_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    claim_text = _read(inputs.claim_audit_path)
    section_text = _read(inputs.section_tracker_path)
    claim_status = _status_from_overall(claim_text)
    blocked_sections = _int(section_text, r"Blocked sections:\s+(\d+)")
    markers = _int(section_text, r"Unresolved markers:\s+(\d+)")
    placeholders = _int(section_text, r"Placeholder mentions:\s+(\d+)")
    status: BlockerStatus = (
        "pass"
        if claim_status == "pass"
        and (blocked_sections or 0) == 0
        and (markers or 0) == 0
        and (placeholders or 0) == 0
        else "blocked"
    )
    evidence = (
        f"{blocked_sections or 0} blocked section(s); "
        f"{markers or 0} unresolved marker(s); "
        f"{placeholders or 0} placeholder mention(s)."
    )
    return PaperBlocker(
        area="claim and section closure",
        status=status,
        dependency="paper writing after evidence",
        evidence=evidence,
        next_action=(
            "Replace claim markers only when the claim ledger points to fixed "
            + (
                "result, metadata, or release evidence; do not add measured "
                "human-baseline claims in preprint mode."
                if inputs.publication_mode == "preprint"
                else "human-baseline, result, metadata, or release evidence."
            )
            if status != "pass"
            else "None."
        ),
        source=inputs.section_tracker_path,
    )


def _source_and_pdf_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    source_text = _read(inputs.source_audit_path)
    pdf_text = _read(inputs.pdf_audit_path)
    source_status = _status_from_overall(source_text)
    pdf_status = _status_from_overall(pdf_text)
    pdf_summary = _line_value(pdf_text, "Summary:")
    source_summary = _line_value(source_text, "Summary:")
    status: BlockerStatus = (
        "pass" if source_status == "pass" and pdf_status == "pass" else "blocked"
    )
    evidence = _join_nonempty([f"source: {source_summary}", f"PDF: {pdf_summary}"])
    return PaperBlocker(
        area="source and PDF build",
        status=status,
        dependency="local writing and LaTeX environment",
        evidence=evidence,
        next_action=(
            "Resolve TeX markers, build PDF with LaTeX, inspect the PDF, and "
            "rerun `make -C paper pdf-audit`."
            if status != "pass"
            else "None."
        ),
        source=inputs.pdf_audit_path,
    )


def _submission_preflight_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    text = _read(inputs.preflight_path)
    status = _status_from_summary(text)
    summary = _line_value(text, "Summary:")
    return PaperBlocker(
        area="arXiv submission preflight",
        status=status,
        dependency="aggregate release gate",
        evidence=summary or "Preflight summary missing.",
        next_action=(
            (
                "Rerun `make -C paper preflight` after claims, PDF, toolchain, "
                "release, and metadata blockers are resolved."
                if inputs.publication_mode == "preprint"
                else "Rerun `make -C paper preflight` after human-baseline, "
                "claims, PDF, toolchain, and metadata blockers are resolved."
            )
            if status != "pass"
            else "None."
        ),
        source=inputs.preflight_path,
    )


def _internal_review_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    text = _read(inputs.internal_review_path)
    status = _status_from_summary(text)
    summary = _line_value(text, "Summary:")
    return PaperBlocker(
        area="internal research review",
        status=status,
        dependency="aggregate research gate",
        evidence=summary or "Internal review summary missing.",
        next_action=(
            "Rerun `make -C paper internal-review` after evidence-backed claims "
            "and final result artifacts exist."
            if status != "pass"
            else "None."
        ),
        source=inputs.internal_review_path,
    )


def _manuscript_completeness_blocker(
    inputs: PaperBlockerDashboardInputs,
) -> PaperBlocker:
    text = _read(inputs.manuscript_completeness_path)
    status = _status_from_overall(text)
    summary = _line_value(text, "Summary:")
    return PaperBlocker(
        area="manuscript completeness",
        status=status,
        dependency="paper writing after evidence",
        evidence=summary or "Manuscript completeness summary missing.",
        next_action=(
            "Resolve missing manuscript components, placeholder language, "
            "unresolved markers, and missing paper assets before final copyedit."
            if status != "pass"
            else "None."
        ),
        source=inputs.manuscript_completeness_path,
    )


def _release_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    text = _read(inputs.release_audit_path)
    status = _status_from_overall(text)
    summary = _line_value(text, "Summary:")
    return PaperBlocker(
        area="public release artifacts",
        status=status,
        dependency="release decision",
        evidence=summary or "Release audit summary missing.",
        next_action=(
            "Confirm license, citation metadata, archive metadata, and public "
            "repository/dataset URLs before confirming arXiv metadata."
            if status != "pass"
            else "None."
        ),
        source=inputs.release_audit_path,
    )


def _metadata_blocker(inputs: PaperBlockerDashboardInputs) -> PaperBlocker:
    text = _read(inputs.metadata_path)
    confirmed = "metadata_status: confirmed" in text
    has_todo = "TODO(" in text
    false_fields = _metadata_false_fields(text)
    status: BlockerStatus = "pass" if confirmed and not has_todo and not false_fields else "blocked"
    evidence = (
        f"metadata_status confirmed: {'yes' if confirmed else 'no'}; "
        f"TODO placeholders: {'yes' if has_todo else 'no'}; "
        f"false fields: {', '.join(false_fields) if false_fields else 'none'}."
    )
    return PaperBlocker(
        area="submission metadata",
        status=status,
        dependency="author/release decision",
        evidence=evidence,
        next_action=(
            "Confirm final title, abstract, authors, category, release links, "
            "submitter status, endorsement status, and AI-tool disclosure."
            if status != "pass"
            else "None."
        ),
        source=inputs.metadata_path,
    )


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _status_from_overall(text: str) -> BlockerStatus:
    line = _line_value(text, "Overall status:")
    if line == "PASS":
        return "pass"
    if line == "BLOCKED":
        return "blocked"
    return "blocked"


def _status_from_summary(text: str) -> BlockerStatus:
    summary = _line_value(text, "Summary:")
    failed = _int(summary, r"(\d+)\s+failed") if summary else None
    if failed == 0:
        return "pass"
    return "blocked"


def _line_value(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    return ""


def _int(text: str, pattern: str) -> int | None:
    match = re.search(pattern, text)
    if not match:
        return None
    return int(match.group(1))


def _bullet_block(text: str, heading: str) -> tuple[str, ...]:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return ()
    bullets: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        if line.startswith("- "):
            bullets.append(line[2:].strip().rstrip("."))
    return tuple(bullets)


def _metadata_false_fields(text: str) -> list[str]:
    fields = (
        "submitter_registered_author",
        "endorsement_checked",
        "submitter_is_author_or_authorized_proxy",
        "title_and_abstract_checked",
    )
    false_fields: list[str] = []
    for field in fields:
        if re.search(rf"^{field}:\s+false\s*$", text, flags=re.M):
            false_fields.append(field)
    return false_fields


def _join_nonempty(parts: list[str]) -> str:
    return " ".join(part for part in parts if part)


def _render_markdown(
    result: PaperBlockerDashboardResult,
    inputs: PaperBlockerDashboardInputs,
) -> str:
    lines = [
        "---",
        "title: ObviousBench arXiv Blocker Dashboard",
        f"date: {inputs.generated_on}",
        "type: status",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench arXiv Blocker Dashboard",
        "",
        "This generated dashboard aggregates the current paper audits into a",
        "single action view. It does not run model providers, collect human data,",
        "choose release metadata, or compile the PDF.",
        "",
        f"Publication mode: `{inputs.publication_mode}`",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        (
            "Summary: "
            f"{result.pass_count} passed, {result.blocked_count} blocked, "
            f"{result.waiting_count} waiting."
        ),
        "",
        "| Area | Status | Dependency | Evidence | Next action | Source |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for blocker in result.blockers:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(blocker.area),
                    blocker.status.upper(),
                    _cell(blocker.dependency),
                    _cell(blocker.evidence),
                    _cell(blocker.next_action),
                    f"`{blocker.source}`",
                ]
            )
            + " |"
        )
    lines.extend(_next_action_sections(result))
    return "\n".join(lines)


def _next_action_sections(result: PaperBlockerDashboardResult) -> list[str]:
    by_dependency: dict[str, list[PaperBlocker]] = {}
    for blocker in result.blockers:
        if blocker.status == "pass":
            continue
        by_dependency.setdefault(blocker.dependency, []).append(blocker)
    lines = ["", "## Blockers By Dependency", ""]
    for dependency, blockers in sorted(by_dependency.items()):
        lines.extend([f"### {dependency}", ""])
        for blocker in blockers:
            lines.append(f"- {blocker.area}: {blocker.next_action}")
        lines.append("")
    return lines


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
