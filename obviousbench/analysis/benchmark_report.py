"""Static benchmark report generation from comparison summaries."""

from __future__ import annotations

import csv
import html
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BenchmarkReportInputs:
    comparison_dir: Path
    output_dir: Path
    generated_on: str
    title: str = "ObviousBench Report"


@dataclass(frozen=True)
class BenchmarkReportPaths:
    html: Path
    leaderboard_csv: Path
    leaderboard_md: Path
    family_heatmap_csv: Path


def build_benchmark_report(inputs: BenchmarkReportInputs) -> BenchmarkReportPaths:
    """Build a dependency-free HTML report plus machine-readable tables."""
    inputs.output_dir.mkdir(parents=True, exist_ok=True)
    comparison_rows = _read_csv(inputs.comparison_dir / "comparison.csv")
    family_rows = _read_csv(inputs.comparison_dir / "family_comparison.csv")

    leaderboard = _leaderboard_rows(comparison_rows)
    family_heatmap = _family_heatmap_rows(family_rows)

    paths = BenchmarkReportPaths(
        html=inputs.output_dir / "report.html",
        leaderboard_csv=inputs.output_dir / "leaderboard.csv",
        leaderboard_md=inputs.output_dir / "leaderboard.md",
        family_heatmap_csv=inputs.output_dir / "family-heatmap.csv",
    )
    _write_csv(paths.leaderboard_csv, leaderboard)
    _write_csv(paths.family_heatmap_csv, family_heatmap)
    paths.leaderboard_md.write_text(_leaderboard_markdown(leaderboard), encoding="utf-8")
    paths.html.write_text(
        _html_report(
            title=inputs.title,
            generated_on=inputs.generated_on,
            leaderboard=leaderboard,
            family_heatmap=family_heatmap,
        ),
        encoding="utf-8",
    )
    return paths


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _leaderboard_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    max_scored_samples = max((_int(row.get("scored_samples")) for row in rows), default=0)
    sorted_rows = sorted(
        rows,
        key=lambda row: (
            _int(row.get("scored_samples")) != max_scored_samples,
            -_float(row.get("accuracy")),
            _int(row.get("provider_errors")),
            _float(row.get("estimated_cost_usd")),
            row.get("label", ""),
        ),
    )
    leaderboard: list[dict[str, str]] = []
    rank = 0
    for row in sorted_rows:
        comparable = (
            max_scored_samples > 0
            and _int(row.get("scored_samples")) == max_scored_samples
        )
        if comparable:
            rank += 1
            rank_value = str(rank)
        else:
            rank_value = ""
        correct = _int(row.get("correct"))
        cost = _optional_float(row.get("estimated_cost_usd"))
        total_tokens = _int(row.get("total_tokens"))
        leaderboard.append(
            {
                "rank": rank_value,
                "label": row.get("label", ""),
                "model": row.get("model", ""),
                "barrage_profile": row.get("barrage_profile", ""),
                "accuracy_pct": _format_percent(row.get("accuracy")),
                "answer_accuracy_pct": _format_percent(
                    row.get("answer_accuracy") or row.get("accuracy")
                ),
                "format_accuracy_pct": _format_percent(
                    row.get("format_accuracy") or row.get("accuracy")
                ),
                "strict_accuracy_pct": _format_percent(
                    row.get("strict_accuracy") or row.get("accuracy")
                ),
                "obvious_failure_rate_pct": _format_percent(
                    row.get("obvious_failure_rate")
                ),
                "correct": str(correct),
                "answer_correct": str(_int(row.get("answer_correct") or row.get("correct"))),
                "format_correct": str(_int(row.get("format_correct") or row.get("correct"))),
                "strict_correct": str(_int(row.get("strict_correct") or row.get("correct"))),
                "scored_samples": str(_int(row.get("scored_samples"))),
                "provider_errors": str(_int(row.get("provider_errors"))),
                "timeouts": str(_int(row.get("timeouts"))),
                "total_tokens": str(total_tokens),
                "estimated_cost_usd": _format_money(cost),
                "cost_per_correct_usd": _format_money(
                    cost / correct if cost is not None and correct else None
                ),
                "tokens_per_correct": _format_number(
                    total_tokens / correct if correct else None
                ),
                "cost_warnings": row.get("cost_warnings", ""),
                "summary_dir": row.get("summary_dir", ""),
            }
        )
    return leaderboard


