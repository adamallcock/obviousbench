from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.arxiv_metadata import (
    ArxivMetadataInputs,
    audit_submission_metadata,
    build_submission_metadata_template,
)


def test_build_submission_metadata_template_writes_draft_that_does_not_pass(
    tmp_path: Path,
):
    output_path = tmp_path / "metadata.md"

    result = build_submission_metadata_template(
        ArxivMetadataInputs(output_path=output_path)
    )

    text = output_path.read_text(encoding="utf-8")
    assert result.output_path == output_path
    assert "metadata_status: draft" in text
    assert "article_title:" in text

    audit = audit_submission_metadata(output_path)
    assert not audit.ok
    assert any("metadata_status must be confirmed" in issue for issue in audit.issues)
    assert any("TODO placeholder" in issue for issue in audit.issues)


def test_audit_submission_metadata_passes_confirmed_metadata(tmp_path: Path):
    output_path = tmp_path / "metadata.md"
    output_path.write_text(
        """---
title: ObviousBench arXiv Submission Metadata
date: 2026-06-01
type: review
status: confirmed
metadata_status: confirmed
article_title: >-
  ObviousBench: Measuring Human-Trivial Failure Modes in Public-Facing
  Language Models
authors:
  - "Ada Example"
abstract: >-
  We introduce a focused benchmark for short tasks that users perceive as
  obvious and report audited data, deterministic scoring, and model results.
primary_category: "cs.CL"
secondary_categories:
  - "cs.AI"
license: "arXiv.org perpetual, non-exclusive license to distribute"
comments: "Submitted source bundle includes TeX, tables, and figures."
repository_url: "https://example.com/obviousbench"
dataset_url: "https://example.com/obviousbench-data"
ai_tool_disclosure: >-
  AI tools were used for drafting assistance; all claims and artifacts were
  author reviewed.
submitter_registered_author: true
endorsement_checked: true
submitter_is_author_or_authorized_proxy: true
title_and_abstract_checked: true
---

# ObviousBench arXiv Submission Metadata
""",
        encoding="utf-8",
    )

    audit = audit_submission_metadata(output_path)

    assert audit.ok
    assert audit.issues == ()


def test_build_arxiv_submission_metadata_script_writes_template(tmp_path: Path):
    output_path = tmp_path / "metadata.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_arxiv_submission_metadata.py",
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote arXiv submission metadata template" in result.stdout
    assert "metadata_status: draft" in output_path.read_text(encoding="utf-8")
