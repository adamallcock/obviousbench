"""Build an arXiv upload handoff from current ObviousBench paper audits."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from obviousbench.research.arxiv_metadata import audit_submission_metadata

HandoffStatus = Literal["pass", "fail"]


@dataclass(frozen=True)
class ArxivSubmissionHandoffInputs:
    output_path: Path
    source_bundle_path: Path = Path("paper/arxiv-src.tar.gz")
    source_bundle_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md"
    )
    pdf_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md"
    )
    preflight_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md"
    )
    release_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md"
    )
    metadata_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md"
    )
    blocker_dashboard_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md"
    )
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class ArxivSubmissionHandoffCheck:
    name: str
    status: HandoffStatus
    evidence: str
    next_action: str


@dataclass(frozen=True)
class ArxivSubmissionHandoffResult:
    output_path: Path
    checks: tuple[ArxivSubmissionHandoffCheck, ...]

    @property
    def ok(self) -> bool:
        return all(check.status == "pass" for check in self.checks)

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    @property
    def failed_count(self) -> int:
        return sum(check.status == "fail" for check in self.checks)

    def check_by_name(self, name: str) -> ArxivSubmissionHandoffCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


def build_arxiv_submission_handoff(
    inputs: ArxivSubmissionHandoffInputs,
) -> ArxivSubmissionHandoffResult:
    """Write an upload-facing handoff without submitting anything."""
    checks = (
        _source_bundle_check(inputs),
        _pdf_check(inputs),
        _preflight_check(inputs),
        _release_check(inputs),
        _metadata_check(inputs),
        _blocker_dashboard_check(inputs),
    )
    result = ArxivSubmissionHandoffResult(
        output_path=inputs.output_path,
        checks=checks,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _source_bundle_check(
    inputs: ArxivSubmissionHandoffInputs,
) -> ArxivSubmissionHandoffCheck:
    audit_text = _read(inputs.source_bundle_audit_path)
    audit_status = _overall(audit_text)
    members = _int(audit_text, r"Members:\s+(\d+)")
    issues = _int(audit_text, r"Issues:\s+(\d+)")
    if not inputs.source_bundle_path.exists():
        return ArxivSubmissionHandoffCheck(
            name="source bundle",
            status="fail",
            evidence=f"Missing source bundle: {inputs.source_bundle_path}",
            next_action="Run `make -C paper arxiv-package` and `make -C paper arxiv-audit`.",
        )
    size = inputs.source_bundle_path.stat().st_size
    if audit_status == "PASS" and issues == 0 and size > 0:
        return ArxivSubmissionHandoffCheck(
            name="source bundle",
            status="pass",
            evidence=(
                f"{inputs.source_bundle_path} exists ({size} bytes); "
                f"bundle audit PASS with {members or 0} member(s), 0 issue(s)."
            ),
            next_action="None.",
        )
    return ArxivSubmissionHandoffCheck(
        name="source bundle",
        status="fail",
        evidence=(
            f"{inputs.source_bundle_path} size {size} bytes; "
            f"bundle audit status {audit_status or 'unknown'}, "
            f"{issues if issues is not None else 'unknown'} issue(s)."
        ),
        next_action="Regenerate and re-audit the arXiv source bundle.",
    )


def _pdf_check(inputs: ArxivSubmissionHandoffInputs) -> ArxivSubmissionHandoffCheck:
    text = _read(inputs.pdf_audit_path)
    status = _overall(text)
    summary = _line_value(text, "Summary:")
    if status == "PASS":
        return ArxivSubmissionHandoffCheck(
            name="PDF build and inspection",
            status="pass",
            evidence=summary or "PDF build audit passed.",
            next_action="None.",
        )
    return ArxivSubmissionHandoffCheck(
        name="PDF build and inspection",
        status="fail",
        evidence=summary or "PDF build audit is missing or blocked.",
        next_action=(
            "Build and inspect `paper/main.pdf`, then rerun "
            "`make -C paper pdf-audit`."
        ),
    )


def _preflight_check(inputs: ArxivSubmissionHandoffInputs) -> ArxivSubmissionHandoffCheck:
    text = _read(inputs.preflight_path)
    status = _overall(text)
    summary = _line_value(text, "Summary:")
    failed = _int(summary, r"(\d+)\s+failed") if summary else None
    if status == "PASS" and failed == 0:
        return ArxivSubmissionHandoffCheck(
            name="submission preflight",
            status="pass",
            evidence=summary or "Preflight passed.",
            next_action="None.",
        )
    return ArxivSubmissionHandoffCheck(
        name="submission preflight",
        status="fail",
        evidence=summary or "Submission preflight is missing or blocked.",
        next_action="Rerun `make -C paper preflight` after upstream blockers are fixed.",
    )


def _release_check(inputs: ArxivSubmissionHandoffInputs) -> ArxivSubmissionHandoffCheck:
    text = _read(inputs.release_audit_path)
    status = _overall(text)
    summary = _line_value(text, "Summary:")
    if status == "PASS":
        return ArxivSubmissionHandoffCheck(
            name="public release artifacts",
            status="pass",
            evidence=summary or "Release audit passed.",
            next_action="None.",
        )
    failed = _int(summary or "", r"(\d+)\s+failed")
    next_action = (
        "Confirm final release metadata and endorsement status; then set "
        "metadata status fields to confirmed."
        if failed == 1 and "| release metadata confirmation | FAIL |" in text
        else (
            "Confirm license, citation metadata, archive metadata, and public "
            "repository/dataset URLs."
        )
    )
    return ArxivSubmissionHandoffCheck(
        name="public release artifacts",
        status="fail",
        evidence=summary or "Public release audit is missing or blocked.",
        next_action=next_action,
    )


def _metadata_check(inputs: ArxivSubmissionHandoffInputs) -> ArxivSubmissionHandoffCheck:
    audit = audit_submission_metadata(inputs.metadata_path)
    if audit.ok:
        return ArxivSubmissionHandoffCheck(
            name="arXiv metadata",
            status="pass",
            evidence=f"Metadata audit passed: {audit.path}",
            next_action="None.",
        )
    shown = "; ".join(audit.issues[:5])
    if len(audit.issues) > 5:
        shown += f"; {len(audit.issues) - 5} additional issue(s) omitted"
    return ArxivSubmissionHandoffCheck(
        name="arXiv metadata",
        status="fail",
        evidence=shown or "Metadata audit failed.",
        next_action=(
            "Confirm final title, abstract, authors, category, license, release "
            "links, submitter status, endorsement status, and AI-tool disclosure."
        ),
    )


def _blocker_dashboard_check(
    inputs: ArxivSubmissionHandoffInputs,
) -> ArxivSubmissionHandoffCheck:
    text = _read(inputs.blocker_dashboard_path)
    status = _overall(text)
    summary = _line_value(text, "Summary:")
    if status == "PASS":
        return ArxivSubmissionHandoffCheck(
            name="blocker dashboard",
            status="pass",
            evidence=summary or "Blocker dashboard passed.",
            next_action="None.",
        )
    return ArxivSubmissionHandoffCheck(
        name="blocker dashboard",
        status="fail",
        evidence=summary or "Blocker dashboard is missing or blocked.",
        next_action="Use `make -C paper blocker-dashboard` to drive remaining fixes.",
    )


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _overall(text: str) -> str:
    return _line_value(text, "Overall status:")


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


def _render_markdown(
    result: ArxivSubmissionHandoffResult,
    inputs: ArxivSubmissionHandoffInputs,
) -> str:
    lines = [
        "---",
        "title: ObviousBench arXiv Submission Handoff",
        f"date: {inputs.generated_on}",
        "type: runbook",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench arXiv Submission Handoff",
        "",
        "This generated handoff describes the current upload packet and the",
        "checks that must pass before using arXiv's submission form. It does not",
        "submit anything, compile LaTeX, publish releases, or run providers.",
        "",
        f"Upload readiness: {'YES' if result.ok else 'NO'}",
        "",
        f"Summary: {result.passed_count} passed, {result.failed_count} failed.",
        "",
        "## Upload Packet",
        "",
        f"- Source bundle: `{inputs.source_bundle_path}`",
        f"- Metadata note: `{inputs.metadata_path}`",
        f"- Source-bundle audit: `{inputs.source_bundle_audit_path}`",
        f"- PDF audit: `{inputs.pdf_audit_path}`",
        f"- Submission preflight: `{inputs.preflight_path}`",
        f"- Public release audit: `{inputs.release_audit_path}`",
        f"- Blocker dashboard: `{inputs.blocker_dashboard_path}`",
        "",
        "## Readiness Checks",
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
            "## Upload Rule",
            "",
            "Do not upload to arXiv until this handoff says `Upload readiness: YES`,",
            "the final PDF has been visually inspected, and the metadata note exactly",
            "matches the final PDF and public release links.",
            "",
        ]
    )
    return "\n".join(lines)


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
