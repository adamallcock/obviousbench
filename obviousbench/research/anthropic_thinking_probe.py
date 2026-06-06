"""Audit Anthropic adaptive-thinking request shape against observed usage."""

from __future__ import annotations

import argparse
import csv
import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from inspect_ai.model import GenerateConfig
from inspect_ai.model._providers.anthropic import AnthropicAPI

from obviousbench.research.model_panel_runner import (
    _generation_settings,
    _load_panel,
    _select_entries,
)

HIGH_EFFORTS = frozenset({"high", "xhigh", "max"})


@dataclass(frozen=True)
class AnthropicThinkingProbeRow:
    entry_id: str
    label: str
    model: str
    effort: str
    control_style: str
    generation_settings: dict[str, Any]
    request_model: str
    request_max_tokens: int | None
    request_thinking_type: str
    request_thinking_display: str
    request_output_effort: str
    request_betas: tuple[str, ...]
    provider_settings_thinking_display: str
    scored_samples: int
    answer_accuracy_pct: float | None
    strict_accuracy_pct: float | None
    estimated_cost_usd: float | None
    observed_reasoning_tokens: int
    observed_reasoning_tokens_per_sample: float | None
    reasoning_nonzero_samples: int
    reasoning_nonzero_share: float | None
    reasoning_max_sample: int
    observed_output_tokens: int
    observed_output_tokens_per_sample: float | None
    estimated_output_tokens_per_sample: float | None
    observed_to_estimated_output_ratio: float | None
    estimated_reasoning_tokens_per_sample: float | None
    configured_reasoning_tokens_per_sample: float | None
    observed_to_estimated_ratio: float | None
    observed_to_configured_ratio: float | None
    reasoning_token_source: str
    summary_dir: str
    warnings: tuple[str, ...]


def build_probe_rows(
    *,
    panel_path: Path,
    summary_root: Path,
    only: Sequence[str] = (),
) -> list[AnthropicThinkingProbeRow]:
    """Build request/usage audit rows for Anthropic entries in a model panel."""
    panel = _load_panel(panel_path)
    defaults = panel.get("defaults") or {}
    entries = _select_entries(panel.get("entries") or [], only, limit=None)
    rows: list[AnthropicThinkingProbeRow] = []
    for entry in entries:
        if not _is_anthropic_entry(entry):
            continue
        rows.append(_build_probe_row(entry, defaults, summary_root / str(entry["id"])))
    return rows


