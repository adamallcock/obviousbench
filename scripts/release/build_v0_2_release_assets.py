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
    release = config["release"]
    snapshot = config["snapshot"]
    generated = config["generated"]
    source_docs = config["source_docs"]

    output_dir = (ROOT / generated["output_dir"]).resolve()
    internal_output_dir = (ROOT / generated["internal_output_dir"]).resolve()
    if clean:
        shutil.rmtree(output_dir, ignore_errors=True)
        shutil.rmtree(internal_output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    internal_output_dir.mkdir(parents=True, exist_ok=True)

    summary_csv = ROOT / snapshot["summary_csv"]
    report_summary_path = ROOT / snapshot["report_summary"]
    review_summary_path = ROOT / snapshot["review_summary"]
    rows = read_csv_rows(summary_csv)
    complete = complete_rows(rows)
    incomplete = [row for row in rows if row not in complete]
    total_cost = sum(as_float(row, "estimated_cost_usd") for row in rows)
    report_summary = read_json(report_summary_path)
    review_summary = read_json(review_summary_path)
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
            "attempt_rows": int(report_summary.get("attempt_rows", 0)),
            "scored_attempts": int(
                report_summary.get(
                    "scored_attempt_rows",
                    report_summary.get("attempt_rows", 0),
                )
            ),
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
        "public_safety": config["public_safety"],
        "public_links": config["public_links"],
        "claim_limits": config["claim_limits"],
    }

    written: list[Path] = []

    def write_output(relative_path: str, text: str) -> None:
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
        "snapshot_name": snapshot["name"],
        "primary_metric": snapshot["primary_metric_label"],
        "model_setting_rows": len(rows),
        "complete_model_setting_rows": len(complete),
        "attempt_rows": int(report_summary.get("attempt_rows", 0)),
        "estimated_cost_usd": round(total_cost, 6),
        "public_links": config["public_links"],
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
                        ["Private items", str(snapshot["private_item_count"])],
                        ["Model/config rows", str(len(rows))],
                        ["Complete rows", str(len(complete))],
                        ["Attempts", str(report_summary.get("attempt_rows"))],
                        ["Scored attempts", str(evidence["summary"]["scored_attempts"])],
                        ["Estimated cost", money(total_cost)],
                        ["Primary metric", snapshot["primary_metric_label"]],
                    ],
                ),
                "",
                "## Generated Files",
                "",
                "- `release-metadata.json`",
                "- `github-release-notes.md`",
                "- `huggingface-dataset-card.md`",
                "- `project-page.md`",
                "- `launch-essay-draft.md`",
                "- `background-and-rhetoric.md`",
                "- `social-snippets.md`",
                "- `public-release-checklist.md`",
                "- `provenance.json`",
                "",
                "## Source Evidence",
                "",
                f"- Results memo: `{source_docs['results_memo']}`",
                f"- Evidence packet: `{source_docs['evidence_packet']}`",
                f"- Sanity supplement: `{source_docs['sanity_supplement']}`",
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
                "Status: local prep only. Do not publish until repository, dataset,",
                "project-page, and bundle-audit gates are complete.",
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
                        ["Private held-out items", str(snapshot["private_item_count"])],
                        ["Model/config rows", str(len(rows))],
                        ["Included headline rows", str(len(complete))],
                        ["Attempt rows", str(report_summary.get("attempt_rows"))],
                        ["Scored attempts", str(evidence["summary"]["scored_attempts"])],
                        ["Estimated cost", money(total_cost)],
                    ],
                ),
                "",
                "Rows affected by provider unavailability or route-level blank-output",
                "failures are excluded from headline comparisons rather than treated",
                "as model-quality evidence.",
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
                        ["Private items", str(snapshot["private_item_count"])],
                        ["Model/config rows", str(len(rows))],
                        ["Attempts", str(report_summary.get("attempt_rows"))],
                        ["Primary metric", snapshot["primary_metric_label"]],
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

    write_output(
        "project-page.md",
        "\n".join(
            [
                "# ObviousBench v0.2 Project Page Draft",
                "",
                "ObviousBench catches obvious AI mistakes before users do.",
                "",
                "It asks models questions that look too simple to miss: literal",
                "counting, spelling transforms, ordering, negation, formatting,",
                "arithmetic, word counting, and basic constraint awareness.",
                "",
                "The v0.2 private pass^3 run shows the desired shape. The strongest",
                "models and highest test-time-compute settings can saturate the",
                "benchmark, which is evidence that the questions are solvable rather",
                "than broken. Lower-compute, smaller, or no-thinking rows still fail",
                "often enough to expose the practical risk: a model can look capable",
                "and still make obvious mistakes.",
                "",
                "## Why This Exists",
                "",
                "Modern models can summarize long documents, write code, and operate",
                "tools, yet still stumble on small literal tasks users instantly",
                "recognize. These failures are not always catastrophic, but they are",
                "embarrassing, trust-eroding, and often avoidable with the right",
                "model/configuration tradeoff.",
                "",
                "ObviousBench turns that failure mode into a small, reproducible",
                "preflight check.",
                "",
                "## How Product Teams Should Use It",
                "",
                "- Compare candidate models and thinking settings before launch.",
                "- Track regressions when changing providers, prompts, or routing.",
                "- Inspect failure examples to decide whether a cheap/small model is",
                "  acceptable for a workflow.",
                "- Keep answer correctness separate from format compliance so product",
                "  teams can see both reasoning failures and interface failures.",
                "",
                "## Top Saturated Rows",
                "",
                *model_rows_table(saturated[:8]),
                "",
                "## High Failure-Risk Rows",
                "",
                *model_rows_table(risky[:8]),
                "",
                "## Public Boundary",
                "",
                "The project page can show aggregate private results and public example",
                "questions. It must not show private held-out questions, raw private",
                "outputs, item-level private outcomes, or private review HTML.",
                "",
                "## What Not To Claim",
                "",
                "Do not use ObviousBench as a global ranking, a general intelligence",
                "measure, a human-baseline claim, or a permanent statement about a",
                "provider. It is a frozen reliability snapshot for a deliberately",
                "narrow class of visible mistakes.",
            ]
        ),
    )

    write_output(
        "launch-essay-draft.md",
        "\n".join(
            [
                "# ObviousBench v0.2 Launch Essay Draft",
                "",
                "Large language models can do work that would have sounded impossible",
                "a few years ago. They can summarize thousands of pages, write code,",
                "use tools, and carry a conversation across domains.",
                "",
                "And then, sometimes, they miss something a careful person would catch",
                "immediately: a letter count, a spelling transform, a reversed list,",
                "or the exact format the user asked for.",
                "",
                "That gap is what ObviousBench is for.",
                "",
                "The point is not that simple questions are hard for everyone. The",
                "point is that simple questions are still an excellent way to see",
                "where capability, model size, and test-time compute stop protecting",
                "a system from looking foolish.",
                "",
                "In v0.2, the top end saturates: the strongest configurations can reach",
                "100% non-strict answer pass^3 across the private set. That is good. A",
                "benchmark of obvious tasks should be solvable by sufficiently capable",
                "systems. The useful signal is what happens below that ceiling.",
                "",
                "The lower rows still miss literal spelling, counting, ordering, and",
                "format constraints. The benchmark therefore gives a concrete way to",
                "compare how much obvious-mistake risk remains when you reduce model",
                "size, disable thinking, or lower test-time compute.",
                "",
                "This is the useful product question: how much risk are you accepting",
                "when you choose a cheaper, faster, smaller, or lower-compute route?",
                "Sometimes that tradeoff is worth it. ObviousBench helps make the",
                "tradeoff explicit.",
                "",
                "It is not a shame board. It is not a claim that one visible miss makes",
                "a model bad. It is not a replacement for broad evaluations. It is a",
                "small, deterministic preflight for a class of failures users notice",
                "immediately.",
                "",
                "This draft is not public copy yet. Before launch, replace local paths",
                "with public repository, dataset, and project URLs and rerun the",
                "public-bundle audit.",
            ]
        ),
    )

    write_output(
        "background-and-rhetoric.md",
        "\n".join(
            [
                "# ObviousBench v0.2 Background And Rhetoric",
                "",
                "## Core Positioning",
                "",
                "ObviousBench is about high-visibility mistakes, not exotic",
                "capability. It tests tasks that should feel mundane: count letters,",
                "edit a word, reverse a list, answer yes or no, choose the object that",
                "must be brought to a service.",
                "",
                "The public story should be practical: if an AI system is going to",
                "face users, product teams should know whether it is likely to make",
                "these obvious mistakes under the exact model and thinking setting",
                "they plan to ship.",
                "",
                "## Tone",
                "",
                "- Serious, but not scolding.",
                "- Concrete, not abstract benchmark theater.",
                "- Useful to product and model teams.",
                "- Explicit that top models can solve the benchmark.",
                "- Clear that lower rows reveal tradeoffs, not moral failure.",
                "",
                "## Messages To Reuse",
                "",
                "- Catch obvious AI mistakes before users do.",
                "- Simple tasks are not a full intelligence test, but they are a",
                "  strong trust test.",
                "- A saturatable benchmark can still be useful: the ceiling proves the",
                "  questions are solvable; the spread shows where risk remains.",
                "- Thinking/test-time compute is often an antidote to these mistakes,",
                "  but it has latency and cost tradeoffs.",
                "- ObviousBench separates answer correctness from format compliance.",
                "",
                "## Claims To Avoid",
                "",
                "- Do not say ObviousBench ranks all models globally.",
                "- Do not say humans were measured at 100%.",
                "- Do not publish private prompts or raw private completions.",
                "- Do not over-explain failures as a single mechanistic cause.",
                "- Do not imply provider/route-unavailable rows are model-quality",
                "  failures; exclude them from headline comparisons.",
            ]
        ),
    )

    write_output(
        "social-snippets.md",
        "\n".join(
            [
                "# ObviousBench v0.2 Social Snippets",
                "",
                "Status: draft local copy only.",
                "",
                "1. ObviousBench v0.2 is designed to be saturatable at the top end: the",
                "best model/config rows can reach 100% answer pass^3. The signal is how",
                "quickly that falls apart when models are smaller or thinking is off.",
                "",
                "2. Simple tasks are not trivial for deployment. Literal counting,",
                "ordering, spelling transforms, negation, and format constraints still",
                "separate model families and thinking settings.",
                "",
                "3. The v0.2 public bundle will publish aggregate private results and",
                "public examples, while keeping the private held-out prompts and raw",
                "model outputs private.",
                "",
                "4. This is not a model shame board. It is a preflight check for the",
                "kind of obvious mistake users remember.",
                "",
                "5. The practical question is not only which model is best. It is how",
                "much visible failure risk you accept when you choose a cheaper,",
                "faster, smaller, or lower-thinking configuration.",
            ]
        ),
    )

    write_output(
        "public-release-checklist.md",
        "\n".join(
            [
                "# ObviousBench v0.2 Public Release Checklist",
                "",
                "## Local Gates",
                "",
                "- [x] Final v0.2 private pass^3 evidence selected.",
                "- [x] Aggregate report and review summaries built.",
                "- [x] Public-safe release surfaces generated locally.",
                "- [x] Public bundle script/audit available for v0.2 aggregate release.",
                "- [!] Public examples are currently a filtered safe placeholder;",
                "  materialize a v0.2 public example manifest before final launch",
                "  if the release should include a polished 64-row public split.",
                "",
                "## Public Gates Still Pending",
                "",
                "- [ ] Materialize and audit v0.2 public/dev/reserve split policy,",
                "  or explicitly publish with aggregate-only private results plus",
                "  filtered public examples.",
                "- [ ] Publish or update the public repository target.",
                "- [ ] Publish or update the dataset page with public examples",
                "  and aggregate results.",
                "- [ ] Publish project page URL.",
                "- [ ] Replace local paths with public URLs in release copy.",
                "- [ ] Rerun strict public bundle audit after final URL substitution.",
                "",
                "No public launch copy should be posted before the pending gates are done.",
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
