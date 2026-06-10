"""Build the pass^3 effort-cost curve report from repeated-run summaries."""
# ruff: noqa: E501

from __future__ import annotations

import csv
import html
import itertools
import math
import shutil
import statistics
import subprocess
import tempfile
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ITEMS = 224
REPORT_DIR = ROOT / "docs/reports/2026-06-06-pass3-effort-cost-curves"
POINTS_CSV = REPORT_DIR / "pass3-effort-cost-curve-points.csv"
SVG_OUT = REPORT_DIR / "pass3-answer-log-cost.svg"
NEW_RESULTS_CSV = ROOT / "docs/research/2026-06-06-gpt-5-5-sonnet-4-6-8x28-pass3-results.csv"
NEW_RESULTS_MD = ROOT / "docs/research/2026-06-06-gpt-5-5-sonnet-4-6-8x28-pass3-results.md"
NEW_INSTABILITY_CSV = (
    ROOT / "docs/research/2026-06-06-gpt-5-5-sonnet-4-6-8x28-pass3-item-instability.csv"
)
GEMINI_RESULTS_CSV = (
    ROOT / "docs/research/2026-06-06-gemini-3-5-flash-3-1-flash-lite-8x28-pass3-results.csv"
)
GEMINI_RESULTS_MD = (
    ROOT / "docs/research/2026-06-06-gemini-3-5-flash-3-1-flash-lite-8x28-pass3-results.md"
)
GEMINI_INSTABILITY_CSV = (
    ROOT
    / "docs/research/2026-06-06-gemini-3-5-flash-3-1-flash-lite-8x28-pass3-item-instability.csv"
)

BACKGROUND_COLOR = "#fbfaf7"
FOREGROUND_COLOR = "#1d1d1f"
MUTED_COLOR = "#5a5d64"
GRID_COLOR = "#ded8ce"
WEB_FONT = "Segoe UI"

MODEL_COLORS = {
    "GPT-5.4 nano": "#d04f83",
    "GPT-5.4 mini": "#7d8b17",
    "GPT-5.5": "#2075b9",
    "Claude Sonnet 4.6": "#c25f3a",
    "Gemini 3.5 Flash": "#2f8f66",
    "Gemini 3.1 Flash Lite": "#8b62b8",
}

EFFORT_ORDER = {
    "minimal": 0,
    "none": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "xhigh": 4,
    "max": 5,
}

MODEL_ORDER = {
    "GPT-5.4 nano": 0,
    "GPT-5.4 mini": 1,
    "GPT-5.5": 2,
    "Claude Sonnet 4.6": 3,
    "Gemini 3.5 Flash": 4,
    "Gemini 3.1 Flash Lite": 5,
}

LABEL_OFFSETS = {
    ("GPT-5.4 nano", "none"): (14, 48),
    ("GPT-5.4 nano", "low"): (-24, -30),
    ("GPT-5.4 nano", "medium"): (-30, -38),
    ("GPT-5.4 nano", "high"): (-28, -42),
    ("GPT-5.4 mini", "none"): (-38, 46),
    ("GPT-5.4 mini", "low"): (-70, -20),
    ("GPT-5.4 mini", "medium"): (-54, 42),
    ("GPT-5.4 mini", "high"): (-36, -38),
    ("GPT-5.5", "none"): (-28, 44),
    ("GPT-5.5", "low"): (-70, -24),
    ("GPT-5.5", "medium"): (-122, 58),
    ("GPT-5.5", "high"): (18, 52),
    ("GPT-5.5", "xhigh"): (18, 10),
    ("Claude Sonnet 4.6", "low"): (-40, 48),
    ("Claude Sonnet 4.6", "medium"): (-112, 38),
    ("Claude Sonnet 4.6", "high"): (20, 38),
    ("Claude Sonnet 4.6", "max"): (20, -34),
    ("Gemini 3.5 Flash", "minimal"): (16, 48),
    ("Gemini 3.5 Flash", "low"): (-92, 42),
    ("Gemini 3.5 Flash", "medium"): (-116, -30),
    ("Gemini 3.5 Flash", "high"): (22, 22),
    ("Gemini 3.1 Flash Lite", "minimal"): (16, 48),
    ("Gemini 3.1 Flash Lite", "low"): (-82, 16),
    ("Gemini 3.1 Flash Lite", "medium"): (-112, -28),
    ("Gemini 3.1 Flash Lite", "high"): (22, 24),
}


@dataclass(frozen=True)
class SourceSpec:
    root: Path
    group_prefix: str
    provider: str
    curve: str
    model: str
    new_run: bool


@dataclass(frozen=True)
class TrialData:
    summary_dir: Path
    answer: dict[str, bool]
    strict: dict[str, bool]
    correct: dict[str, bool]
    family: dict[str, str]
    question: dict[str, str]
    cost_usd: float
    total_tokens: int
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    provider_errors: int
    timeouts: int


@dataclass(frozen=True)
class MetricSummary:
    pass1: float
    pass_pow_3: float
    pass_at_3: float
    pass_pow_3_first3: float
    pass_at_3_first3: float
    unstable_item_rate: float
    pairwise_disagreement: float
    trial_min: float
    trial_max: float
    trial_range: float
    trial_stdev: float


