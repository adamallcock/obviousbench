"""Build an evidence ledger for unresolved paper claim markers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from obviousbench.research.paper_claims import (
    PaperClaimMarker,
    find_paper_claim_markers,
)


@dataclass(frozen=True)
class PaperClaimLedgerInputs:
    paper_dir: Path
    output_path: Path


@dataclass(frozen=True)
class PaperClaimLedgerEntry:
    path: Path
    line_number: int
    marker: str
    category: str
    status: str
    marker_text: str
    required_evidence: str
    source_artifacts: tuple[str, ...]
    acceptance: str


@dataclass(frozen=True)
class PaperClaimLedgerResult:
    output_path: Path
    entries: tuple[PaperClaimLedgerEntry, ...]

    @property
    def ok(self) -> bool:
        return not self.entries

    @property
    def blocked_count(self) -> int:
        return len(self.entries)


def build_paper_claim_ledger(
    inputs: PaperClaimLedgerInputs,
) -> PaperClaimLedgerResult:
    """Render a replacement plan for every unresolved paper marker."""
    markers = find_paper_claim_markers(inputs.paper_dir)
    entries = tuple(_entry_from_marker(inputs.paper_dir, marker) for marker in markers)
    result = PaperClaimLedgerResult(output_path=inputs.output_path, entries=entries)
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result), encoding="utf-8")
    return result


def _entry_from_marker(
    paper_dir: Path,
    marker: PaperClaimMarker,
) -> PaperClaimLedgerEntry:
    relative = marker.path.relative_to(paper_dir)
    marker_text = _extract_marker_text(marker)
    category, evidence, artifacts, acceptance = _classify_marker(relative, marker_text)
    return PaperClaimLedgerEntry(
        path=relative,
        line_number=marker.line_number,
        marker=marker.marker,
        category=category,
        status="blocked",
        marker_text=marker_text,
        required_evidence=evidence,
        source_artifacts=artifacts,
        acceptance=acceptance,
    )


def _classify_marker(
    relative_path: Path,
    line: str,
) -> tuple[str, str, tuple[str, ...], str]:
    haystack = f"{relative_path} {line}".lower()
    if "author" in haystack or "affiliation" in haystack or "contact" in haystack:
        return (
            "submission metadata",
            "Confirmed author list, affiliations, contact email, and arXiv metadata.",
            (
                "docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md",
                "paper/main.tex",
            ),
            "Metadata note is confirmed and paper author block is final.",
        )
    if "abstract" in haystack:
        return (
            "abstract and headline claims",
            (
                "Final dataset, model-panel, result, deferred human-validation, "
                "and release facts."
            ),
            (
                "data/splits/paper_v1_manifest.jsonl",
                "results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison",
                "docs/reports/2026-06-02-paper-v1-combined-234-overline",
                "docs/research/2026-06-01-obviousbench-fast-human-baseline-options.md",
            ),
            "Abstract contains only facts supported by frozen artifacts.",
        )
    if "contribution" in haystack:
        return (
            "introduction contributions",
            "Exact paper split counts, review counts, model-panel size, and release links.",
            (
                "data/splits/paper_v1_manifest.jsonl",
                "data/item_cards/public_v0/cards.yaml",
                "configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv",
                "docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md",
            ),
            "Contribution list uses exact artifact-backed counts and links.",
        )
    if "item card" in haystack or "paper split" in haystack:
        return (
            "data and item-card review",
            "Manifest-scoped readiness audit and reviewed item cards.",
            (
                "data/splits/paper_v1_manifest.jsonl",
                "data/item_cards/public_v0/cards.yaml",
                "docs/research/2026-06-01-obviousbench-arxiv-readiness-audit.md",
            ),
            "Readiness and item-card gates pass for all paper items.",
        )
    if "human" in haystack or "baseline" in haystack:
        return (
            "human validation",
            (
                "Either explicit deferral language for the fast preprint or "
                "audited human-baseline rows for a strict version."
            ),
            (
                "data/human_baseline/paper_v1.csv",
                "docs/research/2026-06-01-obviousbench-fast-human-baseline-options.md",
                "docs/research/2026-06-01-paper-v1-human-baseline-form.md",
            ),
            (
                "The marker is replaced with deferred-validation wording, or "
                "the strict human-baseline gate passes."
            ),
        )
    if (
        "model-comparison" in haystack
        or "sweep" in haystack
        or "family heatmap" in haystack
        or "cost frontier" in haystack
        or "comparison artifacts" in haystack
    ):
        return (
            "final model results",
            "Frozen paper-sweep summaries, comparison tables, and generated figures.",
            (
                "docs/research/2026-06-01-paper-v1-final-sweep-plan.md",
                "configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv",
                "results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison",
                "paper/tables/main_results.tex",
                "paper/figures/leaderboard.pdf",
            ),
            "Final sweep is complete and paper assets are regenerated from it.",
        )
    if "discussion" in haystack or "observed model" in haystack:
        return (
            "discussion interpretation",
            "Final result patterns plus limitations-reviewed interpretation.",
            (
                "results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison",
                "docs/research/2026-06-01-obviousbench-arxiv-internal-review.md",
                "paper/sections/08_discussion.tex",
            ),
            "Discussion cites observed patterns without unsupported rankings or mechanisms.",
        )
    return (
        "general claim evidence",
        "Direct artifact evidence for the marked statement.",
        (
            "docs/research/2026-06-01-obviousbench-arxiv-internal-review.md",
            "docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md",
        ),
        "Marker is removed only after the source artifact supports replacement text.",
    )


def _render_markdown(result: PaperClaimLedgerResult) -> str:
    lines = [
        "---",
        "title: ObviousBench Paper Claim Evidence Ledger",
        "date: 2026-06-01",
        "type: review",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Paper Claim Evidence Ledger",
        "",
        "This ledger turns unresolved manuscript markers into artifact-backed",
        "replacement work. It is editorial guidance; the claim-blocker audit",
        "remains the hard gate.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"Blocked entries: {result.blocked_count}",
        "",
    ]
    if not result.entries:
        lines.append("No unresolved claim markers were found.")
        lines.append("")
        return "\n".join(lines)

    lines.extend(
        [
            "| Location | Marker | Category | Required evidence | Source artifacts | Acceptance |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for entry in result.entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_cell(f"{entry.path}:{entry.line_number}"),
                    _markdown_cell(entry.marker),
                    _markdown_cell(entry.category),
                    _markdown_cell(entry.required_evidence),
                    _markdown_cell(", ".join(entry.source_artifacts)),
                    _markdown_cell(entry.acceptance),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Marker Text", ""])
    for entry in result.entries:
        lines.append(
            f"- `{entry.path}:{entry.line_number}` `{entry.marker}`: "
            f"{_markdown_cell(entry.marker_text)}"
        )
    lines.append("")
    return "\n".join(lines)


def _clean_marker_text(line: str) -> str:
    return " ".join(line.strip().split())


def _extract_marker_text(marker: PaperClaimMarker) -> str:
    lines = marker.path.read_text(encoding="utf-8").splitlines()
    source = "\n".join(lines[marker.line_number - 1 :])
    command = f"\\{marker.marker}"
    start = source.find(command)
    if start == -1:
        return _clean_marker_text(marker.line)
    opening = source.find("{", start + len(command))
    if opening == -1:
        return _clean_marker_text(marker.line)
    depth = 1
    body_chars: list[str] = []
    for char in source[opening + 1 :]:
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return _clean_marker_text("".join(body_chars))
        body_chars.append(char)
    return _clean_marker_text(source[start:])


def _markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()
