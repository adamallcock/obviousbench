"""Audit the ObviousBench manuscript against expected arXiv report sections."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from obviousbench.research.report_section_tracker import (
    CITE_RE,
    FIGURE_RE,
    TABLE_INPUT_RE,
)

CompletenessStatus = Literal["pass", "blocked", "missing"]

DRAFT_PLACEHOLDER_PATTERNS = (
    "placeholder until",
    "placeholder generated",
    "replace the placeholder",
    "remains a placeholder",
    "not yet run",
    "not yet collected",
)
MARKER_RE = re.compile(r"\\(?:claimblocked|obtodo)\{")


@dataclass(frozen=True)
class ManuscriptComponentSpec:
    name: str
    source_path: str
    purpose: str
    required_phrases: tuple[str, ...] = ()
    required_tables: tuple[str, ...] = ()
    required_figures: tuple[str, ...] = ()
    required_citations: tuple[str, ...] = ()
    final_evidence: str = ""


@dataclass(frozen=True)
class ManuscriptCompletenessInputs:
    paper_dir: Path
    output_path: Path
    generated_on: str = "2026-06-01"
    component_specs: tuple[ManuscriptComponentSpec, ...] = ()


@dataclass(frozen=True)
class ManuscriptCompletenessCheck:
    name: str
    status: CompletenessStatus
    source_path: str
    purpose: str
    evidence: str
    next_action: str


@dataclass(frozen=True)
class ManuscriptCompletenessResult:
    output_path: Path
    checks: tuple[ManuscriptCompletenessCheck, ...]

    @property
    def ok(self) -> bool:
        return self.blocked_count == 0 and self.missing_count == 0

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    @property
    def blocked_count(self) -> int:
        return sum(check.status == "blocked" for check in self.checks)

    @property
    def missing_count(self) -> int:
        return sum(check.status == "missing" for check in self.checks)

    def check_by_name(self, name: str) -> ManuscriptCompletenessCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


DEFAULT_COMPONENT_SPECS: tuple[ManuscriptComponentSpec, ...] = (
    ManuscriptComponentSpec(
        name="title, author block, and abstract",
        source_path="main.tex",
        purpose="submission metadata and headline claim summary",
        required_phrases=("\\title{", "\\author{", "\\begin{abstract}"),
        final_evidence=(
            "confirmed metadata, final model summary, deferred "
            "human-validation note, and release links"
        ),
    ),
    ManuscriptComponentSpec(
        name="introduction and contributions",
        source_path="sections/01_introduction.tex",
        purpose="motivation, scope, contribution list, and non-replacement framing",
        required_phrases=("failure modes", "contributions", "not intended to replace"),
        final_evidence="exact artifact-backed counts and release links",
    ),
    ManuscriptComponentSpec(
        name="related work",
        source_path="sections/02_related_work.tex",
        purpose="positioning against nearby benchmark papers",
        required_citations=(
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
        ),
        final_evidence="latest comparator coverage and final positioning pass",
    ),
    ManuscriptComponentSpec(
        name="benchmark definition",
        source_path="sections/03_benchmark.tex",
        purpose="scope, acceptance criteria, taxonomy, and split description",
        required_phrases=("acceptance", "Task families", "does not measure"),
        required_tables=("tables/dataset_composition",),
        final_evidence="reviewed paper item cards and split-policy evidence",
    ),
    ManuscriptComponentSpec(
        name="data construction and review",
        source_path="sections/04_data_review.tex",
        purpose=(
            "item-card lifecycle, source policy, split policy, and deferred "
            "human-validation policy"
        ),
        required_phrases=("Item-card lifecycle", "Split policy", "Human-validation"),
        final_evidence="reviewed item-card evidence and no measured-human claims",
    ),
    ManuscriptComponentSpec(
        name="scoring and evaluation protocol",
        source_path="sections/05_scoring_protocol.tex",
        purpose="deterministic scoring, metrics, model panel, and run protocol",
        required_phrases=("deterministic scorers", "answer correctness", "Run protocol"),
        final_evidence="frozen analysis plan and accepted model panel",
    ),
    ManuscriptComponentSpec(
        name="results",
        source_path="sections/06_results.tex",
        purpose=(
            "model leaderboard, family results, deferred human validation, and costs"
        ),
        required_tables=(
            "tables/main_results",
            "tables/family_results",
        ),
        required_figures=(
            "figures/leaderboard.pdf",
            "figures/family_heatmap.pdf",
            "figures/answer_format_gap.pdf",
            "figures/cost_frontier.pdf",
        ),
        final_evidence="final sweep summaries and explicit deferred human-validation text",
    ),
    ManuscriptComponentSpec(
        name="analysis",
        source_path="sections/07_analysis.tex",
        purpose="failure slices, answer-format gaps, metamorphic instability, and cost",
        required_tables=(
            "tables/thinking_group_results",
            "tables/model_family_results",
            "tables/failure_type_summary",
        ),
        required_phrases=("hypotheses", "Answer versus format", "Metamorphic"),
        final_evidence="family comparison, paired variants, usage exports, failure gallery",
    ),
    ManuscriptComponentSpec(
        name="discussion",
        source_path="sections/08_discussion.tex",
        purpose="restrained interpretation and product implications",
        required_phrases=("preflight benchmark", "narrow scope", "track obvious failure"),
        final_evidence="final result patterns checked against limitations",
    ),
    ManuscriptComponentSpec(
        name="limitations, ethics, and reproducibility",
        source_path="sections/09_limitations_ethics_reproducibility.tex",
        purpose="scope limits, source safety, and reproducibility promises",
        required_phrases=("Limitations", "Ethics and source safety", "Reproducibility"),
        required_tables=("tables/readiness_gates",),
        final_evidence="public release links, commit hash, run dates, and exclusion policy",
    ),
    ManuscriptComponentSpec(
        name="appendix",
        source_path="sections/appendix.tex",
        purpose="artifact inventory, schema, commands, and result reporting checklist",
        required_phrases=("Item-Card Schema", "Reported Results Checklist", "Build commands"),
        required_tables=(
            "tables/scorer_gold_coverage",
            "tables/model_panel",
            "tables/related_work_positioning",
        ),
        final_evidence="final artifact inventory and appendix tables",
    ),
)


def audit_manuscript_completeness(
    inputs: ManuscriptCompletenessInputs,
) -> ManuscriptCompletenessResult:
    """Write a component-level manuscript completeness audit."""
    specs = inputs.component_specs or DEFAULT_COMPONENT_SPECS
    checks = tuple(_check_component(inputs.paper_dir, spec) for spec in specs)
    result = ManuscriptCompletenessResult(
        output_path=inputs.output_path,
        checks=checks,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _check_component(
    paper_dir: Path,
    spec: ManuscriptComponentSpec,
) -> ManuscriptCompletenessCheck:
    path = paper_dir / spec.source_path
    if not path.exists():
        return ManuscriptCompletenessCheck(
            name=spec.name,
            status="missing",
            source_path=spec.source_path,
            purpose=spec.purpose,
            evidence=f"Missing source file `{spec.source_path}`.",
            next_action=f"Create `{spec.source_path}` and add the required component.",
        )

    text = path.read_text(encoding="utf-8")
    missing_phrases = _missing_phrases(text, spec.required_phrases)
    missing_tables = _missing_asset_refs(paper_dir, text, spec.required_tables, "table")
    missing_figures = _missing_asset_refs(
        paper_dir,
        text,
        spec.required_figures,
        "figure",
    )
    missing_citations = _missing_citations(text, spec.required_citations)
    marker_count = len(MARKER_RE.findall(text))
    placeholder_count = _placeholder_count(text)
    issues = (
        tuple(f"missing phrase `{phrase}`" for phrase in missing_phrases)
        + tuple(f"missing table `{table}`" for table in missing_tables)
        + tuple(f"missing figure `{figure}`" for figure in missing_figures)
        + tuple(f"missing citation `{citation}`" for citation in missing_citations)
        + ((f"{marker_count} unresolved marker(s)",) if marker_count else ())
        + ((f"{placeholder_count} placeholder mention(s)",) if placeholder_count else ())
    )
    if not issues:
        return ManuscriptCompletenessCheck(
            name=spec.name,
            status="pass",
            source_path=spec.source_path,
            purpose=spec.purpose,
            evidence="Required manuscript component, assets, and citations are present.",
            next_action="Final copyedit after all upstream evidence is frozen.",
        )
    return ManuscriptCompletenessCheck(
        name=spec.name,
        status="blocked",
        source_path=spec.source_path,
        purpose=spec.purpose,
        evidence="; ".join(issues),
        next_action=(
            f"Resolve component blockers after {spec.final_evidence}."
            if spec.final_evidence
            else "Resolve component blockers before final submission."
        ),
    )


def _missing_phrases(text: str, phrases: tuple[str, ...]) -> tuple[str, ...]:
    lowered = text.lower()
    return tuple(phrase for phrase in phrases if phrase.lower() not in lowered)


def _missing_asset_refs(
    paper_dir: Path,
    text: str,
    assets: tuple[str, ...],
    asset_type: Literal["table", "figure"],
) -> tuple[str, ...]:
    refs = set(TABLE_INPUT_RE.findall(text) if asset_type == "table" else FIGURE_RE.findall(text))
    missing = []
    for asset in assets:
        if asset not in refs:
            missing.append(asset)
            continue
        path = paper_dir / asset
        if asset_type == "table" and path.suffix == "":
            path = path.with_suffix(".tex")
        if not path.exists():
            missing.append(asset)
    return tuple(missing)


def _missing_citations(text: str, citations: tuple[str, ...]) -> tuple[str, ...]:
    found: set[str] = set()
    for match in CITE_RE.findall(text):
        found.update(item.strip() for item in match.split(",") if item.strip())
    return tuple(citation for citation in citations if citation not in found)


def _placeholder_count(text: str) -> int:
    lowered_lines = text.lower().splitlines()
    return sum(
        1
        for line in lowered_lines
        if any(pattern in line for pattern in DRAFT_PLACEHOLDER_PATTERNS)
    )


def _render_markdown(
    result: ManuscriptCompletenessResult,
    inputs: ManuscriptCompletenessInputs,
) -> str:
    lines = [
        "---",
        "title: ObviousBench Manuscript Completeness Audit",
        f"date: {inputs.generated_on}",
        "type: review",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Manuscript Completeness Audit",
        "",
        "This audit checks whether the LaTeX manuscript has every expected",
        "arXiv report component and whether those components are still blocked",
        "by unresolved markers, placeholder language, missing assets, or missing",
        "comparator citations. It does not run providers, collect human data,",
        "compile LaTeX, or publish anything.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        (
            "Summary: "
            f"{result.passed_count} passed, {result.blocked_count} blocked, "
            f"{result.missing_count} missing."
        ),
        "",
        "## Component Matrix",
        "",
        "| Component | Status | Source | Purpose | Evidence | Next action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for check in result.checks:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(check.name),
                    check.status.upper(),
                    _cell(f"`{check.source_path}`"),
                    _cell(check.purpose),
                    _cell(check.evidence),
                    _cell(check.next_action),
                ]
            )
            + " |"
        )
    blocked = [check for check in result.checks if check.status != "pass"]
    lines.extend(["", "## Outstanding Manuscript Work", ""])
    if not blocked:
        lines.extend(["No manuscript completeness blockers remain.", ""])
        return "\n".join(lines)
    for check in blocked:
        lines.append(f"- {check.name}: {check.next_action}")
    lines.append("")
    return "\n".join(lines)


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
