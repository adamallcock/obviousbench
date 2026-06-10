---
title: Substring Absent Count Smoke Results
date: 2026-06-07
type: research
status: complete
---

# Substring Absent Count Smoke Results

## Purpose

This smoke run tests the "absent substring count" failure mode surfaced by the
user-provided Google AI Overview examples: ask how many items in a familiar set
contain a word or sequence that is not present in any item. All ten hand-authored
items have target `0`.

## Artifacts

- Dataset: `data/experiments/2026-06-07-substring-absent-count.jsonl`
- Panel config: `configs/2026-06-07-substring-absent-count-panel.yaml`
- GPT-5.4 size panel config: `configs/2026-06-07-substring-absent-count-gpt-5-4-size-correction-panel.yaml`
- Manifest: `results/summaries/substring-absent-count-20260607/manifest.csv`
- Status ledger: `results/summaries/substring-absent-count-20260607/status.jsonl`
- Per-run summaries: `results/summaries/substring-absent-count-20260607/runs/`
- Raw Inspect logs: `results/raw/substring-absent-count-20260607/`
- GPT-5.4 size summaries: `results/summaries/substring-absent-count-gpt-5-4-correction-20260607/`

## Dataset

The ten prompts cover days, months, planets, rainbow colors, seasons, number
words, cardinal directions, NATO alphabet words, shapes, and chemical elements.
Each uses the existing `character_count` family with subfamily
`substring_absent_count`, private split `private_v0`, scorer
`exact_integer_extract_first_v0`, and answer type `integer`.

Validation command:

```bash
.venv/bin/python scripts/validate_dataset.py \
  data/experiments/2026-06-07-substring-absent-count.jsonl
```

Result: validation passed after fixing the experimental item IDs to use the
existing `char_count` family short name.

## Run

Panel entries:

- OpenAI `openai/gpt-5.5`: none, low, medium
- Google `google/gemini-3.1-flash-lite`: minimal, low, medium, high

Run command, with secrets omitted:

```bash
OPENAI_API_KEY=... GOOGLE_API_KEY=... \
.venv/bin/python scripts/run_model_panel.py \
  --panel configs/2026-06-07-substring-absent-count-panel.yaml \
  --dataset data/experiments/2026-06-07-substring-absent-count.jsonl \
  --raw-root results/raw/substring-absent-count-20260607 \
  --summary-root results/summaries/substring-absent-count-20260607/runs \
  --manifest-out results/summaries/substring-absent-count-20260607/manifest.csv \
  --status-out results/summaries/substring-absent-count-20260607/status.jsonl \
  --mode full \
  --no-cache \
  --no-skip-completed \
  --cost runcost
```

The panel runner completed with exit code 0. `--score-on-error` was enabled, so
provider-error samples are counted as scored failures in the generated summary
CSV files. They should not be interpreted as model answer attempts.

The repo cost estimator was not used for a pre-run total because
`scripts/estimate_paper_model_panel_costs.py` only accepts named barrage
profiles such as `balanced_8x10` or `hard_obvious_8x10`, not this custom
10-item experiment. Post-run costs below come from `runcost`.

## Results

Primary metric is `answer_correct` out of 10.

