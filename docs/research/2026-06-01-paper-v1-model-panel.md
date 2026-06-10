---
title: Paper V1 Model Panel
date: 2026-06-01
type: research
status: draft
---

# Paper V1 Model Panel

Canonical config:

- `configs/paper_v1_model_panel.yaml`

Status: planned, not run.

Smoke status:

- `docs/research/2026-06-01-paper-v1-smoke-status.md`

Run freeze policy:

- `docs/research/2026-06-01-paper-v1-run-freeze-policy.md`

Dry-run cost estimates:

- `docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md`
- `docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.csv`

This panel freezes the intended paper sweep surface without launching expensive
model calls. It is derived from `configs/model_registry_v1.yaml`, which was
generated on 2026-06-01 from OpenRouter model metadata and `runcost` default
price cards, plus direct-provider entries used by the repo's existing model
registry work.

## Selection Rationale

The paper panel is intentionally smaller than the broad registry. It should be
large enough to support a serious report, but small enough that the final sweep
can be audited and repeated.

It includes:

- direct OpenAI, Anthropic, Gemini, and Grok baselines,
- cheaper or smaller direct-provider variants where available,
- free or cheap OpenRouter models representing small/open-weight families,
- deterministic generation settings where supported: `temperature=0` and a high
  output safety cap (`max_tokens=10000`, except providers with a lower
  advertised completion ceiling).

It intentionally excludes:

- the 227-entry broad thinking/settings sweep,
- image/audio/embedding endpoints,
- exploratory model aliases that have not been promoted into the paper panel,
- expensive frontier duplicates that do not add a clear comparison role.

## Preconditions Before Running

Do not run the final paper panel until:

1. `make -C paper readiness-preprint` passes for the fast-preprint path.
2. The one-sample smoke ledger passes or an explicit waiver is recorded.
3. The aliases and prices in `configs/paper_v1_model_panel.yaml` are refreshed
   or re-verified against provider docs or live metadata.
4. The expected cost is accepted.
5. The final output directory and report naming convention are frozen.

The strict benchmark path still requires `make -C paper readiness` and real
human-baseline rows before reporting human accuracy, response time, or
model-versus-human gaps. The fast-preprint path does not require human rows as
long as those claims are omitted.

## Coverage Caveat

The 12-entry panel is a small paper/draft panel. It is not the intended
hundreds-of-configurations benchmark. For the broader run, use
`configs/model_thinking_settings_v1.yaml`, then reconcile the missing current
models listed in `docs/research/2026-06-01-model-coverage-refresh.md`.

## Reporting Policy

The paper should report each model with:

- provider route,
- exact Inspect model string,
- generation settings,
- run date,
- scored sample count,
- provider errors or exclusions,
- answer, format, and strict accuracy,
- confidence intervals,
- token and cost estimates.

Provider exclusions are an audit artifact unless the manuscript re-adds an
explicit provider-exclusions table. They should not appear as Table 4 in the
current simplified paper shape.

The model-panel table generated into `paper/tables/model_panel.tex` is a
planning table. It is not evidence that the final sweep has been run.

The cost-estimate artifacts are also planning artifacts. They use local usage
and price-card estimation paths and do not prove final billed costs.
