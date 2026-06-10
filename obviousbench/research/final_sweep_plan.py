"""Generate the gated final paper-sweep run plan without running models."""

from __future__ import annotations

import csv
import shlex
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from obviousbench.research.arxiv_readiness import (
    ArxivReadinessInputs,
    ReadinessProfile,
    audit_arxiv_readiness,
)


@dataclass(frozen=True)
class FinalSweepPlanInputs:
    panel_path: Path
    dataset_path: Path
    paper_manifest_path: Path
    item_cards_dir: Path
    scorer_gold_dir: Path
    human_baseline_path: Path | None
    cost_estimates_path: Path | None
    output_path: Path
    comparison_manifest_path: Path
    smoke_status_path: Path | None = None
    raw_root: Path = Path("results/raw/paper-v1-final-high-cap")
    summary_root: Path = Path("results/summaries/paper-v1-final-high-cap")
    comparison_dir: Path = Path("results/summaries/paper-v1-final-high-cap/comparison")
    report_dir: Path = Path("docs/reports/2026-06-01-paper-v1-final-high-cap-sweep")
    generated_on: str = "2026-06-01"
    min_gold_examples_per_scorer: int = 20
    min_human_participants: int = 5
    readiness_profile: ReadinessProfile = "preprint"


@dataclass(frozen=True)
class FinalSweepCommand:
    entry_id: str
    label: str
    inspect_model: str
    provider_route: str
    log_dir: Path
    summary_dir: Path
    inspect_command: str
    summarize_command: str


@dataclass(frozen=True)
class FinalSweepPlanResult:
    output_path: Path
    comparison_manifest_path: Path
    run_allowed: bool
    blockers: tuple[str, ...]
    commands: tuple[FinalSweepCommand, ...]

    @property
    def command_count(self) -> int:
        return len(self.commands)


def build_final_sweep_plan(inputs: FinalSweepPlanInputs) -> FinalSweepPlanResult:
    """Write a deterministic final-sweep handoff without making provider calls."""
    panel = (
        yaml.safe_load(inputs.panel_path.read_text(encoding="utf-8")) or {}
        if inputs.panel_path.exists()
        else {}
    )
    commands = tuple(_build_commands(inputs, panel))
    blockers = tuple(_collect_blockers(inputs, panel))
    result = FinalSweepPlanResult(
        output_path=inputs.output_path,
        comparison_manifest_path=inputs.comparison_manifest_path,
        run_allowed=not blockers,
        blockers=blockers,
        commands=commands,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.comparison_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    _write_comparison_manifest(inputs.comparison_manifest_path, commands)
    inputs.output_path.write_text(_render_markdown(result, inputs, panel), encoding="utf-8")
    return result


def _collect_blockers(
    inputs: FinalSweepPlanInputs,
    panel: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    readiness = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=[inputs.dataset_path],
            item_cards_dir=inputs.item_cards_dir,
            scorer_gold_dir=inputs.scorer_gold_dir,
            human_baseline_path=inputs.human_baseline_path,
            paper_manifest_path=inputs.paper_manifest_path,
            min_gold_examples_per_scorer=inputs.min_gold_examples_per_scorer,
            min_human_participants=inputs.min_human_participants,
            manifest_scope=True,
            readiness_profile=inputs.readiness_profile,
        )
    )
    for gate in readiness.gates:
        if gate.status == "fail":
            blockers.append(f"{gate.name}: {gate.message}")

    if not inputs.panel_path.exists():
        blockers.append(f"model panel is missing: {inputs.panel_path}")
    if not panel.get("entries"):
        blockers.append("model panel has no entries")
    if panel.get("run_status") not in {"planned_not_run", "planned"}:
        blockers.append(f"unexpected panel run_status: {panel.get('run_status')}")
    if inputs.cost_estimates_path is None or not inputs.cost_estimates_path.exists():
        blockers.append("model-panel cost estimate artifact is missing")
    blockers.extend(_collect_smoke_status_blockers(inputs.smoke_status_path))
    return blockers


def _collect_smoke_status_blockers(smoke_status_path: Path | None) -> list[str]:
    if smoke_status_path is None:
        return []
    if not smoke_status_path.exists():
        return [f"smoke-status document is missing: {smoke_status_path}"]

    status = _frontmatter_status(smoke_status_path.read_text(encoding="utf-8"))
    accepted_statuses = {"accepted", "passed", "ready", "waived"}
    if status not in accepted_statuses:
        return [
            "smoke status is not accepted: "
            f"{smoke_status_path} has status `{status or 'missing'}`"
        ]
    return []


