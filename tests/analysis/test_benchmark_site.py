import csv
import shutil
from pathlib import Path

from obviousbench.analysis.benchmark_site import (
    BenchmarkSiteInputs,
    build_benchmark_site,
)

REPORT_FIXTURES = Path(__file__).parents[1] / "fixtures" / "benchmark_report"


def test_build_benchmark_site_uses_comparison_artifacts(tmp_path):
    comparison_dir = tmp_path / "comparison"
    shutil.copytree(REPORT_FIXTURES / "rich_comparison", comparison_dir)
    output_dir = tmp_path / "site"

    paths = build_benchmark_site(
        BenchmarkSiteInputs(
            comparison_dir=comparison_dir,
            output_dir=output_dir,
            generated_on="2026-06-14",
            title="ObviousBench Example Site",
            report_href="../archive/reports/report.html",
        )
    )

    html = paths.index.read_text(encoding="utf-8")
    leaderboard_rows = list(csv.DictReader(paths.leaderboard_csv.open(encoding="utf-8")))
    data_json = paths.data_json.read_text(encoding="utf-8")

    assert paths.index == output_dir / "index.html"
    assert paths.leaderboard_csv == output_dir / "leaderboard.csv"
    assert paths.family_heatmap_csv == output_dir / "family-heatmap.csv"
    assert paths.data_json == output_dir / "site-data.json"
    assert leaderboard_rows[0]["display_label"] == (
        "Verbose Correct Model (thinking=medium/reasoning-visible)"
    )
    assert "ObviousBench Example Site" in html
    assert "Human-trivial reliability, made inspectable" in html
    assert "Model Frontier" in html
    assert "Failure Archetypes" in html
    assert "Reproducibility" in html
    assert "../archive/reports/report.html" in html
    assert "docs/reports" in html
    assert "generated on 2026-06-14" in html
    assert "Verbose Correct Model" in html
    assert "Provider Flaky Model" in html
    assert "ob-site-frontier" in html
    assert '"generated_on": "2026-06-14"' in data_json
    assert '"leaderboard"' in data_json
