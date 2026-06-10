"""Audit arXiv source bundles before upload."""

from __future__ import annotations

import tarfile
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN_PATH_PARTS = (
    "results/raw",
    "results/summaries",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".DS_Store",
)
FORBIDDEN_NAME_PARTS = (
    "api_key",
    "apikey",
    "password",
    "secret",
    "credential",
)
REQUIRED_MEMBERS = ("main.tex", "references.bib")
REQUIRED_PREFIXES = ("sections/",)


@dataclass(frozen=True)
class ArxivBundleAuditInputs:
    bundle_path: Path
    output_path: Path


@dataclass(frozen=True)
class ArxivBundleAuditResult:
    output_path: Path
    members: tuple[str, ...]
    issues: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.issues

    @property
    def issue_count(self) -> int:
        return len(self.issues)


def audit_arxiv_source_bundle(
    inputs: ArxivBundleAuditInputs,
) -> ArxivBundleAuditResult:
    members, issues = _inspect_bundle(inputs.bundle_path)
    result = ArxivBundleAuditResult(
        output_path=inputs.output_path,
        members=members,
        issues=tuple(issues),
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result), encoding="utf-8")
    return result


def _inspect_bundle(bundle_path: Path) -> tuple[tuple[str, ...], list[str]]:
    if not bundle_path.exists():
        return (), [f"missing bundle: {bundle_path}"]
    issues: list[str] = []
    try:
        with tarfile.open(bundle_path, "r:gz") as archive:
            members = tuple(sorted(member.name for member in archive.getmembers()))
    except tarfile.TarError as exc:
        return (), [f"invalid tar.gz bundle: {exc}"]

    member_set = set(members)
    for required in REQUIRED_MEMBERS:
        if required not in member_set:
            issues.append(f"missing required member: {required}")
    for prefix in REQUIRED_PREFIXES:
        if not any(member.startswith(prefix) for member in members):
            issues.append(f"missing required prefix: {prefix}")
    for member in members:
        lowered = member.lower()
        if any(part in lowered for part in FORBIDDEN_PATH_PARTS):
            issues.append(f"forbidden path in bundle: {member}")
        if any(part in lowered for part in FORBIDDEN_NAME_PARTS):
            issues.append(f"sensitive-looking filename in bundle: {member}")
    return members, issues


def _render_markdown(result: ArxivBundleAuditResult) -> str:
    lines = [
        "---",
        "title: arXiv Source Bundle Audit",
        "date: 2026-06-01",
        "type: review",
        "status: current",
        "---",
        "",
        "# arXiv Source Bundle Audit",
        "",
        f"Overall status: {'PASS' if result.ok else 'FAIL'}",
        "",
        f"Members: {len(result.members)}",
        "",
        f"Issues: {result.issue_count}",
        "",
    ]
    if result.issues:
        lines.extend(["## Issues", ""])
        lines.extend(f"- {issue}" for issue in result.issues)
        lines.append("")
    return "\n".join(lines)
