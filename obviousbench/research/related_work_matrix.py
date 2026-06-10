"""Generate a related-work positioning matrix for the ObviousBench paper."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml

CoverageStatus = Literal["pass", "blocked"]

BIB_KEY_RE = re.compile(r"@\w+\{([^,\s]+)")
CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\{([^}]+)\}")


@dataclass(frozen=True)
class RelatedWorkMatrixInputs:
    config_path: Path
    paper_dir: Path
    bib_path: Path
    markdown_path: Path
    tex_path: Path
    generated_on: str = "2026-06-01"
    related_work_path: str = "sections/02_related_work.tex"


@dataclass(frozen=True)
class RelatedWorkEntry:
    id: str
    citation_key: str
    title: str
    year: int
    source_url: str
    cluster: str
    comparator_role: str
    evidence_standard: str
    obviousbench_stance: str
    manuscript_use: str
    required: bool
    bib_present: bool
    cited_in_related_work: bool

    @property
    def status(self) -> CoverageStatus:
        if self.required and (not self.bib_present or not self.cited_in_related_work):
            return "blocked"
        return "pass"


@dataclass(frozen=True)
class RelatedWorkMatrixResult:
    markdown_path: Path
    tex_path: Path
    entries: tuple[RelatedWorkEntry, ...]

    @property
    def ok(self) -> bool:
        return self.blocked_count == 0

    @property
    def blocked_count(self) -> int:
        return sum(entry.status == "blocked" for entry in self.entries)

    @property
    def passed_count(self) -> int:
        return sum(entry.status == "pass" for entry in self.entries)

    @property
    def required_count(self) -> int:
        return sum(entry.required for entry in self.entries)

    def entry_by_id(self, entry_id: str) -> RelatedWorkEntry:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        raise KeyError(entry_id)


def build_related_work_matrix(
    inputs: RelatedWorkMatrixInputs,
) -> RelatedWorkMatrixResult:
    """Write Markdown and LaTeX related-work positioning artifacts."""
    config = yaml.safe_load(inputs.config_path.read_text(encoding="utf-8")) or {}
    bib_keys = _bib_keys(inputs.bib_path)
    cited_keys = _cited_keys(inputs.paper_dir / inputs.related_work_path)
    entries = tuple(
        _entry_from_config(entry, bib_keys=bib_keys, cited_keys=cited_keys)
        for entry in config.get("entries", ())
    )
    result = RelatedWorkMatrixResult(
        markdown_path=inputs.markdown_path,
        tex_path=inputs.tex_path,
        entries=entries,
    )
    inputs.markdown_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.tex_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.markdown_path.write_text(
        _render_markdown(result, inputs, config),
        encoding="utf-8",
    )
    inputs.tex_path.write_text(_render_tex(result), encoding="utf-8")
    return result


def _entry_from_config(
    entry: dict[str, Any],
    *,
    bib_keys: set[str],
    cited_keys: set[str],
) -> RelatedWorkEntry:
    citation_key = str(entry["citation_key"])
    return RelatedWorkEntry(
        id=str(entry["id"]),
        citation_key=citation_key,
        title=str(entry["title"]),
        year=int(entry["year"]),
        source_url=str(entry["source_url"]),
        cluster=str(entry["cluster"]),
        comparator_role=str(entry["comparator_role"]),
        evidence_standard=str(entry["evidence_standard"]),
        obviousbench_stance=str(entry["obviousbench_stance"]),
        manuscript_use=str(entry["manuscript_use"]),
        required=bool(entry.get("required", True)),
        bib_present=citation_key in bib_keys,
        cited_in_related_work=citation_key in cited_keys,
    )


def _bib_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return set(BIB_KEY_RE.findall(path.read_text(encoding="utf-8")))


def _cited_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    keys: set[str] = set()
    for match in CITE_RE.findall(text):
        keys.update(key.strip() for key in match.split(",") if key.strip())
    return keys


def _render_markdown(
    result: RelatedWorkMatrixResult,
    inputs: RelatedWorkMatrixInputs,
    config: dict[str, Any],
) -> str:
    lines = [
        "---",
        "title: ObviousBench Related Work Positioning Matrix",
        f"date: {inputs.generated_on}",
        "type: research",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Related Work Positioning Matrix",
        "",
        "This matrix tracks nearby benchmark papers and the evidence standard",
        "each one contributes to the ObviousBench arXiv manuscript. It does not",
        "make result claims or run model providers.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"Summary: {result.passed_count} passed, {result.blocked_count} blocked.",
        "",
        f"Required comparators: {result.required_count}",
        "",
        "Selection policy:",
    ]
    for rule in (config.get("selection_policy") or {}).get("rules", ()):
        lines.append(f"- {rule}")
    lines.extend(
        [
            "",
            "## Positioning Matrix",
            "",
            (
                "| Comparator | Cluster | Role | Evidence standard to borrow | "
                "ObviousBench stance | Coverage |"
            ),
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for entry in result.entries:
        coverage = []
        coverage.append("bib" if entry.bib_present else "missing bib")
        coverage.append("cited" if entry.cited_in_related_work else "missing cite")
        lines.append(
            "| "
            + " | ".join(
                [
                    _md_cell(
                        f"[{entry.title} ({entry.year})]({entry.source_url}) "
                        f"`{entry.citation_key}`"
                    ),
                    _md_cell(entry.cluster),
                    _md_cell(entry.comparator_role),
                    _md_cell(entry.evidence_standard),
                    _md_cell(entry.obviousbench_stance),
                    _md_cell(f"{entry.status.upper()}: {', '.join(coverage)}"),
                ]
            )
            + " |"
        )
    blocked = [entry for entry in result.entries if entry.status == "blocked"]
    if blocked:
        lines.extend(["", "## Blocking Coverage Issues", ""])
        for entry in blocked:
            issues = []
            if not entry.bib_present:
                issues.append(f"add `{entry.citation_key}` to `paper/references.bib`")
            if not entry.cited_in_related_work:
                issues.append(
                    f"cite `{entry.citation_key}` in `paper/{inputs.related_work_path}`"
                )
            lines.append(f"- {entry.title}: {'; '.join(issues)}.")
    lines.extend(
        [
            "",
            "## Manuscript Use",
            "",
            "| Comparator | Manuscript use |",
            "| --- | --- |",
        ]
    )
    for entry in result.entries:
        lines.append(
            f"| {_md_cell(entry.title)} | {_md_cell(entry.manuscript_use)} |"
        )
    lines.append("")
    return "\n".join(lines)


def _render_tex(result: RelatedWorkMatrixResult) -> str:
    lines = [
        "% Generated by scripts/build_related_work_matrix.py; do not edit by hand.",
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{p{0.18\\linewidth}p{0.28\\linewidth}p{0.44\\linewidth}}",
        "\\toprule",
        "Comparator & Evidence standard & ObviousBench positioning \\\\",
        "\\midrule",
    ]
    for entry in result.entries:
        comparator = f"{_tex(entry.title)}~\\citep{{{entry.citation_key}}}"
        lines.append(
            f"{comparator} & {_tex(entry.evidence_standard)} & "
            f"{_tex(entry.obviousbench_stance)} \\\\"
        )
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Related-work positioning matrix for nearby benchmark reports.}",
            "\\label{tab:related-work-positioning}",
            "\\end{table*}",
            "",
        ]
    )
    return "\n".join(lines)


def _md_cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")


def _tex(value: str) -> str:
    replacements = {
        "\\": "\\textbackslash{}",
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
        "{": "\\{",
        "}": "\\}",
        "~": "\\textasciitilde{}",
        "^": "\\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)
