"""Build and audit arXiv submission metadata notes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REQUIRED_TEXT_FIELDS = (
    "article_title",
    "abstract",
    "primary_category",
    "license",
    "comments",
    "repository_url",
    "dataset_url",
    "ai_tool_disclosure",
)
REQUIRED_BOOLEAN_FIELDS = (
    "submitter_registered_author",
    "endorsement_checked",
    "submitter_is_author_or_authorized_proxy",
    "title_and_abstract_checked",
)
PLACEHOLDER_MARKERS = (
    "TODO",
    "TBD",
    "claimblocked",
    "obtodo",
    "<",
    ">",
)


@dataclass(frozen=True)
class ArxivMetadataInputs:
    output_path: Path
    article_title: str = (
        "ObviousBench: Measuring Human-Trivial Failure Modes in "
        "Public-Facing Language Models"
    )
    primary_category: str = "cs.CL"
    secondary_categories: tuple[str, ...] = ("cs.AI",)


@dataclass(frozen=True)
class ArxivMetadataTemplateResult:
    output_path: Path


@dataclass(frozen=True)
class ArxivMetadataAuditResult:
    path: Path
    issues: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.issues


def build_submission_metadata_template(
    inputs: ArxivMetadataInputs,
) -> ArxivMetadataTemplateResult:
    """Write a draft arXiv metadata note that must be confirmed before upload."""
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_template(inputs), encoding="utf-8")
    return ArxivMetadataTemplateResult(output_path=inputs.output_path)


def audit_submission_metadata(path: Path | None) -> ArxivMetadataAuditResult:
    if path is None:
        return ArxivMetadataAuditResult(
            path=Path(""),
            issues=("metadata confirmation path is not configured",),
        )
    if not path.exists():
        return ArxivMetadataAuditResult(
            path=path,
            issues=(f"metadata file is missing: {path}",),
        )
    if path.stat().st_size == 0:
        return ArxivMetadataAuditResult(
            path=path,
            issues=(f"metadata file is empty: {path}",),
        )

    frontmatter, parse_issue = _load_frontmatter(path)
    issues: list[str] = []
    if parse_issue is not None:
        issues.append(parse_issue)
        return ArxivMetadataAuditResult(path=path, issues=tuple(issues))

    if frontmatter.get("metadata_status") != "confirmed":
        issues.append("metadata_status must be confirmed")
    if frontmatter.get("status") != "confirmed":
        issues.append("status must be confirmed")

    authors = frontmatter.get("authors")
    if not isinstance(authors, list) or not authors:
        issues.append("authors must be a non-empty list")
    else:
        for index, author in enumerate(authors, start=1):
            if not _is_non_placeholder_text(author):
                issues.append(f"authors[{index}] is empty or placeholder text")

    secondary_categories = frontmatter.get("secondary_categories")
    if secondary_categories is not None and not isinstance(secondary_categories, list):
        issues.append("secondary_categories must be a list when present")

    for field in REQUIRED_TEXT_FIELDS:
        value = frontmatter.get(field)
        if not _is_non_placeholder_text(value):
            issues.append(f"{field} is missing, empty, or TODO placeholder text")

    for field in REQUIRED_BOOLEAN_FIELDS:
        if frontmatter.get(field) is not True:
            issues.append(f"{field} must be true")

    return ArxivMetadataAuditResult(path=path, issues=tuple(issues))


def _render_template(inputs: ArxivMetadataInputs) -> str:
    secondary_lines = "\n".join(
        f'  - "{category}"' for category in inputs.secondary_categories
    )
    return f"""---
title: ObviousBench arXiv Submission Metadata
date: 2026-06-01
type: review
status: draft
metadata_status: draft
article_title: "{inputs.article_title}"
authors:
  - "TODO(confirm author list, order, affiliations, and contact email)"
abstract: "TODO(replace after readiness gates pass and final results are frozen)"
primary_category: "{inputs.primary_category}"
secondary_categories:
{secondary_lines}
license: "TODO(confirm arXiv license selection)"
comments: "TODO(confirm final page count, figures, tables, and release links)"
repository_url: "TODO(confirm public repository URL)"
dataset_url: "TODO(confirm public data or artifact URL)"
ai_tool_disclosure: "TODO(confirm disclosure text for author workflow)"
submitter_registered_author: false
endorsement_checked: false
submitter_is_author_or_authorized_proxy: false
title_and_abstract_checked: false
---

# ObviousBench arXiv Submission Metadata

This note is the human-confirmed metadata handoff for the arXiv upload form.
It intentionally starts as `draft`; the submission preflight should not pass
until `status` and `metadata_status` are changed to `confirmed`, placeholders
are removed, and all boolean confirmation fields are true.

Official arXiv references checked for this template:

- https://info.arxiv.org/help/submit/index.html
- https://info.arxiv.org/help/prep.html
- https://info.arxiv.org/help/license/index.html
- https://arxiv.org/category_taxonomy

Submission-specific decisions still required:

- Confirm whether the primary category should remain `cs.CL` or move to
  another Computer Science category.
- Confirm any secondary categories.
- Confirm the author list, author order, affiliations, and submitter account.
- Confirm whether an endorsement is needed for the selected category.
- Confirm the license selection.
- Confirm public repository and data release links.
- Confirm final title and abstract exactly match the reviewed manuscript.
"""


def _load_frontmatter(path: Path) -> tuple[dict[str, Any], str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, "metadata file is missing YAML frontmatter"
    try:
        _, raw_frontmatter, _ = text.split("---", 2)
    except ValueError:
        return {}, "metadata file has malformed YAML frontmatter"
    try:
        loaded = yaml.safe_load(raw_frontmatter) or {}
    except yaml.YAMLError as exc:
        return {}, f"metadata YAML could not be parsed: {exc}"
    if not isinstance(loaded, dict):
        return {}, "metadata frontmatter must be a mapping"
    return loaded, None


def _is_non_placeholder_text(value: object) -> bool:
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if not stripped:
        return False
    lowered = stripped.lower()
    return not any(marker.lower() in lowered for marker in PLACEHOLDER_MARKERS)
