"""Cost integrity checks for paper comparison artifacts."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

DEFAULT_LOW_USD_PER_MTOK = 0.01
DEFAULT_FULL_RERUN_SOURCES = frozenset({"repair3_xai_grok", "telemetry_rerun"})


@dataclass(frozen=True)
class CostIntegrityInputs:
    comparison_path: Path
    selection_audit_path: Path | None = None
    output_path: Path | None = None
    low_usd_per_mtok: float = DEFAULT_LOW_USD_PER_MTOK
    full_rerun_sources: frozenset[str] = DEFAULT_FULL_RERUN_SOURCES


@dataclass(frozen=True)
class CostIntegrityFinding:
    check: str
    label: str
    detail: str


@dataclass(frozen=True)
class CostIntegrityResult:
    ok: bool
    comparison_rows: int
    findings: list[CostIntegrityFinding]
    output_path: Path | None = None


def audit_cost_integrity(inputs: CostIntegrityInputs) -> CostIntegrityResult:
    """Audit comparison costs for silently missing or partial accounting."""
    comparison_rows = _read_csv(inputs.comparison_path)
    findings: list[CostIntegrityFinding] = []

    for row in comparison_rows:
        label = row.get("label") or row.get("model") or "<unknown>"
        scored_samples = _int(row.get("scored_samples"))
        provider_errors = _int(row.get("provider_errors"))
        timeouts = _int(row.get("timeouts"))
        successful_samples = max(scored_samples - provider_errors - timeouts, 0)
        total_tokens = _float(row.get("total_tokens"))
        estimated_cost = _float(row.get("estimated_cost_usd"))
        cost_warnings = (row.get("cost_warnings") or "").strip()

        if cost_warnings:
            findings.append(
                CostIntegrityFinding(
                    "cost_warning",
                    label,
                    cost_warnings,
                )
            )
        if successful_samples > 0 and total_tokens == 0:
            findings.append(
                CostIntegrityFinding(
                    "missing_usage_telemetry",
                    label,
                    (
                        f"{successful_samples} successful sample(s) but total_tokens=0 "
                        "and estimated_cost_usd=0"
                    ),
                )
            )
        if total_tokens > 0 and estimated_cost == 0 and not _looks_free(row):
            findings.append(
                CostIntegrityFinding(
                    "nonzero_tokens_zero_cost",
                    label,
                    f"total_tokens={_format_number(total_tokens)} but estimated_cost_usd=0",
                )
            )
        if total_tokens > 0 and estimated_cost > 0 and not _looks_free(row):
            usd_per_mtok = estimated_cost / total_tokens * 1_000_000
            if usd_per_mtok < inputs.low_usd_per_mtok:
                findings.append(
                    CostIntegrityFinding(
                        "suspiciously_low_usd_per_mtok",
                        label,
                        (
                            f"effective price ${usd_per_mtok:.6f}/M tokens is below "
                            f"${inputs.low_usd_per_mtok:.6f}/M"
                        ),
                    )
                )

    if inputs.selection_audit_path is not None:
        findings.extend(
            _selection_findings(
                inputs.selection_audit_path,
                full_rerun_sources=inputs.full_rerun_sources,
            )
        )

    result = CostIntegrityResult(
        ok=not findings,
        comparison_rows=len(comparison_rows),
        findings=findings,
        output_path=inputs.output_path,
    )
    if inputs.output_path is not None:
        _write_report(inputs.output_path, result)
    return result


def _selection_findings(
    selection_audit_path: Path,
    *,
    full_rerun_sources: frozenset[str],
) -> list[CostIntegrityFinding]:
    findings: list[CostIntegrityFinding] = []
    for row in _read_csv(selection_audit_path):
        selected_source = (row.get("selected_source") or "").strip()
        if selected_source in {"", "base"} or selected_source in full_rerun_sources:
            continue
        summary_dir = row.get("summary_dir") or ""
        if "cumulative-cost-runs" not in summary_dir:
            findings.append(
                CostIntegrityFinding(
                    "repair_source_not_cumulative",
                    row.get("label") or row.get("model") or "<unknown>",
                    (
                        f"selected_source={selected_source} points at {summary_dir}; "
                        "repair/cache-hit selections must point at cumulative-cost-runs"
                    ),
                )
            )
    return findings


def _write_report(path: Path, result: CostIntegrityResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result.ok else "BLOCKED"
    lines = [
        "---",
        "title: Paper V1 Cost Integrity Audit",
        "date: 2026-06-03",
        "type: audit",
        f"status: {status.lower()}",
        "---",
        "",
        "# Paper V1 Cost Integrity Audit",
        "",
        f"Overall status: {status}",
        "",
        f"Comparison rows: {result.comparison_rows}",
        f"Findings: {len(result.findings)}",
        "",
    ]
    if result.findings:
        lines.extend(["## Findings", ""])
        for finding in result.findings:
            lines.append(f"- `{finding.check}`: {finding.label} - {finding.detail}")
    else:
        lines.extend(
            [
                "## Findings",
                "",
                "No cost integrity issues found.",
            ]
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _int(value: str | None) -> int:
    return int(_float(value))


def _float(value: str | None) -> float:
    if value in {None, ""}:
        return 0.0
    return float(value)


def _looks_free(row: dict[str, str]) -> bool:
    model = (row.get("model") or "").casefold()
    cost_source = (row.get("cost_source") or "").casefold()
    return model.endswith(":free") or "free" in cost_source


def _format_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return str(value)
