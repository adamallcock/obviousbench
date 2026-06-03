---
title: Anthropic Adaptive Thinking Probe
date: 2026-06-02
type: research
status: draft
---

# Anthropic Adaptive Thinking Probe

- Panel: `configs/paper_v1_top_thinking_clean_20260602_panel.yaml`
- Summary root: `results/summaries/paper-v1-anthropic-adaptive-thinking-rerun-20260602`
- CSV: `docs/research/2026-06-02-anthropic-adaptive-thinking-probe.csv`
- Request-shape source: Inspect Anthropic provider request builder.
- Anthropic docs: <https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking> and <https://platform.claude.com/docs/en/build-with-claude/effort>.

## Findings

> **Metric caveat.** For Claude 4.x, `reasoning_tokens` here is the re-tokenized *summary* length, not billed thinking; it can even exceed `output_tokens`. The authoritative billed field is `usage.output_tokens_details.thinking_tokens`, captured only for runs produced after applying `scripts/patch_inspect_anthropic_thinking_tokens.py`. Effort warnings below are baselined on billed `output_tokens`. See `docs/research/2026-06-03-opus-4-8-adaptive-thinking-diagnosis.md`.

- Audited 9 Anthropic row(s); 4 row(s) have diagnostic warning flags.
- Observed billed output below calibrated estimate for: top-thinking-013-anthropic-claude-opus-4-8-high, top-thinking-014-anthropic-claude-opus-4-8-xhigh, top-thinking-015-anthropic-claude-opus-4-8-max.

## Probe Table

| Entry | Effort | Request thinking | Request effort | Betas | Output/sample | Summary tok/sample | Nonzero samples | Answer | Cost | Warnings |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| top-thinking-011-anthropic-claude-opus-4-8-low | low | adaptive/summarized | low |  | 7.62 | 1.79 | 3/80 | 92.5% | $0.04045 |  |
| top-thinking-012-anthropic-claude-opus-4-8-medium | medium | adaptive/summarized | medium |  | 9.80 | 2.73 | 4/80 | 91.2% | $0.04480 |  |
| top-thinking-013-anthropic-claude-opus-4-8-high | high | adaptive/summarized | high | output-128k-2025-02-19 | 9.10 | 2.40 | 3/80 | 95.0% | $0.04340 | thinking_blocks_sparse;observed_output_below_estimate |
| top-thinking-014-anthropic-claude-opus-4-8-xhigh | xhigh | adaptive/summarized | xhigh | output-128k-2025-02-19 | 17.75 | 7.51 | 9/80 | 95.0% | $0.06070 | thinking_blocks_sparse;observed_output_below_estimate |
| top-thinking-015-anthropic-claude-opus-4-8-max | max | adaptive/summarized | max | output-128k-2025-02-19 | 30.34 | 19.27 | 29/80 | 97.5% | $0.08588 | thinking_blocks_sparse;observed_output_below_estimate |
| top-thinking-016-anthropic-claude-sonnet-4-6-low | low | adaptive/summarized | low |  | 7.31 | 0.00 | 0/80 | 88.8% | $0.02034 | reasoning_zero |
| top-thinking-017-anthropic-claude-sonnet-4-6-medium | medium | adaptive/summarized | medium |  | 15.21 | 4.99 | 9/80 | 96.2% | $0.02982 |  |
| top-thinking-018-anthropic-claude-sonnet-4-6-high | high | adaptive/summarized | high | output-128k-2025-02-19 | 54.09 | 37.39 | 44/80 | 100.0% | $0.07647 |  |
| top-thinking-019-anthropic-claude-sonnet-4-6-max | max | adaptive/summarized | max | output-128k-2025-02-19 | 124.53 | 68.44 | 79/80 | 98.8% | $0.16099 |  |

## Notes

- `observed_output_below_estimate` means a high/xhigh/max run billed less than 10% of the panel's calibrated expected `output_tokens` per sample. Output tokens are billing-authoritative and include any billed thinking, so this is a real spend signal (unlike the summary-length reasoning axis).
- `thinking_blocks_sparse` means a high/xhigh/max run returned a non-empty thinking (summary) block on fewer than half of scored samples. This is a behavioral signal about how often the model chose to think (adaptive thinking treats effort as soft guidance, not a floor), not a telemetry undercount.
- `provider_request_settings_display_mismatch` means the panel metadata does not match the executable Inspect request shape for the `thinking.display` field.
