"""Audit the current PDF build state for the ObviousBench paper."""

from __future__ import annotations

import re
import shutil
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from obviousbench.research.paper_source_audit import (
    PaperSourceAuditInputs,
    audit_paper_source,
)

PdfAuditStatus = Literal["pass", "fail"]
DEFAULT_LATEX_TOOLS = ("latexmk", "pdflatex", "tectonic")
LOG_ERROR_PATTERNS = (
    r"^!",
    r"LaTeX Error",
    r"Undefined control sequence",
    r"Emergency stop",
    r"Fatal error",
    r"Citation .* undefined",
    r"Reference .* undefined",
    r"Overfull \\hbox",
    r"Overfull \\vbox",
)
REQUIRED_FIGURES = (
    "leaderboard.pdf",
    "family_heatmap.pdf",
    "answer_format_gap.pdf",
    "cost_frontier.pdf",
)
FIGURE_PLACEHOLDER_MARKERS = (
    "No result rows available yet",
    "No family result rows available yet",
    "No cost result rows available yet",
    "No rows available.",
    "No plottable rows available.",
    "No answer or format gaps found",
)
MIN_FIGURE_BYTES = 5_000


@dataclass(frozen=True)
class PaperPdfAuditInputs:
    paper_dir: Path
    output_path: Path
    source_audit_output_path: Path
    pdf_path: Path | None = None
    log_path: Path | None = None
    latex_tools: Sequence[str] = DEFAULT_LATEX_TOOLS
    available_latex_tools: Sequence[str] | None = None
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class PaperPdfCheck:
    name: str
    status: PdfAuditStatus
    evidence: str
    next_action: str


@dataclass(frozen=True)
class PaperPdfAuditResult:
    output_path: Path
    checks: tuple[PaperPdfCheck, ...]

    @property
    def ok(self) -> bool:
        return all(check.status == "pass" for check in self.checks)

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    @property
    def failed_count(self) -> int:
        return sum(check.status == "fail" for check in self.checks)

    def check_by_name(self, name: str) -> PaperPdfCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


def audit_paper_pdf_build(inputs: PaperPdfAuditInputs) -> PaperPdfAuditResult:
    """Write a PDF-build audit without invoking LaTeX."""
    pdf_path = inputs.pdf_path or inputs.paper_dir / "main.pdf"
    log_path = inputs.log_path or inputs.paper_dir / "main.log"
    source_result = audit_paper_source(
        PaperSourceAuditInputs(
            paper_dir=inputs.paper_dir,
            output_path=inputs.source_audit_output_path,
        )
    )
    checks = (
        _toolchain_check(inputs),
        _source_audit_check(source_result),
        _pdf_artifact_check(pdf_path),
        _figure_artifacts_check(inputs.paper_dir / "figures"),
        _log_check(log_path),
    )
    result = PaperPdfAuditResult(output_path=inputs.output_path, checks=checks)
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _toolchain_check(inputs: PaperPdfAuditInputs) -> PaperPdfCheck:
    available = (
        tuple(inputs.available_latex_tools)
        if inputs.available_latex_tools is not None
        else tuple(tool for tool in inputs.latex_tools if shutil.which(tool))
    )
    if available:
        return PaperPdfCheck(
            name="LaTeX toolchain",
            status="pass",
            evidence="Available command(s): " + ", ".join(available),
            next_action="None.",
        )
    return PaperPdfCheck(
        name="LaTeX toolchain",
        status="fail",
        evidence="No command found among: " + ", ".join(inputs.latex_tools),
        next_action="Install latexmk/pdflatex or tectonic before final PDF build.",
    )


def _source_audit_check(source_result) -> PaperPdfCheck:
    if source_result.ok:
        return PaperPdfCheck(
            name="static source audit",
            status="pass",
            evidence=(
                f"{source_result.passed_count} passed, 0 failed. "
                f"Audit: {source_result.output_path}"
            ),
            next_action="None.",
        )
    return PaperPdfCheck(
        name="static source audit",
        status="fail",
        evidence=(
            f"{source_result.passed_count} passed, "
            f"{source_result.failed_count} failed. Audit: {source_result.output_path}"
        ),
        next_action="Resolve static source-audit failures before final PDF inspection.",
    )


