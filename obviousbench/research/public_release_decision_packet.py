"""Build a decision packet for ObviousBench public-release metadata."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml

DecisionStatus = Literal["ready", "needs-confirmation"]

PLACEHOLDER_MARKERS = ("TODO", "TBD", "<", ">", "claimblocked", "obtodo")


@dataclass(frozen=True)
class PublicReleaseDecisionPacketInputs:
    root_dir: Path
    output_path: Path
    metadata_path: Path
    release_audit_path: Path
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class ReleaseDecision:
    name: str
    status: DecisionStatus
    target_artifact: str
    current_state: str
    next_action: str


@dataclass(frozen=True)
class PublicReleaseDecisionPacketResult:
    output_path: Path
    decisions: tuple[ReleaseDecision, ...]

    @property
    def ok(self) -> bool:
        return self.needs_confirmation_count == 0

    @property
    def ready_count(self) -> int:
        return sum(decision.status == "ready" for decision in self.decisions)

    @property
    def needs_confirmation_count(self) -> int:
        return sum(decision.status == "needs-confirmation" for decision in self.decisions)

    def decision_by_name(self, name: str) -> ReleaseDecision:
        for decision in self.decisions:
            if decision.name == name:
                return decision
        raise KeyError(name)


def build_public_release_decision_packet(
    inputs: PublicReleaseDecisionPacketInputs,
) -> PublicReleaseDecisionPacketResult:
    """Write a release-decision packet without creating final release files."""
    metadata, metadata_issue = _load_frontmatter(inputs.metadata_path)
    decisions = (
        _license_decision(inputs.root_dir, metadata, metadata_issue),
        _citation_decision(inputs.root_dir),
        _archive_metadata_decision(inputs.root_dir),
        _package_license_decision(inputs.root_dir),
        _public_urls_decision(metadata, metadata_issue),
        _submitter_decision(metadata, metadata_issue),
    )
    result = PublicReleaseDecisionPacketResult(
        output_path=inputs.output_path,
        decisions=decisions,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _license_decision(
    root: Path,
    metadata: dict[str, Any],
    metadata_issue: str | None,
) -> ReleaseDecision:
    license_file = root / "LICENSE"
    metadata_license = metadata.get("license") if metadata_issue is None else None
    license_ready = license_file.is_file() and _is_non_placeholder_text(metadata_license)
    return ReleaseDecision(
        name="license selection",
        status="ready" if license_ready else "needs-confirmation",
        target_artifact="LICENSE and arXiv metadata `license`",
        current_state=(
            f"LICENSE present: {'yes' if license_file.is_file() else 'no'}; "
            f"metadata license: {_display(metadata_license)}"
        ),
        next_action=(
            "Confirm the code/data/paper license before creating `LICENSE` and "
            "before changing arXiv metadata to confirmed."
            if not license_ready
            else "None."
        ),
    )


def _citation_decision(root: Path) -> ReleaseDecision:
    path = root / "CITATION.cff"
    ready = path.is_file() and "TODO" not in path.read_text(encoding="utf-8")
    return ReleaseDecision(
        name="citation metadata",
        status="ready" if ready else "needs-confirmation",
        target_artifact="CITATION.cff",
        current_state=f"CITATION.cff present and de-placeholdered: {'yes' if ready else 'no'}",
        next_action=(
            "Confirm author names, ORCIDs if available, title, version, release "
            "date, repository URL, and preferred citation text."
            if not ready
            else "None."
        ),
    )


def _archive_metadata_decision(root: Path) -> ReleaseDecision:
    path = root / ".zenodo.json"
    ready = path.is_file() and "TODO" not in path.read_text(encoding="utf-8")
    return ReleaseDecision(
        name="archive metadata",
        status="ready" if ready else "needs-confirmation",
        target_artifact=".zenodo.json",
        current_state=f".zenodo.json present and de-placeholdered: {'yes' if ready else 'no'}",
        next_action=(
            "Confirm creators, title, description, keywords, license, related "
            "identifiers, and upload type before archiving."
            if not ready
            else "None."
        ),
    )


def _package_license_decision(root: Path) -> ReleaseDecision:
    path = root / "pyproject.toml"
    license_value = None
    classifier = False
    if path.exists():
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
        project = payload.get("project", {})
        license_value = project.get("license")
        classifiers = project.get("classifiers") or []
        classifier = any(
            isinstance(value, str) and value.startswith("License ::")
            for value in classifiers
        )
    ready = bool(license_value or classifier)
    return ReleaseDecision(
        name="package license metadata",
        status="ready" if ready else "needs-confirmation",
        target_artifact="pyproject.toml",
        current_state=(
            f"project.license: {_display(license_value)}; "
            f"license classifier present: {'yes' if classifier else 'no'}"
        ),
        next_action=(
            "Set package license metadata only after the release license decision is final."
            if not ready
            else "None."
        ),
    )


def _public_urls_decision(
    metadata: dict[str, Any],
    metadata_issue: str | None,
) -> ReleaseDecision:
    repository_url = metadata.get("repository_url") if metadata_issue is None else None
    dataset_url = metadata.get("dataset_url") if metadata_issue is None else None
    ready = _is_non_placeholder_text(repository_url) and _is_non_placeholder_text(dataset_url)
    return ReleaseDecision(
        name="public repository and artifact URLs",
        status="ready" if ready else "needs-confirmation",
        target_artifact="arXiv metadata `repository_url` and `dataset_url`",
        current_state=(
            f"repository_url: {_display(repository_url)}; "
            f"dataset_url: {_display(dataset_url)}"
        ),
        next_action=(
            "Confirm the public repository URL and immutable-enough data/artifact URL "
            "before final arXiv metadata confirmation."
            if not ready
            else "None."
        ),
    )


def _submitter_decision(
    metadata: dict[str, Any],
    metadata_issue: str | None,
) -> ReleaseDecision:
    fields = (
        "submitter_registered_author",
        "endorsement_checked",
        "submitter_is_author_or_authorized_proxy",
        "title_and_abstract_checked",
    )
    false_fields = (
        list(fields)
        if metadata_issue is not None
        else [field for field in fields if metadata.get(field) is not True]
    )
    ready = (
        metadata_issue is None
        and not false_fields
        and metadata.get("metadata_status") == "confirmed"
    )
    return ReleaseDecision(
        name="submitter and final metadata confirmation",
        status="ready" if ready else "needs-confirmation",
        target_artifact="arXiv metadata confirmation fields",
        current_state=(
            "false or unconfirmed fields: "
            + (", ".join(false_fields) if false_fields else "none")
            + f"; metadata_status: {_display(metadata.get('metadata_status'))}"
        ),
        next_action=(
            "Confirm submitter account, endorsement status, title/abstract match, "
            "and metadata status after the final PDF is inspected."
            if not ready
            else "None."
        ),
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


def _display(value: object) -> str:
    if value is None:
        return "missing"
    if isinstance(value, str):
        return value
    return str(value)


def _render_markdown(
    result: PublicReleaseDecisionPacketResult,
    inputs: PublicReleaseDecisionPacketInputs,
) -> str:
    lines = [
        "---",
        "title: ObviousBench Public Release Decision Packet",
        f"date: {inputs.generated_on}",
        "type: decision-record",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Public Release Decision Packet",
        "",
        "This packet turns the release-side arXiv blockers into explicit",
        "human decisions and draft file templates. It does not create a",
        "`LICENSE`, `CITATION.cff`, `.zenodo.json`, publish a repository,",
        "choose a license, or confirm arXiv metadata.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        (
            "Summary: "
            f"{result.ready_count} ready, "
            f"{result.needs_confirmation_count} need confirmation."
        ),
        "",
        "## Decision Matrix",
        "",
        "| Decision | Status | Target artifact | Current state | Next action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for decision in result.decisions:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(decision.name),
                    decision.status.upper(),
                    _cell(decision.target_artifact),
                    _cell(decision.current_state),
                    _cell(decision.next_action),
                ]
            )
            + " |"
        )
    lines.extend(_template_lines())
    return "\n".join(lines)


def _template_lines() -> list[str]:
    return [
        "",
        "## Draft File Templates",
        "",
        "These are templates to apply only after the release decision is made.",
        "Leave the hard public-release audit blocked until the real files are",
        "filled with confirmed values.",
        "",
        "### CITATION.cff",
        "",
        "```yaml",
        "cff-version: 1.2.0",
        "message: \"If you use ObviousBench, please cite the archived release.\"",
        "title: \"ObviousBench: Measuring Human-Trivial Failure Modes in "
        "Public-Facing Language Models\"",
        "version: \"0.1.0\"",
        "date-released: \"2026-06-01\"",
        "authors:",
        "  - family-names: \"TODO\"",
        "    given-names: \"TODO\"",
        "repository-code: \"TODO(confirm public repository URL)\"",
        "url: \"TODO(confirm project or release URL)\"",
        "license: \"TODO(confirm license)\"",
        "```",
        "",
        "### .zenodo.json",
        "",
        "```json",
        "{",
        "  \"title\": \"ObviousBench: Measuring Human-Trivial Failure Modes in "
        "Public-Facing Language Models\",",
        "  \"upload_type\": \"software\",",
        "  \"description\": \"TODO(confirm release description after final "
        "paper artifacts are frozen)\",",
        "  \"creators\": [",
        "    {\"name\": \"TODO\", \"affiliation\": \"TODO\"}",
        "  ],",
        "  \"license\": \"TODO\",",
        "  \"keywords\": [\"language-model-evaluation\", \"benchmark\", \"reliability\"],",
        "  \"related_identifiers\": []",
        "}",
        "```",
        "",
        "### pyproject.toml",
        "",
        "```toml",
        "# Add after license is confirmed.",
        "license = \"TODO\"",
        "classifiers = [",
        "  \"License :: OSI Approved :: TODO\",",
        "]",
        "```",
        "",
    ]


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
