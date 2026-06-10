---
title: GPT-5.4 Nano 8x28 Pass-k Results
date: 2026-06-06
type: research
status: complete
---

# GPT-5.4 Nano 8x28 Pass-k Results

## Run Contract

- Model: `openai/gpt-5.4-nano`
- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl` (`8x28`, 224 samples)
- Thinking modes: `none`, `low`, `medium`, `high`
- Trials: 5 per mode, 20 entries total
- Raw logs: `results/raw/gpt-5-4-nano-passk-8x28-20260606/`
- Summaries: `results/summaries/gpt-5-4-nano-passk-8x28-20260606/runs/`
- Status ledger: `results/summaries/gpt-5-4-nano-passk-8x28-20260606/status.jsonl`
- Panel: `configs/gpt_5_4_nano_passk_8x28_20260606_panel.yaml`
- Cache busting: run command used `--no-cache --no-skip-completed`; the 20 inspect commands in the status ledger contain no `--cache` flag.

All 20 entries returned `status=passed` and `returncode=0`. Three sample-level provider errors were scored because the run used `--score-on-error`: one each in `none` trial 03, `low` trial 05, and `high` trial 02. The `none` provider error was logged as an `AttemptTimeoutError`; the summary rows classify these as `provider_error=True` and `timeout=False`. Reasoning-enabled runs emitted the provider warning that `temperature` is unsupported for reasoning and is always 1, so only `none` should be interpreted as a true temperature-0 condition.

## Metric Definitions

- `pass^k`: all selected attempts for an item are correct; stricter than pass@k and useful for reliability.
- `pass@k`: at least one selected attempt for an item is correct; useful for best-of-k salvage.
- `pass^3` and `pass@3` below are combination means across all 10 three-trial subsets from the five runs. This avoids arbitrary trial ordering.
- `pass^5` and `pass@5` use all five trials.
- Primary score is `strict_correct`; `answer_correct` is reported separately.

## Strict Score Results

| mode | pass1 | pass^3 | pass@3 | pass^5 | pass@5 | unstable items | pairwise disagreement | trial range | provider errors | cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| none | 80.5% | 79.4% | 81.8% | 79.0% | 82.6% | 3.6% | 1.6% | 1.8% | 1 | $0.0192 |
| low | 87.9% | 82.5% | 93.5% | 80.8% | 95.5% | 14.7% | 7.3% | 3.6% | 1 | $0.0392 |
| medium | 93.0% | 88.3% | 97.1% | 86.2% | 98.2% | 12.1% | 5.8% | 3.6% | 0 | $0.0530 |
| high | 94.3% | 90.4% | 97.4% | 87.9% | 98.2% | 10.3% | 4.6% | 1.8% | 1 | $0.0596 |

## Answer-only Results

| mode | pass1 | pass^3 | pass@3 | pass^5 | pass@5 | unstable items |
|---|---:|---:|---:|---:|---:|---:|
| none | 80.9% | 79.9% | 82.0% | 79.5% | 82.6% | 3.1% |
| low | 88.2% | 83.1% | 93.5% | 81.2% | 95.5% | 14.3% |
| medium | 93.1% | 88.6% | 97.1% | 86.6% | 98.2% | 11.6% |
| high | 94.9% | 91.5% | 97.5% | 89.3% | 98.2% | 8.9% |

## Trial Spread

- `none` strict trial accuracies: 79.5%, 80.8%, 81.2%, 80.4%, 80.8%
- `low` strict trial accuracies: 86.2%, 88.8%, 87.5%, 89.7%, 87.1%
- `medium` strict trial accuracies: 91.5%, 93.3%, 95.1%, 92.9%, 92.4%
- `high` strict trial accuracies: 95.5%, 93.8%, 94.2%, 93.8%, 94.2%

## Interpretation

The pass-k framing does make the benchmark materially more discriminating, but in two different directions:

- `pass@5` inflates scores by asking whether the model ever gets an item right. That is useful for measuring recoverability, but it makes the benchmark easier.
- `pass^5` makes the benchmark much harder by asking whether the model is consistently right. This is the better candidate if the goal is to increase spread among otherwise high-scoring models.
- The gap between `pass@5` and `pass^5` is a compact instability signal. A large gap means many items sit in the model's flaky frontier.

For this run, the strict `pass^5` score is substantially below strict `pass1` in every mode, while strict `pass@5` is above it. That confirms repeated runs reveal a meaningful reliability dimension that single-pass accuracy hides.

Thinking mode improved aggregate strict score monotonically in this run: `none < low < medium < high` for pass1, pass^3, and pass^5. The marginal gain from `medium` to `high` is modest relative to the extra cost and reasoning tokens, though, and `high` still has a large gap between pass@5 and pass^5. The `none` mode is also not directly temperature-comparable to low/medium/high because reasoning modes ignored `temperature=0`.

## Most Unstable Examples

| mode | sample_id | family | strict successes | answer successes | question |
|---|---|---|---:|---:|---|
| high | obviousbench.arith.en.v0.public.000022 | arithmetic | 3/5 | 5/5 | Which is larger, 7.2 or 7.12? |
| high | obviousbench.char_count.en.v0.public.000007 | character_count | 2/5 | 2/5 | How many o's are in google? |
| high | obviousbench.constraint.en.v0.public.000008 | constraint_awareness | 2/5 | 2/5 | The window tinting shop is 100m away. If I want the windows on my car tinted, should I walk there or drive the car there? A. Walk there B. Drive the car there C. Bring only the appointment card D. It is impossible |
| high | obviousbench.constraint.en.v0.public.000034 | constraint_awareness | 3/5 | 3/5 | The jewelry repair kiosk is at the mall entrance. If my necklace clasp is broken, should I wear no necklace or wear or bring the necklace? A. Wear no necklace B. Wear or bring the necklace C. Bring only a receipt D. It is impossible |
| high | obviousbench.ordering.en.v0.public.000017 | ordering | 2/5 | 2/5 | Sort these items alphabetically: cat, car, cap. |
| high | obviousbench.spell.en.v0.public.000019 | spelling_transform | 3/5 | 3/5 | Spell committee backwards. |
| low | obviousbench.arith.en.v0.public.000024 | arithmetic | 3/5 | 5/5 | Convert 3 miles to kilometers using 1 mile = 1.609 km. |
| low | obviousbench.char_count.en.v0.public.000056 | character_count | 2/5 | 2/5 | How many u's are in coconut? |
| low | obviousbench.char_count.en.v0.public.000074 | character_count | 2/5 | 2/5 | How many t's are in alphabetical? |
| low | obviousbench.char_count.en.v0.public.000075 | character_count | 3/5 | 3/5 | How many u's are in successes? |
| low | obviousbench.char_count.en.v0.public.000076 | character_count | 2/5 | 2/5 | How many n's are in rearrangement? |
| low | obviousbench.constraint.en.v0.public.000003 | constraint_awareness | 3/5 | 3/5 | The mechanic is two blocks away. If I want my car's oil changed, should I walk there or drive the car there? A. Walk there B. Drive the car there C. Take the bus there D. It is impossible |

## Family Notes

### none

- `character_count`: 3/28 strict-unstable items; mean strict success rate 0.321.
- `negation`: 3/28 strict-unstable items; mean strict success rate 0.957.
- `spelling_transform`: 2/28 strict-unstable items; mean strict success rate 0.414.
- `arithmetic`: 0/28 strict-unstable items; mean strict success rate 1.000.

### low

- `spelling_transform`: 14/28 strict-unstable items; mean strict success rate 0.714.
- `character_count`: 13/28 strict-unstable items; mean strict success rate 0.621.
- `constraint_awareness`: 4/28 strict-unstable items; mean strict success rate 0.857.
- `arithmetic`: 1/28 strict-unstable items; mean strict success rate 0.986.

### medium

- `spelling_transform`: 12/28 strict-unstable items; mean strict success rate 0.836.
- `character_count`: 9/28 strict-unstable items; mean strict success rate 0.886.
- `constraint_awareness`: 3/28 strict-unstable items; mean strict success rate 0.857.
- `ordering`: 2/28 strict-unstable items; mean strict success rate 0.871.

### high

- `spelling_transform`: 9/28 strict-unstable items; mean strict success rate 0.907.
- `constraint_awareness`: 5/28 strict-unstable items; mean strict success rate 0.850.
- `arithmetic`: 3/28 strict-unstable items; mean strict success rate 0.950.
- `character_count`: 3/28 strict-unstable items; mean strict success rate 0.964.

## Artifacts

- Aggregate metrics CSV: `docs/research/2026-06-06-gpt-5-4-nano-8x28-passk-results.csv`
- Item instability CSV: `docs/research/2026-06-06-gpt-5-4-nano-8x28-passk-item-instability.csv`
- Cost estimate prepared before the run: `docs/research/2026-06-06-gpt-5-4-nano-8x28-passk-cost-estimate.md`
- Run plan: `docs/research/2026-06-06-gpt-5-4-nano-8x28-passk-run-plan.md`

## Recommendation

Adopt pass-k reporting as a second axis rather than replacing pass1. For leaderboard-style hardness, report `pass^5` or `pass^3` beside pass1. For debugging and item mining, report `pass@5 - pass^5` and keep the item instability CSV, because those identify questions whose score depends on sampling or provider variance.
