"""Generate cheap LaTeX table assets for the ObviousBench paper draft."""

from __future__ import annotations

import csv
import json
import math
import subprocess
import tempfile
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from statistics import median

import yaml

from obviousbench.analysis.statistics import wilson_interval
from obviousbench.research.arxiv_readiness import (
    ArxivReadinessInputs,
    ReadinessProfile,
    audit_arxiv_readiness,
)
from obviousbench.scorers.gold import load_gold_examples

REPO_ROOT = Path(__file__).resolve().parents[2]
RELEASE_THEME_CONFIG = REPO_ROOT / "configs/release_theme_v0_1_0.yaml"


def _load_release_theme_colors() -> dict[str, str]:
    if not RELEASE_THEME_CONFIG.exists():
        return {}
    loaded = yaml.safe_load(RELEASE_THEME_CONFIG.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        return {}
    colors = loaded.get("colors")
    return colors if isinstance(colors, dict) else {}


def _theme_rgb(
    colors: dict[str, str],
    key: str,
    fallback: tuple[float, float, float],
) -> tuple[float, float, float]:
    value = colors.get(key)
    if not isinstance(value, str) or not value.startswith("#") or len(value) != 7:
        return fallback
    try:
        red = int(value[1:3], 16) / 255
        green = int(value[3:5], 16) / 255
        blue = int(value[5:7], 16) / 255
    except ValueError:
        return fallback
    return (red, green, blue)


THEME_COLORS = _load_release_theme_colors()
COLOR_BLUE = _theme_rgb(THEME_COLORS, "accent", (0.10, 0.29, 0.55))
COLOR_BLUE_LIGHT = (0.87, 0.92, 0.97)
COLOR_ORANGE = _theme_rgb(THEME_COLORS, "accent_warm", (0.87, 0.42, 0.13))
COLOR_GRID = _theme_rgb(THEME_COLORS, "grid", (0.88, 0.88, 0.88))
COLOR_AXIS = _theme_rgb(THEME_COLORS, "foreground", (0.20, 0.20, 0.20))
COLOR_TEXT = _theme_rgb(THEME_COLORS, "foreground", (0.08, 0.08, 0.08))
COLOR_TEXT_MUTED = _theme_rgb(THEME_COLORS, "muted", (0.28, 0.28, 0.28))
COLOR_EMPTY = (0.92, 0.92, 0.92)
FIGURE_WIDTH = 468

FAMILY_LABELS = {
    "arithmetic": "Arithmetic",
    "character_count": "Char count",
    "constraint_awareness": "Constraints",
    "format_compliance": "Format",
    "negation": "Negation",
    "ordering": "Ordering",
    "spelling_transform": "Spelling",
    "simple_arithmetic": "Arithmetic",
    "table_lookup": "Tables",
    "temporal_order": "Temporal",
    "unit_conversion": "Units",
    "word_count": "Word count",
}

FAMILY_SHORT_LABELS = {
    "arithmetic": "Arith.",
    "character_count": "Char",
    "constraint_awareness": "Constr.",
    "format_compliance": "Format",
    "negation": "Neg.",
    "ordering": "Order",
    "spelling_transform": "Spell",
    "simple_arithmetic": "Arith.",
    "table_lookup": "Tables",
    "temporal_order": "Temporal",
    "unit_conversion": "Units",
    "word_count": "Words",
}

SUBFAMILY_LABELS = {
    "alphabetical_sort": "Alphabetical sort",
    "comma_list_count": "Comma-list count",
    "exact_json_schema": "Exact JSON schema",
    "json_field": "JSON field",
    "not_choice": "Not-choice",
    "numeric_comparison": "Numeric comparison",
    "numeric_sort": "Numeric sort",
    "object_must_be_present": "Object must be present",
    "remove_letter": "Remove letter",
    "replace_letter": "Replace letter",
    "single_letter_count": "Single-letter count",
    "small_integer_arithmetic": "Small integer arithmetic",
    "unit_conversion_and_small_calc": "Unit conversion and small calc",
    "without_constraint": "Without constraint",
}

REASONING_DEPTHS = {"none", "minimal", "low", "medium", "high", "auto"}


@dataclass(frozen=True)
class PaperAssetInputs:
    manifest_path: Path
    dataset_paths: Sequence[Path]
    item_cards_dir: Path
    scorer_gold_dir: Path
    human_baseline_path: Path | None
    output_dir: Path
    figures_dir: Path | None = None
    model_panel_path: Path | None = None
    final_results_dir: Path | None = None
    placeholder_results_dir: Path | None = None
    wrong_answer_review_path: Path | None = None
    figure_renderer: str = "pdf"
    min_gold_examples_per_scorer: int = 20
    readiness_profile: ReadinessProfile = "preprint"


@dataclass(frozen=True)
class PaperAssetOutputs:
    dataset_composition: Path
    scorer_gold_coverage: Path
    readiness_gates: Path
    human_baseline_summary: Path
    main_results: Path
    family_results: Path
    thinking_group_results: Path
    model_family_results: Path
    failure_type_summary: Path
    provider_exclusions: Path
    figures: tuple[Path, ...]
    model_panel: Path | None = None


def build_paper_assets(inputs: PaperAssetInputs) -> PaperAssetOutputs:
    """Build deterministic, inexpensive `.tex` tables for the paper scaffold."""
    inputs.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows = _load_manifest_rows(inputs.manifest_path)
    readiness = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=inputs.dataset_paths,
            item_cards_dir=inputs.item_cards_dir,
            scorer_gold_dir=inputs.scorer_gold_dir,
            human_baseline_path=inputs.human_baseline_path,
            paper_manifest_path=inputs.manifest_path,
            min_gold_examples_per_scorer=inputs.min_gold_examples_per_scorer,
            manifest_scope=True,
            readiness_profile=inputs.readiness_profile,
        )
    )

    dataset_composition = inputs.output_dir / "dataset_composition.tex"
    scorer_gold_coverage = inputs.output_dir / "scorer_gold_coverage.tex"
    readiness_gates = inputs.output_dir / "readiness_gates.tex"
    human_baseline_summary = inputs.output_dir / "human_baseline_summary.tex"
    main_results = inputs.output_dir / "main_results.tex"
    family_results = inputs.output_dir / "family_results.tex"
    thinking_group_results = inputs.output_dir / "thinking_group_results.tex"
    model_family_results = inputs.output_dir / "model_family_results.tex"
    failure_type_summary = inputs.output_dir / "failure_type_summary.tex"
    provider_exclusions = inputs.output_dir / "provider_exclusions.tex"
    figures_dir = inputs.figures_dir or inputs.output_dir.parent / "figures"
    model_panel = (
        inputs.output_dir / "model_panel.tex"
        if inputs.model_panel_path is not None and inputs.model_panel_path.exists()
        else None
    )

    dataset_composition.write_text(
        _dataset_composition_table(manifest_rows),
        encoding="utf-8",
    )
    scorer_gold_coverage.write_text(
        _scorer_gold_coverage_table(inputs.scorer_gold_dir),
        encoding="utf-8",
    )
    readiness_gates.write_text(
        _readiness_gates_table(readiness),
        encoding="utf-8",
    )
    human_baseline_summary.write_text(
        _human_baseline_summary_table(manifest_rows, inputs.human_baseline_path),
        encoding="utf-8",
    )
    if model_panel is not None and inputs.model_panel_path is not None:
        model_panel.write_text(
            _model_panel_table(inputs.model_panel_path),
            encoding="utf-8",
        )
    result_bundle = _load_result_bundle(
        final_results_dir=inputs.final_results_dir,
        placeholder_results_dir=inputs.placeholder_results_dir,
        wrong_answer_review_path=inputs.wrong_answer_review_path,
    )
    main_results.write_text(
        _main_results_table(
            result_bundle.comparison_rows,
            result_bundle.source_label,
            is_placeholder=result_bundle.is_placeholder,
        ),
        encoding="utf-8",
    )
    family_results.write_text(
        _family_results_table(
            result_bundle.family_rows,
            result_bundle.source_label,
            is_placeholder=result_bundle.is_placeholder,
        ),
        encoding="utf-8",
    )
    thinking_group_results.write_text(
        _group_results_table(
            result_bundle.comparison_rows,
            result_bundle.source_label,
            group_key="thinking_group",
            group_title="Thinking mode",
            is_placeholder=result_bundle.is_placeholder,
        ),
        encoding="utf-8",
    )
    model_family_results.write_text(
        _group_results_table(
            result_bundle.comparison_rows,
            result_bundle.source_label,
            group_key="model_family",
            group_title="Model family",
            is_placeholder=result_bundle.is_placeholder,
        ),
        encoding="utf-8",
    )
    failure_type_summary.write_text(
        _failure_type_summary_table(
            result_bundle,
        ),
        encoding="utf-8",
    )
    provider_exclusions.write_text(
        _provider_exclusions_table(
            result_bundle.comparison_rows,
            result_bundle.source_label,
            is_placeholder=result_bundle.is_placeholder,
        ),
        encoding="utf-8",
    )
    figures = _write_result_figures(
        figures_dir,
        result_bundle=result_bundle,
        figure_renderer=inputs.figure_renderer,
    )

    return PaperAssetOutputs(
        dataset_composition=dataset_composition,
        scorer_gold_coverage=scorer_gold_coverage,
        readiness_gates=readiness_gates,
        human_baseline_summary=human_baseline_summary,
        main_results=main_results,
        family_results=family_results,
        thinking_group_results=thinking_group_results,
        model_family_results=model_family_results,
        failure_type_summary=failure_type_summary,
        provider_exclusions=provider_exclusions,
        figures=figures,
        model_panel=model_panel,
    )


def _load_manifest_rows(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _dataset_composition_table(rows: Sequence[dict[str, object]]) -> str:
    family_counts = Counter(str(row.get("family", "unknown")) for row in rows)
    subfamily_counts = Counter(
        (
            str(row.get("family", "unknown")),
            str(row.get("subfamily", "unknown")),
        )
        for row in rows
    )
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\begin{tabular}{llr}",
        "\\toprule",
        "Family & Subfamily & Items \\\\",
        "\\midrule",
    ]
    for (family, subfamily), count in sorted(subfamily_counts.items()):
        lines.append(
            f"{_latex_escape(_family_label(family))} & "
            f"{_latex_escape(_subfamily_label(subfamily))} & {count} \\\\"
        )
    lines.extend(
        [
            "\\midrule",
            f"\\multicolumn{{2}}{{r}}{{Total}} & {sum(family_counts.values())} \\\\",
            "\\bottomrule",
            "\\end{tabular}",
            "",
        ]
    )
    return "\n".join(lines)


