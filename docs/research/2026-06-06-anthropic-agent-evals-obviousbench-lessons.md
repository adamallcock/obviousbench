---
title: Anthropic Agent Evals ObviousBench Lessons
date: 2026-06-06
type: research
status: complete
---

# Anthropic Agent Evals ObviousBench Lessons

## Source

Primary source: [Anthropic, "Demystifying evals for AI agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), published January 9, 2026.

Related metric source named by Anthropic: [tau-bench arXiv:2406.12045](https://arxiv.org/abs/2406.12045), which introduced `pass^k` for repeated-trial agent reliability.

## Executive Decision

ObviousBench should add `pass^k` as a secondary reliability lens, not as a
replacement for the current single-trial leaderboard and not as an artificial
"hardness" knob on cached historical runs.

The strongest version is:

1. Keep the main score as `answer_accuracy`, `strict_accuracy`, and obvious
   failure rate on a frozen item set.
2. Add a separate reliability track that runs the same frozen item set `k`
   independent times with cache disabled.
3. Report `pass^k`, `pass@k`, and per-item disagreement for `answer_correct`
   and `strict_correct`.
4. Treat post-hoc repeated-run analysis from existing artifacts as exploratory
   only unless the trials are fresh, same-settings, same-dataset, same-scorer,
   and preselected before looking at outcomes.

This is worth doing because ObviousBench's premise is not merely "can a model
get the answer once?" The premise is "users expect obvious questions to work
every time." That aligns more naturally with `pass^k` than with `pass@k`.

However, the existing local evidence does not prove that `pass^2` materially
increases spread. It makes the benchmark slightly harder in absolute score, but
on the clean five-model 8x28 repeat set the spread is roughly unchanged. Larger
item sets, harder item selection, and reliability-track repeats are complementary
tools, not substitutes.

## Anthropic Lessons That Transfer

### Capability vs Regression Suites

Anthropic separates capability evals from regression evals. Capability evals
should start below saturation and give the team room to climb. Regression evals
should be near 100% and protect against backsliding.

For ObviousBench, this maps cleanly:

- `public_v0`, smoke, and small stable barrages are useful as regression/dev
  surfaces.
- `hard_obvious_8x28` is closer to a capability slice because it was selected
  to expose differences among strong models.
- Future claim-bearing releases should avoid mixing these purposes in one table.
  A saturated 8x10 leaderboard can still be valuable as a regression table, but
  it is weaker as a frontier capability comparison.

### Non-Determinism Is Signal

Anthropic's `pass@k` / `pass^k` distinction is directly relevant. `pass@k`
answers "does at least one attempt work?" `pass^k` answers "do all attempts
work?" ObviousBench should care more about the latter because the benchmark is
about obvious reliability in public-facing systems.

Important implication: repeated trials are not noise to average away. They are
evidence of item-level instability. A model that alternates between correct and
wrong answers on "obvious" questions is different from one with the same mean
accuracy but stable failures on a fixed subset of items.

### Outcome-First Grading

Anthropic warns against over-constraining the path an agent takes. ObviousBench
already does well here because it grades deterministic final outcomes rather
than requiring a reasoning trace or tool-call path. For this repo, the action is
mostly defensive: keep grading the final answer contract, and avoid adding
reasoning-style requirements unless the task family explicitly asks for them.

### Read Transcripts, Especially Surprising Failures

Anthropic emphasizes transcript review because scores alone do not reveal
whether a task, grader, harness, or model caused the failure. In ObviousBench
terms, the equivalent is reading the saved completions/failure galleries and
checking item cards when a frontier model "fails" a human-trivial task.

This reinforces the existing wrong-answer review and item-card direction. A
future reliability report should include a "flaky items" table: items that pass
in one trial and fail in another, with the exact outputs linked or excerpted.

### Harness Isolation

Anthropic calls out trial isolation and shared-state/caching hazards. This is
especially important here because the repo's panel runner defaults to Inspect's
repo-local cache with a long expiry. That is good for development and rescoring,
but cached repeat runs are not independent trials.

For any `pass^k` claim:

- Use `--no-cache`.
- Use a fresh raw root per trial.
- Record the exact generation settings in `status.jsonl`.
- Keep the dataset, scorer revision, prompt policy, and provider route frozen.
- Decide the trial count before looking at outcomes.

### Hard Enough, But Not Broken

Anthropic frames saturation as a maintenance problem: a capability eval at 100%
stops revealing improvement. The repo's own 8x28 pilot already supports that
lesson. The jump from 8x10 to 8x28 uncovered additional top-model failures and
narrowed confidence intervals.

The danger is overcorrecting into ambiguous or brittle tasks. ObviousBench should
continue to prefer human-trivial, deterministic, reviewed items over adversarial
trick prompts. Harder should mean "more coverage of real obvious failure modes,"
not "more obscure instructions."

## Existing Post-Hoc `pass^2` Check

I checked existing local artifacts to see whether we could estimate `pass^k`
without new provider calls.

The cleanest available evidence is a five-model 8x28 repeat set. The second
trial is the no-cache telemetry rerun:

- `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/`

The first trial is the earlier matching 8x28 result:

- Four models: `results/summaries/paper-v1-8x28-pilot-20260602/runs/`
- Gemini 3.1 Flash-Lite: `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/`

The matched item set is `hard_obvious_8x28_seed_20260531` with 224 items. The
calculation treats each item as one task and each run as one trial.

Definitions used:

- `mean pass^1`: mean per-trial success over the two runs.
- `pass@2`: item succeeded in at least one of the two runs.
- `pass^2`: item succeeded in both runs.
- `disagreement`: item outcome changed between the two runs.

### Answer-Correct Reliability

| Model/config | Trial 1 | Trial 2 | Mean pass^1 | pass@2 | pass^2 | Disagreement |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MiniMax M3 | 97.8% | 96.9% | 97.3% | 99.1% | 95.5% | 3.6% |
| DeepSeek V4 Flash | 92.4% | 95.5% | 94.0% | 97.3% | 90.6% | 6.7% |
| Gemini 3.1 Flash-Lite | 90.2% | 90.2% | 90.2% | 90.2% | 90.2% | 0.0% |
| Gemma 3 27B | 81.2% | 80.8% | 81.0% | 82.1% | 79.9% | 2.2% |
| Qwen3 Coder Flash | 67.0% | 67.4% | 67.2% | 69.2% | 65.2% | 4.0% |

### Strict-Correct Reliability

| Model/config | Trial 1 | Trial 2 | Mean pass^1 | pass@2 | pass^2 | Disagreement |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MiniMax M3 | 97.8% | 96.9% | 97.3% | 99.1% | 95.5% | 3.6% |
| DeepSeek V4 Flash | 90.6% | 93.8% | 92.2% | 96.9% | 87.5% | 9.4% |
| Gemini 3.1 Flash-Lite | 90.2% | 90.2% | 90.2% | 90.2% | 90.2% | 0.0% |
| Gemma 3 27B | 68.3% | 68.3% | 68.3% | 69.2% | 67.4% | 1.8% |
| Qwen3 Coder Flash | 57.1% | 57.1% | 57.1% | 59.4% | 54.9% | 4.5% |

### What Changed?

`pass^2` makes scores lower, as expected. The largest strict-correct drop from
mean pass^1 to pass^2 is DeepSeek V4 Flash: 92.2% to 87.5%, driven by 21/224
strict disagreements. MiniMax drops from 97.3% to 95.5%. Gemini 3.1 Flash-Lite
is unchanged because the two runs produced identical item outcomes.

Spread did not materially increase in this five-model slice:

| Metric | Range | Population stdev |
| --- | ---: | ---: |
| Answer trial-1 accuracy | 30.8 pp | 10.78 |
| Answer mean pass^1 | 30.1 pp | 10.84 |
| Answer pass^2 | 30.4 pp | 10.82 |
| Strict trial-1 accuracy | 40.6 pp | 15.42 |
| Strict mean pass^1 | 40.2 pp | 15.53 |
| Strict pass^2 | 40.6 pp | 15.40 |

So: `pass^2` is a better reliability measure, but this post-hoc sample does not
show it as a stronger spread amplifier than the existing 8x28 expansion.

## Why Not Just Reuse All Historical Reruns?

A broader scan found many repeated-looking summary rows, but most are not valid
independent trials:

- Some are comparison-folder copies of the same summary.
- Some are rescored from the same raw logs.
- Some are cached runs under the same Inspect cache key.
- Some are one-sample smoke runs.
- Some are targeted repair runs after provider errors or telemetry issues.
- Some differ in generation settings that are not fully encoded by
  `usage_by_sample.csv`, especially around Anthropic adaptive thinking.

For reliability claims, status-led provenance matters. The key should come from
`status.jsonl` and the raw-root/generation-config record, not just from summary
CSV columns.

## Recommendation

### Add A Reliability Track

Add a separate report mode, probably named `reliability_k2` before going higher:

- Dataset: start with `hard_obvious_8x28_seed_20260531`.
- Trial count: `k=2` first, then `k=3` only if the cost is acceptable.
- Cache: disabled.
- Prompt/scorer/model settings: frozen.
- Output columns: `answer_pass@k`, `answer_pass^k`, `strict_pass@k`,
  `strict_pass^k`, `answer_disagreement_rate`, `strict_disagreement_rate`,
  `provider_error_any_trial`, and `provider_error_all_trials`.

For the paper/report, present it as an exploratory reliability section, not as
the main leaderboard, until the run protocol is pre-registered and repeated
across a broad enough model panel.

### Keep 8x28 As The Main Near-Term Hardness Move

The existing evidence still favors larger/harder item slices as the primary
way to reduce saturation and improve confidence intervals. `pass^k` adds a
different question: reliability under repeated attempts. It should sit next to
the 8x28 result, not replace it.

### Use `strict_correct` For Reliability Claims

For user-facing "obvious reliability," `strict_correct` is the sharper metric.
`answer_correct` is useful for capability because it separates knowledge/task
success from format discipline. `strict_pass^k` captures the product promise:
the model gives the right answer in the requested shape every time.

### Add A Flakiness View

The most actionable output from a pass^k run is not only the model ranking. It
is a per-item instability report:

- Items passed by all models in all trials can graduate toward regression.
- Items failed by all strong models need task/grader review.
- Items with high disagreement identify nondeterministic failure modes worth
  reading manually.

This would make the reliability track useful even before it becomes a polished
leaderboard metric.

## Implementation Sketch

The smallest clean implementation is not to alter scoring. Instead, build an
aggregator over existing `usage_by_sample.csv` files selected by a manifest:

```text
trial_group_id,label,model,trial_index,summary_dir
minimax-m3-8x28-k2,MiniMax M3,openrouter/minimax/minimax-m3,1,results/summaries/.../trial1
minimax-m3-8x28-k2,MiniMax M3,openrouter/minimax/minimax-m3,2,results/summaries/.../trial2
```

The aggregator should:

1. Validate that all trial rows for a group share identical sample IDs.
2. Validate that model/settings/dataset/scorer metadata match, using
   `status.jsonl` when available.
3. Compute item-level vectors for answer and strict outcomes.
4. Emit `reliability_comparison.csv` and `reliability_by_item.csv`.
5. Refuse to rank groups with fewer than `k` complete trials.

Do not infer independent trials from duplicated summary folders. The manifest
should name exactly which summaries are trial 1, trial 2, and so on.

## Bottom Line

Anthropic's post is highly relevant, but the main lesson is not "make the
benchmark harder by exponentiating scores." The better lesson is:

- Use harder/larger item sets to fight saturation.
- Use `pass^k` to measure reliability on repeated attempts.
- Use `pass@k` only when "one good attempt is enough," which is usually not the
  ObviousBench product story.
- Treat cached or post-hoc duplicates as debugging evidence, not leaderboard
  evidence.

My recommendation: add a `k=2` reliability report as the next metric experiment,
grounded in fresh cache-disabled repeats. It should likely increase credibility
more than it increases spread.
