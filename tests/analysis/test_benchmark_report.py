from obviousbench.analysis.benchmark_report import (
    BenchmarkReportInputs,
    build_benchmark_report,
)


def test_build_benchmark_report_writes_leaderboard_charts_and_heatmap(tmp_path):
    comparison_dir = tmp_path / "comparison"
    comparison_dir.mkdir()
    output_dir = tmp_path / "report"

    (comparison_dir / "comparison.csv").write_text(
        "\n".join(
            [
                "label,model,barrage_profile,total_samples,scored_samples,correct,failures,"
                "answer_correct,format_correct,strict_correct,answer_accuracy,"
                "format_accuracy,strict_accuracy,provider_errors,timeouts,accuracy,"
                "obvious_failure_rate,input_tokens,"
                "output_tokens,reasoning_tokens,total_tokens,estimated_cost_usd,cost_source,"
                "cost_warnings,summary_dir",
                "Model A,provider/model-a,balanced_8x10,80,80,72,8,72,76,68,"
                "0.9,0.95,0.85,0,0,0.9,0.1,"
                "100,50,0,150,0.02,runcost,,results/a",
                "Model B,provider/model-b,balanced_8x10,80,80,64,16,64,80,64,"
                "0.8,1.0,0.8,0,0,0.8,0.2,"
                "100,40,0,140,0.004,runcost,,results/b",
                "Model C,provider/model-c,balanced_8x10,80,0,0,0,0,0,0,"
                "0,0,0,80,0,0,0,"
                "0,0,0,0,0.0,runcost,provider rate limited,results/c",
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
    heatmap = paths.family_heatmap_csv.read_text(encoding="utf-8")

    assert "Expanded Sweep" in html
    assert "Accuracy vs Estimated Cost" in html
    assert "<svg" in html
    assert "Family Accuracy Heatmap" in html
    assert "Provider Errors" in html
    assert "rate limited" in html
    assert "rank,label,model,barrage_profile,accuracy_pct" in leaderboard
    assert "1,Model A,provider/model-a,balanced_8x10,90.00" in leaderboard
    assert "strict_accuracy_pct" in leaderboard
    assert "Format" in html
    assert "cost_per_correct_usd" in leaderboard
    assert "Model B,spelling_transform,100.00" in heatmap
