import csv

from obviousbench.analysis.comparison import (
    ComparisonBuildInputs,
    build_comparison_from_manifest,
)


def test_build_comparison_from_manifest_merges_summary_breakdowns_and_delta(tmp_path):
    summary_root = tmp_path / "summaries"
    run_dir = summary_root / "run-a"
    old_run_dir = tmp_path / "baseline-run-a"
    run_dir.mkdir(parents=True)
    old_run_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    baseline = tmp_path / "baseline.csv"
    out_dir = tmp_path / "comparison"

    manifest.write_text(
        "label,summary_dir\nModel A,old/path/run-a\n",
        encoding="utf-8",
    )
    baseline.write_text(
        "label,model,correct,failures,accuracy,summary_dir\n"
        f"Model A,openai/model-a,6,4,0.6,{old_run_dir}\n",
        encoding="utf-8",
    )
    (run_dir / "summary.csv").write_text(
        "run_variant,model,barrage_profile,reasoning_effort,reasoning_summary,"
        "total_samples,scored_samples,correct,failures,answer_correct,"
        "format_correct,strict_correct,accuracy,accuracy_ci_low,accuracy_ci_high,"
        "answer_accuracy,format_accuracy,strict_accuracy,obvious_failure_rate,"
        "provider_errors,timeouts,"
        "input_tokens,output_tokens,reasoning_tokens,cache_read_tokens,"
        "cache_write_tokens,total_tokens,estimated_cost_usd,cost_source,cost_warnings\n"
        "variant,openai/model-a,balanced_1x10,low,none,10,10,8,2,9,8,7,"
        "0.8,0.55,0.93,0.9,0.8,0.7,0.2,0,0,100,20,0,0,0,120,0.01,runcost,\n",
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
    (old_run_dir / "usage_by_sample.csv").write_text(
        "sample_id,correct,provider_error,timeout\n"
        "id1,True,False,False\n"
        "id2,False,False,False\n"
        "id3,False,False,False\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_sample.csv").write_text(
        "sample_id,correct,provider_error,timeout\n"
        "id1,True,False,False\n"
        "id2,True,False,False\n"
        "id4,False,False,False\n",
        encoding="utf-8",
    )
    (run_dir / "metamorphic_consistency.csv").write_text(
        "run_variant,model,family,metamorphic_group_id,metamorphic_relation,"
        "samples,scored_samples,assessable,all_correct,all_incorrect,mixed_outcomes,"
        "consistent\n"
        "variant,openai/model-a,spelling,g1,equivalent,2,2,True,False,False,True,"
        "False\n"
        "variant,openai/model-a,spelling,g2,equivalent,2,2,True,True,False,False,"
        "True\n",
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
    metamorphic_rows = list(
        csv.DictReader(paths.metamorphic_consistency.open(encoding="utf-8"))
    )
    delta_rows = list(csv.DictReader(paths.delta.open(encoding="utf-8")))

    assert comparison_rows[0]["label"] == "Model A"
    assert comparison_rows[0]["answer_correct"] == "9"
    assert comparison_rows[0]["strict_accuracy"] == "0.7"
    assert comparison_rows[0]["accuracy_ci_low"] == "0.55"
    assert comparison_rows[0]["accuracy_ci_high"] == "0.93"
    assert comparison_rows[0]["answer_accuracy_ci_low"] != ""
    assert comparison_rows[0]["strict_accuracy_ci_low"] != ""
    assert comparison_rows[0]["summary_dir"] == str(run_dir)
    assert family_rows[0]["family"] == "spelling"
    assert family_rows[0]["answer_correct"] == "9"
    assert family_rows[0]["scored_samples"] == ""
    assert family_rows[0]["tokens_per_scored_sample"] == ""
    assert metamorphic_rows[0]["family"] == "spelling"
    assert metamorphic_rows[0]["groups"] == "2"
    assert metamorphic_rows[0]["assessable_groups"] == "2"
    assert metamorphic_rows[0]["consistent_groups"] == "1"
    assert metamorphic_rows[0]["mixed_outcome_groups"] == "1"
    assert metamorphic_rows[0]["mixed_group_ids"] == "g1"
    assert delta_rows[0]["correct_delta"] == "2"
    assert delta_rows[0]["answer_correct_delta"] == "3"
    assert delta_rows[0]["strict_correct_delta"] == "1"
    assert delta_rows[0]["delta_method"] == "paired_sample"
    assert delta_rows[0]["matched_samples"] == "2"
    assert delta_rows[0]["baseline_only_samples"] == "1"
    assert delta_rows[0]["comparison_only_samples"] == "1"
    assert delta_rows[0]["paired_wins"] == "1"
    assert delta_rows[0]["paired_losses"] == "0"
    assert delta_rows[0]["paired_ties"] == "1"
    assert delta_rows[0]["paired_accuracy_delta"] == "0.5"


def test_build_comparison_infers_label_effort_and_format_only_counts(tmp_path):
    run_dir = tmp_path / "run-a"
    run_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    out_dir = tmp_path / "comparison"
    manifest.write_text(
        "label,summary_dir\nClaude Sonnet 4.6 max,run-a\n",
        encoding="utf-8",
    )
    (run_dir / "summary.csv").write_text(
        "model,barrage_profile,reasoning_effort,reasoning_summary,total_samples,"
        "scored_samples,correct,failures,answer_correct,format_correct,"
        "strict_correct,accuracy,answer_accuracy,format_accuracy,strict_accuracy,"
        "provider_errors,timeouts,total_tokens,reasoning_tokens\n"
        "anthropic/claude-sonnet-4-6,hard_obvious_8x10_seed_20260531,,,"
        "80,80,56,24,70,66,56,0.7,0.875,0.825,0.7,0,0,4132,0\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "model,family,samples,correct,failures,answer_correct,format_correct,"
        "strict_correct\n"
        "anthropic/claude-sonnet-4-6,format,80,56,24,70,66,56\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_section.csv").write_text(
        "model,family,subfamily,samples,correct,failures,answer_correct,"
        "format_correct,strict_correct\n"
        "anthropic/claude-sonnet-4-6,format,json,80,56,24,70,66,56\n",
        encoding="utf-8",
    )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(manifest=manifest, output_dir=out_dir)
    )

    comparison_rows = list(csv.DictReader(paths.comparison.open(encoding="utf-8")))
    effort_rows = list(csv.DictReader(paths.effort_curve.open(encoding="utf-8")))

    assert comparison_rows[0]["reasoning_effort"] == "max"
    assert comparison_rows[0]["answer_failures"] == "10"
    assert comparison_rows[0]["format_only_failures"] == "14"
    assert effort_rows[0]["reasoning_effort"] == "max"


def test_build_comparison_blanks_unassessable_metamorphic_rate(tmp_path):
    run_dir = tmp_path / "run-a"
    run_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    out_dir = tmp_path / "comparison"
    manifest.write_text("label,summary_dir\nModel A,run-a\n", encoding="utf-8")
    (run_dir / "summary.csv").write_text(
        "model,total_samples,scored_samples,correct,failures,accuracy,"
        "provider_errors,timeouts,total_tokens\n"
        "openai/model-a,1,1,1,0,1,0,0,100\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "model,family,samples,correct,failures\n"
        "openai/model-a,spelling,1,1,0\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_section.csv").write_text(
        "model,family,subfamily,samples,correct,failures\n"
        "openai/model-a,spelling,missing_letter,1,1,0\n",
        encoding="utf-8",
    )
    (run_dir / "metamorphic_consistency.csv").write_text(
        "run_variant,model,family,metamorphic_group_id,metamorphic_relation,"
        "samples,scored_samples,assessable,all_correct,all_incorrect,"
        "mixed_outcomes,consistent\n"
        "variant,openai/model-a,spelling,g1,equivalent,1,1,False,True,False,"
        "False,False\n",
        encoding="utf-8",
    )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(manifest=manifest, output_dir=out_dir)
    )

    [row] = list(csv.DictReader(paths.metamorphic_consistency.open(encoding="utf-8")))

    assert row["assessable_groups"] == "0"
    assert row["unassessable_groups"] == "1"
    assert row["consistency_rate"] == ""