@dataclass(frozen=True)
class GroupSummary:
    provider: str
    curve: str
    model: str
    mode: str
    group_id: str
    trials: int
    items: int
    attempts: int
    answer: MetricSummary
    strict: MetricSummary
    correct: MetricSummary
    pass3_cost_usd: float
    total_cost_usd: float
    total_tokens: int
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    provider_errors: int
    timeouts: int
    summary_dirs: list[Path]


@dataclass(frozen=True)
class ChartPoint:
    provider: str
    curve: str
    model: str
    effort: str
    label: str
    answer_pass3_pct: float
    strict_pass3_pct: float
    correct_pass3_pct: float
    pass3_cost_usd: float
    total_cost_usd: float
    trials: int
    source_root: str
    provider_errors: int


RESULT_FIELDNAMES = [
    "provider",
    "curve",
    "model",
    "mode",
    "trials",
    "items",
    "attempts",
    "strict_pass1",
    "strict_pass_pow_3_combo_mean",
    "strict_pass_at_3_combo_mean",
    "strict_pass_pow_3_first3",
    "strict_pass_at_3_first3",
    "strict_unstable_item_rate",
    "strict_pairwise_disagreement",
    "strict_trial_min",
    "strict_trial_max",
    "strict_trial_range",
    "strict_trial_stdev",
    "answer_pass1",
    "answer_pass_pow_3_combo_mean",
    "answer_pass_at_3_combo_mean",
    "answer_pass_pow_3_first3",
    "answer_pass_at_3_first3",
    "answer_unstable_item_rate",
    "answer_pairwise_disagreement",
    "answer_trial_min",
    "answer_trial_max",
    "answer_trial_range",
    "answer_trial_stdev",
    "correct_pass1",
    "correct_pass_pow_3_combo_mean",
    "correct_pass_at_3_combo_mean",
    "correct_unstable_item_rate",
    "correct_pairwise_disagreement",
    "provider_errors",
    "timeouts",
    "pass3_cost_usd",
    "total_cost_usd",
    "total_tokens",
    "input_tokens",
    "output_tokens",
    "reasoning_tokens",
    "reasoning_token_share",
    "summary_dirs",
]


SOURCES = [
    SourceSpec(
        ROOT / "results/summaries/gpt-5-4-nano-passk-8x28-20260606",
        "gpt-5-4-nano",
        "OpenAI",
        "GPT-5.4 nano",
        "openai/gpt-5.4-nano",
        False,
    ),
    SourceSpec(
        ROOT / "results/summaries/gpt-5-4-mini-passk-8x28-20260606",
        "gpt-5-4-mini",
        "OpenAI",
        "GPT-5.4 mini",
        "openai/gpt-5.4-mini",
        False,
    ),
    SourceSpec(
        ROOT / "results/summaries/gpt-5-5-sonnet-4-6-pass3-8x28-20260606",
        "gpt-5-5",
        "OpenAI",
        "GPT-5.5",
        "openai/gpt-5.5",
        True,
    ),
    SourceSpec(
        ROOT / "results/summaries/gpt-5-5-sonnet-4-6-pass3-8x28-20260606",
        "sonnet-4-6",
        "Anthropic",
        "Claude Sonnet 4.6",
        "anthropic/claude-sonnet-4-6",
        True,
    ),
    SourceSpec(
        ROOT / "results/summaries/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606",
        "gemini-3-5-flash",
        "Google",
        "Gemini 3.5 Flash",
        "google/gemini-3.5-flash",
        True,
    ),
    SourceSpec(
        ROOT / "results/summaries/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606",
        "gemini-3-1-flash-lite",
        "Google",
        "Gemini 3.1 Flash Lite",
        "google/gemini-3.1-flash-lite",
        True,
    ),
]


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    NEW_RESULTS_CSV.parent.mkdir(parents=True, exist_ok=True)

    summaries = build_summaries()
    write_new_run_results(summaries)
    write_new_instability(summaries)
    write_gemini_results(summaries)
    write_gemini_instability(summaries)
    chart_points = chart_points_from_summaries(summaries)
    write_chart_points(chart_points)
    write_chart(chart_points, SVG_OUT)
    rasterize_svgs([SVG_OUT])
    write_index(chart_points)
    return 0


def build_summaries() -> list[GroupSummary]:
    summaries: list[GroupSummary] = []
    for spec in SOURCES:
        for group_id, trial_dirs in grouped_trial_dirs(spec).items():
            mode = group_id.removeprefix(f"{spec.group_prefix}-")
            if mode not in EFFORT_ORDER:
                continue
            trials = [read_trial_data(path) for path in trial_dirs]
            summaries.append(summarize_group(spec, group_id, mode, trials))
    return sorted(
        summaries,
        key=lambda row: (
            MODEL_ORDER.get(row.curve, 99),
            EFFORT_ORDER.get(row.mode, 99),
        ),
    )


def grouped_trial_dirs(spec: SourceSpec) -> dict[str, list[Path]]:
    runs_dir = spec.root / "runs"
    if not runs_dir.exists():
        raise FileNotFoundError(runs_dir)
    groups: dict[str, list[Path]] = defaultdict(list)
    for run_dir in sorted(runs_dir.iterdir()):
        if not run_dir.is_dir() or not run_dir.name.startswith(f"{spec.group_prefix}-"):
            continue
        if "-trial-" not in run_dir.name:
            continue
        group_id, _trial = run_dir.name.rsplit("-trial-", 1)
        groups[group_id].append(run_dir)
    return {group_id: sorted(paths) for group_id, paths in sorted(groups.items())}


