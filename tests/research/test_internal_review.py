from __future__ import annotations

import json
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Literal

from obviousbench.research.internal_review import (
    InternalReviewInputs,
    audit_internal_research_review,
)
from tests.datasets.test_schemas import valid_record
from tests.research.test_arxiv_readiness import _write_card, _write_gold, _write_jsonl


def _write_tar(path: Path, root: Path, names: list[str]) -> None:
    with tarfile.open(path, "w:gz") as archive:
        for name in names:
            file_path = root / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("content\n", encoding="utf-8")
            archive.add(file_path, arcname=name)


def _write_paper(
    paper_dir: Path,
    *,
    has_claim_blocker: bool,
    has_result_placeholders: bool,
) -> None:
    sections_dir = paper_dir / "sections"
    tables_dir = paper_dir / "tables"
    sections_dir.mkdir(parents=True)
    tables_dir.mkdir()
    paper_dir.joinpath("main.tex").write_text(
        "\\title{ObviousBench}\n"
        + (
            "\\claimblocked{final result missing}\n"
            if has_claim_blocker
            else "\\author{Ada Example}\n"
        ),
        encoding="utf-8",
    )
    paper_dir.joinpath("references.bib").write_text(
        "\n".join(
            [
                "@misc{wang2024mmlupro}",
                "@misc{rein2023gpqa}",
                "@misc{phan2026hle}",
                "@misc{wei2024simpleqa}",
                "@misc{zhou2023ifeval}",
                "@misc{jiang2024followbench}",
                "@misc{white2025livebench}",
                "@misc{jain2024livecodebench}",
                "@misc{mirzadeh2025gsmsymbolic}",
                "@misc{jiang2025benchmarkaging}",
                "@misc{simplebench}",
            ]
        ),
        encoding="utf-8",
    )
    sections_dir.joinpath("02_related_work.tex").write_text(
        "\\citep{wang2024mmlupro,rein2023gpqa,phan2026hle}\n"
        "\\citep{wei2024simpleqa,zhou2023ifeval,jiang2024followbench}\n"
        "\\citep{white2025livebench,jain2024livecodebench}\n"
        "\\citep{mirzadeh2025gsmsymbolic,jiang2025benchmarkaging,simplebench}\n",
        encoding="utf-8",
    )
    sections_dir.joinpath("06_results.tex").write_text(
        (
            "No final paper sweep has been run.\n"
            if has_result_placeholders
            else "Final paper sweep results are reported from frozen artifacts.\n"
        ),
        encoding="utf-8",
    )
    sections_dir.joinpath("07_analysis.tex").write_text(
        "Causal explanations are reported as hypotheses.\n",
        encoding="utf-8",
    )
    sections_dir.joinpath("09_limitations_ethics_reproducibility.tex").write_text(
        (
            "The benchmark does not measure general intelligence. Public examples "
            "are contamination-prone. Pricing and provider behavior can change. "
            "The paper excludes private prompts, credentials, and raw provider logs.\n"
        ),
        encoding="utf-8",
    )
    for name in (
        "main_results.tex",
        "family_results.tex",
        "human_baseline_summary.tex",
        "provider_exclusions.tex",
    ):
        tables_dir.joinpath(name).write_text(
            (
                "No final paper sweep has been run\n"
                if has_result_placeholders
                else "Frozen artifact summary\n"
            ),
            encoding="utf-8",
        )
    paper_dir.joinpath("Makefile").write_text(
        "\n".join(
            [
                "assets:",
                "readiness:",
                "readiness-preprint:",
                "related-work:",
                "human-baseline-packet:",
                "human-baseline-audit:",
                "human-baseline-collection-handoff:",
                "human-baseline-score:",
                "human-baseline-thresholds:",
                "human-baseline-promotion:",
                "human-baseline-ops:",
                "result-artifacts:",
                "release-audit:",
                "release-packet:",
                "claims:",
                "pdf:",
                "pdf-audit:",
                "pdf-handoff:",
                "arxiv-package:",
                "arxiv-audit:",
                "metadata:",
                "preflight:",
                "submission-handoff:",
                "analysis-plan:",
                "manuscript-completeness:",
                "report-tracker:",
                "blocker-dashboard:",
                "completion-roadmap:",
                "repro-manifest:",
                "internal-review:",
            ]
        ),
        encoding="utf-8",
    )
    paper_dir.joinpath("README.md").write_text(
        (
            "make assets\n"
            "make readiness\n"
            "make readiness-preprint\n"
            "make related-work\n"
            "make human-baseline-packet\n"
            "make human-baseline-audit\n"
            "make human-baseline-collection-handoff\n"
            "make human-baseline-score\n"
            "make human-baseline-thresholds\n"
            "make human-baseline-promotion\n"
            "make human-baseline-ops\n"
            "make result-artifacts\n"
            "make release-audit\n"
            "make release-packet\n"
            "make pdf-audit\n"
            "make pdf-handoff\n"
            "make preflight\n"
            "make submission-handoff\n"
            "make analysis-plan\n"
            "make manuscript-completeness\n"
            "make report-tracker\n"
            "make blocker-dashboard\n"
            "make completion-roadmap\n"
            "make repro-manifest\n"
        ),
        encoding="utf-8",
    )


