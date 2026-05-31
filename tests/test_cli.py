import json

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
    def fake_summarize(logs, out, cost_mode="none"):
        assert cost_mode == "none"
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
    def fake_summarize(logs, out, cost_mode="none"):
        assert cost_mode == "runcost"
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
