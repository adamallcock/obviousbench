"""Build a small public/shareable results bundle from summary artifacts."""

from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ShareableArtifactInputs:
    comparison_dir: Path
    output_dir: Path
    generated_on: str
    benchmark_card_source: Path
    model_matrix_source: Path = Path("configs/models_v0.example.yaml")
    max_failures: int = 8


@dataclass(frozen=True)
class ShareableArtifactPaths:
    card: Path
    gallery: Path
    comparison: Path
    family_comparison: Path
    model_matrix: Path
    index: Path


def build_shareable_artifacts(inputs: ShareableArtifactInputs) -> ShareableArtifactPaths:
    """Create a reviewable bundle without raw provider logs."""
    inputs.output_dir.mkdir(parents=True, exist_ok=True)

    comparison_source = inputs.comparison_dir / "comparison.csv"
    family_source = inputs.comparison_dir / "family_comparison.csv"
    comparison_rows = _read_csv(comparison_source)
    family_rows = _read_csv(family_source)

    paths = ShareableArtifactPaths(
        card=inputs.output_dir / "benchmark-card.md",
        gallery=inputs.output_dir / "failure-gallery.md",
        comparison=inputs.output_dir / "model-comparison.csv",
        family_comparison=inputs.output_dir / "family-comparison.csv",
        model_matrix=inputs.output_dir / "model-matrix.yaml",
        index=inputs.output_dir / "README.md",
    )

    paths.card.write_text(
        _build_card(
            source=inputs.benchmark_card_source,
            generated_on=inputs.generated_on,
            comparison_rows=comparison_rows,
            family_rows=family_rows,
        ),
        encoding="utf-8",
    )
    paths.gallery.write_text(
        _build_gallery(comparison_rows, max_failures=inputs.max_failures),
        encoding="utf-8",
    )
    shutil.copyfile(comparison_source, paths.comparison)
    shutil.copyfile(family_source, paths.family_comparison)
    if inputs.model_matrix_source.exists():
        shutil.copyfile(inputs.model_matrix_source, paths.model_matrix)
    else:
        paths.model_matrix.write_text(
            "# Model matrix source was not found during artifact generation.\n",
            encoding="utf-8",
        )
    paths.index.write_text(_build_index(inputs.generated_on), encoding="utf-8")

    return paths


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _build_card(
    *,
    source: Path,
    generated_on: str,
    comparison_rows: list[dict[str, str]],
    family_rows: list[dict[str, str]],
) -> str:
    base = source.read_text(encoding="utf-8").rstrip()
    lines = [base, "", "## Latest Comparison Snapshot", "", f"Generated on: {generated_on}", ""]
    for row in comparison_rows:
        label = row.get("label") or row.get("model") or "model"
        accuracy = _percent(row.get("accuracy"))
        failure_rate = _percent(row.get("obvious_failure_rate"))
        cost = row.get("estimated_cost_usd") or ""
        lines.append(
            f"- {label}: {accuracy} accuracy, {failure_rate} obvious failure rate"
            f"{_cost_suffix(cost)}."
        )

    failures_by_family: dict[str, int] = {}
    for row in family_rows:
        family = row.get("family", "")
        failures = _int(row.get("failures"))
        if family and failures:
            failures_by_family[family] = failures_by_family.get(family, 0) + failures

    if failures_by_family:
        lines.extend(["", "## Failure Hotspots", ""])
        for family, failures in sorted(failures_by_family.items()):
            lines.append(f"- {family}: {failures} failures")

    return "\n".join(lines) + "\n"


def _build_gallery(comparison_rows: list[dict[str, str]], *, max_failures: int) -> str:
    sections = [
        "# ObviousBench Failure Gallery",
        "",
        "Curated examples from summarized local runs. Raw Inspect logs and provider "
        "payloads are intentionally excluded.",
        "",
    ]
    failures_added = 0
    for row in comparison_rows:
        summary_dir = Path(row.get("summary_dir", ""))
        gallery = summary_dir / "failure_gallery.md"
        if not gallery.exists():
            continue
        label = row.get("label") or row.get("model") or summary_dir.name
        for failure in _failure_sections(gallery.read_text(encoding="utf-8")):
            if failures_added >= max_failures:
                return "\n".join(sections).rstrip() + "\n"
            failures_added += 1
            sections.append(f"## Example {failures_added}: {label}")
            sections.append("")
            sections.append(_without_failure_heading(failure))
            sections.append("")
    if failures_added == 0:
        sections.append("No scored model failures were available in the selected summaries.")
    return "\n".join(sections).rstrip() + "\n"


def _failure_sections(markdown: str) -> list[str]:
    sections: list[str] = []
    current: list[str] = []
    for line in markdown.splitlines():
        if line.startswith("## Failure "):
            if current:
                sections.append("\n".join(current).strip())
            current = [line]
        elif current:
            current.append(line)
    if current:
        sections.append("\n".join(current).strip())
    return sections


def _without_failure_heading(section: str) -> str:
    lines = section.splitlines()
    if len(lines) > 2 and lines[1] == "":
        return "\n".join(lines[2:]).strip()
    return "\n".join(lines[1:]).strip()


def _build_index(generated_on: str) -> str:
    return "\n".join(
        [
            "# ObviousBench Shareable Results",
            "",
            f"Generated on: {generated_on}",
            "",
            "- `benchmark-card.md`: benchmark scope and headline comparison.",
            "- `failure-gallery.md`: human-readable examples of observed failures.",
            "- `model-comparison.csv`: model-level metrics with token and cost columns.",
            "- `family-comparison.csv`: family-level breakdowns.",
            "- `model-matrix.yaml`: exact Inspect model strings for the promoted panel.",
            "",
            "Raw Inspect logs are intentionally not included.",
            "",
        ]
    )


def _percent(value: str | None) -> str:
    try:
        return f"{float(value or 0) * 100:.1f}%"
    except ValueError:
        return "0.0%"


def _cost_suffix(value: str) -> str:
    if not value:
        return ""
    try:
        return f", estimated cost ${float(value):.6f}"
    except ValueError:
        return ""


def _int(value: str | None) -> int:
    try:
        return int(float(value or 0))
    except ValueError:
        return 0
