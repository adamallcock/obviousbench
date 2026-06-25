import csv

from obviousbench.analysis.effort_curves import build_effort_curve_rows


def test_build_effort_curve_rows_warns_for_more_tokens_without_accuracy_gain():
    rows = build_effort_curve_rows(
        [
            {
                "model": "openai/model-a",
                "barrage_profile": "balanced",
                "reasoning_summary": "none",
                "reasoning_effort": "minimal",
                "accuracy": "0.8",
                "strict_accuracy": "0.75",
                "total_tokens": "100",
                "reasoning_tokens": "10",
                "estimated_cost_usd": "0.01",
            },
            {
                "model": "openai/model-a",
                "barrage_profile": "balanced",
                "reasoning_summary": "none",
                "reasoning_effort": "high",
                "accuracy": "0.8",
                "strict_accuracy": "0.75",
                "total_tokens": "180",
                "reasoning_tokens": "80",
                "estimated_cost_usd": "0.03",
            },
        ]
    )

    assert [row["effort_order"] for row in rows] == ["0", "3"]
    assert rows[1]["accuracy_delta_from_min_effort"] == "0"
    assert rows[1]["token_delta_from_min_effort"] == "80"
    assert rows[1]["cost_delta_from_min_effort"] == "0.02"
    assert rows[1]["efficiency_warning"] == "higher_cost_no_accuracy_gain"


def test_build_effort_curve_rows_compares_across_reasoning_summary_values():
    rows = build_effort_curve_rows(
        [
            {
                "model": "openai/model-a",
                "barrage_profile": "balanced",
                "reasoning_summary": "none",
                "reasoning_effort": "minimal",
                "accuracy": "0.8",
                "strict_accuracy": "0.75",
                "total_tokens": "100",
                "reasoning_tokens": "10",
                "estimated_cost_usd": "0.01",
            },
            {
                "model": "openai/model-a",
                "barrage_profile": "balanced",
                "reasoning_summary": "auto",
                "reasoning_effort": "high",
                "accuracy": "0.8",
                "strict_accuracy": "0.75",
                "total_tokens": "180",
                "reasoning_tokens": "80",
                "estimated_cost_usd": "0.03",
            },
        ]
    )

    assert rows[1]["reasoning_summary"] == "auto"
    assert rows[1]["token_delta_from_min_effort"] == "80"
    assert rows[1]["efficiency_warning"] == "higher_cost_no_accuracy_gain"


def test_build_effort_curve_rows_warns_for_more_tokens_and_lower_accuracy():
    rows = build_effort_curve_rows(
        [
            {
                "model": "openai/model-a",
                "barrage_profile": "balanced",
                "reasoning_summary": "",
                "reasoning_effort": "low",
                "accuracy": "0.9",
                "strict_accuracy": "0.9",
                "total_tokens": "100",
                "reasoning_tokens": "10",
                "estimated_cost_usd": "",
            },
            {
                "model": "openai/model-a",
                "barrage_profile": "balanced",
                "reasoning_summary": "",
                "reasoning_effort": "medium",
                "accuracy": "0.7",
                "strict_accuracy": "0.7",
                "total_tokens": "140",
                "reasoning_tokens": "40",
                "estimated_cost_usd": "",
            },
        ]
    )

    assert rows[1]["efficiency_warning"] == "higher_tokens_lower_accuracy"


def test_comparison_writes_effort_curve_csv(tmp_path):
    from obviousbench.analysis.comparison import (
        ComparisonBuildInputs,
        build_comparison_from_manifest,
    )

    summary_root = tmp_path / "summaries"
    low_dir = summary_root / "low"
    high_dir = summary_root / "high"
    low_dir.mkdir(parents=True)
    high_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    out_dir = tmp_path / "comparison"
    manifest.write_text(
        "label,summary_dir\nModel Low,low\nModel High,high\n",
        encoding="utf-8",
    )
    for summary_dir, effort, accuracy, tokens, cost in [
        (low_dir, "minimal", "0.8", "100", "0.01"),
        (high_dir, "high", "0.8", "180", "0.03"),
    ]:
        summary_dir.joinpath("summary.csv").write_text(
            "model,barrage_profile,reasoning_summary,reasoning_effort,"
            "total_samples,scored_samples,correct,failures,accuracy,"
            "strict_accuracy,provider_errors,timeouts,total_tokens,reasoning_tokens,"
            "estimated_cost_usd\n"
            f"openai/model-a,balanced,none,{effort},10,10,8,2,{accuracy},"
            f"{accuracy},0,0,{tokens},10,{cost}\n",
            encoding="utf-8",
        )
        summary_dir.joinpath("usage_by_family.csv").write_text(
            "model,family,samples,correct,failures\nopenai/model-a,spelling,10,8,2\n",
            encoding="utf-8",
        )
        summary_dir.joinpath("usage_by_section.csv").write_text(
            "model,family,subfamily,samples,correct,failures\n"
            "openai/model-a,spelling,missing_letter,10,8,2\n",
            encoding="utf-8",
        )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(
            manifest=manifest,
            output_dir=out_dir,
            summary_root=summary_root,
        )
    )

    effort_rows = list(csv.DictReader(paths.effort_curve.open(encoding="utf-8")))
    assert effort_rows[1]["efficiency_warning"] == "higher_cost_no_accuracy_gain"