def _scorer_gold_coverage_table(scorer_gold_dir: Path) -> str:
    examples = load_gold_examples(sorted(scorer_gold_dir.glob("*.yaml")))
    counts = Counter(example.scorer for example in examples)
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\begin{tabular}{lr}",
        "\\toprule",
        "Scorer & Gold examples \\\\",
        "\\midrule",
    ]
    for scorer, count in sorted(counts.items()):
        lines.append(f"{_latex_escape(scorer)} & {count} \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(lines)


def _readiness_gates_table(readiness) -> str:
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\begin{tabularx}{\\linewidth}{llX}",
        "\\toprule",
        "Gate & Status & Summary \\\\",
        "\\midrule",
    ]
    for gate in readiness.gates:
        lines.append(
            f"{_latex_escape(gate.name)} & {gate.status.upper()} & "
            f"{_latex_escape(gate.message)} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabularx}", ""])
    return "\n".join(lines)


def _human_baseline_summary_table(
    manifest_rows: Sequence[dict[str, object]],
    human_baseline_path: Path | None,
) -> str:
    family_by_item_id = {
        str(row.get("item_id")): str(row.get("family", "unknown"))
        for row in manifest_rows
        if row.get("item_id")
    }
    rows = _load_human_baseline_rows(human_baseline_path, family_by_item_id)
    if not rows:
        return "\n".join(
            [
                "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
                "\\begin{tabular}{l}",
                "\\toprule",
                "Status \\\\",
                "\\midrule",
                "Measured human baseline deferred for fast preprint \\\\",
                "\\bottomrule",
                "\\end{tabular}",
                "",
            ]
        )

    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["family"]), []).append(row)

    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\begin{tabular}{lrrrrr}",
        "\\toprule",
        "Family & Items & Participants & Responses & Accuracy & Median seconds \\\\",
        "\\midrule",
    ]
    for family, family_rows in sorted(grouped.items()):
        item_count = len({str(row["item_id"]) for row in family_rows})
        participant_count = len({str(row["participant_id"]) for row in family_rows})
        response_count = len(family_rows)
        correct_count = sum(1 for row in family_rows if row["correct"])
        accuracy = 100.0 * correct_count / response_count
        median_seconds = median(float(row["seconds"]) for row in family_rows)
        lines.append(
            f"{_latex_escape(family)} & {item_count} & {participant_count} & "
            f"{response_count} & {accuracy:.1f}\\% & {median_seconds:.2f} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(lines)


def _load_human_baseline_rows(
    path: Path | None,
    family_by_item_id: dict[str, str],
) -> list[dict[str, object]]:
    if path is None or not path.exists() or path.stat().st_size == 0:
        return []
    rows: list[dict[str, object]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            item_id = (row.get("item_id") or "").strip()
            if item_id not in family_by_item_id:
                continue
            correct = (row.get("correct") or "").strip().lower()
            seconds = (row.get("seconds") or "").strip()
            try:
                parsed_seconds = float(seconds)
            except ValueError:
                continue
            rows.append(
                {
                    "item_id": item_id,
                    "participant_id": (row.get("participant_id") or "").strip(),
                    "family": family_by_item_id[item_id],
                    "seconds": parsed_seconds,
                    "correct": correct in {"true", "1"},
                }
            )
    return rows


def _model_panel_table(model_panel_path: Path) -> str:
    if model_panel_path.suffix.lower() == ".csv":
        return _model_manifest_summary_table(model_panel_path)
    payload = yaml.safe_load(model_panel_path.read_text(encoding="utf-8")) or {}
    entries = payload.get("entries") or []
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\footnotesize",
        "\\begin{tabularx}{\\linewidth}{@{}p{0.25\\linewidth}p{0.10\\linewidth}Xp{0.18\\linewidth}@{}}",
        "\\toprule",
        "Model & Route & Inspect model & Status \\\\",
        "\\midrule",
    ]
    for entry in entries:
        settings = _model_settings_summary(entry)
        status = f"{entry.get('run_status', 'planned')}; {settings}"
        lines.append(
            f"{_latex_escape(entry.get('label', 'unknown'))} & "
            f"{_latex_escape(entry.get('provider_route', 'unknown'))} & "
            f"{_latex_path(entry.get('inspect_model', 'unknown'))} & "
            f"{_latex_escape(status)} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabularx}", "\\normalsize", ""])
    return "\n".join(lines)


def _model_manifest_summary_table(manifest_path: Path) -> str:
    rows = _read_csv(manifest_path)
    unique_models = {row.get("model", "") for row in rows if row.get("model")}
    provider_counts = Counter(_provider_route_from_model(row.get("model", "")) for row in rows)
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\footnotesize",
        "\\begin{tabularx}{\\linewidth}{@{}Xrr@{}}",
        "\\toprule",
        "Route & Settings & Unique model ids \\\\",
        "\\midrule",
    ]
    for route, count in sorted(provider_counts.items()):
        route_unique = {
            row.get("model", "")
            for row in rows
            if row.get("model") and _provider_route_from_model(row.get("model", "")) == route
        }
        lines.append(
            f"{_latex_escape(route)} & {count} & {len(route_unique)} \\\\"
        )
    lines.extend(
        [
            "\\midrule",
            f"Total & {len(rows)} & {len(unique_models)} \\\\",
            "\\bottomrule",
            "\\end{tabularx}",
            "\\normalsize",
            "",
        ]
    )
    return "\n".join(lines)


def _provider_route_from_model(model: str) -> str:
    if "/" not in model:
        return "unknown"
    route = model.split("/", 1)[0]
    route_map = {
        "anthropic": "Anthropic direct",
        "google": "Google direct",
        "grok": "xAI direct",
        "openai": "OpenAI direct",
        "openrouter": "OpenRouter",
    }
    return route_map.get(route, route)


def _model_settings_summary(entry: dict[str, object]) -> str:
    temperature = entry.get("temperature")
    max_tokens = entry.get("max_tokens")
    reasoning_effort = entry.get("reasoning_effort")
    reasoning_summary = entry.get("reasoning_summary")
    parts = []
    if temperature is not None:
        parts.append(f"temp={temperature}")
    if max_tokens is not None:
        parts.append(f"max_tokens={max_tokens}")
    if reasoning_effort is not None:
        parts.append(f"reasoning={reasoning_effort}")
    if reasoning_summary is not None:
        parts.append(f"summary={reasoning_summary}")
    return ", ".join(parts) if parts else "settings pending"


def _latex_path(value: object) -> str:
    return "\\path{" + str(value).replace("}", "") + "}"


@dataclass(frozen=True)
class ResultBundle:
    comparison_rows: tuple[dict[str, str], ...]
    family_rows: tuple[dict[str, str], ...]
    wrong_answer_rows: tuple[dict[str, str], ...]
    source_label: str
    is_placeholder: bool

    @property
    def has_results(self) -> bool:
        return bool(self.comparison_rows)


def _load_result_bundle(
    *,
    final_results_dir: Path | None,
    placeholder_results_dir: Path | None,
    wrong_answer_review_path: Path | None,
) -> ResultBundle:
    if final_results_dir is not None:
        comparison_rows, family_rows = _read_result_dir(
            final_results_dir,
            comparison_names=("comparison.csv", "leaderboard.csv", "model-comparison.csv"),
            family_names=("family_comparison.csv", "family-comparison.csv", "family-heatmap.csv"),
        )
        if comparison_rows:
            wrong_answer_rows = (
                _read_csv(wrong_answer_review_path)
                if wrong_answer_review_path is not None
                and wrong_answer_review_path.exists()
                else []
            )
            return ResultBundle(
                comparison_rows=tuple(
                    _disambiguate_duplicate_labels(
                        _normalize_comparison_rows(comparison_rows)
                    )
                ),
                family_rows=tuple(
                    _normalize_family_rows(
                        family_rows,
                        label_overrides=_duplicate_label_overrides(comparison_rows),
                    )
                ),
                wrong_answer_rows=tuple(wrong_answer_rows),
                source_label=_final_result_source_label(final_results_dir),
                is_placeholder=False,
            )

    if placeholder_results_dir is not None:
        comparison_rows, family_rows = _read_result_dir(
            placeholder_results_dir,
            comparison_names=("model-comparison.csv", "leaderboard.csv", "comparison.csv"),
            family_names=("family-comparison.csv", "family-heatmap.csv", "family_comparison.csv"),
        )
        if comparison_rows:
            return ResultBundle(
                comparison_rows=tuple(
                    _disambiguate_duplicate_labels(
                        _normalize_comparison_rows(comparison_rows)
                    )
                ),
                family_rows=tuple(
                    _normalize_family_rows(
                        family_rows,
                        label_overrides=_duplicate_label_overrides(comparison_rows),
                    )
                ),
                wrong_answer_rows=(),
                source_label="draft proof-point placeholder",
                is_placeholder=True,
            )

    return ResultBundle((), (), (), "no result source", is_placeholder=True)


def _final_result_source_label(final_results_dir: Path) -> str:
    parent = final_results_dir.parent.name
    if "paper-v1-combined-234-overline-attempt-scored-20260602" in parent:
        return (
            "paper_v1 combined 234-model-setting evidence run, "
            "attempt-scored on 2026-06-02"
        )
    return f"paper evidence run at {final_results_dir}"


