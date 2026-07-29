# ObviousBench v0.2 Background And Rhetoric

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-07-28`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


## Core Positioning

ObviousBench is about high-visibility mistakes, not exotic capability. It tests
tasks that should feel mundane: count letters, edit a word, reverse a list,
answer yes or no, choose the object that must be brought to a service, and
follow a simple format instruction.

The public story should be practical: if an AI system is going to face users,
product teams should know whether it is likely to make these obvious mistakes
under the exact model and reasoning setting they plan to ship.

## Messages To Reuse

- Catch obvious AI mistakes before users do.
- Simple tasks are not a full intelligence test, but they are a strong trust
  test.
- A saturatable benchmark can still be useful: the ceiling proves the questions
  are solvable; the spread shows where risk remains.
- Reasoning/test-time compute is often an antidote to these mistakes, but it has
  latency and cost tradeoffs.
- Cost matters: the right product choice is not always the highest-effort row.

## Result Hooks

- GPT-5 nano is the cleanest reasoning-depth story: 37.5% minimal to 97.2% high.
- Top-end saturation is a feature, not a bug: it shows the benchmark is
  measuring avoidable visible failures.
- Gemma 4 is a major value/performance outlier in the positive direction.
- O1 and O3 remain strikingly strong given their release ages, but O1 is
  expensive.
- Grok's no-reasoning rows are weak, while explicit reasoning rows are
  answer-strong but often format-poor.
- Gemini 3.5 Flash low is already near saturated, but its reasoning-token
  telemetry means we should not claim it is no-reasoning.
- Opus version comparisons should be phrased cautiously as this dated snapshot,
  not as a permanent ranking.

## Claims To Avoid

- Do not say ObviousBench ranks all models globally.
- Do not say humans were measured at 100%.
- Do not publish private prompts or raw private completions.
- Do not over-explain failures as a single mechanistic cause.
- Do not imply provider/route-unavailable rows are model-quality failures;
  exclude them from headline comparisons.
- Do not imply low/no-reasoning rows are universally bad models; they are risky
  for this visible-mistake surface under this frozen configuration.
