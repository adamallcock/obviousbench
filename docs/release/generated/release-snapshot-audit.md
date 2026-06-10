---
title: ObviousBench Release Snapshot Audit
date: 2026-06-03
type: audit
status: pass
---

# ObviousBench Release Snapshot Audit

Config: `configs/release_v0_1_0.yaml`
Overall status: PASS

Passed: 16
Warnings: 0
Failures: 0

| Check | Status | Evidence | Next action |
| --- | --- | --- | --- |
| release config | PASS | present: configs/release_v0_1_0.yaml | None. |
| snapshot manifest | PASS | present: results/summaries/paper-v1-8x28-current-223-final-20260603/manifest.csv | None. |
| snapshot comparison directory | PASS | present: results/summaries/paper-v1-8x28-current-223-final-20260603/comparison | None. |
| snapshot report directory | PASS | present: docs/reports/2026-06-03-paper-v1-8x28-current-223-final | None. |
| paper manifest | PASS | present: data/splits/paper_v1_manifest.jsonl | None. |
| theme config | PASS | present: configs/release_theme_v0_1_0.yaml | None. |
| surfaces config | PASS | present: configs/release_surfaces_v0_1_0.yaml | None. |
| effort cost report directory | PASS | present: docs/reports/2026-06-02-effort-cost-curves | None. |
| effort cost points CSV | PASS | present: docs/reports/2026-06-02-effort-cost-curves/effort-cost-curve-points.csv | None. |
| effort cost missing points CSV | PASS | present: docs/reports/2026-06-02-effort-cost-curves/effort-cost-curve-missing-points.csv | None. |
| manifest row count | PASS | 223 model/settings rows match expected count | None. |
| comparison contract | PASS | 223 rows, 224 samples, profile hard_obvious_8x28_seed_20260531 | None. |
| report contract | PASS | report files present; leaderboard has 223 rows | None. |
| effort cost contract | PASS | 31 effort points present; no missing requested points | None. |
| stale release references | PASS | checked 6 path(s) for 9 forbidden string(s) | None. |
| evidence bundle contract | PASS | 9 generated evidence files present; 5 status labels; 224 matrix rows | None. |