def _read_result_dir(
    path: Path,
    *,
    comparison_names: Sequence[str],
    family_names: Sequence[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    comparison_rows: list[dict[str, str]] = []
    family_rows: list[dict[str, str]] = []
    for name in comparison_names:
        candidate = path / name
        if candidate.exists():
            comparison_rows = _read_csv(candidate)
            break
    for name in family_names:
        candidate = path / name
        if candidate.exists():
            family_rows = _read_csv(candidate)
            break
    return comparison_rows, family_rows


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _normalize_comparison_rows(rows: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for row in rows:
        scored = _first(row, "scored_samples", "samples", "total_samples")
        scored_count = _int_cell(scored)
        strict = _metric_fraction(row, "strict_accuracy", "strict_accuracy_pct", "accuracy_pct")
        answer = _metric_fraction(row, "answer_accuracy", "answer_accuracy_pct", "accuracy_pct")
        fmt = _metric_fraction(row, "format_accuracy", "format_accuracy_pct", "accuracy_pct")
        strict_correct = _correct_count(
            row,
            ("strict_correct", "correct"),
            strict,
            scored_count,
        )
        answer_correct = _correct_count(
            row,
            ("answer_correct", "correct"),
            answer,
            scored_count,
        )
        format_correct = _correct_count(
            row,
            ("format_correct",),
            fmt,
            scored_count,
        )
        has_answer_ci = bool(answer_correct and scored_count)
        answer_ci_low, answer_ci_high = (
            wilson_interval(_int_cell(answer_correct), scored_count)
            if has_answer_ci
            else (None, None)
        )
        cost = _first(row, "estimated_cost_usd", "cost_usd")
        tokens = _first(row, "total_tokens")
        reasoning_tokens = _first(row, "reasoning_tokens")
        output_tokens = _first(row, "output_tokens")
        raw_label = _first(row, "label", "model") or "unknown"
        reasoning_effort = _inferred_reasoning_effort(row)
        cost_per_correct = _first(row, "cost_per_correct_usd")
        if not cost_per_correct and cost and answer_correct:
            correct = _float_cell(answer_correct)
            if correct:
                cost_per_correct = f"{_float_cell(cost) / correct:.8f}"
        normalized.append(
            {
                "raw_label": raw_label,
                "label": _display_model_label(row),
                "model": _first(row, "model") or "unknown",
                "summary_dir": _first(row, "summary_dir"),
                "scored_samples": scored,
                "answer_correct": answer_correct,
                "format_correct": format_correct,
                "strict_correct": strict_correct,
                "answer_accuracy": _fraction_text(answer),
                "format_accuracy": _fraction_text(fmt),
                "strict_accuracy": _fraction_text(strict),
                "answer_ci_low": _fraction_text(answer_ci_low) if has_answer_ci else "",
                "answer_ci_high": _fraction_text(answer_ci_high) if has_answer_ci else "",
                "obvious_failure_rate": _failure_rate_text(row, answer),
                "provider_errors": _first(row, "provider_errors") or "0",
                "timeouts": _first(row, "timeouts") or "0",
                "estimated_cost_usd": cost,
                "total_tokens": tokens,
                "output_tokens": output_tokens,
                "reasoning_tokens": reasoning_tokens,
                "reasoning_effort": reasoning_effort,
                "thinking_group": _thinking_group(row, reasoning_effort),
                "model_family": _model_family(row),
                "cost_per_correct_usd": cost_per_correct,
                "tokens_per_correct": _first(row, "tokens_per_correct"),
            }
        )
    return normalized


def _normalize_family_rows(
    rows: Sequence[dict[str, str]],
    *,
    label_overrides: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    label_overrides = label_overrides or {}
    for row in rows:
        samples = _first(row, "samples", "scored_samples")
        strict_correct = _first(row, "strict_correct", "correct")
        answer_correct = _first(row, "answer_correct", "correct")
        format_correct = _first(row, "format_correct", "correct")
        raw_label = _first(row, "label", "model") or "unknown"
        summary_dir = _first(row, "summary_dir")
        normalized.append(
            {
                "raw_label": raw_label,
                "label": label_overrides.get(summary_dir, _display_model_label(row)),
                "model": _first(row, "model") or "",
                "summary_dir": summary_dir,
                "family": _first(row, "family") or "unknown",
                "samples": samples,
                "answer_correct": answer_correct,
                "format_correct": format_correct,
                "strict_correct": strict_correct,
                "estimated_cost_usd": _first(row, "estimated_cost_usd") or "",
                "reasoning_tokens": _first(row, "reasoning_tokens"),
            }
        )
    return normalized


def _disambiguate_duplicate_labels(
    rows: Sequence[dict[str, str]],
) -> list[dict[str, str]]:
    counts = Counter(row.get("label", "") for row in rows)
    disambiguated: list[dict[str, str]] = []
    for row in rows:
        label = row.get("label", "")
        if counts[label] <= 1:
            disambiguated.append(dict(row))
            continue
        updated = dict(row)
        updated["label"] = f"{label} ({_run_slug(row)})"
        disambiguated.append(updated)
    return disambiguated


def _duplicate_label_overrides(rows: Sequence[dict[str, str]]) -> dict[str, str]:
    normalized = _normalize_comparison_rows(rows)
    return {
        row.get("summary_dir", ""): row.get("label", "")
        for row in _disambiguate_duplicate_labels(normalized)
        if row.get("summary_dir")
    }


def _run_slug(row: dict[str, str]) -> str:
    value = row.get("summary_dir") or row.get("model") or "run"
    slug = Path(value).name
    for prefix in ("paper-", "next-", "top-thinking-"):
        if slug.startswith(prefix):
            slug = slug[len(prefix) :]
            break
    return _truncate(slug, 24)


def _correct_count(
    row: dict[str, str],
    correct_keys: Sequence[str],
    metric_fraction: float | None,
    samples: int,
) -> str:
    explicit = _first(row, *correct_keys)
    if explicit:
        return str(_int_cell(explicit))
    if metric_fraction is None or samples <= 0:
        return ""
    return str(round(metric_fraction * samples))


def _failure_rate_text(row: dict[str, str], answer: float | None) -> str:
    explicit = _first(row, "obvious_failure_rate", "failure_rate")
    if explicit:
        return _fraction_text(_float_cell(explicit))
    if answer is None:
        return ""
    return _fraction_text(max(0.0, 1.0 - answer))


def _inferred_reasoning_effort(row: dict[str, str]) -> str:
    explicit = _first(row, "reasoning_effort")
    if explicit:
        return explicit.lower()
    label_effort = _reasoning_effort_from_label(_first(row, "label", "model"))
    if label_effort:
        return label_effort
    if _int_cell(_first(row, "reasoning_tokens")) > 0:
        return "auto"
    return ""


def _reasoning_effort_from_label(label: str) -> str:
    normalized = (
        label.lower()
        .replace("(", " ")
        .replace(")", " ")
        .replace("[", " ")
        .replace("]", " ")
    )
    tokens = [token.strip(",:;") for token in normalized.split()]
    for token in reversed(tokens):
        if token in REASONING_DEPTHS:
            return token
    return ""


def _display_model_label(row: dict[str, str]) -> str:
    label = _first(row, "label", "model") or "unknown"
    effort = _inferred_reasoning_effort(row)
    if effort and effort != "none" and not _reasoning_effort_from_label(label):
        return f"{label} {effort}"
    return label


def _thinking_group(row: dict[str, str], reasoning_effort: str) -> str:
    if reasoning_effort in {"none", "off"}:
        return "non-thinking"
    if reasoning_effort in {"minimal", "low", "medium", "high"}:
        return "specified thinking"
    if reasoning_effort == "auto":
        return "auto/observed thinking"
    if _int_cell(_first(row, "reasoning_tokens")) > 0:
        return "auto/observed thinking"
    return "unspecified or no reported reasoning"


def _model_family(row: dict[str, str]) -> str:
    text = f"{_first(row, 'model')} {_first(row, 'label')}".lower()
    if "anthropic" in text or "claude" in text:
        return "Anthropic Claude"
    if "gemini" in text or "google/" in text:
        return "Google Gemini"
    if "grok" in text or "xai" in text or "x-ai" in text:
        return "xAI Grok"
    if "openai" in text or "gpt" in text or "o3" in text or "o4" in text:
        return "OpenAI GPT/O"
    if "openrouter" in text:
        return "OpenRouter other"
    return "Other or unknown"


def _first(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return ""


def _metric_fraction(
    row: dict[str, str],
    fraction_key: str,
    pct_key: str,
    fallback_pct: str,
) -> float | None:
    fraction = _first(row, fraction_key)
    if fraction:
        return _float_cell(fraction)
    pct = _first(row, pct_key, fallback_pct)
    if pct:
        return _float_cell(pct) / 100.0
    return None


def _fraction_text(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6f}"


def _main_results_table(
    rows: Sequence[dict[str, str]],
    source_label: str,
    *,
    is_placeholder: bool,
) -> str:
    if not rows:
        return _single_status_table("No final paper sweep has been run")
    display_rows = _top_model_rows(rows, limit=12)
    source_note = _result_source_note(source_label, is_placeholder=is_placeholder)
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\footnotesize",
        "\\begin{tabularx}{\\linewidth}{@{}Xrrrrrrr@{}}",
        "\\toprule",
        (
            "Model & N & Ans. correct & 95\\% CI & Fmt. & Strict & "
            "Tok./correct & USD/correct \\\\"
        ),
        "\\midrule",
        (
            "\\multicolumn{8}{@{}p{\\linewidth}@{}}{\\emph{"
            f"{_latex_escape(source_note)}"
            "}} \\\\"
        ),
        "\\midrule",
    ]
    for row in display_rows:
        lines.append(
            f"{_latex_escape(_truncate(row.get('label', 'unknown'), 34))} & "
            f"{_latex_escape(row.get('scored_samples', ''))} & "
            f"{_percent_cell(row.get('answer_accuracy'))} & "
            f"{_percent_interval_cell(row.get('answer_ci_low'), row.get('answer_ci_high'))} & "
            f"{_percent_cell(row.get('format_accuracy'))} & "
            f"{_percent_cell(row.get('strict_accuracy'))} & "
            f"{_integer_decimal_cell(row.get('tokens_per_correct'))} & "
            f"{_money_cell(row.get('cost_per_correct_usd'))} \\\\"
        )
    if len(rows) > len(display_rows):
        lines.append(
            "\\multicolumn{8}{@{}l@{}}{"
            f"\\emph{{Showing {len(display_rows)} of {len(rows)} model rows.}}}} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabularx}", "\\normalsize", ""])
    return "\n".join(lines)


def _family_results_table(
    rows: Sequence[dict[str, str]],
    source_label: str,
    *,
    is_placeholder: bool,
) -> str:
    if not rows:
        return _single_status_table("No final family results available yet")
    family_rows = _aggregate_family_rows(rows)
    source_note = _result_source_note(source_label, is_placeholder=is_placeholder)
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\footnotesize",
        "\\begin{tabularx}{\\linewidth}{@{}Xrrrrrr@{}}",
        "\\toprule",
        "Family & N & Answer correct & 95\\% CI & Format & Strict & Cost \\\\",
        "\\midrule",
        (
            "\\multicolumn{7}{@{}p{\\linewidth}@{}}{\\emph{"
            f"{_latex_escape(source_note)}"
            "}} \\\\"
        ),
        "\\midrule",
    ]
    for row in family_rows:
        samples = _int_cell(row["samples"])
        answer = _ratio_percent(row["answer_correct"], row["samples"])
        fmt = _ratio_percent(row["format_correct"], row["samples"])
        strict = _ratio_percent(row["strict_correct"], row["samples"])
        ci_low, ci_high = wilson_interval(_int_cell(row["answer_correct"]), samples)
        lines.append(
            f"{_latex_escape(_family_label(row.get('family', 'unknown')))} & "
            f"{samples} & {answer} & "
            f"{_percent_interval_cell(_fraction_text(ci_low), _fraction_text(ci_high))} & "
            f"{fmt} & {strict} & "
            f"{_money_cell(row.get('estimated_cost_usd'))} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabularx}", "\\normalsize", ""])
    return "\n".join(lines)


def _aggregate_family_rows(rows: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    aggregates: dict[str, Counter[str]] = {}
    costs: Counter[str] = Counter()
    for row in rows:
        family = row.get("family") or "unknown"
        aggregates.setdefault(family, Counter())
        aggregates[family]["samples"] += _int_cell(row.get("samples"))
        aggregates[family]["answer_correct"] += _int_cell(row.get("answer_correct"))
        aggregates[family]["format_correct"] += _int_cell(row.get("format_correct"))
        aggregates[family]["strict_correct"] += _int_cell(row.get("strict_correct"))
        costs[family] += _float_cell(row.get("estimated_cost_usd"))
    output = []
    for family, aggregate in aggregates.items():
        output.append(
            {
                "family": family,
                "samples": str(int(aggregate["samples"])),
                "answer_correct": str(int(aggregate["answer_correct"])),
                "format_correct": str(int(aggregate["format_correct"])),
                "strict_correct": str(int(aggregate["strict_correct"])),
                "estimated_cost_usd": f"{costs[family]:.8f}",
            }
        )
    return sorted(output, key=lambda row: _ratio_value(row["answer_correct"], row["samples"]))


def _group_results_table(
    rows: Sequence[dict[str, str]],
    source_label: str,
    *,
    group_key: str,
    group_title: str,
    is_placeholder: bool,
) -> str:
    if not rows:
        return _single_status_table(f"No {group_title.lower()} results available yet")
    aggregates = _aggregate_model_group_rows(rows, group_key=group_key)
    source_note = _result_source_note(source_label, is_placeholder=is_placeholder)
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\footnotesize",
        "\\begin{tabularx}{\\linewidth}{@{}Xrrrrrr@{}}",
        "\\toprule",
        f"{_latex_escape(group_title)} & Models & N & Correct & Fail & Reason/sample & Cost \\\\",
        "\\midrule",
        (
            "\\multicolumn{7}{@{}p{\\linewidth}@{}}{\\emph{"
            f"{_latex_escape(source_note)} Model-row groups are sample-weighted. "
            "Reason/sample uses reported reasoning tokens only."
            "}} \\\\"
        ),
        "\\midrule",
    ]
    for row in aggregates:
        samples = _int_cell(row["samples"])
        answer = _ratio_percent(row["answer_correct"], row["samples"])
        fail = _percent_cell(row["obvious_failure_rate"])
        reason_per_sample = _decimal_cell(
            _safe_ratio(_float_cell(row["reasoning_tokens"]), samples),
            digits=1,
        )
        lines.append(
            f"{_latex_escape(_group_label(row['group']))} & "
            f"{_int_cell(row['models'])} & "
            f"{samples} & {answer} & {fail} & "
            f"{reason_per_sample} & {_money_cell(row['estimated_cost_usd'])} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabularx}", "\\normalsize", ""])
    return "\n".join(lines)


