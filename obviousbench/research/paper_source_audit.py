"""Static LaTeX source audit for the ObviousBench paper."""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

SourceAuditStatus = Literal["pass", "fail"]

INPUT_RE = re.compile(r"\\input\{([^}]+)\}")
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\{([^}]+)\}")
BIBLIOGRAPHY_RE = re.compile(r"\\bibliography\{([^}]+)\}")
BIB_ENTRY_RE = re.compile(r"@\w+\{([^,\s]+)")
SUBMISSION_MARKERS = (
    "\\claimblocked",
    "\\obtodo",
    "No final",
    "placeholder",
    "Draft:",
    "TODO",
)


@dataclass(frozen=True)
class PaperSourceAuditInputs:
    paper_dir: Path
    output_path: Path
    main_tex: str = "main.tex"


@dataclass(frozen=True)
class PaperSourceCheck:
    name: str
    status: SourceAuditStatus
    evidence: str
    next_action: str


@dataclass(frozen=True)
class PaperSourceAuditResult:
    output_path: Path
    checks: tuple[PaperSourceCheck, ...]

    @property
    def ok(self) -> bool:
        return all(check.status == "pass" for check in self.checks)

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    @property
    def failed_count(self) -> int:
        return sum(check.status == "fail" for check in self.checks)

    def check_by_name(self, name: str) -> PaperSourceCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


def audit_paper_source(inputs: PaperSourceAuditInputs) -> PaperSourceAuditResult:
    """Audit static TeX source references without invoking a LaTeX engine."""
    paper_dir = inputs.paper_dir
    main_path = paper_dir / inputs.main_tex
    tex_files = tuple(sorted(paper_dir.rglob("*.tex")))
    text_by_path = _read_texts(tex_files)
    combined_text = "\n".join(text_by_path.values())
    checks = (
        _main_source_check(main_path),
        _input_files_check(paper_dir, text_by_path),
        _graphics_files_check(paper_dir, text_by_path),
        _bibliography_file_check(paper_dir, combined_text),
        _citation_keys_check(paper_dir, combined_text),
        _submission_markers_check(paper_dir, text_by_path),
    )
    result = PaperSourceAuditResult(output_path=inputs.output_path, checks=checks)
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result), encoding="utf-8")
    return result


def _main_source_check(main_path: Path) -> PaperSourceCheck:
    if not main_path.exists():
        return PaperSourceCheck(
            name="main source",
            status="fail",
            evidence=f"Missing main TeX file: {main_path}",
            next_action="Create paper/main.tex before packaging.",
        )
    text = main_path.read_text(encoding="utf-8")
    missing = [
        marker
        for marker in ("\\documentclass", "\\begin{document}", "\\end{document}")
        if marker not in text
    ]
    if missing:
        return PaperSourceCheck(
            name="main source",
            status="fail",
            evidence="Missing required marker(s): " + ", ".join(missing),
            next_action="Fix the main TeX document skeleton.",
        )
    return PaperSourceCheck(
        name="main source",
        status="pass",
        evidence=f"Main source exists: {main_path}",
        next_action="None.",
    )


def _input_files_check(
    paper_dir: Path,
    text_by_path: dict[Path, str],
) -> PaperSourceCheck:
    references = _collect_references(INPUT_RE, text_by_path.values())
    missing = [
        ref
        for ref in references
        if not _resolve_tex_reference(paper_dir, ref).exists()
    ]
    if missing:
        return PaperSourceCheck(
            name="input files",
            status="fail",
            evidence="Missing input target(s): " + _summarize(missing),
            next_action="Create missing section/table inputs or update TeX references.",
        )
    return PaperSourceCheck(
        name="input files",
        status="pass",
        evidence=f"{len(references)} input target(s) resolve.",
        next_action="None.",
    )


def _graphics_files_check(
    paper_dir: Path,
    text_by_path: dict[Path, str],
) -> PaperSourceCheck:
    references = _collect_references(GRAPHICS_RE, text_by_path.values())
    missing = [ref for ref in references if not (paper_dir / ref).exists()]
    empty = [
        ref
        for ref in references
        if (paper_dir / ref).exists() and (paper_dir / ref).stat().st_size == 0
    ]
    issues = [f"missing {ref}" for ref in missing] + [f"empty {ref}" for ref in empty]
    if issues:
        return PaperSourceCheck(
            name="figure files",
            status="fail",
            evidence=_summarize(issues),
            next_action="Regenerate or fix figure references.",
        )
    return PaperSourceCheck(
        name="figure files",
        status="pass",
        evidence=f"{len(references)} figure target(s) resolve and are non-empty.",
        next_action="None.",
    )


