# ObviousBench v0.2 Background And Rhetoric

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-06-18`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


## Core Positioning

ObviousBench is about high-visibility mistakes, not exotic
capability. It tests tasks that should feel mundane: count letters,
edit a word, reverse a list, answer yes or no, choose the object that
must be brought to a service.

The public story should be practical: if an AI system is going to
face users, product teams should know whether it is likely to make
these obvious mistakes under the exact model and thinking setting
they plan to ship.

## Tone

- Serious, but not scolding.
- Concrete, not abstract benchmark theater.
- Useful to product and model teams.
- Explicit that top models can solve the benchmark.
- Clear that lower rows reveal tradeoffs, not moral failure.

## Messages To Reuse

- Catch obvious AI mistakes before users do.
- Simple tasks are not a full intelligence test, but they are a
  strong trust test.
- A saturatable benchmark can still be useful: the ceiling proves the
  questions are solvable; the spread shows where risk remains.
- Thinking/test-time compute is often an antidote to these mistakes,
  but it has latency and cost tradeoffs.
- ObviousBench separates answer correctness from format compliance.

## Claims To Avoid

- Do not say ObviousBench ranks all models globally.
- Do not say humans were measured at 100%.
- Do not publish private prompts or raw private completions.
- Do not over-explain failures as a single mechanistic cause.
- Do not imply provider/route-unavailable rows are model-quality
  failures; exclude them from headline comparisons.