def read_trial_data(summary_dir: Path) -> TrialData:
    usage_path = summary_dir / "usage_by_sample.csv"
    if not usage_path.exists():
        raise FileNotFoundError(usage_path)
    with usage_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    sample_ids = [row["sample_id"] for row in rows]
    if len(rows) != EXPECTED_ITEMS or len(set(sample_ids)) != EXPECTED_ITEMS:
        raise ValueError(
            f"{usage_path} has {len(rows)} rows and {len(set(sample_ids))} distinct sample ids; expected {EXPECTED_ITEMS}"
        )
    return TrialData(
        summary_dir=summary_dir,
        answer={row["sample_id"]: truthy(row["answer_correct"]) for row in rows},
        strict={row["sample_id"]: truthy(row["strict_correct"]) for row in rows},
        correct={row["sample_id"]: truthy(row["correct"]) for row in rows},
        family={row["sample_id"]: row.get("family", "") for row in rows},
        question={row["sample_id"]: row.get("question", "") for row in rows},
        cost_usd=sum(float(row.get("estimated_cost_usd") or 0) for row in rows),
        total_tokens=sum(to_int(row.get("total_tokens")) for row in rows),
        input_tokens=sum(to_int(row.get("input_tokens")) for row in rows),
        output_tokens=sum(to_int(row.get("output_tokens")) for row in rows),
        reasoning_tokens=sum(to_int(row.get("reasoning_tokens")) for row in rows),
        provider_errors=sum(truthy(row.get("provider_error")) for row in rows),
        timeouts=sum(truthy(row.get("timeout")) for row in rows),
    )


def summarize_group(
    spec: SourceSpec, group_id: str, mode: str, trials: list[TrialData]
) -> GroupSummary:
    if len(trials) < 3:
        raise ValueError(f"{group_id} has {len(trials)} trials; pass^3 needs at least 3")
    sample_ids = sorted(trials[0].answer)
    for trial in trials[1:]:
        if sorted(trial.answer) != sample_ids:
            raise ValueError(f"{group_id}: sample id mismatch across trials")
    pass3_costs = [
        sum(trials[index].cost_usd for index in combo)
        for combo in itertools.combinations(range(len(trials)), 3)
    ]
    return GroupSummary(
        provider=spec.provider,
        curve=spec.curve,
        model=spec.model,
        mode=mode,
        group_id=group_id,
        trials=len(trials),
        items=len(sample_ids),
        attempts=len(sample_ids) * len(trials),
        answer=summarize_metric(trials, "answer"),
        strict=summarize_metric(trials, "strict"),
        correct=summarize_metric(trials, "correct"),
        pass3_cost_usd=statistics.mean(pass3_costs),
        total_cost_usd=sum(trial.cost_usd for trial in trials),
        total_tokens=sum(trial.total_tokens for trial in trials),
        input_tokens=sum(trial.input_tokens for trial in trials),
        output_tokens=sum(trial.output_tokens for trial in trials),
        reasoning_tokens=sum(trial.reasoning_tokens for trial in trials),
        provider_errors=sum(trial.provider_errors for trial in trials),
        timeouts=sum(trial.timeouts for trial in trials),
        summary_dirs=[trial.summary_dir for trial in trials],
    )


def summarize_metric(trials: list[TrialData], metric_name: str) -> MetricSummary:
    metric_trials = [getattr(trial, metric_name) for trial in trials]
    sample_ids = sorted(metric_trials[0])
    trial_rates = [sum(values.values()) / len(sample_ids) for values in metric_trials]
    combo_pass_pow: list[float] = []
    combo_pass_at: list[float] = []
    for combo in itertools.combinations(range(len(metric_trials)), 3):
        combo_pass_pow.append(
            sum(all(metric_trials[index][sample_id] for index in combo) for sample_id in sample_ids)
            / len(sample_ids)
        )
        combo_pass_at.append(
            sum(any(metric_trials[index][sample_id] for index in combo) for sample_id in sample_ids)
            / len(sample_ids)
        )
    success_counts = {
        sample_id: sum(values[sample_id] for values in metric_trials) for sample_id in sample_ids
    }
    disagreements: list[int] = []
    for sample_id in sample_ids:
        values = [values_by_sample[sample_id] for values_by_sample in metric_trials]
        disagreements.extend(
            abs(int(left) - int(right)) for left, right in itertools.combinations(values, 2)
        )
    return MetricSummary(
        pass1=statistics.mean(trial_rates),
        pass_pow_3=statistics.mean(combo_pass_pow),
        pass_at_3=statistics.mean(combo_pass_at),
        pass_pow_3_first3=sum(
            all(metric_trials[index][sample_id] for index in range(3)) for sample_id in sample_ids
        )
        / len(sample_ids),
        pass_at_3_first3=sum(
            any(metric_trials[index][sample_id] for index in range(3)) for sample_id in sample_ids
        )
        / len(sample_ids),
        unstable_item_rate=sum(
            0 < successes < len(metric_trials) for successes in success_counts.values()
        )
        / len(sample_ids),
        pairwise_disagreement=statistics.mean(disagreements),
        trial_min=min(trial_rates),
        trial_max=max(trial_rates),
        trial_range=max(trial_rates) - min(trial_rates),
        trial_stdev=statistics.pstdev(trial_rates),
    )


