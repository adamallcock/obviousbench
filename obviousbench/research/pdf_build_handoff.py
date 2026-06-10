"""Build a PDF toolchain and inspection handoff for the ObviousBench paper."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

HandoffStatus = Literal["pass", "blocked"]
DEFAULT_LATEX_COMMANDS = ("latexmk", "pdflatex", "tectonic")
DEFAULT_SUPPORT_COMMANDS = ("brew", "tlmgr", "pandoc", "quarto")


@dataclass(frozen=True)
class PdfBuildHandoffInputs:
    output_path: Path
    pdf_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md"
    )
    source_audit_path: Path = Path(
        "docs/research/2026-06-01-obviousbench-paper-source-audit.md"
    )
    generated_on: str = "2026-06-01"
    latex_commands: tuple[str, ...] = DEFAULT_LATEX_COMMANDS
    support_commands: tuple[str, ...] = DEFAULT_SUPPORT_COMMANDS
    available_commands: tuple[str, ...] | None = None


@dataclass(frozen=True)
class PdfBuildHandoffResult:
    output_path: Path
    status: HandoffStatus
    pdf_audit_status: str
    source_audit_status: str
    available_latex_commands: tuple[str, ...]
    available_support_commands: tuple[str, ...]
    blockers: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return self.status == "pass"


def build_pdf_build_handoff(
    inputs: PdfBuildHandoffInputs,
) -> PdfBuildHandoffResult:
    """Write a durable PDF build and inspection handoff."""
    available = _available_commands(inputs)
    pdf_text = _read_text(inputs.pdf_audit_path)
    source_text = _read_text(inputs.source_audit_path)
    pdf_status = _overall_status(pdf_text)
    source_status = _overall_status(source_text)
    available_latex = tuple(cmd for cmd in inputs.latex_commands if cmd in available)
    available_support = tuple(cmd for cmd in inputs.support_commands if cmd in available)
    blockers = _blockers(
        pdf_status=pdf_status,
        source_status=source_status,
        available_latex=available_latex,
        pdf_text=pdf_text,
        source_text=source_text,
    )
    status: HandoffStatus = "pass" if not blockers else "blocked"
    result = PdfBuildHandoffResult(
        output_path=inputs.output_path,
        status=status,
        pdf_audit_status=pdf_status,
        source_audit_status=source_status,
        available_latex_commands=available_latex,
        available_support_commands=available_support,
        blockers=tuple(blockers),
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _available_commands(inputs: PdfBuildHandoffInputs) -> set[str]:
    if inputs.available_commands is not None:
        return set(inputs.available_commands)
    commands = set(inputs.latex_commands) | set(inputs.support_commands)
    return {command for command in commands if shutil.which(command)}


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _overall_status(text: str) -> str:
    match = re.search(r"Overall status:\s+([A-Z]+)", text)
    return match.group(1) if match else "MISSING"


def _summary(text: str) -> str:
    match = re.search(r"Summary:\s+(.+)", text)
    return match.group(1).strip() if match else "not recorded"


def _blockers(
    *,
    pdf_status: str,
    source_status: str,
    available_latex: tuple[str, ...],
    pdf_text: str,
    source_text: str,
) -> list[str]:
    blockers: list[str] = []
    if not available_latex:
        blockers.append("No LaTeX build command is available on PATH.")
    if pdf_status != "PASS":
        blockers.append(f"PDF build audit is {pdf_status.lower()}.")
    if source_status != "PASS":
        blockers.append(f"Static source audit is {source_status.lower()}.")
    if "Missing file: paper/main.pdf" in pdf_text:
        blockers.append("No built `paper/main.pdf` is present.")
    if "Missing file: paper/main.log" in pdf_text:
        blockers.append("No `paper/main.log` exists for inspection.")
    if "submission markers" in source_text.lower() and "FAIL" in source_text:
        blockers.append("Draft submission markers remain in TeX source.")
    return blockers


def _render_markdown(
    result: PdfBuildHandoffResult,
    inputs: PdfBuildHandoffInputs,
) -> str:
    latex_available = (
        ", ".join(f"`{cmd}`" for cmd in result.available_latex_commands)
        if result.available_latex_commands
        else "none"
    )
    support_available = (
        ", ".join(f"`{cmd}`" for cmd in result.available_support_commands)
        if result.available_support_commands
        else "none"
    )
    lines = [
        "---",
        "title: ObviousBench PDF Build Handoff",
        f"date: {inputs.generated_on}",
        "type: runbook",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench PDF Build Handoff",
        "",
        "This generated handoff records the local PDF build state, off-the-shelf",
        "toolchain options, and final inspection ladder for the arXiv manuscript.",
        "It does not install software, compile LaTeX, collect data, or run model",
        "providers.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"PDF audit status: {result.pdf_audit_status}",
        "",
        f"Source audit status: {result.source_audit_status}",
        "",
        f"Available LaTeX commands: {latex_available}",
        "",
        f"Available support commands: {support_available}",
        "",
        "## Current Blockers",
        "",
    ]
    if result.blockers:
        for blocker in result.blockers:
            lines.append(f"- {blocker}")
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Recommended Toolchain",
            "",
            "1. For the smallest local install, use Tectonic. The official Tectonic",
            "   documentation describes it as a single executable that downloads",
            "   TeX support files on demand. With Homebrew available, use:",
            "",
            "   ```bash",
            "   brew install tectonic",
            "   ```",
            "",
            "2. For maximum arXiv/TeX Live parity on macOS, use MacTeX. The official",
            "   MacTeX distribution includes TeX, LaTeX, XeTeX, LuaTeX, and related",
            "   tooling. With Homebrew available, use:",
            "",
            "   ```bash",
            "   brew install --cask mactex",
            "   ```",
            "",
            "3. If a system TeX Live install already exists, ensure `latexmk` or",
            "   `pdflatex` is on PATH and rerun the audit before treating the build",
            "   as reproducible.",
            "",
            "## Build Ladder",
            "",
            "```bash",
            "make -C paper related-work",
            "make -C paper assets",
            "make -C paper source-audit",
            "make -C paper pdf",
            "make -C paper pdf-audit",
            "make -C paper arxiv-audit",
            "make -C paper preflight",
            "```",
            "",
            "The source audit is expected to stay blocked while draft markers remain.",
            "A draft PDF may still be useful for layout review, but the final PDF",
            "handoff is not ready until the source audit and PDF audit both pass.",
            "",
            "## Inspection Checklist",
            "",
            "- Title, author block, and abstract match the final metadata note.",
            "- Every table fits the page and preserves readable captions.",
            "- Every figure renders and is not a placeholder shell.",
            "- Bibliography and citation references resolve.",
            "- `paper/main.log` has no fatal errors, undefined references, missing",
            "  citations, or overfull boxes that affect readability.",
            "- The rebuilt `paper/arxiv-src.tar.gz` excludes local logs, raw provider",
            "  outputs, credentials, private prompts, and generated caches.",
            "",
            "## Stop Rules",
            "",
            "- Do not mark the source bundle upload-ready while this handoff is",
            "  blocked.",
            "- Do not use a hand-built PDF as evidence unless `make -C paper pdf-audit`",
            "  has been rerun after that build.",
            "- Do not replace claim blockers just because the PDF compiles; claim",
            "  blockers require human-baseline, final-result, metadata, or release",
            "  evidence.",
            "",
            "## Source Notes",
            "",
            "- Tectonic install docs: <https://tectonic-typesetting.github.io/book/latest/installation/>",
            "- MacTeX project: <https://tug.org/mactex/>",
            "- arXiv TeX submission help: <https://info.arxiv.org/help/submit_tex.html>",
            "",
            "## Audit Inputs",
            "",
            (
                f"- PDF audit: `{inputs.pdf_audit_path}` "
                f"({_summary(_read_text(inputs.pdf_audit_path))})"
            ),
            (
                f"- Source audit: `{inputs.source_audit_path}` "
                f"({_summary(_read_text(inputs.source_audit_path))})"
            ),
            "",
        ]
    )
    return "\n".join(lines)