def _frontmatter_status(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        return ""
    metadata = yaml.safe_load(frontmatter) or {}
    return str(metadata.get("status") or "").strip().lower()


def _build_commands(
    inputs: FinalSweepPlanInputs,
    panel: dict[str, Any],
) -> list[FinalSweepCommand]:
    defaults = panel.get("defaults") or {}
    default_inspect_args = tuple(str(arg) for arg in defaults.get("inspect_args") or ())
    commands = []
    for entry in panel.get("entries") or []:
        entry_id = str(entry["id"])
        log_dir = inputs.raw_root / entry_id
        summary_dir = inputs.summary_root / entry_id
        generation_settings = _generation_settings(entry, defaults)
        inspect_command = _join(
            [
                ".venv/bin/python",
                "-m",
                "obviousbench.runners.inspect_eval",
                "--task",
                "obviousbench/tasks/barrage.py",
                "--model",
                str(entry["inspect_model"]),
                "--log-dir",
                str(log_dir),
                "-T",
                f"dataset={inputs.dataset_path.resolve()}",
                *[
                    f"--inspect-arg={inspect_arg}"
                    for inspect_arg in default_inspect_args
                ],
                *[
                    item
                    for key, value in generation_settings.items()
                    for item in ("--generation-setting", f"{key}={value}")
                ],
            ]
        )
        summarize_command = _join(
            [
                ".venv/bin/python",
                "-m",
                "obviousbench.cli",
                "rescore",
                "--logs",
                str(log_dir),
                "--out",
                str(summary_dir),
                "--cost",
                "runcost",
            ]
        )
        commands.append(
            FinalSweepCommand(
                entry_id=entry_id,
                label=str(entry["label"]),
                inspect_model=str(entry["inspect_model"]),
                provider_route=str(entry["provider_route"]),
                log_dir=log_dir,
                summary_dir=summary_dir,
                inspect_command=inspect_command,
                summarize_command=summarize_command,
            )
        )
    return commands


def _generation_settings(
    entry: dict[str, Any],
    defaults: dict[str, Any],
) -> dict[str, str]:
    settings = {}
    for key in ("temperature", "max_tokens", "reasoning_effort", "reasoning_summary"):
        value = entry.get(key, defaults.get(key))
        if value is not None:
            settings[key] = str(value)
    return settings


def _write_comparison_manifest(
    path: Path,
    commands: Sequence[FinalSweepCommand],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["label", "model", "summary_dir"],
            lineterminator="\n",
        )
        writer.writeheader()
        for command in commands:
            writer.writerow(
                {
                    "label": command.label,
                    "model": command.inspect_model,
                    "summary_dir": str(command.summary_dir),
                }
            )


def _render_markdown(
    result: FinalSweepPlanResult,
    inputs: FinalSweepPlanInputs,
    panel: dict[str, Any],
) -> str:
    lines = [
        "---",
        "title: Paper V1 Final Sweep Plan",
        "date: 2026-06-01",
        "type: runbook",
        f"status: {'ready' if result.run_allowed else 'blocked'}",
        "---",
        "",
        "# Paper V1 Final Sweep Plan",
        "",
        "This is a dry-run handoff. It writes commands and manifests but does not",
        "run model providers.",
        "",
        f"Run allowed: {'YES' if result.run_allowed else 'NO'}",
        "",
        "`Run allowed` covers readiness, cost, and smoke-status gates. Provider",
        "execution is still blocked if credentials or provider access are",
        "unavailable at runtime.",
        "",
        f"Panel: `{inputs.panel_path}`",
        f"Dataset: `{inputs.dataset_path}`",
        f"Paper manifest: `{inputs.paper_manifest_path}`",
        f"Readiness profile: `{inputs.readiness_profile}`",
        f"Comparison manifest: `{inputs.comparison_manifest_path}`",
        f"Raw log root: `{inputs.raw_root}`",
        f"Summary root: `{inputs.summary_root}`",
        f"Comparison dir: `{inputs.comparison_dir}`",
        f"Report dir: `{inputs.report_dir}`",
        f"Panel entries: {len(result.commands)}",
        f"Smoke status: `{inputs.smoke_status_path or 'not gated'}`",
        "Run freeze policy: `docs/research/2026-06-01-paper-v1-run-freeze-policy.md`",
        "",
    ]
    if result.blockers:
        lines.extend(["## Current Blockers", ""])
        lines.extend(f"- {blocker}" for blocker in result.blockers)
        lines.append("")

    lines.extend(["## Preconditions", ""])
    if inputs.readiness_profile == "preprint":
        lines.extend(
            [
                "- `make -C paper readiness-preprint` passes.",
                "- The manuscript omits empirical human-baseline claims or labels "
                "them as planned validation.",
                "- Any `human-trivial` wording is grounded in item-card design and "
                "review, not participant measurements.",
            ]
        )
    else:
        lines.extend(
            [
                "- `make -C paper readiness` passes.",
                "- Human-baseline rows cover every paper item.",
            ]
        )
    lines.extend(
        [
            "- Model aliases and pricing are re-verified immediately before running.",
            "- The expected cost is accepted.",
            "- The operator confirms credentials and provider access.",
            "",
            "## Manifest Runner",
            "",
            "Preferred final execution wrapper:",
            "",
            "```bash",
            _join(
                [
                    ".venv/bin/python",
                    "scripts/run_model_panel.py",
                    "--panel",
                    str(inputs.panel_path),
                    "--dataset",
                    str(inputs.dataset_path),
                    "--raw-root",
                    str(inputs.raw_root),
                    "--summary-root",
                    str(inputs.summary_root),
                    "--manifest-out",
                    str(inputs.comparison_manifest_path),
                    "--status-out",
                    str(inputs.summary_root / "status.jsonl"),
                    "--mode",
                    "full",
                    "--no-cache",
                ]
            ),
            "```",
            "",
            "## Model Commands",
            "",
        ]
    )
    for command in result.commands:
        lines.extend(
            [
                f"### {command.label}",
                "",
                f"- Entry ID: `{command.entry_id}`",
                f"- Provider route: `{command.provider_route}`",
                f"- Inspect model: `{command.inspect_model}`",
                "",
                "Inspect run:",
                "",
                "```bash",
                command.inspect_command,
                "```",
                "",
                "Summarize/rescore:",
                "",
                "```bash",
                command.summarize_command,
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Post-Run Aggregation",
            "",
            "Build the comparison tables:",
            "",
            "```bash",
            _join(
                [
                    ".venv/bin/python",
                    "-m",
                    "obviousbench.cli",
                    "build-comparison",
                    "--manifest",
                    str(inputs.comparison_manifest_path),
                    "--out",
                    str(inputs.comparison_dir),
                    "--manual-xai-costs",
                ]
            ),
            "```",
            "",
            "Build the static report:",
            "",
            "```bash",
            _join(
                [
                    ".venv/bin/python",
                    "-m",
                    "obviousbench.cli",
                    "build-report",
                    "--comparison-dir",
                    str(inputs.comparison_dir),
                    "--out",
                    str(inputs.report_dir),
                    "--generated-on",
                    inputs.generated_on,
                    "--title",
                    "ObviousBench Paper V1 Final Sweep",
                ]
            ),
            "```",
            "",
            "Regenerate paper tables and figures from final results:",
            "",
            "```bash",
            _join(
                [
                    ".venv/bin/python",
                    "scripts/build_paper_assets.py",
                    "--manifest",
                    str(inputs.paper_manifest_path),
                    "--dataset",
                    str(inputs.dataset_path),
                    "--human-baseline",
                    str(inputs.human_baseline_path or ""),
                    "--model-panel",
                    str(inputs.panel_path),
                    "--final-results-dir",
                    str(inputs.comparison_dir),
                    "--out",
                    "paper/tables",
                    "--figures-out",
                    "paper/figures",
                ]
            ),
            "```",
            "",
            "## Panel Notes",
            "",
            f"- Config run status: `{panel.get('run_status', '')}`",
            f"- Profile: `{panel.get('profile') or 'hard_obvious_8x10'}`",
            f"- Seed: `{panel.get('seed') or 20260531}`",
            "",
        ]
    )
    return "\n".join(lines)


def _join(parts: Sequence[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts if part != "")
