from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.paper_source_audit import (
    PaperSourceAuditInputs,
    audit_paper_source,
)


def _write_valid_paper(paper_dir: Path) -> None:
    sections = paper_dir / "sections"
    tables = paper_dir / "tables"
    figures = paper_dir / "figures"
    sections.mkdir(parents=True)
    tables.mkdir()
    figures.mkdir()
    paper_dir.joinpath("main.tex").write_text(
        (
            "\\documentclass{article}\n"
            "\\begin{document}\n"
            "\\input{sections/intro}\n"
            "\\bibliographystyle{plainnat}\n"
            "\\bibliography{references}\n"
            "\\end{document}\n"
        ),
        encoding="utf-8",
    )
    sections.joinpath("intro.tex").write_text(
        (
            "A reviewed claim cites \\citep{known2026}.\n"
            "\\input{tables/results}\n"
            "\\includegraphics[width=\\linewidth]{figures/leaderboard.pdf}\n"
        ),
        encoding="utf-8",
    )
    tables.joinpath("results.tex").write_text("Result & Value \\\\\n", encoding="utf-8")
    figures.joinpath("leaderboard.pdf").write_bytes(b"%PDF-1.4\n%%EOF\n")
    paper_dir.joinpath("references.bib").write_text(
        "@misc{known2026,\n  title={Known Work},\n  year={2026}\n}\n",
        encoding="utf-8",
    )


def test_audit_paper_source_passes_complete_source_tree(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_valid_paper(paper_dir)
    output_path = tmp_path / "source-audit.md"

    result = audit_paper_source(
        PaperSourceAuditInputs(paper_dir=paper_dir, output_path=output_path)
    )

    assert result.ok
    assert result.failed_count == 0
    assert result.check_by_name("citation keys").status == "pass"
    assert "Overall status: PASS" in output_path.read_text(encoding="utf-8")


def test_audit_paper_source_blocks_missing_assets_and_citations(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    paper_dir.mkdir()
    paper_dir.joinpath("main.tex").write_text(
        (
            "\\documentclass{article}\n"
            "\\begin{document}\n"
            "\\input{sections/missing}\n"
            "\\citep{missing2026}\n"
            "\\bibliography{references}\n"
            "\\end{document}\n"
        ),
        encoding="utf-8",
    )
    paper_dir.joinpath("references.bib").write_text("@misc{known2026,}\n")

    result = audit_paper_source(
        PaperSourceAuditInputs(
            paper_dir=paper_dir,
            output_path=tmp_path / "source-audit.md",
        )
    )

    assert not result.ok
    assert result.check_by_name("input files").status == "fail"
    assert result.check_by_name("citation keys").status == "fail"


def test_audit_paper_source_blocks_submission_markers(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_valid_paper(paper_dir)
    (paper_dir / "sections" / "intro.tex").write_text(
        "\\claimblocked{final result missing}\nNo final paper sweep has been run.\n",
        encoding="utf-8",
    )

    result = audit_paper_source(
        PaperSourceAuditInputs(
            paper_dir=paper_dir,
            output_path=tmp_path / "source-audit.md",
        )
    )

    assert not result.ok
    assert result.check_by_name("submission markers").status == "fail"


def test_audit_paper_source_script_writes_report(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_valid_paper(paper_dir)
    output_path = tmp_path / "source-audit.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_paper_source.py",
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
    assert "Wrote paper source audit" in result.stdout
    assert output_path.exists()
