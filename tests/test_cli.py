import json
from pathlib import Path

from obviousbench.cli import main
from obviousbench.datasets.schemas import FAMILY_SHORT_NAMES
from tests.datasets.test_schemas import valid_record


def test_cli_validate_success(tmp_path, capsys):
    path = tmp_path / "items.jsonl"
    path.write_text(json.dumps(valid_record()) + "\n", encoding="utf-8")

    exit_code = main(["validate", str(path)])

    assert exit_code == 0
    assert "Validation passed." in capsys.readouterr().out


def test_cli_validate_failure(tmp_path, capsys):
    path = tmp_path / "items.jsonl"
    path.write_text("{}\n", encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "validation_error" in captured.err


def test_cli_validate_passes_item_card_flags(tmp_path, capsys):
    path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    cards_dir.mkdir()
    path.write_text(json.dumps(valid_record()) + "\n", encoding="utf-8")

    exit_code = main(
        [
            "validate",
            str(path),
            "--item-cards-dir",
            str(cards_dir),
            "--allow-extra-item-cards",
        ]
    )

    assert exit_code == 0
    assert "Validation passed." in capsys.readouterr().out


def test_cli_validate_can_require_item_cards(tmp_path, capsys):
    path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    cards_dir.mkdir()
    path.write_text(json.dumps(valid_record()) + "\n", encoding="utf-8")

    exit_code = main(
        [
            "validate",
            str(path),
            "--item-cards-dir",
            str(cards_dir),
            "--require-item-cards",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "missing_item_card" in captured.err


def test_cli_validate_require_item_cards_requires_cards_dir(tmp_path, capsys):
    path = tmp_path / "items.jsonl"
    path.write_text(json.dumps(valid_record()) + "\n", encoding="utf-8")

    exit_code = main(["validate", str(path), "--require-item-cards"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "missing_item_cards_dir" in captured.err


def _barrage_record(family: str, index: int) -> dict:
    family_short = FAMILY_SHORT_NAMES[family]
    return valid_record(
        id=f"obviousbench.{family_short}.en.v0.public.{index:06d}",
        family=family,
        subfamily="one",
        source_type="generated_variant",
        source_refs=[f"src_{family}"],
    )


def test_cli_make_barrage_writes_materialized_profile(tmp_path, capsys):
    split_dir = tmp_path / "public_v0"
    split_dir.mkdir()
    for offset, family in enumerate(["character_count", "word_count"]):
        rows = [_barrage_record(family, offset * 10 + index) for index in range(1, 4)]
        (split_dir / f"{family}.jsonl").write_text(
            "\n".join(json.dumps(row) for row in rows) + "\n",
            encoding="utf-8",
        )
    out = tmp_path / "barrage.jsonl"

    exit_code = main(
        [
            "make-barrage",
            "--profile",
            "balanced_2x2",
            "--data-dir",
            str(tmp_path),
            "--out",
            str(out),
            "--seed",
            "7",
        ]
    )

    assert exit_code == 0
    assert len(out.read_text(encoding="utf-8").splitlines()) == 4
    assert "Wrote 4 barrage samples" in capsys.readouterr().out


def test_cli_make_barrage_passes_metamorphic_sibling_cap(monkeypatch, tmp_path):
    calls = {}
    out = tmp_path / "barrage.jsonl"

    def fake_load_split_items(split, data_dir=None):
        calls["split"] = split
        calls["data_dir"] = data_dir
        return []

    def fake_build_barrage(items, profile, *, seed, max_metamorphic_siblings_per_group):
        calls["profile"] = profile
        calls["seed"] = seed
        calls["max_metamorphic_siblings_per_group"] = (
            max_metamorphic_siblings_per_group
        )
        return []

    def fake_write_barrage_jsonl(items, path):
        calls["out"] = path
        path.write_text("", encoding="utf-8")
        return path

    monkeypatch.setattr("obviousbench.cli.load_split_items", fake_load_split_items)
    monkeypatch.setattr("obviousbench.cli.build_barrage", fake_build_barrage)
    monkeypatch.setattr("obviousbench.cli.write_barrage_jsonl", fake_write_barrage_jsonl)

    exit_code = main(
        [
            "make-barrage",
            "--profile",
            "balanced_2x2",
            "--data-dir",
            str(tmp_path),
            "--out",
            str(out),
            "--seed",
            "7",
            "--max-metamorphic-siblings-per-group",
            "3",
        ]
    )

    assert exit_code == 0
    assert calls["max_metamorphic_siblings_per_group"] == 3


def test_cli_make_barrage_defaults_metamorphic_sibling_cap(monkeypatch, tmp_path):
    calls = {}
    out = tmp_path / "barrage.jsonl"

    monkeypatch.setattr("obviousbench.cli.load_split_items", lambda split, data_dir=None: [])

    def fake_build_barrage(items, profile, *, seed, max_metamorphic_siblings_per_group):
        calls["max_metamorphic_siblings_per_group"] = (
            max_metamorphic_siblings_per_group
        )
        return []

    monkeypatch.setattr("obviousbench.cli.build_barrage", fake_build_barrage)
    monkeypatch.setattr(
        "obviousbench.cli.write_barrage_jsonl",
        lambda items, path: path,
    )

    exit_code = main(
        [
            "make-barrage",
            "--profile",
            "balanced_2x2",
            "--data-dir",
            str(tmp_path),
            "--out",
            str(out),
        ]
    )

    assert exit_code == 0
    assert calls["max_metamorphic_siblings_per_group"] == 1


def test_cli_estimate_cost_prints_dry_run_estimate(monkeypatch, tmp_path, capsys):
    calls = {}

    class FakeEstimate:
        model = "openai/gpt-5-nano"
        profile = "balanced_2x1"
        seed = 7
        total_samples = 2
        cache_hits = 1
        billable_samples = 1
        estimated_billable_cost_usd = 0.000123
        estimated_cached_cost_avoided_usd = 0.000045
        usage_source = "historical_sample"
        pricing_source = "runcost"
        warnings = ()
        rows = ()

    def fake_estimate(inputs):
        calls["inputs"] = inputs
        return FakeEstimate()

    monkeypatch.setattr("obviousbench.cli.estimate_benchmark_cost", fake_estimate)

    exit_code = main(
        [
            "estimate-cost",
            "--model",
            "openai/gpt-5-nano",
            "--profile",
            "balanced_2x1",
            "--seed",
            "7",
            "--summary-root",
            str(tmp_path / "summaries"),
            "--cache-dir",
            str(tmp_path / "cache"),
            "--setting",
            "reasoning_effort=low",
        ]
    )

    assert exit_code == 0
    assert calls["inputs"].model == "openai/gpt-5-nano"
    assert calls["inputs"].settings == {"reasoning_effort": "low"}
    captured = capsys.readouterr().out
    assert "Dry-run cost estimate" in captured
    assert "billable samples: 1/2" in captured
    assert "$0.000123" in captured


def test_cli_summarize_accepts_cost_none(monkeypatch, tmp_path, capsys):
    def fake_summarize(logs, out, cost_mode="none", rescore=False):
        assert cost_mode == "none"
        assert not rescore
        out.mkdir()
        return out / "summary.csv", out / "failure_gallery.md"

    monkeypatch.setattr("obviousbench.cli.summarize_results", fake_summarize)

    exit_code = main(
        [
            "summarize",
            "--logs",
            "results/raw/example",
            "--out",
            str(tmp_path / "summary"),
            "--cost",
            "none",
        ]
    )

    assert exit_code == 0
    assert "summary.csv" in capsys.readouterr().out


def test_cli_summarize_defaults_to_runcost(monkeypatch, tmp_path):
    def fake_summarize(logs, out, cost_mode="none", rescore=False):
        assert cost_mode == "runcost"
        assert not rescore
        out.mkdir()
        return out / "summary.csv", out / "failure_gallery.md", out / "cost_ledger.json"

    monkeypatch.setattr("obviousbench.cli.summarize_results", fake_summarize)

    exit_code = main(
        [
            "summarize",
            "--logs",
            "results/raw/example",
            "--out",
            str(tmp_path / "summary"),
        ]
    )

    assert exit_code == 0


def test_cli_rescore_uses_current_scorers(monkeypatch, tmp_path):
    def fake_summarize(logs, out, cost_mode="none", rescore=False):
        assert cost_mode == "runcost"
        assert rescore
        out.mkdir()
        return out / "summary.csv", out / "failure_gallery.md", out / "cost_ledger.json"

    monkeypatch.setattr("obviousbench.cli.summarize_results", fake_summarize)

    exit_code = main(
        [
            "rescore",
            "--logs",
            "results/raw/example",
            "--out",
            str(tmp_path / "summary"),
        ]
    )

    assert exit_code == 0


def test_cli_build_shareable_passes_paths(monkeypatch, tmp_path, capsys):
    calls = {}

    class FakePaths:
        card = tmp_path / "shareable" / "benchmark-card.md"
        gallery = tmp_path / "shareable" / "failure-gallery.md"
        comparison = tmp_path / "shareable" / "model-comparison.csv"
        family_comparison = tmp_path / "shareable" / "family-comparison.csv"
        model_matrix = tmp_path / "shareable" / "model-matrix.yaml"
        index = tmp_path / "shareable" / "README.md"

    def fake_build_shareable(inputs):
        calls["comparison_dir"] = inputs.comparison_dir
        calls["output_dir"] = inputs.output_dir
        calls["generated_on"] = inputs.generated_on
        calls["benchmark_card_source"] = inputs.benchmark_card_source
        calls["model_matrix_source"] = inputs.model_matrix_source
        return FakePaths()

    monkeypatch.setattr("obviousbench.cli.build_shareable_artifacts", fake_build_shareable)

    exit_code = main(
        [
            "build-shareable",
            "--comparison-dir",
            "results/summaries/comparison",
            "--out",
            str(tmp_path / "shareable"),
            "--generated-on",
            "2026-05-31",
        ]
    )

    assert exit_code == 0
    assert calls["comparison_dir"].as_posix() == "results/summaries/comparison"
    assert calls["output_dir"] == tmp_path / "shareable"
    assert calls["generated_on"] == "2026-05-31"
    assert calls["benchmark_card_source"] == Path("docs/reference/benchmark-card.md")
    assert calls["model_matrix_source"] == Path("configs/model_panels/models_v0.example.yaml")
    assert "benchmark-card.md" in capsys.readouterr().out


def test_cli_build_report_passes_paths(monkeypatch, tmp_path, capsys):
    calls = {}

    class FakePaths:
        html = tmp_path / "report" / "report.html"
        leaderboard_csv = tmp_path / "report" / "leaderboard.csv"
        leaderboard_md = tmp_path / "report" / "leaderboard.md"
        family_heatmap_csv = tmp_path / "report" / "family-heatmap.csv"

    def fake_build_report(inputs):
        calls["comparison_dir"] = inputs.comparison_dir
        calls["output_dir"] = inputs.output_dir
        calls["generated_on"] = inputs.generated_on
        calls["title"] = inputs.title
        return FakePaths()

    monkeypatch.setattr("obviousbench.cli.build_benchmark_report", fake_build_report)

    exit_code = main(
        [
            "build-report",
            "--comparison-dir",
            "results/summaries/comparison",
            "--out",
            str(tmp_path / "report"),
            "--generated-on",
            "2026-05-31",
            "--title",
            "Expanded Sweep",
        ]
    )

    assert exit_code == 0
    assert calls["comparison_dir"].as_posix() == "results/summaries/comparison"
    assert calls["output_dir"] == tmp_path / "report"
    assert calls["generated_on"] == "2026-05-31"
    assert calls["title"] == "Expanded Sweep"
    assert "report.html" in capsys.readouterr().out


def test_cli_build_site_passes_paths(monkeypatch, tmp_path, capsys):
    calls = {}

    class FakePaths:
        index = tmp_path / "site" / "index.html"
        leaderboard_csv = tmp_path / "site" / "leaderboard.csv"
        family_heatmap_csv = tmp_path / "site" / "family-heatmap.csv"
        data_json = tmp_path / "site" / "site-data.json"

    def fake_build_site(inputs):
        calls["comparison_dir"] = inputs.comparison_dir
        calls["output_dir"] = inputs.output_dir
        calls["generated_on"] = inputs.generated_on
        calls["title"] = inputs.title
        calls["report_href"] = inputs.report_href
        return FakePaths()

    monkeypatch.setattr("obviousbench.cli.build_benchmark_site", fake_build_site)

    exit_code = main(
        [
            "build-site",
            "--comparison-dir",
            "results/summaries/comparison",
            "--out",
            str(tmp_path / "site"),
            "--generated-on",
            "2026-06-14",
            "--title",
            "ObviousBench v0.1",
            "--report-href",
            "../archive/reports/report.html",
        ]
    )

    assert exit_code == 0
    assert calls["comparison_dir"].as_posix() == "results/summaries/comparison"
    assert calls["output_dir"] == tmp_path / "site"
    assert calls["generated_on"] == "2026-06-14"
    assert calls["title"] == "ObviousBench v0.1"
    assert calls["report_href"] == "../archive/reports/report.html"
    assert "index.html" in capsys.readouterr().out


def test_cli_build_comparison_passes_manifest_options(monkeypatch, tmp_path, capsys):
    calls = {}

    class FakePaths:
        comparison = tmp_path / "comparison" / "comparison.csv"
        family_comparison = tmp_path / "comparison" / "family_comparison.csv"
        section_comparison = tmp_path / "comparison" / "section_comparison.csv"
        effort_curve = tmp_path / "comparison" / "effort_curve.csv"
        metamorphic_consistency = tmp_path / "comparison" / "metamorphic_consistency.csv"
        delta = tmp_path / "comparison" / "delta.csv"

    def fake_build_comparison(inputs):
        calls["manifest"] = inputs.manifest
        calls["output_dir"] = inputs.output_dir
        calls["summary_root"] = inputs.summary_root
        calls["baseline_comparison"] = inputs.baseline_comparison
        calls["manual_xai_costs"] = inputs.manual_xai_costs
        calls["openrouter_price_registry"] = inputs.openrouter_price_registry
        return FakePaths()

    monkeypatch.setattr(
        "obviousbench.cli.build_comparison_from_manifest",
        fake_build_comparison,
    )

    exit_code = main(
        [
            "build-comparison",
            "--manifest",
            "results/summaries/original/comparison.csv",
            "--summary-root",
            "results/summaries/rescored",
            "--baseline-comparison",
            "results/summaries/original/comparison.csv",
            "--manual-xai-costs",
            "--openrouter-price-registry",
            "configs/registries/model_registry_v1.yaml",
            "--out",
            str(tmp_path / "comparison"),
        ]
    )

    assert exit_code == 0
    assert calls["manifest"].as_posix() == "results/summaries/original/comparison.csv"
    assert calls["summary_root"].as_posix() == "results/summaries/rescored"
    assert calls["baseline_comparison"].as_posix() == (
        "results/summaries/original/comparison.csv"
    )
    assert calls["manual_xai_costs"]
    assert (
        calls["openrouter_price_registry"].as_posix()
        == "configs/registries/model_registry_v1.yaml"
    )
    assert "comparison.csv" in capsys.readouterr().out
