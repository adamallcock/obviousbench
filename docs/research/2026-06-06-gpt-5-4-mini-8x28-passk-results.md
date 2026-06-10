---
title: GPT-5.4 Mini 8x28 Pass-k Results
date: 2026-06-06
type: research
status: complete
---

# GPT-5.4 Mini 8x28 Pass-k Results

## Run Contract

- Model: `openai/gpt-5.4-mini`
- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl` (`8x28`, 224 samples)
- Thinking modes: `none`, `low`, `medium`, `high`
- Trials: 5 per mode, 20 entries total
- Raw logs: `results/raw/gpt-5-4-mini-passk-8x28-20260606/`
- Summaries: `results/summaries/gpt-5-4-mini-passk-8x28-20260606/runs/`
- Status ledger: `results/summaries/gpt-5-4-mini-passk-8x28-20260606/status.jsonl`
- Panel: `configs/gpt_5_4_mini_passk_8x28_20260606_panel.yaml`
- Cache busting: run command used `--no-cache --no-skip-completed`; the 20 inspect commands in the status ledger contain no `--cache` flag.
- Concurrency: each Inspect eval used `--max-connections=128`.

All 20 entries returned `status=passed` and `returncode=0`. Provider-error samples were scored because the run used `--score-on-error`: low trial 5 obviousbench.negation.en.v0.public.000007 (negation, provider_error, provider_error=True, timeout=False); medium trial 3 obviousbench.arith.en.v0.public.000010 (arithmetic, provider_error, provider_error=True, timeout=False); medium trial 1 obviousbench.spell.en.v0.public.000028 (spelling_transform, provider_error, provider_error=True, timeout=False); medium trial 3 obviousbench.word_count.en.v0.public.000070 (word_count, provider_error, provider_error=True, timeout=False); high trial 2 obviousbench.char_count.en.v0.public.000068 (character_count, provider_error, provider_error=True, timeout=False); high trial 1 obviousbench.spell.en.v0.public.000030 (spelling_transform, provider_error, provider_error=True, timeout=False); high trial 4 obviousbench.word_count.en.v0.public.000007 (word_count, provider_error, provider_error=True, timeout=False)

Reasoning-enabled runs emitted the provider warning that `temperature` is unsupported for reasoning and is always 1, so only `none` should be interpreted as a true temperature-0 condition.

## Metric Definitions

- `pass^k`: all selected attempts for an item are correct; stricter than pass@k and useful for reliability.
- `pass@k`: at least one selected attempt for an item is correct; useful for best-of-k salvage.
- `pass^3` and `pass@3` below are combination means across all 10 three-trial subsets from the five runs.
- `pass^5` and `pass@5` use all five trials.
- Primary score is `strict_correct`; `answer_correct` is reported separately.

## Strict Score Results

| mode | pass1 | pass^3 | pass@3 | pass^5 | pass@5 | unstable items | pairwise disagreement | trial range | provider errors | cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| none | 86.1% | 84.2% | 88.3% | 83.9% | 89.3% | 5.4% | 2.8% | 2.2% | 0 | $0.0702 |
| low | 96.3% | 92.7% | 99.3% | 90.6% | 100.0% | 9.4% | 4.4% | 1.8% | 1 | $0.1967 |
| medium | 96.4% | 93.6% | 98.4% | 91.5% | 98.7% | 7.1% | 3.2% | 1.8% | 3 | $0.2643 |
| high | 97.0% | 94.9% | 98.4% | 93.3% | 98.7% | 5.4% | 2.3% | 1.3% | 3 | $0.3590 |

## Answer-only Results

| mode | pass1 | pass^3 | pass@3 | pass^5 | pass@5 | unstable items |
|---|---:|---:|---:|---:|---:|---:|
| none | 86.1% | 84.2% | 88.3% | 83.9% | 89.3% | 5.4% |
| low | 96.3% | 92.7% | 99.3% | 90.6% | 100.0% | 9.4% |
| medium | 96.4% | 93.6% | 98.4% | 91.5% | 98.7% | 7.1% |
| high | 97.0% | 94.9% | 98.4% | 93.3% | 98.7% | 5.4% |

## Trial Spread

- `none` strict trial accuracies: 86.6%, 87.1%, 84.8%, 85.3%, 86.6%
- `low` strict trial accuracies: 96.9%, 95.5%, 96.4%, 97.3%, 95.5%
- `medium` strict trial accuracies: 96.4%, 97.3%, 96.0%, 96.9%, 95.5%
- `high` strict trial accuracies: 97.3%, 96.0%, 97.3%, 97.3%, 96.9%

## Interpretation

The mini run repeats the same core pattern as nano: `pass@5` raises the score by measuring whether at least one attempt succeeds, while `pass^5` lowers the score by measuring whether all five attempts succeed. The gap between those two columns is the useful instability signal.

For leaderboard hardness, `pass^5` or `pass^3` is the stronger candidate than `pass@k`. For debugging, `pass@5 - pass^5` points directly at flaky items that should be inspected or mined for families.

The raised 128-way sample concurrency reduced the fast portion of each batch, but high-concurrency reasoning runs still had slow tail calls and occasional scored provider errors. This is useful operationally: very high concurrency helps wall clock, but it also seems to expose tail/retry behavior that should be tracked alongside scores.

## Most Unstable Examples

| mode | sample_id | family | strict successes | answer successes | question |
|---|---|---|---:|---:|---|
| high | obviousbench.spell.en.v0.public.000002 | spelling_transform | 2/5 | 2/5 | Write strawberry without the letter e. |
| high | obviousbench.spell.en.v0.public.000006 | spelling_transform | 2/5 | 2/5 | Replace every a in necessary with @. |
| low | obviousbench.char_count.en.v0.public.000030 | character_count | 2/5 | 2/5 | How many h's are in alphabetical? |
| low | obviousbench.constraint.en.v0.public.000010 | constraint_awareness | 3/5 | 3/5 | The motorcycle mechanic is one block away. If my motorcycle needs an oil change, should I walk there or ride the motorcycle there?  A. Walk there B. Ride the motorcycle there C. Take a bus D. It is impossible |
| low | obviousbench.spell.en.v0.public.000002 | spelling_transform | 3/5 | 3/5 | Write strawberry without the letter e. |
| low | obviousbench.spell.en.v0.public.000007 | spelling_transform | 2/5 | 2/5 | Spell sentence backwards. |
| low | obviousbench.spell.en.v0.public.000018 | spelling_transform | 2/5 | 2/5 | Replace every a in orange with @. |
| low | obviousbench.spell.en.v0.public.000029 | spelling_transform | 2/5 | 2/5 | Replace every a in reliability with @. |
| low | obviousbench.spell.en.v0.public.000033 | spelling_transform | 3/5 | 3/5 | Spell cabinet backwards. |
| medium | obviousbench.char_count.en.v0.public.000010 | character_count | 3/5 | 3/5 | How many l's are in google? |
| medium | obviousbench.char_count.en.v0.public.000030 | character_count | 3/5 | 3/5 | How many h's are in alphabetical? |
| medium | obviousbench.spell.en.v0.public.000002 | spelling_transform | 2/5 | 2/5 | Write strawberry without the letter e. |

## Family Notes

### none

- `character_count`: 6/28 strict-unstable items; mean strict success rate 0.379.
- `spelling_transform`: 4/28 strict-unstable items; mean strict success rate 0.736.
- `constraint_awareness`: 2/28 strict-unstable items; mean strict success rate 0.771.
- `arithmetic`: 0/28 strict-unstable items; mean strict success rate 1.000.

### low

- `character_count`: 8/28 strict-unstable items; mean strict success rate 0.907.
- `spelling_transform`: 7/28 strict-unstable items; mean strict success rate 0.871.
- `constraint_awareness`: 5/28 strict-unstable items; mean strict success rate 0.936.
- `negation`: 1/28 strict-unstable items; mean strict success rate 0.993.

### medium

- `character_count`: 7/28 strict-unstable items; mean strict success rate 0.936.
- `spelling_transform`: 6/28 strict-unstable items; mean strict success rate 0.871.
- `arithmetic`: 1/28 strict-unstable items; mean strict success rate 0.993.
- `constraint_awareness`: 1/28 strict-unstable items; mean strict success rate 0.921.

### high

- `character_count`: 5/28 strict-unstable items; mean strict success rate 0.964.
- `spelling_transform`: 5/28 strict-unstable items; mean strict success rate 0.879.
- `constraint_awareness`: 1/28 strict-unstable items; mean strict success rate 0.921.
- `word_count`: 1/28 strict-unstable items; mean strict success rate 0.993.

## Artifacts

- Aggregate metrics CSV: `docs/research/2026-06-06-gpt-5-4-mini-8x28-passk-results.csv`
- Item instability CSV: `docs/research/2026-06-06-gpt-5-4-mini-8x28-passk-item-instability.csv`
- Cost estimate prepared before the run: `docs/research/2026-06-06-gpt-5-4-mini-8x28-passk-cost-estimate.md`
- Run plan: `docs/research/2026-06-06-gpt-5-4-mini-8x28-passk-run-plan.md`