def _fixture(tmp_path: Path, *, complete: bool) -> dict[str, Path]:
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    paper_dir = tmp_path / "paper"
    bundle = paper_dir / "arxiv-src.tar.gz"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir)
    _write_gold(gold_dir)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        )
        if complete
        else "item_id,participant_id,answer,seconds,correct,notes\n",
        encoding="utf-8",
    )
    paper_manifest.write_text(
        json.dumps({"item_id": "obviousbench.char_count.en.v0.public.000001"}) + "\n",
        encoding="utf-8",
    )
    _write_paper(
        paper_dir,
        has_claim_blocker=not complete,
        has_result_placeholders=not complete,
    )
    _write_tar(
        bundle,
        tmp_path / "bundle-src",
        [
            "main.tex",
            "references.bib",
            "sections/02_related_work.tex",
        ],
    )
    return {
        "dataset_path": dataset_path,
        "cards_dir": cards_dir,
        "gold_dir": gold_dir,
        "human_baseline": human_baseline,
        "paper_manifest": paper_manifest,
        "paper_dir": paper_dir,
        "bundle": bundle,
    }


def _inputs(
    fixture: dict[str, Path],
    output_path: Path,
    *,
    readiness_profile: Literal["strict", "preprint"] = "preprint",
) -> InternalReviewInputs:
    return InternalReviewInputs(
        dataset_paths=[fixture["dataset_path"]],
        item_cards_dir=fixture["cards_dir"],
        scorer_gold_dir=fixture["gold_dir"],
        human_baseline_path=fixture["human_baseline"],
        paper_manifest_path=fixture["paper_manifest"],
        paper_dir=fixture["paper_dir"],
        bundle_path=fixture["bundle"],
        output_path=output_path,
        claim_audit_output_path=output_path.parent / "claims.md",
        bundle_audit_output_path=output_path.parent / "bundle.md",
        min_gold_examples_per_scorer=2,
        min_human_participants=1,
        readiness_profile=readiness_profile,
    )


def test_internal_review_reports_current_blockers(tmp_path: Path):
    fixture = _fixture(tmp_path, complete=False)
    output_path = tmp_path / "internal-review.md"

    result = audit_internal_research_review(_inputs(fixture, output_path))

    assert not result.ok
    assert result.check_by_name("data claims against artifacts").status == "pass"
    assert result.check_by_name("paper claim evidence").status == "fail"
    assert result.check_by_name("results and analysis artifacts").status == "fail"
    text = output_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text


def test_internal_review_strict_profile_blocks_missing_human_rows(tmp_path: Path):
    fixture = _fixture(tmp_path, complete=False)
    output_path = tmp_path / "internal-review.md"

    result = audit_internal_research_review(
        _inputs(fixture, output_path, readiness_profile="strict")
    )

    assert not result.ok
    assert result.check_by_name("data claims against artifacts").status == "fail"


def test_internal_review_passes_when_evidence_surface_is_complete(tmp_path: Path):
    fixture = _fixture(tmp_path, complete=True)

    result = audit_internal_research_review(
        _inputs(fixture, tmp_path / "internal-review.md")
    )

    assert result.ok
    assert result.failed_count == 0


def test_internal_review_script_writes_report(tmp_path: Path):
    fixture = _fixture(tmp_path, complete=False)
    output_path = tmp_path / "internal-review.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_internal_research_review.py",
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
    assert "Wrote internal research review" in result.stdout
    assert "Overall status: BLOCKED" in output_path.read_text(encoding="utf-8")