def _aggregate_model_group_rows(
    rows: Sequence[dict[str, str]],
    *,
    group_key: str,
) -> list[dict[str, str]]:
    aggregates: dict[str, Counter[str]] = {}
    costs: Counter[str] = Counter()
    model_counts: Counter[str] = Counter()
    for row in rows:
        group = row.get(group_key) or "Unknown"
        aggregates.setdefault(group, Counter())
        model_counts[group] += 1
        samples = _int_cell(row.get("scored_samples"))
        answer_correct = _int_cell(row.get("answer_correct"))
        aggregates[group]["samples"] += samples
        aggregates[group]["answer_correct"] += answer_correct
        aggregates[group]["reasoning_tokens"] += _int_cell(row.get("reasoning_tokens"))
        costs[group] += _float_cell(row.get("estimated_cost_usd"))
    output = []
    for group, aggregate in aggregates.items():
        samples = int(aggregate["samples"])
        answer_correct = int(aggregate["answer_correct"])
        output.append(
            {
                "group": group,
                "models": str(int(model_counts[group])),
                "samples": str(samples),
                "answer_correct": str(answer_correct),
                "obvious_failure_rate": _fraction_text(
                    1.0 - _safe_ratio(answer_correct, samples)
                ),
                "reasoning_tokens": str(int(aggregate["reasoning_tokens"])),
                "estimated_cost_usd": f"{costs[group]:.8f}",
            }
        )
    return sorted(
        output,
        key=lambda row: (
            -_ratio_value(row["answer_correct"], row["samples"]),
            row["group"],
        ),
    )


def _group_label(value: str) -> str:
    if value in {
        "auto/observed thinking",
        "non-thinking",
        "specified thinking",
        "unspecified or no reported reasoning",
    }:
        return value[:1].upper() + value[1:]
    return value


def _failure_type_summary_table(result_bundle: ResultBundle) -> str:
    if result_bundle.wrong_answer_rows:
        return _wrong_answer_failure_type_table(result_bundle)
    rows = result_bundle.family_rows
    if not rows:
        return _single_status_table("No family failure summary available yet")
    family_rows = _aggregate_family_rows(rows)
    source_note = _result_source_note(
        result_bundle.source_label,
        is_placeholder=result_bundle.is_placeholder,
    )
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\footnotesize",
        "\\begin{tabularx}{\\linewidth}{@{}Xrrrr@{}}",
        "\\toprule",
        "Question family & N & Answer misses & Format misses & Strict misses \\\\",
        "\\midrule",
        (
            "\\multicolumn{5}{@{}p{\\linewidth}@{}}{\\emph{"
            f"{_latex_escape(source_note)} Counts are aggregate misses across "
            "all displayed model rows, not a per-item error taxonomy."
            "}} \\\\"
        ),
        "\\midrule",
    ]
    for row in family_rows:
        samples = _int_cell(row["samples"])
        answer_misses = samples - _int_cell(row["answer_correct"])
        format_misses = samples - _int_cell(row["format_correct"])
        strict_misses = samples - _int_cell(row["strict_correct"])
        lines.append(
            f"{_latex_escape(_family_label(row.get('family', 'unknown')))} & "
            f"{samples} & {answer_misses} & {format_misses} & {strict_misses} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabularx}", "\\normalsize", ""])
    return "\n".join(lines)


def _wrong_answer_failure_type_table(result_bundle: ResultBundle) -> str:
    source_note = _result_source_note(
        result_bundle.source_label,
        is_placeholder=result_bundle.is_placeholder,
    )
    counts: Counter[str] = Counter()
    families_by_type: dict[str, Counter[str]] = {}
    for row in result_bundle.wrong_answer_rows:
        failure_type = row.get("failure_type") or "unknown"
        family = row.get("family") or "unknown"
        counts[failure_type] += 1
        families_by_type.setdefault(failure_type, Counter())[family] += 1
    total = sum(counts.values())
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\footnotesize",
        "\\begin{tabularx}{\\linewidth}{@{}XrrX@{}}",
        "\\toprule",
        "Failure type & Rows & Share & Most common family \\\\",
        "\\midrule",
        (
            "\\multicolumn{4}{@{}p{\\linewidth}@{}}{\\emph{"
            f"{_latex_escape(source_note)} Failure rows come from the "
            "wrong-answer review CSV and include answer-wrong plus "
            "format-only review rows."
            "}} \\\\"
        ),
        "\\midrule",
    ]
    for failure_type, count in counts.most_common(12):
        family, family_count = families_by_type[failure_type].most_common(1)[0]
        share = 100.0 * _safe_ratio(count, total)
        lines.append(
            f"{_latex_escape(_failure_type_label(failure_type))} & "
            f"{count} & {share:.1f}\\% & "
            f"{_latex_escape(_family_label(family))} ({family_count}) \\\\"
        )
    if len(counts) > 12:
        lines.append(
            "\\multicolumn{4}{@{}l@{}}{"
            f"\\emph{{Showing 12 of {len(counts)} failure types.}}}} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabularx}", "\\normalsize", ""])
    return "\n".join(lines)


def _failure_type_label(value: str) -> str:
    labels = {
        "ambiguous_output": "Ambiguous output",
        "format_noncompliance": "Format noncompliance",
        "incorrect_count": "Incorrect count",
        "json_malformed": "Malformed JSON",
        "list_count_error": "List count error",
        "negation_error": "Negation error",
        "non_answer": "Non-answer",
        "ordering_error": "Ordering error",
        "verbose_noncompliance": "Verbose noncompliance",
        "wrong_letter_or_substring": "Wrong letter or substring",
    }
    return labels.get(value, value.replace("_", " ").title())


def _provider_exclusions_table(
    rows: Sequence[dict[str, str]],
    source_label: str,
    *,
    is_placeholder: bool,
) -> str:
    excluded = [
        row
        for row in rows
        if _int_cell(row.get("provider_errors")) > 0 or _int_cell(row.get("timeouts")) > 0
    ]
    if not excluded:
        return _single_status_table(f"No provider exclusions recorded in {source_label}")
    source_note = _result_source_note(source_label, is_placeholder=is_placeholder)
    lines = [
        "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
        "\\begin{tabularx}{\\linewidth}{@{}XrrX@{}}",
        "\\toprule",
        "Model & Provider errors & Timeouts & Inspect model \\\\",
        "\\midrule",
        (
            "\\multicolumn{4}{@{}p{\\linewidth}@{}}{\\emph{"
            f"{_latex_escape(source_note)}"
            "}} \\\\"
        ),
        "\\midrule",
    ]
    for row in sorted(excluded, key=lambda value: value.get("label", "")):
        lines.append(
            f"{_latex_escape(row.get('label', 'unknown'))} & "
            f"{_int_cell(row.get('provider_errors'))} & "
            f"{_int_cell(row.get('timeouts'))} & "
            f"{_latex_path(row.get('model', 'unknown'))} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabularx}", ""])
    return "\n".join(lines)