def _pdf_artifact_check(path: Path) -> PaperPdfCheck:
    if not path.exists():
        return PaperPdfCheck(
            name="PDF artifact",
            status="fail",
            evidence=f"Missing file: {path}",
            next_action="Run `make -C paper pdf` in a LaTeX-enabled environment.",
        )
    if path.stat().st_size == 0:
        return PaperPdfCheck(
            name="PDF artifact",
            status="fail",
            evidence=f"Empty file: {path}",
            next_action="Rebuild the PDF and inspect the LaTeX output.",
        )
    return PaperPdfCheck(
        name="PDF artifact",
        status="pass",
        evidence=f"PDF exists and is non-empty: {path}",
        next_action="None.",
    )


def _figure_artifacts_check(figures_dir: Path) -> PaperPdfCheck:
    paths = [figures_dir / name for name in REQUIRED_FIGURES]
    missing = [path for path in paths if not path.exists()]
    if missing:
        return PaperPdfCheck(
            name="standalone figure artifacts",
            status="fail",
            evidence="missing: " + ", ".join(str(path) for path in missing),
            next_action="Run paper asset generation against the frozen final results.",
        )
    tiny = [path for path in paths if path.stat().st_size < MIN_FIGURE_BYTES]
    if tiny:
        return PaperPdfCheck(
            name="standalone figure artifacts",
            status="fail",
            evidence=(
                "placeholder-sized figure(s): "
                + ", ".join(f"{path} ({path.stat().st_size} bytes)" for path in tiny)
            ),
            next_action="Regenerate non-placeholder figure PDFs from final results.",
        )
    marker_hits: list[str] = []
    for path in paths:
        text = path.read_bytes().decode("latin1", errors="ignore")
        for marker in FIGURE_PLACEHOLDER_MARKERS:
            if marker in text:
                marker_hits.append(f"{path}: {marker}")
    if marker_hits:
        return PaperPdfCheck(
            name="standalone figure artifacts",
            status="fail",
            evidence="; ".join(marker_hits),
            next_action="Regenerate figures from final result artifacts.",
        )
    return PaperPdfCheck(
        name="standalone figure artifacts",
        status="pass",
        evidence=f"{len(paths)}/{len(paths)} figure PDF(s) present and non-placeholder.",
        next_action="None.",
    )


def _log_check(path: Path) -> PaperPdfCheck:
    if not path.exists():
        return PaperPdfCheck(
            name="LaTeX build log",
            status="fail",
            evidence=f"Missing file: {path}",
            next_action="Run a real PDF build and inspect the resulting log.",
        )
    text = path.read_text(encoding="utf-8", errors="replace")
    issues = _log_issues(text)
    if issues:
        return PaperPdfCheck(
            name="LaTeX build log",
            status="fail",
            evidence=_summarize(issues),
            next_action="Fix fatal, undefined-reference, and overfull-box log issues.",
        )
    return PaperPdfCheck(
        name="LaTeX build log",
        status="pass",
        evidence=f"No fatal, undefined-reference, or overfull-box markers in {path}.",
        next_action="None.",
    )


def _log_issues(text: str) -> list[str]:
    issues: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in LOG_ERROR_PATTERNS:
            if re.search(pattern, line):
                issues.append(f"line {line_number}: {line.strip()}")
                break
    return issues


def _render_markdown(
    result: PaperPdfAuditResult,
    inputs: PaperPdfAuditInputs,
) -> str:
    lines = [
        "---",
        "title: ObviousBench Paper PDF Build Audit",
        f"date: {inputs.generated_on}",
        "type: review",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Paper PDF Build Audit",
        "",
        "This audit records the current PDF build and inspection state without",
        "invoking LaTeX. It should pass before the arXiv source bundle is treated",
        "as upload-ready.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"Summary: {result.passed_count} passed, {result.failed_count} failed.",
        "",
        "| Check | Status | Evidence | Next action |",
        "| --- | --- | --- | --- |",
    ]
    for check in result.checks:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(check.name),
                    check.status.upper(),
                    _cell(check.evidence),
                    _cell(check.next_action),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Final PDF Rule",
            "",
            "Do not mark the source bundle as arXiv-ready until this audit passes",
            "after a real PDF build, and the generated PDF has been visually",
            "inspected for table fit, figure rendering, citation resolution, and",
            "title/abstract consistency.",
            "",
        ]
    )
    return "\n".join(lines)


def _summarize(values: Sequence[str], *, limit: int = 6) -> str:
    shown = "; ".join(values[:limit])
    if len(values) > limit:
        shown += f"; {len(values) - limit} additional issue(s) omitted"
    return shown


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
