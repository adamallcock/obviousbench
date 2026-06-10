"""Build a section-level completion tracker for the ObviousBench paper."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from obviousbench.research.paper_claims import (
    PaperClaimMarker,
    find_paper_claim_markers,
)

TABLE_INPUT_RE = re.compile(r"\\input\{(tables/[^}]+)\}")
FIGURE_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\{([^}]+)\}")
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
DRAFT_PLACEHOLDER_PATTERNS = (
    "placeholder until",
    "placeholder generated",
    "replace the placeholder",
    "remains a placeholder",
)


@dataclass(frozen=True)
class ReportSectionTrackerInputs:
    paper_dir: Path
    output_path: Path
    generated_on: str = "2026-06-01"
    main_tex: str = "main.tex"


@dataclass(frozen=True)
class ReportSectionEntry:
    path: Path
    title: str
    role: str
    status: str
    word_count: int
    table_inputs: tuple[str, ...]
    figures: tuple[str, ...]
    citation_count: int
    claimblocked_count: int
    obtodo_count: int
    placeholder_count: int
    dependencies: tuple[str, ...]
    next_action: str

    @property
    def marker_count(self) -> int:
        return self.claimblocked_count + self.obtodo_count


@dataclass(frozen=True)
class ReportSectionTrackerResult:
    output_path: Path
    entries: tuple[ReportSectionEntry, ...]

    @property
    def blocked_count(self) -> int:
        return sum(entry.status == "blocked" for entry in self.entries)

    @property
    def unresolved_marker_count(self) -> int:
        return sum(entry.marker_count for entry in self.entries)

    @property
    def placeholder_count(self) -> int:
        return sum(entry.placeholder_count for entry in self.entries)

    def entry_by_path(self, path: str) -> ReportSectionEntry:
        for entry in self.entries:
            if entry.path.as_posix() == path:
                return entry
        raise KeyError(path)


def build_report_section_tracker(
    inputs: ReportSectionTrackerInputs,
) -> ReportSectionTrackerResult:
    """Write a durable section-by-section paper completion tracker."""
    paper_dir = inputs.paper_dir
    markers_by_path = _markers_by_path(paper_dir)
    entries = tuple(
        _build_entry(paper_dir, path, markers_by_path.get(path, ()))
        for path in _paper_paths(paper_dir, inputs.main_tex)
    )
    result = ReportSectionTrackerResult(
        output_path=inputs.output_path,
        entries=entries,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _paper_paths(paper_dir: Path, main_tex: str) -> tuple[Path, ...]:
    paths = []
    main_path = paper_dir / main_tex
    if main_path.exists():
        paths.append(main_path)
    paths.extend(sorted((paper_dir / "sections").glob("*.tex")))
    return tuple(paths)


def _markers_by_path(paper_dir: Path) -> dict[Path, tuple[PaperClaimMarker, ...]]:
    grouped: dict[Path, list[PaperClaimMarker]] = {}
    for marker in find_paper_claim_markers(paper_dir):
        grouped.setdefault(marker.path, []).append(marker)
    return {path: tuple(markers) for path, markers in grouped.items()}


def _build_entry(
    paper_dir: Path,
    path: Path,
    markers: tuple[PaperClaimMarker, ...],
) -> ReportSectionEntry:
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(paper_dir)
    claimblocked_count = sum(marker.marker == "claimblocked" for marker in markers)
    obtodo_count = sum(marker.marker == "obtodo" for marker in markers)
    placeholder_count = _draft_placeholder_count(text)
    status = _status(markers, placeholder_count)
    dependencies = _dependencies(relative, markers)
    return ReportSectionEntry(
        path=relative,
        title=_title(relative, text),
        role=_role(relative, text),
        status=status,
        word_count=_word_count(text),
        table_inputs=tuple(TABLE_INPUT_RE.findall(text)),
        figures=tuple(FIGURE_RE.findall(text)),
        citation_count=sum(len(_split_csv(match)) for match in CITE_RE.findall(text)),
        claimblocked_count=claimblocked_count,
        obtodo_count=obtodo_count,
        placeholder_count=placeholder_count,
        dependencies=dependencies,
        next_action=_next_action(status, dependencies, placeholder_count, relative),
    )


def _title(relative: Path, text: str) -> str:
    if relative.name == "main.tex":
        return "Title and Abstract"
    matches = _section_titles(text)
    if matches:
        return "; ".join(matches)
    return relative.stem.replace("_", " ").replace("-", " ").title()


def _role(relative: Path, text: str) -> str:
    title = _title(relative, text)
    haystack = f"{relative.as_posix()} {title}".lower()
    if relative.name == "main.tex":
        return "headline framing, metadata, and abstract"
    if "appendix" in haystack:
        return "artifact schema, commands, and reporting checklists"
    if "introduction" in haystack:
        return "motivation, scope, and contribution claims"
    if "related" in haystack:
        return "benchmark positioning and comparator coverage"
    if "data" in haystack:
        return "item review, source safety, and deferred human-validation policy"
    if "scoring" in haystack:
        return "scorer definitions, model panel, and run settings"
    if "results" in haystack:
        return "final empirical tables, figures, costs, and deferred human validation"
    if "analysis" in haystack:
        return "diagnostic slices and failure-mode interpretation"
    if "discussion" in haystack:
        return "interpretation, tradeoffs, and restrained conclusions"
    if "limitations" in haystack:
        return "limitations, ethics, source safety, and reproducibility"
    if "benchmark" in haystack:
        return "task taxonomy, split protocol, and data composition"
    return "paper section"


def _status(markers: tuple[PaperClaimMarker, ...], placeholder_count: int) -> str:
    if markers:
        return "blocked"
    if placeholder_count:
        return "draft-placeholder"
    return "draft-clean"


def _dependencies(
    relative: Path,
    markers: tuple[PaperClaimMarker, ...],
) -> tuple[str, ...]:
    dependencies = []
    for marker in markers:
        dependency = _dependency_for_marker(relative, marker)
        if dependency not in dependencies:
            dependencies.append(dependency)
    return tuple(dependencies)


def _dependency_for_marker(relative: Path, marker: PaperClaimMarker) -> str:
    haystack = f"{relative.as_posix()} {marker.line}".lower()
    if marker.marker == "obtodo" or "author" in haystack:
        return "final submission metadata"
    if "abstract" in haystack or relative.name == "main.tex":
        return "headline dataset, model-result, deferred human-validation, and release facts"
    if "contribution" in haystack:
        return "exact artifact-backed contribution counts and release links"
    if "item card" in haystack or "papersplit" in haystack:
        return "manifest-scoped item-card readiness evidence"
    if "human" in haystack or "baseline" in haystack:
        return "deferred or audited human-validation evidence"
    if "discussion" in haystack or "observed model" in haystack:
        return "final result patterns reviewed against limitations"
    return "final paper-sweep comparison artifacts"


def _next_action(
    status: str,
    dependencies: tuple[str, ...],
    placeholder_count: int,
    relative: Path,
) -> str:
    if dependencies:
        return "Resolve: " + "; ".join(dependencies) + "."
    if placeholder_count:
        return "Replace placeholder wording after the referenced generated asset is real."
    if relative.name == "02_related_work.tex":
        return "Keep comparator coverage current before final submission."
    return "Final copyedit after evidence-backed sections are complete."


def _word_count(text: str) -> int:
    stripped = re.sub(r"\\[A-Za-z]+(?:\[[^\]]*\])?(?:\{[^}]*\})?", " ", text)
    return len(WORD_RE.findall(stripped))


def _draft_placeholder_count(text: str) -> int:
    return sum(
        1
        for line in text.lower().splitlines()
        if any(pattern in line for pattern in DRAFT_PLACEHOLDER_PATTERNS)
    )


def _section_titles(text: str) -> list[str]:
    titles: list[str] = []
    for line in text.splitlines():
        if "\\section{" not in line:
            continue
        raw_title = _extract_braced_argument(line, "\\section")
        if raw_title:
            titles.append(_clean_title(raw_title))
    return titles


def _extract_braced_argument(line: str, command: str) -> str | None:
    command_index = line.find(command)
    if command_index < 0:
        return None
    open_index = line.find("{", command_index + len(command))
    if open_index < 0:
        return None
    depth = 0
    chars = []
    for char in line[open_index:]:
        if char == "{":
            if depth:
                chars.append(char)
            depth += 1
            continue
        if char == "}":
            depth -= 1
            if depth == 0:
                return "".join(chars)
            chars.append(char)
            continue
        if depth:
            chars.append(char)
    return None


def _clean_title(title: str) -> str:
    cleaned = title.replace("\\benchmarkname{}", "ObviousBench")
    cleaned = cleaned.replace("\\paperSplit{}", "paper_v1")
    cleaned = re.sub(r"\\[A-Za-z]+\{\}", "", cleaned)
    cleaned = re.sub(r"\\[A-Za-z]+", "", cleaned)
    cleaned = cleaned.replace("{", "").replace("}", "")
    return " ".join(cleaned.split())


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _render_markdown(
    result: ReportSectionTrackerResult,
    inputs: ReportSectionTrackerInputs,
) -> str:
    lines = [
        "---",
        "title: ObviousBench Report Section Tracker",
        f"date: {inputs.generated_on}",
        "type: research",
        f"status: {'blocked' if result.blocked_count else 'draft'}",
        "---",
        "",
        "# ObviousBench Report Section Tracker",
        "",
        "This tracker summarizes the LaTeX manuscript section by section. It",
        "is not a replacement for the claim-blocker audit; it is an editorial",
        "dashboard for moving the report from scaffold to evidence-backed",
        "arXiv article without losing state across context compaction.",
        "",
        f"Overall status: {'BLOCKED' if result.blocked_count else 'DRAFT-CLEAN'}",
        "",
        f"Sections tracked: {len(result.entries)}",
        f"Blocked sections: {result.blocked_count}",
        f"Unresolved markers: {result.unresolved_marker_count}",
        f"Placeholder mentions: {result.placeholder_count}",
        "",
        "## Section Matrix",
        "",
        (
            "| Section | Source | Status | Words | Tables | Figures | Citations | "
            "Markers | Role | Next action |"
        ),
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for entry in result.entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(entry.title),
                    _cell(f"`{entry.path}`"),
                    _cell(entry.status),
                    str(entry.word_count),
                    str(len(entry.table_inputs)),
                    str(len(entry.figures)),
                    str(entry.citation_count),
                    str(entry.marker_count),
                    _cell(entry.role),
                    _cell(entry.next_action),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Unresolved Evidence Dependencies", ""])
    blocked = [entry for entry in result.entries if entry.dependencies]
    if not blocked:
        lines.extend(["No unresolved evidence dependencies were found.", ""])
        return "\n".join(lines)
    lines.extend(
        [
            "| Source | Section | Dependencies |",
            "| --- | --- | --- |",
        ]
    )
    for entry in blocked:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(f"`{entry.path}`"),
                    _cell(entry.title),
                    _cell("; ".join(entry.dependencies)),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
