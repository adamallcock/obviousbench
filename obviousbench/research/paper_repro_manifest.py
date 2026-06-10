"""Build a reproducibility manifest for the ObviousBench paper workspace."""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReproArtifactSpec:
    path: str
    category: str
    required: bool = True


@dataclass(frozen=True)
class ReproCommandSpec:
    command: str
    purpose: str
    expected_status: str


@dataclass(frozen=True)
class GitState:
    head: str | None
    dirty: bool | None
    status_summary: str


@dataclass(frozen=True)
class ReproArtifact:
    path: str
    category: str
    required: bool
    exists: bool
    size_bytes: int | None
    sha256: str | None


@dataclass(frozen=True)
class PaperReproManifestInputs:
    root_dir: Path
    output_path: Path
    artifact_specs: tuple[ReproArtifactSpec, ...] = ()
    command_specs: tuple[ReproCommandSpec, ...] = ()
    generated_on: str = "2026-06-01"
    include_git_state: bool = True
    git_state: GitState | None = None


@dataclass(frozen=True)
class PaperReproManifestResult:
    output_path: Path
    artifacts: tuple[ReproArtifact, ...]
    commands: tuple[ReproCommandSpec, ...]
    git_state: GitState | None

    @property
    def ok(self) -> bool:
        return self.missing_required_count == 0

    @property
    def missing_required_count(self) -> int:
        return sum(
            artifact.required and not artifact.exists for artifact in self.artifacts
        )

    @property
    def required_count(self) -> int:
        return sum(artifact.required for artifact in self.artifacts)

    @property
    def present_required_count(self) -> int:
        return sum(artifact.required and artifact.exists for artifact in self.artifacts)

    def artifact_by_path(self, path: str) -> ReproArtifact:
        for artifact in self.artifacts:
            if artifact.path == path:
                return artifact
        raise KeyError(path)


DEFAULT_ARTIFACT_SPECS: tuple[ReproArtifactSpec, ...] = (
    ReproArtifactSpec("paper/main.tex", "article source"),
    ReproArtifactSpec("paper/references.bib", "article source"),
    ReproArtifactSpec("paper/sections/*.tex", "article source"),
    ReproArtifactSpec("paper/tables/*.tex", "generated paper assets"),
    ReproArtifactSpec("paper/figures/*.pdf", "generated paper assets"),
    ReproArtifactSpec("data/splits/paper_v1_manifest.jsonl", "frozen paper data"),
    ReproArtifactSpec(
        "data/barrages/hard_obvious_8x10_seed_20260531.jsonl",
        "frozen paper data",
    ),
    ReproArtifactSpec("data/item_cards/public_v0/cards.yaml", "item evidence"),
    ReproArtifactSpec(
        "data/human_baseline/paper_v1.csv",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "data/human_baseline/paper_v1_answer_key.csv",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "data/human_baseline/paper_v1_assignments.csv",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "data/human_baseline/paper_v1_response_template.csv",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "data/human_baseline/paper_v1_scored_draft.csv",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "data/human_baseline/paper_v1_threshold_items.csv",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "data/human_baseline/paper_v1_threshold_families.csv",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec("configs/paper_v1_analysis_plan.yaml", "analysis plan"),
    ReproArtifactSpec("configs/paper_v1_model_panel.yaml", "model panel"),
    ReproArtifactSpec(
        "configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv",
        "evidence-run manifest",
    ),
    ReproArtifactSpec(
        "results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison/comparison.csv",
        "evidence-run comparison",
    ),
    ReproArtifactSpec(
        "docs/reports/2026-06-02-paper-v1-combined-234-overline/report.html",
        "evidence-run report",
    ),
    ReproArtifactSpec("configs/paper_v1_related_work.yaml", "related work"),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-paper-analysis-plan.md",
        "analysis plan",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-related-work-positioning.md",
        "related work",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-human-baseline-participant-packets.md",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-handoff.md",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-human-baseline-promotion-report.md",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-human-baseline-operations.md",
        "deferred human baseline",
        required=False,
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-paper-source-audit.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-pdf-build-handoff.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-paper-claim-evidence-ledger.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-public-release-decision-packet.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-arxiv-internal-review.md",
        "audit report",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-final-sweep-plan.md",
        "run handoff",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md",
        "run handoff",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-report-section-tracker.md",
        "editorial tracker",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md",
        "editorial tracker",
    ),
    ReproArtifactSpec(
        "docs/research/2026-06-01-obviousbench-arxiv-completion-roadmap.md",
        "editorial tracker",
    ),
    ReproArtifactSpec("paper/arxiv-src.tar.gz", "arxiv source bundle"),
)

