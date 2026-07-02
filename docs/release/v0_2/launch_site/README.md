# ObviousBench v0.2 launch site

A complete static launch page that interleaves the ObviousBench essay with the evidence it describes. It is deliberately structured as a release story rather than a dashboard: the hero defines the benchmark compactly, the aggregate frontier and reliability thresholds come first, the one-model proof and saturation framing follow, and the full explorer stays last.

## Included deliverables

- `index.html` — semantic page structure and launch prose.
- `styles.css` — responsive editorial layout, tab/table states, print styles, and accessibility treatment.
- `app.js` — all chart generation, narrative-number binding, tabs, decision table, explorer filters, and sorting.
- `data/results.js` — generated, browser-ready aggregate data.
- `data/build.js` — generated release metadata and source checksum.
- `data/summary.csv` — canonical numerical source used by the build.
- `data/row-metadata.json` — presentation metadata kept separate from benchmark numbers.
- `data/provider-icons.js` — provider marks used in tables.
- `vendor/echarts.min.js` — vendored Apache ECharts runtime; no CDN is required.
- `dist/obviousbench-v0.2-launch.html` — fully self-contained single-file build.
- `build_site.py` — regenerates data files and the standalone artifact.
- `test_site.py` — release-data and artifact smoke tests.

## Run locally

From this directory:

```bash
python -m http.server 8000
```

Open `http://localhost:8000/`.

The single-file build can also be opened directly:

```text
dist/obviousbench-v0.2-launch.html
```

## Rebuild from a new aggregate CSV

Replace `data/summary.csv`, then run:

```bash
python build_site.py
python test_site.py
```

Or point the builder at another CSV:

```bash
python build_site.py --summary /path/to/summary.csv
```

The builder treats the CSV as the sole numerical source of truth. Existing page metadata can label and classify rows, but it cannot overwrite score, cost, or token values.

## Release invariants enforced by the build

The build fails when:

- aggregate row IDs are duplicated;
- a required narrative row is missing;
- configurations disagree on the benchmark item count;
- the core GPT‑5 nano, Gemma, Gemini, Grok, o1, or o3 story rows disappear.

All prose numbers are populated in the browser from `data/results.js`; none of the headline result percentages are hardcoded in the essay HTML.

## Page architecture

1. Hero with compact release snapshot, benchmark scope, task examples, and pass^3 definition.
2. Aggregate cost–reliability frontier with curated views.
3. 90% / 95% / 99% reliability-threshold decision table.
4. GPT‑5 nano connected-dot result as a one-model proof.
5. Saturation-as-design evidence with representative high-band model families.
6. Supporting comparison stories: OpenAI history, GPT‑5 family, Gemini Flash, o1/o3 cost, and Claude snapshots.
7. Full aggregate data explorer over public-surface aggregate rows.

## Data and interpretation choices

- The main frontier uses every `surface_included` aggregate row; written
  rollups and threshold/story tables use `narrative_included !== false`.
- Diagnostic duplicate/accounting rows are excluded from the public browser payload.
- The main scatter reverses the logarithmic cost axis: cheaper is right, more reliable is up.
- Pareto rows are configurations for which no cheaper row has an equal or better answer score.
- Threshold tables choose the cheapest qualifying row per model family.
- Open-weight API cost is shown as a route/pricing snapshot, not self-hosting total cost of ownership.
- “No reported reasoning” is a telemetry label, not a claim about internal computation.

## Deployment

The modular site can be served from any static host. Preserve these relative paths:

```text
index.html
styles.css
app.js
data/*
vendor/*
```

For a single-file publication pipeline, deploy `dist/obviousbench-v0.2-launch.html`.
