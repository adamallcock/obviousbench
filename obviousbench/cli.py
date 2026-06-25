"""Command-line interface for local ObviousBench workflows."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from obviousbench.analysis.benchmark_report import (
    BenchmarkReportInputs,
    build_benchmark_report,
)
from obviousbench.analysis.benchmark_site import (
    BenchmarkSiteInputs,
    build_benchmark_site,
)
from obviousbench.analysis.comparison import (
    ComparisonBuildInputs,
    build_comparison_from_manifest,
)
from obviousbench.analysis.shareable_artifacts import (
    ShareableArtifactInputs,
    build_shareable_artifacts,
)
from obviousbench.analysis.summarize_results import summarize_results
from obviousbench.barrage import (
    BarrageProfile,
    build_barrage,
    load_split_items,
    write_barrage_jsonl,
)
from obviousbench.costing.estimate import CostEstimateInputs, estimate_benchmark_cost
from obviousbench.datasets.validation import validate_dataset_paths


def _validate(args: argparse.Namespace) -> int:
    report = validate_dataset_paths(
        [Path(path) for path in args.paths],
        item_cards_dir=Path(args.item_cards_dir) if args.item_cards_dir else None,
        require_item_cards=args.require_item_cards,
        allow_extra_item_cards=args.allow_extra_item_cards,
    )
    if report.ok:
        print("Validation passed.")
        return 0
    for issue in report.issues:
        print(issue.format(), file=sys.stderr)
    return 1


def _summarize(args: argparse.Namespace) -> int:
    try:
        output_paths = summarize_results(
            Path(args.logs),
            Path(args.out),
            cost_mode=args.cost,
            rescore=getattr(args, "rescore", False),
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    for output_path in output_paths:
        print(f"Wrote {output_path}")
    return 0


def _make_barrage(args: argparse.Namespace) -> int:
    try:
        profile = BarrageProfile.parse(args.profile)
        items = build_barrage(
            load_split_items(args.split, data_dir=Path(args.data_dir)),
            profile,
            seed=args.seed,
            max_metamorphic_siblings_per_group=(
                args.max_metamorphic_siblings_per_group
            ),
        )
        output = write_barrage_jsonl(items, Path(args.out))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Wrote {len(items)} barrage samples to {output}")
    return 0


def _estimate_cost(args: argparse.Namespace) -> int:
    try:
        estimate = estimate_benchmark_cost(
            CostEstimateInputs(
                model=args.model,
                profile=args.profile,
                seed=args.seed,
                split=args.split,
                data_dir=Path(args.data_dir),
                summary_root=Path(args.summary_root),
                cache_dir=None if args.no_cache else Path(args.cache_dir),
                cache=None if args.no_cache else args.cache,
                settings=_parse_settings(args.setting),
                max_metamorphic_siblings_per_group=(
                    args.max_metamorphic_siblings_per_group
                ),
            )
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(asdict(estimate), indent=2, sort_keys=True))
        return 0

    print(f"Dry-run cost estimate for {estimate.model}")
    print(f"profile: {estimate.profile} seed={estimate.seed}")
    print(f"billable samples: {estimate.billable_samples}/{estimate.total_samples}")
    print(f"cache hits: {estimate.cache_hits}")
    print(f"estimated billable cost: {_format_money(estimate.estimated_billable_cost_usd)}")
    print(
        "estimated cached cost avoided: "
        f"{_format_money(estimate.estimated_cached_cost_avoided_usd)}"
    )
    print(f"usage basis: {estimate.usage_source}")
    print(f"pricing: {estimate.pricing_source}")
    for warning in estimate.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return 0


def _build_shareable(args: argparse.Namespace) -> int:
    try:
        output_paths = build_shareable_artifacts(
            ShareableArtifactInputs(
                comparison_dir=Path(args.comparison_dir),
                output_dir=Path(args.out),
                generated_on=args.generated_on,
                benchmark_card_source=Path(args.benchmark_card_source),
                model_matrix_source=Path(args.model_matrix_source),
                max_failures=args.max_failures,
            )
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    for attr in (
        "card",
        "gallery",
        "comparison",
        "family_comparison",
        "model_matrix",
        "index",
    ):
        output_path = getattr(output_paths, attr)
        print(f"Wrote {output_path}")
    return 0


def _build_report(args: argparse.Namespace) -> int:
    try:
        output_paths = build_benchmark_report(
            BenchmarkReportInputs(
                comparison_dir=Path(args.comparison_dir),
                output_dir=Path(args.out),
                generated_on=args.generated_on,
                title=args.title,
            )
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    for attr in ("html", "leaderboard_csv", "leaderboard_md", "family_heatmap_csv"):
        print(f"Wrote {getattr(output_paths, attr)}")
    return 0


def _build_site(args: argparse.Namespace) -> int:
    try:
        output_paths = build_benchmark_site(
            BenchmarkSiteInputs(
                comparison_dir=Path(args.comparison_dir),
                output_dir=Path(args.out),
                generated_on=args.generated_on,
                title=args.title,
                report_href=args.report_href,
            )
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    for attr in ("index", "leaderboard_csv", "family_heatmap_csv", "data_json"):
        print(f"Wrote {getattr(output_paths, attr)}")
    return 0


def _build_comparison(args: argparse.Namespace) -> int:
    try:
        output_paths = build_comparison_from_manifest(
            ComparisonBuildInputs(
                manifest=Path(args.manifest),
                output_dir=Path(args.out),
                summary_root=Path(args.summary_root) if args.summary_root else None,
                baseline_comparison=(
                    Path(args.baseline_comparison)
                    if args.baseline_comparison
                    else None
                ),
                manual_xai_costs=args.manual_xai_costs,
                openrouter_price_registry=(
                    Path(args.openrouter_price_registry)
                    if args.openrouter_price_registry
                    else None
                ),
            )
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    for attr in (
        "comparison",
        "family_comparison",
        "section_comparison",
        "effort_curve",
        "metamorphic_consistency",
        "delta",
    ):
        print(f"Wrote {getattr(output_paths, attr)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="obviousbench")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate benchmark JSONL files")
    validate.add_argument("paths", nargs="+")
    validate.add_argument("--item-cards-dir")
    validate.add_argument("--require-item-cards", action="store_true")
    validate.add_argument("--allow-extra-item-cards", action="store_true")
    validate.set_defaults(func=_validate)

    summarize = subparsers.add_parser("summarize", help="Summarize Inspect logs")
    summarize.add_argument("--logs", required=True)
    summarize.add_argument("--out", required=True)
    summarize.add_argument("--cost", choices=["none", "runcost"], default="runcost")
    summarize.add_argument(
        "--rescore",
        action="store_true",
        help="Recompute deterministic scores from logged model completions.",
    )
    summarize.set_defaults(func=_summarize)

    rescore = subparsers.add_parser(
        "rescore",
        help="Summarize logs after recomputing scores with current deterministic scorers",
    )
    rescore.add_argument("--logs", required=True)
    rescore.add_argument("--out", required=True)
    rescore.add_argument("--cost", choices=["none", "runcost"], default="runcost")
    rescore.set_defaults(func=_summarize, rescore=True)

    make_barrage = subparsers.add_parser(
        "make-barrage",
        help="Materialize a deterministic balanced barrage JSONL file",
    )
    make_barrage.add_argument("--profile", default="balanced_8x5")
    make_barrage.add_argument("--split", default="public_v0")
    make_barrage.add_argument("--seed", default=20260531, type=int)
    make_barrage.add_argument("--data-dir", default="data")
    make_barrage.add_argument("--out", required=True)
    make_barrage.add_argument("--max-metamorphic-siblings-per-group", default=1, type=int)
    make_barrage.set_defaults(func=_make_barrage)

    shareable = subparsers.add_parser(
        "build-shareable",
        help="Promote summarized results into tracked shareable Markdown and CSV artifacts",
    )
    shareable.add_argument("--comparison-dir", required=True)
    shareable.add_argument("--out", required=True)
    shareable.add_argument("--generated-on", required=True)
    shareable.add_argument("--benchmark-card-source", default="docs/reference/benchmark-card.md")
    shareable.add_argument(
        "--model-matrix-source",
        default="configs/model_panels/models_v0.example.yaml",
    )
    shareable.add_argument("--max-failures", default=8, type=int)
    shareable.set_defaults(func=_build_shareable)

    report = subparsers.add_parser(
        "build-report",
        help="Build a static benchmark report with leaderboard tables and SVG charts",
    )
    report.add_argument("--comparison-dir", required=True)
    report.add_argument("--out", required=True)
    report.add_argument("--generated-on", required=True)
    report.add_argument("--title", default="ObviousBench Report")
    report.set_defaults(func=_build_report)

    site = subparsers.add_parser(
        "build-site",
        help="Build a static ObviousBench website shell from comparison artifacts",
    )
    site.add_argument("--comparison-dir", required=True)
    site.add_argument("--out", required=True)
    site.add_argument("--generated-on", required=True)
    site.add_argument("--title", default="ObviousBench")
    site.add_argument("--report-href", default="report.html")
    site.set_defaults(func=_build_site)

    comparison = subparsers.add_parser(
        "build-comparison",
        help="Aggregate summarized run directories into comparison CSVs",
    )
    comparison.add_argument("--manifest", required=True)
    comparison.add_argument("--out", required=True)
    comparison.add_argument(
        "--summary-root",
        help="Optional root used with the basename of each manifest summary_dir",
    )
    comparison.add_argument(
        "--baseline-comparison",
        help="Optional previous comparison.csv used to write delta.csv",
    )
    comparison.add_argument(
        "--manual-xai-costs",
        action="store_true",
        help="Apply direct xAI Grok pricing when runcost has no price card",
    )
    comparison.add_argument(
        "--openrouter-price-registry",
        help=(
            "Optional model_registry_v1.yaml path used to recalculate rows with "
            "missing runcost component prices"
        ),
    )
    comparison.set_defaults(func=_build_comparison)

    estimate = subparsers.add_parser(
        "estimate-cost",
        help="Dry-run benchmark cost using historical usage, runcost, and cache hits",
    )
    estimate.add_argument("--model", required=True)
    estimate.add_argument("--profile", default="balanced_8x5")
    estimate.add_argument("--seed", default=20260531, type=int)
    estimate.add_argument("--split", default="public_v0")
    estimate.add_argument("--data-dir", default="data")
    estimate.add_argument("--summary-root", default="results/summaries")
    estimate.add_argument("--cache", default="10Y")
    estimate.add_argument("--cache-dir", default=".cache/inspect")
    estimate.add_argument("--no-cache", action="store_true")
    estimate.add_argument(
        "--setting",
        action="append",
        default=[],
        help="Generation setting as key=value, e.g. reasoning_effort=low.",
    )
    estimate.add_argument("--max-metamorphic-siblings-per-group", default=1, type=int)
    estimate.add_argument("--json", action="store_true")
    estimate.set_defaults(func=_estimate_cost)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def _parse_settings(values: list[str]) -> dict[str, str]:
    settings = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Invalid setting {value!r}; expected key=value.")
        key, setting_value = value.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid setting {value!r}; expected non-empty key.")
        settings[key] = setting_value.strip()
    return settings


def _format_money(value: float | None) -> str:
    if value is None:
        return "unknown"
    return f"${value:.6f}"


if __name__ == "__main__":
    raise SystemExit(main())
