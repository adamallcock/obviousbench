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
    assert calls["benchmark_card_source"] == Path("docs/benchmark_card.md")
    assert calls["model_matrix_source"] == Path("configs/models_v0.example.yaml")
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


def test_cli_build_comparison_passes_manifest_options(monkeypatch, tmp_path, capsys):
    calls = {}

    class FakePaths:
        comparison = tmp_path / "comparison" / "comparison.csv"
        family_comparison = tmp_path / "comparison" / "family_comparison.csv"
        section_comparison = tmp_path / "comparison" / "section_comparison.csv"
        delta = tmp_path / "comparison" / "delta.csv"

    def fake_build_comparison(inputs):
        calls["manifest"] = inputs.manifest
        calls["output_dir"] = inputs.output_dir
        calls["summary_root"] = inputs.summary_root
        calls["baseline_comparison"] = inputs.baseline_comparison
        calls["manual_xai_costs"] = inputs.manual_xai_costs
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
    assert "comparison.csv" in capsys.readouterr().out