def _write_result_figures(
    figures_dir: Path,
    *,
    result_bundle: ResultBundle,
    figure_renderer: str,
) -> tuple[Path, ...]:
    figures_dir.mkdir(parents=True, exist_ok=True)
    paths = (
        figures_dir / "leaderboard.pdf",
        figures_dir / "family_heatmap.pdf",
        figures_dir / "answer_format_gap.pdf",
        figures_dir / "cost_frontier.pdf",
    )

    if not result_bundle.has_results:
        figure_specs = (
            (paths[0], "Leaderboard", "No result rows available yet."),
            (paths[1], "Family heatmap", "No family result rows available yet."),
            (paths[2], "Answer/format gap", "No result rows available yet."),
            (paths[3], "Cost frontier", "No cost result rows available yet."),
        )
        for path, title, subtitle in figure_specs:
            _write_minimal_pdf(path, title=title, subtitle=subtitle)
        return paths

    _write_leaderboard_pdf(paths[0], result_bundle, figure_renderer=figure_renderer)
    _write_family_heatmap_pdf(paths[1], result_bundle, figure_renderer=figure_renderer)
    _write_answer_format_gap_pdf(paths[2], result_bundle, figure_renderer=figure_renderer)
    _write_cost_frontier_pdf(paths[3], result_bundle, figure_renderer=figure_renderer)
    return paths


def _figure_subtitle(result_bundle: ResultBundle) -> str:
    status = (
        "Draft-only proof-point placeholder; replace before final claims."
        if result_bundle.is_placeholder
        else "First-draft paper evidence output."
    )
    return f"Source: {result_bundle.source_label}. {status}"


def _write_leaderboard_pdf(
    path: Path,
    result_bundle: ResultBundle,
    *,
    figure_renderer: str,
) -> None:
    rows = list(result_bundle.comparison_rows)
    if not rows:
        _write_minimal_pdf(path, title="Leaderboard", subtitle="No rows available.")
        return

    width = FIGURE_WIDTH
    height = 396
    commands = _chart_header(
        "Answer-Correctness Distribution",
        _figure_subtitle(result_bundle),
        width=width,
        height=height,
    )
    commands.extend(
        _pdf_text_commands(
            36,
            318,
            (
                "All model/settings rows are binned by answer correctness; "
                "highlights show representative high-scoring rows."
            ),
            8.2,
            color=COLOR_TEXT_MUTED,
        )
    )

    bands = [
        ("100%", lambda value: value >= 0.999999),
        ("95-<100%", lambda value: 0.95 <= value < 0.999999),
        ("80-<95%", lambda value: 0.80 <= value < 0.95),
        ("<80%", lambda value: value < 0.80),
    ]
    band_counts: list[tuple[str, int]] = []
    for label, predicate in bands:
        band_counts.append(
            (label, sum(1 for row in rows if predicate(_float_cell(row.get("answer_accuracy")))))
        )
    max_count = max(count for _, count in band_counts) or 1
    bar_left = 110
    bar_width = 165
    bar_top = 272
    bar_gap = 34
    commands.extend(_pdf_text_commands(36, 288, "Score band", 7.6, color=COLOR_TEXT_MUTED))
    commands.extend(_pdf_text_commands(198, 288, "Rows", 7.6, color=COLOR_TEXT_MUTED))
    for index, (label, count) in enumerate(band_counts):
        y = bar_top - index * bar_gap
        width_px = bar_width * count / max_count
        commands.extend(_pdf_text_commands(36, y + 5, label, 8.0))
        commands.extend(
            _pdf_rect_commands(
                bar_left,
                y,
                width_px,
                14,
                fill=COLOR_BLUE if index < 2 else COLOR_BLUE_LIGHT,
                stroke=COLOR_AXIS,
            )
        )
        commands.extend(_pdf_text_commands(bar_left + bar_width + 10, y + 3, str(count), 8.0))

    highlights = _distribution_highlight_rows(rows)
    commands.extend(
        _pdf_text_commands(312, 288, "Representative rows", 7.6, color=COLOR_TEXT_MUTED)
    )
    for index, (name, row) in enumerate(highlights):
        y = 268 - index * 30
        label = _truncate(row.get("label", "unknown"), 22)
        value = _pct_label(_float_cell(row.get("answer_accuracy")))
        commands.extend(_pdf_text_commands(312, y + 8, name, 7.4, color=COLOR_TEXT_MUTED))
        commands.extend(
            _pdf_text_commands(
                312,
                y - 1,
                f"{label} ({value})",
                7.4,
            )
        )

    commands.extend(
        _pdf_text_commands(
            36,
            24,
            "Complete row-level values are in the generated leaderboard CSV and report HTML.",
            7.2,
            color=COLOR_TEXT_MUTED,
        )
    )
    _write_figure_pdf(
        path,
        width=width,
        height=height,
        commands=commands,
        figure_renderer=figure_renderer,
    )


def _write_family_heatmap_pdf(
    path: Path,
    result_bundle: ResultBundle,
    *,
    figure_renderer: str,
) -> None:
    if not result_bundle.family_rows:
        _write_minimal_pdf(path, title="Family Heatmap", subtitle="No family rows available.")
        return

    cells, model_families, families = _model_family_task_family_cells(result_bundle)
    if not cells or not model_families or not families:
        _write_minimal_pdf(path, title="Family Heatmap", subtitle="No plottable rows available.")
        return

    width = FIGURE_WIDTH
    height = 414
    left = 116
    right = 20
    top = 264
    cell_height = 34
    cell_width = (width - left - right) / len(families)
    commands = _chart_header(
        "Model-Family by Task-Family Accuracy",
        _figure_subtitle(result_bundle),
        width=width,
        height=height,
    )
    commands.extend(
        _pdf_text_commands(
            36,
            318,
            (
                "Cells show median answer correctness across all rows in each "
                "model-family and task-family group."
            ),
            8.0,
            color=COLOR_TEXT_MUTED,
        )
    )

    for family_index, family in enumerate(families):
        x = left + family_index * cell_width
        commands.extend(
            _pdf_text_commands(
                x + 4,
                top + cell_height + 2,
                _truncate(_family_short_label(family), 7),
                7.4,
            )
        )

    for row_index, model_family in enumerate(model_families):
        y = top - row_index * cell_height
        commands.extend(_pdf_text_commands(36, y + 12, _truncate(model_family, 18), 7.2))
        for family_index, family in enumerate(families):
            x = left + family_index * cell_width
            payload = cells.get((model_family, family))
            value = None if payload is None else payload[0]
            fill = COLOR_EMPTY if value is None else _heat_color(value)
            commands.extend(
                _pdf_rect_commands(
                    x,
                    y,
                    cell_width - 2,
                    cell_height - 2,
                    fill=fill,
                    stroke=(1.0, 1.0, 1.0),
                )
            )
            cell_text = "NA" if payload is None else f"{value * 100:.0f}"
            commands.extend(
                _pdf_text_commands(
                    x + 5,
                    y + 11,
                    cell_text,
                    7.0,
                    color=(0.05, 0.05, 0.05),
                )
            )

    legend_y = 42
    legend = (
        ("<60%", (0.78, 0.20, 0.18)),
        ("60-80%", (0.90, 0.56, 0.18)),
        ("80-95%", (0.52, 0.68, 0.26)),
        (">=95%", (0.16, 0.55, 0.27)),
    )
    for index, (label, color) in enumerate(legend):
        x = 36 + index * 86
        commands.extend(_pdf_rect_commands(x, legend_y, 20, 10, fill=color))
        commands.extend(_pdf_text_commands(x + 25, legend_y + 2, label, 7.4))
    commands.extend(
        _pdf_text_commands(
            36,
            24,
            (
                "Task-family columns are ordered from hardest to easiest by "
                "aggregate answer correctness."
            ),
            7.2,
            color=COLOR_TEXT_MUTED,
        )
    )
    _write_figure_pdf(
        path,
        width=width,
        height=height,
        commands=commands,
        figure_renderer=figure_renderer,
    )


def _distribution_highlight_rows(
    rows: Sequence[dict[str, str]],
) -> list[tuple[str, dict[str, str]]]:
    selected: list[tuple[str, dict[str, str]]] = []
    seen: set[str] = set()

    def add(name: str, row: dict[str, str] | None) -> None:
        if row is None:
            return
        key = row.get("label", "")
        if key in seen:
            return
        selected.append((name, row))
        seen.add(key)

    perfect = [row for row in rows if _float_cell(row.get("answer_accuracy")) >= 0.999999]
    near = [row for row in rows if _float_cell(row.get("answer_accuracy")) >= 0.95]
    add(
        "Cheapest perfect",
        min(perfect, key=lambda row: _float_cell(row.get("estimated_cost_usd")) or 1e9)
        if perfect
        else None,
    )
    add(
        "Fewest-token perfect",
        min(perfect, key=lambda row: _int_cell(row.get("total_tokens")) or 10**12)
        if perfect
        else None,
    )
    add(
        "Cheapest >=95%",
        min(near, key=lambda row: _float_cell(row.get("estimated_cost_usd")) or 1e9)
        if near
        else None,
    )
    add(
        "Best non-perfect",
        max(
            [row for row in rows if _float_cell(row.get("answer_accuracy")) < 0.999999],
            key=lambda row: (
                _float_cell(row.get("answer_accuracy")),
                -_float_cell(row.get("estimated_cost_usd")),
            ),
            default=None,
        ),
    )
    return selected[:4]


