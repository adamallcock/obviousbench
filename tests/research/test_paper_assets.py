from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

from obviousbench.research import paper_assets as paper_assets_module
from obviousbench.research.paper_assets import PaperAssetInputs, build_paper_assets
from tests.datasets.test_schemas import valid_record
from tests.research.test_arxiv_readiness import _write_card, _write_gold


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def _hex_to_rgb(value: str) -> tuple[float, float, float]:
    return (
        int(value[1:3], 16) / 255,
        int(value[3:5], 16) / 255,
        int(value[5:7], 16) / 255,
    )


def test_paper_figure_colors_read_release_theme():
    theme = yaml.safe_load(Path("configs/release_theme_v0_1_0.yaml").read_text())

    assert _hex_to_rgb(theme["colors"]["accent"]) == paper_assets_module.COLOR_BLUE
    assert _hex_to_rgb(theme["colors"]["accent_warm"]) == paper_assets_module.COLOR_ORANGE
    assert _hex_to_rgb(theme["colors"]["grid"]) == paper_assets_module.COLOR_GRID


def test_build_paper_assets_writes_dataset_gold_and_readiness_tables(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    output_dir = tmp_path / "paper" / "tables"
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(
        (
            '{"item_id":"obviousbench.char_count.en.v0.public.000001",'
            '"family":"character_count","subfamily":"single_letter_count",'
            '"scorer":"exact_integer_extract_first_v0"}\n'
        ),
        encoding="utf-8",
    )
    _write_card(cards_dir)
    _write_gold(gold_dir, count=2)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        ),
        encoding="utf-8",
    )

    outputs = build_paper_assets(
        PaperAssetInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=human_baseline,
            output_dir=output_dir,
            min_gold_examples_per_scorer=2,
        )
    )

    assert outputs.dataset_composition.exists()
    assert outputs.scorer_gold_coverage.exists()
    assert outputs.readiness_gates.exists()
    assert outputs.human_baseline_summary.exists()
    dataset_text = outputs.dataset_composition.read_text(encoding="utf-8")
    assert "Char count" in dataset_text
    assert "Single-letter count" in dataset_text
    assert "exact\\_integer\\_extract\\_first\\_v0" in outputs.scorer_gold_coverage.read_text(
        encoding="utf-8"
    )
    assert "PASS" in outputs.readiness_gates.read_text(encoding="utf-8")
    human_text = outputs.human_baseline_summary.read_text(encoding="utf-8")
    assert "character\\_count" in human_text
    assert "Participants" in human_text
    assert "100.0\\%" in human_text
    assert "2.40" in human_text


