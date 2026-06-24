#!/usr/bin/env python3
"""Build the allowlisted v0.2 public-local release bundle."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

try:
    from scripts.release.audit_v0_2_public_bundle import private_leak_terms, private_manifest_rows
except ModuleNotFoundError:  # pragma: no cover - direct script execution path
    from audit_v0_2_public_bundle import private_leak_terms, private_manifest_rows

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "configs/releases/release_v0_2_0.yaml"
DEFAULT_OUT = ROOT / "dist/obviousbench-v0.2-public-local"

SAFE_ROOT_DOCS = (
    "README.md",
    "docs/reference/methodology.md",
    "docs/reference/benchmark-card.md",
    "docs/reference/source-policy.md",
    "docs/reference/scoring-policy.md",
    "docs/reference/website.md",
    "docs/positioning/background-and-rhetoric.md",
)

SAFE_CONFIGS = (
    "configs/releases/release_v0_2_0.yaml",
    "configs/model_panels/models_v0_2_public.yaml",
    "configs/registries/model_registry_v1.yaml",
    "configs/registries/model_thinking_settings_v1.yaml",
)

SAFE_GENERATED_SURFACES = (
    "README.md",
    "github-release-notes.md",
    "huggingface-dataset-card.md",
    "provenance.json",
    "release-metadata.json",
)

SAFE_AGGREGATE_REPORT_KEYS = (
    "summary_csv",
    "report_markdown",
)


@dataclass(frozen=True)
class BundleBuildResult:
    output_dir: Path
    manifest_path: Path
    included_files: list[str]
    skipped_optional_paths: list[str]
    skipped_public_examples: list[str]


def rel(path: Path, *, root: Path = ROOT) -> str:
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path)


def read_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML file is not an object: {path}")
    return payload


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def copy_relative(
    *,
    root: Path,
    output_dir: Path,
    relative_path: str,
    included: list[str],
    required: bool = True,
    skipped: list[str] | None = None,
) -> None:
    source = root / relative_path
    if not source.exists():
        if required:
            raise FileNotFoundError(source)
        if skipped is not None:
            skipped.append(relative_path)
        return
    destination = output_dir / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    included.append(str(destination.relative_to(output_dir)))


def sanitize_public_example(row: dict[str, Any]) -> dict[str, Any]:
    metadata = row.get("metadata")
    metadata = metadata if isinstance(metadata, dict) else {}
    return {
        "id": row["id"],
        "family": row["family"],
        "subfamily": row["subfamily"],
        "split": row["split"],
        "prompt": row["prompt"],
        "question": row["question"],
        "target": row["target"],
        "answer_type": row["answer_type"],
        "scorer": row["scorer"],
        "human_triviality": row["human_triviality"],
        "review_status": row["review_status"],
        "source_type": row["source_type"],
        "source_refs": [],
        "metadata": {
            "choices": metadata.get("choices"),
            "prompt_template_id": metadata.get("prompt_template_id"),
            "publication_status": "public_example_v0_2_bundle",
            "strict_format": metadata.get("strict_format", False),
        },
    }


def copy_public_examples(
    *,
    root: Path,
    output_dir: Path,
    source_dir: Path,
    included: list[str],
    leak_terms: dict[str, str],
    skipped: list[str],
) -> None:
    source_dir = source_dir if source_dir.is_absolute() else root / source_dir
    if not source_dir.exists():
        raise FileNotFoundError(source_dir)
    for source in sorted(source_dir.glob("*.jsonl")):
        destination = output_dir / "data/public_examples" / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        safe_rows = []
        for row in read_jsonl(source):
            label = public_example_private_collision(row, leak_terms)
            if label:
                skipped.append(f"{source.relative_to(root)}:{row.get('id')}:{label}")
                continue
            safe_rows.append(row)
        destination.write_text(
            "".join(
                json.dumps(sanitize_public_example(row), sort_keys=True) + "\n"
                for row in safe_rows
            ),
            encoding="utf-8",
        )
        included.append(str(destination.relative_to(output_dir)))


def public_example_private_collision(row: dict[str, Any], leak_terms: dict[str, str]) -> str:
    metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    values = [
        row.get("id"),
        row.get("question"),
        row.get("prompt"),
        row.get("target"),
        row.get("pool_id"),
        row.get("candidate_id"),
        metadata.get("pool_id"),
        metadata.get("candidate_id"),
    ]
    choices = row.get("choices") or metadata.get("choices")
    if isinstance(choices, list):
        values.extend(choices)
    for value in values:
        text = str(value or "")
        if text and text in leak_terms:
            return leak_terms[text]
    return ""


def copy_generated_surfaces(
    *,
    root: Path,
    output_dir: Path,
    generated_dir: Path,
    included: list[str],
    skipped: list[str],
) -> None:
    generated_dir = generated_dir if generated_dir.is_absolute() else root / generated_dir
    if not generated_dir.exists():
        skipped.append(rel(generated_dir, root=root))
        return
    for source in sorted(path for path in generated_dir.rglob("*") if path.is_file()):
        relative = str(source.relative_to(generated_dir))
        if source.name == "public-bundle-audit.json":
            skipped.append(str(source.relative_to(root)))
            continue
        if relative not in SAFE_GENERATED_SURFACES:
            skipped.append(str(source.relative_to(root)))
            continue
        destination = output_dir / "docs/release/v0_2/generated" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        included.append(str(destination.relative_to(output_dir)))


def copy_aggregate_evidence(
    *,
    root: Path,
    output_dir: Path,
    config: dict[str, Any],
    included: list[str],
) -> None:
    snapshot = config["snapshot"]
    for key in SAFE_AGGREGATE_REPORT_KEYS:
        source = root / snapshot[key]
        if not source.exists():
            raise FileNotFoundError(source)
        destination = output_dir / "reports/v0_2/aggregate" / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        if key == "report_markdown":
            destination.write_text(
                sanitize_aggregate_report_markdown(source.read_text(encoding="utf-8")),
                encoding="utf-8",
            )
        else:
            shutil.copyfile(source, destination)
        included.append(str(destination.relative_to(output_dir)))


def sanitize_aggregate_report_markdown(text: str) -> str:
    sanitized: list[str] = []
    for line in text.splitlines():
        if line.startswith("- Source manifest:"):
            sanitized.append(
                "- Source manifest: held-out runtime manifest retained locally; "
                "not included in this public bundle."
            )
        else:
            sanitized.append(line)
    return "\n".join(sanitized).rstrip() + "\n"


def write_bundle_readme(
    *,
    output_dir: Path,
    config: dict[str, Any],
    included: list[str],
) -> None:
    release = config["release"]
    snapshot = config["snapshot"]
    path = output_dir / "README.md"
    lines = [
        "---",
        f"title: ObviousBench v{release['version']} Public-Local Release Bundle",
        f"date: {release['date']}",
        "type: release-bundle",
        "status: local-prep",
        "---",
        "",
        f"# ObviousBench v{release['version']} Public-Local Release Bundle",
        "",
        "This bundle is allowlisted for public review but has not been published.",
        "It contains public examples and aggregate v0.2 private benchmark results.",
        "",
        "The canonical public narrative and interactive charts live at",
        "[obviousbench.com](https://obviousbench.com). This repository is the",
        "source/data companion rather than a duplicate website deploy tree.",
        "",
        "It intentionally excludes private held-out prompts, raw logs, raw model",
        "outputs, private review HTML, private item-level outcomes, and private",
        "attempt-level outcomes.",
        "",
        "## Snapshot",
        "",
        f"- Private held-out items: {snapshot['private_item_count']}",
        f"- Model/config rows: {snapshot['model_setting_count']}",
        f"- Complete rows: {snapshot['complete_model_setting_count']}",
        f"- Attempt rows: {snapshot['attempt_count']}",
        f"- Scored attempts: {snapshot['scored_attempt_count']}",
        f"- Estimated cost: ${float(snapshot['estimated_cost_usd']):.2f}",
        "",
        "## Included Files",
        "",
    ]
    lines.extend(f"- `{item}`" for item in sorted(included) if item != "README.md")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    if "README.md" not in included:
        included.append("README.md")


def write_manifest(
    *,
    output_dir: Path,
    config: dict[str, Any],
    included: list[str],
    skipped: list[str],
    skipped_public_examples: list[str],
) -> Path:
    release = config["release"]
    if "bundle_manifest.json" not in included:
        included.append("bundle_manifest.json")
    manifest = {
        "bundle": "obviousbench-v0.2-public-local",
        "generated_on": str(release["date"]),
        "release_id": str(release["id"]),
        "included_files": sorted(included),
        "skipped_public_examples_count": len(skipped_public_examples),
        "skipped_optional_paths": sorted(skipped),
        "privacy_policy": {
            "public_examples_included": True,
            "aggregate_private_results_included": True,
            "private_prompts_included": False,
            "private_raw_logs_included": False,
            "private_row_level_outcomes_included": False,
            "private_review_html_included": False,
        },
    }
    path = output_dir / "bundle_manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def build_public_release_bundle(
    *,
    config_path: Path = DEFAULT_CONFIG,
    output_dir: Path = DEFAULT_OUT,
    root: Path = ROOT,
) -> BundleBuildResult:
    config = read_yaml(config_path)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    included: list[str] = []
    skipped: list[str] = []
    skipped_public_examples: list[str] = []
    leak_terms = private_leak_terms(private_manifest_rows(root / "data"))
    for relative_path in SAFE_ROOT_DOCS:
        copy_relative(
            root=root,
            output_dir=output_dir,
            relative_path=relative_path,
            included=included,
        )
    for relative_path in SAFE_CONFIGS:
        copy_relative(
            root=root,
            output_dir=output_dir,
            relative_path=relative_path,
            included=included,
            required=False,
            skipped=skipped,
        )
    copy_generated_surfaces(
        root=root,
        output_dir=output_dir,
        generated_dir=Path(config["generated"]["output_dir"]),
        included=included,
        skipped=skipped,
    )
    copy_public_examples(
        root=root,
        output_dir=output_dir,
        source_dir=Path(config["public_safety"]["public_examples_source"]),
        included=included,
        leak_terms=leak_terms,
        skipped=skipped_public_examples,
    )
    copy_aggregate_evidence(root=root, output_dir=output_dir, config=config, included=included)
    write_bundle_readme(output_dir=output_dir, config=config, included=included)
    manifest_path = write_manifest(
        output_dir=output_dir,
        config=config,
        included=included,
        skipped=skipped,
        skipped_public_examples=skipped_public_examples,
    )
    return BundleBuildResult(
        output_dir=output_dir,
        manifest_path=manifest_path,
        included_files=sorted(included),
        skipped_optional_paths=sorted(skipped),
        skipped_public_examples=sorted(skipped_public_examples),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = build_public_release_bundle(config_path=args.config, output_dir=args.out)
    print(f"Wrote {rel(result.output_dir)}")
    print(f"Wrote {rel(result.manifest_path)}")
    print(
        f"included={len(result.included_files)} "
        f"skipped_optional={len(result.skipped_optional_paths)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
