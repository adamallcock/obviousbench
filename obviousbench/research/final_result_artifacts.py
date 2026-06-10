"""Audit expected final paper-sweep result artifacts without running providers."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from obviousbench.analysis.benchmark_report import BenchmarkReportPaths
from obviousbench.analysis.comparison import (
    COMPARISON_FIELDS,
    DELTA_FIELDS,
    EFFORT_CURVE_FIELDS,
    FAMILY_COMPARISON_FIELDS,
    METAMORPHIC_COMPARISON_FIELDS,
    SECTION_COMPARISON_FIELDS,
)

ArtifactStatus = Literal["present", "missing", "invalid"]

REQUIRED_MANIFEST_COLUMNS = ("label", "model", "summary_dir")
REQUIRED_SUMMARY_FILES = (
    "summary.csv",
    "usage_by_family.csv",
    "usage_by_section.csv",
    "usage_by_question.csv",
    "usage_by_sample.csv",
    "failure_gallery.md",
)
REQUIRED_COMPARISON_FILES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("comparison.csv", tuple(COMPARISON_FIELDS)),
    ("family_comparison.csv", tuple(FAMILY_COMPARISON_FIELDS)),
    ("section_comparison.csv", tuple(SECTION_COMPARISON_FIELDS)),
    ("effort_curve.csv", tuple(EFFORT_CURVE_FIELDS)),
    ("metamorphic_consistency.csv", tuple(METAMORPHIC_COMPARISON_FIELDS)),
    ("delta.csv", tuple(DELTA_FIELDS)),
)
REQUIRED_REPORT_FILES = (
    "report.html",
    "leaderboard.csv",
    "leaderboard.md",
    "family-heatmap.csv",
)


@dataclass(frozen=True)
class FinalResultArtifactInputs:
    manifest_path: Path
    comparison_dir: Path
    report_dir: Path
    output_path: Path
    generated_on: str = "2026-06-02"
    expected_models: int | None = None


@dataclass(frozen=True)
class ManifestEntry:
    label: str
    model: str
    summary_dir: Path


@dataclass(frozen=True)
class ArtifactCheck:
    path: Path
    status: ArtifactStatus
    evidence: str


@dataclass(frozen=True)
class FinalResultArtifactResult:
    output_path: Path
    manifest_entries: tuple[ManifestEntry, ...]
    summary_checks: tuple[ArtifactCheck, ...]
    comparison_checks: tuple[ArtifactCheck, ...]
    report_checks: tuple[ArtifactCheck, ...]
    issues: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.issues and all(
            check.status == "present"
            for check in (
                *self.summary_checks,
                *self.comparison_checks,
                *self.report_checks,
            )
        )

    @property
    def planned_model_count(self) -> int:
        return len(self.manifest_entries)

    @property
    def present_summary_file_count(self) -> int:
        return sum(check.status == "present" for check in self.summary_checks)

    @property
    def missing_summary_file_count(self) -> int:
        return sum(check.status == "missing" for check in self.summary_checks)

    @property
    def present_comparison_file_count(self) -> int:
        return sum(check.status == "present" for check in self.comparison_checks)

    @property
    def missing_comparison_file_count(self) -> int:
        return sum(check.status == "missing" for check in self.comparison_checks)

    @property
    def present_report_file_count(self) -> int:
        return sum(check.status == "present" for check in self.report_checks)

    @property
    def missing_report_file_count(self) -> int:
        return sum(check.status == "missing" for check in self.report_checks)


def audit_final_result_artifacts(
    inputs: FinalResultArtifactInputs,
) -> FinalResultArtifactResult:
    """Check the expected final paper-sweep outputs without creating them."""
    issues: list[str] = []
    manifest_entries = _load_manifest(inputs.manifest_path, issues)
    if inputs.expected_models is not None and len(manifest_entries) != inputs.expected_models:
        issues.append(
            "manifest model count mismatch: "
            f"expected {inputs.expected_models}, found {len(manifest_entries)}"
        )

    summary_checks = tuple(
        check
        for entry in manifest_entries
        for check in _summary_file_checks(entry.summary_dir)
    )
    comparison_checks = tuple(_comparison_file_checks(inputs.comparison_dir))
    report_checks = tuple(_report_file_checks(inputs.report_dir))
    result = FinalResultArtifactResult(
        output_path=inputs.output_path,
        manifest_entries=manifest_entries,
        summary_checks=summary_checks,
        comparison_checks=comparison_checks,
        report_checks=report_checks,
        issues=tuple(issues),
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _load_manifest(path: Path, issues: list[str]) -> tuple[ManifestEntry, ...]:
    if not path.exists():
        issues.append(f"manifest missing: {path}")
        return ()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(REQUIRED_MANIFEST_COLUMNS) - set(reader.fieldnames or ()))
        if missing:
            issues.append(f"{path} missing columns: {', '.join(missing)}")
            return ()
        entries = []
        for index, row in enumerate(reader, start=2):
            label = (row.get("label") or "").strip()
            model = (row.get("model") or "").strip()
            summary_dir = (row.get("summary_dir") or "").strip()
            if not label or not model or not summary_dir:
                issues.append(f"{path}:{index} has a blank label, model, or summary_dir")
                continue
            entries.append(
                ManifestEntry(
                    label=label,
                    model=model,
                    summary_dir=Path(summary_dir),
                )
            )
        return tuple(entries)


def _summary_file_checks(summary_dir: Path) -> list[ArtifactCheck]:
    return [_check_file(summary_dir / filename) for filename in REQUIRED_SUMMARY_FILES]


def _comparison_file_checks(comparison_dir: Path) -> list[ArtifactCheck]:
    return [
        _check_csv(comparison_dir / filename, required_columns)
        for filename, required_columns in REQUIRED_COMPARISON_FILES
    ]


def _report_file_checks(report_dir: Path) -> list[ArtifactCheck]:
    paths = BenchmarkReportPaths(
        html=report_dir / "report.html",
        leaderboard_csv=report_dir / "leaderboard.csv",
        leaderboard_md=report_dir / "leaderboard.md",
        family_heatmap_csv=report_dir / "family-heatmap.csv",
    )
    return [
        _check_file(getattr(paths, attr))
        for attr in (
            "html",
            "leaderboard_csv",
            "leaderboard_md",
            "family_heatmap_csv",
        )
    ]


def _check_file(path: Path) -> ArtifactCheck:
    if not path.exists():
        return ArtifactCheck(path=path, status="missing", evidence="missing")
    if path.stat().st_size == 0:
        return ArtifactCheck(path=path, status="invalid", evidence="empty file")
    return ArtifactCheck(path=path, status="present", evidence=f"{path.stat().st_size} bytes")


def _check_csv(path: Path, required_columns: tuple[str, ...]) -> ArtifactCheck:
    basic = _check_file(path)
    if basic.status != "present":
        return basic
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(required_columns) - set(reader.fieldnames or ()))
        rows = list(reader)
    if missing:
        return ArtifactCheck(
            path=path,
            status="invalid",
            evidence="missing columns: " + ", ".join(missing),
        )
    if not rows and path.name in {"comparison.csv", "family_comparison.csv"}:
        return ArtifactCheck(path=path, status="invalid", evidence="no data rows")
    return ArtifactCheck(
        path=path,
        status="present",
        evidence=f"{len(rows)} row(s), {path.stat().st_size} bytes",
    )


def _render_markdown(
    result: FinalResultArtifactResult,
    inputs: FinalResultArtifactInputs,
) -> str:
    lines = [
        "---",
        "title: Paper V1 Final Result Artifact Audit",
        f"date: {inputs.generated_on}",
        "type: review",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# Paper V1 Final Result Artifact Audit",
        "",
        "This audit checks the output contract for the paper evidence run.",
        "It does not run model providers, rescore logs, or build comparison",
        "reports. It verifies that the manifest, per-model summaries,",
        "comparison CSVs, and generated report files are present.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"- Final sweep manifest: `{inputs.manifest_path}`",
        f"- Comparison directory: `{inputs.comparison_dir}`",
        f"- Report directory: `{inputs.report_dir}`",
        f"- Planned models: {result.planned_model_count}",
        (
            "- Summary files present: "
            f"{result.present_summary_file_count}/{len(result.summary_checks)}"
        ),
        (
            "- Comparison files present: "
            f"{result.present_comparison_file_count}/{len(result.comparison_checks)}"
        ),
        (
            "- Report files present: "
            f"{result.present_report_file_count}/{len(result.report_checks)}"
        ),
        f"- Structural issues: {len(result.issues)}",
        "",
    ]
    lines.extend(_manifest_lines(result.manifest_entries))
    lines.extend(_check_lines("Summary Artifacts", result.summary_checks))
    lines.extend(_check_lines("Comparison Artifacts", result.comparison_checks))
    lines.extend(_check_lines("Report Artifacts", result.report_checks))
    if result.issues:
        lines.extend(["## Issues", ""])
        lines.extend(f"- {issue}" for issue in result.issues)
        lines.append("")
    lines.extend(
        [
            "## Promotion Rule",
            "",
            (
                "Paper result prose may cite this evidence run only when this "
                "audit passes, paper tables and figures are regenerated from "
                "the same comparison directory, and `make -C paper "
                "internal-review` no longer reports result or analysis "
                "placeholder blockers."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def _manifest_lines(entries: tuple[ManifestEntry, ...]) -> list[str]:
    lines = [
        "## Planned Models",
        "",
        "| Label | Model | Summary directory |",
        "| --- | --- | --- |",
    ]
    if not entries:
        lines.append("| n/a | n/a | n/a |")
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(entry.label),
                    _cell(f"`{entry.model}`"),
                    _cell(f"`{entry.summary_dir}`"),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _check_lines(title: str, checks: tuple[ArtifactCheck, ...]) -> list[str]:
    lines = [
        f"## {title}",
        "",
        "| Path | Status | Evidence |",
        "| --- | --- | --- |",
    ]
    if not checks:
        lines.append("| n/a | missing | no checks configured |")
    for check in checks:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(f"`{check.path}`"),
                    check.status.upper(),
                    _cell(check.evidence),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
