from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.paper_claim_ledger import (
    PaperClaimLedgerInputs,
    build_paper_claim_ledger,
)


def test_build_paper_claim_ledger_classifies_human_and_result_claims(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    sections = paper_dir / "sections"
    sections.mkdir(parents=True)
    paper_dir.joinpath("main.tex").write_text(
        "\\author{\\obtodo{Confirm author list}}\n",
        encoding="utf-8",
    )
    sections.joinpath("data.tex").write_text(
        "\\claimblocked{Human-baseline file needs audited participant rows.}\n",
        encoding="utf-8",
    )
    sections.joinpath("results.tex").write_text(
        "\\claimblocked{Replace final model-comparison table after sweep.}\n",
        encoding="utf-8",
    )
    sections.joinpath("benchmark.tex").write_text(
        "\\claimblocked{Before submission, every paper item must have a reviewed\n"
        "item card with source summary and answer derivation.}\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "ledger.md"

    result = build_paper_claim_ledger(
        PaperClaimLedgerInputs(paper_dir=paper_dir, output_path=output_path)
    )

    assert not result.ok
    assert result.blocked_count == 4
    categories = {entry.category for entry in result.entries}
    assert "human validation" in categories
    assert "final model results" in categories
    assert "submission metadata" in categories
    assert "data and item-card review" in categories
    text = output_path.read_text(encoding="utf-8")
    assert "deferred-validation wording" in text
    assert (
        "results/summaries/"
        "paper-v1-combined-234-overline-attempt-scored-20260602/comparison"
        in text
    )
    assert "submission metadata" in text


def test_paper_claim_ledger_passes_when_no_markers(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    paper_dir.mkdir()
    paper_dir.joinpath("main.tex").write_text(
        "\\author{Ada Example}\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "ledger.md"

    result = build_paper_claim_ledger(
        PaperClaimLedgerInputs(paper_dir=paper_dir, output_path=output_path)
    )

    assert result.ok
    assert result.blocked_count == 0
    assert "Overall status: PASS" in output_path.read_text(encoding="utf-8")


def test_paper_claim_ledger_script_writes_report(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    paper_dir.mkdir()
    paper_dir.joinpath("main.tex").write_text(
        "\\claimblocked{Need final abstract.}\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "ledger.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_paper_claim_ledger.py",
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

    assert result.returncode == 1
    assert "Wrote paper claim ledger" in result.stdout
    assert output_path.exists()
