"""Build an evidence-derived completion roadmap for the ObviousBench paper."""

from __future__ import annotations

import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

RoadmapStatus = Literal["pass", "blocked", "waiting"]
PublicationMode = Literal["strict", "preprint"]


@dataclass(frozen=True)
class PaperCompletionRoadmapInputs:
    output_path: Path
    paper_dir: Path = Path("paper")
    report_plan_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-report-plan.md"
    )
    blocker_dashboard_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md"
    )
    repro_manifest_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-paper-reproducibility-manifest.md"
    )
    threshold_items_path: Path = Path(
        "data/human_baseline/paper_v1_threshold_items.csv"
    )
    threshold_report_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md"
    )
    collection_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md"
    )
    human_baseline_ops_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-operations.md"
    )
    final_sweep_plan_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-final-sweep-plan.md"
    )
    result_artifact_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md"
    )
    internal_review_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-internal-review.md"
    )
    section_tracker_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-report-section-tracker.md"
    )
    manuscript_completeness_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md"
    )
    submission_checklist_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md"
    )
    submission_handoff_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md"
    )
    pdf_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md"
    )
    metadata_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md"
    )
    release_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md"
    )
    release_packet_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-public-release-decision-packet.md"
    )
    generated_on: str = "2026-06-01"
    publication_mode: PublicationMode = "preprint"


@dataclass(frozen=True)
class RoadmapPhase:
    phase: int
    name: str
    status: RoadmapStatus
    evidence: tuple[str, ...]
    actions: tuple[str, ...]
    exit_criteria: tuple[str, ...]


@dataclass(frozen=True)
class PaperCompletionRoadmapResult:
    output_path: Path
    phases: tuple[RoadmapPhase, ...]

    @property
    def ok(self) -> bool:
        return all(phase.status == "pass" for phase in self.phases)

    @property
    def blocked_count(self) -> int:
        return sum(phase.status == "blocked" for phase in self.phases)

    @property
    def waiting_count(self) -> int:
        return sum(phase.status == "waiting" for phase in self.phases)

    @property
    def passed_count(self) -> int:
        return sum(phase.status == "pass" for phase in self.phases)

    def phase_by_name(self, name: str) -> RoadmapPhase:
        for phase in self.phases:
            if phase.name == name:
                return phase
        raise KeyError(name)


