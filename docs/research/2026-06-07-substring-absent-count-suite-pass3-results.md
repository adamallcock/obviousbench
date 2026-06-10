---
title: Substring Absent Count Suite Pass3 Results
date: 2026-06-07
type: research
status: complete
---

# Substring Absent Count Suite Pass3 Results

## Context

The new category targets "double cross" substring-count failures: questions ask
how many members of an explicit finite collection contain an exact letter
sequence, often where the answer is zero despite a semantic or visual lure.
The motivating screenshot asked how many days of the week include `"toe"`; the
correct answer is `0`.

I used the requested ChatGPT Pro consult through the visible ChatGPT web UI.
The thread initially returned short planning-preface text, then after the
requested wait completed with full suite-design guidance. I treated that output
as design input rather than verified truth.

The Pro guidance that shaped this run:

- Use explicit finite collections as the source of truth.
- Define matching as case-insensitive contiguous substring containment.
- Keep a zero-heavy suite, but include positive controls so "always answer 0"
  is not a viable strategy.
- Tag lure categories and item metadata so later reports can slice by zero
  target, positive controls, semantic lures, and public seed examples.
- Track pass^3, pass@3, majority pass, instability, and zero-vs-positive
  behavior.

## Suite

- Dataset: `data/experiments/2026-06-07-substring-absent-count-suite.jsonl`
- Generator: `scripts/build_substring_absent_count_suite.py`
- Items: 80
- Zero-target absent-substring traps: 64
- Positive controls: 16
- Matching rule: contiguous substring, case-insensitive, no rewriting collection
  members.
- Prompt form: "Return only the final answer, with no explanation."

The suite is intentionally larger than the 10-item smoke while still small
enough for fast repeated paid runs. Pro recommended scaling the release-grade
category to around 160 items with dev/test/challenge splits; this 80-item suite
is the first inclusion candidate and immediate model-stress run.

## Run Contract

- Model: `openai/gpt-5.4-nano`
- Thinking modes: `none`, `low`, `medium`
- Trials: 3 per mode
- Attempts: 720 total
- Panel: `configs/2026-06-07-substring-absent-count-suite-gpt-5-4-nano-pass3-panel.yaml`
- Raw logs: `results/raw/substring-absent-count-suite-gpt-5-4-nano-pass3-20260607/`
- Summaries: `results/summaries/substring-absent-count-suite-gpt-5-4-nano-pass3-20260607/runs/`
- Status ledger: `results/summaries/substring-absent-count-suite-gpt-5-4-nano-pass3-20260607/status.jsonl`
- Cache policy: provider run used `--no-cache --no-skip-completed`.

Commands:

```bash
.venv/bin/python scripts/build_substring_absent_count_suite.py
.venv/bin/python scripts/validate_dataset.py data/experiments/2026-06-07-substring-absent-count-suite.jsonl
.venv/bin/python scripts/run_model_panel.py \
  --panel configs/2026-06-07-substring-absent-count-suite-gpt-5-4-nano-pass3-panel.yaml \
  --dataset data/experiments/2026-06-07-substring-absent-count-suite.jsonl \
  --raw-root results/raw/substring-absent-count-suite-gpt-5-4-nano-pass3-20260607 \
  --summary-root results/summaries/substring-absent-count-suite-gpt-5-4-nano-pass3-20260607/runs \
  --manifest-out results/summaries/substring-absent-count-suite-gpt-5-4-nano-pass3-20260607/manifest.csv \
  --status-out results/summaries/substring-absent-count-suite-gpt-5-4-nano-pass3-20260607/status.jsonl \
  --mode full \
  --no-cache \
  --no-skip-completed \
  --cost runcost
```

## Results

Primary score is `answer_correct`. `strict_correct` was identical in this run.

| mode | pass1 | all-item pass^3 | pass@3 | majority pass | unstable items | zero-item pass^3 | positive-control pass^3 | provider errors | cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| none | 87.9% | 87.5% | 88.8% | 87.5% | 1 | 92.2% | 68.8% | 0 | $0.0039 |
| low | 97.9% | 95.0% | 100.0% | 98.8% | 4 | 96.9% | 87.5% | 1 | $0.0207 |
| medium | 99.6% | 98.8% | 100.0% | 100.0% | 1 | 98.4% | 100.0% | 0 | $0.0275 |

`all-item pass^3` is computed over all 80 suite items. `zero-item pass^3`
is computed only over the 64 zero-target traps, while `positive-control pass^3`
is computed only over the 16 positive controls. This is why the no-thinking
zero-item pass^3 can be higher than all-item pass^3: the positive controls
dragged the all-item score down. In counts, no-thinking got 59/64 zero items
correct on all three trials, but only 11/16 positive controls correct on all
three trials, for 70/80 all-item pass^3.

`pass@3` is the complementary reliability metric: an item passes if any of the
three trials got it right. It can therefore be 100.0% even when pass^3 is lower.

The `low` provider error was a scored sample error on
`obviousbench.char_count.en.v0.private.100046`, logged by Inspect as
`RetryError(... AttemptTimeoutError ...)`. The summary reports it as
`provider_error=True` and `timeout=False`.

## Failure Pattern

No-thinking failed nine items on every trial and one item on two of three
trials. The hardest stable failures were a mix of false nonzero zero-target
answers and missed positive controls:

- `100015`: secondary colors + `"cat"`, target `0`, no-thinking `0/3`.
- `100028`: US bill value names + `"cat"`, target `0`, no-thinking `0/3`.
- `100035`: punctuation names + `"cat"`, target `0`, no-thinking `0/3`.
- `100041`: Boolean words + `"cat"`, target `0`, no-thinking `0/3`.
- `100069`: season names + `"mer"`, target `1`, no-thinking `0/3`.
- `100072`: NATO alphabet words + `"x"`, target `1`, no-thinking `0/3`.
- `100073`: shape names + `"angle"`, target `2`, no-thinking `0/3`.
- `100075`: Greek letter names + `"eta"`, target `4`, no-thinking `0/3`.
- `100080`: tool names + `"saw"`, target `1`, no-thinking `0/3`.

The recurring `"cat"` zero-target failures are especially relevant to this
category: the model often appears to count semantic or component-letter overlap
instead of exact contiguous substring containment.

Low reasoning fixed most of the stable no-thinking misses, but introduced four
unstable items: `100012`, `100046`, `100068`, and `100075`. Medium reasoning
left only `100012` unstable: "How many of these letters from a to f contain the
exact letter sequence `"cat"`: a, b, c, d, e, f?"

## Artifacts

- Aggregate metrics CSV:
  `docs/research/2026-06-07-substring-absent-count-suite-gpt-5-4-nano-pass3-results.csv`
- Item instability CSV:
  `docs/research/2026-06-07-substring-absent-count-suite-gpt-5-4-nano-pass3-item-instability.csv`
- Failure-attempt CSV:
  `docs/research/2026-06-07-substring-absent-count-suite-gpt-5-4-nano-pass3-failures.csv`

## Recommendation

Keep this category. It catches a qualitatively different failure mode from
ordinary character counting: the model must respect a negative exact-substring
condition over a listed collection, and smaller/no-thinking settings still
confidently invent counts.

Follow-up: the category was expanded into the 160-item release-candidate split
in `docs/research/2026-06-07-substring-absent-count-release-160-pass3-results.md`.
That corpus tags the known public `days_toe` seed as calibration-only and keeps
private-eval claims separate from `dev_calibration`.