def test_build_comparison_delta_falls_back_to_aggregate_unpaired(tmp_path):
    run_dir = tmp_path / "run-a"
    run_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    baseline = tmp_path / "baseline.csv"
    out_dir = tmp_path / "comparison"
    manifest.write_text("label,summary_dir\nModel A,run-a\n", encoding="utf-8")
    baseline.write_text(
        "label,model,correct,failures,accuracy,summary_dir\n"
        "Model A,openai/model-a,3,2,0.6,old/path/run-a\n",
        encoding="utf-8",
    )
    (run_dir / "summary.csv").write_text(
        "model,total_samples,scored_samples,correct,failures,accuracy,"
        "provider_errors,timeouts\n"
        "openai/model-a,5,5,4,1,0.8,0,0\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "model,family,samples,correct,failures\n"
        "openai/model-a,spelling,5,4,1\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_section.csv").write_text(
        "model,family,subfamily,samples,correct,failures\n"
        "openai/model-a,spelling,missing_letter,5,4,1\n",
        encoding="utf-8",
    )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(
            manifest=manifest,
            output_dir=out_dir,
            baseline_comparison=baseline,
        )
    )

    delta_rows = list(csv.DictReader(paths.delta.open(encoding="utf-8")))
    comparison_rows = list(csv.DictReader(paths.comparison.open(encoding="utf-8")))

    assert comparison_rows[0]["accuracy_ci_low"] != ""
    assert comparison_rows[0]["accuracy_ci_high"] != ""
    assert delta_rows[0]["accuracy_delta"] == "0.2"
    assert delta_rows[0]["delta_method"] == "aggregate_unpaired"
    assert delta_rows[0]["paired_accuracy_delta"] == ""


