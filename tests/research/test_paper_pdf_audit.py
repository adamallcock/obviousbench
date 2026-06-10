from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.paper_pdf_audit import (
    REQUIRED_FIGURES,
    PaperPdfAuditInputs,
    audit_paper_pdf_build,
)


def _write_minimal_paper(paper_dir: Path, *, with_marker: bool = False) -> None:
    paper_dir.mkdir(parents=True, exist_ok=True)
    paper_dir.joinpath("main.tex").write_text(
        "\n".join(
            [
                "\\documentclass{article}",
                "\\begin{document}",
                "\\title{ObviousBench}",
                "\\maketitle",
                "\\claimblocked{waiting}" if with_marker else "Final text.",
                "\\end{document}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _write_non_placeholder_figures(paper_dir: Path) -> None:
    figures_dir = paper_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    for name in REQUIRED_FIGURES:
        figures_dir.joinpath(name).write_bytes(b"%PDF-1.7\n" + b"figure-bytes" * 600)


def test_pdf_audit_blocks_missing_toolchain_pdf_and_log(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_minimal_paper(paper_dir, with_marker=True)

    result = audit_paper_pdf_build(
        PaperPdfAuditInputs(
            paper_dir=paper_dir,
            output_path=tmp_path / "pdf-audit.md",
            source_audit_output_path=tmp_path / "source-audit.md",
            available_latex_tools=(),
        )
    )

    assert not result.ok
    assert result.check_by_name("LaTeX toolchain").status == "fail"
    assert result.check_by_name("static source audit").status == "fail"
    assert result.check_by_name("PDF artifact").status == "fail"
    assert result.check_by_name("standalone figure artifacts").status == "fail"
    assert result.check_by_name("LaTeX build log").status == "fail"
    assert "Overall status: BLOCKED" in result.output_path.read_text(encoding="utf-8")


def test_pdf_audit_passes_clean_built_pdf_surface(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_minimal_paper(paper_dir)
    _write_non_placeholder_figures(paper_dir)
    paper_dir.joinpath("main.pdf").write_bytes(b"%PDF-1.7\n")
    paper_dir.joinpath("main.log").write_text(
        "This is pdfTeX\nOutput written on main.pdf\n",
        encoding="utf-8",
    )

    result = audit_paper_pdf_build(
        PaperPdfAuditInputs(
            paper_dir=paper_dir,
            output_path=tmp_path / "pdf-audit.md",
            source_audit_output_path=tmp_path / "source-audit.md",
            available_latex_tools=("tectonic",),
        )
    )

    assert result.ok
    assert result.failed_count == 0
    assert "Overall status: PASS" in result.output_path.read_text(encoding="utf-8")


def test_pdf_audit_blocks_placeholder_figure_artifacts(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_minimal_paper(paper_dir)
    _write_non_placeholder_figures(paper_dir)
    (paper_dir / "figures" / "leaderboard.pdf").write_bytes(
        b"%PDF-1.7\nNo result rows available yet."
    )
    paper_dir.joinpath("main.pdf").write_bytes(b"%PDF-1.7\n")
    paper_dir.joinpath("main.log").write_text(
        "This is pdfTeX\nOutput written on main.pdf\n",
        encoding="utf-8",
    )

    result = audit_paper_pdf_build(
        PaperPdfAuditInputs(
            paper_dir=paper_dir,
            output_path=tmp_path / "pdf-audit.md",
            source_audit_output_path=tmp_path / "source-audit.md",
            available_latex_tools=("tectonic",),
        )
    )

    assert not result.ok
    assert result.check_by_name("standalone figure artifacts").status == "fail"
    assert "placeholder-sized figure" in result.check_by_name(
        "standalone figure artifacts"
    ).evidence


def test_pdf_audit_script_writes_report(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_minimal_paper(paper_dir)
    output_path = tmp_path / "pdf-audit.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_paper_pdf.py",
            "--paper-dir",
            str(paper_dir),
            "--out",
            str(output_path),
            "--source-audit-out",
            str(tmp_path / "source-audit.md"),
            "--available-tool",
            "tectonic",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote paper PDF build audit" in result.stdout
    assert output_path.exists()
