from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import yaml

from obviousbench.analysis.comparison import COMPARISON_FIELDS
from obviousbench.research.release_snapshot import (
    ReleaseSnapshotInputs,
    audit_release_snapshot,
    build_local_release_assets,
)


def _write(path: Path, text: str = "content\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _config(root: Path, *, write_evidence_bundle_outputs: bool = True) -> Path:
    manifest = root / "manifest.csv"
    comparison_dir = root / "comparison"
    report_dir = root / "report"
    effort_dir = root / "effort"
    paper_dir = root / "paper"
    docs_dir = root / "docs"
    data_dir = root / "data"
    public_data_dir = data_dir / "public_v0"
    cards_dir = data_dir / "item_cards" / "public_v0"
    proofpoint_dir = docs_dir / "shareable" / "proofpoint"
    stale_report_dir = docs_dir / "reports" / "stale"
    exploratory_dir = data_dir / "experiments"
    _write_csv(
        manifest,
        ["label", "model", "summary_dir"],
        [{"label": "Unit", "model": "provider/unit", "summary_dir": str(root / "run")}],
    )
    comparison_row = {field: "" for field in COMPARISON_FIELDS}
    comparison_row.update(
        {
            "label": "Unit",
            "model": "provider/unit",
            "barrage_profile": "unit_profile",
            "scored_samples": "2",
            "answer_accuracy": "1",
        }
    )
    _write_csv(comparison_dir / "comparison.csv", list(COMPARISON_FIELDS), [comparison_row])
    _write_csv(
        report_dir / "leaderboard.csv",
        ["label", "model", "barrage_profile", "scored_samples"],
        [
            {
                "label": "Unit",
                "model": "provider/unit",
                "barrage_profile": "unit_profile",
                "scored_samples": "2",
            }
        ],
    )
    for filename in (
        "report.html",
        "leaderboard.md",
        "family-heatmap.csv",
        "wrong-answer-review.csv",
        "wrong-answer-review.html",
    ):
        _write(report_dir / filename)
    _write_csv(
        effort_dir / "effort-cost-curve-points.csv",
        ["provider", "curve", "model", "effort", "label", "scored_samples"],
        [
            {
                "provider": "Unit",
                "curve": "Unit",
                "model": "provider/unit",
                "effort": "low",
                "label": "Unit low",
                "scored_samples": "2",
            }
        ],
    )
    _write_csv(
        effort_dir / "effort-cost-curve-missing-points.csv",
        ["provider", "curve", "model", "effort", "label", "expected_summary_suffix", "note"],
        [],
    )
    _write(root / "paper_manifest.jsonl", "{}\n")
    _write(
        public_data_dir / "arithmetic.jsonl",
        "\n".join(
            [
                json.dumps(
                    {
                        "id": "obviousbench.arith.en.v0.public.000001",
                        "family": "arithmetic",
                        "subfamily": "small_integer_arithmetic",
                        "prompt": "Answer only.\n\nQuestion: What is 1 + 1?\nAnswer:",
                        "question": "What is 1 + 1?",
                        "target": "2",
                        "answer_type": "integer",
                        "scorer": "exact_integer_extract_first_v0",
                        "split": "public_v0",
                        "source_type": "generated_variant",
                        "source_refs": ["unit_source"],
                        "human_triviality": "H0",
                        "review_status": "reviewed",
                        "metadata": {
                            "generated": True,
                            "prompt_template_id": "final_answer_only_v0",
                            "strict_format": False,
                            "why_obvious": "Simple arithmetic.",
                        },
                    },
                    sort_keys=True,
                ),
                json.dumps(
                    {
                        "id": "obviousbench.format.en.v0.public.000001",
                        "family": "format_compliance",
                        "subfamily": "exact_json_schema",
                        "prompt": "Return JSON with field answer set to yes.",
                        "question": "Return JSON with field answer set to yes.",
                        "target": '{"answer":"yes"}',
                        "answer_type": "json",
                        "scorer": "json_exact_field_v0",
                        "split": "public_v0",
                        "source_type": "hand_authored",
                        "source_refs": ["unit_source"],
                        "human_triviality": "H1",
                        "review_status": "reviewed",
                        "metadata": {
                            "generated": False,
                            "prompt_template_id": "final_answer_only_v0",
                            "strict_format": True,
                            "why_obvious": "The field and value are stated directly.",
                            "metamorphic_group_id": "unit-format",
                            "metamorphic_role": "base",
                        },
                    },
                    sort_keys=True,
                ),
            ]
        )
        + "\n",
    )
    _write(
        cards_dir / "cards.yaml",
        yaml.safe_dump(
            {
                "cards": [
                    {
                        "item_id": "obviousbench.arith.en.v0.public.000001",
                        "archetype_id": "unit_arithmetic",
                        "source_refs": ["unit_source"],
                        "source_type": "generated_variant",
                        "source_summary": "Unit source.",
                        "answer_derivation": "1 + 1 evaluates to 2.",
                        "expected_answer": "2",
                        "scorer_contract": {
                            "scorer": "exact_integer_extract_first_v0",
                            "answer_type": "integer",
                            "strict_format": False,
                            "acceptable_outputs": ["2"],
                            "unacceptable_outputs": [],
                        },
                        "ambiguity_notes": ["Prompt identifies the operands directly."],
                        "split_policy": {
                            "allowed_splits": ["public_v0"],
                            "leakage_risk": "medium",
                            "publishable": True,
                            "rationale": "Unit public item.",
                        },
                        "review": {
                            "status": "reviewed",
                            "reviewer": "unit",
                            "reviewed_on": "2026-06-03",
                            "notes": "Unit reviewed item.",
                        },
                    },
                    {
                        "item_id": "obviousbench.format.en.v0.public.000001",
                        "archetype_id": "unit_format",
                        "source_refs": ["unit_source"],
                        "source_type": "hand_authored",
                        "source_summary": "Unit source.",
                        "answer_derivation": "The prompt names the exact JSON field and value.",
                        "expected_answer": '{"answer":"yes"}',
                        "scorer_contract": {
                            "scorer": "json_exact_field_v0",
                            "answer_type": "json",
                            "strict_format": True,
                            "acceptable_outputs": ['{"answer":"yes"}'],
                            "unacceptable_outputs": [],
                        },
                        "ambiguity_notes": ["No ambiguity in requested JSON field."],
                        "split_policy": {
                            "allowed_splits": ["public_v0"],
                            "leakage_risk": "low",
                            "publishable": True,
                            "rationale": "Unit public item.",
                        },
                        "review": {
                            "status": "reviewed",
                            "reviewer": "unit",
                            "reviewed_on": "2026-06-03",
                            "notes": "Unit reviewed item.",
                        },
                    },
                ]
            },
            sort_keys=False,
        ),
    )
    _write(proofpoint_dir / "README.md", "Proofpoint bundle.\n")
    _write(stale_report_dir / "README.md", "Stale report.\n")
    _write(exploratory_dir / "experiment.jsonl", "{}\n")
    _write(root / "theme.yaml", "colors: {}\n")
    _write(
        root / "surfaces.yaml",
        yaml.safe_dump(
            {
                "surfaces": {
                    "citation_cff": {"path": str(root / "CITATION.cff")},
                    "zenodo_metadata": {"path": str(root / ".zenodo.json")},
                }
            },
            sort_keys=False,
        ),
    )
    _write(paper_dir / "Makefile", "EVIDENCE_EXPECTED_MODELS := 1\n")
    config = {
        "release": {
            "id": "unit",
            "version": "0.0.0",
            "tag": "v0",
            "title": "Unit",
            "short_name": "Unit",
            "date": "2026-06-03",
        },
        "authors": [
            {
                "family_names": "Example",
                "given_names": "Ada",
                "name": "Example, Ada",
                "affiliation": "Test Lab",
            }
        ],
        "licenses": {"code": "Apache-2.0", "data_docs": "CC-BY-4.0"},
        "snapshot": {
            "name": "unit",
            "dataset_split": "unit",
            "item_count": 2,
            "expected_model_settings": 1,
            "expected_scored_samples": 2,
            "barrage_profile": "unit_profile",
            "manifest": str(manifest),
            "comparison_dir": str(comparison_dir),
            "report_dir": str(report_dir),
            "paper_manifest": str(root / "paper_manifest.jsonl"),
            "wrong_answer_review": str(report_dir / "wrong-answer-review.csv"),
        },
        "effort_cost": {
            "report_dir": str(effort_dir),
            "points_csv": str(effort_dir / "effort-cost-curve-points.csv"),
            "missing_points_csv": str(effort_dir / "effort-cost-curve-missing-points.csv"),
            "expected_scored_samples": 2,
            "required_points": [
                {"model": "provider/unit", "effort": "low", "label": "Unit low"}
            ],
        },
        "generated": {
            "output_dir": str(root / "generated"),
            "theme_config": str(root / "theme.yaml"),
            "surfaces_config": str(root / "surfaces.yaml"),
            "paper_release_makefile": str(root / "paper" / "release.mk"),
            "provenance": str(root / "generated" / "provenance.json"),
            "release_index": str(root / "generated" / "README.md"),
            "release_metadata": str(root / "generated" / "release-metadata.json"),
        },
        "evidence_bundle": {
            "snapshot_registry": str(root / "generated" / "snapshot-registry.json"),
            "release_evidence_json": str(root / "generated" / "release-evidence.json"),
            "item_review_matrix_json": str(
                root / "docs" / "internal" / "release" / "generated" / "item-review-matrix.json"
            ),
            "item_review_matrix_md": str(
                root / "docs" / "internal" / "release" / "generated" / "item-review-matrix.md"
            ),
            "external_review_packet": str(root / "generated" / "external-review-packet.md"),
            "evidence_and_claims": str(docs_dir / "evidence-and-claims.md"),
            "charts_dir": str(root / "generated" / "charts"),
            "item_cards_dir": str(cards_dir),
            "dataset_files": [str(public_data_dir / "arithmetic.jsonl")],
            "item_review_source_files": [str(public_data_dir / "arithmetic.jsonl")],
            "artifact_registry": [
                {
                    "id": "unit-current-release-control-plane",
                    "status_label": "current",
                    "paths": [str(root / "release.yaml")],
                    "claim_allowed": "Use for current local release-prep commands.",
                    "claim_disallowed": "Do not cite as a frozen result snapshot.",
                },
                {
                    "id": "unit-release-snapshot",
                    "status_label": "release_snapshot",
                    "paths": [str(manifest), str(comparison_dir), str(report_dir)],
                    "claim_allowed": "Use for frozen v0.0.0 result claims.",
                    "claim_disallowed": "Do not treat as a live leaderboard.",
                },
                {
                    "id": "unit-proofpoint",
                    "status_label": "proofpoint",
                    "paths": [str(proofpoint_dir)],
                    "claim_allowed": "Use as a small demo bundle.",
                    "claim_disallowed": "Do not cite as release evidence.",
                },
                {
                    "id": "unit-exploratory",
                    "status_label": "exploratory",
                    "paths": [str(exploratory_dir)],
                    "claim_allowed": "Use for research notes only.",
                    "claim_disallowed": "Do not cite as release evidence.",
                },
                {
                    "id": "unit-stale-report",
                    "status_label": "stale",
                    "paths": [str(stale_report_dir)],
                    "claim_allowed": "Use only as historical context.",
                    "claim_disallowed": "Do not use for current claims.",
                },
            ],
        },
        "claim_limits": {"summary": "Unit summary", "caveats": ["Unit caveat"]},
        "public_links": {
            "repository_url": {"value": "https://example.test/repo", "status": "planned"},
            "dataset_url": {"value": "https://example.test/data", "status": "planned"},
        },
        "audit": {
            "stale_reference_paths": [str(paper_dir)],
            "forbidden_release_strings": ["old-snapshot"],
        },
    }
    config_path = root / "release.yaml"
    _write(config_path, yaml.safe_dump(config, sort_keys=False))
    if write_evidence_bundle_outputs:
        _write(
            root / "generated" / "snapshot-registry.json",
            json.dumps(
                {
                    "artifacts": [
                        {
                            "id": label,
                            "status_label": label,
                            "paths": [{"path": str(root), "exists": True}],
                        }
                        for label in (
                            "current",
                            "stale",
                            "exploratory",
                            "proofpoint",
                            "release_snapshot",
                        )
                    ]
                }
            )
            + "\n",
        )
        _write(root / "generated" / "release-evidence.json", json.dumps({"schema_version": 1}))
        _write(
            root / "docs" / "internal" / "release" / "generated" / "item-review-matrix.json",
            json.dumps({"summary": {"item_count": 2}, "items": []}) + "\n",
        )
        _write(
            root / "docs" / "internal" / "release" / "generated" / "item-review-matrix.md",
            "# Matrix\n",
        )
        _write(root / "generated" / "external-review-packet.md", "# External Review\n")
        _write(docs_dir / "evidence-and-claims.md", "# Evidence\n")
        for path in (
            root / "generated" / "charts" / "snapshot-status.svg",
            root / "generated" / "charts" / "evidence-readiness.svg",
            root / "generated" / "charts" / "model-accuracy.svg",
        ):
            _write(path, "<svg>Generated from fixture</svg>\n")
    return config_path


def test_release_snapshot_audit_passes_complete_local_contract(tmp_path: Path):
    config_path = _config(tmp_path)

    result = audit_release_snapshot(
        ReleaseSnapshotInputs(config_path=config_path, output_path=tmp_path / "audit.md")
    )

    assert result.ok
    assert result.failed_count == 0
    assert result.check_by_name("manifest row count").status == "pass"
    assert result.check_by_name("effort cost contract").status == "pass"
    assert "Overall status: PASS" in (tmp_path / "audit.md").read_text(encoding="utf-8")


def test_release_snapshot_audit_blocks_stale_references(tmp_path: Path):
    config_path = _config(tmp_path)
    _write(tmp_path / "paper" / "main.tex", "this cites old-snapshot\n")

    result = audit_release_snapshot(
        ReleaseSnapshotInputs(config_path=config_path, output_path=tmp_path / "audit.md")
    )

    assert not result.ok
    assert result.check_by_name("stale release references").status == "fail"
    assert "old-snapshot" in result.check_by_name("stale release references").evidence


def test_build_release_assets_writes_metadata_makefile_and_drafts(tmp_path: Path):
    config_path = _config(tmp_path)
    outputs = build_local_release_assets(config_path)

    assert tmp_path / "generated" / "README.md" in outputs
    release_mk = tmp_path / "paper" / "release.mk"
    assert release_mk.exists()
    assert "EVIDENCE_EXPECTED_MODELS := 1" in release_mk.read_text(encoding="utf-8")
    assert (tmp_path / "generated" / "release-metadata.json").exists()
    assert (tmp_path / "generated" / "provenance.json").exists()
    assert (tmp_path / "CITATION.cff").exists()
    assert (tmp_path / ".zenodo.json").exists()


def test_build_release_assets_writes_evidence_bundle_registry_matrix_and_charts(tmp_path: Path):
    config_path = _config(tmp_path, write_evidence_bundle_outputs=False)

    outputs = build_local_release_assets(config_path)

    output_set = set(outputs)
    registry_path = tmp_path / "generated" / "snapshot-registry.json"
    release_evidence_path = tmp_path / "generated" / "release-evidence.json"
    matrix_json_path = (
        tmp_path / "docs" / "internal" / "release" / "generated" / "item-review-matrix.json"
    )
    matrix_md_path = (
        tmp_path / "docs" / "internal" / "release" / "generated" / "item-review-matrix.md"
    )
    review_packet_path = tmp_path / "generated" / "external-review-packet.md"
    evidence_doc_path = tmp_path / "docs" / "evidence-and-claims.md"
    chart_paths = {
        tmp_path / "generated" / "charts" / "snapshot-status.svg",
        tmp_path / "generated" / "charts" / "evidence-readiness.svg",
        tmp_path / "generated" / "charts" / "model-accuracy.svg",
    }

    assert {
        registry_path,
        release_evidence_path,
        matrix_json_path,
        matrix_md_path,
        review_packet_path,
        evidence_doc_path,
    } <= output_set
    assert chart_paths <= output_set

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    assert registry["schema_version"] == 1
    assert set(registry["required_status_labels"]) == {
        "current",
        "stale",
        "exploratory",
        "proofpoint",
        "release_snapshot",
    }
    artifact_by_id = {artifact["id"]: artifact for artifact in registry["artifacts"]}
    assert artifact_by_id["unit-release-snapshot"]["status_label"] == "release_snapshot"
    assert artifact_by_id["unit-release-snapshot"]["path_count"] == 3
    assert artifact_by_id["unit-release-snapshot"]["all_paths_present"] is True

    release_evidence = json.loads(release_evidence_path.read_text(encoding="utf-8"))
    assert release_evidence["schema_version"] == 1
    assert release_evidence["registry"]["status_label_counts"]["release_snapshot"] == 1
    assert release_evidence["item_review_matrix"]["item_count"] == 2
    assert release_evidence["item_review_matrix"]["visibility"] == "internal-only"
    assert release_evidence["charts"] == [
        str(tmp_path / "generated" / "charts" / "snapshot-status.svg"),
        str(tmp_path / "generated" / "charts" / "evidence-readiness.svg"),
        str(tmp_path / "generated" / "charts" / "model-accuracy.svg"),
    ]

    matrix = json.loads(matrix_json_path.read_text(encoding="utf-8"))
    assert matrix["summary"]["item_count"] == 2
    assert matrix["summary"]["review_status_counts"] == {"reviewed": 2}
    assert matrix["summary"]["strict_format_count"] == 1
    row_by_id = {row["item_id"]: row for row in matrix["items"]}
    assert row_by_id["obviousbench.format.en.v0.public.000001"]["source_type"] == "hand_authored"
    assert row_by_id["obviousbench.format.en.v0.public.000001"]["metamorphic_group_id"] == (
        "unit-format"
    )
    assert "No ambiguity in requested JSON field." in row_by_id[
        "obviousbench.format.en.v0.public.000001"
    ]["ambiguity_notes"]

    matrix_md = matrix_md_path.read_text(encoding="utf-8")
    assert "# ObviousBench Item Review Matrix" in matrix_md
    assert "| obviousbench.format.en.v0.public.000001 | format_compliance |" in matrix_md
    assert "strict format items: 1" in matrix_md

    review_packet = review_packet_path.read_text(encoding="utf-8")
    assert "# ObviousBench External Review Packet" in review_packet
    assert "## Reviewer Questions" in review_packet
    assert "`unit-release-snapshot`" in review_packet
    assert f"- Snapshot registry: `{registry_path}`" in review_packet
    assert f"- Item review matrix: `{matrix_md_path}`" in review_packet
    assert f"- Release evidence JSON: `{release_evidence_path}`" in review_packet

    evidence_doc = evidence_doc_path.read_text(encoding="utf-8")
    assert "title: ObviousBench Evidence And Claims" in evidence_doc
    assert "## Allowed Claims" in evidence_doc
    assert "`unit-release-snapshot`" in evidence_doc
    assert "item-review-matrix" not in evidence_doc
    assert "item review matrix" not in evidence_doc.lower()

    for chart_path in chart_paths:
        svg = chart_path.read_text(encoding="utf-8")
        assert svg.startswith("<svg")
        assert "Generated from" in svg


def test_release_snapshot_audit_blocks_missing_evidence_bundle_outputs(tmp_path: Path):
    config_path = _config(tmp_path, write_evidence_bundle_outputs=False)

    result = audit_release_snapshot(ReleaseSnapshotInputs(config_path=config_path))

    check = result.check_by_name("evidence bundle contract")
    assert check.status == "fail"
    assert "snapshot-registry.json" in check.evidence

    build_local_release_assets(config_path)
    repaired = audit_release_snapshot(ReleaseSnapshotInputs(config_path=config_path))

    assert repaired.check_by_name("evidence bundle contract").status == "pass"


def test_release_snapshot_audit_blocks_public_item_review_matrix_paths(tmp_path: Path):
    config_path = _config(tmp_path)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["evidence_bundle"]["item_review_matrix_json"] = str(
        tmp_path / "generated" / "item-review-matrix.json"
    )
    config["evidence_bundle"]["item_review_matrix_md"] = str(
        tmp_path / "generated" / "item-review-matrix.md"
    )
    _write(
        Path(config["evidence_bundle"]["item_review_matrix_json"]),
        json.dumps({"summary": {"item_count": 2}, "items": []}) + "\n",
    )
    _write(Path(config["evidence_bundle"]["item_review_matrix_md"]), "# Review\n")
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")

    result = audit_release_snapshot(ReleaseSnapshotInputs(config_path=config_path))

    check = result.check_by_name("evidence bundle contract")
    assert check.status == "fail"
    assert "item review matrix must be under an internal path" in check.evidence


def test_release_snapshot_audit_blocks_public_item_review_matrix_surface(tmp_path: Path):
    config_path = _config(tmp_path)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    surfaces_path = Path(config["generated"]["surfaces_config"])
    surfaces = yaml.safe_load(surfaces_path.read_text(encoding="utf-8"))
    surfaces["surfaces"]["item_review_matrix_md"] = {
        "path": config["evidence_bundle"]["item_review_matrix_md"],
        "public": True,
    }
    surfaces_path.write_text(yaml.safe_dump(surfaces, sort_keys=False), encoding="utf-8")

    result = audit_release_snapshot(ReleaseSnapshotInputs(config_path=config_path))

    check = result.check_by_name("evidence bundle contract")
    assert check.status == "fail"
    assert "item review matrix surface must be public: false" in check.evidence


def test_build_release_assets_generates_citation_and_zenodo_metadata(tmp_path: Path):
    config_path = _config(tmp_path)
    build_local_release_assets(config_path)

    citation = (tmp_path / "CITATION.cff").read_text(encoding="utf-8")
    zenodo = json.loads((tmp_path / ".zenodo.json").read_text(encoding="utf-8"))

    assert 'date-released: "2026-06-03"' in citation
    assert 'repository-code: "https://example.test/repo"' in citation
    assert zenodo["creators"] == [{"name": "Example, Ada", "affiliation": "Test Lab"}]
    assert zenodo["license"] == "Apache-2.0"


def test_build_release_assets_records_source_input_hashes(tmp_path: Path):
    config_path = _config(tmp_path)
    build_local_release_assets(config_path)

    provenance = json.loads(
        (tmp_path / "generated" / "provenance.json").read_text(encoding="utf-8")
    )
    input_by_role = {item["role"]: item for item in provenance["inputs"]}

    assert provenance["python_environment"]["python_version"]
    assert isinstance(provenance["python_environment"]["lockfiles_present"], bool)
    assert provenance["python_environment"]["dependency_files"]
    assert input_by_role["release config"]["sha256"]
    assert input_by_role["theme config"]["sha256"]
    assert input_by_role["surfaces config"]["sha256"]
    assert input_by_role["snapshot manifest"]["sha256"]
    assert input_by_role["comparison CSV"]["sha256"]
    assert input_by_role["leaderboard CSV"]["sha256"]
    assert input_by_role["effort cost points"]["sha256"]
    assert any(
        item["role"] == "item cards directory" and item["sha256"] and item["file_count"]
        for item in provenance["inputs"]
    )
    assert any(
        item["role"] == "item review source file" and item["sha256"]
        for item in provenance["inputs"]
    )
    assert any(
        item["role"] == "release dataset file" and item["sha256"]
        for item in provenance["inputs"]
    )
    assert all(item["exists"] for item in provenance["inputs"])


def test_release_snapshot_script_strict_returns_nonzero_on_failure(tmp_path: Path):
    config_path = _config(tmp_path)
    _write(tmp_path / "paper" / "main.tex", "old-snapshot\n")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_release_snapshot.py",
            "--config",
            str(config_path),
            "--out",
            str(tmp_path / "audit.md"),
            "--strict",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "BLOCKED" in result.stdout