def test_build_comparison_does_not_backfill_usage_tokens_without_scored_samples(
    tmp_path,
):
    run_dir = tmp_path / "run-a"
    run_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    out_dir = tmp_path / "comparison"
    manifest.write_text("label,summary_dir\nModel A,run-a\n", encoding="utf-8")
    (run_dir / "summary.csv").write_text(
        "model,total_samples,scored_samples,correct,failures,accuracy,"
        "provider_errors,timeouts,total_tokens\n"
        "openai/model-a,2,1,1,0,1,1,0,100\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "model,family,samples,correct,failures,total_tokens\n"
        "openai/model-a,spelling,2,1,1,100\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_section.csv").write_text(
        "model,family,subfamily,samples,correct,failures,total_tokens\n"
        "openai/model-a,spelling,missing_letter,2,1,1,100\n",
        encoding="utf-8",
    )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(manifest=manifest, output_dir=out_dir)
    )

    family_rows = list(csv.DictReader(paths.family_comparison.open(encoding="utf-8")))

    assert family_rows[0]["samples"] == "2"
    assert family_rows[0]["scored_samples"] == ""
    assert family_rows[0]["tokens_per_scored_sample"] == ""


def test_build_comparison_delta_falls_back_when_sample_ids_are_disjoint(tmp_path):
    run_dir = tmp_path / "run-a"
    old_run_dir = tmp_path / "baseline-run-a"
    run_dir.mkdir()
    old_run_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    baseline = tmp_path / "baseline.csv"
    out_dir = tmp_path / "comparison"
    manifest.write_text("label,summary_dir\nModel A,run-a\n", encoding="utf-8")
    baseline.write_text(
        "label,model,correct,failures,accuracy,summary_dir\n"
        f"Model A,openai/model-a,3,2,0.6,{old_run_dir}\n",
        encoding="utf-8",
    )
    (run_dir / "summary.csv").write_text(
        "model,total_samples,scored_samples,correct,failures,accuracy,"
        "provider_errors,timeouts\n"
        "openai/model-a,5,5,4,1,0.8,0,0\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "model,family,samples,correct,failures\n"
        "openai/model-a,spelling,5,4,1\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_section.csv").write_text(
        "model,family,subfamily,samples,correct,failures\n"
        "openai/model-a,spelling,missing_letter,5,4,1\n",
        encoding="utf-8",
    )
    (old_run_dir / "usage_by_sample.csv").write_text(
        "sample_id,correct,provider_error,timeout\nold-only,True,False,False\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_sample.csv").write_text(
        "sample_id,correct,provider_error,timeout\nnew-only,False,False,False\n",
        encoding="utf-8",
    )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(
            manifest=manifest,
            output_dir=out_dir,
            baseline_comparison=baseline,
        )
    )

    delta_rows = list(csv.DictReader(paths.delta.open(encoding="utf-8")))

    assert delta_rows[0]["delta_method"] == "aggregate_unpaired"
    assert delta_rows[0]["matched_samples"] == ""
    assert delta_rows[0]["paired_accuracy_delta"] == ""


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
        "cache_write_tokens,total_tokens,estimated_cost_usd,cost_per_correct_usd,"
        "cost_source,cost_warnings\n"
        "grok/grok-4.3,1,1,1,0,1,1,1,1,1,1,1,0,0,0,"
        "1000000,1000000,1000000,1000000,1000000,5000000,0,0,runcost,"
        "missing price\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "model,family,samples,correct,failures,answer_correct,format_correct,"
        "strict_correct,input_tokens,output_tokens,reasoning_tokens,"
        "cache_read_tokens,cache_write_tokens,total_tokens,estimated_cost_usd,"
        "cost_per_correct_usd,cost_source,cost_warnings\n"
        "grok/grok-4.3,object_choice,1,1,0,1,1,1,1000000,1000000,"
        "1000000,1000000,1000000,5000000,0,0,runcost,missing price\n",
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
    family_rows = list(csv.DictReader(paths.family_comparison.open(encoding="utf-8")))

    assert comparison_rows[0]["estimated_cost_usd"] == "3.95"
    assert comparison_rows[0]["cost_per_correct_usd"] == "3.95"
    assert family_rows[0]["cost_per_correct_usd"] == "3.95"
    assert comparison_rows[0]["cost_source"] == "xai_docs_2026-05-31"
    assert comparison_rows[0]["cost_warnings"] == ""


