#!/usr/bin/env python3
"""Build local v0.2 publication-prep surfaces from aggregate final evidence."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "configs/releases/release_v0_2_0.yaml"
PUBLIC_OUTPUT_ALLOWLIST = {
    "README.md",
    "github-release-notes.md",
    "huggingface-dataset-card.md",
    "provenance.json",
    "release-metadata.json",
}


@dataclass(frozen=True)
class ReleaseAssetResult:
    output_dir: Path
    internal_output_dir: Path
    written_files: list[str]


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


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON file is not an object: {path}")
    return payload


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value else 0.0


def as_int(row: dict[str, str], key: str) -> int:
    value = row.get(key, "")
    return int(float(value)) if value else 0


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def money(value: float) -> str:
    return f"${value:.2f}"


def complete_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if str(row.get("complete_for_pass3")).lower() == "true"]


def top_saturated_rows(rows: list[dict[str, str]], *, limit: int = 10) -> list[dict[str, str]]:
    complete = complete_rows(rows)
    saturated = [row for row in complete if as_float(row, "answer_pass3_accuracy") >= 0.9995]
    return sorted(
        saturated,
        key=lambda row: (
            -as_float(row, "strict_pass3_accuracy"),
            as_float(row, "estimated_cost_usd"),
            row.get("provider_model", ""),
            row.get("reasoning_effort", ""),
        ),
    )[:limit]


def high_risk_rows(rows: list[dict[str, str]], *, limit: int = 10) -> list[dict[str, str]]:
    return sorted(
        complete_rows(rows),
        key=lambda row: (
            as_float(row, "answer_pass3_accuracy"),
            as_float(row, "strict_pass3_accuracy"),
            row.get("provider_model", ""),
        ),
    )[:limit]


def cost_outlier_rows(rows: list[dict[str, str]], *, limit: int = 10) -> list[dict[str, str]]:
    return sorted(
        rows,
        key=lambda row: as_float(row, "estimated_cost_usd"),
        reverse=True,
    )[:limit]


def thinking_delta_rows(rows: list[dict[str, str]], *, limit: int = 10) -> list[dict[str, Any]]:
    by_model: dict[str, list[dict[str, str]]] = {}
    for row in complete_rows(rows):
        by_model.setdefault(row.get("provider_model", ""), []).append(row)
    deltas: list[dict[str, Any]] = []
    for model, model_rows in by_model.items():
        if len(model_rows) < 2:
            continue
        low = min(model_rows, key=lambda row: as_float(row, "answer_pass3_accuracy"))
        high = max(model_rows, key=lambda row: as_float(row, "answer_pass3_accuracy"))
        delta = as_float(high, "answer_pass3_accuracy") - as_float(low, "answer_pass3_accuracy")
        if delta <= 0:
            continue
        deltas.append(
            {
                "provider_model": model,
                "rows": len(model_rows),
                "low_effort": low.get("reasoning_effort", ""),
                "low_answer_pass3": as_float(low, "answer_pass3_accuracy"),
                "high_effort": high.get("reasoning_effort", ""),
                "high_answer_pass3": as_float(high, "answer_pass3_accuracy"),
                "delta": delta,
            }
        )
    return sorted(deltas, key=lambda row: row["delta"], reverse=True)[:limit]


def row_for_metadata(row: dict[str, str]) -> dict[str, Any]:
    return {
        "model_entry_id": row.get("model_entry_id"),
        "provider_model": row.get("provider_model"),
        "reasoning_effort": row.get("reasoning_effort"),
        "answer_pass3_accuracy": as_float(row, "answer_pass3_accuracy"),
        "strict_pass3_accuracy": as_float(row, "strict_pass3_accuracy"),
        "complete_for_pass3": str(row.get("complete_for_pass3")).lower() == "true",
        "estimated_cost_usd": as_float(row, "estimated_cost_usd"),
        "reasoning_tokens": as_int(row, "reasoning_tokens"),
        "provider_errors": as_int(row, "provider_errors"),
    }


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    return [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
        *(("| " + " | ".join(row) + " |") for row in rows),
    ]


def generated_notice_block(*, config_path: Path, release: dict[str, Any]) -> list[str]:
    command = (
        "uv run --extra dev python scripts/release/build_v0_2_release_assets.py "
        f"--config {rel(config_path)}"
    )
    return [
        "",
        "## Generated Artifact Notice",
        "",
        f"- Source config: `{rel(config_path)}`",
        f"- Generator: `{command}`",
        f"- Release date: `{release['date']}`",
        f"- Status: `{release['status']}`",
        "- Public/private boundary: excludes private held-out prompts, raw outputs,",
        "  item-level private outcomes, private review HTML, and attempt-level outcomes.",
        "",
    ]


def with_generated_notice(
    text: str,
    *,
    config_path: Path,
    release: dict[str, Any],
) -> str:
    if "## Generated Artifact Notice" in text:
        return text
    lines = text.rstrip().splitlines()
    notice = generated_notice_block(config_path=config_path, release=release)
    if lines and lines[0] == "---":
        for index in range(1, len(lines)):
            if lines[index] == "---":
                return "\n".join([*lines[: index + 1], *notice, *lines[index + 1 :]])
    if lines and lines[0].startswith("# "):
        return "\n".join([lines[0], *notice, *lines[1:]])
    return "\n".join([*notice, *lines])


def model_rows_table(rows: list[dict[str, str]]) -> list[str]:
    return markdown_table(
        ["Model", "Effort", "Answer pass^3", "Strict pass^3", "Cost", "Reasoning tok"],
        [
            [
                row.get("provider_model", ""),
                row.get("reasoning_effort", ""),
                pct(as_float(row, "answer_pass3_accuracy")),
                pct(as_float(row, "strict_pass3_accuracy")),
                money(as_float(row, "estimated_cost_usd")),
                str(as_int(row, "reasoning_tokens")),
            ]
            for row in rows
        ],
    )


def assert_public_safe_config(config: dict[str, Any]) -> None:
    safety = config.get("public_safety") or {}
    unsafe_flags = [
        "private_prompts_in_public_bundle",
        "private_raw_logs_in_public_bundle",
        "private_row_level_outcomes_in_public_bundle",
        "private_review_html_in_public_bundle",
    ]
    enabled = [flag for flag in unsafe_flags if safety.get(flag) is not False]
    if enabled:
        raise ValueError(f"Public-safety config must set these flags false: {enabled}")


def build_release_assets(
    *,
    config_path: Path = DEFAULT_CONFIG,
    clean: bool = True,
) -> ReleaseAssetResult:
    config = read_yaml(config_path)
    assert_public_safe_config(config)
    release_config = config.get("release") or {}
    release = {
        "date": str(release_config.get("date", "unknown")),
        "id": str(release_config.get("id", "obviousbench-v0.2.0-public-aggregate")),
        "publication_intent": release_config.get(
            "publication_intent", "non_arxiv_public_release"
        ),
        "status": str(release_config.get("status", "local-publication-prep")),
        "version": str(release_config.get("version", "0.2.0")),
    }
    snapshot = config["snapshot"]
    generated = config.get("generated") or {}
    source_docs = config.get("source_docs") or {}

    output_dir = (ROOT / generated["output_dir"]).resolve()
    internal_output_dir = (
        ROOT / generated.get("internal_output_dir", "docs/internal/release/v0_2/generated")
    ).resolve()
    if clean:
        shutil.rmtree(output_dir, ignore_errors=True)
        shutil.rmtree(internal_output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    internal_output_dir.mkdir(parents=True, exist_ok=True)

    summary_csv = ROOT / snapshot["summary_csv"]
    rows = read_csv_rows(summary_csv)
    complete = complete_rows(rows)
    incomplete = [row for row in rows if row not in complete]
    total_cost = sum(as_float(row, "estimated_cost_usd") for row in rows)
    report_summary_path = snapshot.get("report_summary")
    review_summary_path = snapshot.get("review_summary")
    report_summary = (
        read_json(ROOT / report_summary_path)
        if isinstance(report_summary_path, str) and (ROOT / report_summary_path).exists()
        else {}
    )
    review_summary = (
        read_json(ROOT / review_summary_path)
        if isinstance(review_summary_path, str) and (ROOT / review_summary_path).exists()
        else {}
    )
    attempt_rows = int(
        snapshot.get(
            "attempt_count",
            report_summary.get("attempt_rows", report_summary.get("scored_attempt_rows", 0)),
        )
    )
    scored_attempts = int(
        snapshot.get(
            "scored_attempt_count",
            report_summary.get("scored_attempt_rows", report_summary.get("attempt_rows", 0)),
        )
    )
    private_item_count = int(snapshot.get("private_item_count", 144))
    primary_metric_label = snapshot.get("primary_metric_label", "non-strict answer pass^3")
    snapshot_name = snapshot.get("name", "v0.2 public aggregate")
    saturated = top_saturated_rows(rows, limit=10)
    risky = high_risk_rows(rows, limit=10)
    cost_outliers = cost_outlier_rows(rows, limit=10)
    deltas = thinking_delta_rows(rows, limit=10)

    evidence = {
        "release": release,
        "snapshot": snapshot,
        "source_docs": source_docs,
        "summary": {
            "model_setting_rows": len(rows),
            "complete_model_setting_rows": len(complete),
            "incomplete_model_setting_rows": len(incomplete),
            "attempt_rows": attempt_rows,
            "scored_attempts": scored_attempts,
            "provider_error_attempts": int(
                report_summary.get("provider_error_attempt_rows", 0)
            ),
            "manual_adjusted_attempts": int(
                report_summary.get("manual_adjusted_attempt_rows", 0)
            ),
            "blank_provider_fault_attempts": int(
                report_summary.get("blank_provider_fault_attempt_rows", 0)
            ),
            "estimated_cost_usd": total_cost,
            "review_data_mode": review_summary.get("question_failure_review_data_mode"),
            "raw_hydrated_attempts": review_summary.get("raw_hydrated_attempts"),
        },
        "top_saturated_rows": [row_for_metadata(row) for row in saturated],
        "high_failure_risk_rows": [row_for_metadata(row) for row in risky],
        "cost_outlier_rows": [row_for_metadata(row) for row in cost_outliers],
        "thinking_depth_deltas": deltas,
        "public_safety": config.get("public_safety") or {},
        "public_links": config.get("public_links") or {},
        "claim_limits": config.get("claim_limits") or {},
    }

    written: list[Path] = []

    def write_output(relative_path: str, text: str) -> None:
        if relative_path not in PUBLIC_OUTPUT_ALLOWLIST:
            return
        path = output_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".md":
            text = with_generated_notice(text, config_path=config_path, release=release)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        written.append(path)

    def write_internal(relative_path: str, text: str) -> None:
        path = internal_output_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        written.append(path)

    metadata = {
        "release_id": release["id"],
        "version": release["version"],
        "status": release["status"],
        "publication_intent": release["publication_intent"],
        "generated_on": release["date"],
        "snapshot_name": snapshot_name,
        "primary_metric": primary_metric_label,
        "model_setting_rows": len(rows),
        "complete_model_setting_rows": len(complete),
        "attempt_rows": attempt_rows,
        "estimated_cost_usd": round(snapshot.get("estimated_cost_usd", total_cost), 6),
        "public_links": config.get("public_links") or {},
        "source_config": rel(config_path),
    }
    write_output("release-metadata.json", json.dumps(metadata, indent=2, sort_keys=True))
    write_output(
        "provenance.json",
        json.dumps(
            {
                "config": rel(config_path),
                "generator": "scripts/release/build_v0_2_release_assets.py",
                "public_boundary": {
                    "private_prompts_included": False,
                    "private_raw_outputs_included": False,
                    "private_item_level_outcomes_included": False,
                    "private_review_html_included": False,
                    "private_attempt_level_outcomes_included": False,
                },
                "release_metadata": rel(output_dir / "release-metadata.json"),
                "source_docs": source_docs,
                "status": release["status"],
            },
            indent=2,
            sort_keys=True,
        ),
    )
    write_internal("release-evidence.json", json.dumps(evidence, indent=2, sort_keys=True))

    write_output(
        "README.md",
        "\n".join(
            [
                "---",
                f"title: ObviousBench v{release['version']} Local Release Surfaces",
                f"date: {release['date']}",
                "type: release",
                "status: local-prep",
                "---",
                "",
                f"# ObviousBench v{release['version']} Local Release Surfaces",
                "",
                "These files are local publication-prep artifacts. They do not publish",
                "anything and they intentionally exclude private held-out prompts, raw",
                "outputs, item-level private outcomes, and private review HTML.",
                "",
                "## Snapshot",
                "",
                *markdown_table(
                    ["Field", "Value"],
                    [
                        ["Private items", str(private_item_count)],
                        ["Model/config rows", str(len(rows))],
                        ["Complete rows", str(len(complete))],
                        ["Attempts", str(attempt_rows)],
                        ["Scored attempts", str(scored_attempts)],
                        ["Estimated cost", money(total_cost)],
                        ["Primary metric", primary_metric_label],
                    ],
                ),
                "",
                "Canonical public launch site:",
                "[https://obviousbench.com](https://obviousbench.com)",
                "",
                "## Generated Files",
                "",
                "- `README.md`",
                "- `release-metadata.json`",
                "- `github-release-notes.md`",
                "- `huggingface-dataset-card.md`",
                "- `provenance.json`",
                "",
                "The launch-site narrative and interactive charts live at",
                "[https://obviousbench.com](https://obviousbench.com). This repository",
                "keeps the public-safe source data, configs, aggregate CSVs, and",
                "reproducibility materials rather than duplicating the deployable website",
                "source.",
                "",
                "## Source Evidence",
                "",
                *(
                    [f"- Results memo: `{source_docs['results_memo']}`"]
                    if source_docs.get("results_memo")
                    else []
                ),
                *(
                    [f"- Evidence packet: `{source_docs['evidence_packet']}`"]
                    if source_docs.get("evidence_packet")
                    else []
                ),
                *(
                    [f"- Sanity supplement: `{source_docs['sanity_supplement']}`"]
                    if source_docs.get("sanity_supplement")
                    else []
                ),
                *(
                    [f"- Split inventory: `{source_docs['split_inventory']}`"]
                    if source_docs.get("split_inventory")
                    else []
                ),
                "- Aggregate report: copied into the public bundle under",
                "  `reports/v0_2/aggregate/report.md` after bundle build.",
            ]
        ),
    )

    write_output(
        "github-release-notes.md",
        "\n".join(
            [
                "# ObviousBench v0.2.0 Draft Release Notes",
                "",
                "Status: local prep only. Do not publish until repository visibility,",
                "dataset publication, website link checks, and bundle-audit gates are",
                "complete.",
                "",
                "## What Is ObviousBench?",
                "",
                "ObviousBench is a compact reliability benchmark for mistakes users",
                "notice immediately: letter counts, spelling transforms, small",
                "arithmetic, ordering, negation, format compliance, word counting,",
                "and simple constraint awareness.",
                "",
                "The benchmark is intentionally narrow. It is not a general",
                "intelligence score and it is not a shame board. It is a preflight",
                "surface for checking whether a model/configuration still makes",
                "obvious literal mistakes before those mistakes reach users.",
                "",
                "## v0.2 Headline",
                "",
                "The v0.2 private pass^3 snapshot has the desired shape: top",
                "model/config rows saturate or near-saturate the benchmark, while",
                "smaller, no-thinking, or lower-test-time-compute rows still fail",
                "visibly. That means the tasks are solvable by sufficiently capable",
                "systems, and still useful for measuring obvious-mistake risk below",
                "the top end.",
                "",
                "## Evidence Shape",
                "",
                *markdown_table(
                    ["Metric", "Value"],
                    [
                        ["Private held-out items", str(private_item_count)],
                        ["Model/config rows", str(len(rows))],
                        ["Included headline rows", str(len(complete))],
                        ["Attempt rows", str(attempt_rows)],
                        ["Scored attempts", str(scored_attempts)],
                        ["Estimated cost", money(total_cost)],
                    ],
                ),
                "",
                "Rows affected by provider unavailability or route-level blank-output",
                "failures are excluded from headline comparisons rather than treated",
                "as model-quality evidence.",
                "",
                "The canonical public narrative and interactive charts are on",
                "[obviousbench.com](https://obviousbench.com). This repository is the",
                "public source/data companion for those results.",
                "",
                "## What Changed Since v0.1",
                "",
                "- v0.2 rebalances toward subfamilies that still separate modern",
                "  models.",
                "- Saturated low-signal forms are reduced or removed.",
                "- Ambiguous wording found during private review was corrected before",
                "  the final run.",
                "- The primary headline metric is non-strict answer pass^3; strict",
                "  and format correctness remain diagnostics.",
                "",
                "## How To Read The Results",
                "",
                "A high score means the model/configuration reliably answers these",
                "simple tasks under the frozen snapshot. A low score does not mean",
                "the model is generally bad; it means this configuration is more",
                "likely to make visible obvious mistakes unless product safeguards,",
                "more capable models, or more test-time compute are used.",
                "",
                "## Caveats",
                "",
                "- Do not claim a global model ranking.",
                "- Do not claim measured human accuracy or response time.",
                "- Do not publish private held-out prompts, raw outputs, item-level",
                "  private outcomes, or private review HTML.",
                "- Treat scores as a dated frozen snapshot, not permanent provider",
                "  behavior.",
            ]
        ),
    )

    write_output(
        "huggingface-dataset-card.md",
        "\n".join(
            [
                "---",
                "language: en",
                "license: cc-by-4.0",
                "task_categories:",
                "- text-generation",
                "pretty_name: ObviousBench v0.2",
                "---",
                "",
                "# ObviousBench v0.2",
                "",
                "This is draft dataset-card copy for the future public release.",
                "The intended public bundle contains documentation, public examples,",
                "and aggregate v0.2 private benchmark results. It does not include",
                "private held-out prompts, private raw completions, private review",
                "HTML, or private item-level outcome rows.",
                "",
                "## Intended Use",
                "",
                "ObviousBench measures whether models miss simple literal tasks that",
                "humans normally regard as obvious, and how those failures change with",
                "model size and test-time compute.",
                "",
                "Appropriate uses include model-selection preflight, regression",
                "testing, prompt/interface QA, and inspecting how much obvious-mistake",
                "risk remains when thinking depth or model size is reduced.",
                "",
                "Inappropriate uses include global model ranking, broad intelligence",
                "claims, or treating one visible failure as proof that a model is",
                "generally unsuitable.",
                "",
                "## Final Private Snapshot",
                "",
                *markdown_table(
                    ["Metric", "Value"],
                    [
                        ["Private items", str(private_item_count)],
                        ["Model/config rows", str(len(rows))],
                        ["Attempts", str(attempt_rows)],
                        ["Primary metric", primary_metric_label],
                        ["Estimated cost", money(total_cost)],
                    ],
                ),
                "",
                "## Public-Safety Boundary",
                "",
                "The private evaluation set remains held out. Public materials should",
                "use only public examples and aggregate private results.",
                "",
                "## Scoring",
                "",
                "The benchmark uses deterministic Python scorers. The headline metric",
                "for v0.2 is non-strict answer pass^3: all three attempts for an",
                "item/model/config must be answer-correct. Strict and format",
                "correctness remain available as diagnostics.",
            ]
        ),
    )

    return ReleaseAssetResult(
        output_dir=output_dir,
        internal_output_dir=internal_output_dir,
        written_files=sorted(rel(path) for path in written),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--no-clean", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = build_release_assets(config_path=args.config, clean=not args.no_clean)
    print(f"Wrote {rel(result.output_dir)}")
    print(f"Wrote {rel(result.internal_output_dir)}")
    print(f"files={len(result.written_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
