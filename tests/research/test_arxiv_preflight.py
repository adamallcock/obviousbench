from __future__ import annotations

import subprocess
import sys
import tarfile
from pathlib import Path

from obviousbench.research.arxiv_metadata import (
    ArxivMetadataInputs,
    build_submission_metadata_template,
)
from obviousbench.research.arxiv_preflight import (
    ArxivPreflightInputs,
    build_arxiv_preflight,
)
from tests.datasets.test_schemas import valid_record
from tests.research.test_arxiv_readiness import (
    _write_card,
    _write_gold,
    _write_jsonl,
)


def _write_tar(path: Path, root: Path, names: list[str]) -> None:
    with tarfile.open(path, "w:gz") as archive:
        for name in names:
            file_path = root / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("content\n", encoding="utf-8")
            archive.add(file_path, arcname=name)


def _write_preflight_fixture(tmp_path: Path) -> dict[str, Path]:
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    paper_dir = tmp_path / "paper"
    bundle = paper_dir / "arxiv-src.tar.gz"
    model_panel = tmp_path / "paper_v1_model_panel.yaml"
    model_costs = tmp_path / "model-costs.md"

    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir)
    _write_gold(gold_dir)
    human_baseline.write_text(
        "item_id,participant_id,answer,seconds,correct,notes\n",
        encoding="utf-8",
    )
    paper_manifest.write_text(
        '{"item_id":"obviousbench.char_count.en.v0.public.000001"}\n',
        encoding="utf-8",
    )
    paper_dir.mkdir()
    paper_dir.joinpath("main.tex").write_text(
        "\\title{ObviousBench}\n\\claimblocked{final results missing}\n",
        encoding="utf-8",
    )
    paper_dir.joinpath("references.bib").write_text("@misc{unit}\n", encoding="utf-8")
    _write_tar(
        bundle,
        tmp_path / "bundle-src",
        [
            "main.tex",
            "references.bib",
            "sections/01_introduction.tex",
        ],
    )
    model_panel.write_text("schema_version: paper-model-panel-v1\nentries: []\n")
    model_costs.write_text("# Model costs\n", encoding="utf-8")

    return {
        "dataset_path": dataset_path,
        "cards_dir": cards_dir,
        "gold_dir": gold_dir,
        "human_baseline": human_baseline,
        "paper_manifest": paper_manifest,
        "paper_dir": paper_dir,
        "bundle": bundle,
        "model_panel": model_panel,
        "model_costs": model_costs,
    }


def test_build_arxiv_preflight_writes_blocked_checklist_with_passed_bundle(
    tmp_path: Path,
):
    fixture = _write_preflight_fixture(tmp_path)
    output_path = tmp_path / "submission-checklist.md"

    result = build_arxiv_preflight(
        ArxivPreflightInputs(
            dataset_paths=[fixture["dataset_path"]],
            item_cards_dir=fixture["cards_dir"],
            scorer_gold_dir=fixture["gold_dir"],
            human_baseline_path=fixture["human_baseline"],
            paper_manifest_path=fixture["paper_manifest"],
            paper_dir=fixture["paper_dir"],
            bundle_path=fixture["bundle"],
            output_path=output_path,
            claim_audit_output_path=tmp_path / "claim-audit.md",
            bundle_audit_output_path=tmp_path / "bundle-audit.md",
            model_panel_path=fixture["model_panel"],
            model_costs_path=fixture["model_costs"],
            metadata_confirmation_path=tmp_path / "metadata.md",
            available_latex_tools=("unittex",),
            min_gold_examples_per_scorer=2,
            min_human_participants=1,
        )
    )

    assert not result.ok
    assert result.check_by_name("source bundle audit").status == "pass"
    assert result.check_by_name("human baseline").status == "pass"
    assert result.check_by_name("paper claim blockers").status == "fail"
    assert result.check_by_name("submission metadata confirmation").status == "fail"
    assert result.check_by_name("PDF build artifact").status == "fail"

    text = output_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "| human baseline | PASS |" in text
    assert "| source bundle audit | PASS |" in text


