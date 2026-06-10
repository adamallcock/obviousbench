"""Aggregate final arXiv submission checks for the ObviousBench paper."""

from __future__ import annotations

import shutil
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from obviousbench.research.arxiv_metadata import audit_submission_metadata
from obviousbench.research.arxiv_readiness import (
    ArxivReadinessInputs,
    ReadinessGate,
    ReadinessProfile,
    audit_arxiv_readiness,
)
from obviousbench.research.arxiv_source_bundle import (
    ArxivBundleAuditInputs,
    audit_arxiv_source_bundle,
)
from obviousbench.research.paper_claims import (
    PaperClaimAuditInputs,
    audit_paper_claims,
)

PreflightStatus = Literal["pass", "fail"]

DEFAULT_LATEX_TOOLCHAIN_COMMANDS = ("latexmk", "pdflatex", "tectonic")


@dataclass(frozen=True)
class ArxivPreflightInputs:
    dataset_paths: Sequence[Path]
    item_cards_dir: Path
    scorer_gold_dir: Path
    human_baseline_path: Path | None
    paper_manifest_path: Path | None
    paper_dir: Path
    bundle_path: Path
    output_path: Path
    claim_audit_output_path: Path | None = None
    bundle_audit_output_path: Path | None = None
    model_panel_path: Path | None = None
    model_costs_path: Path | None = None
    pdf_path: Path | None = None
    metadata_confirmation_path: Path | None = None
    latex_toolchain_commands: Sequence[str] = DEFAULT_LATEX_TOOLCHAIN_COMMANDS
    available_latex_tools: Sequence[str] | None = None
    min_gold_examples_per_scorer: int = 20
    min_human_participants: int = 5
    manifest_scope: bool = True
    readiness_profile: ReadinessProfile = "preprint"


@dataclass(frozen=True)
class ArxivPreflightCheck:
    name: str
    status: PreflightStatus
    evidence: str
    next_action: str


@dataclass(frozen=True)
class ArxivPreflightResult:
    output_path: Path
    checks: tuple[ArxivPreflightCheck, ...]

    @property
    def ok(self) -> bool:
        return all(check.status == "pass" for check in self.checks)

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    @property
    def failed_count(self) -> int:
        return sum(check.status == "fail" for check in self.checks)

    def check_by_name(self, name: str) -> ArxivPreflightCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


def build_arxiv_preflight(inputs: ArxivPreflightInputs) -> ArxivPreflightResult:
    """Run cheap local checks and write a human-readable submission checklist."""
    checks: list[ArxivPreflightCheck] = []
    readiness = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=inputs.dataset_paths,
            item_cards_dir=inputs.item_cards_dir,
            scorer_gold_dir=inputs.scorer_gold_dir,
            human_baseline_path=inputs.human_baseline_path,
            paper_manifest_path=inputs.paper_manifest_path,
            min_gold_examples_per_scorer=inputs.min_gold_examples_per_scorer,
            min_human_participants=inputs.min_human_participants,
            manifest_scope=inputs.manifest_scope,
            readiness_profile=inputs.readiness_profile,
        )
    )
    checks.extend(_readiness_check(gate) for gate in readiness.gates)

    claim_output_path = inputs.claim_audit_output_path or (
        inputs.output_path.parent / "2026-06-01-paper-claim-blocker-audit.md"
    )
    claim_result = audit_paper_claims(
        PaperClaimAuditInputs(
            paper_dir=inputs.paper_dir,
            output_path=claim_output_path,
        )
    )
    checks.append(
        ArxivPreflightCheck(
            name="paper claim blockers",
            status="pass" if claim_result.ok else "fail",
            evidence=(
                f"{len(claim_result.markers)} unresolved marker(s): "
                f"{claim_result.claimblocked_count} claimblocked, "
                f"{claim_result.obtodo_count} obtodo. "
                f"Audit: {claim_result.output_path}"
            ),
            next_action=(
                "None."
                if claim_result.ok
                else "Replace each marker only after supporting evidence exists."
            ),
        )
    )

    bundle_output_path = inputs.bundle_audit_output_path or (
        inputs.output_path.parent / "2026-06-01-obviousbench-arxiv-source-bundle-audit.md"
    )
    bundle_result = audit_arxiv_source_bundle(
        ArxivBundleAuditInputs(
            bundle_path=inputs.bundle_path,
            output_path=bundle_output_path,
        )
    )
    checks.append(
        ArxivPreflightCheck(
            name="source bundle audit",
            status="pass" if bundle_result.ok else "fail",
            evidence=_bundle_evidence(bundle_result.members, bundle_result.issues)
            + f" Audit: {bundle_result.output_path}",
            next_action=(
                "None."
                if bundle_result.ok
                else "Regenerate the bundle and remove forbidden or missing files."
            ),
        )
    )

    checks.extend(
        [
            _required_file_check(
                "model panel freeze",
                inputs.model_panel_path,
                pass_message="Frozen model-panel file exists.",
                fail_action="Create or confirm the paper evidence-run manifest.",
            ),
            _required_file_check(
                "model cost estimates",
                inputs.model_costs_path,
                pass_message="Dry-run cost-estimate note exists.",
                fail_action="Generate model-panel cost estimates before final sweeps.",
            ),
            _required_file_check(
                "PDF build artifact",
                inputs.pdf_path or inputs.paper_dir / "main.pdf",
                pass_message="Local paper PDF exists.",
                fail_action="Run make -C paper pdf in a LaTeX-enabled environment.",
            ),
            _latex_toolchain_check(inputs),
            _submission_metadata_check(inputs.metadata_confirmation_path),
        ]
    )

    result = ArxivPreflightResult(
        output_path=inputs.output_path,
        checks=tuple(checks),
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result), encoding="utf-8")
    return result


