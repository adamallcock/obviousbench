from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.arxiv_submission_handoff import (
    ArxivSubmissionHandoffInputs,
    build_arxiv_submission_handoff,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _metadata(confirmed: bool) -> str:
    if not confirmed:
        return """---
title: Metadata
status: draft
metadata_status: draft
authors:
  - "TODO(confirm)"
abstract: "TODO(replace)"
article_title: "ObviousBench"
primary_category: "cs.CL"
license: "TODO"
comments: "TODO"
repository_url: "TODO"
dataset_url: "TODO"
ai_tool_disclosure: "TODO"
submitter_registered_author: false
endorsement_checked: false
submitter_is_author_or_authorized_proxy: false
title_and_abstract_checked: false
---
"""
    return """---
title: Metadata
status: confirmed
metadata_status: confirmed
authors:
  - "Ada Example"
abstract: "We introduce ObviousBench and report audited results."
article_title: "ObviousBench"
primary_category: "cs.CL"
license: "CC BY 4.0"
comments: "12 pages, 4 figures"
repository_url: "https://github.com/example/obviousbench"
dataset_url: "https://doi.org/10.0000/example"
ai_tool_disclosure: "AI tools assisted editing and code generation."
submitter_registered_author: true
endorsement_checked: true
submitter_is_author_or_authorized_proxy: true
title_and_abstract_checked: true
---
"""


def _inputs(tmp_path: Path, *, complete: bool) -> ArxivSubmissionHandoffInputs:
    source_bundle = tmp_path / "arxiv-src.tar.gz"
    source_bundle.write_bytes(b"bundle\n")
    source_audit = tmp_path / "source-audit.md"
    pdf_audit = tmp_path / "pdf-audit.md"
    preflight = tmp_path / "preflight.md"
    release = tmp_path / "release.md"
    metadata = tmp_path / "metadata.md"
    dashboard = tmp_path / "dashboard.md"
    if complete:
        _write(source_audit, "Overall status: PASS\nMembers: 4\nIssues: 0\n")
        _write(pdf_audit, "Overall status: PASS\nSummary: 4 passed, 0 failed.\n")
        _write(preflight, "Overall status: PASS\nSummary: 12 passed, 0 failed.\n")
        _write(release, "Overall status: PASS\nSummary: 6 passed, 0 failed.\n")
        _write(dashboard, "Overall status: PASS\nSummary: 10 passed, 0 blocked, 0 waiting.\n")
        _write(metadata, _metadata(confirmed=True))
    else:
        _write(source_audit, "Overall status: PASS\nMembers: 4\nIssues: 0\n")
        _write(pdf_audit, "Overall status: BLOCKED\nSummary: 0 passed, 4 failed.\n")
        _write(preflight, "Overall status: BLOCKED\nSummary: 7 passed, 5 failed.\n")
        _write(release, "Overall status: BLOCKED\nSummary: 2 passed, 4 failed.\n")
        _write(dashboard, "Overall status: BLOCKED\nSummary: 0 passed, 9 blocked, 1 waiting.\n")
        _write(metadata, _metadata(confirmed=False))
    return ArxivSubmissionHandoffInputs(
        output_path=tmp_path / "handoff.md",
        source_bundle_path=source_bundle,
        source_bundle_audit_path=source_audit,
        pdf_audit_path=pdf_audit,
        preflight_path=preflight,
        release_audit_path=release,
        metadata_path=metadata,
        blocker_dashboard_path=dashboard,
    )


def test_submission_handoff_blocks_incomplete_upload_packet(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=False)

    result = build_arxiv_submission_handoff(inputs)

    assert not result.ok
    assert result.check_by_name("source bundle").status == "pass"
    assert result.check_by_name("PDF build and inspection").status == "fail"
    assert result.check_by_name("arXiv metadata").status == "fail"
    text = inputs.output_path.read_text(encoding="utf-8")
    assert "Upload readiness: NO" in text
    assert "Do not upload to arXiv" in text


def test_submission_handoff_passes_complete_upload_packet(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=True)

    result = build_arxiv_submission_handoff(inputs)

    assert result.ok
    assert result.failed_count == 0
    assert "Upload readiness: YES" in inputs.output_path.read_text(encoding="utf-8")


def test_submission_handoff_script_writes_report(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=False)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_arxiv_submission_handoff.py",
            "--out",
            str(inputs.output_path),
            "--source-bundle",
            str(inputs.source_bundle_path),
            "--source-bundle-audit",
            str(inputs.source_bundle_audit_path),
            "--pdf-audit",
            str(inputs.pdf_audit_path),
            "--preflight",
            str(inputs.preflight_path),
            "--release-audit",
            str(inputs.release_audit_path),
            "--metadata",
            str(inputs.metadata_path),
            "--blocker-dashboard",
            str(inputs.blocker_dashboard_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote arXiv submission handoff" in result.stdout
    assert inputs.output_path.exists()
