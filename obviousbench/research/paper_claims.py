"""Audit unresolved claim blockers in the paper source."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PaperClaimAuditInputs:
    paper_dir: Path
    output_path: Path


@dataclass(frozen=True)
class PaperClaimMarker:
    path: Path
    line_number: int
    marker: str
    line: str


@dataclass(frozen=True)
class PaperClaimAuditResult:
    output_path: Path
    markers: tuple[PaperClaimMarker, ...]

    @property
    def ok(self) -> bool:
        return not self.markers

    @property
    def claimblocked_count(self) -> int:
        return sum(marker.marker == "claimblocked" for marker in self.markers)

    @property
    def obtodo_count(self) -> int:
        return sum(marker.marker == "obtodo" for marker in self.markers)


def find_paper_claim_markers(paper_dir: Path) -> tuple[PaperClaimMarker, ...]:
    """Find unresolved paper claim markers without writing an audit report."""
    return tuple(_iter_markers(paper_dir))


def audit_paper_claims(inputs: PaperClaimAuditInputs) -> PaperClaimAuditResult:
    markers = find_paper_claim_markers(inputs.paper_dir)
    result = PaperClaimAuditResult(output_path=inputs.output_path, markers=markers)
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs.paper_dir), encoding="utf-8")
    return result


def _iter_markers(paper_dir: Path):
    for path in sorted(paper_dir.rglob("*.tex")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if _is_marker_definition(line):
                continue
            for marker in ("claimblocked", "obtodo"):
                if f"\\{marker}" in line:
                    yield PaperClaimMarker(
                        path=path,
                        line_number=line_number,
                        marker=marker,
                        line=line.strip(),
                    )


def _is_marker_definition(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("\\newcommand{\\claimblocked}") or stripped.startswith(
        "\\newcommand{\\obtodo}"
    )


def _render_markdown(result: PaperClaimAuditResult, paper_dir: Path) -> str:
    lines = [
        "---",
        "title: Paper Claim Blocker Audit",
        "date: 2026-06-01",
        "type: review",
        "status: current",
        "---",
        "",
        "# Paper Claim Blocker Audit",
        "",
        f"Overall status: {'PASS' if result.ok else 'FAIL'}",
        "",
        f"Unresolved markers: {len(result.markers)}",
        "",
        f"- `claimblocked`: {result.claimblocked_count}",
        f"- `obtodo`: {result.obtodo_count}",
        "",
    ]
    if result.markers:
        lines.extend(["## Markers", ""])
        for marker in result.markers:
            relative = marker.path.relative_to(paper_dir)
            lines.append(
                f"- `{relative}:{marker.line_number}` `{marker.marker}`: "
                f"{_truncate(marker.line)}"
            )
        lines.append("")
    return "\n".join(lines)


def _truncate(text: str, limit: int = 160) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."
