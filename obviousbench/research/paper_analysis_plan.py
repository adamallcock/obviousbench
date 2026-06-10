"""Render and audit the frozen analysis plan for the ObviousBench paper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REQUIRED_TOP_LEVEL_KEYS = (
    "schema_version",
    "status",
    "applies_to",
    "no_provider_calls",
    "analysis_freeze",
    "primary_question",
    "inputs",
    "primary_metrics",
    "secondary_metrics",
    "intervals",
    "stratification",
    "reported_tables",
    "reported_figures",
    "exclusion_policy",
    "human_baseline_policy",
    "claim_policy",
)
REQUIRED_INPUT_KEYS = (
    "dataset_manifest",
    "model_panel",
    "human_baseline",
    "final_comparison_dir",
    "final_report_dir",
    "scoring_gold_dir",
)
REQUIRED_PRIMARY_METRICS = ("answer_accuracy",)
REQUIRED_INTERVAL_KEYS = ("binomial", "paired_deltas")
REQUIRED_CLAIM_POLICY_KEYS = (
    "reporting_vs_hypothesis_generation",
    "solution_policy",
    "ranking_policy",
    "release_policy",
)
ACCEPTED_PLAN_STATUSES = (
    "frozen_before_final_sweep",
    "frozen_for_first_draft_evidence_run",
)


@dataclass(frozen=True)
class PaperAnalysisPlanInputs:
    plan_path: Path
    output_path: Path


@dataclass(frozen=True)
class PaperAnalysisPlanResult:
    plan_path: Path
    output_path: Path
    plan: dict[str, Any]
    issues: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.issues

    @property
    def primary_metric_count(self) -> int:
        return len(self.plan.get("primary_metrics") or [])

    @property
    def secondary_metric_count(self) -> int:
        return len(self.plan.get("secondary_metrics") or [])

    @property
    def table_count(self) -> int:
        return len(self.plan.get("reported_tables") or [])

    @property
    def figure_count(self) -> int:
        return len(self.plan.get("reported_figures") or [])


def build_paper_analysis_plan(
    inputs: PaperAnalysisPlanInputs,
) -> PaperAnalysisPlanResult:
    """Audit and render the paper analysis plan without running model providers."""
    plan = _load_plan(inputs.plan_path)
    issues = tuple(_audit_plan(plan))
    result = PaperAnalysisPlanResult(
        plan_path=inputs.plan_path,
        output_path=inputs.output_path,
        plan=plan,
        issues=issues,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result), encoding="utf-8")
    return result


def _load_plan(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _audit_plan(plan: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not plan:
        return ["analysis plan is missing or empty"]
    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in plan:
            issues.append(f"missing top-level key: {key}")
    if plan.get("schema_version") != "paper-analysis-plan-v1":
        issues.append("schema_version must be paper-analysis-plan-v1")
    if plan.get("status") not in ACCEPTED_PLAN_STATUSES:
        issues.append(
            "status must be one of: " + ", ".join(ACCEPTED_PLAN_STATUSES)
        )
    if plan.get("applies_to") != "paper_v1":
        issues.append("applies_to must be paper_v1")
    if plan.get("no_provider_calls") is not True:
        issues.append("no_provider_calls must be true")
    issues.extend(_audit_inputs(plan.get("inputs")))
    issues.extend(_audit_primary_metrics(plan.get("primary_metrics")))
    issues.extend(_audit_intervals(plan.get("intervals")))
    issues.extend(_audit_sequence("secondary_metrics", plan.get("secondary_metrics")))
    issues.extend(_audit_sequence("reported_tables", plan.get("reported_tables")))
    issues.extend(_audit_sequence("reported_figures", plan.get("reported_figures")))
    issues.extend(_audit_claim_policy(plan.get("claim_policy")))
    freeze = plan.get("analysis_freeze") or {}
    if not isinstance(freeze, dict) or (
        freeze.get("frozen_before_final_sweep") is not True
        and freeze.get("frozen_for_first_draft_evidence_run") is not True
    ):
        issues.append(
            "analysis_freeze must mark frozen_before_final_sweep or "
            "frozen_for_first_draft_evidence_run as true"
        )
    return issues


def _audit_inputs(inputs: Any) -> list[str]:
    if not isinstance(inputs, dict):
        return ["inputs must be a mapping"]
    return [
        f"inputs.{key} is required"
        for key in REQUIRED_INPUT_KEYS
        if not inputs.get(key)
    ]


def _audit_primary_metrics(metrics: Any) -> list[str]:
    issues = _audit_sequence("primary_metrics", metrics)
    if issues:
        return issues
    metric_ids = {str(metric.get("id")) for metric in metrics}
    for metric_id in REQUIRED_PRIMARY_METRICS:
        if metric_id not in metric_ids:
            issues.append(f"primary_metrics must include {metric_id}")
    if "strict_accuracy" in metric_ids:
        issues.append("strict_accuracy must be secondary, not primary")
    if "format_accuracy" in metric_ids:
        issues.append("format_accuracy must be secondary, not primary")
    for metric in metrics:
        for key in ("id", "label", "numerator", "denominator", "source_column"):
            if not metric.get(key):
                issues.append(f"primary metric missing {key}")
        if metric.get("interval") != "wilson_95":
            issues.append(f"primary metric {metric.get('id')} must use wilson_95")
    return issues


def _audit_intervals(intervals: Any) -> list[str]:
    if not isinstance(intervals, dict):
        return ["intervals must be a mapping"]
    issues = []
    for key in REQUIRED_INTERVAL_KEYS:
        if key not in intervals:
            issues.append(f"intervals.{key} is required")
    binomial = intervals.get("binomial") or {}
    paired = intervals.get("paired_deltas") or {}
    if binomial.get("implementation") != "obviousbench.analysis.statistics.wilson_interval":
        issues.append("binomial interval must use obviousbench.analysis.statistics.wilson_interval")
    if paired.get("implementation") != "obviousbench.analysis.statistics.paired_boolean_delta":
        issues.append(
            "paired deltas must use "
            "obviousbench.analysis.statistics.paired_boolean_delta"
        )
    if paired.get("seed") != 20260531:
        issues.append("paired delta bootstrap seed must be 20260531")
    return issues


def _audit_sequence(name: str, value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{name} must be a non-empty list"]
    issues = []
    seen: set[str] = set()
    for row in value:
        if not isinstance(row, dict):
            issues.append(f"{name} entries must be mappings")
            continue
        row_id = str(row.get("id") or "")
        if not row_id:
            issues.append(f"{name} entry missing id")
        elif row_id in seen:
            issues.append(f"{name} duplicate id: {row_id}")
        seen.add(row_id)
    return issues


def _audit_claim_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["claim_policy must be a mapping"]
    return [
        f"claim_policy.{key} is required"
        for key in REQUIRED_CLAIM_POLICY_KEYS
        if not policy.get(key)
    ]


def _render_markdown(result: PaperAnalysisPlanResult) -> str:
    plan = result.plan
    lines = [
        "---",
        "title: ObviousBench Paper Analysis Plan",
        f"date: {plan.get('created_at', '2026-06-01')}",
        "type: research",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Paper Analysis Plan",
        "",
        "This document records the paper's reporting and statistical analysis",
        "policy for the selected evidence run. It is generated from",
        f"`{result.plan_path}` and does not run provider calls.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"Plan status: `{plan.get('status', 'missing')}`",
        f"Applies to: `{plan.get('applies_to', 'missing')}`",
        f"No provider calls: `{plan.get('no_provider_calls', False)}`",
        "",
    ]
    if result.issues:
        lines.extend(["## Issues", ""])
        lines.extend(f"- {issue}" for issue in result.issues)
        lines.append("")
    lines.extend(_summary_lines(result))
    lines.extend(_input_lines(plan.get("inputs") or {}))
    lines.extend(_metric_lines("Primary Metrics", plan.get("primary_metrics") or []))
    lines.extend(_metric_lines("Secondary Metrics", plan.get("secondary_metrics") or []))
    lines.extend(_interval_lines(plan.get("intervals") or {}))
    lines.extend(_artifact_lines("Reported Tables", plan.get("reported_tables") or []))
    if plan.get("audit_artifacts"):
        lines.extend(_artifact_lines("Audit Artifacts", plan.get("audit_artifacts") or []))
    lines.extend(_artifact_lines("Reported Figures", plan.get("reported_figures") or []))
    lines.extend(_policy_lines("Exclusion Policy", plan.get("exclusion_policy") or {}))
    lines.extend(_policy_lines("Human Baseline Policy", plan.get("human_baseline_policy") or {}))
    lines.extend(_policy_lines("Claim Policy", plan.get("claim_policy") or {}))
    return "\n".join(lines)


def _summary_lines(result: PaperAnalysisPlanResult) -> list[str]:
    return [
        "## Summary",
        "",
        f"- Primary metrics: {result.primary_metric_count}",
        f"- Secondary metrics: {result.secondary_metric_count}",
        f"- Reported tables: {result.table_count}",
        f"- Reported figures: {result.figure_count}",
        "",
    ]


def _input_lines(inputs: dict[str, Any]) -> list[str]:
    lines = ["## Frozen Inputs", "", "| Input | Path |", "| --- | --- |"]
    for key in REQUIRED_INPUT_KEYS:
        lines.append(f"| `{key}` | `{_cell(str(inputs.get(key, 'missing')))}` |")
    extra_keys = sorted(key for key in inputs if key not in REQUIRED_INPUT_KEYS)
    for key in extra_keys:
        lines.append(f"| `{key}` | `{_cell(str(inputs.get(key, 'missing')))}` |")
    lines.append("")
    return lines


def _metric_lines(title: str, rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        f"## {title}",
        "",
        "| ID | Label | Source column | Interpretation |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        interpretation = row.get("paper_role") or row.get("interpretation") or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(str(row.get("id", ""))),
                    _cell(str(row.get("label", ""))),
                    _cell(str(row.get("source_column", ""))),
                    _cell(str(interpretation)),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _interval_lines(intervals: dict[str, Any]) -> list[str]:
    lines = ["## Intervals", "", "| Estimate | Method | Implementation |", "| --- | --- | --- |"]
    for key in REQUIRED_INTERVAL_KEYS:
        row = intervals.get(key) or {}
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(key),
                    _cell(str(row.get("method", ""))),
                    _cell(str(row.get("implementation", ""))),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _artifact_lines(title: str, rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "## " + title,
        "",
        "| ID | Path | Source | Pre-sweep status |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(str(row.get("id", ""))),
                    _cell(f"`{row.get('path', '')}`"),
                    _cell(str(row.get("source", ""))),
                    _cell(str(row.get("status_before_sweep", ""))),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _policy_lines(title: str, policy: dict[str, Any]) -> list[str]:
    lines = [f"## {title}", ""]
    if not policy:
        lines.extend(["No policy recorded.", ""])
        return lines
    for key, value in policy.items():
        lines.append(f"- `{key}`: {_cell(str(value))}")
    lines.append("")
    return lines


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
