---
title: ObviousBench Figure And Table Guidelines
date: 2026-06-02
type: research
status: draft
---

# ObviousBench Figure And Table Guidelines

## Scope

This note evaluates the current ObviousBench paper figures and tables against research-paper visualization and table guidance, with the specific goal of improving the first arXiv draft. It owns recommendations only. It does not edit paper source, generators, data, or tests.

Inspected local artifacts:

- `paper/main.pdf`
- `paper/figures/leaderboard.pdf`
- `paper/figures/family_heatmap.pdf`
- `paper/figures/answer_format_gap.pdf`
- `paper/figures/cost_frontier.pdf`
- `paper/tables/main_results.tex`
- `paper/tables/family_results.tex`
- `paper/tables/thinking_group_results.tex`
- `paper/tables/model_family_results.tex`
- `paper/tables/failure_type_summary.tex`
- `paper/tables/model_panel.tex`
- `docs/reports/2026-06-02-paper-v1-combined-234-overline/report.html`
- `docs/reports/2026-06-02-paper-v1-combined-234-overline/leaderboard.csv`
- `docs/reports/2026-06-02-paper-v1-combined-234-overline/family-heatmap.csv`
- `docs/reports/2026-06-02-paper-v1-combined-234-overline/wrong-answer-review.csv`

## Executive Summary

The paper needs a figure/table redesign, not just styling polish. The current tables are structurally close to publishable LaTeX tables, but the main visual strategy over-indexes on top-ranked rows and undersells the most interesting 234-setting story: many settings saturate the 80-item score, while the useful signal is in family-specific brittleness, strict-compliance gaps, provider/settings clusters, cost/token burden, and lower-tail failures.

One immediate technical risk also showed up: the standalone generated figure PDFs currently render as placeholders. `pdftotext` on the figure PDFs returns only:

- `leaderboard.pdf`: "Leaderboard / No result rows available yet."
- `family_heatmap.pdf`: "Family heatmap / No family result rows available yet."
- `answer_format_gap.pdf`: "Answer/format gap / No result rows available yet."
- `cost_frontier.pdf`: "Cost frontier / No cost result rows available yet."

Rendered via Poppler at 200 DPI, those standalone files show only a hairline and otherwise blank white pages. `paper/main.pdf` contains a fuller embedded visualization snapshot, so the PDF and figure files are out of sync. Before design changes, make the asset build deterministic and add a smoke check that fails if any paper figure contains placeholder text.

Highest-priority replacements:

1. Replace Figure 1 with a compact distribution-plus-highlight figure rather than a top-12 saturated leaderboard.
2. Replace Figure 2 with a model-family/task-family summary that uses all 234 settings, not sampled rows.
3. Keep Figure 3 conceptually, but redesign it as a compliance diagnostic with example failure classes and a clear denominator.
4. Replace Figure 4 with a true Pareto frontier plot, faceted or annotated by provider/family, with frontier membership and cost buckets.
5. Replace Table 2's top-12-only view with a ranked excerpt plus distribution counts and an explicit pointer to a full appendix/CSV.
6. Keep Table 3, but add per-family failure rows, median/dispersion across models, and optionally a small adjacent visual.
7. Move the 234-setting full table to an appendix longtable or external CSV/HTML, while giving the main paper curated slices: top frontier, bottom tail, per-family worst cases, and setting sweeps.

## Source-Backed Guidelines

### Figure Legibility And Submission Fitness

