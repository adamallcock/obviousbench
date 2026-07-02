#!/usr/bin/env python3
"""Smoke tests for the generated ObviousBench launch site."""

from __future__ import annotations

import json
import re
import struct
import unittest
from pathlib import Path

from build_site import build_rows, make_standalone

ROOT = Path(__file__).resolve().parent


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if not header.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"{path} is not a PNG")
    return struct.unpack(">II", header[16:24])


class ReleaseSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows, cls.build = build_rows(
            ROOT / "data" / "summary.csv",
            ROOT / "data" / "row-metadata.json",
        )
        cls.by_id = {row["row_id"]: row for row in cls.rows}

    def test_release_counts(self) -> None:
        self.assertEqual(len(self.rows), 306)
        self.assertEqual(self.build["item_count"], 144)
        self.assertEqual(self.build["attempts_per_item"], 3)
        self.assertEqual(self.build["failure_family_count"], 8)
        self.assertEqual(self.build["surface_row_count"], 299)
        self.assertEqual(self.build["narrative_row_count"], 293)
        self.assertEqual(self.build["narrative_surface_row_count"], 286)
        self.assertEqual(self.build["diagnostic_row_count"], 7)
        self.assertEqual(self.build["release_date"], "2026-07-01")

    def test_canonical_story_values(self) -> None:
        expected_values = (
            ("old-136-openai-gpt-5-4-nano-no-thinking", "answer", 36.8056),
            ("old-199-openai-gpt-5-4-nano-low", "answer", 52.7778),
            ("old-230-openai-gpt-5-4-nano-medium", "answer", 71.5278),
            ("old-231-openai-gpt-5-4-nano-high", "answer", 81.9444),
            ("old-234-openai-gpt-5-4-nano-xhigh", "answer", 91.6667),
            ("manual-20260612-google-gemma-4-31b-it-high", "answer", 100.0),
            ("manual-20260612-google-gemma-4-31b-it-high", "strict", 100.0),
        )
        for row_id, metric, expected in expected_values:
            self.assertAlmostEqual(self.by_id[row_id][metric], expected)

    def test_no_duplicate_ids(self) -> None:
        self.assertEqual(len(self.by_id), len(self.rows))

    def test_builder_does_not_depend_on_internal_archives(self) -> None:
        builder = (ROOT / "build_site.py").read_text(encoding="utf-8")
        self.assertNotIn("internal_archive", builder)
        self.assertNotIn("report_review_surfaces", builder)

    def test_diagnostics_are_not_on_public_browser_surface(self) -> None:
        diagnostic = [row for row in self.rows if not row["surface_included"]]
        self.assertTrue(any(row["row_id"] == "old-157-grok-build-0-1" for row in diagnostic))
        public_rows = [row for row in self.rows if row["surface_included"]]
        self.assertEqual(len(public_rows), self.build["surface_row_count"])
        self.assertFalse(any(row["row_id"] == "old-157-grok-build-0-1" for row in public_rows))
        explicit_grok_build = [
            row
            for row in self.rows
            if row["model"] == "x-ai/grok-build-0.1"
            and row["row_id"] != "old-157-grok-build-0-1"
        ]
        self.assertTrue(explicit_grok_build)
        self.assertTrue(all(row["surface_included"] for row in explicit_grok_build))

    def test_gemini_31_pro_is_public_data_not_narrative(self) -> None:
        gemini_rows = [
            row for row in self.rows if row["model"] == "google/gemini-3.1-pro-preview"
        ]
        self.assertEqual(
            {row["row_id"] for row in gemini_rows},
            {
                "manual-20260625-google-gemini-3-1-pro-preview-low",
                "manual-20260625-google-gemini-3-1-pro-preview-medium",
                "manual-20260625-google-gemini-3-1-pro-preview-high",
            },
        )
        self.assertEqual({row["effort"] for row in gemini_rows}, {"low", "medium", "high"})
        self.assertTrue(all(row["surface_included"] for row in gemini_rows))
        self.assertTrue(all(row["narrative_included"] is False for row in gemini_rows))
        self.assertEqual(
            {row["surface_note"] for row in gemini_rows},
            {
                "Published aggregate row; included on public data and frontier surfaces, "
                "excluded from written narrative rollups."
            },
        )

    def test_sonnet_5_is_public_data_in_frontier_and_sonnet_progress_cut(self) -> None:
        sonnet_rows = [
            row for row in self.rows if row["model"] == "anthropic/claude-sonnet-5"
        ]
        self.assertEqual(
            {row["row_id"] for row in sonnet_rows},
            {
                "manual-20260630-anthropic-claude-sonnet-5-low",
                "manual-20260630-anthropic-claude-sonnet-5-medium",
                "manual-20260630-anthropic-claude-sonnet-5-high",
                "manual-20260630-anthropic-claude-sonnet-5-xhigh",
                "manual-20260630-anthropic-claude-sonnet-5-max",
            },
        )
        self.assertEqual(
            {row["effort"] for row in sonnet_rows},
            {"low", "medium", "high", "xhigh", "max"},
        )
        self.assertTrue(all(row["surface_included"] for row in sonnet_rows))
        self.assertTrue(all(row["narrative_included"] is False for row in sonnet_rows))
        self.assertEqual(
            {row["surface_note"] for row in sonnet_rows},
            {
                "Published aggregate row; included on public data, frontier, and Claude "
                "Sonnet progress surfaces; excluded from written narrative rollups."
            },
        )

    def test_fable_5_is_public_data_not_narrative(self) -> None:
        fable_rows = [
            row for row in self.rows if row["model"] == "anthropic/claude-fable-5"
        ]
        self.assertEqual(
            {row["row_id"] for row in fable_rows},
            {
                "manual-20260701-anthropic-claude-fable-5-low",
                "manual-20260701-anthropic-claude-fable-5-medium",
                "manual-20260701-anthropic-claude-fable-5-high",
                "manual-20260701-anthropic-claude-fable-5-xhigh",
                "manual-20260701-anthropic-claude-fable-5-max",
            },
        )
        self.assertEqual(
            {row["effort"] for row in fable_rows},
            {"low", "medium", "high", "xhigh", "max"},
        )
        self.assertTrue(all(row["surface_included"] for row in fable_rows))
        self.assertTrue(all(row["narrative_included"] is False for row in fable_rows))
        self.assertEqual(
            {row["surface_note"] for row in fable_rows},
            {
                "Published aggregate row; included on public data and frontier surfaces, "
                "excluded from written narrative rollups."
            },
        )

    def test_public_frontier_uses_all_surface_rows(self) -> None:
        public_frontier_rows = [row for row in self.rows if row["surface_included"]]
        non_narrative_surface_models = {
            row["model"] for row in public_frontier_rows if row["narrative_included"] is False
        }
        self.assertEqual(len(public_frontier_rows), 299)
        self.assertEqual(
            non_narrative_surface_models,
            {
                "anthropic/claude-fable-5",
                "anthropic/claude-sonnet-5",
                "google/gemini-3.1-pro-preview",
            },
        )

    def test_saturation_family_counts(self) -> None:
        best = {}
        for row in self.rows:
            if not row["surface_included"] or not row["narrative_included"]:
                continue
            current = best.get(row["model_family"])
            if (
                current is None
                or row["answer"] > current["answer"]
                or (row["answer"] == current["answer"] and row["cost"] < current["cost"])
            ):
                best[row["model_family"]] = row
        family_ids_at_95 = {
            row["model_family"]
            for row in best.values()
            if row["answer"] >= 95
        }
        self.assertEqual(len(family_ids_at_95), 42)
        self.assertEqual(sum(row["answer"] >= 98 for row in best.values()), 18)
        self.assertEqual(
            sum(
                row["surface_included"]
                and row["narrative_included"]
                and row["model_family"] in family_ids_at_95
                and row["answer"] < 80
                for row in self.rows
            ),
            22,
        )

    def test_saturation_section_layout_and_context_link(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        section_start = html.index('id="saturation"')
        section_end = html.index('id="comparisons"', section_start)
        saturation_section = html[section_start:section_end]

        self.assertIn(
            "techcrunch.com/2026/05/27/why-googles-ai-cant-spell-google-or-anything-else/",
            html,
        )
        self.assertIn('class="inline-text-link"', html)
        self.assertIn('rel="noopener noreferrer"', html)
        self.assertNotIn("evidence-layout-reverse", saturation_section)
        self.assertNotIn("mini-stat-row", saturation_section)
        self.assertIn("or obscure false negatives", saturation_section)

    def test_release_story_frontloads_findings_and_keeps_measure_context_in_hero(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        ordered_sections = [
            'id="overview"',
            'id="frontier"',
            'id="thresholds"',
            'id="result"',
            'id="saturation"',
            'id="comparisons"',
            'id="explorer"',
        ]
        positions = [html.index(marker) for marker in ordered_sections]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('id="measure"', html)
        self.assertIn('class="hero-summary"', html)
        self.assertIn("visible-failure families", html)
        self.assertIn("What this measures", html)
        self.assertIn("How to read it", html)
        self.assertIn("What it is not", html)
        self.assertIn('href="#frontier">Findings</a>', html)
        self.assertIn('href="#thresholds">Decision table</a>', html)
        self.assertIn('href="#result">Reasoning proof</a>', html)
        self.assertIn("Benchmark release · July 2026", html)
        self.assertIn('data-build-stat="release_date">2026-07-01', html)

    def test_standalone_has_no_local_asset_dependencies(self) -> None:
        output = make_standalone(ROOT)
        html = output.read_text(encoding="utf-8")
        self.assertNotRegex(html, r'<script src="(?!https?)[^"]+')
        self.assertNotRegex(html, r'<link rel="stylesheet" href="[^"]+')
        self.assertNotIn('href="assets/', html)
        self.assertNotIn('src="assets/', html)
        self.assertIn('href="data:image/png;base64,', html)
        self.assertIn('src="data:image/png;base64,', html)
        self.assertIn('href="data:application/manifest+json;base64,', html)
        self.assertIn("window.OBVIOUSBENCH_ROWS=", html)
        self.assertIn("window.OBVIOUSBENCH_BUILD=", html)
        self.assertNotIn("old-157-grok-build-0-1", html)
        self.assertNotIn("Show diagnostic rows", html)

    def test_standalone_has_apex_canonical_metadata(self) -> None:
        output = make_standalone(ROOT)
        html = output.read_text(encoding="utf-8")
        self.assertIn('<link rel="canonical" href="https://obviousbench.com/">', html)
        self.assertIn('property="og:url" content="https://obviousbench.com/"', html)
        self.assertIn('name="twitter:card" content="summary"', html)

    def test_category_examples_are_aligned_and_use_car_wash_constraint(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count("<span><strong>"), 8)
        self.assertIn("The car wash is 100m away.", html)
        self.assertIn("→ drive there", html)
        self.assertNotIn("repair garage", html)
        self.assertNotIn("car windshield", html)
        self.assertIn("<small><em>What is 27 - 9 + 4?</em><b>→ 22</b></small>", html)

    def test_html_ids_are_unique(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        ids = re.findall(r'\sid="([^"]+)"', html)
        self.assertEqual(len(ids), len(set(ids)))

    def test_release_page_branding_and_method_section_are_removed(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        brand_mark = re.search(r"\.brand-mark \{(?P<body>.*?)\n\}", css, re.S)
        self.assertIsNotNone(brand_mark)
        mark_css = brand_mark.group("body")
        self.assertIn("<span>ObviousBench</span>", html)
        self.assertIn('src="assets/obviousbench-mark.png"', html)
        self.assertIn('rel="icon" type="image/png" sizes="32x32"', html)
        self.assertIn('rel="icon" type="image/png" sizes="16x16"', html)
        self.assertIn('rel="apple-touch-icon" sizes="180x180"', html)
        self.assertIn('rel="manifest" href="assets/site.webmanifest"', html)
        self.assertIn("background: transparent;", mark_css)
        self.assertIn("box-shadow: none;", mark_css)
        self.assertIn("object-fit: contain;", css)
        self.assertNotIn("object-fit: cover;", css)
        self.assertNotIn("<svg viewBox=", html)
        self.assertNotIn('href="data:,"', html)
        self.assertIn('href="#explorer">See data</a>', html)
        self.assertNotIn("ObviousBench v0.2", html)
        self.assertNotIn("<b>v0.2</b>", html)
        self.assertNotIn("Read the methodology", html)
        self.assertNotIn("Open aggregate CSV", html)
        self.assertNotIn('href="#methodology"', html)
        self.assertNotIn('id="methodology"', html)
        self.assertNotIn("Methodology and interpretation", html)
        explorer = re.search(
            r'<section id="explorer".*?<div class="section-number" aria-hidden="true">06</div>',
            html,
            re.S,
        )
        self.assertIsNotNone(explorer)
        self.assertIn(
            '<section id="explorer" class="section section-shell section-tint">',
            html,
        )

    def test_manifest_icons_use_surface_specific_assets(self) -> None:
        manifest = json.loads((ROOT / "assets" / "site.webmanifest").read_text(encoding="utf-8"))
        icons = {(icon["src"], icon.get("purpose", "any")): icon for icon in manifest["icons"]}
        self.assertIn(("icon-192.png", "any"), icons)
        self.assertIn(("icon-512.png", "any"), icons)
        self.assertIn(("icon-maskable-192.png", "maskable"), icons)
        self.assertIn(("icon-maskable-512.png", "maskable"), icons)

        expected_sizes = {
            "favicon-16x16.png": (16, 16),
            "favicon-32x32.png": (32, 32),
            "apple-touch-icon.png": (180, 180),
            "icon-192.png": (192, 192),
            "icon-512.png": (512, 512),
            "icon-maskable-192.png": (192, 192),
            "icon-maskable-512.png": (512, 512),
            "obviousbench-mark.png": (512, 512),
        }
        for filename, expected in expected_sizes.items():
            self.assertEqual(png_size(ROOT / "assets" / filename), expected)

    def test_frontier_controls_are_public_surface_only(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "app.js").read_text(encoding="utf-8")
        for required_id in (
            "frontier-provider-picker",
            "frontier-model-picker",
            "frontier-effort-picker",
            "frontier-provider-strip",
        ):
            self.assertIn(f'id="{required_id}"', html)
        self.assertNotIn('id="frontier-diagnostics"', html)
        self.assertNotIn('id="explorer-diagnostics"', html)
        self.assertNotIn("Show diagnostic rows", html)
        self.assertIn(
            "const inputRows = Array.isArray(window.OBVIOUSBENCH_ROWS)",
            script,
        )
        self.assertIn(
            "const rows = inputRows.filter((row) => row.surface_included);",
            script,
        )
        self.assertIn(
            "const narrativeRows = rows.filter((row) => row.narrative_included !== false);",
            script,
        )
        self.assertIn(
            "const narrativeSurfaceRows = narrativeRows.filter((row) => row.surface_included);",
            script,
        )
        self.assertIn("const filtered = surfaceRows", script)
        self.assertNotIn("frontierState.diagnostics", script)
        self.assertNotIn("explorerState.diagnostics", script)
        self.assertNotIn(".filter((row) => frontierState.diagnostics", script)
        self.assertNotIn(".filter((row) => explorerState.diagnostics", script)
        self.assertNotIn("diagnostic-row", script)
        self.assertNotIn("diagnostic-note", script)
        self.assertIn("cheapestPerFamily(narrativeRows", script)
        self.assertIn("familyBest(narrativeSurfaceRows)", script)
        self.assertIn("filter: (row) => row.cost > 0,", script)
        self.assertIn("frontierState.modelFamily", script)
        self.assertIn("providers: []", script)
        self.assertIn(".filter(rowMatchesFrontierProviders)", script)
        self.assertIn("function frontierColor(row)", script)
        self.assertIn("Color = model family", script)
        self.assertIn('option.value !== "all"', script)
        self.assertIn("event.altKey || event.shiftKey || event.metaKey || event.ctrlKey", script)
        self.assertIn('id="frontier-color-legend"', html)
        self.assertNotIn("highlightedFamily =", script)
        self.assertIn("highlightedFamilies: []", script)
        self.assertIn(
            "frontierState.highlightedFamilies = value === \"all\" ? [] : [value]",
            script,
        )
        self.assertIn("Shift/Alt/Cmd/Ctrl-click to compare several families", script)
        self.assertIn("replaceMerge: [\"series\"]", script)
        self.assertIn("DEFAULT_FRONTIER_LABEL_FAMILIES", script)
        self.assertIn("function frontierFamilyConnectorSeries", script)
        self.assertIn("Faint colored lines connect visible settings", script)
        self.assertIn("frontier-family-trail-", script)
        self.assertIn("frontier-default-labels", script)
        self.assertIn("frontier-selected-labels", script)
        self.assertIn("selected.clear();", script)
        self.assertIn("Colored lines label all visible settings", script)

    def test_gemini_31_pro_is_not_hardcoded_into_narrative_surfaces(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("Gemini 3.1 Pro", html)
        self.assertNotIn("gemini-3.1-pro", html)
        self.assertNotIn("google/gemini-3.1-pro-preview", script)
        self.assertNotIn("gemini-3-1-pro", script)
        self.assertNotIn("Gemini 3.1 Pro", script)

    def test_fable_5_is_not_hardcoded_into_narrative_surfaces(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("Claude Fable 5", html)
        self.assertNotIn("Fable 5", html)
        self.assertNotIn("anthropic/claude-fable-5", script)
        self.assertNotIn("claude-fable-5", script)
        self.assertNotIn("Claude Fable 5", script)

    def test_section_two_uses_gpt_5_4_nano_story(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("GPT‑5.4 nano", html)
        self.assertIn("The line shows repeated-answer reliability", html)
        self.assertIn('data-story="nano-none-answer"', html)
        self.assertIn('data-story="nano-xhigh-answer"', html)
        self.assertIn('findRow("openai/gpt-5.4-nano", "none")', script)
        self.assertIn('findRow("openai/gpt-5.4-nano", effort)', script)
        self.assertIn('name: "Run cost"', script)
        self.assertIn("yAxisIndex: 1", script)
        self.assertIn("formatCostAxisCompact", script)
        self.assertNotIn("95%+ band", script)
        self.assertNotIn("markArea:", script)
        self.assertNotIn('data-story="nano-minimal-answer"', html)

    def test_history_chart_uses_dual_axis_progression(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "app.js").read_text(encoding="utf-8")
        start = script.index("function renderHistoryChart")
        end = script.find("\n  function ", start + 1)
        block = script[start:] if end == -1 else script[start:end]
        self.assertIn(
            "The line shows answer pass^3; bars show measured run cost.",
            html,
        )
        self.assertIn("GPT‑5.5 was a significant step up in performance", html)
        self.assertIn('type: "category"', block)
        self.assertIn('name: "Run cost"', block)
        self.assertIn('type: "bar"', block)
        self.assertIn("yAxisIndex: 1", block)
        self.assertIn('name: "Answer pass^3"', block)
        self.assertIn("formatter: formatCostAxisCompact", block)
        self.assertIn("formatPct(item.row.answer)", block)
        self.assertNotIn('type: "log"', block)
        self.assertNotIn("inverse: true", block)

    def test_decision_table_uses_short_labels_and_mobile_width_controls(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        script = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn('<th scope="col" title="Model family">Model</th>', html)
        self.assertIn(
            '<th scope="col" title="Minimum reasoning setting">Effort</th>',
            html,
        )
        self.assertIn(
            '<th scope="col" class="numeric" title="Answer pass^3">Pass^3</th>',
            html,
        )
        self.assertIn(
            '<th scope="col" class="numeric" title="Estimated full-run cost">Cost</th>',
            html,
        )
        self.assertIn(
            '<th scope="col" class="numeric" title="Reported reasoning tokens">'
            "Tokens</th>",
            html,
        )
        self.assertIn(
            '<button type="button" data-threshold-weights="open_weights" '
            'aria-label="Open weights">Open</button>',
            html,
        )
        self.assertIn(
            '<button type="button" data-sort="effort_order" '
            'title="Reasoning effort">Effort</button>',
            html,
        )
        self.assertIn(
            '<button type="button" data-sort="answer" '
            'title="Answer pass^3">Pass^3</button>',
            html,
        )
        self.assertIn(
            '<button type="button" data-sort="reasoning_tokens" '
            'title="Reasoning tokens">Tokens</button>',
            html,
        )
        self.assertNotIn("Min. reasoning", html)
        self.assertNotIn("Reasoning toks.", html)
        self.assertIn("scrollbar-color", css)
        self.assertIn(".provider-picker-menu::-webkit-scrollbar-thumb", css)
        self.assertNotIn(".table-scroll::-webkit-scrollbar", css)
        self.assertIn(".decision-table {\n  min-width: 620px;\n  table-layout: fixed;", css)
        self.assertIn(".decision-table { min-width: 400px; font-size: 10.5px; }", css)
        self.assertIn("min-width: 560px;\n    table-layout: fixed;", css)
        self.assertIn(".explorer-table th:nth-child(7)", css)
        self.assertIn(".explorer-table .provider-cell", css)
        self.assertIn(
            ".table-card:not(.explorer-table-card) .table-scroll { max-height: none; }",
            css,
        )
        self.assertIn(".saturation-chip { max-width: 100%; min-width: 0; }", css)
        self.assertIn(".decision-table .model-cell strong", css)
        self.assertIn("function displayCompactEffort", script)
        self.assertIn("function displayThresholdEffort", script)
        self.assertIn('return label === "Default reasoning" ? "Default" : label;', script)
        self.assertIn("compactAvailabilityLabel(row)", script)
        self.assertIn('if (row.availability === "open_weights") return "Open";', script)
        self.assertIn('if (row.availability === "proprietary") return "Closed";', script)
        self.assertIn('title="${escapeHtml(displayEffort(row))}"', script)
        self.assertIn('title="${escapeHtml(row.availability_label)}"', script)

    def test_claude_progression_comparisons_are_wired(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("Minimum reasoning setting", html)
        expected_tabs = (
            "Non-reasoning progression",
            "Reasoning progression",
            "GPT‑5.x family",
            "Claude Opus progress",
            "Claude Sonnet Progress",
            "Claude Haiku Progress",
            "Gemini Flash progression",
        )
        for tab_name in expected_tabs:
            self.assertIn(tab_name, html)
        self.assertLess(
            html.index('data-comparison="o-series"'),
            html.index('data-comparison="gpt5-family"'),
        )
        self.assertLess(
            html.index('data-comparison="haiku"'),
            html.index('data-comparison="gemini"'),
        )
        self.assertNotIn("OpenAI: Non-reasoning progression", html)
        self.assertNotIn("OpenAI: Reasoning progress", html)
        self.assertNotIn("OpenAI without reported reasoning", html)
        for provider in ("openai", "google", "anthropic"):
            self.assertIn(f'data-comparison-provider="{provider}"', html)
        self.assertIn("hydrateComparisonTabs", script)
        self.assertIn("providerIconFor(provider, providerLabel, true)", script)
        for panel_name in ("opus", "sonnet", "haiku"):
            self.assertIn(f'data-comparison="{panel_name}"', html)
            self.assertIn(f'data-comparison-panel="{panel_name}"', html)
        for chart_id in ("opus-chart", "sonnet-chart", "haiku-chart"):
            self.assertIn(f'id="{chart_id}"', html)
            self.assertIn(f'{chart_id}"', script)
        self.assertIn("makeCostPointSizer", script)
        self.assertIn('model: "openai/gpt-5.5"', script)
        self.assertIn("renderClaudeProgressChart", script)
        self.assertIn("renderSonnetChart", script)
        self.assertIn("renderHaikuChart", script)
        self.assertIn('model: "anthropic/claude-sonnet-5"', script)
        self.assertIn(
            "Sonnet 5 performs similarly to 4.6 but at higher costs due to the tokenizer change.",
            html,
        )
        self.assertIn("progressLabelIndexes", script)
        self.assertIn("const costBounds = logCostBounds(allProgressRows, 0.08)", script)
        self.assertIn("labelLayout: { hideOverlap: true, moveOverlap: \"shiftY\" }", script)
        self.assertIn("Cost is reversed on a log scale", html)
        self.assertIn("data-saturation-expand", script)
        roster_start = script.index("function renderSaturationRoster")
        roster_end = script.find("\n  const FRONTIER_VIEWS", roster_start)
        roster_block = script[roster_start:roster_end]
        self.assertLess(
            roster_block.index('{ label: "98%+", test: (value) => value >= 98 }'),
            roster_block.index('{ label: "95–98%", test: (value) => value >= 95 && value < 98 }'),
        )

    def test_story_progression_charts_use_sparse_labels_and_compact_cost_axes(
        self,
    ) -> None:
        script = (ROOT / "app.js").read_text(encoding="utf-8")

        def function_block(name: str) -> str:
            start = script.index(f"function {name}")
            next_function = script.find("\n  function ", start + 1)
            if next_function == -1:
                return script[start:]
            return script[start:next_function]

        for function_name in (
            "renderGeminiChart",
            "renderGPT5FamilyChart",
            "renderOSeriesChart",
            "renderClaudeProgressChart",
        ):
            block = function_block(function_name)
            self.assertIn("progressLabelIndexes", block)
            self.assertIn("progressPoint(row, index, labelIndexes, dataRows)", block)
            self.assertIn("const costBounds = logCostBounds(allProgressRows, 0.08)", block)
            self.assertIn("min: costBounds.min", block)
            self.assertIn("max: costBounds.max", block)
            self.assertIn("formatter: formatCostAxisCompact", block)
            self.assertIn("labelLayout: { hideOverlap: true, moveOverlap: \"shiftY\" }", block)
            self.assertIn("show: false", block)
        self.assertIn("function progressLabelPosition", script)


if __name__ == "__main__":
    unittest.main(verbosity=2)
