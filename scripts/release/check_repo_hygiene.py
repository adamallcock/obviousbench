#!/usr/bin/env python3
"""Check the public repository for private-data and release-lane regressions."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

PRIVATE_DATA_PREFIXES = (
    "data/private_heldout_v0_1/",
    "data/private_heldout_v0_2/",
    "data/benchmark/private_heldout/",
)

PRIVATE_MANIFEST_PATHS = (
    "data/manifests/splits/draft_v0_1/private_heldout_manifest.jsonl",
    "data/manifests/splits/draft_v0_1/reserve_manifest.jsonl",
    "data/splits/draft_v0_1/private_heldout_manifest.jsonl",
    "data/splits/draft_v0_1/reserve_manifest.jsonl",
)

PRIVATE_MANIFEST_PREFIXES = (
    "data/manifests/candidate_pools/candidate_pool_v0_2",
    "data/splits/candidate_pool_v0_2",
)

PRIVATE_MANIFEST_EXACT = (
    "data/manifests/candidate_pools/candidate_pool_v0_1_approved_manifest.jsonl",
    "data/splits/candidate_pool_v0_1_approved_manifest.jsonl",
)

LEGACY_DATA_PREFIXES = (
    "data/barrages/",
    "data/calibration_v0/",
    "data/dev_regression_v0_1/",
    "data/experiments/",
    "data/human_baseline/",
    "data/item_cards/",
    "data/public_examples_v0_1/",
    "data/public_v0/",
    "data/source_catalog/",
    "data/splits/",
)

GENERATED_OUTPUT_PREFIXES = ("dist/", "results/", "tmp/")
ALLOWED_REPORT_PREFIXES = ("reports/v0_2/aggregate/",)
FORBIDDEN_REPORT_PREFIXES = (
    "reports/runs/",
    "reports/v0_1/",
    "reports/v0_2/private_pass3",
    "reports/v0_2/v0_2_private_pass3",
    "reports/v0_2/rebalance_analysis",
    "reports/v0_2/diagnostics",
)

DISALLOWED_DOC_FILES = {
    "docs/evidence-and-claims.md",
    "docs/positioning/branding.md",
}

DISALLOWED_DOC_PREFIXES = (
    "docs/concepts/",
    "docs/internal/",
    "docs/release/v0_1/",
    "docs/superpowers/plans/",
)

REQUIRED_IGNORE_PATTERNS = (
    "dist/",
    "results/",
    "reports/runs/",
    "reports/v0_2/private_pass3*",
    "data/benchmark/private_heldout/v0_2/",
    "data/manifests/candidate_pools/candidate_pool_v0_2*.jsonl",
    "data/manifests/splits/draft_v0_1/private_heldout_manifest.jsonl",
)

REQUIRED_REPO_FILES = (
    "README.md",
    "configs/README.md",
    "configs/releases/release_v0_2_0.yaml",
    "configs/model_panels/models_v0.example.yaml",
    "configs/model_panels/models_v0_2_public.yaml",
    "configs/registries/model_registry_v1.yaml",
    "configs/registries/model_thinking_settings_v1.yaml",
    "docs/positioning/background-and-rhetoric.md",
    "docs/reference/benchmark-card.md",
    "docs/reference/methodology.md",
    "docs/reference/scoring-policy.md",
    "docs/reference/source-policy.md",
    "docs/reference/website.md",
    "docs/release/v0_2/generated/README.md",
    "reports/v0_2/aggregate/report.md",
    "reports/v0_2/aggregate/summary.csv",
    "scripts/README.md",
)

ACTIVE_TEXT_FILES = (
    "README.md",
    "configs/README.md",
    "docs/positioning/background-and-rhetoric.md",
    "docs/reference/benchmark-card.md",
    "docs/reference/methodology.md",
    "docs/reference/scoring-policy.md",
    "docs/reference/source-policy.md",
    "docs/reference/website.md",
    "docs/release/v0_2/generated/README.md",
    "scripts/README.md",
)

BANNED_ACTIVE_TEXT = (
    "docs/concepts",
    "docs/internal",
    "docs/superpowers/plans",
    "wrong_answer_review.html",
    "question_failure_review.html",
)

FORBIDDEN_CODE_IMPORTS = (
    "obviousbench.research",
    "scripts.build_v0_1_private_pass3",
    "scripts.plan_v0_1_private_pass3",
    "scripts.run_v0_1_private_pass3",
)


@dataclass(frozen=True)
class HygieneIssue:
    check: str
    path: str
    detail: str


def _normalize(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def _git_ls_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    raw = result.stdout.decode("utf-8")
    return [_normalize(path) for path in raw.split("\0") if path]


def _read_text(root: Path, path: str) -> str:
    try:
        return (root / path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def tracked_path_issues(paths: Iterable[str]) -> list[HygieneIssue]:
    issues: list[HygieneIssue] = []
    for raw_path in sorted({_normalize(path) for path in paths}):
        name = Path(raw_path).name
        if name == ".DS_Store" or raw_path.endswith((".pyc", ".pyo")):
            issues.append(
                HygieneIssue(
                    "tracked-local-junk",
                    raw_path,
                    "local cache or OS metadata should never be tracked",
                )
            )
        if raw_path.startswith(PRIVATE_DATA_PREFIXES):
            issues.append(
                HygieneIssue(
                    "tracked-private-data",
                    raw_path,
                    "private held-out runtime data must remain local and ignored",
                )
            )
        if raw_path in PRIVATE_MANIFEST_PATHS:
            issues.append(
                HygieneIssue(
                    "tracked-private-manifest",
                    raw_path,
                    "private/reserve split manifests must remain local and ignored",
                )
            )
        if raw_path in PRIVATE_MANIFEST_EXACT or raw_path.startswith(
            PRIVATE_MANIFEST_PREFIXES
        ):
            issues.append(
                HygieneIssue(
                    "tracked-private-candidate-pool",
                    raw_path,
                    "private candidate-pool manifests must remain local and ignored",
                )
            )
        if raw_path.startswith(LEGACY_DATA_PREFIXES):
            issues.append(
                HygieneIssue(
                    "tracked-legacy-data-path",
                    raw_path,
                    "public v0.2 data belongs under data/public_examples/",
                )
            )
        if raw_path.startswith(GENERATED_OUTPUT_PREFIXES):
            issues.append(
                HygieneIssue(
                    "tracked-generated-output",
                    raw_path,
                    "local run outputs, caches, and release bundles must stay untracked",
                )
            )
        if raw_path.startswith("reports/") and not raw_path.startswith(
            ALLOWED_REPORT_PREFIXES
        ):
            issues.append(
                HygieneIssue(
                    "tracked-nonaggregate-report",
                    raw_path,
                    "only sanitized aggregate reports are public-tracked",
                )
            )
        for prefix in FORBIDDEN_REPORT_PREFIXES:
            if raw_path.startswith(prefix):
                issues.append(
                    HygieneIssue(
                        "tracked-private-or-generated-report",
                        raw_path,
                        "private/rebalance/diagnostic report outputs are not public release assets",
                    )
                )
                break
        if raw_path in DISALLOWED_DOC_FILES:
            issues.append(
                HygieneIssue(
                    "tracked-disallowed-doc",
                    raw_path,
                    "retired docs must stay untracked or in the internal repo",
                )
            )
        for prefix in DISALLOWED_DOC_PREFIXES:
            if raw_path.startswith(prefix):
                issues.append(
                    HygieneIssue(
                        "tracked-disallowed-doc-path",
                        raw_path,
                        "internal, v0.1, and planning docs must not ship in the public repo",
                    )
                )
                break
    return issues


def docs_architecture_issues(root: Path) -> list[HygieneIssue]:
    issues: list[HygieneIssue] = []

    for relative in REQUIRED_REPO_FILES:
        if not (root / relative).is_file():
            issues.append(
                HygieneIssue(
                    "missing-required-public-file",
                    relative,
                    "public release source file must remain materialized",
                )
            )

    ignore_path = root / ".gitignore"
    ignore_lines = (
        ignore_path.read_text(encoding="utf-8").splitlines()
        if ignore_path.is_file()
        else []
    )
    for pattern in REQUIRED_IGNORE_PATTERNS:
        if pattern not in ignore_lines:
            issues.append(
                HygieneIssue(
                    "missing-ignore-pattern",
                    ".gitignore",
                    f"expected ignore pattern {pattern}",
                )
            )

    for relative in ACTIVE_TEXT_FILES:
        path = root / relative
        if not path.is_file():
            issues.append(
                HygieneIssue(
                    "missing-active-public-text",
                    relative,
                    "active public text file should exist",
                )
            )
            continue
        text = _read_text(root, relative)
        for needle in BANNED_ACTIVE_TEXT:
            if needle in text:
                issues.append(
                    HygieneIssue(
                        "banned-active-text-reference",
                        relative,
                        f"replace stale/private reference to {needle}",
                    )
                )
    return issues


def code_import_issues(root: Path, paths: Iterable[str]) -> list[HygieneIssue]:
    issues: list[HygieneIssue] = []
    for path in sorted({_normalize(path) for path in paths}):
        if not path.endswith(".py"):
            continue
        if not path.startswith(("obviousbench/", "scripts/")):
            continue
        text = _read_text(root, path)
        for needle in FORBIDDEN_CODE_IMPORTS:
            if needle in text and path != "scripts/release/check_repo_hygiene.py":
                issues.append(
                    HygieneIssue(
                        "forbidden-private-code-import",
                        path,
                        f"public code must not import {needle}",
                    )
                )
    return issues


def check_repo_hygiene(
    root: Path,
    tracked_paths: Sequence[str] | None = None,
    *,
    check_repository_files: bool | None = None,
) -> list[HygieneIssue]:
    paths = list(tracked_paths) if tracked_paths is not None else _git_ls_files(root)
    issues = tracked_path_issues(paths)
    if check_repository_files is None:
        check_repository_files = tracked_paths is None
    if check_repository_files:
        issues.extend(docs_architecture_issues(root))
    issues.extend(code_import_issues(root, paths))
    return sorted(issues, key=lambda issue: (issue.check, issue.path, issue.detail))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check tracked ObviousBench public paths for repo hygiene regressions."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root. Defaults to the checkout containing this script.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    issues = check_repo_hygiene(root)
    if args.format == "json":
        payload = {
            "ok": not issues,
            "issue_count": len(issues),
            "issues": [asdict(issue) for issue in issues],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif issues:
        print(f"Repo hygiene check failed: {len(issues)} issue(s).")
        for issue in issues:
            print(f"- [{issue.check}] {issue.path}: {issue.detail}")
    else:
        print("Repo hygiene check passed.")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