def _family_heatmap_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    heatmap: list[dict[str, str]] = []
    for row in sorted(rows, key=lambda item: (item.get("label", ""), item.get("family", ""))):
        samples = _int(row.get("samples"))
        correct = _int(row.get("correct"))
        heatmap.append(
            {
                "label": row.get("label", ""),
                "family": row.get("family", ""),
                "accuracy_pct": f"{(correct / samples * 100):.2f}" if samples else "",
                "correct": str(correct),
                "samples": str(samples),
                "failures": str(_int(row.get("failures"))),
                "estimated_cost_usd": row.get("estimated_cost_usd", ""),
            }
        )
    return heatmap


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _leaderboard_markdown(rows: list[dict[str, str]]) -> str:
    headers = [
        "Rank",
        "Model",
        "Answer",
        "Format",
        "Strict",
        "Cost",
        "Cost / Correct",
        "Provider Errors",
    ]
    lines = [
        "# ObviousBench Leaderboard",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["rank"] or "n/a",
                    row["label"],
                    f"{row['answer_accuracy_pct']}%",
                    f"{row['format_accuracy_pct']}%",
                    f"{row['strict_accuracy_pct']}%",
                    _display_money(row["estimated_cost_usd"]),
                    _display_money(row["cost_per_correct_usd"]),
                    row["provider_errors"],
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def _html_report(
    *,
    title: str,
    generated_on: str,
    leaderboard: list[dict[str, str]],
    family_heatmap: list[dict[str, str]],
) -> str:
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{html.escape(title)}</title>",
            "<style>",
            _css(),
            "</style>",
            "</head>",
            "<body>",
            "<main>",
            f"<h1>{html.escape(title)}</h1>",
            f'<p class="meta">Generated on {html.escape(generated_on)}</p>',
            _summary_cards(leaderboard),
            "<h2>Leaderboard</h2>",
            _leaderboard_table(leaderboard),
            "<h2>Accuracy vs Estimated Cost</h2>",
            _scatter_svg(leaderboard),
            "<h2>Accuracy Leaderboard</h2>",
            _bar_svg(leaderboard),
            "<h2>Family Accuracy Heatmap</h2>",
            _heatmap_table(family_heatmap),
            "<h2>Provider Errors</h2>",
            _provider_errors(leaderboard),
            "<h2>Reading Notes</h2>",
            "<ul>",
            "<li>Rank scored runs by accuracy, while keeping provider-error rows visible.</li>",
            "<li>Show cost, token, and cost-per-correct tradeoffs beside accuracy.</li>",
            "<li>Use family slices to reveal where aggregate scores hide weak spots.</li>",
            "</ul>",
            "</main>",
            "</body>",
            "</html>",
        ]
    )


def _summary_cards(rows: list[dict[str, str]]) -> str:
    scored = [row for row in rows if row["rank"]]
    best = scored[0] if scored else {}
    cheapest = min(
        scored,
        key=lambda row: _optional_float(row["estimated_cost_usd"]) or float("inf"),
        default={},
    )
    return (
        '<section class="cards">'
        f'<div><span>Best Accuracy</span><strong>{html.escape(best.get("label", "n/a"))}</strong>'
        f'<em>{html.escape(best.get("accuracy_pct", ""))}%</em></div>'
        f'<div><span>Lowest Cost</span><strong>{html.escape(cheapest.get("label", "n/a"))}</strong>'
        f'<em>{html.escape(_display_money(cheapest.get("estimated_cost_usd", "")))}</em></div>'
        f"<div><span>Runs</span><strong>{len(rows)}</strong><em>{len(scored)} scored</em></div>"
        "</section>"
    )


