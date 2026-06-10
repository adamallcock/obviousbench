"""Internal research-review gate for the ObviousBench arXiv manuscript."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from obviousbench.research.arxiv_readiness import (
    ArxivReadinessInputs,
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

ReviewStatus = Literal["pass", "fail"]

EXPECTED_RELATED_WORK_KEYS = (
    "wang2024mmlupro",
    "rein2023gpqa",
    "phan2026hle",
    "wei2024simpleqa",
    "zhou2023ifeval",
    "jiang2024followbench",
    "white2025livebench",
    "jain2024livecodebench",
    "mirzadeh2025gsmsymbolic",
    "jiang2025benchmarkaging",
    "simplebench",
)
RESULT_PLACEHOLDER_MARKERS = (
    "No final",
    "placeholder",
    "not yet run",
    "not yet collected",
    "claimblocked",
    "obtodo",
)
REQUIRED_MAKE_TARGETS = (
    "assets",
    "readiness",
    "readiness-preprint",
    "related-work",
    "human-baseline-packet",
    "human-baseline-audit",
    "human-baseline-collection-handoff",
    "human-baseline-score",
    "human-baseline-thresholds",
    "human-baseline-promotion",
    "human-baseline-ops",
    "result-artifacts",
    "release-audit",
    "release-packet",
    "claims",
    "pdf",
    "pdf-audit",
    "pdf-handoff",
    "arxiv-package",
    "arxiv-audit",
    "metadata",
    "preflight",
    "submission-handoff",
    "analysis-plan",
    "manuscript-completeness",
    "report-tracker",
    "blocker-dashboard",
    "completion-roadmap",
    "repro-manifest",
)
SOURCE_SAFETY_TERMS = (
    "private",
    "credentials",
    "provider",
)
LIMITATION_TERMS = (
    "does not measure",
    "contamination",
    "pricing",
    "provider",
)


@dataclass(frozen=True)
class InternalReviewInputs:
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
    min_gold_examples_per_scorer: int = 20
    min_human_participants: int = 5
    manifest_scope: bool = True
    readiness_profile: ReadinessProfile = "preprint"


@dataclass(frozen=True)
class InternalReviewCheck:
    name: str
    status: ReviewStatus
    evidence: str
    next_action: str


@dataclass(frozen=True)
class InternalReviewResult:
    output_path: Path
    checks: tuple[InternalReviewCheck, ...]

    @property
    def ok(self) -> bool:
        return all(check.status == "pass" for check in self.checks)

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    @property
    def failed_count(self) -> int:
        return sum(check.status == "fail" for check in self.checks)

    def check_by_name(self, name: str) -> InternalReviewCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


def audit_internal_research_review(
    inputs: InternalReviewInputs,
) -> InternalReviewResult:
    """Audit the manuscript against research-readiness expectations."""
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
    claim_result = audit_paper_claims(
        PaperClaimAuditInputs(
            paper_dir=inputs.paper_dir,
            output_path=inputs.claim_audit_output_path
            or inputs.output_path.parent / "2026-06-01-paper-claim-blocker-audit.md",
        )
    )
    bundle_result = audit_arxiv_source_bundle(
        ArxivBundleAuditInputs(
            bundle_path=inputs.bundle_path,
            output_path=inputs.bundle_audit_output_path
            or inputs.output_path.parent
            / "2026-06-01-obviousbench-arxiv-source-bundle-audit.md",
        )
    )

    checks = (
        _data_claims_check(readiness),
        _claim_evidence_check(claim_result),
        _results_artifact_check(
            inputs.paper_dir,
            include_human_baseline=inputs.readiness_profile == "strict",
        ),
        _reproducibility_check(inputs.paper_dir),
        _source_safety_check(inputs.paper_dir, bundle_result.ok, bundle_result.issues),
        _related_work_check(inputs.paper_dir),
        _limitations_and_interpretation_check(inputs.paper_dir),
    )
    result = InternalReviewResult(output_path=inputs.output_path, checks=checks)
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result), encoding="utf-8")
    return result


def _data_claims_check(readiness) -> InternalReviewCheck:
    failing = [gate for gate in readiness.gates if gate.status == "fail"]
    if not failing:
        return InternalReviewCheck(
            name="data claims against artifacts",
            status="pass",
            evidence=f"{len(readiness.gates)} readiness gate(s) pass.",
            next_action="None.",
        )
    evidence = "; ".join(f"{gate.name}: {gate.message}" for gate in failing[:4])
    return InternalReviewCheck(
        name="data claims against artifacts",
        status="fail",
        evidence=evidence,
        next_action="Resolve failing readiness gates before final data claims.",
    )


def _claim_evidence_check(claim_result) -> InternalReviewCheck:
    if claim_result.ok:
        return InternalReviewCheck(
            name="paper claim evidence",
            status="pass",
            evidence=f"0 unresolved claim marker(s). Audit: {claim_result.output_path}",
            next_action="None.",
        )
    return InternalReviewCheck(
        name="paper claim evidence",
        status="fail",
        evidence=(
            f"{len(claim_result.markers)} unresolved marker(s): "
            f"{claim_result.claimblocked_count} claimblocked, "
            f"{claim_result.obtodo_count} obtodo. Audit: {claim_result.output_path}"
        ),
        next_action="Replace markers only where artifact evidence supports the claim.",
    )


def _results_artifact_check(
    paper_dir: Path,
    *,
    include_human_baseline: bool,
) -> InternalReviewCheck:
    targets = [
        paper_dir / "sections" / "06_results.tex",
        paper_dir / "sections" / "07_analysis.tex",
        paper_dir / "tables" / "main_results.tex",
        paper_dir / "tables" / "family_results.tex",
        paper_dir / "tables" / "provider_exclusions.tex",
    ]
    if include_human_baseline:
        targets.append(paper_dir / "tables" / "human_baseline_summary.tex")
    issues: list[str] = []
    for path in targets:
        if not path.exists():
            issues.append(f"missing {path.relative_to(paper_dir)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in RESULT_PLACEHOLDER_MARKERS:
            if marker.lower() in text.lower():
                issues.append(f"{path.relative_to(paper_dir)} contains {marker!r}")
                break
    if not issues:
        return InternalReviewCheck(
            name="results and analysis artifacts",
            status="pass",
            evidence=f"{len(targets)} result/analysis artifact(s) are non-placeholder.",
            next_action="None.",
        )
    return InternalReviewCheck(
        name="results and analysis artifacts",
        status="fail",
        evidence=_summarize(issues),
        next_action="Regenerate final tables/figures from frozen paper-sweep artifacts.",
    )


def _reproducibility_check(paper_dir: Path) -> InternalReviewCheck:
    makefile = paper_dir / "Makefile"
    readme = paper_dir / "README.md"
    issues: list[str] = []
    if not makefile.exists():
        issues.append("paper/Makefile is missing")
    else:
        targets = set(re.findall(r"^([A-Za-z0-9_.-]+):", makefile.read_text("utf-8"), re.M))
        missing = [target for target in REQUIRED_MAKE_TARGETS if target not in targets]
        if missing:
            issues.append("missing Makefile target(s): " + ", ".join(missing))
    if not readme.exists():
        issues.append("paper/README.md is missing")
    else:
        readme_text = readme.read_text(encoding="utf-8")
        for command in (
            "make assets",
            "make readiness",
            "make readiness-preprint",
            "make human-baseline-packet",
            "make human-baseline-audit",
            "make human-baseline-score",
            "make human-baseline-thresholds",
            "make human-baseline-ops",
            "make result-artifacts",
            "make release-audit",
            "make release-packet",
            "make pdf-audit",
            "make preflight",
            "make submission-handoff",
            "make analysis-plan",
            "make manuscript-completeness",
            "make report-tracker",
            "make blocker-dashboard",
            "make completion-roadmap",
            "make repro-manifest",
        ):
            if command not in readme_text:
                issues.append(f"paper/README.md missing command: {command}")
    if not issues:
        return InternalReviewCheck(
            name="reproducibility commands",
            status="pass",
            evidence="Paper Makefile targets and README commands are present.",
            next_action="None.",
        )
    return InternalReviewCheck(
        name="reproducibility commands",
        status="fail",
        evidence=_summarize(issues),
        next_action="Document and wire every paper build/audit command.",
    )


def _source_safety_check(
    paper_dir: Path,
    bundle_ok: bool,
    bundle_issues: Sequence[str],
) -> InternalReviewCheck:
    issues = list(bundle_issues)
    safety_text = _read_existing(
        paper_dir / "sections" / "09_limitations_ethics_reproducibility.tex"
    ) + _read_existing(paper_dir / "sections" / "appendix.tex")
    lowered = safety_text.lower()
    for term in SOURCE_SAFETY_TERMS:
        if term not in lowered:
            issues.append(f"source-safety discussion missing term: {term}")
    if bundle_ok and not issues:
        return InternalReviewCheck(
            name="source safety and privacy",
            status="pass",
            evidence="Source bundle audit passes and safety/privacy terms are present.",
            next_action="None.",
        )
    return InternalReviewCheck(
        name="source safety and privacy",
        status="fail",
        evidence=_summarize(issues) or "source bundle audit failed",
        next_action="Fix bundle issues and source-safety discussion before upload.",
    )


def _related_work_check(paper_dir: Path) -> InternalReviewCheck:
    related_text = _read_existing(paper_dir / "sections" / "02_related_work.tex")
    references_text = _read_existing(paper_dir / "references.bib")
    missing = [
        key
        for key in EXPECTED_RELATED_WORK_KEYS
        if key not in related_text or f"{{{key}" not in references_text
    ]
    if not missing:
        return InternalReviewCheck(
            name="related work coverage",
            status="pass",
            evidence=f"{len(EXPECTED_RELATED_WORK_KEYS)} comparator citation(s) covered.",
            next_action="None.",
        )
    return InternalReviewCheck(
        name="related work coverage",
        status="fail",
        evidence="missing comparator key(s): " + ", ".join(missing),
        next_action="Add or justify missing comparator coverage.",
    )


def _limitations_and_interpretation_check(paper_dir: Path) -> InternalReviewCheck:
    limitations_text = _read_existing(
        paper_dir / "sections" / "09_limitations_ethics_reproducibility.tex"
    ).lower()
    analysis_text = _read_existing(paper_dir / "sections" / "07_analysis.tex").lower()
    issues = [
        f"limitations section missing term: {term}"
        for term in LIMITATION_TERMS
        if term not in limitations_text
    ]
    if "hypoth" not in analysis_text:
        issues.append("analysis section does not flag causal explanations as hypotheses")
    if not issues:
        return InternalReviewCheck(
            name="limitations and interpretation discipline",
            status="pass",
            evidence="Limitations and hypothesis discipline are explicit.",
            next_action="None.",
        )
    return InternalReviewCheck(
        name="limitations and interpretation discipline",
        status="fail",
        evidence=_summarize(issues),
        next_action="Tighten limitations and avoid unsupported causal explanations.",
    )


def _render_markdown(result: InternalReviewResult) -> str:
    lines = [
        "---",
        "title: ObviousBench arXiv Internal Research Review",
        "date: 2026-06-01",
        "type: review",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench arXiv Internal Research Review",
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


def _read_existing(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _summarize(issues: Sequence[str], *, limit: int = 4) -> str:
    shown = "; ".join(issues[:limit])
    if len(issues) > limit:
        shown += f"; {len(issues) - limit} additional issue(s) omitted"
    return shown


def _markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()
