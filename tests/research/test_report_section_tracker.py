from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.report_section_tracker import (
    ReportSectionTrackerInputs,
    build_report_section_tracker,
)


def _write_paper(paper_dir: Path, section_text: str) -> None:
    sections = paper_dir / "sections"
    sections.mkdir(parents=True)
    paper_dir.joinpath("main.tex").write_text(
        (
            "\\documentclass{article}\n"
            "\\newcommand{\\claimblocked}[1]{#1}\n"
            "\\newcommand{\\obtodo}[1]{#1}\n"
            "\\begin{document}\n"
            "\\begin{abstract}A draft abstract.\\end{abstract}\n"
            "\\input{sections/01_intro}\n"
            "\\end{document}\n"
        ),
        encoding="utf-8",
    )
    sections.joinpath("01_intro.tex").write_text(section_text, encoding="utf-8")


def test_section_tracker_summarizes_clean_sections(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_paper(
        paper_dir,
        (
            "\\section{Introduction}\n"
            "A clean section cites \\citep{known2026}.\n"
            "\\input{tables/results}\n"
            "\\includegraphics{figures/leaderboard.pdf}\n"
        ),
    )
    output_path = tmp_path / "section-tracker.md"

    result = build_report_section_tracker(
        ReportSectionTrackerInputs(paper_dir=paper_dir, output_path=output_path)
    )

    intro = result.entry_by_path("sections/01_intro.tex")
    assert result.blocked_count == 0
    assert intro.title == "Introduction"
    assert intro.status == "draft-clean"
    assert intro.table_inputs == ("tables/results",)
    assert intro.figures == ("figures/leaderboard.pdf",)
    assert intro.citation_count == 1
    assert "Overall status: DRAFT-CLEAN" in output_path.read_text(encoding="utf-8")


def test_section_tracker_records_markers_and_dependencies(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_paper(
        paper_dir,
        (
            "\\section{Results}\n"
            "This table remains a placeholder until final sweep evidence exists.\n"
            "\\claimblocked{Replace human baseline after "
            "data/human_baseline/paper_v1.csv is audited.}\n"
        ),
    )

    result = build_report_section_tracker(
        ReportSectionTrackerInputs(
            paper_dir=paper_dir,
            output_path=tmp_path / "section-tracker.md",
        )
    )

    section = result.entry_by_path("sections/01_intro.tex")
    assert result.blocked_count == 1
    assert result.unresolved_marker_count == 1
    assert section.status == "blocked"
    assert section.claimblocked_count == 1
    assert section.placeholder_count == 1
    assert section.dependencies == ("deferred or audited human-validation evidence",)


def test_section_tracker_script_writes_report(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_paper(paper_dir, "\\section{Related Work}\nComparator coverage.\n")
    output_path = tmp_path / "section-tracker.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_report_section_tracker.py",
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
    assert "Wrote report section tracker" in result.stdout
    assert output_path.exists()