def write_new_run_results(summaries: list[GroupSummary]) -> None:
    new_summaries = [
        summary for summary in summaries if summary.curve in {"GPT-5.5", "Claude Sonnet 4.6"}
    ]
    fieldnames = [
        "provider",
        "curve",
        "model",
        "mode",
        "trials",
        "items",
        "attempts",
        "strict_pass1",
        "strict_pass_pow_3_combo_mean",
        "strict_pass_at_3_combo_mean",
        "strict_pass_pow_3_first3",
        "strict_pass_at_3_first3",
        "strict_unstable_item_rate",
        "strict_pairwise_disagreement",
        "strict_trial_min",
        "strict_trial_max",
        "strict_trial_range",
        "strict_trial_stdev",
        "answer_pass1",
        "answer_pass_pow_3_combo_mean",
        "answer_pass_at_3_combo_mean",
        "answer_pass_pow_3_first3",
        "answer_pass_at_3_first3",
        "answer_unstable_item_rate",
        "answer_pairwise_disagreement",
        "answer_trial_min",
        "answer_trial_max",
        "answer_trial_range",
        "answer_trial_stdev",
        "correct_pass1",
        "correct_pass_pow_3_combo_mean",
        "correct_pass_at_3_combo_mean",
        "correct_unstable_item_rate",
        "correct_pairwise_disagreement",
        "provider_errors",
        "timeouts",
        "pass3_cost_usd",
        "total_cost_usd",
        "total_tokens",
        "input_tokens",
        "output_tokens",
        "reasoning_tokens",
        "reasoning_token_share",
        "summary_dirs",
    ]
    with NEW_RESULTS_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(result_row(summary) for summary in new_summaries)
    write_new_results_markdown(new_summaries)


def write_gemini_results(summaries: list[GroupSummary]) -> None:
    gemini_summaries = [
        summary
        for summary in summaries
        if summary.curve in {"Gemini 3.5 Flash", "Gemini 3.1 Flash Lite"}
    ]
    write_results_csv(GEMINI_RESULTS_CSV, gemini_summaries)
    write_gemini_results_markdown(gemini_summaries)


