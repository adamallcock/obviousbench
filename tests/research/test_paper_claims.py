from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.paper_claims import (
    PaperClaimAuditInputs,
    audit_paper_claims,
)


def test_audit_paper_claims_finds_claimblocked_and_obtodo(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    sections_dir = paper_dir / "sections"
    sections_dir.mkdir(parents=True)
    paper_dir.joinpath("main.tex").write_text(
        "\\author{\\obtodo{confirm author}}\\n",
        encoding="utf-8",
    )
    sections_dir.joinpath("results.tex").write_text(
        "\\claimblocked{final sweep missing}\\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "claim-audit.md"

    result = audit_paper_claims(
        PaperClaimAuditInputs(paper_dir=paper_dir, output_path=output_path)
    )

    text = output_path.read_text(encoding="utf-8")
    assert not result.ok
    assert result.claimblocked_count == 1
    assert result.obtodo_count == 1
    assert "results.tex:1" in text
    assert "main.tex:1" in text


def test_audit_paper_claims_script_writes_report(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    paper_dir.mkdir()
    paper_dir.joinpath("main.tex").write_text("No blockers.\\n", encoding="utf-8")
    output_path = tmp_path / "claim-audit.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_paper_claims.py",
            "--paper-dir",
            str(paper_dir),
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "0 unresolved paper marker(s)" in result.stdout
    assert "Overall status: PASS" in output_path.read_text(encoding="utf-8")