def _leaderboard_table(rows: list[dict[str, str]]) -> str:
    headers = [
        "Rank",
        "Model",
        "Profile",
        "Answer",
        "Format",
        "Strict",
        "Correct",
        "Cost",
        "Cost / Correct",
        "Tokens",
        "Provider Errors",
    ]
    body = []
    for row in rows:
        body.append(
            "<tr>"
            f"<td>{html.escape(row['rank'] or 'n/a')}</td>"
            f"<td>{html.escape(row['label'])}<br><code>{html.escape(row['model'])}</code></td>"
            f"<td>{html.escape(row['barrage_profile'])}</td>"
            f"<td>{html.escape(row['answer_accuracy_pct'])}%</td>"
            f"<td>{html.escape(row['format_accuracy_pct'])}%</td>"
            f"<td>{html.escape(row['strict_accuracy_pct'])}%</td>"
            f"<td>{html.escape(row['correct'])}/{html.escape(row['scored_samples'])}</td>"
            f"<td>{html.escape(_display_money(row['estimated_cost_usd']))}</td>"
            f"<td>{html.escape(_display_money(row['cost_per_correct_usd']))}</td>"
            f"<td>{html.escape(row['total_tokens'])}</td>"
            f"<td>{html.escape(row['provider_errors'])}</td>"
            "</tr>"
        )
    return _table(headers, body)


def _scatter_svg(rows: list[dict[str, str]]) -> str:
    points = [
        (
            row,
            _optional_float(row["estimated_cost_usd"]),
            _optional_float(row["accuracy_pct"]),
        )
        for row in rows
        if row["rank"] and _optional_float(row["estimated_cost_usd"]) is not None
    ]
    if not points:
        return "<p>No costed scored runs available.</p>"
    max_cost = max(cost or 0 for _, cost, _ in points) or 1
    width, height, pad = 760, 360, 48
    circles = []
    for row, cost, accuracy in points:
        x = pad + ((cost or 0) / max_cost) * (width - pad * 2)
        y = height - pad - ((accuracy or 0) / 100) * (height - pad * 2)
        label = html.escape(row["label"])
        circles.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6"><title>{label}: '
            f'{row["accuracy_pct"]}% at '
            f'{_display_money(row["estimated_cost_usd"])}</title></circle>'
        )
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" '
        'aria-label="Accuracy versus estimated cost scatter plot">'
        f'<line x1="{pad}" y1="{height-pad}" x2="{width-pad}" y2="{height-pad}" />'
        f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{height-pad}" />'
        f'<text x="{width/2}" y="{height-10}">Estimated cost USD</text>'
        '<text x="8" y="24">Accuracy</text>'
        + "".join(circles)
        + "</svg>"
    )


def _bar_svg(rows: list[dict[str, str]]) -> str:
    scored = [row for row in rows if row["rank"]][:12]
    width = 760
    row_height = 30
    height = 36 + len(scored) * row_height
    bars = []
    for index, row in enumerate(scored):
        y = 24 + index * row_height
        value = _optional_float(row["accuracy_pct"]) or 0
        bar_width = value / 100 * 420
        bars.append(
            f'<text x="0" y="{y + 15}">{html.escape(row["label"][:28])}</text>'
            f'<rect x="240" y="{y}" width="{bar_width:.1f}" height="18" />'
            f'<text x="{248 + bar_width:.1f}" y="{y + 14}">{value:.1f}%</text>'
        )
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" '
        'aria-label="Accuracy leaderboard bar chart">'
        + "".join(bars)
        + "</svg>"
    )


def _heatmap_table(rows: list[dict[str, str]]) -> str:
    headers = ["Model", "Family", "Accuracy", "Failures", "Samples"]
    body = []
    for row in rows:
        accuracy = _optional_float(row["accuracy_pct"])
        shade = _heat_color(accuracy)
        body.append(
            "<tr>"
            f"<td>{html.escape(row['label'])}</td>"
            f"<td>{html.escape(row['family'])}</td>"
            f'<td style="background:{shade}">{html.escape(row["accuracy_pct"])}%</td>'
            f"<td>{html.escape(row['failures'])}</td>"
            f"<td>{html.escape(row['samples'])}</td>"
            "</tr>"
        )
    return _table(headers, body)