def _model_family_task_family_cells(
    result_bundle: ResultBundle,
) -> tuple[dict[tuple[str, str], tuple[float, int]], list[str], list[str]]:
    model_family_by_label = {
        row.get("label", ""): row.get("model_family", "Other or unknown")
        for row in result_bundle.comparison_rows
    }
    values: dict[tuple[str, str], list[float]] = {}
    family_totals: dict[str, Counter[str]] = {}
    model_family_values: dict[str, list[float]] = {}
    for row in result_bundle.family_rows:
        label = row.get("label", "")
        model_family = model_family_by_label.get(label, "Other or unknown")
        family = row.get("family", "unknown")
        samples = _int_cell(row.get("samples"))
        answer_correct = _int_cell(row.get("answer_correct"))
        if samples <= 0:
            continue
        value = _safe_ratio(answer_correct, samples)
        values.setdefault((model_family, family), []).append(value)
        model_family_values.setdefault(model_family, []).append(value)
        family_totals.setdefault(family, Counter())
        family_totals[family]["samples"] += samples
        family_totals[family]["answer_correct"] += answer_correct

    cells = {
        key: (float(median(cell_values)), len(cell_values))
        for key, cell_values in values.items()
    }
    families = sorted(
        family_totals,
        key=lambda family: (
            _safe_ratio(
                int(family_totals[family]["answer_correct"]),
                int(family_totals[family]["samples"]),
            ),
            family,
        ),
    )[:8]
    model_families = sorted(
        model_family_values,
        key=lambda family: (-float(median(model_family_values[family])), family),
    )[:7]
    return cells, model_families, families


def _write_answer_format_gap_pdf(
    path: Path,
    result_bundle: ResultBundle,
    *,
    figure_renderer: str,
) -> None:
    gap_rows: list[tuple[dict[str, str], float, float]] = []
    for row in result_bundle.comparison_rows:
        strict = _float_cell(row.get("strict_accuracy"))
        answer_gap = max(0.0, _float_cell(row.get("answer_accuracy")) - strict)
        format_gap = max(0.0, _float_cell(row.get("format_accuracy")) - strict)
        if max(answer_gap, format_gap) > 0:
            gap_rows.append((row, answer_gap, format_gap))
    gap_rows = sorted(
        gap_rows,
        key=lambda item: (-max(item[1], item[2]), item[0].get("label", "")),
    )[:12]
    if not gap_rows:
        _write_minimal_pdf(
            path,
            title="Answer/Format Gap",
            subtitle="No answer or format gaps found in current rows.",
        )
        return

    max_gap = max(max(answer_gap, format_gap) for _, answer_gap, format_gap in gap_rows)
    max_gap = max(0.05, max_gap * 1.08)
    width = FIGURE_WIDTH
    height = 396
    left = 150
    right = 30
    chart_width = width - left - right
    top = 270
    row_height = 17
    bottom = top - (len(gap_rows) - 1) * row_height - 12
    commands = _chart_header(
        "Strict-Compliance Gap Relative to Correctness",
        _figure_subtitle(result_bundle),
        width=width,
        height=height,
    )
    commands.extend(_pdf_rect_commands(36, 302, 12, 7, fill=COLOR_BLUE))
    commands.extend(_pdf_text_commands(54, 300, "answer minus strict", 7.5))
    commands.extend(_pdf_rect_commands(170, 302, 12, 7, fill=COLOR_ORANGE))
    commands.extend(_pdf_text_commands(188, 300, "format minus strict", 7.5))

    for tick in _gap_ticks(max_gap):
        if tick > max_gap:
            continue
        x = left + chart_width * tick / max_gap
        commands.extend(_pdf_line_commands(x, bottom, x, top + 10, color=COLOR_GRID))
        commands.extend(_pdf_text_commands(x - 9, bottom - 18, f"{tick * 100:.0f}%", 7.2))

    for index, (row, answer_gap, format_gap) in enumerate(gap_rows):
        y = top - index * row_height
        commands.extend(
            _pdf_text_commands(
                36,
                y + 3,
                _truncate(row.get("label", "unknown"), 24),
                7.5,
            )
        )
        commands.extend(
            _pdf_rect_commands(
                left,
                y + 8,
                chart_width * answer_gap / max_gap,
                6,
                fill=COLOR_BLUE,
            )
        )
        commands.extend(
            _pdf_rect_commands(
                left,
                y,
                chart_width * format_gap / max_gap,
                6,
                fill=COLOR_ORANGE,
            )
        )

    commands.extend(
        _pdf_text_commands(
            36,
            24,
            "Gaps expose where non-strict success differs from strict scoring.",
            7.2,
            color=COLOR_TEXT_MUTED,
        )
    )
    _write_figure_pdf(
        path,
        width=width,
        height=height,
        commands=commands,
        figure_renderer=figure_renderer,
    )


def _write_cost_frontier_pdf(
    path: Path,
    result_bundle: ResultBundle,
    *,
    figure_renderer: str,
) -> None:
    points: list[tuple[dict[str, str], float, float]] = []
    for row in result_bundle.comparison_rows:
        cost = _float_cell(row.get("estimated_cost_usd"))
        strict = _float_cell(row.get("answer_accuracy"))
        if cost > 0:
            points.append((row, strict, cost))
    if not points:
        _write_minimal_pdf(path, title="Cost Frontier", subtitle="No cost rows available.")
        return

    width = FIGURE_WIDTH
    height = 376
    left = 62
    right = 28
    bottom = 82
    top = 286
    chart_width = width - left - right
    chart_height = top - bottom
    costs = [cost for _, _, cost in points]
    min_cost, max_cost = _nice_cost_bounds(min(costs), max(costs))
    min_log = math.log10(min_cost)
    max_log = math.log10(max_cost)
    if min_log == max_log:
        min_log -= 0.5
        max_log += 0.5
    accuracy_values = [strict for _, strict, _ in points]
    y_min, y_max = _accuracy_axis_bounds(accuracy_values, floor_hint=0.50)
    commands = _chart_header(
        "Answer Correctness vs Estimated 224-Question Run Cost",
        _figure_subtitle(result_bundle),
        width=width,
        height=height,
    )
    commands.extend(
        _pdf_text_commands(
            36,
            306,
            (
                "X-axis is estimated total USD for this 224-question split on a "
                "log scale; y-axis is answer correctness."
            ),
            8.2,
            color=COLOR_TEXT_MUTED,
        )
    )

    for pct in _percent_ticks(y_min, y_max):
        y = _scale_linear(pct, y_min, y_max, bottom, chart_height)
        commands.extend(
            _pdf_line_commands(left, y, width - right, y, color=COLOR_GRID)
        )
        commands.extend(_pdf_text_commands(32, y - 3, f"{pct * 100:.0f}%", 7.3))

    tick_costs = _cost_ticks(min_cost, max_cost)
    for cost in tick_costs:
        x = left + chart_width * (math.log10(cost) - min_log) / (max_log - min_log)
        commands.extend(_pdf_line_commands(x, bottom, x, top, color=COLOR_GRID))
        commands.extend(
            _pdf_text_commands(x - 15, bottom - 22, _cost_tick_label(cost), 7.1)
        )

    commands.extend(
        _pdf_line_commands(left, bottom, width - right, bottom, color=COLOR_AXIS)
    )
    commands.extend(_pdf_line_commands(left, bottom, left, top, color=COLOR_AXIS))
    commands.extend(
        _pdf_text_commands(150, 32, "Estimated run cost, USD for 224 questions (log scale)", 7.6)
    )
    commands.extend(_pdf_text_commands(16, top + 2, "Answer correctness", 7.4))
    label_set = _frontier_label_set(points)
    point_positions: list[tuple[dict[str, str], float, float]] = []
    for row, strict, cost in points:
        x = left + chart_width * (math.log10(cost) - min_log) / (max_log - min_log)
        y = _scale_linear(max(y_min, min(y_max, strict)), y_min, y_max, bottom, chart_height)
        point_positions.append((row, x, y))
        commands.extend(
            _pdf_rect_commands(x - 3.0, y - 3.0, 6.0, 6.0, fill=COLOR_BLUE)
        )

    label_boxes: list[tuple[float, float, float, float]] = []
    for row, x, y in point_positions:
        if row.get("label", "") in label_set:
            label = _truncate(row.get("label", "unknown"), 18)
            label_x, label_y, label_box = _frontier_label_position(
                x,
                y,
                label,
                bounds=(left, bottom, width - right, top + 18),
                existing_boxes=label_boxes,
            )
            label_boxes.append(label_box)
            commands.extend(
                _pdf_text_commands(
                    label_x,
                    label_y,
                    label,
                    7.3,
                )
            )

    _write_figure_pdf(
        path,
        width=width,
        height=height,
        commands=commands,
        figure_renderer=figure_renderer,
    )


def _single_status_table(status: str) -> str:
    return "\n".join(
        [
            "% Generated by scripts/build_paper_assets.py. Do not hand-edit.",
            "\\begin{tabular}{l}",
            "\\toprule",
            "Status \\\\",
            "\\midrule",
            f"{_latex_escape(status)} \\\\",
            "\\bottomrule",
            "\\end{tabular}",
            "",
        ]
    )


def _percent_cell(value: str | None) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value) * 100:.1f}\\%"


def _percent_interval_cell(low: str | None, high: str | None) -> str:
    if low is None or high is None or low == "" or high == "":
        return ""
    return f"{float(low) * 100:.1f}--{float(high) * 100:.1f}\\%"


def _ratio_percent(numerator: str | None, denominator: str | None) -> str:
    denom = _int_cell(denominator)
    if denom == 0:
        return ""
    return f"{(_int_cell(numerator) / denom) * 100:.1f}\\%"


def _money_cell(value: str | None) -> str:
    if value is None or value == "":
        return ""
    parsed = float(value)
    if parsed == 0:
        return "\\$0"
    if parsed < 0.0001:
        return f"\\${parsed:.6f}"
    if parsed < 0.01:
        return f"\\${parsed:.5f}"
    return f"\\${parsed:.4f}"


def _integer_decimal_cell(value: str | None) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.0f}"


def _int_cell(value: str | None) -> int:
    if value is None or value == "":
        return 0
    return int(float(value))


def _float_cell(value: str | None) -> float:
    if value is None or value == "":
        return 0.0
    try:
        parsed = float(value)
    except ValueError:
        return 0.0
    if not math.isfinite(parsed):
        return 0.0
    return parsed


def _decimal_cell(value: float | None, *, digits: int) -> str:
    if value is None:
        return ""
    return f"{value:.{digits}f}"


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _ratio_value(numerator: str | None, denominator: str | None) -> float:
    denom = _int_cell(denominator)
    if denom == 0:
        return 0.0
    return _int_cell(numerator) / denom