def build_paper_completion_roadmap(
    inputs: PaperCompletionRoadmapInputs,
) -> PaperCompletionRoadmapResult:
    """Write the ordered plan from current evidence to a final arXiv article."""
    phases = (
        _source_scaffold_phase(inputs),
        _human_baseline_phase(inputs),
        _final_sweep_phase(inputs),
        _result_integration_phase(inputs),
        _submission_package_phase(inputs),
        _release_and_submit_phase(inputs),
    )
    result = PaperCompletionRoadmapResult(
        output_path=inputs.output_path,
        phases=phases,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _source_scaffold_phase(inputs: PaperCompletionRoadmapInputs) -> RoadmapPhase:
    main_tex = inputs.paper_dir / "main.tex"
    report_plan_exists = inputs.report_plan_path.exists()
    manifest = _read_text(inputs.repro_manifest_path)
    missing_required = _extract_int(manifest, r"Missing required artifacts:\s+(\d+)")
    evidence = [
        _file_evidence("Manuscript source", main_tex),
        _file_evidence("arXiv report plan", inputs.report_plan_path),
        _file_evidence("blocker dashboard", inputs.blocker_dashboard_path),
        _file_evidence("reproducibility manifest", inputs.repro_manifest_path),
    ]
    if missing_required is not None:
        evidence.append(f"Reproducibility manifest missing required artifacts: {missing_required}.")
    status: RoadmapStatus = (
        "pass"
        if main_tex.exists() and report_plan_exists and missing_required == 0
        else "blocked"
    )
    return RoadmapPhase(
        phase=1,
        name="Source scaffold and reproducibility inventory",
        status=status,
        evidence=tuple(evidence),
        actions=(
            "Keep `paper/main.tex` as the canonical article source.",
            "Regenerate `make -C paper report-tracker` and "
            "`make -C paper blocker-dashboard` after paper artifact changes.",
            "Regenerate `make -C paper repro-manifest` after generated paper "
            "artifacts are refreshed.",
            "Do not move provider logs or private material into the arXiv source bundle.",
        ),
        exit_criteria=(
            "`paper/main.tex`, section TeX files, generated tables, generated "
            "figures, and `paper/arxiv-src.tar.gz` are present.",
            "The blocker dashboard exists and classifies every known open gate.",
            "The reproducibility manifest reports 0 missing required artifacts.",
        ),
    )


def _human_baseline_phase(inputs: PaperCompletionRoadmapInputs) -> RoadmapPhase:
    if inputs.publication_mode == "preprint":
        return RoadmapPhase(
            phase=2,
            name="Human-baseline policy and deferred validation",
            status="pass",
            evidence=(
                "Fast-preprint path selected: measured human-baseline collection "
                "is deferred until the benchmark split is frozen.",
                _file_evidence("Collection audit", inputs.collection_audit_path),
                _file_evidence("Human-baseline operations packet", inputs.human_baseline_ops_path),
            ),
            actions=(
                "Remove empirical human-baseline claims from the manuscript.",
                "Describe human-triviality as a design target supported by reviewed "
                "item cards, answer derivations, ambiguity notes, and deterministic "
                "scorer-gold coverage.",
                "Keep participant packets and threshold tooling as future validation "
                "artifacts, not blockers for the fast preprint.",
            ),
            exit_criteria=(
                "`make -C paper readiness-preprint` passes.",
                "The manuscript does not report human accuracy, response-time "
                "statistics, or core-H0 thresholds.",
                "Human-baseline collection is listed as future work or appendix "
                "infrastructure rather than completed evidence.",
            ),
        )

    counts, row_count = _threshold_status_counts(inputs.threshold_items_path)
    no_data = counts["no_data"]
    core = counts["core_h0"]
    ignored_text = _read_text(inputs.threshold_report_path)
    collection_text = _read_text(inputs.collection_audit_path)
    ops_text = _read_text(inputs.human_baseline_ops_path)
    ignored_rows = _extract_int(ignored_text, r"Ignored scored rows:\s+(\d+)")
    collection_status = _extract_line(collection_text, "Overall status:")
    ops_summary = _extract_line(ops_text, "Summary:")
    expected_collection_rows = _extract_int(
        collection_text, r"Expected response rows:\s+(\d+)"
    )
    completed_collection_rows = _extract_int(
        collection_text, r"Completed answer\+timing rows:\s+(\d+)"
    )
    evidence = [
        _file_evidence("Collection audit", inputs.collection_audit_path),
        _file_evidence("Human-baseline operations packet", inputs.human_baseline_ops_path),
        _file_evidence("Threshold item CSV", inputs.threshold_items_path),
        (
            "Threshold status counts: "
            f"{core} core_h0, {counts['borderline']} borderline, "
            f"{counts['exclude']} exclude, {no_data} no_data across {row_count} item(s)."
        ),
    ]
    if expected_collection_rows is not None and completed_collection_rows is not None:
        evidence.append(
            "Human collection progress: "
            f"{completed_collection_rows}/{expected_collection_rows} "
            "answer+timing row(s) complete."
        )
    if collection_status:
        evidence.append(collection_status)
    if ops_summary:
        evidence.append(ops_summary)
    if ignored_rows is not None:
        evidence.append(f"Ignored scored rows in current threshold audit: {ignored_rows}.")
    status: RoadmapStatus = (
        "pass"
        if row_count > 0
        and no_data == 0
        and core > 0
        and collection_status == "Overall status: PASS"
        else "blocked"
    )
    return RoadmapPhase(
        phase=2,
        name="Human-baseline evidence and core H0 set",
        status=status,
        evidence=tuple(evidence),
        actions=(
            "Collect real answers and timings in "
            "`data/human_baseline/paper_v1_response_template.csv` from at "
            "least 5 participants.",
            "Run `make -C paper human-baseline-audit` until every response "
            "row has a real answer and parseable timing.",
            "Run `make -C paper human-baseline-score` and inspect the scoring "
            "report for missing answers, invalid timings, and scorer failures.",
            "Run `make -C paper human-baseline-thresholds` and use only "
            "`core_h0` items for headline human-trivial claims.",
            "Run `make -C paper human-baseline-ops` after each collection, "
            "scoring, or threshold refresh to keep the handoff current.",
            "Promote checked rows to `data/human_baseline/paper_v1.csv` only "
            "after scoring and threshold audit evidence is complete.",
        ),
        exit_criteria=(
            "Every paper item has scored human response rows with parseable "
            "timings and boolean correctness.",
            "The collection audit passes before response scoring is treated as final.",
            "The threshold audit has 0 `no_data` rows and identifies the final `core_h0` set.",
            "`make -C paper readiness` passes before any final model array is run.",
        ),
    )


def _final_sweep_phase(inputs: PaperCompletionRoadmapInputs) -> RoadmapPhase:
    artifact_text = _read_text(inputs.result_artifact_audit_path)
    artifact_status = _extract_line(artifact_text, "Overall status:")
    planned = _extract_int(artifact_text, r"Planned models:\s+(\d+)") or _extract_int(
        artifact_text,
        r"Planned model rows:\s+(\d+)",
    )
    if _status_is_pass(artifact_status):
        evidence = [
            _file_evidence("Result artifact audit", inputs.result_artifact_audit_path),
            "Final evidence-run artifacts pass."
            + (f" Planned model rows: {planned}." if planned else ""),
        ]
        return RoadmapPhase(
            phase=3,
            name="Final model sweep authorization and execution",
            status="pass",
            evidence=tuple(evidence),
            actions=(
                "Do not run additional provider calls for the first draft unless "
                "a new evidence-run decision is made.",
                "Use the passing evidence-run manifest, summaries, comparison "
                "CSVs, and report artifacts for manuscript claims.",
            ),
            exit_criteria=(
                "Result artifact audit passes.",
                "Paper tables and figures are regenerated from the same evidence run.",
            ),
        )
    sweep_text = _read_text(inputs.final_sweep_plan_path)
    run_allowed = _extract_run_allowed(sweep_text)
    panel_entries = _extract_int(sweep_text, r"Panel entries:\s+(\d+)")
    blockers = _extract_bullet_block(sweep_text, "## Current Blockers")
    evidence = [
        _file_evidence("Final sweep handoff", inputs.final_sweep_plan_path),
        f"Run allowed: {run_allowed or 'unknown'}.",
    ]
    if panel_entries is not None:
        evidence.append(f"Planned model-panel entries: {panel_entries}.")
    if blockers:
        blocker_text = "; ".join(blocker.rstrip(".") for blocker in blockers)
        evidence.append("Current sweep blockers: " + blocker_text + ".")
    status: RoadmapStatus = "pass" if run_allowed == "YES" else "waiting"
    return RoadmapPhase(
        phase=3,
        name="Final model sweep authorization and execution",
        status=status,
        evidence=tuple(evidence),
        actions=(
            "Re-verify model aliases, provider access, and expected cost "
            "immediately before the run.",
            (
                "Run the generated per-model commands only after "
                + (
                    "`make -C paper readiness-preprint` passes and cost is accepted."
                    if inputs.publication_mode == "preprint"
                    else "`make -C paper readiness` passes and cost is accepted."
                )
            ),
            "Summarize and rescore each model into "
            "`results/summaries/paper-v1-final-high-cap/` before comparison artifacts.",
            "Keep raw provider logs out of the paper source bundle.",
        ),
        exit_criteria=(
            "All planned model entries have raw logs and rescored summaries.",
            "The comparison manifest has one complete row per planned model.",
            "No model array is run while `Run allowed: NO` remains in the handoff.",
        ),
    )


def _result_integration_phase(inputs: PaperCompletionRoadmapInputs) -> RoadmapPhase:
    internal_text = _read_text(inputs.internal_review_path)
    section_text = _read_text(inputs.section_tracker_path)
    manuscript_text = _read_text(inputs.manuscript_completeness_path)
    result_artifact_text = _read_text(inputs.result_artifact_audit_path)
    internal_summary = _extract_line(internal_text, "Summary:")
    manuscript_status = _extract_line(manuscript_text, "Overall status:")
    manuscript_summary = _extract_line(manuscript_text, "Summary:")
    artifact_status = _extract_line(result_artifact_text, "Overall status:")
    markers = _extract_int(section_text, r"Unresolved markers:\s+(\d+)")
    placeholders = _extract_int(section_text, r"Placeholder mentions:\s+(\d+)")
    blocked_sections = _extract_int(section_text, r"Blocked sections:\s+(\d+)")
    evidence = [
        _file_evidence("Internal research review", inputs.internal_review_path),
        _file_evidence("Section tracker", inputs.section_tracker_path),
        _file_evidence(
            "Manuscript completeness audit",
            inputs.manuscript_completeness_path,
        ),
        _file_evidence("Final result artifact audit", inputs.result_artifact_audit_path),
    ]
    if internal_summary:
        evidence.append(internal_summary)
    if manuscript_status:
        evidence.append(manuscript_status)
    if manuscript_summary:
        evidence.append(manuscript_summary)
    if artifact_status:
        evidence.append(artifact_status)
    if markers is not None and placeholders is not None and blocked_sections is not None:
        evidence.append(
            f"Section tracker: {blocked_sections} blocked section(s), "
            f"{markers} unresolved marker(s), {placeholders} placeholder mention(s)."
        )
    status: RoadmapStatus = (
        "pass"
        if markers == 0
        and placeholders == 0
        and "0 failed" in internal_summary
        and manuscript_status == "Overall status: PASS"
        else "blocked"
    )
    return RoadmapPhase(
        phase=4,
        name="Result integration and claim closure",
        status=status,
        evidence=tuple(evidence),
        actions=(
            "Regenerate `paper/tables/main_results.tex`, `family_results.tex`, "
            "`provider_exclusions.tex`, and final figures from frozen "
            "comparison artifacts.",
            "Run `make -C paper result-artifacts` before replacing result "
            "placeholders in TeX.",
            "Replace each `\\claimblocked{...}` and `\\obtodo{...}` marker only "
            "where the claim-evidence ledger points to supporting artifacts.",
            "Keep causal explanations in analysis/discussion framed as "
            "hypotheses unless a direct ablation supports them.",
            "Rerun `make -C paper internal-review`, `make -C paper claims`, "
            "`make -C paper manuscript-completeness`, and "
            "`make -C paper report-tracker` after prose changes.",
        ),
        exit_criteria=(
            "The claim audit reports 0 unresolved markers.",
            "The final result artifact audit passes.",
            "The manuscript completeness audit passes.",
            "The section tracker reports 0 blocked sections and 0 placeholder mentions.",
            "The internal research review reports 0 failed checks.",
        ),
    )


def _submission_package_phase(inputs: PaperCompletionRoadmapInputs) -> RoadmapPhase:
    checklist_text = _read_text(inputs.submission_checklist_path)
    handoff_text = _read_text(inputs.submission_handoff_path)
    pdf_audit_text = _read_text(inputs.pdf_audit_path)
    summary = _extract_line(checklist_text, "Summary:")
    handoff_ready = _extract_line(handoff_text, "Upload readiness:")
    handoff_summary = _extract_line(handoff_text, "Summary:")
    pdf_status = _extract_line(pdf_audit_text, "Overall status:")
    pdf_summary = _extract_line(pdf_audit_text, "Summary:")
    failed = _extract_int(summary, r"(\d+) failed")
    evidence = [
        _file_evidence("Submission checklist", inputs.submission_checklist_path),
        _file_evidence("Submission handoff", inputs.submission_handoff_path),
        _file_evidence("PDF build audit", inputs.pdf_audit_path),
        _file_evidence("Submission metadata note", inputs.metadata_path),
    ]
    if summary:
        evidence.append(summary)
    if handoff_ready:
        evidence.append(handoff_ready)
    if handoff_summary:
        evidence.append(handoff_summary)
    if pdf_status:
        evidence.append(pdf_status)
    if pdf_summary:
        evidence.append(pdf_summary)
    status: RoadmapStatus = (
        "pass"
        if failed == 0
        and pdf_status == "Overall status: PASS"
        and handoff_ready == "Upload readiness: YES"
        else "blocked"
    )
    return RoadmapPhase(
        phase=5,
        name="PDF, metadata, and arXiv source package",
        status=status,
        evidence=tuple(evidence),
        actions=(
            "Confirm author list, arXiv category, license, release links, "
            "submitter status, endorsement status, and AI-tool disclosure.",
            "Install or use a LaTeX-enabled environment with `latexmk`, "
            "`pdflatex`, or `tectonic` and run `make -C paper pdf`.",
            "Inspect the generated PDF for table overflow, figure rendering, "
            "citation resolution, and abstract/title consistency.",
            "Run `make -C paper pdf-audit` after every PDF build and resolve "
            "toolchain, PDF artifact, source, and log blockers.",
            "Run `make -C paper arxiv-audit` and `make -C paper preflight` "
            "after the final PDF/source build.",
            "Run `make -C paper submission-handoff` before upload and treat "
            "`Upload readiness: NO` as a hard stop.",
        ),
        exit_criteria=(
            "`paper/main.pdf` exists and has been inspected.",
            "The PDF build audit passes.",
            "The source bundle audit passes with only upload-safe files.",
            "The submission checklist reports 0 failed checks.",
            "The submission handoff reports `Upload readiness: YES`.",
        ),
    )


def _release_and_submit_phase(inputs: PaperCompletionRoadmapInputs) -> RoadmapPhase:
    metadata_text = _read_text(inputs.metadata_path)
    release_audit_text = _read_text(inputs.release_audit_path)
    release_packet_text = _read_text(inputs.release_packet_path)
    metadata_confirmed = "metadata_status: confirmed" in metadata_text
    has_todo = "TODO(" in metadata_text
    release_status = _extract_line(release_audit_text, "Overall status:")
    release_summary = _extract_line(release_audit_text, "Summary:")
    release_packet_status = _extract_line(release_packet_text, "Overall status:")
    release_packet_summary = _extract_line(release_packet_text, "Summary:")
    prior_open = any(
        phase.status != "pass"
        for phase in (
            _human_baseline_phase(inputs),
            _final_sweep_phase(inputs),
            _result_integration_phase(inputs),
            _submission_package_phase(inputs),
        )
    )
    evidence = [
        f"Metadata confirmed: {'yes' if metadata_confirmed else 'no'}.",
        f"Metadata TODO placeholders present: {'yes' if has_todo else 'no'}.",
        _file_evidence("Public release artifact audit", inputs.release_audit_path),
        _file_evidence("Public release decision packet", inputs.release_packet_path),
        f"Earlier roadmap phases still open: {'yes' if prior_open else 'no'}.",
    ]
    if release_status:
        evidence.append(release_status)
    if release_summary:
        evidence.append(release_summary)
    if release_packet_status:
        evidence.append(release_packet_status)
    if release_packet_summary:
        evidence.append(release_packet_summary)
    status: RoadmapStatus = (
        "pass"
        if metadata_confirmed
        and not has_todo
        and not prior_open
        and release_status == "Overall status: PASS"
        and release_packet_status == "Overall status: PASS"
        else "waiting"
    )
    return RoadmapPhase(
        phase=6,
        name="Public release and arXiv submission",
        status=status,
        evidence=tuple(evidence),
        actions=(
            "Tag or archive the exact code/data state used for the paper and "
            "record permanent repository/dataset URLs.",
            "Run `make -C paper release-packet` and resolve every explicit "
            "license, citation, archive, URL, and submitter decision.",
            "Run `make -C paper release-audit` and resolve license, citation, "
            "archive metadata, and public URL blockers.",
            "Confirm the arXiv submitter is an author or authorized proxy and "
            "has any needed endorsement for the selected category.",
            "Submit the final TeX source bundle and matching metadata after all checks pass.",
            "After announcement, record the arXiv identifier and update release "
            "links without changing reported results.",
        ),
        exit_criteria=(
            "Repository and dataset/artifact URLs are public and immutable enough for citation.",
            "The public release decision packet reports 0 decisions needing confirmation.",
            "The public release artifact audit passes.",
            "arXiv metadata is confirmed and matches the final PDF exactly.",
            "The arXiv submission is uploaded from the final audited source bundle.",
        ),
    )


def _threshold_status_counts(path: Path) -> tuple[Counter[str], int]:
    counts: Counter[str] = Counter()
    if not path.exists():
        return counts, 0
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    for row in rows:
        counts[row.get("status", "").strip()] += 1
    return counts, len(rows)


def _file_evidence(label: str, path: Path) -> str:
    if path.exists():
        return f"{label}: present at `{path}`."
    return f"{label}: missing at `{path}`."


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_int(text: str, pattern: str) -> int | None:
    match = re.search(pattern, text)
    if not match:
        return None
    return int(match.group(1))


def _extract_line(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line.strip()
    return ""


def _extract_run_allowed(text: str) -> str | None:
    match = re.search(r"Run allowed:\s+(YES|NO)", text)
    if not match:
        return None
    return match.group(1)


def _status_is_pass(value: str) -> bool:
    return value == "PASS" or value.endswith(": PASS")


def _uses_completed_evidence_run(result: PaperCompletionRoadmapResult) -> bool:
    phase = result.phase_by_name("Final model sweep authorization and execution")
    return phase.status == "pass" and any(
        "Final evidence-run artifacts pass" in evidence for evidence in phase.evidence
    )


def _extract_bullet_block(text: str, heading: str) -> tuple[str, ...]:
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
            bullets.append(line[2:].strip())
    return tuple(bullets)


def _render_markdown(
    result: PaperCompletionRoadmapResult,
    inputs: PaperCompletionRoadmapInputs,
) -> str:
    completed_evidence_run = _uses_completed_evidence_run(result)
    provider_ladder_lines = (
        [
            "make -C paper result-artifacts",
            "# Provider calls are already audited for this evidence snapshot.",
            "# Rerun providers only when intentionally creating a new evidence run.",
        ]
        if completed_evidence_run
        else [
            "make -C paper sweep-plan",
            (
                "# Run final model commands from the sweep plan only after "
                "Run allowed is YES."
            ),
        ]
    )
    if inputs.publication_mode == "preprint" and completed_evidence_run:
        operating_rule = (
            "The current fast-preprint package uses the passing evidence run; "
            "do not run additional provider calls unless intentionally creating "
            "a new evidence snapshot. Human-baseline collection is deferred and "
            "must not appear as measured evidence in the fast preprint."
        )
    elif inputs.publication_mode == "preprint":
        operating_rule = (
            "Do not run the final model array until `make -C paper "
            "readiness-preprint` passes and the final sweep plan says "
            "`Run allowed: YES`. Human-baseline collection is deferred and "
            "must not appear as measured evidence in the fast preprint."
        )
    else:
        operating_rule = (
            "Do not run the final model array until the human-baseline phase "
            "exits with `make -C paper readiness` passing and the final sweep "
            "plan says `Run allowed: YES`."
        )
    lines = [
        "---",
        "title: ObviousBench arXiv Completion Roadmap",
        f"date: {inputs.generated_on}",
        "type: plan",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench arXiv Completion Roadmap",
        "",
        "This roadmap converts the current paper audits into an ordered path from",
        "the local manuscript scaffold to a final arXiv submission. It is",
        "generated from repository evidence and does not run model providers.",
        "",
        f"Publication mode: `{inputs.publication_mode}`",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        (
            "Phase summary: "
            f"{result.passed_count} passed, {result.blocked_count} blocked, "
            f"{result.waiting_count} waiting."
        ),
        "",
        "## Operating Rule",
        "",
        operating_rule,
        "",
        "## Phase Matrix",
        "",
        "| Phase | Name | Status | Key evidence | Next action |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for phase in result.phases:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(phase.phase),
                    _cell(phase.name),
                    phase.status.upper(),
                    _cell(phase.evidence[0] if phase.evidence else ""),
                    _cell(phase.actions[0] if phase.actions else ""),
                ]
            )
            + " |"
        )
    lines.append("")
    for phase in result.phases:
        lines.extend(_phase_lines(phase))
    lines.extend(
        [
            "## Final Verification Ladder",
            "",
            "Run this ladder only after the relevant inputs exist; failing commands",
            "before that point should be treated as evidence, not hidden.",
            "",
            "```bash",
            *(
                [
                    "make -C paper readiness-preprint",
                ]
                if inputs.publication_mode == "preprint"
                else [
                    "make -C paper human-baseline-audit",
                    "make -C paper human-baseline-score",
                    "make -C paper human-baseline-thresholds",
                    "make -C paper human-baseline-ops",
                    "make -C paper readiness",
                ]
            ),
            *provider_ladder_lines,
            "make -C paper assets",
            "make -C paper claim-ledger",
            "make -C paper claims",
            "make -C paper manuscript-completeness",
            "make -C paper report-tracker",
            "make -C paper blocker-dashboard",
            "make -C paper arxiv-package",
            "make -C paper arxiv-audit",
            "make -C paper metadata",
            "make -C paper release-packet",
            "make -C paper pdf-audit",
            "make -C paper release-audit",
            "make -C paper submission-handoff",
            "make -C paper preflight",
            "make -C paper internal-review",
            "make -C paper repro-manifest",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def _phase_lines(phase: RoadmapPhase) -> list[str]:
    lines = [
        f"## Phase {phase.phase}: {phase.name}",
        "",
        f"Status: {phase.status.upper()}",
        "",
        "Evidence:",
        "",
    ]
    lines.extend(f"- {item}" for item in phase.evidence)
    lines.extend(["", "Actions:", ""])
    lines.extend(f"- {item}" for item in phase.actions)
    lines.extend(["", "Exit criteria:", ""])
    lines.extend(f"- {item}" for item in phase.exit_criteria)
    lines.append("")
    return lines


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