DEFAULT_COMMAND_SPECS: tuple[ReproCommandSpec, ...] = (
    ReproCommandSpec(
        "make -C paper assets",
        "Regenerate paper tables and figures from the current evidence run.",
        "Should pass without provider calls.",
    ),
    ReproCommandSpec(
        "make -C paper readiness",
        "Run the strict manifest-scoped paper-readiness gate.",
        "Expected to fail until real human-baseline rows exist.",
    ),
    ReproCommandSpec(
        "make -C paper readiness-preprint",
        "Run the fast-preprint paper-readiness gate.",
        (
            "Should pass without human-baseline rows when measured-human "
            "claims are omitted."
        ),
    ),
    ReproCommandSpec(
        "make -C paper related-work",
        "Regenerate the related-work positioning matrix and LaTeX table.",
        "Should pass when required comparator citations are present.",
    ),
    ReproCommandSpec(
        "make -C paper human-baseline-packet",
        "Regenerate participant assignments and response templates.",
        "Should pass without provider calls.",
    ),
    ReproCommandSpec(
        "make -C paper human-baseline-audit",
        "Audit human-baseline response collection completeness before scoring.",
        "Should pass and report blockers until real responses and timings are present.",
    ),
    ReproCommandSpec(
        "make -C paper human-baseline-collection-handoff",
        "Regenerate the human-baseline collection execution handoff.",
        "Should pass and report blockers until every response row is complete.",
    ),
    ReproCommandSpec(
        "make -C paper human-baseline-score",
        "Score filled human-baseline responses against the local answer key.",
        "Should pass and report blockers until real responses are present.",
    ),
    ReproCommandSpec(
        "make -C paper human-baseline-thresholds",
        "Classify scored human-baseline rows against predeclared paper thresholds.",
        "Should pass and report no-data blockers until real responses are present.",
    ),
    ReproCommandSpec(
        "make -C paper human-baseline-promotion",
        "Audit whether scored human-baseline rows can be promoted into paper_v1.csv.",
        "Should pass and report blockers until collection, scoring, and thresholds pass.",
    ),
    ReproCommandSpec(
        "make -C paper human-baseline-ops",
        "Regenerate the human-baseline collection and promotion operations handoff.",
        (
            "Should pass and report blockers until collection, scoring, "
            "thresholds, and readiness pass."
        ),
    ),
    ReproCommandSpec(
        "make -C paper result-artifacts",
        "Audit expected final paper-sweep summaries, comparison CSVs, and reports.",
        "Should pass and report missing artifacts until the final sweep has run.",
    ),
    ReproCommandSpec(
        "make -C paper release-audit",
        "Audit public release, license, citation, and metadata-link artifacts.",
        "Should pass and report blockers until public release decisions are confirmed.",
    ),
    ReproCommandSpec(
        "make -C paper release-packet",
        "Build the public-release decision packet and draft metadata templates.",
        "Should pass and report confirmation blockers until release decisions are final.",
    ),
    ReproCommandSpec(
        "make -C paper claims",
        "Audit unresolved manuscript claim markers.",
        "Expected to fail while claimblocked or obtodo markers remain.",
    ),
    ReproCommandSpec(
        "make -C paper claim-ledger",
        "Map unresolved claim markers to required replacement evidence.",
        "Expected to fail while markers remain, after writing the ledger.",
    ),
    ReproCommandSpec(
        "make -C paper source-audit",
        "Check TeX inputs, figures, bibliography, citations, and upload markers.",
        "Expected to fail while submission markers remain.",
    ),
    ReproCommandSpec(
        "make -C paper pdf-audit",
        "Audit the current PDF build environment, artifact, source, and log state.",
        "Expected to fail until a LaTeX toolchain, PDF, clean log, and clean source exist.",
    ),
    ReproCommandSpec(
        "make -C paper pdf-handoff",
        "Regenerate the PDF toolchain and inspection handoff.",
        "Should pass and report blockers until the PDF audit is clean.",
    ),
    ReproCommandSpec(
        "make -C paper arxiv-audit",
        "Build and audit the draft arXiv source bundle.",
        "Should pass when the local source bundle contains only allowed files.",
    ),
    ReproCommandSpec(
        "make -C paper preflight",
        "Aggregate final arXiv submission blockers.",
        "Expected to fail until PDF, metadata, release links, and claims are final.",
    ),
    ReproCommandSpec(
        "make -C paper submission-handoff",
        "Regenerate the upload-facing arXiv submission handoff.",
        "Should pass and report blocked upload readiness until final checks pass.",
    ),
    ReproCommandSpec(
        "make -C paper internal-review",
        "Run the local research-review gate.",
        "Expected to fail until final result evidence and claim replacements exist.",
    ),
    ReproCommandSpec(
        "make -C paper sweep-plan",
        "Generate the dry-run final-sweep handoff without running providers.",
        (
            "Should pass; Run allowed may be YES after preprint readiness and "
            "cost artifacts pass, but provider execution still needs approval."
        ),
    ),
    ReproCommandSpec(
        "make -C paper analysis-plan",
        "Regenerate the frozen paper reporting and statistics plan.",
        "Should pass without provider calls.",
    ),
    ReproCommandSpec(
        "make -C paper manuscript-completeness",
        "Audit expected arXiv manuscript components, assets, citations, and markers.",
        "Should pass and report blockers until final evidence-backed prose exists.",
    ),
    ReproCommandSpec(
        "make -C paper report-tracker",
        "Regenerate the manuscript section-status dashboard.",
        "Should pass without provider calls.",
    ),
    ReproCommandSpec(
        "make -C paper blocker-dashboard",
        "Regenerate the consolidated blocker dashboard from current paper audits.",
        "Should pass and report blocked/waiting rows until final evidence exists.",
    ),
    ReproCommandSpec(
        "make -C paper completion-roadmap",
        "Regenerate the ordered roadmap from current paper audits to arXiv submission.",
        "Should pass and report blocked/waiting phases until final evidence exists.",
    ),
    ReproCommandSpec(
        "make -C paper repro-manifest",
        "Regenerate this reproducibility manifest.",
        "Should pass once required local artifacts exist.",
    ),
)