def test_preflight_strict_profile_blocks_missing_human_rows(tmp_path: Path):
    fixture = _write_preflight_fixture(tmp_path)
    output_path = tmp_path / "submission-checklist.md"

    result = build_arxiv_preflight(
        ArxivPreflightInputs(
            dataset_paths=[fixture["dataset_path"]],
            item_cards_dir=fixture["cards_dir"],
            scorer_gold_dir=fixture["gold_dir"],
            human_baseline_path=fixture["human_baseline"],
            paper_manifest_path=fixture["paper_manifest"],
            paper_dir=fixture["paper_dir"],
            bundle_path=fixture["bundle"],
            output_path=output_path,
            claim_audit_output_path=tmp_path / "claim-audit.md",
            bundle_audit_output_path=tmp_path / "bundle-audit.md",
            model_panel_path=fixture["model_panel"],
            model_costs_path=fixture["model_costs"],
            metadata_confirmation_path=tmp_path / "metadata.md",
            available_latex_tools=("unittex",),
            min_gold_examples_per_scorer=2,
            min_human_participants=1,
            readiness_profile="strict",
        )
    )

    assert not result.ok
    assert result.check_by_name("human baseline").status == "fail"
    assert "| human baseline | FAIL |" in output_path.read_text(encoding="utf-8")


def test_build_arxiv_submission_checklist_script_writes_report(tmp_path: Path):
    fixture = _write_preflight_fixture(tmp_path)
    output_path = tmp_path / "submission-checklist.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_arxiv_submission_checklist.py",
            "--dataset",
            str(fixture["dataset_path"]),
            "--item-cards-dir",
            str(fixture["cards_dir"]),
            "--scorer-gold-dir",
            str(fixture["gold_dir"]),
            "--human-baseline",
            str(fixture["human_baseline"]),
            "--paper-manifest",
            str(fixture["paper_manifest"]),
            "--paper-dir",
            str(fixture["paper_dir"]),
            "--bundle",
            str(fixture["bundle"]),
            "--model-panel",
            str(fixture["model_panel"]),
            "--model-costs",
            str(fixture["model_costs"]),
            "--metadata-confirmation",
            str(tmp_path / "metadata.md"),
            "--out",
            str(output_path),
            "--claim-audit-out",
            str(tmp_path / "claim-audit.md"),
            "--bundle-audit-out",
            str(tmp_path / "bundle-audit.md"),
            "--min-gold-examples-per-scorer",
            "2",
            "--min-human-participants",
            "1",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Wrote arXiv submission checklist" in result.stdout
    assert "Overall status: BLOCKED" in output_path.read_text(encoding="utf-8")


def test_preflight_keeps_draft_metadata_blocked(tmp_path: Path):
    fixture = _write_preflight_fixture(tmp_path)
    metadata_path = tmp_path / "metadata.md"
    output_path = tmp_path / "submission-checklist.md"
    build_submission_metadata_template(ArxivMetadataInputs(output_path=metadata_path))

    result = build_arxiv_preflight(
        ArxivPreflightInputs(
            dataset_paths=[fixture["dataset_path"]],
            item_cards_dir=fixture["cards_dir"],
            scorer_gold_dir=fixture["gold_dir"],
            human_baseline_path=fixture["human_baseline"],
            paper_manifest_path=fixture["paper_manifest"],
            paper_dir=fixture["paper_dir"],
            bundle_path=fixture["bundle"],
            output_path=output_path,
            claim_audit_output_path=tmp_path / "claim-audit.md",
            bundle_audit_output_path=tmp_path / "bundle-audit.md",
            model_panel_path=fixture["model_panel"],
            model_costs_path=fixture["model_costs"],
            metadata_confirmation_path=metadata_path,
            available_latex_tools=("unittex",),
            min_gold_examples_per_scorer=2,
            min_human_participants=1,
        )
    )

    metadata_check = result.check_by_name("submission metadata confirmation")
    assert metadata_check.status == "fail"
    assert "metadata_status must be confirmed" in metadata_check.evidence
