"""Static ObviousBench website generation from comparison artifacts."""

from __future__ import annotations

import html
import json
from dataclasses import dataclass
from pathlib import Path

from obviousbench.analysis.benchmark_report import (
    _bar_svg,
    _display_money,
    _family_heatmap_rows,
    _leaderboard_rows,
    _read_csv,
    _scatter_svg,
    _tokens_scatter_svg,
    _write_csv,
)


@dataclass(frozen=True)
class BenchmarkSiteInputs:
    comparison_dir: Path
    output_dir: Path
    generated_on: str
    title: str = "ObviousBench"
    report_href: str = "report.html"


@dataclass(frozen=True)
class BenchmarkSitePaths:
    index: Path
    leaderboard_csv: Path
    family_heatmap_csv: Path
    data_json: Path


def build_benchmark_site(inputs: BenchmarkSiteInputs) -> BenchmarkSitePaths:
    """Build a dependency-free static site from comparison CSV artifacts."""
    inputs.output_dir.mkdir(parents=True, exist_ok=True)
    comparison_rows = _read_csv(inputs.comparison_dir / "comparison.csv")
    family_rows = _read_csv(inputs.comparison_dir / "family_comparison.csv")
    leaderboard = _leaderboard_rows(comparison_rows)
    family_heatmap = _family_heatmap_rows(family_rows)

    paths = BenchmarkSitePaths(
        index=inputs.output_dir / "index.html",
        leaderboard_csv=inputs.output_dir / "leaderboard.csv",
        family_heatmap_csv=inputs.output_dir / "family-heatmap.csv",
        data_json=inputs.output_dir / "site-data.json",
    )
    _write_csv(paths.leaderboard_csv, leaderboard)
    _write_csv(paths.family_heatmap_csv, family_heatmap)
    paths.data_json.write_text(
        json.dumps(
            {
                "title": inputs.title,
                "generated_on": inputs.generated_on,
                "source_files": [
                    (inputs.comparison_dir / "comparison.csv").as_posix(),
                    (inputs.comparison_dir / "family_comparison.csv").as_posix(),
                ],
                "leaderboard": leaderboard,
                "family_heatmap": family_heatmap,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    paths.index.write_text(
        _site_html(
            title=inputs.title,
            generated_on=inputs.generated_on,
            report_href=inputs.report_href,
            leaderboard=leaderboard,
            family_heatmap=family_heatmap,
        ),
        encoding="utf-8",
    )
    return paths


def _site_html(
    *,
    title: str,
    generated_on: str,
    report_href: str,
    leaderboard: list[dict[str, str]],
    family_heatmap: list[dict[str, str]],
) -> str:
    best = next((row for row in leaderboard if row["rank"]), leaderboard[0])
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{html.escape(title)}</title>",
            "<style>",
            _site_css(),
            "</style>",
            "</head>",
            "<body>",
            "<main>",
            '<section class="site-hero">',
            f'<p class="site-meta">generated on {html.escape(generated_on)}</p>',
            f"<h1>{html.escape(title)}</h1>",
            "<p class=\"site-lede\">Human-trivial reliability, made inspectable</p>",
            "<div class=\"site-summary\">",
            _site_stat("Top answer accuracy", f"{html.escape(best['answer_accuracy_pct'])}%"),
            _site_stat("Comparable runs", str(sum(1 for row in leaderboard if row["rank"]))),
            _site_stat("Published surface", "docs/reports"),
            "</div>",
            "</section>",
            '<section class="site-section ob-site-frontier" id="model-frontier">',
            "<h2>Model Frontier</h2>",
            "<p>Accuracy, token use, and cost sit beside each other so leaderboard "
            "wins can be read as tradeoffs instead of a single score.</p>",
            _scatter_svg(leaderboard),
            _tokens_scatter_svg(leaderboard),
            _bar_svg(leaderboard),
            _site_leaderboard_table(leaderboard),
            "</section>",
            '<section class="site-section" id="failure-archetypes">',
            "<h2>Failure Archetypes</h2>",
            "<p>Family slices expose where aggregate scores hide brittle behavior.</p>",
            _site_family_table(family_heatmap),
            "</section>",
            '<section class="site-section" id="reproducibility">',
            "<h2>Reproducibility</h2>",
            "<p>This page is generated from the same comparison CSVs used by the "
            "non-arXiv report. Publish the paired outputs under docs/reports and "
            "link the detailed report for audit trails.</p>",
            f'<a class="report-link" href="{html.escape(report_href, quote=True)}">'
            "Open full report</a>",
            "</section>",
            "</main>",
            "</body>",
            "</html>",
        ]
    )


def _site_stat(label: str, value: str) -> str:
    return (
        "<div>"
        f"<span>{html.escape(label)}</span>"
        f"<strong>{value}</strong>"
        "</div>"
    )


def _site_leaderboard_table(rows: list[dict[str, str]]) -> str:
    body = []
    for row in rows:
        body.append(
            "<tr>"
            f"<td>{html.escape(row['rank'] or 'n/a')}</td>"
            f"<td>{html.escape(row['display_label'])}</td>"
            f"<td>{html.escape(row['answer_accuracy_pct'])}%</td>"
            f"<td>{html.escape(row['format_accuracy_pct'])}%</td>"
            f"<td>{html.escape(row['strict_accuracy_pct'])}%</td>"
            f"<td>{html.escape(_display_money(row['estimated_cost_usd']))}</td>"
            f"<td>{html.escape(row['provider_errors'])}</td>"
            "</tr>"
        )
    return _site_table(
        ["Rank", "Model", "Answer", "Format", "Strict", "Run Cost", "Provider Errors"],
        body,
    )


def _site_family_table(rows: list[dict[str, str]]) -> str:
    body = []
    for row in rows[:24]:
        body.append(
            "<tr>"
            f"<td>{html.escape(row['label'])}</td>"
            f"<td>{html.escape(row['family'])}</td>"
            f"<td>{html.escape(row['accuracy_pct'])}%</td>"
            f"<td>{html.escape(row['failures'])}</td>"
            f"<td>{html.escape(row['samples'])}</td>"
            "</tr>"
        )
    return _site_table(["Model", "Family", "Accuracy", "Failures", "Samples"], body)


def _site_table(headers: list[str], body_rows: list[str]) -> str:
    header = "".join(f"<th>{html.escape(value)}</th>" for value in headers)
    return (
        "<table><thead><tr>"
        + header
        + "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table>"
    )


def _site_css() -> str:
    return "\n".join(
        [
            ":root { --ink: #171b1f; --muted: #5e6673; --line: #d7dde5; "
            "--paper: #ffffff; --wash: #f4f2ed; --accent: #106a63; "
            "--accent-2: #c25a2a; --gold: #e7b84b; --rose: #b4475f; }",
            "body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, "
            "sans-serif; color: var(--ink); background: var(--wash); }",
            "main { max-width: 1180px; margin: 0 auto; padding: 34px 24px 72px; }",
            ".site-hero { min-height: 72vh; display: grid; align-content: center; "
            "border-bottom: 1px solid #ddd4c7; }",
            ".site-meta { color: var(--muted); margin: 0 0 10px; font-size: 13px; }",
            "h1 { margin: 0; font-size: 64px; line-height: 0.98; }",
            ".site-lede { max-width: 680px; margin: 18px 0 0; font-size: 23px; "
            "line-height: 1.35; color: #39414a; }",
            ".site-summary { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); "
            "gap: 12px; margin-top: 32px; }",
            ".site-summary div { background: var(--paper); border: 1px solid var(--line); "
            "border-radius: 8px; padding: 14px 16px; }",
            ".site-summary span { display: block; color: var(--muted); "
            "font-size: 12px; font-weight: 650; }",
            ".site-summary strong { display: block; margin-top: 6px; font-size: 18px; }",
            ".site-section { padding: 30px 0; border-bottom: 1px solid #ddd4c7; }",
            ".site-section h2 { margin: 0 0 10px; font-size: 26px; }",
            ".site-section p { max-width: 760px; color: var(--muted); line-height: 1.55; }",
            ".ob-site-frontier svg { margin-top: 14px; }",
            "table { width: 100%; border-collapse: collapse; margin-top: 16px; "
            "background: var(--paper); border: 1px solid var(--line); border-radius: 8px; "
            "overflow: hidden; }",
            "th, td { padding: 9px 10px; border-bottom: 1px solid #e8ebef; "
            "text-align: left; vertical-align: top; font-size: 13px; }",
            "th { background: #ece7dd; font-weight: 650; }",
            ".report-link { display: inline-flex; margin-top: 8px; padding: 9px 12px; "
            "border: 1px solid var(--accent); border-radius: 6px; color: #fff; "
            "background: var(--accent); text-decoration: none; font-weight: 650; }",
            "svg { width: 100%; height: auto; background: var(--paper); "
            "border: 1px solid var(--line); border-radius: 8px; padding: 12px; "
            "box-sizing: border-box; }",
            "svg rect { fill: var(--accent); }",
            "svg.ob-range-bar rect:nth-of-type(2n) { fill: var(--accent-2); }",
            "svg circle { fill: var(--muted); stroke: #fff; stroke-width: 1.5; }",
            "svg .provider-openai { fill: #1874a5; }",
            "svg .provider-anthropic { fill: #8b5e3c; }",
            "svg .provider-google { fill: #278656; }",
            "svg .provider-openrouter { fill: #c25a2a; }",
            "svg .provider-grok { fill: #b4475f; }",
            "svg .frontier { stroke: #111827; stroke-width: 2; }",
            "svg .frontier-line { fill: none; stroke: #111827; stroke-width: 2; "
            "stroke-dasharray: 5 4; }",
            "svg .grid-line { stroke: #e4e7ec; stroke-width: 1; }",
            "svg line { stroke: #98a2b3; stroke-width: 1; }",
            "svg text { fill: #344054; font-size: 12px; }",
            "svg .point-label { font-size: 11px; }",
            "@media (max-width: 820px) { main { padding: 24px 16px 56px; } "
            ".site-hero { min-height: 66vh; } h1 { font-size: 42px; } "
            ".site-lede { font-size: 19px; } .site-summary { grid-template-columns: 1fr; } "
            "table { display: block; overflow-x: auto; } }",
        ]
    )