def _top_model_rows(
    rows: Sequence[dict[str, str]],
    *,
    limit: int,
) -> list[dict[str, str]]:
    def sort_key(row: dict[str, str]) -> tuple[float, float, float, str]:
        cost = (
            _float_cell(row.get("cost_per_correct_usd"))
            if row.get("cost_per_correct_usd")
            else math.inf
        )
        tokens = (
            _float_cell(row.get("tokens_per_correct"))
            if row.get("tokens_per_correct")
            else math.inf
        )
        return (
            -_float_cell(row.get("answer_accuracy")),
            cost,
            tokens,
            row.get("label", ""),
        )

    return list(sorted(rows, key=sort_key)[:limit])


def _heatmap_model_rows(
    rows: Sequence[dict[str, str]],
    *,
    limit: int,
) -> list[dict[str, str]]:
    general_rows = [row for row in rows if not _is_special_purpose_display_row(row)]
    if len(general_rows) >= limit:
        rows = general_rows
    ranked = sorted(
        rows,
        key=lambda row: (
            -_float_cell(row.get("answer_accuracy")),
            _float_cell(row.get("cost_per_correct_usd")) or math.inf,
            row.get("label", ""),
        ),
    )
    if len(ranked) <= limit:
        return ranked
    candidate_indexes = [
        0,
        1,
        2,
        3,
        len(ranked) // 4,
        len(ranked) // 2,
        (len(ranked) * 3) // 4,
        len(ranked) - 1,
    ]
    selected: list[dict[str, str]] = []
    seen: set[str] = set()
    for index in candidate_indexes:
        row = ranked[index]
        key = row.get("summary_dir") or row.get("label", "")
        if key in seen:
            continue
        selected.append(row)
        seen.add(key)
    cursor = 0
    while len(selected) < limit and cursor < len(ranked):
        row = ranked[cursor]
        key = row.get("summary_dir") or row.get("label", "")
        if key not in seen:
            selected.append(row)
            seen.add(key)
        cursor += 1
    return selected[:limit]


def _is_special_purpose_display_row(row: dict[str, str]) -> bool:
    text = f"{row.get('label', '')} {row.get('model', '')}".lower()
    return any(term in text for term in ("guard", "safeguard"))


def _result_source_note(source_label: str, *, is_placeholder: bool) -> str:
    if is_placeholder:
        return (
            f"Source: {source_label}. Draft-only placeholder for paper review; "
            "replace with the frozen final sweep before any final paper claims."
        )
    return f"Source: {source_label}. First-draft paper evidence output."


def _write_figure_pdf(
    path: Path,
    *,
    width: int,
    height: int,
    commands: Sequence[str],
    figure_renderer: str,
) -> None:
    if figure_renderer == "chrome-svg" and _write_chrome_svg_pdf(
        path,
        width=width,
        height=height,
        commands=commands,
    ):
        return
    _write_pdf(path, width=width, height=height, commands=commands)


def _write_chrome_svg_pdf(
    path: Path,
    *,
    width: int,
    height: int,
    commands: Sequence[str],
) -> bool:
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if not chrome.exists():
        return False
    svg = _svg_from_pdf_commands(width=width, height=height, commands=commands)
    page_width = width / 72
    page_height = height / 72
    html = "\n".join(
        [
            "<!doctype html>",
            "<html>",
            "<head>",
            "<meta charset=\"utf-8\">",
            "<style>",
            (
                f"@page {{ size: {page_width:.4f}in {page_height:.4f}in; "
                "margin: 0; }}"
            ),
            (
                f"html, body {{ margin: 0; width: {page_width:.4f}in; "
                f"height: {page_height:.4f}in; }}"
            ),
            "svg { display: block; width: 100%; height: 100%; }",
            "</style>",
            "</head>",
            "<body>",
            svg,
            "</body>",
            "</html>",
        ]
    )
    with tempfile.TemporaryDirectory(prefix="obviousbench-figure-") as tmp_dir:
        html_path = Path(tmp_dir) / "figure.html"
        html_path.write_text(html, encoding="utf-8")
        result = subprocess.run(
            [
                str(chrome),
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--print-to-pdf-no-header",
                f"--print-to-pdf={path}",
                html_path.as_uri(),
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
    return result.returncode == 0 and path.exists() and path.stat().st_size > 0


def _svg_from_pdf_commands(
    *,
    width: int,
    height: int,
    commands: Sequence[str],
) -> str:
    elements: list[str] = []
    fill = (0.0, 0.0, 0.0)
    stroke = (0.0, 0.0, 0.0)
    stroke_width = 0.5
    font_size = 10.0
    text_x = 0.0
    text_y = 0.0
    pending_rect: tuple[float, float, float, float] | None = None
    pending_move: tuple[float, float] | None = None
    pending_line: tuple[float, float, float, float] | None = None
    for command in commands:
        parts = command.split()
        if len(parts) == 4 and parts[-1] == "rg":
            fill = (float(parts[0]), float(parts[1]), float(parts[2]))
            continue
        if len(parts) == 4 and parts[-1] == "RG":
            stroke = (float(parts[0]), float(parts[1]), float(parts[2]))
            continue
        if len(parts) == 2 and parts[-1] == "w":
            stroke_width = float(parts[0])
            continue
        if len(parts) == 5 and parts[-1] == "re":
            pending_rect = (
                float(parts[0]),
                float(parts[1]),
                float(parts[2]),
                float(parts[3]),
            )
            continue
        if command == "f" and pending_rect is not None:
            x, y, rect_width, rect_height = pending_rect
            elements.append(
                "<rect "
                f"x=\"{x:.2f}\" y=\"{height - y - rect_height:.2f}\" "
                f"width=\"{rect_width:.2f}\" height=\"{rect_height:.2f}\" "
                f"fill=\"{_svg_color(fill)}\" />"
            )
            pending_rect = None
            continue
        if command == "S" and pending_rect is not None:
            x, y, rect_width, rect_height = pending_rect
            elements.append(
                "<rect "
                f"x=\"{x:.2f}\" y=\"{height - y - rect_height:.2f}\" "
                f"width=\"{rect_width:.2f}\" height=\"{rect_height:.2f}\" "
                f"fill=\"none\" stroke=\"{_svg_color(stroke)}\" "
                f"stroke-width=\"{stroke_width:.2f}\" />"
            )
            pending_rect = None
            continue
        if len(parts) == 3 and parts[-1] == "m":
            pending_move = (float(parts[0]), float(parts[1]))
            continue
        if len(parts) == 3 and parts[-1] == "l" and pending_move is not None:
            pending_line = (
                pending_move[0],
                pending_move[1],
                float(parts[0]),
                float(parts[1]),
            )
            continue
        if command == "S" and pending_line is not None:
            x1, y1, x2, y2 = pending_line
            elements.append(
                "<line "
                f"x1=\"{x1:.2f}\" y1=\"{height - y1:.2f}\" "
                f"x2=\"{x2:.2f}\" y2=\"{height - y2:.2f}\" "
                f"stroke=\"{_svg_color(stroke)}\" "
                f"stroke-width=\"{stroke_width:.2f}\" />"
            )
            pending_line = None
            continue
        if len(parts) == 3 and parts[0] == "/F1" and parts[-1] == "Tf":
            font_size = float(parts[1])
            continue
        if len(parts) == 7 and parts[-1] == "Tm":
            text_x = float(parts[4])
            text_y = float(parts[5])
            continue
        if command.startswith("(") and command.endswith(") Tj"):
            text = _pdf_unescape(command[1:-4])
            elements.append(
                "<text "
                f"x=\"{text_x:.2f}\" y=\"{height - text_y:.2f}\" "
                f"font-family=\"Helvetica, Arial, sans-serif\" "
                f"font-size=\"{font_size:.2f}\" "
                f"fill=\"{_svg_color(fill)}\">"
                f"{_svg_escape(text)}</text>"
            )
    return "\n".join(
        [
            (
                f"<svg width=\"{width}\" height=\"{height}\" "
                f"viewBox=\"0 0 {width} {height}\" "
                "xmlns=\"http://www.w3.org/2000/svg\">"
            ),
            *elements,
            "</svg>",
        ]
    )


def _svg_color(color: tuple[float, float, float]) -> str:
    red, green, blue = (round(max(0.0, min(1.0, channel)) * 255) for channel in color)
    return f"rgb({red},{green},{blue})"


def _svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _pdf_unescape(text: str) -> str:
    return text.replace("\\)", ")").replace("\\(", "(").replace("\\\\", "\\")


def _write_minimal_pdf(path: Path, *, title: str, subtitle: str) -> None:
    commands = _chart_header(title, subtitle, width=FIGURE_WIDTH, height=320)
    _write_pdf(path, width=FIGURE_WIDTH, height=320, commands=commands)


def _write_pdf(
    path: Path,
    *,
    width: int,
    height: int,
    commands: Sequence[str],
) -> None:
    stream = "\n".join(commands).encode("ascii", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
            "/Resources << /ProcSet [/PDF /Text] /Font << /F1 5 0 R >> >> "
            "/Contents 4 0 R >>"
        ).encode("ascii"),
        (
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"\nendstream"
        ),
        (
            b"<< /Type /Font /Subtype /Type1 /Name /F1 "
            b"/BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        ),
    ]
    body = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(body))
        body.extend(f"{index} 0 obj\n".encode("ascii"))
        body.extend(obj)
        body.extend(b"\nendobj\n")
    xref_offset = len(body)
    body.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    body.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        body.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    body.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    path.write_bytes(bytes(body))


def _chart_header(title: str, subtitle: str, *, width: int, height: int) -> list[str]:
    commands: list[str] = []
    commands.extend(_pdf_rect_commands(0, 0, width, height, fill=(1.0, 1.0, 1.0)))
    commands.extend(
        _pdf_text_commands(36, height - 32, title, 14.5, color=COLOR_TEXT)
    )
    commands.extend(
        _pdf_wrapped_text_commands(
            36,
            height - 52,
            subtitle,
            7.5,
            max_chars=92,
            max_lines=2,
            line_height=9.5,
            color=COLOR_TEXT_MUTED,
        )
    )
    commands.extend(
        _pdf_line_commands(36, height - 76, width - 36, height - 76, color=COLOR_GRID)
    )
    return commands


def _pdf_wrapped_text_commands(
    x: float,
    y: float,
    text: str,
    size: float,
    *,
    max_chars: int,
    max_lines: int,
    line_height: float,
    color: tuple[float, float, float] = (0.16, 0.16, 0.16),
) -> list[str]:
    commands: list[str] = []
    for index, line in enumerate(_wrap_text(text, max_chars=max_chars, max_lines=max_lines)):
        commands.extend(
            _pdf_text_commands(x, y - index * line_height, line, size, color=color)
        )
    return commands


def _wrap_text(text: str, *, max_chars: int, max_lines: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join([*current, word])
        if current and len(candidate) > max_chars:
            lines.append(" ".join(current))
            current = [word]
            if len(lines) == max_lines:
                break
        else:
            current.append(word)
    if current and len(lines) < max_lines:
        lines.append(" ".join(current))
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = _truncate(lines[-1], max_chars)
    return lines


def _pdf_text_commands(
    x: float,
    y: float,
    text: str,
    size: float,
    *,
    color: tuple[float, float, float] = (0.16, 0.16, 0.16),
) -> list[str]:
    return [
        "q",
        f"{_pdf_color(color)} rg",
        "BT",
        f"/F1 {size:.2f} Tf",
        f"1 0 0 1 {x:.2f} {y:.2f} Tm",
        f"({_pdf_escape(text)}) Tj",
        "ET",
        "Q",
    ]


def _pdf_rect_commands(
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    fill: tuple[float, float, float],
    stroke: tuple[float, float, float] | None = None,
) -> list[str]:
    commands = [
        "q",
        f"{_pdf_color(fill)} rg",
        f"{x:.2f} {y:.2f} {max(width, 0):.2f} {max(height, 0):.2f} re",
        "f",
        "Q",
    ]
    if stroke is not None:
        commands.extend(
            [
                "q",
                f"{_pdf_color(stroke)} RG",
                "0.50 w",
                f"{x:.2f} {y:.2f} {max(width, 0):.2f} {max(height, 0):.2f} re",
                "S",
                "Q",
            ]
        )
    return commands


def _pdf_line_commands(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: tuple[float, float, float],
    width: float = 0.5,
) -> list[str]:
    return [
        "q",
        f"{_pdf_color(color)} RG",
        f"{width:.2f} w",
        f"{x1:.2f} {y1:.2f} m",
        f"{x2:.2f} {y2:.2f} l",
        "S",
        "Q",
    ]


def _pdf_color(color: tuple[float, float, float]) -> str:
    return " ".join(f"{max(0.0, min(1.0, channel)):.3f}" for channel in color)


def _pct_label(value: float) -> str:
    return f"{value * 100:.1f}%"


def _truncate(value: str | None, max_chars: int) -> str:
    text = value or ""
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 3)].rstrip() + "..."


