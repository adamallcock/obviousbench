#!/usr/bin/env python
"""Build the ObviousBench paper reproducibility manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.paper_repro_manifest import (  # noqa: E402
    PaperReproManifestInputs,
    ReproArtifactSpec,
    build_paper_repro_manifest,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_paper_repro_manifest.py")
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--out",
        default=(
            "docs/research/"
            "2026-06-01-obviousbench-paper-reproducibility-manifest.md"
        ),
    )
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help=(
            "Required artifact path to include instead of the default paper "
            "manifest set. May be repeated."
        ),
    )
    parser.add_argument(
        "--no-git-state",
        action="store_true",
        help="Skip git head/worktree status capture.",
    )
    args = parser.parse_args(argv)

    artifact_specs = tuple(
        ReproArtifactSpec(path=path, category="custom artifact")
        for path in args.artifact
    )
    result = build_paper_repro_manifest(
        PaperReproManifestInputs(
            root_dir=Path(args.root),
            output_path=Path(args.out),
            artifact_specs=artifact_specs,
            include_git_state=not args.no_git_state,
        )
    )
    print(
        f"Wrote paper reproducibility manifest to {result.output_path}: "
        f"{len(result.artifacts)} artifact entrie(s), "
        f"{result.missing_required_count} missing required"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