| entry | model | thinking | answer correct | provider errors | cost | input tokens | output tokens | reasoning tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt-5-5-none` | `openai/gpt-5.5` | none | 8/10 | 0 | $0.003405 | 381 | 50 | 0 |
| `gpt-5-5-low` | `openai/gpt-5.5` | low | 10/10 | 0 | $0.034695 | 381 | 1093 | 1023 |
| `gpt-5-5-medium` | `openai/gpt-5.5` | medium | 10/10 | 0 | $0.046005 | 381 | 1470 | 1400 |
| `gemini-3-1-flash-lite-minimal` | `google/gemini-3.1-flash-lite` | minimal | 9/10 | 0 | $0.000100 | 341 | 10 | 0 |
| `gemini-3-1-flash-lite-low` | `google/gemini-3.1-flash-lite` | low | 9/10 | 0 | $0.001918 | 341 | 10 | 1212 |
| `gemini-3-1-flash-lite-medium` | `google/gemini-3.1-flash-lite` | medium | 10/10 | 0 | $0.005967 | 341 | 9 | 3912 |
| `gemini-3-1-flash-lite-high` | `google/gemini-3.1-flash-lite` | high | 10/10 | 0 | $0.010563 | 341 | 10 | 6975 |

## GPT-5.4 Size Run

A second panel ran GPT-5.4 nano and GPT-5.4 mini at none, low, and medium
thinking on the same 10-item dataset. It did not rerun GPT-5.5 base or Gemini.

GPT-5.4 size run command, with secrets omitted:

```bash
OPENAI_API_KEY=... \
.venv/bin/python scripts/run_model_panel.py \
  --panel configs/2026-06-07-substring-absent-count-gpt-5-4-size-correction-panel.yaml \
  --dataset data/experiments/2026-06-07-substring-absent-count.jsonl \
  --raw-root results/raw/substring-absent-count-gpt-5-4-correction-20260607 \
  --summary-root results/summaries/substring-absent-count-gpt-5-4-correction-20260607/runs \
  --manifest-out results/summaries/substring-absent-count-gpt-5-4-correction-20260607/manifest.csv \
  --status-out results/summaries/substring-absent-count-gpt-5-4-correction-20260607/status.jsonl \
  --mode full \
  --no-cache \
  --no-skip-completed \
  --cost runcost
```

GPT-5.4 size panel result:

| entry | model | thinking | answer correct | provider errors | cost | input tokens | output tokens | reasoning tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt-5-4-nano-none` | `openai/gpt-5.4-nano` | none | 7/10 | 0 | $0.000139 | 381 | 50 | 0 |
| `gpt-5-4-nano-low` | `openai/gpt-5.4-nano` | low | 8/10 | 0 | $0.001175 | 381 | 879 | 811 |
| `gpt-5-4-nano-medium` | `openai/gpt-5.4-nano` | medium | 9/10 | 0 | $0.001387 | 381 | 1049 | 979 |
| `gpt-5-4-mini-none` | `openai/gpt-5.4-mini` | none | 7/10 | 0 | $0.000619 | 381 | 74 | 0 |
| `gpt-5-4-mini-low` | `openai/gpt-5.4-mini` | low | 9/10 | 0 | $0.002909 | 381 | 583 | 513 |
| `gpt-5-4-mini-medium` | `openai/gpt-5.4-mini` | medium | 9/10 | 0 | $0.011936 | 381 | 2589 | 2519 |

## Behavioral Failures

GPT-5.5 base with `reasoning_effort=none` failed two absent-substring prompts:

- `How many days of the week include the word "toe"?` Expected `0`; raw answer `1`.
- `How many seasons contain the word "box"?` Expected `0`; raw answer `1`.

Gemini 3.1 Flash Lite minimal and low both failed the same prompt:

- `How many colors of the rainbow contain the word "car"?` Expected `0`; raw answer `1`.

GPT-5.5 low/medium and Gemini 3.1 Flash Lite medium/high got all ten correct.

The GPT-5.4 nano and mini failures concentrated on a few prompts:

- GPT-5.4 nano none failed `toe`, `car`, and `up`; low failed `box` and `up`; medium failed `up`.
- GPT-5.4 mini none failed `toe`, `box`, and `up`; low failed `box`; medium failed `box`.

## Interpretation

This tiny smoke suggests the absent-substring count mode is a real discriminant:
no-thinking GPT-5.5 base and low-thinking Gemini 3.1 Flash Lite both hallucinate
one positive match on at least one obvious zero-count item, while moderate
thinking settings clear the set for those two models. The GPT-5.4
nano/mini run strengthens the signal: both smaller GPT-5.4 models still fail at
least one item at medium thinking, with `up` for cardinal directions and `box`
for seasons being especially sticky. The sample is intentionally small and
hand-authored, so it is useful as a probe and future seed set rather than a
release-grade conclusion.

Next useful expansion would be a balanced 40 to 80 item generated set with:

- familiar sets where the true answer is `0`,
- paired controls where the true answer is `1` or `2`,
- multi-character needles and single-letter absent needles,
- overlap traps such as phonetic near-matches, misspellings, and substrings that
  only appear after an invalid rewrite.