def write_results_csv(path: Path, summaries: list[GroupSummary]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(result_row(summary) for summary in summaries)


def result_row(summary: GroupSummary) -> dict[str, str]:
    row = {
        "provider": summary.provider,
        "curve": summary.curve,
        "model": summary.model,
        "mode": summary.mode,
        "trials": str(summary.trials),
        "items": str(summary.items),
        "attempts": str(summary.attempts),
        "provider_errors": str(summary.provider_errors),
        "timeouts": str(summary.timeouts),
        "pass3_cost_usd": trim(summary.pass3_cost_usd),
        "total_cost_usd": trim(summary.total_cost_usd),
        "total_tokens": str(summary.total_tokens),
        "input_tokens": str(summary.input_tokens),
        "output_tokens": str(summary.output_tokens),
        "reasoning_tokens": str(summary.reasoning_tokens),
        "reasoning_token_share": trim(
            summary.reasoning_tokens / summary.total_tokens if summary.total_tokens else 0
        ),
        "summary_dirs": ";".join(str(path.relative_to(ROOT)) for path in summary.summary_dirs),
    }
    for prefix, metric in [
        ("strict", summary.strict),
        ("answer", summary.answer),
        ("correct", summary.correct),
    ]:
        row[f"{prefix}_pass1"] = trim(metric.pass1)
        row[f"{prefix}_pass_pow_3_combo_mean"] = trim(metric.pass_pow_3)
        row[f"{prefix}_pass_at_3_combo_mean"] = trim(metric.pass_at_3)
        row[f"{prefix}_unstable_item_rate"] = trim(metric.unstable_item_rate)
        row[f"{prefix}_pairwise_disagreement"] = trim(metric.pairwise_disagreement)
        if prefix != "correct":
            row[f"{prefix}_pass_pow_3_first3"] = trim(metric.pass_pow_3_first3)
            row[f"{prefix}_pass_at_3_first3"] = trim(metric.pass_at_3_first3)
            row[f"{prefix}_trial_min"] = trim(metric.trial_min)
            row[f"{prefix}_trial_max"] = trim(metric.trial_max)
            row[f"{prefix}_trial_range"] = trim(metric.trial_range)
            row[f"{prefix}_trial_stdev"] = trim(metric.trial_stdev)
    return row


def write_new_results_markdown(summaries: list[GroupSummary]) -> None:
    total_cost = sum(summary.total_cost_usd for summary in summaries)
    total_errors = sum(summary.provider_errors for summary in summaries)
    rows = "\n".join(
        f"| {summary.curve} | {summary.mode} | {fmt_pct(summary.answer.pass1)} | {fmt_pct(summary.answer.pass_pow_3)} | {fmt_pct(summary.strict.pass_pow_3)} | {fmt_cost(summary.pass3_cost_usd)} | {summary.provider_errors} |"
        for summary in summaries
    )
    provider_rows = "\n".join(
        f"- {sample}"
        for sample in provider_error_samples(
            ROOT / "results/summaries/gpt-5-5-sonnet-4-6-pass3-8x28-20260606"
        )
    )
    if not provider_rows:
        provider_rows = "- None."
    md = f"""---
title: GPT-5.5 And Sonnet 4.6 8x28 Pass^3 Results
date: 2026-06-06
type: report
status: complete
---

# GPT-5.5 And Sonnet 4.6 8x28 Pass^3 Results

## Run

- Panel: `configs/gpt_5_5_sonnet_4_6_pass3_8x28_20260606_panel.yaml`
- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl`
- Status ledger: `results/summaries/gpt-5-5-sonnet-4-6-pass3-8x28-20260606/status.jsonl`
- Entries: 27 passed / 27 total.
- Cache busting: launched with `--no-cache --no-skip-completed`.
- Concurrency: each Inspect eval used `--max-connections=128`.
- Scoring: `--score-on-error` was enabled, so provider-error samples count as scored failures.

OpenAI Responses emitted the expected provider warning that the `seed` parameter is unsupported. Anthropic adaptive-thinking entries were generated with `reasoning_effort` settings.

## Answer-Correct Pass^3

Primary score here is `answer_correct` pass^3. `strict_correct` pass^3 is shown beside it for format-sensitive comparison.

| model | mode | answer pass1 | answer pass^3 | strict pass^3 | pass^3 cost | provider errors |
|---|---:|---:|---:|---:|---:|---:|
{rows}

Total measured cost for these 27 runs: {fmt_cost(total_cost)}. Provider-error samples scored: {total_errors}.

## Provider-Error Samples

{provider_rows}

## Chart

The combined pass^3 cost curve is in `docs/reports/2026-06-06-pass3-effort-cost-curves/pass3-answer-log-cost.svg`.
"""
    NEW_RESULTS_MD.write_text(md, encoding="utf-8")


def write_gemini_results_markdown(summaries: list[GroupSummary]) -> None:
    total_cost = sum(summary.total_cost_usd for summary in summaries)
    total_errors = sum(summary.provider_errors for summary in summaries)
    rows = "\n".join(
        f"| {summary.curve} | {summary.mode} | {fmt_pct(summary.answer.pass1)} | {fmt_pct(summary.answer.pass_pow_3)} | {fmt_pct(summary.strict.pass_pow_3)} | {fmt_cost(summary.pass3_cost_usd)} | {summary.provider_errors} |"
        for summary in summaries
    )
    provider_rows = "\n".join(
        f"- {sample}"
        for sample in provider_error_samples(
            ROOT / "results/summaries/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606"
        )
    )
    if not provider_rows:
        provider_rows = "- None."
    md = f"""---
title: Gemini 3.5 Flash And 3.1 Flash Lite 8x28 Pass^3 Results
date: 2026-06-06
type: report
status: complete
---

# Gemini 3.5 Flash And 3.1 Flash Lite 8x28 Pass^3 Results

## Run

- Panel: `configs/gemini_3_5_flash_3_1_flash_lite_pass3_8x28_20260606_panel.yaml`
- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl`
- Status ledger: `results/summaries/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606/status.jsonl`
- Entries: 24 passed / 24 total.
- Cache busting: launched with `--no-cache --no-skip-completed`.
- Concurrency: each Inspect eval used `--max-connections=128`.
- Scoring: `--score-on-error` was enabled, so provider-error samples count as scored failures.
- Direct Gemini route: `google/gemini-3.5-flash` and `google/gemini-3.1-flash-lite`.

Gemini thinking settings were sent through Inspect `reasoning_effort`, which maps
to Gemini `thinkingLevel` for Gemini 3 models. The panel does not set explicit
generation seeds.

Cost note: with `runcost` 0.1.4, reported Gemini reasoning tokens are emitted as
`output_reasoning_tokens` ledger components and priced using the Gemini output
token rate. The component metadata records
`pricing_policy=gemini_thinking_tokens_priced_as_output_tokens`.

## Answer-Correct Pass^3

Primary score here is `answer_correct` pass^3. `strict_correct` pass^3 is shown beside it for format-sensitive comparison.

| model | mode | answer pass1 | answer pass^3 | strict pass^3 | pass^3 cost | provider errors |
|---|---:|---:|---:|---:|---:|---:|
{rows}

Total measured cost for these 24 runs: {fmt_cost(total_cost)}. Provider-error samples scored: {total_errors}.

## Provider-Error Samples

{provider_rows}

## Chart

The combined pass^3 cost curve is in `docs/reports/2026-06-06-pass3-effort-cost-curves/pass3-answer-log-cost.svg`.
"""
    GEMINI_RESULTS_MD.write_text(md, encoding="utf-8")


def provider_error_samples(root: Path) -> list[str]:
    samples: list[str] = []
    for usage_path in sorted((root / "runs").glob("*/usage_by_sample.csv")):
        with usage_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if truthy(row.get("provider_error")):
                    samples.append(
                        f"`{usage_path.parent.name}` `{row['sample_id']}` ({row.get('family', '')})"
                    )
    return samples


def write_new_instability(summaries: list[GroupSummary]) -> None:
    write_instability_csv(
        NEW_INSTABILITY_CSV,
        summaries,
        {"GPT-5.5", "Claude Sonnet 4.6"},
    )


def write_gemini_instability(summaries: list[GroupSummary]) -> None:
    write_instability_csv(
        GEMINI_INSTABILITY_CSV,
        summaries,
        {"Gemini 3.5 Flash", "Gemini 3.1 Flash Lite"},
    )


def write_instability_csv(
    out: Path,
    summaries: list[GroupSummary],
    curves: set[str],
) -> None:
    fieldnames = [
        "curve",
        "model",
        "mode",
        "sample_id",
        "family",
        "answer_successes",
        "strict_successes",
        "correct_successes",
        "trials",
        "question",
    ]
    rows: list[dict[str, str]] = []
    for summary in summaries:
        if summary.curve not in curves:
            continue
        trials = [read_trial_data(path) for path in summary.summary_dirs]
        sample_ids = sorted(trials[0].answer)
        for sample_id in sample_ids:
            answer_successes = sum(trial.answer[sample_id] for trial in trials)
            strict_successes = sum(trial.strict[sample_id] for trial in trials)
            correct_successes = sum(trial.correct[sample_id] for trial in trials)
            if not (
                0 < answer_successes < len(trials)
                or 0 < strict_successes < len(trials)
                or 0 < correct_successes < len(trials)
            ):
                continue
            rows.append(
                {
                    "curve": summary.curve,
                    "model": summary.model,
                    "mode": summary.mode,
                    "sample_id": sample_id,
                    "family": trials[0].family[sample_id],
                    "answer_successes": str(answer_successes),
                    "strict_successes": str(strict_successes),
                    "correct_successes": str(correct_successes),
                    "trials": str(len(trials)),
                    "question": trials[0].question[sample_id],
                }
            )
    rows.sort(
        key=lambda row: (
            row["curve"],
            EFFORT_ORDER.get(row["mode"], 99),
            abs(int(row["answer_successes"]) - int(row["trials"]) / 2),
            row["sample_id"],
        )
    )
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def chart_points_from_summaries(summaries: list[GroupSummary]) -> list[ChartPoint]:
    points: list[ChartPoint] = []
    for summary in summaries:
        points.append(
            ChartPoint(
                provider=summary.provider,
                curve=summary.curve,
                model=summary.model,
                effort=summary.mode,
                label=f"{summary.curve} {summary.mode}",
                answer_pass3_pct=summary.answer.pass_pow_3 * 100,
                strict_pass3_pct=summary.strict.pass_pow_3 * 100,
                correct_pass3_pct=summary.correct.pass_pow_3 * 100,
                pass3_cost_usd=summary.pass3_cost_usd,
                total_cost_usd=summary.total_cost_usd,
                trials=summary.trials,
                source_root=str(summary.summary_dirs[0].parents[1].relative_to(ROOT)),
                provider_errors=summary.provider_errors,
            )
        )
    return points


def write_chart_points(points: list[ChartPoint]) -> None:
    fieldnames = [
        "provider",
        "curve",
        "model",
        "mode",
        "label",
        "answer_pass_pow_3_pct",
        "strict_pass_pow_3_pct",
        "correct_pass_pow_3_pct",
        "pass3_cost_usd",
        "total_cost_usd",
        "trials",
        "source_root",
        "provider_errors",
    ]
    with POINTS_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for point in points:
            writer.writerow(
                {
                    "provider": point.provider,
                    "curve": point.curve,
                    "model": point.model,
                    "mode": point.effort,
                    "label": point.label,
                    "answer_pass_pow_3_pct": trim(point.answer_pass3_pct),
                    "strict_pass_pow_3_pct": trim(point.strict_pass3_pct),
                    "correct_pass_pow_3_pct": trim(point.correct_pass3_pct),
                    "pass3_cost_usd": trim(point.pass3_cost_usd),
                    "total_cost_usd": trim(point.total_cost_usd),
                    "trials": str(point.trials),
                    "source_root": point.source_root,
                    "provider_errors": str(point.provider_errors),
                }
            )


def write_chart(points: list[ChartPoint], out: Path) -> None:
    chart = SvgChart(
        title="Answer Pass^3 vs Log Cost",
        subtitle="224-question 8x28; y = answer_correct pass^3; x = mean three-trial cost",
        x_label="Pass^3 run cost, USD (log scale)",
        y_label="Answer-correct pass^3 (%)",
        points=points,
    )
    chart.start()
    for curve in sorted({point.curve for point in points}, key=model_order):
        curve_points = sorted(
            [point for point in points if point.curve == curve],
            key=lambda point: EFFORT_ORDER.get(point.effort, 99),
        )
        color = MODEL_COLORS.get(curve, "#6f6a60")
        chart.line(curve_points, color=color)
        for point in curve_points:
            chart.point(point, color=color)
    chart.legend(
        [
            (curve, MODEL_COLORS.get(curve, "#6f6a60"))
            for curve in sorted({point.curve for point in points}, key=model_order)
        ]
    )
    chart.footnote(
        "Cost for 5-trial nano/mini sources is the mean cost of all 3-trial subsets; y uses answer_correct, not strict_correct."
    )
    out.write_text(chart.finish(), encoding="utf-8")


class SvgChart:
    def __init__(
        self,
        *,
        title: str,
        subtitle: str,
        x_label: str,
        y_label: str,
        points: list[ChartPoint],
        width: int = 1900,
        height: int = 1120,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.x_label = x_label
        self.y_label = y_label
        self.points = points
        self.width = width
        self.height = height
        self.left = 170
        self.right = 430
        self.top = 190
        self.bottom = 170
        self.plot_w = self.width - self.left - self.right
        self.plot_h = self.height - self.top - self.bottom
        self.x_min = nice_log_lower(min(point.pass3_cost_usd for point in points))
        self.x_max = nice_log_upper(max(point.pass3_cost_usd for point in points))
        self.y_min = 78.0
        self.y_max = 101.0
        self.parts: list[str] = []

    def start(self) -> None:
        self.parts.extend(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">',
                "<style>",
                f"text{{font-family:-apple-system,BlinkMacSystemFont,'{esc(WEB_FONT)}',sans-serif;fill:{FOREGROUND_COLOR}}}",
                f".title{{font-size:54px;font-weight:800}}.subtitle{{font-size:30px;fill:{MUTED_COLOR}}}",
                f".axis{{font-size:30px;font-weight:700}}.tick{{font-size:24px;fill:{MUTED_COLOR}}}",
                f".label{{font-size:25px;font-weight:750}}.foot{{font-size:21px;fill:{MUTED_COLOR}}}",
                "</style>",
                f'<rect width="100%" height="100%" fill="{BACKGROUND_COLOR}"/>',
                f'<text class="title" x="{centered_text_x(self.title, 54, self.width / 2, bold=True):.1f}" y="78">{esc(self.title)}</text>',
                f'<text class="subtitle" x="{centered_text_x(self.subtitle, 30, self.width / 2):.1f}" y="124">{esc(self.subtitle)}</text>',
            ]
        )
        self.grid()

    def grid(self) -> None:
        for tick in self.y_ticks():
            y = self.y(tick)
            label = f"{tick:.0f}%"
            self.parts.append(
                f'<line x1="{self.left}" y1="{y:.1f}" x2="{self.width - self.right}" y2="{y:.1f}" stroke="{GRID_COLOR}" stroke-width="2"/>'
            )
            self.parts.append(
                f'<text class="tick" x="{self.left - 24 - approx_text_width(label, 24):.1f}" y="{y + 8:.1f}">{label}</text>'
            )
        for tick in self.x_ticks():
            x = self.x(tick)
            label = format_cost(tick)
            self.parts.append(
                f'<line x1="{x:.1f}" y1="{self.top}" x2="{x:.1f}" y2="{self.height - self.bottom}" stroke="{GRID_COLOR}" stroke-width="2"/>'
            )
            self.parts.append(
                f'<text class="tick" x="{centered_text_x(label, 24, x):.1f}" y="{self.height - self.bottom + 46}">{esc(label)}</text>'
            )
        self.parts.append(
            f'<line x1="{self.left}" y1="{self.height - self.bottom}" x2="{self.width - self.right}" y2="{self.height - self.bottom}" stroke="{FOREGROUND_COLOR}" stroke-width="4"/>'
        )
        self.parts.append(
            f'<line x1="{self.left}" y1="{self.top}" x2="{self.left}" y2="{self.height - self.bottom}" stroke="{FOREGROUND_COLOR}" stroke-width="4"/>'
        )
        self.parts.append(
            f'<text class="axis" x="{self.left}" y="{self.top - 32}">{esc(self.y_label)}</text>'
        )
        self.parts.append(
            f'<text class="axis" x="{centered_text_x(self.x_label, 30, self.left + self.plot_w / 2, bold=True):.1f}" y="{self.height - 65}">{esc(self.x_label)}</text>'
        )

    def line(self, points: list[ChartPoint], *, color: str) -> None:
        if len(points) < 2:
            return
        coords = " ".join(
            f"{self.x(point.pass3_cost_usd):.1f},{self.y(point.answer_pass3_pct):.1f}"
            for point in points
        )
        self.parts.append(
            f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def point(self, point: ChartPoint, *, color: str) -> None:
        x = self.x(point.pass3_cost_usd)
        y = self.y(point.answer_pass3_pct)
        dx, dy = LABEL_OFFSETS.get((point.curve, point.effort), (14, -16))
        title = (
            f"{point.label}: answer pass^3 {point.answer_pass3_pct:.2f}% at "
            f"{format_cost(point.pass3_cost_usd)}"
        )
        self.parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{color}" stroke="{BACKGROUND_COLOR}" stroke-width="4"><title>{esc(title)}</title></circle>'
        )
        self.parts.append(
            f'<text class="label" x="{x + dx:.1f}" y="{y + dy:.1f}">{esc(short_effort(point.effort))}</text>'
        )

    def legend(self, entries: list[tuple[str, str]]) -> None:
        x = self.width - self.right + 70
        y = self.top + 15
        self.parts.append(f'<text class="label" x="{x}" y="{y}">Models</text>')
        for index, (name, color) in enumerate(entries):
            yy = y + 48 + index * 48
            self.parts.append(
                f'<line x1="{x}" y1="{yy - 8}" x2="{x + 70}" y2="{yy - 8}" stroke="{color}" stroke-width="7"/>'
            )
            self.parts.append(f'<text class="tick" x="{x + 86}" y="{yy}">{esc(name)}</text>')
        y2 = y + 48 + len(entries) * 48 + 52
        notes = [
            "Each point is a mode.",
            "pass^3 = all 3 attempts right.",
            "answer_correct excludes format.",
            "min = minimal.",
            "med = medium.",
        ]
        for index, note in enumerate(notes):
            self.parts.append(
                f'<text class="tick" x="{x}" y="{y2 + index * 36}">{esc(note)}</text>'
            )

    def footnote(self, text: str) -> None:
        self.parts.append(
            f'<text class="foot" x="{self.left}" y="{self.height - 22}">{esc(text)}</text>'
        )

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"

    def x(self, value: float) -> float:
        start = math.log10(self.x_min)
        end = math.log10(self.x_max)
        frac = (math.log10(value) - start) / (end - start)
        return self.left + frac * self.plot_w

    def y(self, value: float) -> float:
        frac = (value - self.y_min) / (self.y_max - self.y_min)
        return self.height - self.bottom - frac * self.plot_h

    def x_ticks(self) -> list[float]:
        candidates = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0]
        return [tick for tick in candidates if self.x_min <= tick <= self.x_max]

    def y_ticks(self) -> list[float]:
        return [80.0, 85.0, 90.0, 95.0, 100.0]