ACL formatting guidance says table and figure text should use document-sized fonts when possible and be clearly readable when printed; it warns that abused small figure/table text can cause desk rejection. ACL also recommends vector formats such as PDF/EPS and checking legibility in print and PDF viewers. Source: [ACL paper formatting guidelines](https://acl-org.github.io/ACLPUB/formatting.html).

IEEE's figure/table guidance recommends consistent font type, font size, label style, spacing, symbol definitions, and graphics style, with about 9-10 point graphics text. Source: [Proceedings of the IEEE guidelines for figures and tables](https://proceedingsoftheieee.ieee.org/resources/guidelines-for-figures-and-tables/).

Nature final-submission guidance is stricter than arXiv but useful as a quality bar: do not rasterize line art or text where possible, use vector artwork for graphs, and check that lettering and line weights remain readable at final reduced size. Source: [Nature final submission guidance](https://www.nature.com/nature/for-authors/final-submission).

arXiv's TeX submission documentation puts responsibility on authors to verify the processed PDF and figure conversions. It accepts PDF/PNG/JPG figures in PDFLaTeX mode, recommends `graphicx`, and says authors must examine converted figures because conversion can change scientific meaning. Source: [arXiv Submit TeX/LaTeX](https://info.arxiv.org/help/submit_tex.html).

Implication for ObviousBench:

- Generate final-size vector PDFs from the actual CSV source.
- Enforce non-placeholder text, embedded fonts, legible labels, and visible marks in CI or a paper asset smoke.
- Stop relying on `paper/main.pdf` as evidence that current standalone figure files are valid.

### Accessibility And Color

NeurIPS accessibility guidance recommends high-contrast figures, color-accessible palettes, not relying on color alone, and figure fonts no smaller than figure caption text. It also calls out embedded fonts, figure alt text, and marked table headers. Source: [NeurIPS author accessibility guidance](https://neurips.cc/Conferences/2021/PaperInformation/Author-Guidelines).

ACM figure-description guidance distinguishes figure descriptions from captions and says descriptions should convey important information not already in caption or main text. Source: [ACM describing figures](https://authors.acm.org/proceedings/production-information/describing-figures).

ColorBrewer distinguishes sequential, diverging, and qualitative schemes. Sequential schemes fit ordered low-to-high data; diverging schemes need a meaningful middle break; qualitative schemes fit nominal categories and should not imply magnitude. Source: [ColorBrewer scheme guidance](https://colorbrewer2.org/learnmore/schemes_full.html). ColorBrewer also exposes filters for colorblind-safe, print-friendly, and photocopy-safe palettes. Source: [ColorBrewer 2.0](https://colorbrewer2.org/).

W3C contrast guidance uses 4.5:1 for ordinary text and emphasizes light-dark contrast because hue and saturation do not ensure legibility for color-vision-deficient readers. Source: [W3C WCAG contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

Implication for ObviousBench:

- Use color as a secondary channel. Pair color with markers, labels, grouping, or direct annotations.
- For heatmaps, use a sequential palette for accuracy and avoid red/green categorical bins unless the bins are also labeled.
- Use provider colors only for discrete provider identity; use shape or label style for route/setting differences.
- Add caption/description text that states the actual takeaway, not just "X versus Y."

### Scientific Visualization Principles

Rougier, Droettboom, and Bourne's "Ten Simple Rules for Better Figures" is still a useful paper-level checklist: do not trust defaults, use color intentionally, avoid misleading rescaling, use simple plot types that convey the message, and avoid chartjunk. The paper explicitly warns that numeric values should be provided elsewhere or clearly on the figure when important. Source: [PLOS Computational Biology, Ten Simple Rules for Better Figures](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833).

Implication for ObviousBench:

- Avoid charts whose only visible result is "many rows are 100%."
- If truncating axes, make the truncation visually obvious and explain why. For the main score, an axis from 85% to 100% can help separate leaders but can also exaggerate tiny differences on an 80-item split.
- Pair headline figures with complete data tables or CSV/HTML so exact values are available elsewhere.
- Prefer a smaller number of multi-purpose figures that each answer a research question.

### Tables

The `booktabs` package documentation is explicit: avoid vertical rules and double rules in formal tables. Source: [booktabs documentation](https://tug.org/docs/latex/booktabs/booktabs.pdf).

W3C table guidance says tables need structural markup that links header and data cells; relying on visual cues alone is an accessibility barrier. Source: [W3C tables tutorial](https://www.w3.org/WAI/tutorials/tables/).

APA-style guidance, while not an ML venue rule, matches scientific-table norms: use tables/figures only when they assist communication, make them intelligible without the text, do not duplicate the same data, define abbreviations, and avoid vertical borders. Source: [Purdue OWL APA tables and figures](https://owl.purdue.edu/owl/research_and_citation/apa_style/apa_formatting_and_style_guide/apa_tables_and_figures.html).

Implication for ObviousBench:

- The current generated tables already use `booktabs`-style rules and no vertical bars, which is good.
- The table issue is not typography first. It is selection strategy, long labels, repeated columns, and insufficient disclosure of the full 234-setting panel.
- Main-paper tables should summarize evidence; appendix/external tables should provide exhaustive rows.

### Benchmark-Paper Examples

HELM is relevant because it argues for dense, standardized, multi-metric model evaluation and releases raw prompts/completions and a living benchmark site. It also exposes results through an interactive result surface with multiple plot options rather than trying to fit the full evaluation into one static table. Sources: [HELM arXiv abstract](https://arxiv.org/abs/2211.09110), [HELM result surface](https://nlp.stanford.edu/helm/instruction-pilot_six_scenarios/?plots=1).

MMLU-Pro is a useful static-paper precedent: its paper table shows a subset of frontier models and representative domains due to space constraints, then points readers to a full leaderboard. Source: [MMLU-Pro NeurIPS paper](https://papers.nips.cc/paper_files/paper/2024/file/ad236edc564f3e3156e1b2feafb99a24-Paper-Datasets_and_Benchmarks_Track.pdf).

Implication for ObviousBench:

- It is acceptable for the main paper to show slices, not all 234 rows, if the slice criteria are principled and the full data are linked in an appendix/CSV/HTML.
- The static paper should explain the compression policy: "main figures show distributions and representative/frontier slices; complete rows are in Appendix/Table CSV/report HTML."
- Interactive HTML is an excellent supplement for 234 settings, but the static paper still needs complete enough evidence to be read offline.

## Local Artifact Evaluation

### Figure Asset Integrity

Current standalone figure PDFs are not usable as paper figures. They contain placeholder messages and render visually blank aside from a horizontal rule. This conflicts with the current `paper/main.pdf`, which contains fuller figure text in its embedded pages. Treat this as a build reproducibility issue.

Recommended gate:

- `pdftotext paper/figures/*.pdf -` must not contain `No result rows available yet`, `No family result rows available yet`, or `No cost result rows available yet`.
- Render each figure to PNG with Poppler and verify non-white pixel count above a low threshold.
- Verify each figure has at least one title, axis label, and data mark or table cell label in extracted text.

### Figure 1: Leaderboard

Current main-PDF version:

- Shows top 12 rows by answer correctness.
- All visible rows are 100.0%.
- Uses horizontal Wilson CI whiskers on a truncated 85%-100% x-axis.
- Labels are truncated, so readers cannot identify several models without Table 2.

Strengths:

- Directly states the headline metric.
- Uses Wilson intervals, which is statistically appropriate for an 80-item split.
- Keeps strict compliance separate.

Problems:

- The chart communicates saturation more than ranking. With 24 perfect settings and 77 settings at 95% or higher, a top-12-only plot hides the real distribution.
- Ranking rows with identical 100% answer correctness by cost/tokens is not visually obvious.
- Truncated labels reduce inspectability.
- The truncated axis may overemphasize minor differences if non-perfect rows are shown later.

Recommended replacement:

Use a two-panel Figure 1:

- Panel A: distribution of answer correctness across all 234 settings, preferably a histogram or beeswarm/strip plot grouped by route/provider. Add reference bands for 100%, >=95%, 80%-95%, and <80%. Annotate counts: 24 perfect, 77 at >=95%, 45 below 80%.
- Panel B: highlighted frontier/top slice: show only representative top rows selected by distinct claim value, such as cheapest perfect setting, lowest-token perfect setting, highest-cost perfect setting, best direct-provider setting, best OpenRouter-routed setting, and selected near-perfect cheaper settings.

Alternative if limited to one panel:

- Use a ranked dot plot of all 234 settings with y-axis as rank and x-axis as answer correctness, but label only breakpoints and highlighted models. Add shaded bands for 100%, 95%-100%, 80%-95%, <80%.

Implementation tasks:

- Build `paper/figures/score_distribution.pdf`.
- Add a selection table or annotation data file for highlighted labels.
- Keep `leaderboard.csv` as the exact-value source.
- Caption should state the saturation result and why the figure uses all 234 settings.

Priority: P0.

### Figure 2: Family Heatmap

Current main-PDF version:

- Shows only eight sampled model rows against eight task families.
- Samples high-, middle-, and low-scoring rows.
- Includes values in cells and coarse bins.

Strengths:

- Family columns are the right abstraction for ObviousBench.
- It exposes the real family signal: character counting and spelling are the weak points.

Problems:

- A handful of rows cannot support claims about 234 settings.
- Mixed sampling makes the visual easy to misread as representative or exhaustive.
- Several rows are perfect, creating large uniform blocks.
- Binned legend loses detail while numeric cell labels clutter the chart.
- Because the figure is called a "family heatmap," readers expect a comprehensive model-family/task-family view, not a manually sampled display.

Recommended replacement:

Use all 234 settings, but aggregate to avoid unreadable rows:

- Main-paper Figure 2 should be a model-family x task-family heatmap, where rows are provider/model families or route groups and columns are task families. Cell value should be median answer correctness across settings in that group, with an optional small text label for `median% (n settings)`.
- Add a second small panel showing per-task-family distribution across settings as box/violin/ridgeline strips. This makes char-count and spelling brittleness visible without listing every model.
- Sort task-family columns by aggregate difficulty: char count, spelling, constraints, arithmetic, ordering, negation, word count, format, or whatever the data currently supports.
- Sort row groups by overall median accuracy, with broad route/provider grouping preserved.

Appendix companion:

- Full 234 x 8 heatmap as a landscape appendix page or external HTML. Use clustering within provider/family groups, not arbitrary top/mid/low sampling. If static, omit numeric cell labels and include only row labels for group boundaries or selected models.

Implementation tasks:

- Derive provider/model-family groups from existing labels/model IDs.
- Compute per-group median, interquartile range, and n settings per task family.
- Generate `paper/figures/family_summary_heatmap.pdf`.
- Generate `paper/figures/task_family_distributions.pdf` if using a two-panel figure.

Priority: P0.

### Figure 3: Strict-Compliance Gap

Current main-PDF version:

- Horizontal bars show largest answer-minus-strict and format-minus-strict gaps for selected models.
- This is the most conceptually useful current figure because it separates "knows the answer" from "follows the requested interface."

Strengths:

- Directly supports a distinctive ObviousBench claim: answer correctness and strict interface compliance are different diagnostics.
- Bars are readable and sorted.
- It helps explain why strict should not be the headline score.

Problems:

- The denominator and selection policy are not visible enough.
- Model labels are truncated.
- It does not show whether gaps are caused by verbosity, JSON shape, case/normalization, or format-only failures.
- "format minus strict" can confuse readers unless the exact scoring hierarchy is repeated nearby.

Recommended replacement:

Keep the figure but redesign as:

- Left panel: sorted gap bars for top 10-12 gap rows, using full readable labels or numbered labels with a companion mini-table.
- Right panel: stacked bar of gap causes across all rows, using wrong-answer review tags where available: verbose noncompliance, malformed JSON, extra text, case/normalization, non-answer, etc.
- Add visible formulas: `answer gap = answer accuracy - strict accuracy`; `format gap = format accuracy - strict accuracy`.
- Add n and selection rule in caption: "Top complete 80-item rows by answer-strict gap; provider-error rows excluded" or similar.

Implementation tasks:

- Generate a small `strict_gap_examples.csv` with selected labels and gap components.
- Map review tags into 4-6 cause buckets, not every raw failure type.
- Use color only for gap type; use direct labels at bar ends.

Priority: P1.

### Figure 4: Cost/Accuracy Scatter

Current main-PDF version:

- Scatter of answer correctness vs estimated 80-item run cost on log x-axis.
- Shows mostly unlabeled gray dots and one label near the bottom.
- Does not draw or label the Pareto frontier despite the paper needing cost/accuracy tradeoff evidence.

Strengths:

- Cost/accuracy is the right question because many rows tie on accuracy.
- Log cost is appropriate because costs span orders of magnitude.

Problems:

- As criticized, it is simplistic: one undifferentiated cloud with minimal interpretation.
- No frontier line, no frontier points, no provider/family encoding, no uncertainty, and no special treatment of perfect-score rows.
- Provider errors and incomplete rows can distort low-accuracy/zero-cost regions if not excluded or marked.
- It does not answer the practical question: which settings are dominated, and which are cheap enough to matter?

Recommended replacement:

Use a true Pareto frontier:

- X-axis: estimated USD for the 80-item run, log scale.
- Y-axis: answer correctness.
- Mark every complete row as a small low-alpha point.
- Color by route/provider group or broad family; shape by setting type: provider default, explicit thinking, model-named thinking, special-purpose/guard.
- Draw the Pareto frontier: rows not dominated by any cheaper-or-equal and higher-or-equal accuracy setting.
- Label only frontier points plus a few high-cost dominated exemplars.
- Add horizontal bands at 80%, 95%, and 100%.
- Optionally add marginal rug or density on cost to show clustering.

If the paper wants a stronger efficiency claim, use a two-panel Figure 4:

- Panel A: accuracy vs cost frontier.
- Panel B: accuracy vs tokens-per-correct or reasoning tokens per visible token for thinking settings.

Implementation tasks:

- Compute `is_pareto_frontier` using answer accuracy and estimated cost among complete 80-item rows.
- Exclude or separately mark rows with provider errors/timeouts.
- Add hover/interactive detail only in HTML; keep static labels sparse.
- Caption should state pricing vintage and that cost estimates are snapshot assumptions.

Priority: P0.

### Table 2: Main Results

Current table:

- Shows 12 of 234 model rows.
- Ranks by answer correctness, then cost per correct answer and tokens per correct answer.
- All visible rows are 100% answer correctness.
- Long model labels are truncated with ellipses.

Strengths:

- Uses a clean `booktabs` table with no vertical rules.
- Includes N, answer, CI, format, strict, tokens/correct, and USD/correct.
- Includes source note and "Showing 12 of 234" disclosure.

Problems:

- The table mostly repeats Figure 1 and does not reveal the breadth of the 234-setting run.
- Top-12-only selection hides lower-tail and family-specific failure behavior.
- Truncated labels weaken reproducibility.
- It omits route/provider, generation setting class, provider errors, and full run cost, all of which matter for interpreting model settings.

Recommended replacement:

Use a main-results table with principled slices rather than only top 12:

- Section 1: "Perfect answer rows, cheapest first" - top 5 by cost/correct among 100% rows.
- Section 2: "Near-perfect low-cost rows" - top 3-5 rows under a cost threshold or frontier rows below 100%.
- Section 3: "High-accuracy but strict-gap rows" - 2-3 rows with large answer-strict gaps.
- Section 4: "Lower-tail examples" - 2-3 rows illustrating common failure modes, not to shame models but to expose benchmark signal.

Columns:

- Model setting
- Route/provider
- Setting class
- Answer correct
- Strict
- 95% CI
- Cost/correct
- Tokens/correct
- Provider errors

Appendix:

- Full 234-row table as a landscape `longtable` or `supertabular` with compact labels, or as a CSV plus an appendix manifest summary. For arXiv readability, the full table should be searchable text, not a screenshot.

Priority: P0.

### Table 3: Family Results

Current table:

- Aggregates across families with N, answer correct, CI, format, strict, and cost.
- Correctly surfaces char count and spelling as hardest families.

Strengths:

- Probably the strongest current table.
- Compact, readable, and directly tied to the paper's key empirical claim.
- Uses aggregate denominators and Wilson intervals.

Problems:

- Cost by family is less interpretable than error counts and model dispersion.
- It lacks per-family model-level spread, so readers cannot see whether failures are universal or concentrated in weak rows.
- It separates from Figure 2 when the two should reinforce the same family-brittleness story.

Recommended replacement:

Keep a family table, but revise columns:

- Family
- Items
- Attempts/scored rows
- Answer correct
- 95% CI
- Median model-setting accuracy
- IQR or 10th-90th percentile across settings
- Strict gap
- Most common failure tag

Move cost to the cost/efficiency figure or an appendix unless there is a specific cost-by-family claim.

Priority: P1.

### Appendix Model Panel And Large Table Strategy

Current model panel table:

- Summarizes route, setting count, unique model IDs, and manifest path.
- It is concise and useful, but it is not a full model panel.

Problem:

- The paper says it evaluated 234 model settings and 189 unique model IDs, but the appendix table does not let a reader audit those settings without opening the manifest CSV.

Recommended strategy for 234 settings:

Use three layers.

Layer 1: Main paper:

- Distribution figures and curated slice tables.
- No full 234-row wall in the main text.
- Explain the compression policy explicitly.

Layer 2: Appendix:

- A route/provider/model-family summary table.
- A compact full model-setting table, ideally landscape and split across pages:
  - rank
  - display label
  - model ID
  - route/provider
  - setting class
  - answer correct
  - strict
  - provider errors
  - cost/correct
  - tokens/correct
  - summary directory or manifest row ID
- Optional per-family appendix heatmap or per-family top/bottom tables.

Layer 3: External reproducibility artifacts:

- CSV files for all 234 rows.
- HTML report with sortable/filterable table and interactive plots.
- Exact manifest path and report path in the paper.

This mirrors the MMLU-Pro pattern: representative results in the paper, full leaderboard elsewhere, while keeping enough static appendix detail for offline review.

Priority: P0.

## Recommended Figure Set For The Next Paper Draft

### Figure 1: Score Distribution And Saturation

Question answered: how broad is performance across 234 settings?

Recommended form:

- Histogram/beeswarm of answer correctness across all settings.
- Group or color by route/provider.
- Annotate 24 perfect rows, 77 >=95%, 45 below 80%.
- Add small frontier/top highlights only if space allows.

Why it is better:

- It makes the "small benchmark but broad panel" result visible.
- It avoids pretending the top 12 perfect rows are meaningfully separated by answer accuracy.

### Figure 2: Family Brittleness Across The Full Panel

Question answered: which obvious-task families still break models?

Recommended form:

- Provider/model-family x task-family heatmap using all settings after aggregation.
- Adjacent distribution plot by task family.
- Sequential palette from low to high answer correctness.

Why it is better:

- It replaces the sampled heatmap with a full-panel family-level view.
- It directly supports the character-count/spelling hotspot claim.

### Figure 3: Answer Versus Interface Compliance

Question answered: how often do models know the answer but fail the requested interface?

Recommended form:

- Gap bars plus cause buckets from review tags.
- Clear formulas and denominators.
- Sparse labels and a companion mini-table if labels are long.

Why it is better:

- It preserves the most distinctive current diagnostic but makes it causally interpretable.

### Figure 4: Cost/Accuracy Pareto Frontier

Question answered: which settings are efficient, and which are dominated?

Recommended form:

- Log-cost scatter, frontier line, frontier labels, provider/route encoding, 80/95/100 bands.
- Exclude incomplete/provider-error rows or mark them separately.

Why it is better:

- It turns the current simple scatter into a model-selection figure.
- It handles many 100% rows by shifting attention to cost and domination.

### Optional Figure 5 Or Appendix Figure: Thinking/Token Burden

Question answered: when thinking settings help, what do they cost?

Recommended form:

- Slopegraph or connected dot plot for models with multiple thinking settings.
- X-axis: thinking level/budget; y-axis: answer correctness, with token/cost annotations.
- Facet by model family for OpenAI, Gemini, Claude, Qwen where settings are comparable.

Why it is useful:

- The current paper already has thinking-group tables, but the more interesting story is within-model setting sweeps rather than sample-weighted broad groups.

## Table Strategy

### Main Tables

Use no more than three main result tables:

1. Table 2: curated model-setting result slices.
2. Table 3: family-level aggregate plus dispersion and failure-tag summaries.
3. Optional Table 4: thinking/setting summary only if the paper makes thinking-cost claims.

Avoid making both Figure 1 and Table 2 show the same top 12 perfect rows. One should show the distribution; the other should show representative exact values.

### Appendix Tables

Recommended appendix tables:

- Full 234 model settings, split across pages or linked as CSV/HTML.
- Route/provider/model-family summary.
- Per-task-family top/bottom table, especially for char count and spelling.
- Strict-gap detail table.
- Provider-error/incomplete rows table.

### Table Formatting Rules

- Keep `booktabs`; do not add vertical rules.
- Use `siunitx`-style numeric alignment if available.
- Define all abbreviations in captions or notes: N, CI, Fmt., Strict, Tok./correct, USD/correct.
- Avoid ellipsized model labels in final source. Use short display labels plus a model ID column or appendix mapping.
- Put source/run-vintage notes in captions or table notes, not as a full-width row that visually competes with data.
- Right-align numeric columns; left-align labels.
- Use no more precision than the sample supports: one decimal point for percentages is enough for 80-item rows; costs can use compact scientific/decimal notation as currently done.

## Representing 234 Model Settings Without Hiding Too Much

The paper should not force all 234 rows into one main figure or one main table. It should expose the full-panel shape while preserving exact auditability.

Recommended static-paper mix:

- Distribution plot: all 234 rows.
- Aggregated family heatmap: all 234 rows summarized by provider/model-family.
- Pareto frontier: all complete rows, labels only on frontier/highlighted rows.
- Curated table: 12-18 rows selected by explicit rules.
- Appendix full table: all 234 rows.

Recommended external supplement:

- Keep `report.html` as the interactive full surface.
- Add or preserve sortable CSV downloads.
- Make the paper cite exact artifact paths, run date, pricing vintage, and manifest.

Specific visual forms considered:

- Full 234-row table in main text: reject. It is unreadable and duplicates CSV.
- Full 234 x 8 heatmap in main text: reject unless rendered as an appendix landscape figure with clustering and no cell labels.
- Top/bottom/sliced tables: use, but define slice rules.
- Small multiples: use for thinking/setting sweeps and provider-family comparisons.
- Distribution plots: use for Figure 1 and family dispersion.
- Provider/model-family faceting: use for family heatmap and cost frontier.
- Rank plots: useful if all 234 are shown with sparse labels.
- Pareto frontier plots: required for cost/accuracy.
- Slopegraphs: useful for within-model thinking/effort settings.
- Violin/box/histograms: useful for family distributions; box/strip is safer than violin when group counts are small or uneven.
- Interactive website: use as supplement, not as replacement for static evidence.

## Priority Order

P0:

1. Fix paper figure asset integrity so standalone `paper/figures/*.pdf` are not placeholders and match `paper/main.pdf`.
2. Replace Figure 1 with an all-234 score distribution plus highlighted saturated/top/frontier examples.
3. Replace Figure 2 with a full-panel aggregated family-brittleness visualization.
4. Replace Figure 4 with a true Pareto frontier and clear provider/route/setting encoding.
5. Redesign Table 2 as curated slices plus a pointer to the full 234-row appendix/CSV.
6. Add a full appendix model-setting table or an explicit static appendix summary plus exact CSV/HTML path.

P1:

7. Redesign Figure 3 to include gap causes and formulas.
8. Revise Table 3 to include model-setting dispersion and common failure tags by family.
9. Add a provider-error/incomplete-row appendix table so failed/incomplete rows do not pollute visual interpretation.
10. Add figure/table accessibility checks: no color-only distinctions, readable text at final size, alt/description text where the venue/toolchain supports it.

P2:

11. Add optional thinking-setting slopegraphs for models with comparable setting sweeps.
12. Standardize figure captions into conclusion-style captions: first sentence states the takeaway; second sentence defines metric/denominator.
13. Add source-data notes under each figure naming the CSV/report artifact used.

## Suggested Implementation Tasks

1. Add a paper-asset smoke test:
   - Render all paper figures with `pdftoppm`.
   - Fail on placeholder text.
   - Fail on near-blank PNG output.
   - Fail when extracted text lacks expected title/axis/data labels.

2. Build a `paper/assets/figure_source_manifest.json` or similar:
   - figure ID
   - source CSV path
   - run/report ID
   - generated file path
   - generation timestamp
   - expected row count

3. Add derived CSVs for static figures:
   - `score_distribution.csv`
   - `family_group_summary.csv`
   - `strict_gap_summary.csv`
   - `cost_pareto_frontier.csv`
   - `main_results_slices.csv`

4. Implement new figures in `scripts/build_paper_assets.py`:
   - Use fixed final figure sizes.
   - Use consistent fonts and line weights.
   - Use `matplotlib`/LaTeX PDF output or another vector path that preserves text.
   - Keep labels sparse; use direct labels only for highlighted rows.

5. Update tests after implementation:
   - Check non-placeholder figure text.
   - Check frontier labels/classes in generated PDF/SVG text where feasible.
   - Check Table 2 slice rules.
   - Check full model panel row count equals 234 for this run.

6. Update paper captions and text after figures exist:
   - Make each caption state the paper claim it supports.
   - Add static-to-interactive handoff text: "Complete model-setting rows are in Appendix X and `docs/reports/.../leaderboard.csv`; interactive sorting/filtering is in `report.html`."

## Open Questions And Risks

- The current standalone paper figure PDFs are placeholders while `paper/main.pdf` has fuller embedded figures. The next implementation pass should first determine whether this is stale build output, wrong source directory, or generator fallback behavior.
- Model grouping rules need a durable taxonomy. Provider route, model family, and setting type are all useful, but mixing them ad hoc will make figures unstable.
- Pricing/cost figures require a pricing vintage. Free/promotional/OpenRouter-routed costs can be misleading if treated as stable market facts.
- The 80-item split creates wide Wilson intervals near the top. The visual design should not imply that 100.0%, 98.8%, and 97.5% rows are strongly separated without more data.
- Special-purpose guard/safety rows and incomplete provider-error rows should be excluded from some plots or clearly marked; otherwise they can distort low-end distributions.
- If the final arXiv paper uses a venue style later, figure sizes and font sizes may need to be rechecked at that actual final layout.
