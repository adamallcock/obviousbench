---
title: Paper V1 Scaled 100-Setting Run Summary
date: 2026-06-01
type: runbook
status: draft
---

# Paper V1 Scaled 100-Setting Run Summary

This is the first broad paper_v1 scale test after the grader/max-output fixes. It should be treated as a reliability and shape-of-results run, not yet as the final paper table.

## Artifacts

- Panel: `configs/paper_v1_scaled_100_under_10_panel.yaml`
- Original manifest: `configs/paper_v1_scaled_100_10k_20260601_manifest.csv`
- Nonempty comparison manifest: `configs/paper_v1_scaled_100_10k_20260601_nonempty_manifest.csv`
- Raw eval logs: `results/raw/paper-v1-scaled-100-10k-20260601/`
- Per-model summaries: `results/summaries/paper-v1-scaled-100-10k-20260601/`
- Comparison CSVs: `results/summaries/paper-v1-scaled-100-10k-20260601/comparison/`
- Static report: `docs/reports/2026-06-01-paper-v1-scaled-100-10k/report.html`

## Cost

The uncached pre-run estimate was `$0.387956` for 100 settings, far below the `$10` budget.

The summarized priced usage from the regenerated comparison is:

| Scope | Rows | Cost |
| --- | ---: | ---: |
| Nonempty summaries | 98 | `$0.277090` |
| Comparable full 80/80 rows | 86 | `$0.184396` |

This excludes any provider-side billing for two empty failed eval summaries and depends on runcost/manual price coverage. Even allowing for that, the run is comfortably under the `$10` target.

## Completion

| Category | Count |
| --- | ---: |
| Attempted settings | 100 |
| Runner status `passed` | 88 |
| Runner status `failed_inspect` | 8 |
| Runner status `failed_summary_validation` | 4 |
| Nonempty comparison rows after rescoring | 98 |
| Comparable full 80/80 rows | 86 |
| Partial rows | 8 |
| Zero-scored rows | 4 |
| Empty summaries | 2 |

The static report ranks only rows with the maximum scored sample count, so partial and zero-scored rows are visible but not comparable leaderboard entries.

## Top Comparable Rows

Sorted by answer accuracy, then cost.

| Model | Answer | Strict | Cost | Tokens |
| --- | ---: | ---: | ---: | ---: |
| Tencent: Hy3 preview | 100.0% | 100.0% | `$0.002392` | 38,483 |
| Qwen: Qwen3 235B A22B Thinking 2507 | 100.0% | 100.0% | `$0.003042` | 56,916 |
| Gemini 3.5 Flash | 100.0% | 100.0% | `$0.004946` | 21,085 |
| Qwen: Qwen3 30B A3B Thinking 2507 | 98.8% | 98.8% | `$0.000550` | 58,757 |
| Xiaomi: MiMo-V2.5-Pro | 98.8% | 95.0% | `$0.000670` | 37,735 |
| StepFun: Step 3.5 Flash | 98.8% | 98.8% | `$0.000802` | 38,922 |
| Qwen: Qwen3 Next 80B A3B Thinking | 98.8% | 96.3% | `$0.002158` | 72,911 |
| Qwen: Qwen3 14B | 97.5% | 95.0% | `$0.001070` | 29,024 |
| Z.ai: GLM 4.5 | 97.5% | 93.8% | `$0.001889` | 63,115 |
| Z.ai: GLM 5 | 97.5% | 97.5% | `$0.004040` | 32,623 |

## Partial And Failed Rows

| Model | Scored | Answer | Provider Errors | Notes |
| --- | ---: | ---: | ---: | --- |
| Grok 4.3 | 70/80 | 100.0% | 10 | Salvaged from full eval; not comparable due provider errors. |
| OpenAI GPT-OSS 20B | 70/70 | 100.0% | 0 | Salvaged from killed eval; not comparable because log stopped before 80. |
| NVIDIA: Llama 3.3 Nemotron Super 49B V1.5 | 70/70 | 100.0% | 0 | Salvaged from killed eval; not comparable because log stopped before 80. |
| NVIDIA: Nemotron 3 Super | 70/70 | 98.6% | 0 | Salvaged from killed eval; not comparable because log stopped before 80. |
| OpenAI: gpt-oss-safeguard-20b | 18/32 | 94.4% | 14 | Rate-limited / partial. |
| MoonshotAI: Kimi K2 0711 | 41/70 | 87.8% | 29 | Rate-limited / partial. |
| AionLabs: Aion-1.0-Mini | 70/70 | 84.3% | 0 | Salvaged from killed eval; not comparable because log stopped before 80. |
| Qwen: Qwen3 Coder 30B A3B Instruct | 70/70 | 70.0% | 0 | Salvaged from killed eval; not comparable because log stopped before 80. |

Zero-scored rows were `Llama Guard 3 8B`, `Meta: Llama 3.2 3B Instruct`, `AllenAI: Olmo 3 32B Think`, and `Qwen2.5 Coder 32B Instruct`. Two empty summaries remained: `Reka Flash 3` and `Nous: Hermes 3 70B Instruct`.

## Token Outliers

| Model | Total Tokens | Reasoning Tokens | Scored |
| --- | ---: | ---: | ---: |
| Arcee AI: Trinity Mini | 88,927 | 55,782 | 80 |
| Prime Intellect: INTELLECT-3 | 86,714 | 84,459 | 80 |
| Qwen: Qwen3 Next 80B A3B Thinking | 72,911 | 67,001 | 80 |
| Z.ai: GLM 4.7 Flash | 64,664 | 58,718 | 80 |
| Z.ai: GLM 4.5 | 63,115 | 59,198 | 80 |
| Qwen: Qwen3 30B A3B Thinking 2507 | 58,757 | 54,428 | 80 |
| Qwen: Qwen3 235B A22B Thinking 2507 | 56,916 | 53,091 | 80 |

## Caveats Before Final Paper Run

- This run still used the current harness temperature setting of `0`; decide whether the final public run should use model/provider defaults instead.
- Several OpenRouter routes were stale, rate-limited, or hung after writing partial logs. For the final paper run, consider excluding known bad routes or retrying them separately.
- The non-strict answer scoring now matters more than strict formatting; the report still includes strict metrics, but leaderboard interpretation should use answer correctness as the main benchmark metric.
- The largest insight from this run is not just accuracy: some small or cheap routes perform very well, while several thinking-style routes spend tens of thousands of reasoning tokens on 80 obvious questions.
