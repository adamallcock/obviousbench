---
title: Substring Absent Count Release 160 Pass3 Results
date: 2026-06-07
type: research
status: complete
---

# Substring Absent Count Release 160 Pass3 Results

## Context

This run continues the substring absent-count promotion path by moving from the 80-item stress suite to a 160-item release-candidate corpus. The known public `days_toe` seed is tagged `dev_calibration_only=true` and placed in `calibration_v0`, so private-eval claims can be read from the private/main/challenge slices rather than from the full corpus alone.

A first provider run was discarded after an integrity check found that the initial release builder reused the earlier experiment ID range. The release builder was corrected to emit non-overlapping `2607xx` IDs, the dataset was regenerated and revalidated, and the results below come from the corrected `id2607` run root.

## Suite

- Dataset: `data/experiments/2026-06-07-substring-absent-count-release-160.jsonl`
- Items: 160
- Zero-target absent-substring traps: 127
- Positive controls: 33
- Canonical split: 10 `calibration_v0`, 150 `private_v0`
- Suite split: 10 `dev_calibration`, 120 `main_eval`, 30 `challenge`
- ID range: `obviousbench.char_count.en.v0.calibration.260701-260710` and `obviousbench.char_count.en.v0.private.260701-260850`
- Known public seed examples: 1 (`days_toe`)
- Matching rule: contiguous substring, case-insensitive, no rewriting collection members.

## Run Contract

- Model: `openai/gpt-5.4-nano`
- Thinking modes: `none`, `low`, `medium`
- Trials: 3 per mode
- Attempts: 1,440 total
- Panel: `configs/2026-06-07-substring-absent-count-release-160-gpt-5-4-nano-pass3-panel.yaml`
- Raw logs: `results/raw/substring-absent-count-release-160-gpt-5-4-nano-pass3-id2607-20260607/`
- Summaries: `results/summaries/substring-absent-count-release-160-gpt-5-4-nano-pass3-id2607-20260607/runs/`
- Status ledger: `results/summaries/substring-absent-count-release-160-gpt-5-4-nano-pass3-id2607-20260607/status.jsonl`
- Cache policy: provider run used `--no-cache --no-skip-completed`.

Commands:

```bash
.venv/bin/python scripts/build_substring_absent_count_release_suite.py
.venv/bin/python scripts/validate_dataset.py data/experiments/2026-06-07-substring-absent-count-release-160.jsonl
OPENAI_API_KEY="$(security find-generic-password -s OPENAI_API_KEY -w)" \
  .venv/bin/python scripts/run_model_panel.py \
  --panel configs/2026-06-07-substring-absent-count-release-160-gpt-5-4-nano-pass3-panel.yaml \
  --dataset data/experiments/2026-06-07-substring-absent-count-release-160.jsonl \
  --raw-root results/raw/substring-absent-count-release-160-gpt-5-4-nano-pass3-id2607-20260607 \
  --summary-root results/summaries/substring-absent-count-release-160-gpt-5-4-nano-pass3-id2607-20260607/runs \
  --manifest-out results/summaries/substring-absent-count-release-160-gpt-5-4-nano-pass3-id2607-20260607/manifest.csv \
  --status-out results/summaries/substring-absent-count-release-160-gpt-5-4-nano-pass3-id2607-20260607/status.jsonl \
  --mode full \
  --no-cache \
  --no-skip-completed \
  --cost runcost
```

## Results

Primary score is `answer_correct`. `strict_correct` was identical in this run.

| mode | pass1 | all-item pass^3 | private pass^3 | pass@3 | majority pass | unstable items | zero-item pass^3 | positive-control pass^3 | main_eval pass^3 | challenge pass^3 | provider errors | cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| none | 86.0% | 85.6% | 84.7% | 86.2% | 86.2% | 1 | 94.5% | 51.5% | 92.5% | 53.3% | 0 | $0.0080 |
| low | 96.9% | 91.2% | 90.7% | 100.0% | 99.4% | 14 | 94.5% | 78.8% | 94.2% | 76.7% | 1 | $0.0445 |
| medium | 99.6% | 98.8% | 98.7% | 100.0% | 100.0% | 2 | 98.4% | 100.0% | 98.3% | 100.0% | 0 | $0.0556 |

`all-item pass^3` is computed over all 160 corpus items, including calibration. `private pass^3` is computed over the 150 private items only. `zero-item pass^3` is computed over the 127 zero-target traps, while `positive-control pass^3` is computed over the 33 positive controls. `pass@3` means an item was answered correctly at least once across the three trials.

## Provider Error

- `low` trial 1 had a scored provider `AttemptTimeoutError` sample error on `obviousbench.char_count.en.v0.private.260776` (`planet names` + `"pluto"`, target `0`); the repo summary counted this as `provider_error=True` and `timeout=False`.

## Failure Pattern

No-thinking remains the brittle setting. Its stable failures include both false nonzero answers on zero-target traps and missed positive controls. Low reasoning substantially improves reliability but had one scored provider `AttemptTimeoutError`; medium reasoning reached perfect pass@3 with no provider errors in the corrected run.

Stable 0/3 failures by mode, first rows:

- `none` `obviousbench.char_count.en.v0.private.260709`: secondary colors + `"cat"`, target `0`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260722`: US bill value names + `"cat"`, target `0`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260729`: punctuation mark names + `"cat"`, target `0`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260735`: Boolean words + `"cat"`, target `0`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260759`: season names + `"mer"`, target `1`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260762`: NATO alphabet words + `"x"`, target `1`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260763`: shape names + `"angle"`, target `2`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260765`: Greek letter names + `"eta"`, target `4`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260770`: tool names + `"saw"`, target `1`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260815`: arithmetic operation names + `"plus"`, target `0`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260818`: web browser names + `"net"`, target `0`, suite split `main_eval`.
- `none` `obviousbench.char_count.en.v0.private.260822`: month names + `"ber"`, target `4`, suite split `challenge`.
- `none` `obviousbench.char_count.en.v0.private.260825`: planet names + `"ur"`, target `3`, suite split `main_eval`.
- `none` `obviousbench.char_count.en.v0.private.260827`: chemical element names + `"ium"`, target `3`, suite split `challenge`.

## Artifacts

- Aggregate metrics CSV: `docs/research/2026-06-07-substring-absent-count-release-160-gpt-5-4-nano-pass3-results.csv`
- Non-perfect item CSV: `docs/research/2026-06-07-substring-absent-count-release-160-gpt-5-4-nano-pass3-item-instability.csv`
- Failure-attempt CSV: `docs/research/2026-06-07-substring-absent-count-release-160-gpt-5-4-nano-pass3-failures.csv`

## Recommendation

Keep the category and the release-shaped split. For headline private-eval claims, report `private_v0`, `main_eval`, and `challenge` slices separately from `dev_calibration`. The public `days_toe` seed should remain calibration-only.