def _readiness_check(gate: ReadinessGate) -> ArxivPreflightCheck:
    return ArxivPreflightCheck(
        name=gate.name,
        status=gate.status,
        evidence=_readiness_evidence(gate),
        next_action=(
            "None."
            if gate.status == "pass"
            else _readiness_next_action(gate.name)
        ),
    )


def _readiness_evidence(gate: ReadinessGate) -> str:
    parts = [gate.message]
    if gate.details:
        parts.extend(gate.details[:3])
        if len(gate.details) > 3:
            parts.append(f"{len(gate.details) - 3} additional detail(s) omitted.")
    return "; ".join(parts)


def _readiness_next_action(name: str) -> str:
    actions = {
        "dataset validation": "Fix dataset/schema issues for the paper manifest items.",
        "item-card review": "Review and de-placeholder all paper manifest item cards.",
        "scorer-gold coverage": "Add scorer-gold fixtures for every scorer used.",
        "human baseline": (
            "Collect audited rows from enough participants covering every paper item."
        ),
        "paper split manifest": "Fix or regenerate the paper split manifest.",
    }
    return actions.get(name, "Resolve the failing readiness gate.")


def _bundle_evidence(members: Sequence[str], issues: Sequence[str]) -> str:
    if not issues:
        return f"{len(members)} bundle member(s), 0 issue(s)."
    shown = "; ".join(issues[:3])
    if len(issues) > 3:
        shown += f"; {len(issues) - 3} additional issue(s) omitted."
    return f"{len(members)} bundle member(s), {len(issues)} issue(s): {shown}."


def _required_file_check(
    name: str,
    path: Path | None,
    *,
    pass_message: str,
    fail_action: str,
) -> ArxivPreflightCheck:
    if path is None:
        return ArxivPreflightCheck(
            name=name,
            status="fail",
            evidence="No path configured.",
            next_action=fail_action,
        )
    if not path.exists():
        return ArxivPreflightCheck(
            name=name,
            status="fail",
            evidence=f"Missing file: {path}",
            next_action=fail_action,
        )
    if path.stat().st_size == 0:
        return ArxivPreflightCheck(
            name=name,
            status="fail",
            evidence=f"Empty file: {path}",
            next_action=fail_action,
        )
    return ArxivPreflightCheck(
        name=name,
        status="pass",
        evidence=f"{pass_message} Path: {path}",
        next_action="None.",
    )


def _latex_toolchain_check(inputs: ArxivPreflightInputs) -> ArxivPreflightCheck:
    available = (
        tuple(inputs.available_latex_tools)
        if inputs.available_latex_tools is not None
        else tuple(
            command
            for command in inputs.latex_toolchain_commands
            if shutil.which(command)
        )
    )
    if available:
        return ArxivPreflightCheck(
            name="LaTeX build toolchain",
            status="pass",
            evidence="Available command(s): " + ", ".join(available),
            next_action="None.",
        )
    return ArxivPreflightCheck(
        name="LaTeX build toolchain",
        status="fail",
        evidence=(
            "No command found among: "
            + ", ".join(inputs.latex_toolchain_commands)
        ),
        next_action="Install latexmk/pdflatex or tectonic before PDF inspection.",
    )


def _submission_metadata_check(path: Path | None) -> ArxivPreflightCheck:
    result = audit_submission_metadata(path)
    if not result.ok:
        evidence = "; ".join(result.issues[:4])
        if len(result.issues) > 4:
            evidence += f"; {len(result.issues) - 4} additional issue(s) omitted"
        return ArxivPreflightCheck(
            name="submission metadata confirmation",
            status="fail",
            evidence=evidence,
            next_action=(
                "Confirm final abstract, authors, arXiv category, license, "
                "release links, submitter status, and AI-tool disclosure."
            ),
        )
    return ArxivPreflightCheck(
        name="submission metadata confirmation",
        status="pass",
        evidence=f"Required metadata is confirmed. Path: {result.path}",
        next_action="None.",
    )


def _render_markdown(result: ArxivPreflightResult) -> str:
    status = "ready" if result.ok else "blocked"
    lines = [
        "---",
        "title: ObviousBench arXiv Submission Checklist",
        "date: 2026-06-01",
        "type: review",
        f"status: {status}",
        "---",
        "",
        "# ObviousBench arXiv Submission Checklist",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"Summary: {result.passed_count} passed, {result.failed_count} failed.",
        "",
        "| Check | Status | Evidence | Next action |",
        "| --- | --- | --- | --- |",
    ]
    for check in result.checks:
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_cell(check.name),
                    check.status.upper(),
                    _markdown_cell(check.evidence),
                    _markdown_cell(check.next_action),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()
