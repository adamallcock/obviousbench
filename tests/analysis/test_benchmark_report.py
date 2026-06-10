import csv
import shutil
from pathlib import Path

from obviousbench.analysis.benchmark_report import (
    BenchmarkReportInputs,
    _tokens_scatter_svg,
    _uncertainty_cautions,
    build_benchmark_report,
)

REPORT_FIXTURES = Path(__file__).parents[1] / "fixtures" / "benchmark_report"


def test_build_benchmark_report_from_rich_fixture(tmp_path):
    comparison_dir = tmp_path / "comparison"
    shutil.copytree(REPORT_FIXTURES / "rich_comparison", comparison_dir)
    output_dir = tmp_path / "report"

    paths = build_benchmark_report(
        BenchmarkReportInputs(
            comparison_dir=comparison_dir,
            output_dir=output_dir,
            generated_on="2026-05-31",
            title="Rich Fixture Sweep",
        )
    )

    html = paths.html.read_text(encoding="utf-8")
    leaderboard_rows = list(csv.DictReader(paths.leaderboard_csv.open(encoding="utf-8")))
    heatmap_rows = list(csv.DictReader(paths.family_heatmap_csv.open(encoding="utf-8")))
    leaderboard_md = paths.leaderboard_md.read_text(encoding="utf-8")

    assert [row["label"] for row in leaderboard_rows] == [
        "Verbose Correct Model",
        "Strict Model",
        "Provider Flaky Model",
    ]
    assert leaderboard_rows[0]["rank"] == "1"
    assert leaderboard_rows[0]["answer_accuracy_pct"] == "97.5"
    assert leaderboard_rows[0]["format_accuracy_pct"] == "82.5"
    assert leaderboard_rows[0]["strict_accuracy_pct"] == "77.5"
    assert leaderboard_rows[0]["overthinking_index"] == "1.64"
    assert leaderboard_rows[2]["rank"] == ""
    assert leaderboard_rows[2]["provider_errors"] == "12"
    assert leaderboard_rows[2]["timeouts"] == "4"

    flaky_format = [
        row
        for row in heatmap_rows
        if row["label"] == "Provider Flaky Model"
        and row["family"] == "format_compliance"
    ][0]
    assert flaky_format["accuracy_pct"] == "66.67"
    assert flaky_format["samples"] == "10"
    assert flaky_format["scored_samples"] == "6"
    assert flaky_format["provider_errors"] == "2"
    assert flaky_format["timeouts"] == "2"

    assert "Rich Fixture Sweep" in html
    assert "higher_cost_no_accuracy_gain" in html
    assert "high reasoning token share" in html
    assert "rate limited on 12 samples; timed out on 4 samples" in html
    assert "spell.remove.001;spell.remove.002" in html
    assert "Provider Flaky Model</strong>: 12 provider errors" in html
    assert "Accuracy interval cautions" in html
    assert (
        "| 1 | Verbose Correct Model (thinking=medium/reasoning-visible) | 97.5%"
        in leaderboard_md
    )