def test_build_comparison_can_apply_openrouter_registry_costs(tmp_path):
    run_dir = tmp_path / "run-glm"
    run_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    registry = tmp_path / "model_registry_v1.yaml"
    out_dir = tmp_path / "comparison"
    manifest.write_text("label,summary_dir\nGLM,run-glm\n", encoding="utf-8")
    registry.write_text(
        "entries:\n"
        "  - label: Z.ai GLM\n"
        "    provider_route: openrouter\n"
        "    inspect_model: openrouter/z-ai/glm-4.5\n"
        "    model_id: z-ai/glm-4.5\n"
        "    input_price_per_mtok_usd: 0.6\n"
        "    output_price_per_mtok_usd: 2.2\n"
        "    pricing_source: openrouter_models_api\n",
        encoding="utf-8",
    )
    (run_dir / "summary.csv").write_text(
        "model,total_samples,scored_samples,correct,failures,answer_correct,"
        "format_correct,strict_correct,accuracy,answer_accuracy,format_accuracy,"
        "strict_accuracy,obvious_failure_rate,provider_errors,timeouts,"
        "input_tokens,output_tokens,reasoning_tokens,cache_read_tokens,"
        "cache_write_tokens,total_tokens,estimated_cost_usd,cost_source,cost_warnings\n"
        "openrouter/z-ai/glm-4.5,1,1,1,0,1,1,1,1,1,1,1,0,0,0,"
        "1000000,2000000,1500000,0,0,3000000,0.1,runcost,missing reasoning price\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "model,family,samples,correct,failures,answer_correct,format_correct,"
        "strict_correct,input_tokens,output_tokens,reasoning_tokens,total_tokens,"
        "estimated_cost_usd,cost_source,cost_warnings\n"
        "openrouter/z-ai/glm-4.5,spelling,1,1,0,1,1,1,1000000,2000000,"
        "1500000,3000000,0.1,runcost,missing reasoning price\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_section.csv").write_text(
        "model,family,subfamily,samples,correct,failures,answer_correct,"
        "format_correct,strict_correct,input_tokens,output_tokens,"
        "reasoning_tokens,total_tokens,estimated_cost_usd,cost_source,cost_warnings\n"
        "openrouter/z-ai/glm-4.5,spelling,letters,1,1,0,1,1,1,1000000,"
        "2000000,1500000,3000000,0.1,runcost,missing reasoning price\n",
        encoding="utf-8",
    )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(
            manifest=manifest,
            output_dir=out_dir,
            openrouter_price_registry=registry,
        )
    )

    comparison_rows = list(csv.DictReader(paths.comparison.open(encoding="utf-8")))
    family_rows = list(csv.DictReader(paths.family_comparison.open(encoding="utf-8")))

    assert comparison_rows[0]["estimated_cost_usd"] == "5"
    assert comparison_rows[0]["cost_source"] == (
        "openrouter_models_api_manual_reasoning_completion_fallback"
    )
    assert comparison_rows[0]["cost_warnings"] == ""
    assert comparison_rows[0]["cost_per_correct_usd"] == "5"
    assert family_rows[0]["estimated_cost_usd"] == "5"


