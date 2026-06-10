"""Audit public release artifacts needed for the ObviousBench arXiv paper."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml

ReleaseStatus = Literal["pass", "fail"]

REQUIRED_PUBLIC_DOCS = (
    "README.md",
    "docs/benchmark_card.md",
    "docs/methodology.md",
    "docs/scoring_policy.md",
    "docs/source_policy.md",
    "docs/prompt_policy.md",
    "paper/README.md",
)
REQUIRED_RELEASE_DATA = (
    "data/splits/paper_v1_manifest.jsonl",
    "data/barrages/hard_obvious_8x10_seed_20260531.jsonl",
    "data/item_cards/public_v0/cards.yaml",
    "configs/paper_v1_model_panel.yaml",
    "configs/paper_v1_final_sweep_manifest.csv",
)
REQUIRED_CITATION_FILES = ("LICENSE", "CITATION.cff", ".zenodo.json")
REQUIRED_METADATA_URL_FIELDS = ("repository_url", "dataset_url")
PLACEHOLDER_MARKERS = ("TODO", "TBD", "<", ">", "claimblocked", "obtodo")


@dataclass(frozen=True)
class PublicReleaseAuditInputs:
    root_dir: Path
    output_path: Path
    metadata_path: Path
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class ReleaseCheck:
    name: str
    status: ReleaseStatus
    evidence: str
    next_action: str


@dataclass(frozen=True)
class PublicReleaseAuditResult:
    output_path: Path
    checks: tuple[ReleaseCheck, ...]

    @property
    def ok(self) -> bool:
        return all(check.status == "pass" for check in self.checks)

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    @property
    def failed_count(self) -> int:
        return sum(check.status == "fail" for check in self.checks)

    def check_by_name(self, name: str) -> ReleaseCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


def audit_public_release_artifacts(
    inputs: PublicReleaseAuditInputs,
) -> PublicReleaseAuditResult:
    """Write a release-readiness audit without publishing anything."""
    root = inputs.root_dir
    checks = (
        _required_paths_check(
            "public documentation",
            root,
            REQUIRED_PUBLIC_DOCS,
            "Keep public-facing benchmark docs present and current.",
        ),
        _required_paths_check(
            "paper release data",
            root,
            REQUIRED_RELEASE_DATA,
            "Preserve frozen paper split, item-card, barrage, and model-panel artifacts.",
        ),
        _license_and_citation_check(root),
        _pyproject_license_check(root / "pyproject.toml"),
        _metadata_urls_check(inputs.metadata_path),
        _metadata_confirmation_check(inputs.metadata_path),
    )
    result = PublicReleaseAuditResult(output_path=inputs.output_path, checks=checks)
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _required_paths_check(
    name: str,
    root: Path,
    relative_paths: tuple[str, ...],
    pass_action: str,
) -> ReleaseCheck:
    missing = [path for path in relative_paths if not (root / path).is_file()]
    if not missing:
        return ReleaseCheck(
            name=name,
            status="pass",
            evidence=f"{len(relative_paths)}/{len(relative_paths)} required file(s) present.",
            next_action="None.",
        )
    return ReleaseCheck(
        name=name,
        status="fail",
        evidence=(
            f"{len(relative_paths) - len(missing)}/{len(relative_paths)} present; "
            "missing: " + ", ".join(missing)
        ),
        next_action=pass_action,
    )


def _license_and_citation_check(root: Path) -> ReleaseCheck:
    missing = [path for path in REQUIRED_CITATION_FILES if not (root / path).is_file()]
    if not missing:
        return ReleaseCheck(
            name="license and citation files",
            status="pass",
            evidence="LICENSE, CITATION.cff, and .zenodo.json are present.",
            next_action="None.",
        )
    return ReleaseCheck(
        name="license and citation files",
        status="fail",
        evidence="missing: " + ", ".join(missing),
        next_action=(
            "Confirm license, author metadata, and archival metadata before public release."
        ),
    )


def _pyproject_license_check(path: Path) -> ReleaseCheck:
    if not path.exists():
        return ReleaseCheck(
            name="pyproject license metadata",
            status="fail",
            evidence=f"missing: {path}",
            next_action="Add project metadata before publishing package artifacts.",
        )
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    project = payload.get("project", {})
    license_value = project.get("license")
    classifiers = project.get("classifiers") or []
    has_license_classifier = any(
        isinstance(value, str) and value.startswith("License ::") for value in classifiers
    )
    if license_value or has_license_classifier:
        return ReleaseCheck(
            name="pyproject license metadata",
            status="pass",
            evidence="project license metadata is present.",
            next_action="None.",
        )
    return ReleaseCheck(
        name="pyproject license metadata",
        status="fail",
        evidence="project.license/classifier is not configured.",
        next_action="Set package license metadata after the release license is confirmed.",
    )


def _metadata_urls_check(path: Path) -> ReleaseCheck:
    metadata, issue = _load_frontmatter(path)
    if issue:
        return ReleaseCheck(
            name="public release URLs",
            status="fail",
            evidence=issue,
            next_action="Fix metadata frontmatter before confirming release URLs.",
        )
    missing = [
        field
        for field in REQUIRED_METADATA_URL_FIELDS
        if not _is_non_placeholder_text(metadata.get(field))
    ]
    if not missing:
        return ReleaseCheck(
            name="public release URLs",
            status="pass",
            evidence="repository_url and dataset_url are confirmed.",
            next_action="None.",
        )
    return ReleaseCheck(
        name="public release URLs",
        status="fail",
        evidence="missing or placeholder field(s): " + ", ".join(missing),
        next_action="Confirm public repository and dataset/artifact URLs.",
    )


def _metadata_confirmation_check(path: Path) -> ReleaseCheck:
    metadata, issue = _load_frontmatter(path)
    if issue:
        return ReleaseCheck(
            name="release metadata confirmation",
            status="fail",
            evidence=issue,
            next_action="Fix metadata frontmatter before final submission.",
        )
    required_true = (
        "submitter_registered_author",
        "endorsement_checked",
        "submitter_is_author_or_authorized_proxy",
        "title_and_abstract_checked",
    )
    false_fields = [field for field in required_true if metadata.get(field) is not True]
    if metadata.get("metadata_status") == "confirmed" and not false_fields:
        return ReleaseCheck(
            name="release metadata confirmation",
            status="pass",
            evidence="metadata_status is confirmed and release boolean checks are true.",
            next_action="None.",
        )
    evidence_parts = []
    if metadata.get("metadata_status") != "confirmed":
        evidence_parts.append("metadata_status is not confirmed")
    if false_fields:
        evidence_parts.append("false fields: " + ", ".join(false_fields))
    return ReleaseCheck(
        name="release metadata confirmation",
        status="fail",
        evidence="; ".join(evidence_parts),
        next_action="Confirm submitter, endorsement, title/abstract, and metadata status.",
    )


def _load_frontmatter(path: Path) -> tuple[dict[str, Any], str | None]:
    if not path.exists():
        return {}, f"metadata file missing: {path}"
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, "metadata file is missing YAML frontmatter"
    try:
        _, raw_frontmatter, _ = text.split("---", 2)
    except ValueError:
        return {}, "metadata file has malformed YAML frontmatter"
    loaded = yaml.safe_load(raw_frontmatter) or {}
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


def _render_markdown(
    result: PublicReleaseAuditResult,
    inputs: PublicReleaseAuditInputs,
) -> str:
    lines = [
        "---",
        "title: ObviousBench Public Release Artifact Audit",
        f"date: {inputs.generated_on}",
        "type: review",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Public Release Artifact Audit",
        "",
        "This audit checks the release-side artifacts needed before the arXiv",
        "metadata can contain final public code and data links. It does not",
        "publish a repository, choose a license, or upload data archives.",
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
            "## Final Release Rule",
            "",
            "Do not mark the arXiv metadata note as confirmed until this audit",
            "passes, the repository and dataset/artifact URLs are public, and the",
            "license and citation files match the final release decision.",
            "",
        ]
    )
    return "\n".join(lines)


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