def _family_label(value: str) -> str:
    return FAMILY_LABELS.get(value, value.replace("_", " ").title())


def _family_short_label(value: str) -> str:
    return FAMILY_SHORT_LABELS.get(value, _truncate(_family_label(value), 7))


def _subfamily_label(value: str) -> str:
    return SUBFAMILY_LABELS.get(value, value.replace("_", " ").title())


def _heat_color(value: float) -> tuple[float, float, float]:
    if value >= 0.95:
        return (0.16, 0.55, 0.27)
    if value >= 0.80:
        return (0.52, 0.68, 0.26)
    if value >= 0.60:
        return (0.90, 0.56, 0.18)
    return (0.78, 0.20, 0.18)


def _scale_linear(
    value: float,
    minimum: float,
    maximum: float,
    start: float,
    length: float,
) -> float:
    if maximum <= minimum:
        return start + length / 2
    return start + length * (value - minimum) / (maximum - minimum)


def _accuracy_axis_bounds(
    low_values: Sequence[float],
    *,
    high_values: Sequence[float] | None = None,
    floor_hint: float,
) -> tuple[float, float]:
    values = [value for value in low_values if math.isfinite(value) and value > 0]
    if high_values is not None:
        values.extend(value for value in high_values if math.isfinite(value) and value > 0)
    if not values:
        return floor_hint, 1.0
    lower = max(0.0, min(values))
    upper = min(1.0, max(values))
    axis_min = max(
        0.0,
        min(0.95, max(floor_hint, math.floor((lower - 0.025) * 20) / 20)),
    )
    axis_max = min(1.0, math.ceil((upper + 0.015) * 20) / 20)
    if axis_max < 1.0 and upper > 0.92:
        axis_max = 1.0
    if axis_max - axis_min < 0.15:
        axis_min = max(0.0, axis_max - 0.15)
    return axis_min, axis_max


def _percent_ticks(minimum: float, maximum: float) -> list[float]:
    if maximum <= minimum:
        return [minimum]
    step = 0.10 if maximum - minimum >= 0.35 else 0.05
    start = math.ceil((minimum - 1e-9) / step) * step
    ticks: list[float] = []
    value = start
    while value <= maximum + 1e-9:
        ticks.append(round(value, 4))
        value += step
    for bound in (minimum, maximum):
        if all(abs(bound - tick) > 0.012 for tick in ticks):
            ticks.append(round(bound, 4))
    return sorted(ticks)


def _gap_ticks(max_gap: float) -> list[float]:
    if max_gap <= 0.10:
        step = 0.025
    elif max_gap <= 0.25:
        step = 0.05
    else:
        step = 0.10
    ticks = [0.0]
    value = step
    while value <= max_gap + 1e-9:
        ticks.append(round(value, 4))
        value += step
    return ticks


def _nice_cost_bounds(min_cost: float, max_cost: float) -> tuple[float, float]:
    if min_cost <= 0 or max_cost <= 0:
        return max(min_cost, 1e-6), max(max_cost, 1e-5)
    candidates = _nice_cost_candidates(min_cost / 2, max_cost * 2)
    lower = max((value for value in candidates if value <= min_cost), default=min_cost)
    upper = min((value for value in candidates if value >= max_cost), default=max_cost)
    if lower == upper:
        lower /= 2
        upper *= 2
    return lower, upper


def _nice_cost_candidates(min_cost: float, max_cost: float) -> list[float]:
    min_exp = math.floor(math.log10(max(min_cost, 1e-9))) - 1
    max_exp = math.ceil(math.log10(max_cost)) + 1
    candidates: list[float] = []
    for exponent in range(min_exp, max_exp + 1):
        scale = 10**exponent
        for multiplier in (1, 2, 5):
            value = multiplier * scale
            if min_cost <= value <= max_cost:
                candidates.append(value)
    return sorted(set(candidates))


def _cost_ticks(min_cost: float, max_cost: float) -> list[float]:
    if min_cost <= 0 or max_cost <= 0:
        return []
    if min_cost == max_cost:
        return [min_cost]
    ticks = [min_cost]
    for exponent in range(math.floor(math.log10(min_cost)), math.ceil(math.log10(max_cost)) + 1):
        tick = 10**exponent
        if min_cost < tick < max_cost:
            ticks.append(tick)
    ticks.append(max_cost)
    return ticks


def _cost_tick_label(cost: float) -> str:
    if cost < 0.001:
        return f"${cost:.5f}".rstrip("0")
    if cost < 0.01:
        return f"${cost:.4f}".rstrip("0")
    if cost < 1:
        return f"${cost:.2f}" if cost >= 0.10 else f"${cost:.3f}".rstrip("0")
    return f"${cost:.2f}"


def _frontier_label_set(
    points: Sequence[tuple[dict[str, str], float, float]],
) -> set[str]:
    general_points = [
        point for point in points if not _is_special_purpose_display_row(point[0])
    ]
    if general_points:
        points = general_points
    by_cost = sorted(
        points,
        key=lambda item: (item[2], -item[1], item[0].get("label", "")),
    )
    by_low_accuracy = sorted(
        points,
        key=lambda item: (item[1], -item[2], item[0].get("label", "")),
    )
    labels: set[str] = set()
    labels.update(row.get("label", "") for row, _, _ in by_cost[:1])
    labels.update(row.get("label", "") for row, _, _ in by_low_accuracy[:1])
    return labels


def _frontier_label_position(
    x: float,
    y: float,
    label: str,
    *,
    bounds: tuple[float, float, float, float],
    existing_boxes: Sequence[tuple[float, float, float, float]],
) -> tuple[float, float, tuple[float, float, float, float]]:
    left, bottom, right, top = bounds
    label_width = min(120.0, max(44.0, len(label) * 5.2))
    label_height = 13.0
    candidates = (
        (6.0, 6.0),
        (6.0, -14.0),
        (-label_width - 6.0, 6.0),
        (-label_width - 6.0, -14.0),
        (12.0, 18.0),
        (-label_width - 6.0, 18.0),
    )
    for dx, dy in candidates:
        label_x = min(max(x + dx, left + 2), right - label_width - 2)
        label_y = min(max(y + dy, bottom + 4), top - label_height - 2)
        box = (
            label_x,
            label_y - 2.0,
            label_x + label_width,
            label_y + label_height,
        )
        if not any(_boxes_overlap(box, existing) for existing in existing_boxes):
            return label_x, label_y, box
    label_x = min(max(x + 6.0, left + 2), right - label_width - 2)
    label_y = min(max(y + 6.0, bottom + 4), top - label_height - 2)
    box = (label_x, label_y - 2.0, label_x + label_width, label_y + label_height)
    return label_x, label_y, box


def _boxes_overlap(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
) -> bool:
    return not (
        first[2] < second[0]
        or second[2] < first[0]
        or first[3] < second[1]
        or second[3] < first[1]
    )


def _pareto_frontier_labels(
    points: Sequence[tuple[dict[str, str], float, float]],
    *,
    limit: int,
) -> set[str]:
    """Return low-cost, non-dominated model labels for sparse frontier annotation."""
    frontier: list[str] = []
    best_accuracy = -1.0
    for row, strict, _cost in sorted(
        points,
        key=lambda item: (item[2], -item[1], item[0].get("label", "")),
    ):
        if strict > best_accuracy:
            frontier.append(row.get("label", ""))
            best_accuracy = strict
        if len(frontier) >= limit:
            break
    return set(frontier)


def _pdf_escape(text: str) -> str:
    safe = text.encode("ascii", errors="replace").decode("ascii")
    return safe.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _latex_escape(value: object) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)
