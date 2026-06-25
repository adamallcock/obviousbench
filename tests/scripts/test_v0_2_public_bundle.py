"""Tests for v0.2 public-local bundle build and audit."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.release.audit_v0_2_public_bundle import audit_public_bundle
from scripts.release.build_v0_2_public_release_bundle import build_public_release_bundle


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    _write(
        path,
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
    )


def _write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _root_docs(root: Path) -> None:
    for relative in (
        ".zenodo.json",
        "CITATION.cff",
        "LICENSE",
        "LICENSE-DATA-DOCS.md",
        "README.md",
        "docs/reference/methodology.md",
        "docs/reference/benchmark-card.md",
        "docs/reference/public-release-surface.md",
        "docs/reference/source-policy.md",
        "docs/reference/scoring-policy.md",
        "docs/reference/website.md",
        "docs/positioning/background-and-rhetoric.md",
    ):
        _write(root / relative, f"# {relative}\n")


def _public_example(root: Path) -> None:
    _write_jsonl(
        root / "data/benchmark/public_examples/v0_1/character_count.jsonl",
        [
            {
                "answer_type": "integer",
                "family": "character_count",
                "human_triviality": "H0",
                "id": "public.1",
                "metadata": {
                    "choices": None,
                    "pool_id": "private-pool-id-should-not-copy",
                    "prompt_template_id": "final_answer_only_v0",
                },
                "prompt": "Question: public example?\nAnswer:",
                "question": "public example?",
                "review_status": "reviewed",
                "scorer": "exact_integer_extract_first_v0",
                "source_type": "generated_variant",
                "split": "public_examples_v0_1",
                "subfamily": "single_letter_count",
                "target": "1",
            }
        ],
    )


def _aggregate_files(root: Path) -> dict[str, str]:
    files = {
        "summary_csv": "reports/final/summary.csv",
        "report_markdown": "reports/final/report.md",
    }
    for key, relative in files.items():
        text = "aggregate only\n"
        if key == "report_markdown":
            text = (
                "# Report\n\n"
                "- Source manifest: `results/manifests/v0_2_private_pass3_final.jsonl`\n"
                "- Primary metric: answer pass^3\n"
            )
        _write(root / relative, text)
    return files


def _config(root: Path, aggregate_files: dict[str, str]) -> Path:
    _write(
        root / "docs/release/v0_2/generated/README.md",
        "\n".join(
            [
                "# generated release",
                "",
                "## Generated Artifact Notice",
                "",
                "- Source config: `configs/releases/release_v0_2_0.yaml`",
                "- Generator: `scripts/release/build_v0_2_release_assets.py`",
                "- Status: `local-publication-prep`",
                "- Public/private boundary: excludes private held-out prompts, raw outputs,",
                "  item-level private outcomes, private review HTML, and attempt-level outcomes.",
                "",
            ]
        ),
    )
    config = root / "configs/releases/release_v0_2_0.yaml"
    _write_yaml(
        config,
        {
            "generated": {"output_dir": "docs/release/v0_2/generated"},
            "public_safety": {"public_examples_source": "data/benchmark/public_examples/v0_1"},
            "release": {
                "date": "2026-06-15",
                "id": "test",
                "version": "0.2.0",
            },
            "snapshot": {
                **aggregate_files,
                "attempt_count": 129600,
                "complete_model_setting_count": 294,
                "estimated_cost_usd": 133.18,
                "model_setting_count": 300,
                "private_item_count": 144,
                "scored_attempt_count": 128172,
            },
        },
    )
    _write_yaml(
        root / "configs/model_panels/models_v0_2_public.yaml",
        {"release_panel": [{"label": "mock", "inspect_model": "mockllm/model"}]},
    )
    _write_yaml(
        root / "configs/registries/model_registry_v1.yaml",
        {"models": []},
    )
    _write_yaml(
        root / "configs/registries/model_thinking_settings_v1.yaml",
        {"models": []},
    )
    return config


def _private_data(root: Path) -> None:
    private_row = {
        "answer_type": "integer",
        "id": "obviousbench.private.v02.000001",
        "metadata": {"candidate_id": "private-candidate-1", "pool_id": "private-pool-1"},
        "prompt": "Answer only.\nQuestion: Count the private bananas.\nAnswer:",
        "question": "Count the private bananas.",
        "target": "7",
    }
    _write_jsonl(
        root / "data/benchmark/private_heldout/v0_2/character_count.jsonl",
        [private_row],
    )
    _write_jsonl(
        root
        / "data/manifests/candidate_pools/"
        "candidate_pool_v0_2_private_heldout_draft_manifest.jsonl",
        [private_row],
    )


def test_v0_2_public_bundle_excludes_private_terms(tmp_path: Path) -> None:
    _root_docs(tmp_path)
    _public_example(tmp_path)
    config = _config(tmp_path, _aggregate_files(tmp_path))
    _private_data(tmp_path)

    bundle = build_public_release_bundle(
        config_path=config,
        output_dir=tmp_path / "dist/bundle",
        root=tmp_path,
    )
    audit = audit_public_bundle(bundle_dir=bundle.output_dir, data_dir=tmp_path / "data")

    assert audit["ok"] is True
    public_example = bundle.output_dir / "data/public_examples/character_count.jsonl"
    assert "private-pool-id-should-not-copy" not in public_example.read_text(encoding="utf-8")
    report = bundle.output_dir / "reports/v0_2/aggregate/report.md"
    assert "results/manifests/v0_2_private_pass3" not in report.read_text(encoding="utf-8")
    manifest = json.loads((bundle.output_dir / "bundle_manifest.json").read_text(encoding="utf-8"))
    assert sorted(manifest["included_files"]) == sorted(
        str(path.relative_to(bundle.output_dir))
        for path in bundle.output_dir.rglob("*")
        if path.is_file()
    )


def test_v0_2_public_bundle_audit_ignores_platform_metadata(tmp_path: Path) -> None:
    _root_docs(tmp_path)
    _public_example(tmp_path)
    config = _config(tmp_path, _aggregate_files(tmp_path))
    _private_data(tmp_path)

    bundle = build_public_release_bundle(
        config_path=config,
        output_dir=tmp_path / "dist/bundle",
        root=tmp_path,
    )
    _write(bundle.output_dir / ".DS_Store", "finder metadata\n")

    audit = audit_public_bundle(bundle_dir=bundle.output_dir, data_dir=tmp_path / "data")

    assert audit["ok"] is True


def test_v0_2_public_bundle_audit_flags_private_question(tmp_path: Path) -> None:
    _private_data(tmp_path)
    bundle_dir = tmp_path / "dist/bundle"
    _write(bundle_dir / "README.md", "Count the private bananas.\n")

    audit = audit_public_bundle(bundle_dir=bundle_dir, data_dir=tmp_path / "data")

    assert audit["ok"] is False
    assert "private_term_leak" in {issue["code"] for issue in audit["issues"]}


def test_v0_2_public_bundle_audit_flags_stale_private_paths(tmp_path: Path) -> None:
    _private_data(tmp_path)
    bundle_dir = tmp_path / "dist/bundle"
    _write(
        bundle_dir / "bundle_manifest.json",
        json.dumps({"included_files": ["README.md", "bundle_manifest.json"]}),
    )
    _write(bundle_dir / "README.md", "reports/v0_1/private_pass3_final/report.md\n")

    audit = audit_public_bundle(bundle_dir=bundle_dir, data_dir=tmp_path / "data")

    assert audit["ok"] is False
    assert "forbidden_private_reference" in {issue["code"] for issue in audit["issues"]}


def test_v0_2_public_bundle_audit_requires_generated_markdown_notice(
    tmp_path: Path,
) -> None:
    _private_data(tmp_path)
    bundle_dir = tmp_path / "dist/bundle"
    _write(bundle_dir / "docs/release/v0_2/generated/README.md", "# generated\n")
    files = sorted(
        str(path.relative_to(bundle_dir)) for path in bundle_dir.rglob("*") if path.is_file()
    )
    _write(
        bundle_dir / "bundle_manifest.json",
        json.dumps({"included_files": sorted([*files, "bundle_manifest.json"])}),
    )

    audit = audit_public_bundle(bundle_dir=bundle_dir, data_dir=tmp_path / "data")

    assert audit["ok"] is False
    assert "missing_generated_provenance" in {issue["code"] for issue in audit["issues"]}