def write_probe_csv(rows: Sequence[AnthropicThinkingProbeRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=_csv_fieldnames(), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(_csv_row(row))


def write_probe_markdown(
    rows: Sequence[AnthropicThinkingProbeRow],
    path: Path,
    *,
    panel_path: Path,
    summary_root: Path,
    csv_path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        "title: Anthropic Adaptive Thinking Probe",
        "date: 2026-06-02",
        "type: research",
        "status: draft",
        "---",
        "",
        "# Anthropic Adaptive Thinking Probe",
        "",
        f"- Panel: `{panel_path}`",
        f"- Summary root: `{summary_root}`",
        f"- CSV: `{csv_path}`",
        "- Request-shape source: Inspect Anthropic provider request builder.",
        (
            "- Anthropic docs: "
            "<https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking> "
            "and <https://platform.claude.com/docs/en/build-with-claude/effort>."
        ),
        "",
        "## Findings",
        "",
        (
            "> **Metric caveat.** For Claude 4.x, `reasoning_tokens` here is the "
            "re-tokenized *summary* length, not billed thinking; it can even "
            "exceed `output_tokens`. The authoritative billed field is "
            "`usage.output_tokens_details.thinking_tokens`, captured only for runs "
            "produced after applying "
            "`scripts/patch_inspect_anthropic_thinking_tokens.py`. Effort warnings "
            "below are baselined on billed `output_tokens`. See "
            "`docs/research/2026-06-03-opus-4-8-adaptive-thinking-diagnosis.md`."
        ),
        "",
    ]
    if rows:
        warning_rows = [row for row in rows if row.warnings]
        lines.append(
            f"- Audited {len(rows)} Anthropic row(s); "
            f"{len(warning_rows)} row(s) have diagnostic warning flags."
        )
        low_spend = [
            row
            for row in rows
            if "observed_output_below_estimate" in row.warnings
        ]
        if low_spend:
            labels = ", ".join(row.entry_id for row in low_spend)
            lines.append(
                f"- Observed billed output below calibrated estimate for: {labels}."
            )
    else:
        lines.append("- No Anthropic rows were selected.")
    lines.extend(
        [
            "",
            "## Probe Table",
            "",
            (
                "| Entry | Effort | Request thinking | Request effort | Betas | "
                "Output/sample | Summary tok/sample | Nonzero samples | Answer | "
                "Cost | Warnings |"
            ),
            "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        request_thinking = _join_nonempty(
            [row.request_thinking_type, row.request_thinking_display],
            sep="/",
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    _md(row.entry_id),
                    _md(row.effort),
                    _md(request_thinking),
                    _md(row.request_output_effort),
                    _md(",".join(row.request_betas)),
                    _md(_format_float(row.observed_output_tokens_per_sample, 2)),
                    _md(_format_float(row.observed_reasoning_tokens_per_sample, 2)),
                    _md(f"{row.reasoning_nonzero_samples}/{row.scored_samples}"),
                    _md(_format_percent(row.answer_accuracy_pct)),
                    _md(_format_money(row.estimated_cost_usd)),
                    _md(";".join(row.warnings)),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            (
                "- `observed_output_below_estimate` means a high/xhigh/max run "
                "billed less than 10% of the panel's calibrated expected "
                "`output_tokens` per sample. Output tokens are billing-authoritative "
                "and include any billed thinking, so this is a real spend signal "
                "(unlike the summary-length reasoning axis)."
            ),
            (
                "- `thinking_blocks_sparse` means a high/xhigh/max run returned a "
                "non-empty thinking (summary) block on fewer than half of scored "
                "samples. This is a behavioral signal about how often the model "
                "chose to think (adaptive thinking treats effort as soft guidance, "
                "not a floor), not a telemetry undercount."
            ),
            (
                "- `provider_request_settings_display_mismatch` means the panel "
                "metadata does not match the executable Inspect request shape for "
                "the `thinking.display` field."
            ),
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="probe_anthropic_thinking.py")
    parser.add_argument(
        "--panel",
        type=Path,
        default=Path("configs/paper_v1_top_thinking_clean_20260602_panel.yaml"),
    )
    parser.add_argument(
        "--summary-root",
        type=Path,
        default=Path("results/summaries/paper-v1-anthropic-adaptive-thinking-rerun-20260602"),
    )
    parser.add_argument(
        "--out-csv",
        type=Path,
        default=Path("docs/research/2026-06-02-anthropic-adaptive-thinking-probe.csv"),
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("docs/research/2026-06-02-anthropic-adaptive-thinking-probe.md"),
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Panel entry id to audit. May be repeated.",
    )
    args = parser.parse_args(argv)

    rows = build_probe_rows(
        panel_path=args.panel,
        summary_root=args.summary_root,
        only=tuple(args.only),
    )
    write_probe_csv(rows, args.out_csv)
    write_probe_markdown(
        rows,
        args.out_md,
        panel_path=args.panel,
        summary_root=args.summary_root,
        csv_path=args.out_csv,
    )
    print(
        f"Wrote {len(rows)} Anthropic thinking probe row(s) to "
        f"{args.out_csv} and {args.out_md}"
    )
    return 0


def _build_probe_row(
    entry: dict[str, Any],
    defaults: dict[str, Any],
    summary_dir: Path,
) -> AnthropicThinkingProbeRow:
    settings = _generation_settings(entry, defaults)
    request_payload, request_betas = _anthropic_completion_request(
        str(entry["inspect_model"]),
        settings,
    )
    thinking = request_payload.get("thinking") or {}
    output_config = request_payload.get("output_config") or {}
    summary = _load_summary(summary_dir)
    usage = _load_usage(summary_dir)
    effort = str(settings.get("reasoning_effort") or entry.get("thinking_depth") or "")
    scored_samples = _int(summary.get("scored_samples")) or len(usage)
    observed_reasoning_tokens = _int(summary.get("reasoning_tokens"))
    if observed_reasoning_tokens == 0 and usage:
        observed_reasoning_tokens = sum(_int(row.get("reasoning_tokens")) for row in usage)
    nonzero_samples = sum(1 for row in usage if _int(row.get("reasoning_tokens")) > 0)
    max_sample = max((_int(row.get("reasoning_tokens")) for row in usage), default=0)
    observed_per_sample = _safe_div(observed_reasoning_tokens, scored_samples)
    estimated_usage = entry.get("estimated_usage") or {}
    estimated_per_sample = _optional_float(
        estimated_usage.get("reasoning_tokens_per_sample")
    )
    configured_per_sample = _optional_float(
        entry.get("configured_reasoning_tokens_per_sample")
    )
    # Billed output tokens are the authoritative spend axis (output_tokens already
    # includes any billed thinking). For Claude 4.x `reasoning_tokens` above is the
    # re-tokenized summary length, not billed thinking, so effort warnings are
    # baselined on output tokens instead. See
    # docs/research/2026-06-03-opus-4-8-adaptive-thinking-diagnosis.md.
    observed_output_tokens = sum(_int(row.get("output_tokens")) for row in usage)
    if observed_output_tokens == 0:
        observed_output_tokens = _int(summary.get("output_tokens"))
    observed_output_per_sample = _safe_div(observed_output_tokens, scored_samples)
    estimated_output_billed = _optional_float(
        estimated_usage.get("output_tokens_billed")
    )
    estimated_sample_count = _optional_float(estimated_usage.get("sample_count"))
    estimated_output_per_sample = (
        estimated_output_billed / estimated_sample_count
        if estimated_output_billed is not None and estimated_sample_count
        else None
    )
    row = AnthropicThinkingProbeRow(
        entry_id=str(entry["id"]),
        label=str(entry.get("label") or ""),
        model=str(entry.get("inspect_model") or ""),
        effort=effort,
        control_style=str(entry.get("control_style") or ""),
        generation_settings=settings,
        request_model=str(request_payload.get("model") or ""),
        request_max_tokens=_optional_int(request_payload.get("max_tokens")),
        request_thinking_type=str(thinking.get("type") or ""),
        request_thinking_display=str(thinking.get("display") or ""),
        request_output_effort=str(output_config.get("effort") or ""),
        request_betas=request_betas,
        provider_settings_thinking_display=_provider_settings_display(entry),
        scored_samples=scored_samples,
        answer_accuracy_pct=_percent(summary.get("answer_accuracy")),
        strict_accuracy_pct=_percent(summary.get("strict_accuracy")),
        estimated_cost_usd=_optional_float(summary.get("estimated_cost_usd")),
        observed_reasoning_tokens=observed_reasoning_tokens,
        observed_reasoning_tokens_per_sample=observed_per_sample,
        reasoning_nonzero_samples=nonzero_samples,
        reasoning_nonzero_share=_safe_div(nonzero_samples, scored_samples),
        reasoning_max_sample=max_sample,
        observed_output_tokens=observed_output_tokens,
        observed_output_tokens_per_sample=observed_output_per_sample,
        estimated_output_tokens_per_sample=estimated_output_per_sample,
        observed_to_estimated_output_ratio=_ratio(
            observed_output_per_sample, estimated_output_per_sample
        ),
        estimated_reasoning_tokens_per_sample=estimated_per_sample,
        configured_reasoning_tokens_per_sample=configured_per_sample,
        observed_to_estimated_ratio=_ratio(observed_per_sample, estimated_per_sample),
        observed_to_configured_ratio=_ratio(observed_per_sample, configured_per_sample),
        reasoning_token_source=str(summary.get("reasoning_token_source") or ""),
        summary_dir=str(summary_dir),
        warnings=(),
    )
    return AnthropicThinkingProbeRow(
        **{**asdict(row), "warnings": _warnings(row)}
    )


def _anthropic_completion_request(
    inspect_model: str,
    settings: dict[str, Any],
) -> tuple[dict[str, Any], tuple[str, ...]]:
    model_name = inspect_model.split("/", 1)[1] if "/" in inspect_model else inspect_model
    completion_config = AnthropicAPI(
        model_name=model_name,
        api_key="dummy",
    ).completion_config(GenerateConfig(**settings))
    payload = dict(completion_config[0])
    betas = tuple(str(beta) for beta in completion_config[3])
    return payload, betas


def _load_summary(summary_dir: Path) -> dict[str, str]:
    summary_path = summary_dir / "summary.csv"
    if not summary_path.exists():
        return {}
    with summary_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[0] if rows else {}


def _load_usage(summary_dir: Path) -> list[dict[str, str]]:
    usage_path = summary_dir / "usage_by_sample.csv"
    if not usage_path.exists():
        return []
    with usage_path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _warnings(row: AnthropicThinkingProbeRow) -> tuple[str, ...]:
    warnings: list[str] = []
    if row.control_style == "anthropic_adaptive_thinking_effort":
        if row.request_thinking_type != "adaptive":
            warnings.append("adaptive_request_missing")
        if row.request_output_effort != row.effort:
            warnings.append("output_effort_mismatch")
    if (
        row.provider_settings_thinking_display
        and row.request_thinking_display
        and row.provider_settings_thinking_display != row.request_thinking_display
    ):
        warnings.append("provider_request_settings_display_mismatch")
    if (
        row.effort in HIGH_EFFORTS
        and row.reasoning_nonzero_share is not None
        and row.reasoning_nonzero_share < 0.5
    ):
        warnings.append("thinking_blocks_sparse")
    if (
        row.effort in HIGH_EFFORTS
        and row.observed_to_estimated_output_ratio is not None
        and row.observed_to_estimated_output_ratio < 0.1
    ):
        warnings.append("observed_output_below_estimate")
    if row.scored_samples > 0 and row.effort != "none" and row.observed_reasoning_tokens == 0:
        warnings.append("reasoning_zero")
    if not row.reasoning_token_source:
        warnings.append("summary_missing_or_unscored")
    return tuple(warnings)


def _csv_fieldnames() -> list[str]:
    return [
        "entry_id",
        "label",
        "model",
        "effort",
        "control_style",
        "generation_settings",
        "request_model",
        "request_max_tokens",
        "request_thinking_type",
        "request_thinking_display",
        "request_output_effort",
        "request_betas",
        "provider_settings_thinking_display",
        "scored_samples",
        "answer_accuracy_pct",
        "strict_accuracy_pct",
        "estimated_cost_usd",
        "observed_reasoning_tokens",
        "observed_reasoning_tokens_per_sample",
        "reasoning_nonzero_samples",
        "reasoning_nonzero_share",
        "reasoning_max_sample",
        "observed_output_tokens",
        "observed_output_tokens_per_sample",
        "estimated_output_tokens_per_sample",
        "observed_to_estimated_output_ratio",
        "estimated_reasoning_tokens_per_sample",
        "configured_reasoning_tokens_per_sample",
        "observed_to_estimated_ratio",
        "observed_to_configured_ratio",
        "reasoning_token_source",
        "summary_dir",
        "warnings",
    ]


def _csv_row(row: AnthropicThinkingProbeRow) -> dict[str, str | int | float | None]:
    values = asdict(row)
    values["generation_settings"] = json.dumps(
        row.generation_settings,
        sort_keys=True,
        separators=(",", ":"),
    )
    values["request_betas"] = ";".join(row.request_betas)
    values["warnings"] = ";".join(row.warnings)
    return values


def _is_anthropic_entry(entry: dict[str, Any]) -> bool:
    return str(entry.get("provider_route") or "") == "anthropic" or str(
        entry.get("inspect_model") or ""
    ).startswith("anthropic/")


def _provider_settings_display(entry: dict[str, Any]) -> str:
    provider_settings = entry.get("provider_request_settings") or {}
    thinking = provider_settings.get("thinking") or {}
    return str(thinking.get("display") or "")


def _int(value: Any) -> int:
    if value is None or value == "":
        return 0
    try:
        return int(value)
    except ValueError:
        return int(float(value))


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return _int(value)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_div(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def _ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def _percent(value: Any) -> float | None:
    parsed = _optional_float(value)
    if parsed is None:
        return None
    return parsed * 100 if parsed <= 1 else parsed


def _format_float(value: float | None, digits: int) -> str:
    if value is None:
        return ""
    return f"{value:.{digits}f}"


def _format_percent(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.1f}%"


def _format_money(value: float | None) -> str:
    if value is None:
        return ""
    return f"${value:.5f}"


def _join_nonempty(values: Sequence[str], *, sep: str) -> str:
    return sep.join(value for value in values if value)


def _md(value: object) -> str:
    text = str(value)
    return text.replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