def test_build_comparison_can_apply_direct_provider_registry_costs(tmp_path):
    run_dir = tmp_path / "run-gemini"
    run_dir.mkdir()
    manifest = tmp_path / "manifest.csv"
    registry = tmp_path / "model_registry_v1.yaml"
    out_dir = tmp_path / "comparison"
    manifest.write_text("label,summary_dir\nGemini,run-gemini\n", encoding="utf-8")
    registry.write_text(
        "entries:\n"
        "  - label: Gemini 3.5 Flash\n"
        "    provider_route: gemini\n"
        "    inspect_model: google/gemini-3.5-flash\n"
        "    model_id: gemini-3.5-flash\n"
        "    input_price_per_mtok_usd: 1.5\n"
        "    output_price_per_mtok_usd: 9\n"
        "    pricing_source: runcost_default_price_cards\n",
        encoding="utf-8",
    )
    (run_dir / "summary.csv").write_text(
        "model,total_samples,scored_samples,correct,failures,answer_correct,"
        "format_correct,strict_correct,accuracy,answer_accuracy,format_accuracy,"
        "strict_accuracy,obvious_failure_rate,provider_errors,timeouts,"
        "input_tokens,output_tokens,reasoning_tokens,cache_read_tokens,"
        "cache_write_tokens,total_tokens,estimated_cost_usd,cost_source,cost_warnings\n"
        "google/gemini-3.5-flash,1,1,1,0,1,1,1,1,1,1,1,0,0,0,"
        "1000000,2000000,1500000,0,0,4500000,0.1,runcost,missing reasoning price\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_family.csv").write_text(
        "model,family,samples,correct,failures,answer_correct,format_correct,"
        "strict_correct,input_tokens,output_tokens,reasoning_tokens,total_tokens,"
        "estimated_cost_usd,cost_source,cost_warnings\n"
        "google/gemini-3.5-flash,spelling,1,1,0,1,1,1,1000000,2000000,"
        "1500000,4500000,0.1,runcost,missing reasoning price\n",
        encoding="utf-8",
    )
    (run_dir / "usage_by_section.csv").write_text(
        "model,family,subfamily,samples,correct,failures,answer_correct,"
        "format_correct,strict_correct,input_tokens,output_tokens,"
        "reasoning_tokens,total_tokens,estimated_cost_usd,cost_source,cost_warnings\n"
        "google/gemini-3.5-flash,spelling,letters,1,1,0,1,1,1,1000000,"
        "2000000,1500000,4500000,0.1,runcost,missing reasoning price\n",
        encoding="utf-8",
    )

    paths = build_comparison_from_manifest(
        ComparisonBuildInputs(
            manifest=manifest,
            output_dir=out_dir,
            openrouter_price_registry=registry,
        )
    )

    comparison_rows = list(csv.DictReader(paths.comparison.open(encoding="utf-8")))
    family_rows = list(csv.DictReader(paths.family_comparison.open(encoding="utf-8")))

    assert comparison_rows[0]["estimated_cost_usd"] == "33"
    assert comparison_rows[0]["cost_source"] == (
        "runcost_default_price_cards_manual_reasoning_completion_fallback"
    )
    assert comparison_rows[0]["cost_warnings"] == ""
    assert family_rows[0]["estimated_cost_usd"] == "33"
