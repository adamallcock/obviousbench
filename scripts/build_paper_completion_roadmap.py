#!/usr/bin/env python
"""Build the ObviousBench arXiv completion roadmap."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.paper_completion_roadmap import (  # noqa: E402
    PaperCompletionRoadmapInputs,
    build_paper_completion_roadmap,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_paper_completion_roadmap.py")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-arxiv-completion-roadmap.md",
    )
    parser.add_argument("--paper-dir", default="paper")
    parser.add_argument(
        "--report-plan",
        default="docs/research/2026-06-01-obviousbench-arxiv-report-plan.md",
    )
    parser.add_argument(
        "--blocker-dashboard",
        default="docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md",
    )
    parser.add_argument(
        "--repro-manifest",
        default="docs/research/2026-06-01-obviousbench-paper-reproducibility-manifest.md",
    )
    parser.add_argument(
        "--threshold-items",
        default="data/human_baseline/paper_v1_threshold_items.csv",
    )
    parser.add_argument(
        "--threshold-report",
        default="docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md",
    )
    parser.add_argument(
        "--collection-audit",
        default="docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md",
    )
    parser.add_argument(
        "--human-baseline-ops",
        default="docs/research/2026-06-01-paper-v1-human-baseline-operations.md",
    )
    parser.add_argument(
        "--final-sweep-plan",
        default="docs/research/2026-06-01-paper-v1-final-sweep-plan.md",
    )
    parser.add_argument(
        "--result-artifact-audit",
        default="docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md",
    )
    parser.add_argument(
        "--internal-review",
        default="docs/research/2026-06-01-obviousbench-arxiv-internal-review.md",
    )
    parser.add_argument(
        "--section-tracker",
        default="docs/research/2026-06-01-obviousbench-report-section-tracker.md",
    )
    parser.add_argument(
        "--manuscript-completeness",
        default=(
            "docs/research/"
            "2026-06-01-obviousbench-manuscript-completeness-audit.md"
        ),
    )
    parser.add_argument(
        "--submission-checklist",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md",
    )
    parser.add_argument(
        "--submission-handoff",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md",
    )
    parser.add_argument(
        "--pdf-audit",
        default="docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md",
    )
    parser.add_argument(
        "--metadata",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md",
    )
    parser.add_argument(
        "--release-audit",
        default="docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md",
    )
    parser.add_argument(
        "--release-packet",
        default=(
            "docs/research/"
            "2026-06-01-obviousbench-public-release-decision-packet.md"
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when any completion-roadmap phase is not passing.",
    )
    parser.add_argument(
        "--publication-mode",
        choices=("strict", "preprint"),
        default="preprint",
        help=(
            "strict treats human collection as a required phase; preprint "
            "defers human-baseline validation and blocks measured-human claims."
        ),
    )
    args = parser.parse_args(argv)

    result = build_paper_completion_roadmap(
        PaperCompletionRoadmapInputs(
            output_path=Path(args.out),
            paper_dir=Path(args.paper_dir),
            report_plan_path=Path(args.report_plan),
            blocker_dashboard_path=Path(args.blocker_dashboard),
            repro_manifest_path=Path(args.repro_manifest),
            threshold_items_path=Path(args.threshold_items),
            threshold_report_path=Path(args.threshold_report),
            collection_audit_path=Path(args.collection_audit),
            human_baseline_ops_path=Path(args.human_baseline_ops),
            final_sweep_plan_path=Path(args.final_sweep_plan),
            result_artifact_audit_path=Path(args.result_artifact_audit),
            internal_review_path=Path(args.internal_review),
            section_tracker_path=Path(args.section_tracker),
            manuscript_completeness_path=Path(args.manuscript_completeness),
            submission_checklist_path=Path(args.submission_checklist),
            submission_handoff_path=Path(args.submission_handoff),
            pdf_audit_path=Path(args.pdf_audit),
            metadata_path=Path(args.metadata),
            release_audit_path=Path(args.release_audit),
            release_packet_path=Path(args.release_packet),
            publication_mode=args.publication_mode,
        )
    )
    print(
        f"Wrote paper completion roadmap to {result.output_path}: "
        f"{result.passed_count} passed, {result.blocked_count} blocked, "
        f"{result.waiting_count} waiting"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