def _bibliography_file_check(paper_dir: Path, combined_text: str) -> PaperSourceCheck:
    references = _collect_references(BIBLIOGRAPHY_RE, (combined_text,))
    missing = []
    for ref_group in references:
        for ref in _split_csv(ref_group):
            if not _resolve_bib_reference(paper_dir, ref).exists():
                missing.append(ref)
    if missing:
        return PaperSourceCheck(
            name="bibliography files",
            status="fail",
            evidence="Missing bibliography file(s): " + _summarize(missing),
            next_action="Create missing .bib files or update bibliography references.",
        )
    return PaperSourceCheck(
        name="bibliography files",
        status="pass",
        evidence=f"{len(references)} bibliography directive(s) resolve.",
        next_action="None.",
    )


def _citation_keys_check(paper_dir: Path, combined_text: str) -> PaperSourceCheck:
    cited_keys = {
        key
        for ref_group in _collect_references(CITE_RE, (combined_text,))
        for key in _split_csv(ref_group)
    }
    bib_files = [
        _resolve_bib_reference(paper_dir, ref)
        for ref_group in _collect_references(BIBLIOGRAPHY_RE, (combined_text,))
        for ref in _split_csv(ref_group)
    ]
    known_keys: set[str] = set()
    for bib_file in bib_files:
        if bib_file.exists():
            known_keys.update(BIB_ENTRY_RE.findall(bib_file.read_text(encoding="utf-8")))
    missing = sorted(cited_keys - known_keys)
    if missing:
        return PaperSourceCheck(
            name="citation keys",
            status="fail",
            evidence="Missing citation key(s): " + _summarize(missing),
            next_action="Add missing BibTeX entries or fix citation keys.",
        )
    return PaperSourceCheck(
        name="citation keys",
        status="pass",
        evidence=f"{len(cited_keys)} cited key(s) resolve in bibliography.",
        next_action="None.",
    )


def _submission_markers_check(
    paper_dir: Path,
    text_by_path: dict[Path, str],
) -> PaperSourceCheck:
    issues: list[str] = []
    for path, text in sorted(text_by_path.items()):
        for line_number, line in enumerate(text.splitlines(), 1):
            if _is_marker_definition(line):
                continue
            for marker in SUBMISSION_MARKERS:
                if marker == "placeholder" and "placeholder-free" in line.lower():
                    continue
                if marker.lower() in line.lower():
                    issues.append(
                        f"{path.relative_to(paper_dir)}:{line_number} contains {marker!r}"
                    )
                    break
    if issues:
        return PaperSourceCheck(
            name="submission markers",
            status="fail",
            evidence=_summarize(issues),
            next_action="Replace draft markers and placeholders before final upload.",
        )
    return PaperSourceCheck(
        name="submission markers",
        status="pass",
        evidence="No draft or claim-blocker markers found in TeX sources.",
        next_action="None.",
    )


def _read_texts(paths: Sequence[Path]) -> dict[Path, str]:
    return {path: path.read_text(encoding="utf-8") for path in paths}


def _collect_references(pattern: re.Pattern[str], texts: Iterable[str]) -> list[str]:
    references: list[str] = []
    for text in texts:
        references.extend(match.strip() for match in pattern.findall(text))
    return references


def _split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def _resolve_tex_reference(paper_dir: Path, ref: str) -> Path:
    path = paper_dir / ref
    if path.suffix:
        return path
    return path.with_suffix(".tex")


def _resolve_bib_reference(paper_dir: Path, ref: str) -> Path:
    path = paper_dir / ref
    if path.suffix:
        return path
    return path.with_suffix(".bib")


def _is_marker_definition(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("\\newcommand{\\claimblocked}") or stripped.startswith(
        "\\newcommand{\\obtodo}"
    )


def _render_markdown(result: PaperSourceAuditResult) -> str:
    lines = [
        "---",
        "title: ObviousBench Paper Source Audit",
        "date: 2026-06-01",
        "type: review",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Paper Source Audit",
        "",
        "This static audit checks TeX references without running a LaTeX engine.",
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
                    _markdown_cell(check.name),
                    check.status.upper(),
                    _markdown_cell(check.evidence),
                    _markdown_cell(check.next_action),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _summarize(values: Sequence[str], *, limit: int = 5) -> str:
    shown = "; ".join(values[:limit])
    if len(values) > limit:
        shown += f"; {len(values) - limit} additional issue(s) omitted"
    return shown


def _markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()
