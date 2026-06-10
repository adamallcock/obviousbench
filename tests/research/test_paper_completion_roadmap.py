from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from obviousbench.research.paper_completion_roadmap import (
    PaperCompletionRoadmapInputs,
    build_paper_completion_roadmap,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_threshold_items(path: Path, statuses: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("item_id", "status"))
        writer.writeheader()
        for index, status in enumerate(statuses, start=1):
            writer.writerow({"item_id": f"item-{index}", "status": status})


def _fixture(tmp_path: Path) -> PaperCompletionRoadmapInputs:
    paper_dir = tmp_path / "paper"
    _write(paper_dir / "main.tex", "\\title{ObviousBench}\n")
    report_plan = tmp_path / "report-plan.md"
    blocker_dashboard = tmp_path / "blocker-dashboard.md"
    repro_manifest = tmp_path / "repro.md"
    threshold_items = tmp_path / "threshold-items.csv"
    threshold_report = (
        tmp_path
        / "docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md"
    )
    collection_audit = tmp_path / "collection-audit.md"
    human_baseline_ops = tmp_path / "human-baseline-ops.md"
    final_sweep = tmp_path / "final-sweep.md"
    result_artifact_audit = tmp_path / "result-artifacts.md"
    internal_review = tmp_path / "internal-review.md"
    section_tracker = tmp_path / "section-tracker.md"
    manuscript_completeness = tmp_path / "manuscript-completeness.md"
    submission_checklist = tmp_path / "submission-checklist.md"
    submission_handoff = tmp_path / "submission-handoff.md"
    pdf_audit = tmp_path / "pdf-audit.md"
    metadata = tmp_path / "metadata.md"
    release_audit = tmp_path / "release-audit.md"
    release_packet = tmp_path / "release-packet.md"
    _write(report_plan, "# Report plan\n")
    _write(blocker_dashboard, "Summary: 0 passed, 9 blocked, 1 waiting.\n")
    _write(repro_manifest, "Missing required artifacts: 0\n")
    _write_threshold_items(threshold_items, ["core_h0", "no_data"])
    _write(threshold_report, "Ignored scored rows: 1\n")
    _write(
        collection_audit,
        "Overall status: BLOCKED\n"
        "Expected response rows: 400\n"
        "Completed answer+timing rows: 0\n",
    )
    _write(human_baseline_ops, "Overall status: BLOCKED\nSummary: 1 passed, 5 blocked.\n")
    _write(
        final_sweep,
        "Run allowed: NO\nPanel entries: 12\n\n## Current Blockers\n\n"
        "- human baseline\n\n## Preconditions\n",
    )
    _write(result_artifact_audit, "Overall status: BLOCKED\n")
    _write(internal_review, "Summary: 4 passed, 3 failed.\n")
    _write(
        section_tracker,
        "Blocked sections: 7\nUnresolved markers: 11\nPlaceholder mentions: 10\n",
    )
    _write(
        manuscript_completeness,
        "Overall status: BLOCKED\nSummary: 4 passed, 7 blocked, 0 missing.\n",
    )
    _write(submission_checklist, "Summary: 7 passed, 5 failed.\n")
    _write(submission_handoff, "Upload readiness: NO\nSummary: 1 passed, 5 failed.\n")
    _write(pdf_audit, "Overall status: BLOCKED\nSummary: 1 passed, 3 failed.\n")
    _write(metadata, "metadata_status: draft\nabstract: TODO(replace)\n")
    _write(release_audit, "Overall status: BLOCKED\nSummary: 2 passed, 4 failed.\n")
    _write(
        release_packet,
        "Overall status: BLOCKED\nSummary: 0 ready, 6 need confirmation.\n",
    )
    return PaperCompletionRoadmapInputs(
        output_path=tmp_path / "roadmap.md",
        paper_dir=paper_dir,
        report_plan_path=report_plan,
        blocker_dashboard_path=blocker_dashboard,
        repro_manifest_path=repro_manifest,
        threshold_items_path=threshold_items,
        threshold_report_path=threshold_report,
        collection_audit_path=collection_audit,
        human_baseline_ops_path=human_baseline_ops,
        final_sweep_plan_path=final_sweep,
        result_artifact_audit_path=result_artifact_audit,
        internal_review_path=internal_review,
        section_tracker_path=section_tracker,
        manuscript_completeness_path=manuscript_completeness,
        submission_checklist_path=submission_checklist,
        submission_handoff_path=submission_handoff,
        pdf_audit_path=pdf_audit,
        metadata_path=metadata,
        release_audit_path=release_audit,
        release_packet_path=release_packet,
    )


def test_completion_roadmap_reports_ordered_current_blockers(tmp_path: Path):
    inputs = _fixture(tmp_path)

    result = build_paper_completion_roadmap(inputs)

    assert not result.ok
    assert result.phase_by_name("Source scaffold and reproducibility inventory").status == "pass"
    assert (
        result.phase_by_name("Human-baseline policy and deferred validation").status
        == "pass"
    )
    assert result.phase_by_name("Final model sweep authorization and execution").status == "waiting"
    assert result.blocked_count == 2
    assert result.waiting_count == 2
    text = inputs.output_path.read_text(encoding="utf-8")
    assert "Publication mode: `preprint`" in text
    assert "readiness-preprint" in text
    assert "Human-baseline collection is deferred" in text


def test_completion_roadmap_uses_completed_evidence_run_when_artifacts_pass(
    tmp_path: Path,
):
    inputs = _fixture(tmp_path)
    _write(
        inputs.result_artifact_audit_path,
        "Overall status: PASS\nPlanned models: 234\n",
    )

    result = build_paper_completion_roadmap(inputs)

    phase = result.phase_by_name("Final model sweep authorization and execution")
    assert phase.status == "pass"
    text = inputs.output_path.read_text(encoding="utf-8")
    assert "Planned model rows: 234" in text
    assert "do not run additional provider calls" in text
    assert "make -C paper result-artifacts" in text
    assert "paper-v1-final-high-cap" not in text


def test_completion_roadmap_strict_mode_keeps_human_phase_blocked(tmp_path: Path):
    base = _fixture(tmp_path)
    inputs = PaperCompletionRoadmapInputs(
        **{
            **base.__dict__,
            "publication_mode": "strict",
        }
    )

    result = build_paper_completion_roadmap(inputs)

    assert result.phase_by_name("Human-baseline evidence and core H0 set").status == "blocked"
    text = inputs.output_path.read_text(encoding="utf-8")
    assert "make -C paper human-baseline-thresholds" in text


def test_completion_roadmap_script_writes_report(tmp_path: Path):
    inputs = _fixture(tmp_path)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_paper_completion_roadmap.py",
            "--out",
            str(inputs.output_path),
            "--paper-dir",
            str(inputs.paper_dir),
            "--report-plan",
            str(inputs.report_plan_path),
            "--blocker-dashboard",
            str(inputs.blocker_dashboard_path),
            "--repro-manifest",
            str(inputs.repro_manifest_path),
            "--threshold-items",
            str(inputs.threshold_items_path),
            "--threshold-report",
            str(inputs.threshold_report_path),
            "--collection-audit",
            str(inputs.collection_audit_path),
            "--human-baseline-ops",
            str(inputs.human_baseline_ops_path),
            "--final-sweep-plan",
            str(inputs.final_sweep_plan_path),
            "--result-artifact-audit",
            str(inputs.result_artifact_audit_path),
            "--internal-review",
            str(inputs.internal_review_path),
            "--section-tracker",
            str(inputs.section_tracker_path),
            "--manuscript-completeness",
            str(inputs.manuscript_completeness_path),
            "--submission-checklist",
            str(inputs.submission_checklist_path),
            "--submission-handoff",
            str(inputs.submission_handoff_path),
            "--pdf-audit",
            str(inputs.pdf_audit_path),
            "--metadata",
            str(inputs.metadata_path),
            "--release-audit",
            str(inputs.release_audit_path),
            "--release-packet",
            str(inputs.release_packet_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote paper completion roadmap" in result.stdout
    assert inputs.output_path.exists()


def test_completion_roadmap_script_can_fail_strictly(tmp_path: Path):
    inputs = _fixture(tmp_path)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_paper_completion_roadmap.py",
            "--out",
            str(inputs.output_path),
            "--paper-dir",
            str(inputs.paper_dir),
            "--report-plan",
            str(inputs.report_plan_path),
            "--blocker-dashboard",
            str(inputs.blocker_dashboard_path),
            "--repro-manifest",
            str(inputs.repro_manifest_path),
            "--threshold-items",
            str(inputs.threshold_items_path),
            "--threshold-report",
            str(inputs.threshold_report_path),
            "--collection-audit",
            str(inputs.collection_audit_path),
            "--human-baseline-ops",
            str(inputs.human_baseline_ops_path),
            "--final-sweep-plan",
            str(inputs.final_sweep_plan_path),
            "--result-artifact-audit",
            str(inputs.result_artifact_audit_path),
            "--internal-review",
            str(inputs.internal_review_path),
            "--section-tracker",
            str(inputs.section_tracker_path),
            "--manuscript-completeness",
            str(inputs.manuscript_completeness_path),
            "--submission-checklist",
            str(inputs.submission_checklist_path),
            "--submission-handoff",
            str(inputs.submission_handoff_path),
            "--pdf-audit",
            str(inputs.pdf_audit_path),
            "--metadata",
            str(inputs.metadata_path),
            "--release-audit",
            str(inputs.release_audit_path),
            "--release-packet",
            str(inputs.release_packet_path),
            "--strict",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Wrote paper completion roadmap" in result.stdout
