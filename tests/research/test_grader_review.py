from __future__ import annotations

from pathlib import Path

from obviousbench.research.grader_review import (
    GraderReviewInputs,
    LogCandidateStats,
    SummaryTargets,
    build_grader_review,
    select_matching_log_files,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_select_matching_log_files_prefers_log_matching_final_summary_counts():
    candidates = [
        LogCandidateStats(
            path=Path("raw/model/final.eval"),
            total_samples=80,
            scored_samples=80,
            provider_errors=10,
            timeout_count=0,
        ),
        LogCandidateStats(
            path=Path("raw/model/retry.eval"),
            total_samples=10,
            scored_samples=0,
            provider_errors=10,
            timeout_count=0,
        ),
    ]

    selected, warnings = select_matching_log_files(
        candidates,
        SummaryTargets(total_samples=80, scored_samples=80, provider_errors=10),
        entry_id="paper-grok-4-3",
    )

    assert selected == (Path("raw/model/final.eval"),)
    assert warnings == ()


def test_select_matching_log_files_warns_before_using_all_logs_without_match():
    candidates = [
        LogCandidateStats(
            path=Path("raw/model/first.eval"),
            total_samples=5,
            scored_samples=5,
            provider_errors=0,
            timeout_count=0,
        ),
        LogCandidateStats(
            path=Path("raw/model/second.eval"),
            total_samples=5,
            scored_samples=4,
            provider_errors=1,
            timeout_count=0,
        ),
    ]

    selected, warnings = select_matching_log_files(
        candidates,
        SummaryTargets(total_samples=80, scored_samples=80, provider_errors=0),
        entry_id="paper-unit",
    )

    assert selected == (Path("raw/model/first.eval"), Path("raw/model/second.eval"))
    assert warnings == (
        "paper-unit: no single raw log matched summary counts; using all 2 logs",
    )


def test_build_grader_review_can_use_summary_failure_galleries(tmp_path: Path):
    summary_dir = tmp_path / "summaries" / "unit-run"
    manifest = tmp_path / "manifest.csv"
    _write(
        manifest,
        "label,model,summary_dir\nUnit Model,provider/unit,"
        + str(summary_dir)
        + "\n",
    )
    _write(
        summary_dir / "failure_gallery.md",
        """# ObviousBench Failure Gallery

## Failure 1: character_count

- Model: `provider/unit`
- Sample ID: `sample-1`
- Reference: `run=unit sample=sample-1`
- Question: How many e's are in tree?
- Expected answer: `2`
- Extracted answer: `1`
- Raw model answer: `1`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count letters.

## Failure 2: format_compliance

- Model: `provider/unit`
- Sample ID: `sample-2`
- Reference: `run=unit sample=sample-2`
- Question: Return JSON with the answer.
- Expected answer: `{"answer": "yes"}`
- Extracted answer: `yes`
- Raw model answer: `The answer is yes.`
- Failure type: `format_error`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: The requested schema is explicit.
""",
    )
    _write(
        summary_dir / "usage_by_sample.csv",
        "sample_id,family,subfamily,question,answer_correct,format_correct,strict_correct\n"
        "sample-1,character_count,single_letter_count,How many e's are in tree?,False,True,False\n"
        "sample-2,format_compliance,json_field,Return JSON with the answer.,True,False,False\n",
    )

    result = build_grader_review(
        GraderReviewInputs(
            manifest_path=manifest,
            raw_root=tmp_path / "raw",
            csv_output_path=tmp_path / "wrong-answer-review.csv",
            html_output_path=tmp_path / "wrong-answer-review.html",
            source="summary_galleries",
        )
    )

    assert result.row_count == 2
    assert result.answer_wrong_count == 1
    assert result.format_only_count == 1
    csv_text = result.csv_output_path.read_text(encoding="utf-8")
    assert "answer_wrong" in csv_text
    assert "format_only" in csv_text
    assert "wrong-answer-review.html" in str(result.html_output_path)
