import csv

from obviousbench.analysis.comparison import (
    ComparisonBuildInputs,
    build_comparison_from_manifest,
)


def test_build_comparison_from_manifest_merges_summary_breakdowns_and_delta(tmp_path):
    summary_root = tmp_path / "summaries"
    run_dir = summary_root / "run-a"
    run_dir.mkdir(parents=True)
    manifest = tmp_path / "manifest.csv"
    baseline = tmp_path / "baseline.csv"
    out_dir = tmp_path / "comparison"

    manifest.write_text(
        "label,summary_dir\nModel A,old/path/run-a\n",
        encoding="utf-8",
    )
    baseline.write_text(
        "label,model,correct,failures,accuracy,summary_dir\n"
        "Model A,openai/model-a,6,4,0.6,old/path/run-a\n",
        encoding="utf-8",
    )
    (run_dir / "summary.csv").write_text(
        "run_variant,model,barrage_profile,reasoning_effort,reasoning_summary,"
        "total_samples,scored_samples,correct,failures,answer_correct,"
        "format_correct,strict_correct,accuracy,answer_accuracy,format_accuracy,"
        "strict_accuracy,obvious_failure_rate,provider_errors,timeouts,"
        "input_tokens,output_tokens,reasoning_tokens,cache_read_tokens,"
        "cache_write_tokens,total_tokens,estimated_cost_usd,cost_source,cost_warnings\n"
        "variant,openai/model-a,balanced_1x10,low,none,10,10,8,2,9,8,7,"
        "0.8,0.9,0.8,0.7,0.2,0,0,100,20,0,0,0,120,0.01,runcost,\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "run_variant,model,family,samples,correct,failures,answer_correct,"
        "format_correct,strict_correct,total_tokens,estimated_cost_usd,"
        "cost_source,cost_warnings\n"
        "variant,openai/model-a,spelling,10,8,2,9,8,7,120,0.01,runcost,\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_section.csv").write_text(
        "run_variant,model,family,subfamily,samples,correct,failures,"
        "answer_correct,format_correct,strict_correct,total_tokens,"
        "estimated_cost_usd,cost_source,cost_warnings\n"
        "variant,openai/model-a,spelling,missing_letter,10,8,2,9,8,7,"
        "120,0.01,runcost,\n",
        encoding="utf-8",
    )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(
            manifest=manifest,
            output_dir=out_dir,
            summary_root=summary_root,
            baseline_comparison=baseline,
        )
    )

    comparison_rows = list(csv.DictReader(paths.comparison.open(encoding="utf-8")))
    family_rows = list(csv.DictReader(paths.family_comparison.open(encoding="utf-8")))
    delta_rows = list(csv.DictReader(paths.delta.open(encoding="utf-8")))

    assert comparison_rows[0]["label"] == "Model A"
    assert comparison_rows[0]["answer_correct"] == "9"
    assert comparison_rows[0]["strict_accuracy"] == "0.7"
    assert comparison_rows[0]["summary_dir"] == str(run_dir)
    assert family_rows[0]["family"] == "spelling"
    assert family_rows[0]["answer_correct"] == "9"
    assert delta_rows[0]["correct_delta"] == "2"
    assert delta_rows[0]["answer_correct_delta"] == "3"
    assert delta_rows[0]["strict_correct_delta"] == "1"


def test_build_comparison_can_apply_manual_xai_costs(tmp_path):
    run_dir = tmp_path / "run-grok"
    run_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    out_dir = tmp_path / "comparison"
    manifest.write_text("label,summary_dir\nGrok,run-grok\n", encoding="utf-8")
    (run_dir / "summary.csv").write_text(
        "model,total_samples,scored_samples,correct,failures,answer_correct,"
        "format_correct,strict_correct,accuracy,answer_accuracy,format_accuracy,"
        "strict_accuracy,obvious_failure_rate,provider_errors,timeouts,"
        "input_tokens,output_tokens,reasoning_tokens,cache_read_tokens,"
        "cache_write_tokens,total_tokens,estimated_cost_usd,cost_source,cost_warnings\n"
        "grok/grok-4.3,1,1,1,0,1,1,1,1,1,1,1,0,0,0,"
        "1000000,1000000,1000000,1000000,1000000,5000000,0,runcost,missing price\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "model,family,samples,correct,failures,answer_correct,format_correct,"
        "strict_correct,input_tokens,output_tokens,reasoning_tokens,"
        "cache_read_tokens,cache_write_tokens,total_tokens,estimated_cost_usd,"
        "cost_source,cost_warnings\n"
        "grok/grok-4.3,object_choice,1,1,0,1,1,1,1000000,1000000,"
        "1000000,1000000,1000000,5000000,0,runcost,missing price\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_section.csv").write_text(
        "model,family,subfamily,samples,correct,failures,answer_correct,"
        "format_correct,strict_correct,input_tokens,output_tokens,"
        "reasoning_tokens,cache_read_tokens,cache_write_tokens,total_tokens,"
        "estimated_cost_usd,cost_source,cost_warnings\n"
        "grok/grok-4.3,object_choice,vehicle,1,1,0,1,1,1,1000000,"
        "1000000,1000000,1000000,1000000,5000000,0,runcost,missing price\n",
        encoding="utf-8",
    )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(
            manifest=manifest,
            output_dir=out_dir,
            manual_xai_costs=True,
        )
    )

    comparison_rows = list(csv.DictReader(paths.comparison.open(encoding="utf-8")))

    assert comparison_rows[0]["estimated_cost_usd"] == "6.45"
    assert comparison_rows[0]["cost_source"] == "xai_docs_2026-05-31"
    assert comparison_rows[0]["cost_warnings"] == ""
