from pathlib import Path

from obviousbench.analysis.shareable_artifacts import (
    ShareableArtifactInputs,
    build_shareable_artifacts,
)


def test_build_shareable_artifacts_promotes_card_comparison_and_gallery(tmp_path):
    comparison_dir = tmp_path / "comparison"
    comparison_dir.mkdir()
    summary_dir = tmp_path / "summaries" / "model-a"
    summary_dir.mkdir(parents=True)
    output_dir = tmp_path / "shareable"
    model_matrix = tmp_path / "models.yaml"

    (comparison_dir / "comparison.csv").write_text(
        "\n".join(
            [
                "label,model,reasoning_effort,reasoning_summary,total_samples,correct,failures,"
                "accuracy,obvious_failure_rate,input_tokens,output_tokens,reasoning_tokens,"
                "total_tokens,estimated_cost_usd,summary_dir",
                f"Model A,provider/model-a,,,10,8,2,0.8,0.2,100,20,0,120,0.001,{summary_dir}",
            ]
        ).replace("\n", "\r\n")
        + "\r\n",
        encoding="utf-8",
    )
    (comparison_dir / "family_comparison.csv").write_text(
        "\n".join(
            [
                "label,model,family,samples,correct,failures,input_tokens,output_tokens,"
                "total_tokens,estimated_cost_usd",
                "Model A,provider/model-a,character_count,5,3,2,50,10,60,0.0005",
            ]
        ).replace("\n", "\r\n")
        + "\r\n",
        encoding="utf-8",
    )
    (summary_dir / "failure_gallery.md").write_text(
        "\n".join(
            [
                "# ObviousBench Failure Gallery",
                "",
                "## Failure 1: character_count",
                "",
                "- Model: `provider/model-a`",
                "- Sample ID: `obviousbench.char_count.en.v0.public.000001`",
                "- Question: How many r's are in strawberry?",
                "- Expected answer: `3`",
                "- Extracted answer: `2`",
                "- Raw model answer: `2`",
                "- Failure type: `incorrect_count`",
                "- Human triviality: `H0`",
                "- Source type: `generated_variant`",
                "- Why humans find it obvious: Humans can count the visible letters directly.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    model_matrix.write_text(
        "comparison_panel:\n"
        "  - label: Model A\n"
        "    inspect_model: provider/model-a\n"
        "    external_note: Test comparison model.\n",
        encoding="utf-8",
    )

    paths = build_shareable_artifacts(
        ShareableArtifactInputs(
            comparison_dir=comparison_dir,
            output_dir=output_dir,
            generated_on="2026-05-31",
            benchmark_card_source=Path("docs/benchmark_card.md"),
            model_matrix_source=model_matrix,
        )
    )

    assert paths.card == output_dir / "benchmark-card.md"
    assert paths.gallery == output_dir / "failure-gallery.md"
    assert paths.comparison == output_dir / "model-comparison.csv"
    assert paths.family_comparison == output_dir / "family-comparison.csv"
    assert paths.model_matrix == output_dir / "model-matrix.yaml"
    assert paths.index == output_dir / "README.md"
    assert "\r" not in paths.comparison.read_text(encoding="utf-8")
    assert "\r" not in paths.family_comparison.read_text(encoding="utf-8")

    card = paths.card.read_text(encoding="utf-8")
    gallery = paths.gallery.read_text(encoding="utf-8")
    index = paths.index.read_text(encoding="utf-8")

    assert "80.0% accuracy" in card
    assert "20.0% obvious failure rate" in card
    assert "character_count: 2 failures" in card
    assert "type: reference" not in card
    assert "How many r's are in strawberry?" in gallery
    assert "generated_variant" in gallery
    assert "provider/model-a" in paths.model_matrix.read_text(encoding="utf-8")
    assert "Raw Inspect logs are intentionally not included" in index