def _provider_errors(rows: list[dict[str, str]]) -> str:
    error_rows = [
        row
        for row in rows
        if _int(row["provider_errors"]) or row.get("cost_warnings")
    ]
    if not error_rows:
        return "<p>No provider errors or cost warnings in this comparison.</p>"
    items = []
    for row in error_rows:
        details = row.get("cost_warnings") or "provider request errors"
        items.append(
            f"<li><strong>{html.escape(row['label'])}</strong>: "
            f"{html.escape(row['provider_errors'])} provider errors; "
            f"{html.escape(details)}</li>"
        )
    return "<ul>" + "".join(items) + "</ul>"


def _table(headers: list[str], body_rows: list[str]) -> str:
    header = "".join(f"<th>{html.escape(value)}</th>" for value in headers)
    return (
        "<table><thead><tr>"
        + header
        + "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table>"
    )


def _css() -> str:
    return "\n".join(
        [
            "body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, "
            "sans-serif; color: #18202a; background: #f7f8fa; }",
            "main { max-width: 1180px; margin: 0 auto; padding: 32px 24px 64px; }",
            "h1 { margin: 0 0 4px; font-size: 32px; }",
            "h2 { margin-top: 34px; font-size: 21px; }",
            ".meta { color: #667085; margin-top: 0; }",
            ".cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); "
            "gap: 12px; margin: 24px 0; }",
            ".cards div { background: #fff; border: 1px solid #d9dee7; "
            "border-radius: 8px; padding: 14px 16px; }",
            ".cards span { display: block; color: #667085; font-size: 13px; }",
            ".cards strong { display: block; margin-top: 6px; }",
            ".cards em { display: block; margin-top: 4px; color: #475467; "
            "font-style: normal; }",
            "table { width: 100%; border-collapse: collapse; background: #fff; "
            "border: 1px solid #d9dee7; }",
            "th, td { padding: 9px 10px; border-bottom: 1px solid #e7eaf0; "
            "text-align: left; vertical-align: top; font-size: 13px; }",
            "th { background: #eef1f6; font-weight: 650; }",
            "code { color: #475467; font-size: 12px; }",
            "svg { width: 100%; height: auto; background: #fff; "
            "border: 1px solid #d9dee7; border-radius: 8px; padding: 12px; "
            "box-sizing: border-box; }",
            "svg rect { fill: #4062bb; }",
            "svg circle { fill: #cc5a43; stroke: #fff; stroke-width: 1.5; }",
            "svg line { stroke: #98a2b3; stroke-width: 1; }",
            "svg text { fill: #344054; font-size: 12px; }",
            "@media (max-width: 720px) { .cards { grid-template-columns: 1fr; } "
            "table { display: block; overflow-x: auto; } }",
        ]
    )


def _heat_color(value: float | None) -> str:
    if value is None:
        return "#f2f4f7"
    if value >= 95:
        return "#c7f0d8"
    if value >= 85:
        return "#dff3b8"
    if value >= 70:
        return "#fff0a6"
    return "#ffd0c2"


def _display_money(value: str) -> str:
    if value == "":
        return "n/a"
    try:
        return f"${float(value):.6f}"
    except ValueError:
        return value


def _format_percent(value: str | None) -> str:
    return f"{_float(value) * 100:.2f}"


def _format_money(value: float | None) -> str:
    return "" if value is None else f"{value:.8f}".rstrip("0").rstrip(".")


def _format_number(value: float | None) -> str:
    return "" if value is None else f"{value:.2f}"


def _optional_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _float(value: str | None) -> float:
    return _optional_float(value) or 0.0


def _int(value: str | None) -> int:
    try:
        return int(float(value or 0))
    except ValueError:
        return 0