def test_build_benchmark_report_writes_leaderboard_charts_and_heatmap(tmp_path):
    comparison_dir = tmp_path / "comparison"
    comparison_dir.mkdir()
    output_dir = tmp_path / "report"

    (comparison_dir / "comparison.csv").write_text(
        "\n".join(
            [
                "label,model,barrage_profile,total_samples,scored_samples,correct,failures,"
                "answer_correct,format_correct,strict_correct,accuracy_ci_low,"
                "accuracy_ci_high,answer_accuracy,"
                "format_accuracy,strict_accuracy,provider_errors,timeouts,accuracy,"
                "obvious_failure_rate,input_tokens,"
                "output_tokens,reasoning_tokens,total_tokens,estimated_cost_usd,cost_source,"
                "tokens_per_correct,cost_per_correct_usd,overthinking_index,"
                "cost_warnings,summary_dir",
                "Model A,provider/model-a,balanced_8x10,80,80,72,8,72,76,68,"
                "0.82,0.95,0.9,0.95,0.85,0,0,0.9,0.1,"
                "100,50,0,150,0.02,runcost,2.083333,0.000278,0,,results/a",
                "Model B,provider/model-b,balanced_8x10,80,80,64,16,64,80,64,"
                "0.7,0.88,0.8,1.0,0.8,0,0,0.8,0.2,"
                "100,40,0,140,0.004,runcost,2.1875,0.000063,0,,results/b",
                "Model C,provider/model-c,balanced_8x10,80,0,0,0,0,0,0,"
                "0,0,0,0,0,80,0,0,0,"
                "0,0,0,0,0.0,runcost,,,,provider rate limited,results/c",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (comparison_dir / "family_comparison.csv").write_text(
        "\n".join(
            [
                "label,model,barrage_profile,family,samples,correct,failures,total_tokens,"
                "estimated_cost_usd,summary_dir",
                "Model A,provider/model-a,balanced_8x10,character_count,10,9,1,20,0.002,results/a",
                "Model A,provider/model-a,balanced_8x10,spelling_transform,10,8,2,"
                "20,0.002,results/a",
                "Model B,provider/model-b,balanced_8x10,character_count,10,6,4,20,0.001,results/b",
                "Model B,provider/model-b,balanced_8x10,spelling_transform,10,10,"
                "0,20,0.001,results/b",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (comparison_dir / "section_comparison.csv").write_text(
        "label,model,barrage_profile,family,subfamily,samples,correct,failures,"
        "total_tokens,estimated_cost_usd,summary_dir\n",
        encoding="utf-8",
    )
    (comparison_dir / "effort_curve.csv").write_text(
        "\n".join(
            [
                "model_base,barrage_profile,reasoning_summary,effort_order,"
                "reasoning_effort,accuracy,strict_accuracy,total_tokens,"
                "reasoning_tokens,estimated_cost_usd,accuracy_delta_from_min_effort,"
                "token_delta_from_min_effort,cost_delta_from_min_effort,"
                "efficiency_warning",
                "provider/model-a,balanced_8x10,,2,medium,0.9,0.85,150,100,"
                "0.02,0,10,0.01,higher_cost_no_accuracy_gain",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (comparison_dir / "metamorphic_consistency.csv").write_text(
        "\n".join(
            [
                "label,model,barrage_profile,reasoning_effort,reasoning_summary,"
                "family,groups,samples,scored_samples,consistent_groups,"
                "inconsistent_groups,assessable_groups,unassessable_groups,"
                "mixed_outcome_groups,consistency_rate,mixed_group_ids,summary_dir",
                "Model A,provider/model-a,balanced_8x10,,,spelling_transform,2,4,"
                "4,1,1,2,0,1,0.5,spell.reverse.001,results/a",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    paths = build_benchmark_report(
        BenchmarkReportInputs(
            comparison_dir=comparison_dir,
            output_dir=output_dir,
            generated_on="2026-05-31",
            title="Expanded Sweep",
        )
    )

    assert paths.html == output_dir / "report.html"
    assert paths.leaderboard_csv == output_dir / "leaderboard.csv"
    assert paths.leaderboard_md == output_dir / "leaderboard.md"
    assert paths.family_heatmap_csv == output_dir / "family-heatmap.csv"

    html = paths.html.read_text(encoding="utf-8")
    leaderboard = paths.leaderboard_csv.read_text(encoding="utf-8")
    leaderboard_md = paths.leaderboard_md.read_text(encoding="utf-8")
    heatmap = paths.family_heatmap_csv.read_text(encoding="utf-8")

    assert "Expanded Sweep" in html
    assert "Answer Accuracy vs Run Cost" in html
    assert "Accuracy vs tokens" in html
    assert "Overthinking index" in html
    assert "Efficiency warnings" in html
    assert "higher_cost_no_accuracy_gain" in html
    assert "Accuracy interval" in html
    assert "<svg" in html
    assert 'class="point-label"' in html
    assert "Model A (provider default)" in html
    assert "Model B (provider default)" in html
    assert 'class="point provider-provider frontier"' in html
    assert 'class="frontier-line"' in html
    assert 'class="grid-line"' in html
    assert 'class="tick-label"' in html
    assert ">50%</text>" in html
    assert ">2</text>" in html
    assert ">$0.020000</text>" in html
    assert "Scatter charts omit 1 run with incomplete samples or missing chart values." in html
    assert "Family Accuracy Heatmap" in html
    assert "Metamorphic Consistency" in html
    assert "spell.reverse.001" in html
    assert "Provider Errors" in html
    assert "rate limited" in html
    assert "rank,label,display_label,model,thinking_level,barrage_profile" in leaderboard
    assert "1,Model A,Model A (provider default),provider/model-a" in leaderboard
    assert "90.0,82.0-95.0%" in leaderboard
    assert "strict_accuracy_pct" in leaderboard
    assert (
        "| Rank | Model | Answer Accuracy | 95% CI | Answer | Format | Strict | Cost | "
        "Tokens | Tokens / Correct |"
        in leaderboard_md
    )
    assert (
        "| 1 | Model A (provider default) | 90.0% | 82.0-95.0% | "
        "90.0% | 95.0% | 85.0% | $0.020000 | 0.15k |"
        in leaderboard_md
    )
    assert "Format" in html
    assert "cost_per_correct_usd" in leaderboard
    assert "Model B,spelling_transform,100.00" in heatmap


def test_leaderboard_does_not_treat_reported_tokens_as_configured_thinking(tmp_path):
    comparison_dir = tmp_path / "comparison"
    comparison_dir.mkdir()
    output_dir = tmp_path / "report"

    (comparison_dir / "comparison.csv").write_text(
        "\n".join(
            [
                "label,model,barrage_profile,total_samples,scored_samples,correct,"
                "failures,answer_correct,format_correct,strict_correct,answer_accuracy,"
                "format_accuracy,strict_accuracy,provider_errors,timeouts,total_tokens,"
                "output_tokens,reasoning_tokens,estimated_cost_usd,cost_warnings,"
                "summary_dir",
                "Gemini Default,google/gemini-3.5-flash,balanced_8x10,80,80,80,"
                "0,80,80,80,1,1,1,0,0,21000,200,17000,0.01,,results/gemini",
                "Gemini 2.5 Flash-Lite low_budget_1024,google/gemini-2.5-flash-lite,"
                "balanced_8x10,80,80,"
                "76,4,76,80,76,0.95,1,0.95,0,0,17000,360,14000,0.01,,"
                "results/gemini-budget",
                "Gemini 3.1 Flash-Lite minimal_budget_1024,google/gemini-3.1-flash-lite,"
                "balanced_8x10,80,80,"
                "68,12,68,80,68,0.85,1,0.85,0,0,0,0,0,0.01,,"
                "results/gemini-3-budget-label",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (comparison_dir / "family_comparison.csv").write_text(
        "label,model,barrage_profile,family,samples,correct,failures,total_tokens,"
        "estimated_cost_usd,summary_dir\n",
        encoding="utf-8",
    )

    paths = build_benchmark_report(
        BenchmarkReportInputs(
            comparison_dir=comparison_dir,
            output_dir=output_dir,
            generated_on="2026-06-02",
        )
    )

    leaderboard_rows = list(csv.DictReader(paths.leaderboard_csv.open(encoding="utf-8")))

    assert leaderboard_rows[0]["display_label"] == "Gemini Default (provider default)"
    assert leaderboard_rows[0]["thinking_level"] == "provider default"
    assert leaderboard_rows[0]["reasoning_token_source"] == "reported"
    assert (
        leaderboard_rows[1]["display_label"]
        == "Gemini 2.5 Flash-Lite low_budget_1024 (thinking=low budget=1024)"
    )
    assert leaderboard_rows[1]["thinking_level"] == "thinking=low budget=1024"
    assert (
        leaderboard_rows[2]["display_label"]
        == "Gemini 3.1 Flash-Lite minimal_budget_1024 (provider default)"
    )
    assert leaderboard_rows[2]["thinking_level"] == "provider default"
    assert "reported reasoning" not in paths.leaderboard_csv.read_text(encoding="utf-8")


def test_family_heatmap_uses_scored_samples_denominator(tmp_path):
    comparison_dir = tmp_path / "comparison"
    comparison_dir.mkdir()
    output_dir = tmp_path / "report"

    (comparison_dir / "comparison.csv").write_text(
        "label,model,barrage_profile,total_samples,scored_samples,correct,failures,"
        "accuracy,provider_errors,timeouts,total_tokens,estimated_cost_usd,"
        "cost_warnings,summary_dir\n"
        "Model A,provider/model-a,balanced_8x10,2,1,1,0,1,1,0,100,0.01,,"
        "results/a\n",
        encoding="utf-8",
    )
    (comparison_dir / "family_comparison.csv").write_text(
        "label,model,barrage_profile,family,samples,scored_samples,provider_errors,"
        "timeouts,correct,failures,total_tokens,estimated_cost_usd,summary_dir\n"
        "Model A,provider/model-a,balanced_8x10,character_count,2,1,1,0,1,0,"
        "100,0.01,results/a\n",
        encoding="utf-8",
    )

    paths = build_benchmark_report(
        BenchmarkReportInputs(
            comparison_dir=comparison_dir,
            output_dir=output_dir,
            generated_on="2026-05-31",
        )
    )

    heatmap = paths.family_heatmap_csv.read_text(encoding="utf-8")
    assert "Model A,character_count,100.00,1,2,1,1,0,0,0.01" in heatmap


def test_build_benchmark_report_backfills_accuracy_interval(tmp_path):
    comparison_dir = tmp_path / "comparison"
    comparison_dir.mkdir()
    output_dir = tmp_path / "report"

    (comparison_dir / "comparison.csv").write_text(
        "\n".join(
            [
                "label,model,barrage_profile,total_samples,scored_samples,correct,"
                "failures,accuracy,provider_errors,timeouts,total_tokens,"
                "estimated_cost_usd,cost_warnings,summary_dir",
                "Model A,provider/model-a,balanced_8x10,10,10,8,2,0.8,0,0,150,"
                "0.02,,results/a",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (comparison_dir / "family_comparison.csv").write_text(
        "label,model,barrage_profile,family,samples,correct,failures,total_tokens,"
        "estimated_cost_usd,summary_dir\n",
        encoding="utf-8",
    )

    paths = build_benchmark_report(
        BenchmarkReportInputs(
            comparison_dir=comparison_dir,
            output_dir=output_dir,
            generated_on="2026-05-31",
        )
    )

    leaderboard = paths.leaderboard_csv.read_text(encoding="utf-8")
    leaderboard_md = paths.leaderboard_md.read_text(encoding="utf-8")

    assert "accuracy_ci_95" in leaderboard
    assert "49.0-94.3%" in leaderboard_md


def test_build_benchmark_report_marks_unassessable_metamorphic_groups(tmp_path):
    comparison_dir = tmp_path / "comparison"
    comparison_dir.mkdir()
    output_dir = tmp_path / "report"

    (comparison_dir / "comparison.csv").write_text(
        "label,model,barrage_profile,total_samples,scored_samples,correct,failures,"
        "accuracy,provider_errors,timeouts,total_tokens,estimated_cost_usd,"
        "cost_warnings,summary_dir\n"
        "Model A,provider/model-a,balanced_8x10,1,1,1,0,1,0,0,100,0.01,,"
        "results/a\n",
        encoding="utf-8",
    )
    (comparison_dir / "family_comparison.csv").write_text(
        "label,model,barrage_profile,family,samples,correct,failures,total_tokens,"
        "estimated_cost_usd,summary_dir\n",
        encoding="utf-8",
    )
    (comparison_dir / "metamorphic_consistency.csv").write_text(
        "label,model,barrage_profile,reasoning_effort,reasoning_summary,family,"
        "groups,samples,scored_samples,assessable_groups,unassessable_groups,"
        "consistent_groups,inconsistent_groups,mixed_outcome_groups,"
        "consistency_rate,mixed_group_ids,summary_dir\n"
        "Model A,provider/model-a,balanced_8x10,,,spelling,3,3,3,0,3,0,0,0,,,"
        "results/a\n",
        encoding="utf-8",
    )

    paths = build_benchmark_report(
        BenchmarkReportInputs(
            comparison_dir=comparison_dir,
            output_dir=output_dir,
            generated_on="2026-05-31",
        )
    )

    html = paths.html.read_text(encoding="utf-8")

    assert "Unassessable" in html
    assert "<td>3</td>" in html
    assert "<td>n/a</td>" in html


def test_uncertainty_cautions_parse_percent_bounds_on_both_sides():
    html = _uncertainty_cautions(
        [
            {
                "rank": "1",
                "label": "Model A",
                "accuracy_pct": "90.00",
                "accuracy_ci_95": "82.00% - 95.00%",
            },
            {
                "rank": "2",
                "label": "Model B",
                "accuracy_pct": "50.00",
                "accuracy_ci_95": "45.00% - 55.00%",
            },
        ]
    )

    assert html == ""


def test_scatter_chart_suppresses_colliding_point_labels():
    html = _tokens_scatter_svg(
        [
            {
                "rank": "1",
                "label": "Model A",
                "model": "openai/model-a",
                "tokens_per_correct": "10",
                "accuracy_pct": "90.00",
            },
            {
                "rank": "2",
                "label": "Model B",
                "model": "anthropic/model-b",
                "tokens_per_correct": "10",
                "accuracy_pct": "90.00",
            },
        ]
    )

    assert html.count('class="point-label"') == 1
    assert 'class="label-suppressed"' in html
    assert "Model B label hidden to avoid overlap" in html