def test_build_paper_assets_writes_model_panel_table(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    output_dir = tmp_path / "paper" / "tables"
    model_panel = tmp_path / "paper_v1_model_panel.yaml"
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(
        (
            '{"item_id":"obviousbench.char_count.en.v0.public.000001",'
            '"family":"character_count","subfamily":"single_letter_count",'
            '"scorer":"exact_integer_extract_first_v0"}\n'
        ),
        encoding="utf-8",
    )
    _write_card(cards_dir)
    _write_gold(gold_dir, count=2)
    model_panel.write_text(
        yaml.safe_dump(
            {
                "schema_version": "paper-model-panel-v1",
                "entries": [
                    {
                        "id": "unit-openai-gpt-4-1",
                        "label": "GPT-4.1",
                        "provider_route": "openai",
                        "inspect_model": "openai/gpt-4.1",
                        "role": "direct frontier baseline",
                        "temperature": 0,
                        "max_tokens": 64,
                        "pricing_source": "runcost_default_price_cards",
                        "run_status": "planned",
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    outputs = build_paper_assets(
        PaperAssetInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=None,
            output_dir=output_dir,
            model_panel_path=model_panel,
            min_gold_examples_per_scorer=2,
        )
    )

    assert outputs.model_panel is not None
    text = outputs.model_panel.read_text(encoding="utf-8")
    assert "GPT-4.1" in text
    assert "openai/gpt-4.1" in text
    assert "planned" in text


def test_build_paper_assets_writes_compact_model_manifest_summary_table(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    output_dir = tmp_path / "paper" / "tables"
    model_manifest = tmp_path / "release_manifest.csv"
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(
        (
            '{"item_id":"obviousbench.char_count.en.v0.public.000001",'
            '"family":"character_count","subfamily":"single_letter_count",'
            '"scorer":"exact_integer_extract_first_v0"}\n'
        ),
        encoding="utf-8",
    )
    _write_card(cards_dir)
    _write_gold(gold_dir, count=2)
    model_manifest.write_text(
        (
            "label,model,summary_dir\n"
            "OpenAI Unit,openai/unit,tmp/openai\n"
            "OpenRouter Unit,openrouter/unit,tmp/openrouter\n"
        ),
        encoding="utf-8",
    )

    outputs = build_paper_assets(
        PaperAssetInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=None,
            output_dir=output_dir,
            model_panel_path=model_manifest,
            min_gold_examples_per_scorer=2,
        )
    )

    assert outputs.model_panel is not None
    text = outputs.model_panel.read_text(encoding="utf-8")
    assert "OpenAI direct" in text
    assert "OpenRouter" in text
    assert "\\path{" not in text


def test_build_paper_assets_writes_final_result_tables_from_comparison_dir(
    tmp_path: Path,
):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    output_dir = tmp_path / "paper" / "tables"
    figures_dir = tmp_path / "paper" / "figures"
    final_results_dir = tmp_path / "final-results"
    final_results_dir.mkdir()
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(
        (
            '{"item_id":"obviousbench.char_count.en.v0.public.000001",'
            '"family":"character_count","subfamily":"single_letter_count",'
            '"scorer":"exact_integer_extract_first_v0"}\n'
        ),
        encoding="utf-8",
    )
    _write_card(cards_dir)
    _write_gold(gold_dir, count=2)
    (final_results_dir / "comparison.csv").write_text(
        (
            "label,model,scored_samples,answer_accuracy,format_accuracy,"
            "strict_accuracy,provider_errors,timeouts,estimated_cost_usd\n"
            "Unit Model,provider/unit,80,0.875,1.0,0.875,1,0,0.0123\n"
            "Loose Correct Model,provider/loose,80,1.0,0.5,0.5,0,0,0.0100\n"
        ),
        encoding="utf-8",
    )
    (final_results_dir / "family_comparison.csv").write_text(
        (
            "label,model,family,samples,answer_correct,format_correct,"
            "strict_correct,estimated_cost_usd\n"
            "Unit Model,provider/unit,character_count,10,8,10,8,0.001\n"
            "Loose Correct Model,provider/loose,character_count,10,10,5,5,0.001\n"
        ),
        encoding="utf-8",
    )

    outputs = build_paper_assets(
        PaperAssetInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=None,
            output_dir=output_dir,
            figures_dir=figures_dir,
            final_results_dir=final_results_dir,
            min_gold_examples_per_scorer=2,
        )
    )

    assert "Unit Model" in outputs.main_results.read_text(encoding="utf-8")
    main_text = outputs.main_results.read_text(encoding="utf-8")
    assert "87.5\\%" in main_text
    assert "Ans. correct" in main_text
    assert "95\\% CI" in main_text
    assert "Fail" not in main_text
    assert "--" in main_text
    assert main_text.index("Loose Correct Model") < main_text.index("Unit Model")
    assert "0.0\\%" in main_text
    assert "Char count" in outputs.family_results.read_text(encoding="utf-8")
    assert "provider/unit" in outputs.provider_exclusions.read_text(encoding="utf-8")
    for figure_path in outputs.figures:
        assert figure_path.read_bytes().startswith(b"%PDF-")


def test_build_paper_assets_uses_placeholder_results_when_final_missing(
    tmp_path: Path,
):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    output_dir = tmp_path / "paper" / "tables"
    figures_dir = tmp_path / "paper" / "figures"
    placeholder_results_dir = tmp_path / "proof-point"
    placeholder_results_dir.mkdir()
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(
        (
            '{"item_id":"obviousbench.char_count.en.v0.public.000001",'
            '"family":"character_count","subfamily":"single_letter_count",'
            '"scorer":"exact_integer_extract_first_v0"}\n'
        ),
        encoding="utf-8",
    )
    _write_card(cards_dir)
    _write_gold(gold_dir, count=2)
    (placeholder_results_dir / "model-comparison.csv").write_text(
        (
            "label,model,total_samples,scored_samples,answer_accuracy,"
            "format_accuracy,strict_accuracy,estimated_cost_usd,reasoning_tokens\n"
            "Draft Model,provider/draft,80,80,0.925,1.0,0.900,0.045,0\n"
            "Gap Model,provider/gap,80,80,0.850,0.700,0.550,0.010,0\n"
            "Gemini 3.5 Flash OR,openrouter/google/gemini-3.5-flash,"
            "80,80,1.0,1.0,1.0,0.149,1200\n"
        ),
        encoding="utf-8",
    )
    (placeholder_results_dir / "family-comparison.csv").write_text(
        (
            "label,model,family,samples,answer_correct,format_correct,"
            "strict_correct,estimated_cost_usd\n"
            "Draft Model,provider/draft,character_count,10,9,10,9,0.005\n"
            "Gap Model,provider/gap,character_count,10,8,7,5,0.004\n"
            "Gemini 3.5 Flash OR,openrouter/google/gemini-3.5-flash,"
            "character_count,10,10,10,10,0.018\n"
        ),
        encoding="utf-8",
    )

    outputs = build_paper_assets(
        PaperAssetInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=None,
            output_dir=output_dir,
            figures_dir=figures_dir,
            final_results_dir=None,
            placeholder_results_dir=placeholder_results_dir,
            min_gold_examples_per_scorer=2,
        )
    )

    main_text = outputs.main_results.read_text(encoding="utf-8")
    assert "Draft Model" in main_text
    assert "Gemini 3.5 Flash OR auto" in main_text
    assert "Ans. correct" in main_text
    assert "95\\% CI" in main_text
    assert "Draft-only placeholder" in main_text
    assert "90.0\\%" in main_text
    assert "Char count" in outputs.family_results.read_text(encoding="utf-8")
    assert "Auto/observed thinking" in outputs.thinking_group_results.read_text(
        encoding="utf-8"
    )
    assert "Google Gemini" in outputs.model_family_results.read_text(encoding="utf-8")
    assert "Strict misses" in outputs.failure_type_summary.read_text(encoding="utf-8")
    for figure_path in outputs.figures:
        data = figure_path.read_bytes()
        assert data.startswith(b"%PDF-")
        assert len(data) > 1000


def test_build_paper_assets_writes_explicit_placeholders_without_final_results(
    tmp_path: Path,
):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    output_dir = tmp_path / "paper" / "tables"
    figures_dir = tmp_path / "paper" / "figures"
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(
        (
            '{"item_id":"obviousbench.char_count.en.v0.public.000001",'
            '"family":"character_count","subfamily":"single_letter_count",'
            '"scorer":"exact_integer_extract_first_v0"}\n'
        ),
        encoding="utf-8",
    )
    _write_card(cards_dir)
    _write_gold(gold_dir, count=2)

    outputs = build_paper_assets(
        PaperAssetInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=None,
            output_dir=output_dir,
            figures_dir=figures_dir,
            final_results_dir=None,
            min_gold_examples_per_scorer=2,
        )
    )

    assert "No final paper sweep has been run" in outputs.main_results.read_text(
        encoding="utf-8"
    )
    assert "No final family results available yet" in outputs.family_results.read_text(
        encoding="utf-8"
    )
    assert len(outputs.figures) == 4


def test_build_paper_assets_escapes_latex_sensitive_manifest_values(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    output_dir = tmp_path / "paper" / "tables"
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(
        (
            '{"item_id":"obviousbench.char_count.en.v0.public.000001",'
            '"family":"format_compliance","subfamily":"json_field",'
            '"scorer":"exact_integer_extract_first_v0",'
            '"selection_rationale":"cost & format % check"}\n'
        ),
        encoding="utf-8",
    )
    _write_card(cards_dir)
    _write_gold(gold_dir, count=2)

    outputs = build_paper_assets(
        PaperAssetInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=None,
            output_dir=output_dir,
            min_gold_examples_per_scorer=2,
        )
    )

    text = outputs.dataset_composition.read_text(encoding="utf-8")
    assert "Format" in text
    assert "JSON field" in text
    assert "\\%" not in text
    assert outputs.human_baseline_summary.exists()
    human_summary = outputs.human_baseline_summary.read_text(encoding="utf-8")
    assert "Measured human baseline deferred for fast preprint" in human_summary


def test_build_paper_assets_script_writes_default_tables(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    output_dir = tmp_path / "paper" / "tables"
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(
        (
            '{"item_id":"obviousbench.char_count.en.v0.public.000001",'
            '"family":"character_count","subfamily":"single_letter_count",'
            '"scorer":"exact_integer_extract_first_v0"}\n'
        ),
        encoding="utf-8",
    )
    _write_card(cards_dir)
    _write_gold(gold_dir, count=2)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_paper_assets.py",
            "--manifest",
            str(manifest_path),
            "--dataset",
            str(dataset_path),
            "--item-cards-dir",
            str(cards_dir),
            "--scorer-gold-dir",
            str(gold_dir),
            "--human-baseline",
            str(human_baseline),
            "--out",
            str(output_dir),
            "--min-gold-examples-per-scorer",
            "2",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "dataset_composition.tex" in result.stdout
    assert "human_baseline_summary.tex" in result.stdout
    assert (output_dir / "dataset_composition.tex").exists()
