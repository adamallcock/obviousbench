from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.manuscript_completeness import (
    ManuscriptCompletenessInputs,
    audit_manuscript_completeness,
)


def _write(path: Path, text: str = "content\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_complete_paper(paper_dir: Path, *, blocked: bool = False) -> None:
    marker = "\\claimblocked{final result evidence}\n" if blocked else ""
    _write(
        paper_dir / "main.tex",
        "\\title{ObviousBench}\n"
        "\\author{Ada Example}\n"
        "\\begin{abstract}\n"
        "We introduce a complete manuscript.\n"
        "\\end{abstract}\n"
        + marker,
    )
    _write(
        paper_dir / "sections/01_introduction.tex",
        "\\section{Introduction}\n"
        "Visible failure modes motivate this benchmark. It is not intended to "
        "replace broad benchmarks. Our contributions are listed.\n",
    )
    _write(
        paper_dir / "sections/02_related_work.tex",
        "\\section{Related Work}\n"
        "\\citep{wang2024mmlupro,rein2023gpqa,phan2026hle,wei2024simpleqa}\n"
        "\\citep{zhou2023ifeval,jiang2024followbench,white2025livebench}\n"
        "\\citep{jain2024livecodebench,mirzadeh2025gsmsymbolic,jiang2025benchmarkaging,simplebench}\n",
    )
    _write(
        paper_dir / "sections/03_benchmark.tex",
        "\\section{Benchmark Definition}\n"
        "The acceptance criteria define the scope. Task families are listed. "
        "The benchmark does not measure general intelligence.\n"
        "\\input{tables/dataset_composition}\n",
    )
    _write(
        paper_dir / "sections/04_data_review.tex",
        "\\section{Data Construction and Review}\n"
        "\\paragraph{Item-card lifecycle} Cards are reviewed.\n"
        "\\paragraph{Split policy} Splits are frozen.\n"
        "\\paragraph{Human-validation policy} Measured rows are deferred.\n",
    )
    _write(
        paper_dir / "sections/05_scoring_protocol.tex",
        "\\section{Scoring and Evaluation Protocol}\n"
        "The benchmark uses deterministic scorers. The metric is answer "
        "correctness. Run protocol is frozen.\n"
    )
    _write(
        paper_dir / "sections/06_results.tex",
        "\\section{Results}\n"
        "\\input{tables/main_results}\n"
        "\\input{tables/family_results}\n"
        "\\includegraphics{figures/leaderboard.pdf}\n"
        "\\includegraphics{figures/family_heatmap.pdf}\n"
        "\\includegraphics{figures/answer_format_gap.pdf}\n"
        "\\includegraphics{figures/cost_frontier.pdf}\n",
    )
    _write(
        paper_dir / "sections/07_analysis.tex",
        "\\section{Analysis}\n"
        "We frame mechanisms as hypotheses. Answer versus format failures, "
        "Metamorphic variants, and cost are analyzed.\n"
        "\\input{tables/thinking_group_results}\n"
        "\\input{tables/model_family_results}\n"
        "\\input{tables/failure_type_summary}\n",
    )
    _write(
        paper_dir / "sections/08_discussion.tex",
        "\\section{Discussion}\n"
        "The benchmark is a preflight benchmark. Its narrow scope helps teams "
        "track obvious failure modes.\n",
    )
    _write(
        paper_dir / "sections/09_limitations_ethics_reproducibility.tex",
        "\\section{Limitations, Ethics, and Reproducibility}\n"
        "\\paragraph{Limitations} Scope is narrow.\n"
        "\\paragraph{Ethics and source safety} Private data is excluded.\n"
        "\\paragraph{Reproducibility} Commands are listed.\n"
        "\\input{tables/readiness_gates}\n",
    )
    _write(
        paper_dir / "sections/appendix.tex",
        "\\appendix\n"
        "\\input{tables/scorer_gold_coverage}\n"
        "\\input{tables/model_panel}\n"
        "\\input{tables/related_work_positioning}\n"
        "\\section{Appendix: Item-Card Schema}\n"
        "\\section{Appendix: Reported Results Checklist}\n"
        "\\paragraph{Build commands} make assets\n",
    )
    for table in (
        "dataset_composition",
        "related_work_positioning",
        "scorer_gold_coverage",
        "model_panel",
        "main_results",
        "family_results",
        "thinking_group_results",
        "model_family_results",
        "failure_type_summary",
        "human_baseline_summary",
        "provider_exclusions",
        "readiness_gates",
    ):
        _write(paper_dir / "tables" / f"{table}.tex")
    for figure in (
        "leaderboard.pdf",
        "family_heatmap.pdf",
        "answer_format_gap.pdf",
        "cost_frontier.pdf",
    ):
        _write(paper_dir / "figures" / figure, "%PDF\n")


def test_manuscript_completeness_passes_complete_scaffold(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_complete_paper(paper_dir)

    result = audit_manuscript_completeness(
        ManuscriptCompletenessInputs(
            paper_dir=paper_dir,
            output_path=tmp_path / "audit.md",
        )
    )

    assert result.ok
    assert result.missing_count == 0
    assert result.blocked_count == 0
    text = result.output_path.read_text(encoding="utf-8")
    assert "Overall status: PASS" in text


def test_manuscript_completeness_blocks_markers_and_missing_assets(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_complete_paper(paper_dir, blocked=True)
    (paper_dir / "figures" / "cost_frontier.pdf").unlink()

    result = audit_manuscript_completeness(
        ManuscriptCompletenessInputs(
            paper_dir=paper_dir,
            output_path=tmp_path / "audit.md",
        )
    )

    assert not result.ok
    assert result.check_by_name("title, author block, and abstract").status == "blocked"
    assert result.check_by_name("results").status == "blocked"
    text = result.output_path.read_text(encoding="utf-8")
    assert "unresolved marker" in text
    assert "missing figure `figures/cost_frontier.pdf`" in text


def test_manuscript_completeness_script_writes_report(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    _write_complete_paper(paper_dir, blocked=True)
    output_path = tmp_path / "audit.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_manuscript_completeness.py",
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
    assert "Wrote manuscript completeness audit" in result.stdout
    assert output_path.exists()
