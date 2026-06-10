from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.paper_blocker_dashboard import (
    PaperBlockerDashboardInputs,
    build_paper_blocker_dashboard,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _inputs(tmp_path: Path, *, complete: bool = False) -> PaperBlockerDashboardInputs:
    status = "PASS" if complete else "BLOCKED"
    summary = "10 passed, 0 failed" if complete else "7 passed, 5 failed"
    collection = tmp_path / "collection.md"
    threshold = tmp_path / "threshold.md"
    sweep = tmp_path / "sweep.md"
    results = tmp_path / "results.md"
    claims = tmp_path / "claims.md"
    sections = tmp_path / "sections.md"
    source = tmp_path / "source.md"
    pdf = tmp_path / "pdf.md"
    preflight = tmp_path / "preflight.md"
    internal = tmp_path / "internal.md"
    manuscript = tmp_path / "manuscript.md"
    release = tmp_path / "release.md"
    metadata = tmp_path / "metadata.md"
    _write(
        collection,
        (
            f"Overall status: {status}\n"
            "Expected response rows: 4\n"
            f"Completed answer+timing rows: {'4' if complete else '0'}\n"
            f"Missing answers: {'0' if complete else '4'}\n"
            f"Invalid timings: {'0' if complete else '4'}\n"
        ),
    )
    _write(
        threshold,
        (
            f"Overall status: {status}\n"
            f"- Core H0 items: {'2' if complete else '0'}\n"
            f"- Items with no scored data: {'0' if complete else '2'}\n"
            f"- Ignored scored rows: {'0' if complete else '4'}\n"
        ),
    )
    _write(
        sweep,
        (
            f"Run allowed: {'YES' if complete else 'NO'}\n"
            "\n## Current Blockers\n\n"
            + ("" if complete else "- human baseline\n")
        ),
    )
    _write(results, f"Overall status: {status}\nSummary: 6 passed, 0 failed.\n")
    _write(claims, f"Overall status: {status}\n")
    _write(
        sections,
        (
            f"Blocked sections: {'0' if complete else '3'}\n"
            f"Unresolved markers: {'0' if complete else '5'}\n"
            f"Placeholder mentions: {'0' if complete else '4'}\n"
        ),
    )
    _write(source, f"Overall status: {status}\nSummary: 6 passed, 0 failed.\n")
    _write(pdf, f"Overall status: {status}\nSummary: 4 passed, 0 failed.\n")
    _write(preflight, f"Summary: {summary}.\n")
    _write(internal, f"Summary: {summary}.\n")
    _write(
        manuscript,
        (
            f"Overall status: {status}\n"
            "Summary: "
            + (
                "11 passed, 0 blocked, 0 missing"
                if complete
                else "4 passed, 7 blocked, 0 missing"
            )
            + ".\n"
        ),
    )
    _write(release, f"Overall status: {status}\nSummary: 6 passed, 0 failed.\n")
    _write(
        metadata,
        (
            "metadata_status: confirmed\n"
            "submitter_registered_author: true\n"
            "endorsement_checked: true\n"
            "submitter_is_author_or_authorized_proxy: true\n"
            "title_and_abstract_checked: true\n"
            if complete
            else "metadata_status: draft\n"
            "abstract: TODO(replace)\n"
            "submitter_registered_author: false\n"
        ),
    )
    return PaperBlockerDashboardInputs(
        output_path=tmp_path / "dashboard.md",
        collection_audit_path=collection,
        threshold_audit_path=threshold,
        final_sweep_plan_path=sweep,
        result_artifact_audit_path=results,
        claim_audit_path=claims,
        section_tracker_path=sections,
        source_audit_path=source,
        pdf_audit_path=pdf,
        preflight_path=preflight,
        internal_review_path=internal,
        manuscript_completeness_path=manuscript,
        release_audit_path=release,
        metadata_path=metadata,
    )


def test_blocker_dashboard_summarizes_current_blockers(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=False)

    result = build_paper_blocker_dashboard(inputs)

    assert not result.ok
    assert result.blocker_by_area("human-baseline validation").status == "pass"
    assert result.blocker_by_area("final model sweep").status == "waiting"
    assert result.blocker_by_area("submission metadata").status == "blocked"
    assert result.blocker_by_area("manuscript completeness").status == "blocked"
    text = inputs.output_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "Publication mode: `preprint`" in text
    assert "Blockers By Dependency" in text


def test_blocker_dashboard_strict_mode_blocks_human_collection(tmp_path: Path):
    base = _inputs(tmp_path, complete=False)
    inputs = PaperBlockerDashboardInputs(
        **{
            **base.__dict__,
            "publication_mode": "strict",
        }
    )

    result = build_paper_blocker_dashboard(inputs)

    assert result.blocker_by_area("human-baseline collection").status == "blocked"


def test_blocker_dashboard_can_pass_complete_surface(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=True)

    result = build_paper_blocker_dashboard(inputs)

    assert result.ok
    assert result.blocked_count == 0
    assert result.waiting_count == 0
    assert "Overall status: PASS" in inputs.output_path.read_text(encoding="utf-8")


def test_blocker_dashboard_script_writes_report(tmp_path: Path):
    output_path = tmp_path / "dashboard.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_paper_blocker_dashboard.py",
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote paper blocker dashboard" in result.stdout
    assert output_path.exists()