def build_paper_repro_manifest(
    inputs: PaperReproManifestInputs,
) -> PaperReproManifestResult:
    """Hash paper artifacts and write a reproducibility manifest."""
    artifact_specs = inputs.artifact_specs or DEFAULT_ARTIFACT_SPECS
    command_specs = inputs.command_specs or DEFAULT_COMMAND_SPECS
    artifacts = tuple(_collect_artifacts(inputs.root_dir, artifact_specs))
    git_state = inputs.git_state
    if git_state is None and inputs.include_git_state:
        git_state = _read_git_state(inputs.root_dir)
    result = PaperReproManifestResult(
        output_path=inputs.output_path,
        artifacts=artifacts,
        commands=command_specs,
        git_state=git_state,
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _collect_artifacts(
    root_dir: Path,
    specs: tuple[ReproArtifactSpec, ...],
) -> list[ReproArtifact]:
    artifacts: list[ReproArtifact] = []
    for spec in specs:
        matches = _expand_spec(root_dir, spec.path)
        if not matches:
            artifacts.append(
                ReproArtifact(
                    path=spec.path,
                    category=spec.category,
                    required=spec.required,
                    exists=False,
                    size_bytes=None,
                    sha256=None,
                )
            )
            continue
        for path in matches:
            relative = path.relative_to(root_dir).as_posix()
            artifacts.append(
                ReproArtifact(
                    path=relative,
                    category=spec.category,
                    required=spec.required,
                    exists=True,
                    size_bytes=path.stat().st_size,
                    sha256=_sha256(path),
                )
            )
    return sorted(artifacts, key=lambda artifact: (artifact.category, artifact.path))


def _expand_spec(root_dir: Path, pattern: str) -> list[Path]:
    if any(char in pattern for char in "*?["):
        return sorted(path for path in root_dir.glob(pattern) if path.is_file())
    path = root_dir / pattern
    return [path] if path.is_file() else []


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_git_state(root_dir: Path) -> GitState | None:
    head = _git_output(root_dir, "rev-parse", "--short", "HEAD")
    status = _git_output(root_dir, "status", "--short")
    if head is None and status is None:
        return None
    status_lines = status.splitlines() if status else []
    return GitState(
        head=head,
        dirty=bool(status_lines),
        status_summary=(
            f"{len(status_lines)} changed or untracked path(s)"
            if status_lines
            else "clean"
        ),
    )


def _git_output(root_dir: Path, *args: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root_dir,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def _render_markdown(
    result: PaperReproManifestResult,
    inputs: PaperReproManifestInputs,
) -> str:
    lines = [
        "---",
        "title: ObviousBench Paper Reproducibility Manifest",
        f"date: {inputs.generated_on}",
        "type: research",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Paper Reproducibility Manifest",
        "",
        "This manifest records the local paper artifacts, hashes, and cheap",
        "rebuild commands needed to reproduce the current arXiv manuscript",
        "workspace. It is intentionally limited to source, configs, frozen",
        "paper data, generated paper assets, audit reports, and the draft",
        "source bundle. Provider logs and post-sweep summary directories are",
        "outside this manifest's scope.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        (
            "Required artifacts: "
            f"{result.present_required_count}/{result.required_count} present"
        ),
        "",
        f"Missing required artifacts: {result.missing_required_count}",
        "",
    ]
    lines.extend(_git_lines(result.git_state))
    lines.extend(_artifact_lines(result.artifacts))
    lines.extend(_command_lines(result.commands))
    return "\n".join(lines)


def _git_lines(git_state: GitState | None) -> list[str]:
    lines = ["## Git State", ""]
    if git_state is None:
        lines.extend(
            [
                "Git state was not recorded.",
                "",
            ]
        )
        return lines
    lines.extend(
        [
            f"- Head: `{git_state.head or 'unknown'}`",
            f"- Worktree: `{_dirty_label(git_state.dirty)}`",
            f"- Status summary: {git_state.status_summary}",
            "",
        ]
    )
    return lines


def _artifact_lines(artifacts: tuple[ReproArtifact, ...]) -> list[str]:
    lines = [
        "## Artifact Inventory",
        "",
        "| Category | Path | Required | Status | Bytes | SHA-256 |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for artifact in artifacts:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(artifact.category),
                    _cell(f"`{artifact.path}`"),
                    "yes" if artifact.required else "no",
                    "present" if artifact.exists else "missing",
                    str(artifact.size_bytes) if artifact.size_bytes is not None else "",
                    f"`{artifact.sha256}`" if artifact.sha256 else "",
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _command_lines(commands: tuple[ReproCommandSpec, ...]) -> list[str]:
    lines = [
        "## Rebuild And Check Commands",
        "",
        "| Command | Purpose | Expected status |",
        "| --- | --- | --- |",
    ]
    for command in commands:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(f"`{command.command}`"),
                    _cell(command.purpose),
                    _cell(command.expected_status),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _dirty_label(dirty: bool | None) -> str:
    if dirty is None:
        return "unknown"
    return "dirty" if dirty else "clean"


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")