def write_index(points: list[ChartPoint]) -> None:
    best = max(points, key=lambda point: point.answer_pass3_pct)
    cheapest = min(points, key=lambda point: point.pass3_cost_usd)
    html_text = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pass^3 Effort-Cost Curve</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"{esc(WEB_FONT)}",sans-serif;margin:32px;background:{BACKGROUND_COLOR};color:{FOREGROUND_COLOR}}}
main{{max-width:1540px;margin:auto}}
img{{display:block;width:100%;height:auto;margin:24px 0 34px;border:1px solid {GRID_COLOR};background:{BACKGROUND_COLOR}}}
code{{font-size:.95em}}
p{{line-height:1.45}}
</style>
</head>
<body>
<main>
<h1>Pass^3 Effort-Cost Curve</h1>
<p>Y axis is answer-correct pass^3, not strict correctness. X axis is log-scaled pass^3 run cost. For the five-trial GPT-5.4 nano/mini sources, cost is the mean cost of all three-trial subsets. Gemini points use runcost 0.1.4, which prices reported Gemini reasoning tokens as <code>output_reasoning_tokens</code> at the Gemini output-token rate.</p>
<p>Best plotted answer pass^3: <code>{esc(best.label)}</code> at {best.answer_pass3_pct:.2f}%. Cheapest plotted pass^3 cost: <code>{esc(cheapest.label)}</code> at {fmt_cost(cheapest.pass3_cost_usd)}.</p>
<img src="pass3-answer-log-cost.svg" alt="Answer-correct pass^3 versus log pass^3 cost">
<p>Data: <a href="pass3-effort-cost-curve-points.csv">pass3-effort-cost-curve-points.csv</a></p>
</main>
</body>
</html>
"""
    (REPORT_DIR / "index.html").write_text(html_text, encoding="utf-8")


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def to_int(value: object) -> int:
    if value in {None, ""}:
        return 0
    return int(float(str(value)))


def trim(value: float) -> str:
    text = f"{float(value):.10f}".rstrip("0").rstrip(".")
    return text or "0"


def fmt_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def fmt_cost(value: float) -> str:
    return f"${value:.4f}" if value < 1 else f"${value:.3f}"


def format_cost(value: float) -> str:
    if value < 0.1:
        return f"${value:.2f}"
    if value < 1:
        return f"${value:.1f}"
    return f"${value:.0f}" if value == int(value) else f"${value:.1f}"


def model_order(name: str) -> tuple[int, str]:
    return (MODEL_ORDER.get(name, 99), name)


def short_effort(effort: str) -> str:
    return {"minimal": "min", "medium": "med"}.get(effort, effort)


def nice_log_lower(value: float) -> float:
    candidates = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
    target = value * 0.9
    lower = candidates[0]
    for candidate in candidates:
        if candidate <= target:
            lower = candidate
    return lower


def nice_log_upper(value: float) -> float:
    candidates = [0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
    target = value * 1.08
    for candidate in candidates:
        if candidate >= target:
            return candidate
    return candidates[-1]


def centered_text_x(text: str, font_size: float, center_x: float, *, bold: bool = False) -> float:
    return center_x - approx_text_width(text, font_size, bold=bold) / 2


def approx_text_width(text: str, font_size: float, *, bold: bool = False) -> float:
    width = 0.0
    for char in text:
        if char in "ilI.,:;|!":
            width += 0.26
        elif char in "mwMW@#%":
            width += 0.86
        elif char == " ":
            width += 0.32
        else:
            width += 0.56
    if bold:
        width *= 1.08
    return width * font_size


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def rasterize_svgs(paths: Iterable[Path]) -> None:
    svg_paths = list(paths)
    if rasterize_svgs_with_cairosvg(svg_paths):
        return
    qlmanage = shutil.which("qlmanage")
    if not qlmanage:
        return
    for svg in svg_paths:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [qlmanage, "-t", "-s", "1900", "-o", tmpdir, str(svg)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            png = Path(tmpdir) / f"{svg.name}.png"
            if not png.exists():
                raise FileNotFoundError(png)
            shutil.copyfile(png, svg.with_suffix(".svg.png"))
            shutil.copyfile(png, svg.with_suffix(".png"))


def rasterize_svgs_with_cairosvg(paths: Iterable[Path]) -> bool:
    try:
        import cairosvg
    except ImportError:
        return False

    for svg in paths:
        png = svg.with_suffix(".png")
        cairosvg.svg2png(url=str(svg), write_to=str(png), output_width=1900)
        shutil.copyfile(png, svg.with_suffix(".svg.png"))
    return True


if __name__ == "__main__":
    raise SystemExit(main())
