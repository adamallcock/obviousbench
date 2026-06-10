---
title: Paper V1 Final Result Artifact Audit
date: 2026-06-02
type: review
status: ready
---

# Paper V1 Final Result Artifact Audit

This audit checks the output contract for the paper evidence run.
It does not run model providers, rescore logs, or build comparison
reports. It verifies that the manifest, per-model summaries,
comparison CSVs, and generated report files are present.

Overall status: PASS

- Final sweep manifest: `results/summaries/paper-v1-8x28-current-223-final-20260603/manifest.csv`
- Comparison directory: `results/summaries/paper-v1-8x28-current-223-final-20260603/comparison`
- Report directory: `docs/reports/2026-06-03-paper-v1-8x28-current-223-final`
- Planned models: 223
- Summary files present: 1338/1338
- Comparison files present: 6/6
- Report files present: 4/4
- Structural issues: 0

## Planned Models

| Label | Model | Summary directory |
| --- | --- | --- |
| NVIDIA: Nemotron 3 Super | `openrouter/nvidia/nemotron-3-super-120b-a12b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b` |
| OpenAI GPT-5.4 nano high | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-003-openai-gpt-5-4-nano-high` |
| Qwen: Qwen3 235B A22B Thinking 2507 | `openrouter/qwen/qwen3-235b-a22b-thinking-2507` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507` |
| Tencent: Hy3 preview | `openrouter/tencent/hy3-preview` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-038-openrouter-126-tencent-hy3-preview` |
| Google: Gemini 3.1 Flash Lite medium | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium` |
| Z.ai: GLM 4.6V | `openrouter/z-ai/glm-4.6v` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-033-registry-openrouter-170-z-ai-glm-4-6v` |
| Google: Gemini 3.1 Flash Lite high | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high` |
| Gemini 3 Flash Preview | `google/gemini-3-flash-preview` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-060-registry-gemini-3-flash-preview` |
| MoonshotAI: Kimi K2.5 | `openrouter/moonshotai/kimi-k2.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-049-registry-openrouter-169-moonshotai-kimi-k2-5` |
| MoonshotAI: Kimi K2.6 | `openrouter/moonshotai/kimi-k2.6` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-065-registry-openrouter-164-moonshotai-kimi-k2-6` |
| OpenAI GPT-5.5 low | `openai/gpt-5.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-002-openai-gpt-5-5-low` |
| Google: Gemini 3.5 Flash low | `openrouter/google/gemini-3.5-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-029-openrouter-google-gemini-3-5-flash-low` |
| OpenAI GPT-5.5 low | `openai/gpt-5.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-085-registry-openai-gpt-5-5-low` |
| OpenAI GPT-5.5 medium | `openai/gpt-5.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-003-openai-gpt-5-5-medium` |
| Qwen: Qwen3.6 Plus | `openrouter/qwen/qwen3.6-plus` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-048-registry-openrouter-166-qwen-qwen3-6-plus` |
| OpenAI GPT-5.5 high | `openai/gpt-5.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-004-openai-gpt-5-5-high` |
| Google: Gemini 3.1 Pro Preview Custom Tools low | `openrouter/google/gemini-3.1-pro-preview-customtools` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low` |
| Google: Gemini 3.5 Flash high | `openrouter/google/gemini-3.5-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-031-openrouter-google-gemini-3-5-flash-high` |
| Qwen: Qwen3.7 Max | `openrouter/qwen/qwen3.7-max` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-067-registry-openrouter-178-qwen-qwen3-7-max` |
| Z.ai: GLM 5.1 | `openrouter/z-ai/glm-5.1` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-063-registry-openrouter-128-z-ai-glm-5-1` |
| Gemini 3.5 Flash | `google/gemini-3.5-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-3-5-flash` |
| OpenAI GPT-5.5 xhigh | `openai/gpt-5.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-005-openai-gpt-5-5-xhigh` |
| Google: Gemini 3.1 Pro Preview Custom Tools high | `openrouter/google/gemini-3.1-pro-preview-customtools` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high` |
| Qwen: Qwen3.6 Max Preview | `openrouter/qwen/qwen3.6-max-preview` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-071-registry-openrouter-179-qwen-qwen3-6-max-preview` |
| OpenAI GPT-5.4 nano xhigh | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-006-openai-gpt-5-4-nano-xhigh` |
| MiniMax: MiniMax M3 | `openrouter/minimax/minimax-m3` | `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-039-registry-openrouter-080-minimax-minimax-m3` |
| StepFun: Step 3.5 Flash | `openrouter/stepfun/step-3.5-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-044-openrouter-032-stepfun-step-3-5-flash` |
| Xiaomi: MiMo-V2.5-Pro | `openrouter/xiaomi/mimo-v2.5-pro` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro` |
| Gemini 2.5 Flash | `google/gemini-2.5-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-056-registry-gemini-2-5-flash` |
| Qwen: Qwen3 30B A3B Thinking 2507 | `openrouter/qwen/qwen3-30b-a3b-thinking-2507` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507` |
| Qwen: Qwen3.6 Flash low_budget_512 | `openrouter/qwen/qwen3.6-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-098-thinking-openrouter-qwen-qwen3-6-flash-low` |
| MoonshotAI Kimi Latest | `openrouter/~moonshotai/kimi-latest` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-064-registry-openrouter-161-moonshotai-kimi-latest` |
| OpenAI GPT-5.4 xhigh | `openai/gpt-5.4` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-010-openai-gpt-5-4-xhigh` |
| Qwen: Qwen3 Next 80B A3B Thinking | `openrouter/qwen/qwen3-next-80b-a3b-thinking` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking` |
| Qwen: Qwen3.5 Plus 2026-04-20 | `openrouter/qwen/qwen3.5-plus-20260420` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420` |
| Google: Gemini 3.5 Flash medium | `openrouter/google/gemini-3.5-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-030-openrouter-google-gemini-3-5-flash-medium` |
| Qwen: Qwen3.5 397B A17B | `openrouter/qwen/qwen3.5-397b-a17b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b` |
| Qwen: Qwen3 VL 235B A22B Thinking | `openrouter/qwen/qwen3-vl-235b-a22b-thinking` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking` |
| OpenAI: gpt-oss-120b | `openrouter/openai/gpt-oss-120b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-034-openrouter-048-openai-gpt-oss-120b` |
| OpenAI GPT-OSS 20B | `openrouter/openai/gpt-oss-20b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-gpt-oss-20b` |
| OpenAI GPT-5 nano low | `openai/gpt-5-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-088-thinking-openai-gpt-5-nano-low` |
| OpenAI GPT-5 nano medium | `openai/gpt-5-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-090-thinking-openai-gpt-5-nano-medium` |
| Qwen: Qwen3 14B | `openrouter/qwen/qwen3-14b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-039-openrouter-059-qwen-qwen3-14b` |
| Xiaomi: MiMo-V2.5 | `openrouter/xiaomi/mimo-v2.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-016-registry-openrouter-163-xiaomi-mimo-v2-5` |
| OpenAI GPT-5.4 mini medium | `openai/gpt-5.4-mini` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-004-openai-gpt-5-4-mini-medium` |
| Qwen: Qwen3 30B A3B | `openrouter/qwen/qwen3-30b-a3b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-061-openrouter-057-qwen-qwen3-30b-a3b` |
| MiniMax: MiniMax M2 | `openrouter/minimax/minimax-m2` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-084-openrouter-040-minimax-minimax-m2` |
| OpenAI GPT-5.4 medium | `openai/gpt-5.4` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-008-openai-gpt-5-4-medium` |
| OpenAI GPT-5.4 high | `openai/gpt-5.4` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-009-openai-gpt-5-4-high` |
| Z.ai: GLM 5 Turbo | `openrouter/z-ai/glm-5-turbo` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-068-registry-openrouter-180-z-ai-glm-5-turbo` |
| Z.ai: GLM 5 | `openrouter/z-ai/glm-5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-097-openrouter-129-z-ai-glm-5` |
| Z.ai: GLM 4.6 | `openrouter/z-ai/glm-4.6` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-093-openrouter-136-z-ai-glm-4-6` |
| Qwen: Qwen3.5-27B | `openrouter/qwen/qwen3.5-27b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-043-registry-openrouter-088-qwen-qwen3-5-27b` |
| Z.ai: GLM 5V Turbo | `openrouter/z-ai/glm-5v-turbo` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-069-registry-openrouter-184-z-ai-glm-5v-turbo` |
| Prime Intellect: INTELLECT-3 | `openrouter/prime-intellect/intellect-3` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-087-openrouter-135-prime-intellect-intellect-3` |
| Z.ai: GLM 4.5 | `openrouter/z-ai/glm-4.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-098-openrouter-146-z-ai-glm-4-5` |
| Qwen: Qwen3.5-122B-A10B | `openrouter/qwen/qwen3.5-122b-a10b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b` |
| DeepSeek: DeepSeek V4 Flash | `openrouter/deepseek/deepseek-v4-flash` | `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-035-openrouter-027-deepseek-deepseek-v4-flash` |
| OpenAI GPT-5.4 nano medium | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-002-openai-gpt-5-4-nano-medium` |
| NVIDIA Nemotron 3 Nano 30B A3B | `openrouter/nvidia/nemotron-3-nano-30b-a3b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-nemotron-3-nano` |
| NVIDIA: Llama 3.3 Nemotron Super 49B V1.5 | `openrouter/nvidia/llama-3.3-nemotron-super-49b-v1.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5` |
| Google: Gemini 3.1 Flash Lite low | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low` |
| DeepSeek: DeepSeek V4 Pro | `openrouter/deepseek/deepseek-v4-pro` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-079-openrouter-125-deepseek-deepseek-v4-pro` |
| OpenAI GPT-5.4 mini high | `openai/gpt-5.4-mini` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-005-openai-gpt-5-4-mini-high` |
| Qwen: Qwen3.5-Flash | `openrouter/qwen/qwen3.5-flash-02-23` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23` |
| OpenAI GPT-5.4 low | `openai/gpt-5.4` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-007-openai-gpt-5-4-low` |
| Z.ai: GLM 4.7 | `openrouter/z-ai/glm-4.7` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-094-openrouter-131-z-ai-glm-4-7` |
| Qwen: Qwen3.6 Flash | `openrouter/qwen/qwen3.6-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-036-registry-openrouter-081-qwen-qwen3-6-flash` |
| Qwen: Qwen3.6 35B A3B low_budget_512 | `openrouter/qwen/qwen3.6-35b-a3b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low` |
| Qwen: Qwen3 235B A22B | `openrouter/qwen/qwen3-235b-a22b` | `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-096-openrouter-061-qwen-qwen3-235b-a22b` |
| Grok Build 0.1 | `grok/grok-build-0.1` | `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-next-058-registry-grok-build-0-1` |
| Gemini 2.5 Flash-Lite low_budget_1024 | `google/gemini-2.5-flash-lite` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-089-thinking-gemini-gemini-2-5-flash-lite-low` |
| MiniMax: MiniMax M2.1 | `openrouter/minimax/minimax-m2.1` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-082-openrouter-034-minimax-minimax-m2-1` |
| OpenAI GPT-5.4 mini xhigh | `openai/gpt-5.4-mini` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-007-openai-gpt-5-4-mini-xhigh` |
| Qwen: Qwen3.6 35B A3B | `openrouter/qwen/qwen3.6-35b-a3b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b` |
| Grok 4.3 | `grok/grok-4.3` | `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-paper-grok-4-3` |
| Google: Gemma 4 31B | `openrouter/google/gemma-4-31b-it` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-017-registry-openrouter-165-google-gemma-4-31b-it` |
| OpenAI GPT-4.1 | `openai/gpt-4.1` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1` |
| Qwen: Qwen3.5 Plus 2026-02-15 | `openrouter/qwen/qwen3.5-plus-02-15` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15` |
| Anthropic Claude Opus 4.7 | `anthropic/claude-opus-4-7` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-083-registry-anthropic-claude-opus-4-7` |
| Anthropic Claude Opus 4.6 | `anthropic/claude-opus-4-6` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-082-registry-anthropic-claude-opus-4-6` |
| Qwen: Qwen3.6 27B | `openrouter/qwen/qwen3.6-27b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-059-registry-openrouter-083-qwen-qwen3-6-27b` |
| Qwen: Qwen3 VL 8B Thinking | `openrouter/qwen/qwen3-vl-8b-thinking` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking` |
| Qwen: Qwen3 VL 30B A3B Thinking | `openrouter/qwen/qwen3-vl-30b-a3b-thinking` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking` |
| MoonshotAI: Kimi K2 0905 | `openrouter/moonshotai/kimi-k2-0905` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-100-openrouter-142-moonshotai-kimi-k2-0905` |
| OpenAI GPT-4o | `openai/gpt-4o` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-078-registry-openai-gpt-4o` |
| Qwen: Qwen3 32B | `openrouter/qwen/qwen3-32b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-041-openrouter-060-qwen-qwen3-32b` |
| Gemini 2.5 Flash-Lite medium_budget_8192 | `google/gemini-2.5-flash-lite` | `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-097-thinking-gemini-gemini-2-5-flash-lite-medium` |
| OpenAI GPT-5.5 no thinking | `openai/gpt-5.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-086-registry-openai-gpt-5-5-none` |
| Claude Opus 4.8 high | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-013-anthropic-claude-opus-4-8-high` |
| Claude Opus 4.8 low | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-011-anthropic-claude-opus-4-8-low` |
| Claude Opus 4.8 medium | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-012-anthropic-claude-opus-4-8-medium` |
| Claude Opus 4.8 xhigh | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-014-anthropic-claude-opus-4-8-xhigh` |
| Anthropic Claude Opus 4.8 | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-084-registry-anthropic-claude-opus-4-8` |
| MiniMax: MiniMax M2.5 | `openrouter/minimax/minimax-m2.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-089-openrouter-031-minimax-minimax-m2-5` |
| Qwen: Qwen3.5-35B-A3B | `openrouter/qwen/qwen3.5-35b-a3b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b` |
| Xiaomi MiMo-V2-Flash | `openrouter/xiaomi/mimo-v2-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-xiaomi-mimo-v2-flash` |
| Qwen: Qwen3 Coder Next | `openrouter/qwen/qwen3-coder-next` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-075-openrouter-130-qwen-qwen3-coder-next` |
| Claude Sonnet 4.6 low | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-016-anthropic-claude-sonnet-4-6-low` |
| OpenAI GPT-5.5 none | `openai/gpt-5.5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-001-openai-gpt-5-5-none` |
| Claude Opus 4.8 max | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-015-anthropic-claude-opus-4-8-max` |
| Google: Gemma 4 26B A4B | `openrouter/google/gemma-4-26b-a4b-it` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it` |
| OpenAI: GPT-5.4 Nano low | `openrouter/openai/gpt-5.4-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-100-thinking-openrouter-openai-gpt-5-4-nano-low` |
| Google: Gemini 3.5 Flash minimal | `openrouter/google/gemini-3.5-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-028-openrouter-google-gemini-3-5-flash-minimal` |
| OpenAI GPT-5.4 no thinking | `openai/gpt-5.4` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-081-registry-openai-gpt-5-4-none` |
| Claude Sonnet 4.6 medium | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-017-anthropic-claude-sonnet-4-6-medium` |
| OpenAI GPT-5 minimal | `openai/gpt-5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-077-registry-openai-gpt-5-minimal` |
| Claude Sonnet 4.6 high | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-018-anthropic-claude-sonnet-4-6-high` |
| Anthropic Claude Sonnet 4.6 | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-sonnet-4-6` |
| Z.ai: GLM 4.5V | `openrouter/z-ai/glm-4.5v` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-053-registry-openrouter-173-z-ai-glm-4-5v` |
| Z.ai: GLM 4.7 Flash | `openrouter/z-ai/glm-4.7-flash` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-051-openrouter-033-z-ai-glm-4-7-flash` |
| MiniMax: MiniMax M2.7 | `openrouter/minimax/minimax-m2.7` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-090-openrouter-028-minimax-minimax-m2-7` |
| Z.ai: GLM 4.5 Air | `openrouter/z-ai/glm-4.5-air` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-078-openrouter-147-z-ai-glm-4-5-air` |
| OpenAI GPT-4.1 mini | `openai/gpt-4.1-mini` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1-mini` |
| Nex AGI: DeepSeek V3.1 Nex N1 | `openrouter/nex-agi/deepseek-v3.1-nex-n1` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1` |
| Qwen: Qwen3 235B A22B Instruct 2507 | `openrouter/qwen/qwen3-235b-a22b-2507` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507` |
| Mistral: Mistral Small 4 | `openrouter/mistralai/mistral-small-2603` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-025-registry-openrouter-085-mistralai-mistral-small-2603` |
| Qwen3 Next 80B A3B Instruct | `openrouter/qwen/qwen3-next-80b-a3b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-qwen3-next` |
| MoonshotAI: Kimi K2 0711 | `openrouter/moonshotai/kimi-k2` | `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-099-openrouter-149-moonshotai-kimi-k2` |
| Nous: Hermes 4 405B | `openrouter/nousresearch/hermes-4-405b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-062-registry-openrouter-144-nousresearch-hermes-4-405b` |
| Anthropic Claude Haiku 4.5 | `anthropic/claude-haiku-4-5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-haiku-4-5` |
| AI21: Jamba Large 1.7 | `openrouter/ai21/jamba-large-1.7` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-076-registry-openrouter-181-ai21-jamba-large-1-7` |
| Baidu: ERNIE 4.5 VL 424B A47B | `openrouter/baidu/ernie-4.5-vl-424b-a47b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b` |
| Claude Sonnet 4.6 max | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-019-anthropic-claude-sonnet-4-6-max` |
| Gemini 2.5 Flash-Lite | `google/gemini-2.5-flash-lite` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-2-5-flash-lite` |
| Qwen: Qwen-Plus | `openrouter/qwen/qwen-plus` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-072-openrouter-152-qwen-qwen-plus` |
| Mistral: Devstral 2 2512 | `openrouter/mistralai/devstral-2512` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-051-registry-openrouter-092-mistralai-devstral-2512` |
| OpenAI GPT-5.4 nano low | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-099-thinking-openai-gpt-5-4-nano-low` |
| OpenAI GPT-5 mini minimal | `openai/gpt-5-mini` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-092-thinking-openai-gpt-5-mini-minimal` |
| Nous: Hermes 3 405B Instruct | `openrouter/nousresearch/hermes-3-llama-3.1-405b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b` |
| MiniMax: MiniMax-01 | `openrouter/minimax/minimax-01` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-035-registry-openrouter-113-minimax-minimax-01` |
| OpenAI GPT-5.2 no thinking | `openai/gpt-5.2` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-080-registry-openai-gpt-5-2-none` |
| Qwen: Qwen3 8B | `openrouter/qwen/qwen3-8b` | `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-050-openrouter-058-qwen-qwen3-8b` |
| OpenAI GPT-5.4 none | `openai/gpt-5.4` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-006-openai-gpt-5-4-none` |
| Mistral: Mistral Large 3 2512 | `openrouter/mistralai/mistral-large-2512` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-045-registry-openrouter-171-mistralai-mistral-large-2512` |
| Gemini 3.1 Flash-Lite minimal_budget_1024 | `google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-093-thinking-gemini-gemini-3-1-flash-lite-minimal` |
| Google: Gemma 3 12B | `openrouter/google/gemma-3-12b-it` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-002-registry-openrouter-110-google-gemma-3-12b-it` |
| Meta: Llama 3.3 70B Instruct | `openrouter/meta-llama/llama-3.3-70b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct` |
| OpenAI GPT-5 nano minimal | `openai/gpt-5-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-5-nano-minimal` |
| Qwen: Qwen3 VL 235B A22B Instruct | `openrouter/qwen/qwen3-vl-235b-a22b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct` |
| Google: Gemini 3.1 Flash Lite minimal | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal` |
| Google: Gemini 3.1 Flash Lite minimal | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal` |
| Google: Gemini 3.1 Flash Lite Preview minimal | `openrouter/google/gemini-3.1-flash-lite-preview` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal` |
| Gemini 3.1 Flash-Lite | `google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-042-registry-gemini-3-1-flash-lite` |
| Qwen: Qwen Plus 0728 | `openrouter/qwen/qwen-plus-2025-07-28` | `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28` |
| Qwen: Qwen3 Coder 480B A35B | `openrouter/qwen/qwen3-coder` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-095-openrouter-148-qwen-qwen3-coder` |
| Qwen: Qwen2.5 VL 72B Instruct | `openrouter/qwen/qwen2.5-vl-72b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct` |
| Meta: Llama 3.1 70B Instruct | `openrouter/meta-llama/llama-3.1-70b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct` |
| Qwen: Qwen3 Coder Plus | `openrouter/qwen/qwen3-coder-plus` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-061-registry-openrouter-139-qwen-qwen3-coder-plus` |
| OpenAI GPT-5 mini minimal | `openai/gpt-5-mini` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-047-registry-openai-gpt-5-mini-minimal` |
| Mistral: Mixtral 8x22B Instruct | `openrouter/mistralai/mixtral-8x22b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct` |
| Magnum v4 72B | `openrouter/anthracite-org/magnum-v4-72b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b` |
| Arcee AI: Trinity Mini | `openrouter/arcee-ai/trinity-mini` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-030-openrouter-037-arcee-ai-trinity-mini` |
| Mistral Large 2407 | `openrouter/mistralai/mistral-large-2407` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-074-registry-openrouter-185-mistralai-mistral-large-2407` |
| Z.ai: GLM 4 32B | `openrouter/z-ai/glm-4-32b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-024-openrouter-052-z-ai-glm-4-32b` |
| Nous: Hermes 4 70B | `openrouter/nousresearch/hermes-4-70b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-054-openrouter-143-nousresearch-hermes-4-70b` |
| Mistral: Saba | `openrouter/mistralai/mistral-saba` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-027-registry-openrouter-176-mistralai-mistral-saba` |
| Mistral: Mistral Medium 3.1 | `openrouter/mistralai/mistral-medium-3.1` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-052-registry-openrouter-172-mistralai-mistral-medium-3-1` |
| Mistral: Mistral Medium 3 | `openrouter/mistralai/mistral-medium-3` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-054-registry-openrouter-175-mistralai-mistral-medium-3` |
| Cohere: Command A | `openrouter/cohere/command-a` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-079-registry-openrouter-182-cohere-command-a` |
| IBM: Granite 4.1 8B | `openrouter/ibm-granite/granite-4.1-8b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-021-openrouter-026-ibm-granite-granite-4-1-8b` |
| Google: Gemma 3n 4B | `openrouter/google/gemma-3n-e4b-it` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-027-openrouter-056-google-gemma-3n-e4b-it` |
| OpenAI GPT-4.1 nano | `openai/gpt-4.1-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-019-registry-openai-gpt-4-1-nano` |
| Meta: Llama 4 Maverick | `openrouter/meta-llama/llama-4-maverick` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-026-registry-openrouter-106-meta-llama-llama-4-maverick` |
| DeepSeek: DeepSeek V3.1 | `openrouter/deepseek/deepseek-chat-v3.1` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1` |
| DeepSeek: DeepSeek V3.1 Terminus | `openrouter/deepseek/deepseek-v3.1-terminus` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus` |
| Mistral: Codestral 2508 | `openrouter/mistralai/codestral-2508` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-034-registry-openrouter-174-mistralai-codestral-2508` |
| Qwen2.5 72B Instruct | `openrouter/qwen/qwen-2.5-72b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct` |
| Baidu: ERNIE 4.5 300B A47B | `openrouter/baidu/ernie-4.5-300b-a47b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b` |
| Meta: Llama 3 70B Instruct | `openrouter/meta-llama/llama-3-70b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct` |
| TheDrummer: Cydonia 24B V4.1 | `openrouter/thedrummer/cydonia-24b-v4.1` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1` |
| TheDrummer: Skyfall 36B V2 | `openrouter/thedrummer/skyfall-36b-v2` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-076-openrouter-151-thedrummer-skyfall-36b-v2` |
| OpenAI GPT-5.4 mini no thinking | `openai/gpt-5.4-mini` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-070-registry-openai-gpt-5-4-mini-none` |
| NVIDIA: Nemotron Nano 9B V2 | `openrouter/nvidia/nemotron-nano-9b-v2` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2` |
| IBM: Granite 4.0 Micro | `openrouter/ibm-granite/granite-4.0-h-micro` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro` |
| Google: Gemma 3 27B | `openrouter/google/gemma-3-27b-it` | `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-006-registry-openrouter-111-google-gemma-3-27b-it` |
| OpenAI GPT-4o mini | `openai/gpt-4o-mini` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-024-registry-openai-gpt-4o-mini` |
| Mistral: Ministral 3 14B 2512 | `openrouter/mistralai/ministral-14b-2512` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-014-registry-openrouter-093-mistralai-ministral-14b-2512` |
| DeepSeek: DeepSeek V3.2 | `openrouter/deepseek/deepseek-v3.2` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-048-openrouter-134-deepseek-deepseek-v3-2` |
| Mistral: Mistral Small 3 | `openrouter/mistralai/mistral-small-24b-instruct-2501` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501` |
| OpenAI GPT-5 nano minimal | `openai/gpt-5-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-087-thinking-openai-gpt-5-nano-minimal` |
| DeepSeek: DeepSeek V3.2 Exp | `openrouter/deepseek/deepseek-v3.2-exp` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp` |
| WizardLM-2 8x22B | `openrouter/microsoft/wizardlm-2-8x22b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b` |
| Mistral: Ministral 3 8B 2512 | `openrouter/mistralai/ministral-8b-2512` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-008-registry-openrouter-094-mistralai-ministral-8b-2512` |
| Qwen: Qwen3 VL 30B A3B Instruct | `openrouter/qwen/qwen3-vl-30b-a3b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct` |
| OpenAI GPT-5.4 nano no thinking | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-037-registry-openai-gpt-5-4-nano-none` |
| Mistral: Mistral Medium 3.5 | `openrouter/mistralai/mistral-medium-3-5` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-075-registry-openrouter-183-mistralai-mistral-medium-3-5` |
| Qwen: Qwen3 30B A3B Instruct 2507 | `openrouter/qwen/qwen3-30b-a3b-instruct-2507` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507` |
| LiquidAI: LFM2-24B-A2B | `openrouter/liquid/lfm-2-24b-a2b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-026-openrouter-030-liquid-lfm-2-24b-a2b` |
| Sao10K: Llama 3 8B Lunaris | `openrouter/sao10k/l3-lunaris-8b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-017-openrouter-121-sao10k-l3-lunaris-8b` |
| Mistral: Mistral Small 3.2 24B | `openrouter/mistralai/mistral-small-3.2-24b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct` |
| Meta: Llama 3.2 11B Vision Instruct | `openrouter/meta-llama/llama-3.2-11b-vision-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct` |
| Google: Gemma 2 27B | `openrouter/google/gemma-2-27b-it` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-068-openrouter-074-google-gemma-2-27b-it` |
| Mistral: Voxtral Small 24B 2507 | `openrouter/mistralai/voxtral-small-24b-2507` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507` |
| Meta: Llama 4 Scout | `openrouter/meta-llama/llama-4-scout` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-012-registry-openrouter-107-meta-llama-llama-4-scout` |
| Qwen: Qwen3 VL 8B Instruct | `openrouter/qwen/qwen3-vl-8b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct` |
| Qwen: Qwen2.5 7B Instruct | `openrouter/qwen/qwen-2.5-7b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct` |
| Tencent: Hunyuan A13B Instruct | `openrouter/tencent/hunyuan-a13b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct` |
| EssentialAI: Rnj 1 Instruct | `openrouter/essentialai/rnj-1-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-031-openrouter-133-essentialai-rnj-1-instruct` |
| DeepSeek: DeepSeek V3 0324 | `openrouter/deepseek/deepseek-chat-v3-0324` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324` |
| DeepSeek: DeepSeek V3 | `openrouter/deepseek/deepseek-chat` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-077-openrouter-153-deepseek-deepseek-chat` |
| TheDrummer: UnslopNemo 12B | `openrouter/thedrummer/unslopnemo-12b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-056-openrouter-068-thedrummer-unslopnemo-12b` |
| Meta: Llama 3.1 8B Instruct | `openrouter/meta-llama/llama-3.1-8b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct` |
| Google: Gemma 3 4B | `openrouter/google/gemma-3-4b-it` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-001-registry-openrouter-109-google-gemma-3-4b-it` |
| Mistral: Ministral 3 3B 2512 | `openrouter/mistralai/ministral-3b-2512` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-004-registry-openrouter-095-mistralai-ministral-3b-2512` |
| TheDrummer: Rocinante 12B | `openrouter/thedrummer/rocinante-12b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-059-openrouter-070-thedrummer-rocinante-12b` |
| Microsoft: Phi 4 Mini Instruct | `openrouter/microsoft/phi-4-mini-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-049-openrouter-042-microsoft-phi-4-mini-instruct` |
| ByteDance: UI-TARS 7B | `openrouter/bytedance/ui-tars-1.5-7b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b` |
| MythoMax 13B | `openrouter/gryphe/mythomax-l2-13b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-018-openrouter-079-gryphe-mythomax-l2-13b` |
| NousResearch: Hermes 2 Pro - Llama-3 8B | `openrouter/nousresearch/hermes-2-pro-llama-3-8b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b` |
| Mistral: Mistral Nemo | `openrouter/mistralai/mistral-nemo` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-013-openrouter-159-mistralai-mistral-nemo` |
| Meta: Llama 3 8B Instruct | `openrouter/meta-llama/llama-3-8b-instruct` | `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct` |
| Microsoft: Phi 4 | `openrouter/microsoft/phi-4` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-028-openrouter-066-microsoft-phi-4` |
| ReMM SLERP 13B | `openrouter/undi95/remm-slerp-l2-13b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-067-openrouter-078-undi95-remm-slerp-l2-13b` |
| Qwen: Qwen3 Coder Flash | `openrouter/qwen/qwen3-coder-flash` | `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-083-openrouter-045-qwen-qwen3-coder-flash` |
| Qwen: Qwen3 Coder 30B A3B Instruct | `openrouter/qwen/qwen3-coder-30b-a3b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct` |
| Reka Edge | `openrouter/rekaai/reka-edge` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-005-registry-openrouter-167-rekaai-reka-edge` |
| AionLabs: Aion-RP 1.0 (8B) | `openrouter/aion-labs/aion-rp-llama-3.1-8b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b` |
| Qwen: Qwen3 Max | `openrouter/qwen/qwen3-max` | `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-066-registry-openrouter-138-qwen-qwen3-max` |
| DeepSeek: R1 Distill Qwen 32B | `openrouter/deepseek/deepseek-r1-distill-qwen-32b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b` |
| Meta: Llama 3.2 1B Instruct | `openrouter/meta-llama/llama-3.2-1b-instruct` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct` |
| Meta: Llama Guard 4 12B | `openrouter/meta-llama/llama-guard-4-12b` | `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b` |
| OpenAI GPT-5.4 mini low | `openai/gpt-5.4-mini` | `results/summaries/paper-v1-8x28-fill-gpt-5-4-mini-low-20260603/runs/expand222-fill-openai-gpt-5-4-mini-low` |

## Summary Artifacts

| Path | Status | Evidence |
| --- | --- | --- |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/summary.csv` | PRESENT | 1390 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/usage_by_family.csv` | PRESENT | 2583 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/usage_by_section.csv` | PRESENT | 4908 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/usage_by_question.csv` | PRESENT | 87864 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/usage_by_sample.csv` | PRESENT | 98824 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/failure_gallery.md` | PRESENT | 5685 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-003-openai-gpt-5-4-nano-high/summary.csv` | PRESENT | 1315 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-003-openai-gpt-5-4-nano-high/usage_by_family.csv` | PRESENT | 2690 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-003-openai-gpt-5-4-nano-high/usage_by_section.csv` | PRESENT | 5006 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-003-openai-gpt-5-4-nano-high/usage_by_question.csv` | PRESENT | 82819 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-003-openai-gpt-5-4-nano-high/usage_by_sample.csv` | PRESENT | 90863 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-003-openai-gpt-5-4-nano-high/failure_gallery.md` | PRESENT | 11140 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/summary.csv` | PRESENT | 1533 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/usage_by_family.csv` | PRESENT | 3718 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/usage_by_section.csv` | PRESENT | 7054 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/usage_by_question.csv` | PRESENT | 104847 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/usage_by_sample.csv` | PRESENT | 109207 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/failure_gallery.md` | PRESENT | 5722 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-038-openrouter-126-tencent-hy3-preview/summary.csv` | PRESENT | 1385 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-038-openrouter-126-tencent-hy3-preview/usage_by_family.csv` | PRESENT | 3407 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-038-openrouter-126-tencent-hy3-preview/usage_by_section.csv` | PRESENT | 6469 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-038-openrouter-126-tencent-hy3-preview/usage_by_question.csv` | PRESENT | 96459 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-038-openrouter-126-tencent-hy3-preview/usage_by_sample.csv` | PRESENT | 101418 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-038-openrouter-126-tencent-hy3-preview/failure_gallery.md` | PRESENT | 2711 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/summary.csv` | PRESENT | 1350 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/usage_by_family.csv` | PRESENT | 3163 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/usage_by_section.csv` | PRESENT | 5507 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/usage_by_question.csv` | PRESENT | 91391 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/usage_by_sample.csv` | PRESENT | 100197 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/failure_gallery.md` | PRESENT | 4000 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-033-registry-openrouter-170-z-ai-glm-4-6v/summary.csv` | PRESENT | 1358 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-033-registry-openrouter-170-z-ai-glm-4-6v/usage_by_family.csv` | PRESENT | 2284 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-033-registry-openrouter-170-z-ai-glm-4-6v/usage_by_section.csv` | PRESENT | 4301 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-033-registry-openrouter-170-z-ai-glm-4-6v/usage_by_question.csv` | PRESENT | 78903 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-033-registry-openrouter-170-z-ai-glm-4-6v/usage_by_sample.csv` | PRESENT | 89922 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-033-registry-openrouter-170-z-ai-glm-4-6v/failure_gallery.md` | PRESENT | 8045 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/summary.csv` | PRESENT | 1359 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/usage_by_family.csv` | PRESENT | 3182 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/usage_by_section.csv` | PRESENT | 5512 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/usage_by_question.csv` | PRESENT | 91048 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/usage_by_sample.csv` | PRESENT | 99320 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/failure_gallery.md` | PRESENT | 2962 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-060-registry-gemini-3-flash-preview/summary.csv` | PRESENT | 1371 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-060-registry-gemini-3-flash-preview/usage_by_family.csv` | PRESENT | 3335 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-060-registry-gemini-3-flash-preview/usage_by_section.csv` | PRESENT | 5503 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-060-registry-gemini-3-flash-preview/usage_by_question.csv` | PRESENT | 88394 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-060-registry-gemini-3-flash-preview/usage_by_sample.csv` | PRESENT | 96966 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-060-registry-gemini-3-flash-preview/failure_gallery.md` | PRESENT | 1089 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-049-registry-openrouter-169-moonshotai-kimi-k2-5/summary.csv` | PRESENT | 1394 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-049-registry-openrouter-169-moonshotai-kimi-k2-5/usage_by_family.csv` | PRESENT | 3439 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-049-registry-openrouter-169-moonshotai-kimi-k2-5/usage_by_section.csv` | PRESENT | 5631 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-049-registry-openrouter-169-moonshotai-kimi-k2-5/usage_by_question.csv` | PRESENT | 90566 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-049-registry-openrouter-169-moonshotai-kimi-k2-5/usage_by_sample.csv` | PRESENT | 98079 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-049-registry-openrouter-169-moonshotai-kimi-k2-5/failure_gallery.md` | PRESENT | 1697 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-065-registry-openrouter-164-moonshotai-kimi-k2-6/summary.csv` | PRESENT | 1392 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-065-registry-openrouter-164-moonshotai-kimi-k2-6/usage_by_family.csv` | PRESENT | 3447 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-065-registry-openrouter-164-moonshotai-kimi-k2-6/usage_by_section.csv` | PRESENT | 5653 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-065-registry-openrouter-164-moonshotai-kimi-k2-6/usage_by_question.csv` | PRESENT | 90621 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-065-registry-openrouter-164-moonshotai-kimi-k2-6/usage_by_sample.csv` | PRESENT | 98139 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-065-registry-openrouter-164-moonshotai-kimi-k2-6/failure_gallery.md` | PRESENT | 844 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-002-openai-gpt-5-5-low/summary.csv` | PRESENT | 1230 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-002-openai-gpt-5-5-low/usage_by_family.csv` | PRESENT | 2657 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-002-openai-gpt-5-5-low/usage_by_section.csv` | PRESENT | 4594 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-002-openai-gpt-5-5-low/usage_by_question.csv` | PRESENT | 78790 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-002-openai-gpt-5-5-low/usage_by_sample.csv` | PRESENT | 87277 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-002-openai-gpt-5-5-low/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-029-openrouter-google-gemini-3-5-flash-low/summary.csv` | PRESENT | 1344 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-029-openrouter-google-gemini-3-5-flash-low/usage_by_family.csv` | PRESENT | 3084 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-029-openrouter-google-gemini-3-5-flash-low/usage_by_section.csv` | PRESENT | 5256 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-029-openrouter-google-gemini-3-5-flash-low/usage_by_question.csv` | PRESENT | 88377 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-029-openrouter-google-gemini-3-5-flash-low/usage_by_sample.csv` | PRESENT | 96499 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-029-openrouter-google-gemini-3-5-flash-low/failure_gallery.md` | PRESENT | 2092 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-085-registry-openai-gpt-5-5-low/summary.csv` | PRESENT | 1316 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-085-registry-openai-gpt-5-5-low/usage_by_family.csv` | PRESENT | 2778 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-085-registry-openai-gpt-5-5-low/usage_by_section.csv` | PRESENT | 4693 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-085-registry-openai-gpt-5-5-low/usage_by_question.csv` | PRESENT | 79717 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-085-registry-openai-gpt-5-5-low/usage_by_sample.csv` | PRESENT | 89096 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-085-registry-openai-gpt-5-5-low/failure_gallery.md` | PRESENT | 959 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-003-openai-gpt-5-5-medium/summary.csv` | PRESENT | 1315 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-003-openai-gpt-5-5-medium/usage_by_family.csv` | PRESENT | 2685 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-003-openai-gpt-5-5-medium/usage_by_section.csv` | PRESENT | 4634 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-003-openai-gpt-5-5-medium/usage_by_question.csv` | PRESENT | 79510 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-003-openai-gpt-5-5-medium/usage_by_sample.csv` | PRESENT | 88659 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-003-openai-gpt-5-5-medium/failure_gallery.md` | PRESENT | 959 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-048-registry-openrouter-166-qwen-qwen3-6-plus/summary.csv` | PRESENT | 1380 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-048-registry-openrouter-166-qwen-qwen3-6-plus/usage_by_family.csv` | PRESENT | 3367 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-048-registry-openrouter-166-qwen-qwen3-6-plus/usage_by_section.csv` | PRESENT | 5556 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-048-registry-openrouter-166-qwen-qwen3-6-plus/usage_by_question.csv` | PRESENT | 89443 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-048-registry-openrouter-166-qwen-qwen3-6-plus/usage_by_sample.csv` | PRESENT | 96969 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-048-registry-openrouter-166-qwen-qwen3-6-plus/failure_gallery.md` | PRESENT | 4545 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-004-openai-gpt-5-5-high/summary.csv` | PRESENT | 1300 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-004-openai-gpt-5-5-high/usage_by_family.csv` | PRESENT | 2677 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-004-openai-gpt-5-5-high/usage_by_section.csv` | PRESENT | 4610 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-004-openai-gpt-5-5-high/usage_by_question.csv` | PRESENT | 79243 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-004-openai-gpt-5-5-high/usage_by_sample.csv` | PRESENT | 87782 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-004-openai-gpt-5-5-high/failure_gallery.md` | PRESENT | 959 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/summary.csv` | PRESENT | 1391 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/usage_by_family.csv` | PRESENT | 3298 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/usage_by_section.csv` | PRESENT | 5831 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/usage_by_question.csv` | PRESENT | 96363 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/usage_by_sample.csv` | PRESENT | 104556 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/failure_gallery.md` | PRESENT | 3320 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-031-openrouter-google-gemini-3-5-flash-high/summary.csv` | PRESENT | 1358 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-031-openrouter-google-gemini-3-5-flash-high/usage_by_family.csv` | PRESENT | 3073 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-031-openrouter-google-gemini-3-5-flash-high/usage_by_section.csv` | PRESENT | 5305 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-031-openrouter-google-gemini-3-5-flash-high/usage_by_question.csv` | PRESENT | 88690 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-031-openrouter-google-gemini-3-5-flash-high/usage_by_sample.csv` | PRESENT | 97018 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-031-openrouter-google-gemini-3-5-flash-high/failure_gallery.md` | PRESENT | 2950 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-067-registry-openrouter-178-qwen-qwen3-7-max/summary.csv` | PRESENT | 1308 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-067-registry-openrouter-178-qwen-qwen3-7-max/usage_by_family.csv` | PRESENT | 3345 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-067-registry-openrouter-178-qwen-qwen3-7-max/usage_by_section.csv` | PRESENT | 5486 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-067-registry-openrouter-178-qwen-qwen3-7-max/usage_by_question.csv` | PRESENT | 88774 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-067-registry-openrouter-178-qwen-qwen3-7-max/usage_by_sample.csv` | PRESENT | 96268 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-067-registry-openrouter-178-qwen-qwen3-7-max/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-063-registry-openrouter-128-z-ai-glm-5-1/summary.csv` | PRESENT | 1385 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-063-registry-openrouter-128-z-ai-glm-5-1/usage_by_family.csv` | PRESENT | 3210 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-063-registry-openrouter-128-z-ai-glm-5-1/usage_by_section.csv` | PRESENT | 5338 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-063-registry-openrouter-128-z-ai-glm-5-1/usage_by_question.csv` | PRESENT | 87324 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-063-registry-openrouter-128-z-ai-glm-5-1/usage_by_sample.csv` | PRESENT | 94724 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-063-registry-openrouter-128-z-ai-glm-5-1/failure_gallery.md` | PRESENT | 4704 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-3-5-flash/summary.csv` | PRESENT | 1371 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-3-5-flash/usage_by_family.csv` | PRESENT | 3043 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-3-5-flash/usage_by_section.csv` | PRESENT | 5747 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-3-5-flash/usage_by_question.csv` | PRESENT | 89811 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-3-5-flash/usage_by_sample.csv` | PRESENT | 99971 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-3-5-flash/failure_gallery.md` | PRESENT | 19686 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-005-openai-gpt-5-5-xhigh/summary.csv` | PRESENT | 1217 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-005-openai-gpt-5-5-xhigh/usage_by_family.csv` | PRESENT | 2780 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-005-openai-gpt-5-5-xhigh/usage_by_section.csv` | PRESENT | 4680 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-005-openai-gpt-5-5-xhigh/usage_by_question.csv` | PRESENT | 79521 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-005-openai-gpt-5-5-xhigh/usage_by_sample.csv` | PRESENT | 88246 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-005-openai-gpt-5-5-xhigh/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/summary.csv` | PRESENT | 1387 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/usage_by_family.csv` | PRESENT | 3361 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/usage_by_section.csv` | PRESENT | 5907 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/usage_by_question.csv` | PRESENT | 96670 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/usage_by_sample.csv` | PRESENT | 105001 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/failure_gallery.md` | PRESENT | 1151 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/summary.csv` | PRESENT | 1392 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/usage_by_family.csv` | PRESENT | 3505 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/usage_by_section.csv` | PRESENT | 5765 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/usage_by_question.csv` | PRESENT | 92655 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/usage_by_sample.csv` | PRESENT | 100028 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/failure_gallery.md` | PRESENT | 1897 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-006-openai-gpt-5-4-nano-xhigh/summary.csv` | PRESENT | 1330 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-006-openai-gpt-5-4-nano-xhigh/usage_by_family.csv` | PRESENT | 2799 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-006-openai-gpt-5-4-nano-xhigh/usage_by_section.csv` | PRESENT | 5288 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-006-openai-gpt-5-4-nano-xhigh/usage_by_question.csv` | PRESENT | 84667 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-006-openai-gpt-5-4-nano-xhigh/usage_by_sample.csv` | PRESENT | 91399 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-006-openai-gpt-5-4-nano-xhigh/failure_gallery.md` | PRESENT | 7242 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-039-registry-openrouter-080-minimax-minimax-m3/summary.csv` | PRESENT | 1314 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-039-registry-openrouter-080-minimax-minimax-m3/usage_by_family.csv` | PRESENT | 3187 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-039-registry-openrouter-080-minimax-minimax-m3/usage_by_section.csv` | PRESENT | 6026 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-039-registry-openrouter-080-minimax-minimax-m3/usage_by_question.csv` | PRESENT | 99958 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-039-registry-openrouter-080-minimax-minimax-m3/usage_by_sample.csv` | PRESENT | 103258 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-039-registry-openrouter-080-minimax-minimax-m3/failure_gallery.md` | PRESENT | 6058 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-044-openrouter-032-stepfun-step-3-5-flash/summary.csv` | PRESENT | 1402 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-044-openrouter-032-stepfun-step-3-5-flash/usage_by_family.csv` | PRESENT | 3420 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-044-openrouter-032-stepfun-step-3-5-flash/usage_by_section.csv` | PRESENT | 6503 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-044-openrouter-032-stepfun-step-3-5-flash/usage_by_question.csv` | PRESENT | 98582 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-044-openrouter-032-stepfun-step-3-5-flash/usage_by_sample.csv` | PRESENT | 103364 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-044-openrouter-032-stepfun-step-3-5-flash/failure_gallery.md` | PRESENT | 5014 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/summary.csv` | PRESENT | 1402 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/usage_by_family.csv` | PRESENT | 3467 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/usage_by_section.csv` | PRESENT | 6498 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/usage_by_question.csv` | PRESENT | 98095 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/usage_by_sample.csv` | PRESENT | 102781 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/failure_gallery.md` | PRESENT | 5302 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-056-registry-gemini-2-5-flash/summary.csv` | PRESENT | 1380 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-056-registry-gemini-2-5-flash/usage_by_family.csv` | PRESENT | 3138 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-056-registry-gemini-2-5-flash/usage_by_section.csv` | PRESENT | 5294 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-056-registry-gemini-2-5-flash/usage_by_question.csv` | PRESENT | 85854 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-056-registry-gemini-2-5-flash/usage_by_sample.csv` | PRESENT | 94809 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-056-registry-gemini-2-5-flash/failure_gallery.md` | PRESENT | 23513 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/summary.csv` | PRESENT | 1417 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/usage_by_family.csv` | PRESENT | 3615 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/usage_by_section.csv` | PRESENT | 6856 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/usage_by_question.csv` | PRESENT | 103073 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/usage_by_sample.csv` | PRESENT | 107964 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/failure_gallery.md` | PRESENT | 8572 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-098-thinking-openrouter-qwen-qwen3-6-flash-low/summary.csv` | PRESENT | 1396 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-098-thinking-openrouter-qwen-qwen3-6-flash-low/usage_by_family.csv` | PRESENT | 3425 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-098-thinking-openrouter-qwen-qwen3-6-flash-low/usage_by_section.csv` | PRESENT | 5606 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-098-thinking-openrouter-qwen-qwen3-6-flash-low/usage_by_question.csv` | PRESENT | 90103 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-098-thinking-openrouter-qwen-qwen3-6-flash-low/usage_by_sample.csv` | PRESENT | 97498 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-098-thinking-openrouter-qwen-qwen3-6-flash-low/failure_gallery.md` | PRESENT | 5463 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-064-registry-openrouter-161-moonshotai-kimi-latest/summary.csv` | PRESENT | 1395 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-064-registry-openrouter-161-moonshotai-kimi-latest/usage_by_family.csv` | PRESENT | 3467 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-064-registry-openrouter-161-moonshotai-kimi-latest/usage_by_section.csv` | PRESENT | 5713 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-064-registry-openrouter-161-moonshotai-kimi-latest/usage_by_question.csv` | PRESENT | 91974 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-064-registry-openrouter-161-moonshotai-kimi-latest/usage_by_sample.csv` | PRESENT | 99597 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-064-registry-openrouter-161-moonshotai-kimi-latest/failure_gallery.md` | PRESENT | 5097 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-010-openai-gpt-5-4-xhigh/summary.csv` | PRESENT | 1315 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-010-openai-gpt-5-4-xhigh/usage_by_family.csv` | PRESENT | 2734 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-010-openai-gpt-5-4-xhigh/usage_by_section.csv` | PRESENT | 4702 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-010-openai-gpt-5-4-xhigh/usage_by_question.csv` | PRESENT | 79572 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-010-openai-gpt-5-4-xhigh/usage_by_sample.csv` | PRESENT | 88362 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-010-openai-gpt-5-4-xhigh/failure_gallery.md` | PRESENT | 1850 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/summary.csv` | PRESENT | 1435 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/usage_by_family.csv` | PRESENT | 3641 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/usage_by_section.csv` | PRESENT | 6856 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/usage_by_question.csv` | PRESENT | 103666 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/usage_by_sample.csv` | PRESENT | 108411 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/failure_gallery.md` | PRESENT | 17767 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/summary.csv` | PRESENT | 1409 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/usage_by_family.csv` | PRESENT | 3489 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/usage_by_section.csv` | PRESENT | 5813 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/usage_by_question.csv` | PRESENT | 93386 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/usage_by_sample.csv` | PRESENT | 100886 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/failure_gallery.md` | PRESENT | 4897 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-030-openrouter-google-gemini-3-5-flash-medium/summary.csv` | PRESENT | 1349 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-030-openrouter-google-gemini-3-5-flash-medium/usage_by_family.csv` | PRESENT | 3110 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-030-openrouter-google-gemini-3-5-flash-medium/usage_by_section.csv` | PRESENT | 5347 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-030-openrouter-google-gemini-3-5-flash-medium/usage_by_question.csv` | PRESENT | 89155 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-030-openrouter-google-gemini-3-5-flash-medium/usage_by_sample.csv` | PRESENT | 97904 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-030-openrouter-google-gemini-3-5-flash-medium/failure_gallery.md` | PRESENT | 2918 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/summary.csv` | PRESENT | 1401 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/usage_by_family.csv` | PRESENT | 3461 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/usage_by_section.csv` | PRESENT | 5709 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/usage_by_question.csv` | PRESENT | 91783 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/usage_by_sample.csv` | PRESENT | 99156 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/failure_gallery.md` | PRESENT | 2743 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/summary.csv` | PRESENT | 1411 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/usage_by_family.csv` | PRESENT | 3606 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/usage_by_section.csv` | PRESENT | 6012 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/usage_by_question.csv` | PRESENT | 96337 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/usage_by_sample.csv` | PRESENT | 103697 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/failure_gallery.md` | PRESENT | 3974 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-034-openrouter-048-openai-gpt-oss-120b/summary.csv` | PRESENT | 1561 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-034-openrouter-048-openai-gpt-oss-120b/usage_by_family.csv` | PRESENT | 4469 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-034-openrouter-048-openai-gpt-oss-120b/usage_by_section.csv` | PRESENT | 7767 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-034-openrouter-048-openai-gpt-oss-120b/usage_by_question.csv` | PRESENT | 97287 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-034-openrouter-048-openai-gpt-oss-120b/usage_by_sample.csv` | PRESENT | 102819 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-034-openrouter-048-openai-gpt-oss-120b/failure_gallery.md` | PRESENT | 9014 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-gpt-oss-20b/summary.csv` | PRESENT | 1510 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-gpt-oss-20b/usage_by_family.csv` | PRESENT | 4177 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-gpt-oss-20b/usage_by_section.csv` | PRESENT | 7647 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-gpt-oss-20b/usage_by_question.csv` | PRESENT | 96359 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-gpt-oss-20b/usage_by_sample.csv` | PRESENT | 104220 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-gpt-oss-20b/failure_gallery.md` | PRESENT | 20872 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-088-thinking-openai-gpt-5-nano-low/summary.csv` | PRESENT | 1322 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-088-thinking-openai-gpt-5-nano-low/usage_by_family.csv` | PRESENT | 2770 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-088-thinking-openai-gpt-5-nano-low/usage_by_section.csv` | PRESENT | 4724 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-088-thinking-openai-gpt-5-nano-low/usage_by_question.csv` | PRESENT | 79784 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-088-thinking-openai-gpt-5-nano-low/usage_by_sample.csv` | PRESENT | 89610 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-088-thinking-openai-gpt-5-nano-low/failure_gallery.md` | PRESENT | 12011 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-090-thinking-openai-gpt-5-nano-medium/summary.csv` | PRESENT | 1304 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-090-thinking-openai-gpt-5-nano-medium/usage_by_family.csv` | PRESENT | 2753 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-090-thinking-openai-gpt-5-nano-medium/usage_by_section.csv` | PRESENT | 4818 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-090-thinking-openai-gpt-5-nano-medium/usage_by_question.csv` | PRESENT | 81637 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-090-thinking-openai-gpt-5-nano-medium/usage_by_sample.csv` | PRESENT | 91288 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-090-thinking-openai-gpt-5-nano-medium/failure_gallery.md` | PRESENT | 4560 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-039-openrouter-059-qwen-qwen3-14b/summary.csv` | PRESENT | 1389 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-039-openrouter-059-qwen-qwen3-14b/usage_by_family.csv` | PRESENT | 3339 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-039-openrouter-059-qwen-qwen3-14b/usage_by_section.csv` | PRESENT | 6350 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-039-openrouter-059-qwen-qwen3-14b/usage_by_question.csv` | PRESENT | 94907 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-039-openrouter-059-qwen-qwen3-14b/usage_by_sample.csv` | PRESENT | 99871 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-039-openrouter-059-qwen-qwen3-14b/failure_gallery.md` | PRESENT | 10907 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-016-registry-openrouter-163-xiaomi-mimo-v2-5/summary.csv` | PRESENT | 1407 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-016-registry-openrouter-163-xiaomi-mimo-v2-5/usage_by_family.csv` | PRESENT | 3291 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-016-registry-openrouter-163-xiaomi-mimo-v2-5/usage_by_section.csv` | PRESENT | 5475 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-016-registry-openrouter-163-xiaomi-mimo-v2-5/usage_by_question.csv` | PRESENT | 89369 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-016-registry-openrouter-163-xiaomi-mimo-v2-5/usage_by_sample.csv` | PRESENT | 96857 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-016-registry-openrouter-163-xiaomi-mimo-v2-5/failure_gallery.md` | PRESENT | 9416 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-004-openai-gpt-5-4-mini-medium/summary.csv` | PRESENT | 1330 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-004-openai-gpt-5-4-mini-medium/usage_by_family.csv` | PRESENT | 2762 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-004-openai-gpt-5-4-mini-medium/usage_by_section.csv` | PRESENT | 5254 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-004-openai-gpt-5-4-mini-medium/usage_by_question.csv` | PRESENT | 85105 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-004-openai-gpt-5-4-mini-medium/usage_by_sample.csv` | PRESENT | 91860 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-004-openai-gpt-5-4-mini-medium/failure_gallery.md` | PRESENT | 6882 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-061-openrouter-057-qwen-qwen3-30b-a3b/summary.csv` | PRESENT | 1393 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-061-openrouter-057-qwen-qwen3-30b-a3b/usage_by_family.csv` | PRESENT | 3437 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-061-openrouter-057-qwen-qwen3-30b-a3b/usage_by_section.csv` | PRESENT | 6412 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-061-openrouter-057-qwen-qwen3-30b-a3b/usage_by_question.csv` | PRESENT | 96869 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-061-openrouter-057-qwen-qwen3-30b-a3b/usage_by_sample.csv` | PRESENT | 101585 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-061-openrouter-057-qwen-qwen3-30b-a3b/failure_gallery.md` | PRESENT | 2823 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-084-openrouter-040-minimax-minimax-m2/summary.csv` | PRESENT | 1400 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-084-openrouter-040-minimax-minimax-m2/usage_by_family.csv` | PRESENT | 3364 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-084-openrouter-040-minimax-minimax-m2/usage_by_section.csv` | PRESENT | 6377 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-084-openrouter-040-minimax-minimax-m2/usage_by_question.csv` | PRESENT | 96802 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-084-openrouter-040-minimax-minimax-m2/usage_by_sample.csv` | PRESENT | 101816 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-084-openrouter-040-minimax-minimax-m2/failure_gallery.md` | PRESENT | 11306 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-008-openai-gpt-5-4-medium/summary.csv` | PRESENT | 1305 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-008-openai-gpt-5-4-medium/usage_by_family.csv` | PRESENT | 2700 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-008-openai-gpt-5-4-medium/usage_by_section.csv` | PRESENT | 4662 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-008-openai-gpt-5-4-medium/usage_by_question.csv` | PRESENT | 79653 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-008-openai-gpt-5-4-medium/usage_by_sample.csv` | PRESENT | 88774 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-008-openai-gpt-5-4-medium/failure_gallery.md` | PRESENT | 3555 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-009-openai-gpt-5-4-high/summary.csv` | PRESENT | 1306 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-009-openai-gpt-5-4-high/usage_by_family.csv` | PRESENT | 2686 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-009-openai-gpt-5-4-high/usage_by_section.csv` | PRESENT | 4661 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-009-openai-gpt-5-4-high/usage_by_question.csv` | PRESENT | 79276 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-009-openai-gpt-5-4-high/usage_by_sample.csv` | PRESENT | 87939 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-009-openai-gpt-5-4-high/failure_gallery.md` | PRESENT | 4396 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-068-registry-openrouter-180-z-ai-glm-5-turbo/summary.csv` | PRESENT | 1386 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-068-registry-openrouter-180-z-ai-glm-5-turbo/usage_by_family.csv` | PRESENT | 3340 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-068-registry-openrouter-180-z-ai-glm-5-turbo/usage_by_section.csv` | PRESENT | 5447 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-068-registry-openrouter-180-z-ai-glm-5-turbo/usage_by_question.csv` | PRESENT | 88692 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-068-registry-openrouter-180-z-ai-glm-5-turbo/usage_by_sample.csv` | PRESENT | 96376 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-068-registry-openrouter-180-z-ai-glm-5-turbo/failure_gallery.md` | PRESENT | 5369 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-097-openrouter-129-z-ai-glm-5/summary.csv` | PRESENT | 1381 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-097-openrouter-129-z-ai-glm-5/usage_by_family.csv` | PRESENT | 3253 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-097-openrouter-129-z-ai-glm-5/usage_by_section.csv` | PRESENT | 6113 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-097-openrouter-129-z-ai-glm-5/usage_by_question.csv` | PRESENT | 93094 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-097-openrouter-129-z-ai-glm-5/usage_by_sample.csv` | PRESENT | 98146 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-097-openrouter-129-z-ai-glm-5/failure_gallery.md` | PRESENT | 15094 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-093-openrouter-136-z-ai-glm-4-6/summary.csv` | PRESENT | 1386 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-093-openrouter-136-z-ai-glm-4-6/usage_by_family.csv` | PRESENT | 3310 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-093-openrouter-136-z-ai-glm-4-6/usage_by_section.csv` | PRESENT | 6280 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-093-openrouter-136-z-ai-glm-4-6/usage_by_question.csv` | PRESENT | 94410 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-093-openrouter-136-z-ai-glm-4-6/usage_by_sample.csv` | PRESENT | 99643 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-093-openrouter-136-z-ai-glm-4-6/failure_gallery.md` | PRESENT | 22466 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-043-registry-openrouter-088-qwen-qwen3-5-27b/summary.csv` | PRESENT | 1393 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-043-registry-openrouter-088-qwen-qwen3-5-27b/usage_by_family.csv` | PRESENT | 3358 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-043-registry-openrouter-088-qwen-qwen3-5-27b/usage_by_section.csv` | PRESENT | 5519 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-043-registry-openrouter-088-qwen-qwen3-5-27b/usage_by_question.csv` | PRESENT | 89149 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-043-registry-openrouter-088-qwen-qwen3-5-27b/usage_by_sample.csv` | PRESENT | 96766 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-043-registry-openrouter-088-qwen-qwen3-5-27b/failure_gallery.md` | PRESENT | 21259 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-069-registry-openrouter-184-z-ai-glm-5v-turbo/summary.csv` | PRESENT | 1396 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-069-registry-openrouter-184-z-ai-glm-5v-turbo/usage_by_family.csv` | PRESENT | 3326 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-069-registry-openrouter-184-z-ai-glm-5v-turbo/usage_by_section.csv` | PRESENT | 5518 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-069-registry-openrouter-184-z-ai-glm-5v-turbo/usage_by_question.csv` | PRESENT | 89477 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-069-registry-openrouter-184-z-ai-glm-5v-turbo/usage_by_sample.csv` | PRESENT | 97446 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-069-registry-openrouter-184-z-ai-glm-5v-turbo/failure_gallery.md` | PRESENT | 21960 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-087-openrouter-135-prime-intellect-intellect-3/summary.csv` | PRESENT | 1425 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-087-openrouter-135-prime-intellect-intellect-3/usage_by_family.csv` | PRESENT | 3562 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-087-openrouter-135-prime-intellect-intellect-3/usage_by_section.csv` | PRESENT | 6774 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-087-openrouter-135-prime-intellect-intellect-3/usage_by_question.csv` | PRESENT | 101070 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-087-openrouter-135-prime-intellect-intellect-3/usage_by_sample.csv` | PRESENT | 105803 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-087-openrouter-135-prime-intellect-intellect-3/failure_gallery.md` | PRESENT | 11337 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-098-openrouter-146-z-ai-glm-4-5/summary.csv` | PRESENT | 1400 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-098-openrouter-146-z-ai-glm-4-5/usage_by_family.csv` | PRESENT | 3345 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-098-openrouter-146-z-ai-glm-4-5/usage_by_section.csv` | PRESENT | 6294 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-098-openrouter-146-z-ai-glm-4-5/usage_by_question.csv` | PRESENT | 94550 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-098-openrouter-146-z-ai-glm-4-5/usage_by_sample.csv` | PRESENT | 99610 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-098-openrouter-146-z-ai-glm-4-5/failure_gallery.md` | PRESENT | 22528 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/summary.csv` | PRESENT | 1400 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/usage_by_family.csv` | PRESENT | 3409 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/usage_by_section.csv` | PRESENT | 5661 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/usage_by_question.csv` | PRESENT | 91795 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/usage_by_sample.csv` | PRESENT | 99175 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/failure_gallery.md` | PRESENT | 7178 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-035-openrouter-027-deepseek-deepseek-v4-flash/summary.csv` | PRESENT | 1414 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-035-openrouter-027-deepseek-deepseek-v4-flash/usage_by_family.csv` | PRESENT | 3512 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-035-openrouter-027-deepseek-deepseek-v4-flash/usage_by_section.csv` | PRESENT | 6558 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-035-openrouter-027-deepseek-deepseek-v4-flash/usage_by_question.csv` | PRESENT | 103328 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-035-openrouter-027-deepseek-deepseek-v4-flash/usage_by_sample.csv` | PRESENT | 107231 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-035-openrouter-027-deepseek-deepseek-v4-flash/failure_gallery.md` | PRESENT | 13375 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-002-openai-gpt-5-4-nano-medium/summary.csv` | PRESENT | 1319 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-002-openai-gpt-5-4-nano-medium/usage_by_family.csv` | PRESENT | 2744 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-002-openai-gpt-5-4-nano-medium/usage_by_section.csv` | PRESENT | 5021 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-002-openai-gpt-5-4-nano-medium/usage_by_question.csv` | PRESENT | 83133 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-002-openai-gpt-5-4-nano-medium/usage_by_sample.csv` | PRESENT | 91819 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-002-openai-gpt-5-4-nano-medium/failure_gallery.md` | PRESENT | 13078 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-nemotron-3-nano/summary.csv` | PRESENT | 1421 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-nemotron-3-nano/usage_by_family.csv` | PRESENT | 3314 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-nemotron-3-nano/usage_by_section.csv` | PRESENT | 5974 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-nemotron-3-nano/usage_by_question.csv` | PRESENT | 89946 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-nemotron-3-nano/usage_by_sample.csv` | PRESENT | 103070 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-nemotron-3-nano/failure_gallery.md` | PRESENT | 26662 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/summary.csv` | PRESENT | 1408 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/usage_by_family.csv` | PRESENT | 3753 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/usage_by_section.csv` | PRESENT | 6248 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/usage_by_question.csv` | PRESENT | 99523 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/usage_by_sample.csv` | PRESENT | 107196 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/failure_gallery.md` | PRESENT | 7619 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/summary.csv` | PRESENT | 1363 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/usage_by_family.csv` | PRESENT | 3156 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/usage_by_section.csv` | PRESENT | 5447 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/usage_by_question.csv` | PRESENT | 90709 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/usage_by_sample.csv` | PRESENT | 99024 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/failure_gallery.md` | PRESENT | 9702 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-079-openrouter-125-deepseek-deepseek-v4-pro/summary.csv` | PRESENT | 1426 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-079-openrouter-125-deepseek-deepseek-v4-pro/usage_by_family.csv` | PRESENT | 3547 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-079-openrouter-125-deepseek-deepseek-v4-pro/usage_by_section.csv` | PRESENT | 6681 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-079-openrouter-125-deepseek-deepseek-v4-pro/usage_by_question.csv` | PRESENT | 98215 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-079-openrouter-125-deepseek-deepseek-v4-pro/usage_by_sample.csv` | PRESENT | 103718 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-079-openrouter-125-deepseek-deepseek-v4-pro/failure_gallery.md` | PRESENT | 17031 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-005-openai-gpt-5-4-mini-high/summary.csv` | PRESENT | 1327 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-005-openai-gpt-5-4-mini-high/usage_by_family.csv` | PRESENT | 2863 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-005-openai-gpt-5-4-mini-high/usage_by_section.csv` | PRESENT | 5318 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-005-openai-gpt-5-4-mini-high/usage_by_question.csv` | PRESENT | 84851 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-005-openai-gpt-5-4-mini-high/usage_by_sample.csv` | PRESENT | 90975 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-005-openai-gpt-5-4-mini-high/failure_gallery.md` | PRESENT | 3443 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/summary.csv` | PRESENT | 1409 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/usage_by_family.csv` | PRESENT | 3454 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/usage_by_section.csv` | PRESENT | 5767 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/usage_by_question.csv` | PRESENT | 92435 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/usage_by_sample.csv` | PRESENT | 100416 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/failure_gallery.md` | PRESENT | 22722 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-007-openai-gpt-5-4-low/summary.csv` | PRESENT | 1313 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-007-openai-gpt-5-4-low/usage_by_family.csv` | PRESENT | 2665 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-007-openai-gpt-5-4-low/usage_by_section.csv` | PRESENT | 4546 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-007-openai-gpt-5-4-low/usage_by_question.csv` | PRESENT | 78358 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-007-openai-gpt-5-4-low/usage_by_sample.csv` | PRESENT | 87406 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-007-openai-gpt-5-4-low/failure_gallery.md` | PRESENT | 5119 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-094-openrouter-131-z-ai-glm-4-7/summary.csv` | PRESENT | 1400 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-094-openrouter-131-z-ai-glm-4-7/usage_by_family.csv` | PRESENT | 3292 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-094-openrouter-131-z-ai-glm-4-7/usage_by_section.csv` | PRESENT | 6238 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-094-openrouter-131-z-ai-glm-4-7/usage_by_question.csv` | PRESENT | 94315 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-094-openrouter-131-z-ai-glm-4-7/usage_by_sample.csv` | PRESENT | 99503 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-094-openrouter-131-z-ai-glm-4-7/failure_gallery.md` | PRESENT | 22213 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-036-registry-openrouter-081-qwen-qwen3-6-flash/summary.csv` | PRESENT | 1386 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-036-registry-openrouter-081-qwen-qwen3-6-flash/usage_by_family.csv` | PRESENT | 3415 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-036-registry-openrouter-081-qwen-qwen3-6-flash/usage_by_section.csv` | PRESENT | 5556 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-036-registry-openrouter-081-qwen-qwen3-6-flash/usage_by_question.csv` | PRESENT | 90110 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-036-registry-openrouter-081-qwen-qwen3-6-flash/usage_by_sample.csv` | PRESENT | 97579 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-036-registry-openrouter-081-qwen-qwen3-6-flash/failure_gallery.md` | PRESENT | 6966 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/summary.csv` | PRESENT | 1387 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/usage_by_family.csv` | PRESENT | 3415 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/usage_by_section.csv` | PRESENT | 5627 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/usage_by_question.csv` | PRESENT | 90819 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/usage_by_sample.csv` | PRESENT | 98354 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/failure_gallery.md` | PRESENT | 7001 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-096-openrouter-061-qwen-qwen3-235b-a22b/summary.csv` | PRESENT | 1301 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-096-openrouter-061-qwen-qwen3-235b-a22b/usage_by_family.csv` | PRESENT | 2932 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-096-openrouter-061-qwen-qwen3-235b-a22b/usage_by_section.csv` | PRESENT | 5709 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-096-openrouter-061-qwen-qwen3-235b-a22b/usage_by_question.csv` | PRESENT | 82826 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-096-openrouter-061-qwen-qwen3-235b-a22b/usage_by_sample.csv` | PRESENT | 108373 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-096-openrouter-061-qwen-qwen3-235b-a22b/failure_gallery.md` | PRESENT | 12693 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-next-058-registry-grok-build-0-1/summary.csv` | PRESENT | 1316 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-next-058-registry-grok-build-0-1/usage_by_family.csv` | PRESENT | 2932 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-next-058-registry-grok-build-0-1/usage_by_section.csv` | PRESENT | 5591 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-next-058-registry-grok-build-0-1/usage_by_question.csv` | PRESENT | 92948 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-next-058-registry-grok-build-0-1/usage_by_sample.csv` | PRESENT | 98538 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-next-058-registry-grok-build-0-1/failure_gallery.md` | PRESENT | 23749 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-089-thinking-gemini-gemini-2-5-flash-lite-low/summary.csv` | PRESENT | 1401 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-089-thinking-gemini-gemini-2-5-flash-lite-low/usage_by_family.csv` | PRESENT | 3297 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-089-thinking-gemini-gemini-2-5-flash-lite-low/usage_by_section.csv` | PRESENT | 5426 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-089-thinking-gemini-gemini-2-5-flash-lite-low/usage_by_question.csv` | PRESENT | 87907 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-089-thinking-gemini-gemini-2-5-flash-lite-low/usage_by_sample.csv` | PRESENT | 97189 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-089-thinking-gemini-gemini-2-5-flash-lite-low/failure_gallery.md` | PRESENT | 22357 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-082-openrouter-034-minimax-minimax-m2-1/summary.csv` | PRESENT | 1401 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-082-openrouter-034-minimax-minimax-m2-1/usage_by_family.csv` | PRESENT | 3426 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-082-openrouter-034-minimax-minimax-m2-1/usage_by_section.csv` | PRESENT | 6486 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-082-openrouter-034-minimax-minimax-m2-1/usage_by_question.csv` | PRESENT | 97626 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-082-openrouter-034-minimax-minimax-m2-1/usage_by_sample.csv` | PRESENT | 102623 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-082-openrouter-034-minimax-minimax-m2-1/failure_gallery.md` | PRESENT | 9942 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-007-openai-gpt-5-4-mini-xhigh/summary.csv` | PRESENT | 1320 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-007-openai-gpt-5-4-mini-xhigh/usage_by_family.csv` | PRESENT | 2817 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-007-openai-gpt-5-4-mini-xhigh/usage_by_section.csv` | PRESENT | 5252 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-007-openai-gpt-5-4-mini-xhigh/usage_by_question.csv` | PRESENT | 85560 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-007-openai-gpt-5-4-mini-xhigh/usage_by_sample.csv` | PRESENT | 91508 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-overline-007-openai-gpt-5-4-mini-xhigh/failure_gallery.md` | PRESENT | 3607 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/summary.csv` | PRESENT | 1385 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/usage_by_family.csv` | PRESENT | 3443 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/usage_by_section.csv` | PRESENT | 5607 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/usage_by_question.csv` | PRESENT | 90855 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/usage_by_sample.csv` | PRESENT | 98356 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/failure_gallery.md` | PRESENT | 7123 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-paper-grok-4-3/summary.csv` | PRESENT | 1333 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-paper-grok-4-3/usage_by_family.csv` | PRESENT | 2886 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-paper-grok-4-3/usage_by_section.csv` | PRESENT | 5404 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-paper-grok-4-3/usage_by_question.csv` | PRESENT | 90527 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-paper-grok-4-3/usage_by_sample.csv` | PRESENT | 96351 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-repair3-xai-grok/runs/expand222-paper-grok-4-3/failure_gallery.md` | PRESENT | 25944 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-017-registry-openrouter-165-google-gemma-4-31b-it/summary.csv` | PRESENT | 1356 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-017-registry-openrouter-165-google-gemma-4-31b-it/usage_by_family.csv` | PRESENT | 2983 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-017-registry-openrouter-165-google-gemma-4-31b-it/usage_by_section.csv` | PRESENT | 5139 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-017-registry-openrouter-165-google-gemma-4-31b-it/usage_by_question.csv` | PRESENT | 84244 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-017-registry-openrouter-165-google-gemma-4-31b-it/usage_by_sample.csv` | PRESENT | 95102 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-017-registry-openrouter-165-google-gemma-4-31b-it/failure_gallery.md` | PRESENT | 21646 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1/summary.csv` | PRESENT | 1276 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1/usage_by_family.csv` | PRESENT | 2429 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1/usage_by_section.csv` | PRESENT | 4418 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1/usage_by_question.csv` | PRESENT | 76446 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1/usage_by_sample.csv` | PRESENT | 87049 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1/failure_gallery.md` | PRESENT | 22759 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/summary.csv` | PRESENT | 1397 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/usage_by_family.csv` | PRESENT | 3432 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/usage_by_section.csv` | PRESENT | 5718 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/usage_by_question.csv` | PRESENT | 92017 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/usage_by_sample.csv` | PRESENT | 99880 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/failure_gallery.md` | PRESENT | 21616 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-083-registry-anthropic-claude-opus-4-7/summary.csv` | PRESENT | 1292 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-083-registry-anthropic-claude-opus-4-7/usage_by_family.csv` | PRESENT | 2645 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-083-registry-anthropic-claude-opus-4-7/usage_by_section.csv` | PRESENT | 4635 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-083-registry-anthropic-claude-opus-4-7/usage_by_question.csv` | PRESENT | 80645 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-083-registry-anthropic-claude-opus-4-7/usage_by_sample.csv` | PRESENT | 90873 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-083-registry-anthropic-claude-opus-4-7/failure_gallery.md` | PRESENT | 8493 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-082-registry-anthropic-claude-opus-4-6/summary.csv` | PRESENT | 1308 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-082-registry-anthropic-claude-opus-4-6/usage_by_family.csv` | PRESENT | 2607 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-082-registry-anthropic-claude-opus-4-6/usage_by_section.csv` | PRESENT | 4596 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-082-registry-anthropic-claude-opus-4-6/usage_by_question.csv` | PRESENT | 80549 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-082-registry-anthropic-claude-opus-4-6/usage_by_sample.csv` | PRESENT | 91000 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-082-registry-anthropic-claude-opus-4-6/failure_gallery.md` | PRESENT | 16848 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-059-registry-openrouter-083-qwen-qwen3-6-27b/summary.csv` | PRESENT | 1330 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-059-registry-openrouter-083-qwen-qwen3-6-27b/usage_by_family.csv` | PRESENT | 3354 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-059-registry-openrouter-083-qwen-qwen3-6-27b/usage_by_section.csv` | PRESENT | 5498 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-059-registry-openrouter-083-qwen-qwen3-6-27b/usage_by_question.csv` | PRESENT | 88641 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-059-registry-openrouter-083-qwen-qwen3-6-27b/usage_by_sample.csv` | PRESENT | 96410 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-059-registry-openrouter-083-qwen-qwen3-6-27b/failure_gallery.md` | PRESENT | 12282 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/summary.csv` | PRESENT | 1402 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/usage_by_family.csv` | PRESENT | 3488 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/usage_by_section.csv` | PRESENT | 5814 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/usage_by_question.csv` | PRESENT | 93199 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/usage_by_sample.csv` | PRESENT | 100961 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/failure_gallery.md` | PRESENT | 53883 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/summary.csv` | PRESENT | 1408 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/usage_by_family.csv` | PRESENT | 3605 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/usage_by_section.csv` | PRESENT | 5944 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/usage_by_question.csv` | PRESENT | 95477 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/usage_by_sample.csv` | PRESENT | 103227 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/failure_gallery.md` | PRESENT | 23118 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-100-openrouter-142-moonshotai-kimi-k2-0905/summary.csv` | PRESENT | 1302 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-100-openrouter-142-moonshotai-kimi-k2-0905/usage_by_family.csv` | PRESENT | 2804 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-100-openrouter-142-moonshotai-kimi-k2-0905/usage_by_section.csv` | PRESENT | 5214 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-100-openrouter-142-moonshotai-kimi-k2-0905/usage_by_question.csv` | PRESENT | 85576 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-100-openrouter-142-moonshotai-kimi-k2-0905/usage_by_sample.csv` | PRESENT | 95728 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-100-openrouter-142-moonshotai-kimi-k2-0905/failure_gallery.md` | PRESENT | 21110 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-078-registry-openai-gpt-4o/summary.csv` | PRESENT | 1273 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-078-registry-openai-gpt-4o/usage_by_family.csv` | PRESENT | 2385 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-078-registry-openai-gpt-4o/usage_by_section.csv` | PRESENT | 4264 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-078-registry-openai-gpt-4o/usage_by_question.csv` | PRESENT | 75139 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-078-registry-openai-gpt-4o/usage_by_sample.csv` | PRESENT | 86419 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-078-registry-openai-gpt-4o/failure_gallery.md` | PRESENT | 22652 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-041-openrouter-060-qwen-qwen3-32b/summary.csv` | PRESENT | 1403 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-041-openrouter-060-qwen-qwen3-32b/usage_by_family.csv` | PRESENT | 3254 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-041-openrouter-060-qwen-qwen3-32b/usage_by_section.csv` | PRESENT | 6293 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-041-openrouter-060-qwen-qwen3-32b/usage_by_question.csv` | PRESENT | 94986 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-041-openrouter-060-qwen-qwen3-32b/usage_by_sample.csv` | PRESENT | 100236 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-041-openrouter-060-qwen-qwen3-32b/failure_gallery.md` | PRESENT | 24099 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-097-thinking-gemini-gemini-2-5-flash-lite-medium/summary.csv` | PRESENT | 1281 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-097-thinking-gemini-gemini-2-5-flash-lite-medium/usage_by_family.csv` | PRESENT | 2834 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-097-thinking-gemini-gemini-2-5-flash-lite-medium/usage_by_section.csv` | PRESENT | 5067 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-097-thinking-gemini-gemini-2-5-flash-lite-medium/usage_by_question.csv` | PRESENT | 80640 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-097-thinking-gemini-gemini-2-5-flash-lite-medium/usage_by_sample.csv` | PRESENT | 102752 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-097-thinking-gemini-gemini-2-5-flash-lite-medium/failure_gallery.md` | PRESENT | 22562 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-086-registry-openai-gpt-5-5-none/summary.csv` | PRESENT | 1281 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-086-registry-openai-gpt-5-5-none/usage_by_family.csv` | PRESENT | 2478 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-086-registry-openai-gpt-5-5-none/usage_by_section.csv` | PRESENT | 4380 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-086-registry-openai-gpt-5-5-none/usage_by_question.csv` | PRESENT | 77443 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-086-registry-openai-gpt-5-5-none/usage_by_sample.csv` | PRESENT | 89491 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-086-registry-openai-gpt-5-5-none/failure_gallery.md` | PRESENT | 7045 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-013-anthropic-claude-opus-4-8-high/summary.csv` | PRESENT | 1350 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-013-anthropic-claude-opus-4-8-high/usage_by_family.csv` | PRESENT | 2695 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-013-anthropic-claude-opus-4-8-high/usage_by_section.csv` | PRESENT | 4967 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-013-anthropic-claude-opus-4-8-high/usage_by_question.csv` | PRESENT | 84092 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-013-anthropic-claude-opus-4-8-high/usage_by_sample.csv` | PRESENT | 93669 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-013-anthropic-claude-opus-4-8-high/failure_gallery.md` | PRESENT | 7506 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-011-anthropic-claude-opus-4-8-low/summary.csv` | PRESENT | 1336 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-011-anthropic-claude-opus-4-8-low/usage_by_family.csv` | PRESENT | 2721 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-011-anthropic-claude-opus-4-8-low/usage_by_section.csv` | PRESENT | 5022 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-011-anthropic-claude-opus-4-8-low/usage_by_question.csv` | PRESENT | 83783 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-011-anthropic-claude-opus-4-8-low/usage_by_sample.csv` | PRESENT | 93227 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-011-anthropic-claude-opus-4-8-low/failure_gallery.md` | PRESENT | 8391 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-012-anthropic-claude-opus-4-8-medium/summary.csv` | PRESENT | 1354 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-012-anthropic-claude-opus-4-8-medium/usage_by_family.csv` | PRESENT | 2715 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-012-anthropic-claude-opus-4-8-medium/usage_by_section.csv` | PRESENT | 5004 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-012-anthropic-claude-opus-4-8-medium/usage_by_question.csv` | PRESENT | 84446 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-012-anthropic-claude-opus-4-8-medium/usage_by_sample.csv` | PRESENT | 94567 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-012-anthropic-claude-opus-4-8-medium/failure_gallery.md` | PRESENT | 8366 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-014-anthropic-claude-opus-4-8-xhigh/summary.csv` | PRESENT | 1352 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-014-anthropic-claude-opus-4-8-xhigh/usage_by_family.csv` | PRESENT | 2777 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-014-anthropic-claude-opus-4-8-xhigh/usage_by_section.csv` | PRESENT | 5080 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-014-anthropic-claude-opus-4-8-xhigh/usage_by_question.csv` | PRESENT | 84463 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-014-anthropic-claude-opus-4-8-xhigh/usage_by_sample.csv` | PRESENT | 94119 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-014-anthropic-claude-opus-4-8-xhigh/failure_gallery.md` | PRESENT | 7830 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-084-registry-anthropic-claude-opus-4-8/summary.csv` | PRESENT | 1289 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-084-registry-anthropic-claude-opus-4-8/usage_by_family.csv` | PRESENT | 2632 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-084-registry-anthropic-claude-opus-4-8/usage_by_section.csv` | PRESENT | 4630 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-084-registry-anthropic-claude-opus-4-8/usage_by_question.csv` | PRESENT | 80651 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-084-registry-anthropic-claude-opus-4-8/usage_by_sample.csv` | PRESENT | 90890 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-084-registry-anthropic-claude-opus-4-8/failure_gallery.md` | PRESENT | 7472 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-089-openrouter-031-minimax-minimax-m2-5/summary.csv` | PRESENT | 1497 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-089-openrouter-031-minimax-minimax-m2-5/usage_by_family.csv` | PRESENT | 4284 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-089-openrouter-031-minimax-minimax-m2-5/usage_by_section.csv` | PRESENT | 7965 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-089-openrouter-031-minimax-minimax-m2-5/usage_by_question.csv` | PRESENT | 102784 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-089-openrouter-031-minimax-minimax-m2-5/usage_by_sample.csv` | PRESENT | 107759 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-089-openrouter-031-minimax-minimax-m2-5/failure_gallery.md` | PRESENT | 7195 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/summary.csv` | PRESENT | 1401 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/usage_by_family.csv` | PRESENT | 3406 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/usage_by_section.csv` | PRESENT | 5632 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/usage_by_question.csv` | PRESENT | 90826 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/usage_by_sample.csv` | PRESENT | 98558 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/failure_gallery.md` | PRESENT | 21584 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-xiaomi-mimo-v2-flash/summary.csv` | PRESENT | 1312 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-xiaomi-mimo-v2-flash/usage_by_family.csv` | PRESENT | 2720 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-xiaomi-mimo-v2-flash/usage_by_section.csv` | PRESENT | 4999 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-xiaomi-mimo-v2-flash/usage_by_question.csv` | PRESENT | 84426 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-xiaomi-mimo-v2-flash/usage_by_sample.csv` | PRESENT | 94600 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-xiaomi-mimo-v2-flash/failure_gallery.md` | PRESENT | 21302 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-075-openrouter-130-qwen-qwen3-coder-next/summary.csv` | PRESENT | 1301 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-075-openrouter-130-qwen-qwen3-coder-next/usage_by_family.csv` | PRESENT | 2707 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-075-openrouter-130-qwen-qwen3-coder-next/usage_by_section.csv` | PRESENT | 4995 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-075-openrouter-130-qwen-qwen3-coder-next/usage_by_question.csv` | PRESENT | 84698 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-075-openrouter-130-qwen-qwen3-coder-next/usage_by_sample.csv` | PRESENT | 94913 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-075-openrouter-130-qwen-qwen3-coder-next/failure_gallery.md` | PRESENT | 21579 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-016-anthropic-claude-sonnet-4-6-low/summary.csv` | PRESENT | 1345 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-016-anthropic-claude-sonnet-4-6-low/usage_by_family.csv` | PRESENT | 2662 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-016-anthropic-claude-sonnet-4-6-low/usage_by_section.csv` | PRESENT | 4958 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-016-anthropic-claude-sonnet-4-6-low/usage_by_question.csv` | PRESENT | 84408 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-016-anthropic-claude-sonnet-4-6-low/usage_by_sample.csv` | PRESENT | 94387 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-016-anthropic-claude-sonnet-4-6-low/failure_gallery.md` | PRESENT | 21533 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-001-openai-gpt-5-5-none/summary.csv` | PRESENT | 1277 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-001-openai-gpt-5-5-none/usage_by_family.csv` | PRESENT | 2458 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-001-openai-gpt-5-5-none/usage_by_section.csv` | PRESENT | 4327 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-001-openai-gpt-5-5-none/usage_by_question.csv` | PRESENT | 76520 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-001-openai-gpt-5-5-none/usage_by_sample.csv` | PRESENT | 87750 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-001-openai-gpt-5-5-none/failure_gallery.md` | PRESENT | 9549 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-015-anthropic-claude-opus-4-8-max/summary.csv` | PRESENT | 1348 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-015-anthropic-claude-opus-4-8-max/usage_by_family.csv` | PRESENT | 2879 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-015-anthropic-claude-opus-4-8-max/usage_by_section.csv` | PRESENT | 5297 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-015-anthropic-claude-opus-4-8-max/usage_by_question.csv` | PRESENT | 85800 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-015-anthropic-claude-opus-4-8-max/usage_by_sample.csv` | PRESENT | 93394 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-015-anthropic-claude-opus-4-8-max/failure_gallery.md` | PRESENT | 7683 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/summary.csv` | PRESENT | 1324 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/usage_by_family.csv` | PRESENT | 2985 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/usage_by_section.csv` | PRESENT | 5169 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/usage_by_question.csv` | PRESENT | 85943 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/usage_by_sample.csv` | PRESENT | 96506 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/failure_gallery.md` | PRESENT | 18425 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-100-thinking-openrouter-openai-gpt-5-4-nano-low/summary.csv` | PRESENT | 1391 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-100-thinking-openrouter-openai-gpt-5-4-nano-low/usage_by_family.csv` | PRESENT | 3154 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-100-thinking-openrouter-openai-gpt-5-4-nano-low/usage_by_section.csv` | PRESENT | 5362 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-100-thinking-openrouter-openai-gpt-5-4-nano-low/usage_by_question.csv` | PRESENT | 86384 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-100-thinking-openrouter-openai-gpt-5-4-nano-low/usage_by_sample.csv` | PRESENT | 96734 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-100-thinking-openrouter-openai-gpt-5-4-nano-low/failure_gallery.md` | PRESENT | 21968 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/summary.csv` | PRESENT | 1327 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/usage_by_family.csv` | PRESENT | 2778 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/usage_by_section.csv` | PRESENT | 5021 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/usage_by_question.csv` | PRESENT | 86134 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/usage_by_sample.csv` | PRESENT | 98163 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/failure_gallery.md` | PRESENT | 15296 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-081-registry-openai-gpt-5-4-none/summary.csv` | PRESENT | 1275 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-081-registry-openai-gpt-5-4-none/usage_by_family.csv` | PRESENT | 2514 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-081-registry-openai-gpt-5-4-none/usage_by_section.csv` | PRESENT | 4406 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-081-registry-openai-gpt-5-4-none/usage_by_question.csv` | PRESENT | 77537 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-081-registry-openai-gpt-5-4-none/usage_by_sample.csv` | PRESENT | 89634 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-081-registry-openai-gpt-5-4-none/failure_gallery.md` | PRESENT | 10182 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-017-anthropic-claude-sonnet-4-6-medium/summary.csv` | PRESENT | 1362 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-017-anthropic-claude-sonnet-4-6-medium/usage_by_family.csv` | PRESENT | 2734 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-017-anthropic-claude-sonnet-4-6-medium/usage_by_section.csv` | PRESENT | 5019 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-017-anthropic-claude-sonnet-4-6-medium/usage_by_question.csv` | PRESENT | 85783 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-017-anthropic-claude-sonnet-4-6-medium/usage_by_sample.csv` | PRESENT | 95626 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-017-anthropic-claude-sonnet-4-6-medium/failure_gallery.md` | PRESENT | 14735 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-077-registry-openai-gpt-5-minimal/summary.csv` | PRESENT | 1243 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-077-registry-openai-gpt-5-minimal/usage_by_family.csv` | PRESENT | 2495 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-077-registry-openai-gpt-5-minimal/usage_by_section.csv` | PRESENT | 4380 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-077-registry-openai-gpt-5-minimal/usage_by_question.csv` | PRESENT | 77428 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-077-registry-openai-gpt-5-minimal/usage_by_sample.csv` | PRESENT | 90311 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-077-registry-openai-gpt-5-minimal/failure_gallery.md` | PRESENT | 16848 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-018-anthropic-claude-sonnet-4-6-high/summary.csv` | PRESENT | 1347 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-018-anthropic-claude-sonnet-4-6-high/usage_by_family.csv` | PRESENT | 2870 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-018-anthropic-claude-sonnet-4-6-high/usage_by_section.csv` | PRESENT | 5301 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-018-anthropic-claude-sonnet-4-6-high/usage_by_question.csv` | PRESENT | 88548 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-018-anthropic-claude-sonnet-4-6-high/usage_by_sample.csv` | PRESENT | 95354 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-018-anthropic-claude-sonnet-4-6-high/failure_gallery.md` | PRESENT | 31524 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-sonnet-4-6/summary.csv` | PRESENT | 1301 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-sonnet-4-6/usage_by_family.csv` | PRESENT | 2619 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-sonnet-4-6/usage_by_section.csv` | PRESENT | 4869 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-sonnet-4-6/usage_by_question.csv` | PRESENT | 82502 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-sonnet-4-6/usage_by_sample.csv` | PRESENT | 92638 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-sonnet-4-6/failure_gallery.md` | PRESENT | 21630 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-053-registry-openrouter-173-z-ai-glm-4-5v/summary.csv` | PRESENT | 1402 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-053-registry-openrouter-173-z-ai-glm-4-5v/usage_by_family.csv` | PRESENT | 3175 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-053-registry-openrouter-173-z-ai-glm-4-5v/usage_by_section.csv` | PRESENT | 5344 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-053-registry-openrouter-173-z-ai-glm-4-5v/usage_by_question.csv` | PRESENT | 87323 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-053-registry-openrouter-173-z-ai-glm-4-5v/usage_by_sample.csv` | PRESENT | 96103 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-053-registry-openrouter-173-z-ai-glm-4-5v/failure_gallery.md` | PRESENT | 33099 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-051-openrouter-033-z-ai-glm-4-7-flash/summary.csv` | PRESENT | 1394 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-051-openrouter-033-z-ai-glm-4-7-flash/usage_by_family.csv` | PRESENT | 3364 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-051-openrouter-033-z-ai-glm-4-7-flash/usage_by_section.csv` | PRESENT | 6431 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-051-openrouter-033-z-ai-glm-4-7-flash/usage_by_question.csv` | PRESENT | 96560 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-051-openrouter-033-z-ai-glm-4-7-flash/usage_by_sample.csv` | PRESENT | 101816 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-051-openrouter-033-z-ai-glm-4-7-flash/failure_gallery.md` | PRESENT | 16695 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-090-openrouter-028-minimax-minimax-m2-7/summary.csv` | PRESENT | 1489 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-090-openrouter-028-minimax-minimax-m2-7/usage_by_family.csv` | PRESENT | 4263 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-090-openrouter-028-minimax-minimax-m2-7/usage_by_section.csv` | PRESENT | 7903 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-090-openrouter-028-minimax-minimax-m2-7/usage_by_question.csv` | PRESENT | 99846 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-090-openrouter-028-minimax-minimax-m2-7/usage_by_sample.csv` | PRESENT | 105061 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-090-openrouter-028-minimax-minimax-m2-7/failure_gallery.md` | PRESENT | 21130 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-078-openrouter-147-z-ai-glm-4-5-air/summary.csv` | PRESENT | 1398 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-078-openrouter-147-z-ai-glm-4-5-air/usage_by_family.csv` | PRESENT | 3367 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-078-openrouter-147-z-ai-glm-4-5-air/usage_by_section.csv` | PRESENT | 6329 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-078-openrouter-147-z-ai-glm-4-5-air/usage_by_question.csv` | PRESENT | 94118 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-078-openrouter-147-z-ai-glm-4-5-air/usage_by_sample.csv` | PRESENT | 100400 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-078-openrouter-147-z-ai-glm-4-5-air/failure_gallery.md` | PRESENT | 22273 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1-mini/summary.csv` | PRESENT | 1247 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1-mini/usage_by_family.csv` | PRESENT | 2491 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1-mini/usage_by_section.csv` | PRESENT | 4684 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1-mini/usage_by_question.csv` | PRESENT | 78753 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1-mini/usage_by_sample.csv` | PRESENT | 88858 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-4-1-mini/failure_gallery.md` | PRESENT | 20706 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/summary.csv` | PRESENT | 1313 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/usage_by_family.csv` | PRESENT | 2782 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/usage_by_section.csv` | PRESENT | 5382 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/usage_by_question.csv` | PRESENT | 88740 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/usage_by_sample.csv` | PRESENT | 98492 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/failure_gallery.md` | PRESENT | 21971 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/summary.csv` | PRESENT | 1365 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/usage_by_family.csv` | PRESENT | 3190 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/usage_by_section.csv` | PRESENT | 5755 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/usage_by_question.csv` | PRESENT | 87689 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/usage_by_sample.csv` | PRESENT | 97936 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/failure_gallery.md` | PRESENT | 21805 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-025-registry-openrouter-085-mistralai-mistral-small-2603/summary.csv` | PRESENT | 1330 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-025-registry-openrouter-085-mistralai-mistral-small-2603/usage_by_family.csv` | PRESENT | 2767 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-025-registry-openrouter-085-mistralai-mistral-small-2603/usage_by_section.csv` | PRESENT | 5044 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-025-registry-openrouter-085-mistralai-mistral-small-2603/usage_by_question.csv` | PRESENT | 86619 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-025-registry-openrouter-085-mistralai-mistral-small-2603/usage_by_sample.csv` | PRESENT | 98193 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-025-registry-openrouter-085-mistralai-mistral-small-2603/failure_gallery.md` | PRESENT | 21557 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-qwen3-next/summary.csv` | PRESENT | 1325 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-qwen3-next/usage_by_family.csv` | PRESENT | 2874 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-qwen3-next/usage_by_section.csv` | PRESENT | 5455 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-qwen3-next/usage_by_question.csv` | PRESENT | 89569 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-qwen3-next/usage_by_sample.csv` | PRESENT | 100247 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openrouter-qwen3-next/failure_gallery.md` | PRESENT | 24065 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-099-openrouter-149-moonshotai-kimi-k2/summary.csv` | PRESENT | 1225 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-099-openrouter-149-moonshotai-kimi-k2/usage_by_family.csv` | PRESENT | 2424 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-099-openrouter-149-moonshotai-kimi-k2/usage_by_section.csv` | PRESENT | 4626 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-099-openrouter-149-moonshotai-kimi-k2/usage_by_question.csv` | PRESENT | 81289 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-099-openrouter-149-moonshotai-kimi-k2/usage_by_sample.csv` | PRESENT | 98388 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-099-openrouter-149-moonshotai-kimi-k2/failure_gallery.md` | PRESENT | 20843 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-062-registry-openrouter-144-nousresearch-hermes-4-405b/summary.csv` | PRESENT | 1317 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-062-registry-openrouter-144-nousresearch-hermes-4-405b/usage_by_family.csv` | PRESENT | 2748 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-062-registry-openrouter-144-nousresearch-hermes-4-405b/usage_by_section.csv` | PRESENT | 4978 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-062-registry-openrouter-144-nousresearch-hermes-4-405b/usage_by_question.csv` | PRESENT | 85739 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-062-registry-openrouter-144-nousresearch-hermes-4-405b/usage_by_sample.csv` | PRESENT | 96538 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-062-registry-openrouter-144-nousresearch-hermes-4-405b/failure_gallery.md` | PRESENT | 21413 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-haiku-4-5/summary.csv` | PRESENT | 1285 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-haiku-4-5/usage_by_family.csv` | PRESENT | 2576 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-haiku-4-5/usage_by_section.csv` | PRESENT | 4813 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-haiku-4-5/usage_by_question.csv` | PRESENT | 81842 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-haiku-4-5/usage_by_sample.csv` | PRESENT | 92522 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-anthropic-claude-haiku-4-5/failure_gallery.md` | PRESENT | 22501 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-076-registry-openrouter-181-ai21-jamba-large-1-7/summary.csv` | PRESENT | 1309 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-076-registry-openrouter-181-ai21-jamba-large-1-7/usage_by_family.csv` | PRESENT | 2705 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-076-registry-openrouter-181-ai21-jamba-large-1-7/usage_by_section.csv` | PRESENT | 4796 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-076-registry-openrouter-181-ai21-jamba-large-1-7/usage_by_question.csv` | PRESENT | 83008 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-076-registry-openrouter-181-ai21-jamba-large-1-7/usage_by_sample.csv` | PRESENT | 95024 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-076-registry-openrouter-181-ai21-jamba-large-1-7/failure_gallery.md` | PRESENT | 21085 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/summary.csv` | PRESENT | 1299 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/usage_by_family.csv` | PRESENT | 2843 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/usage_by_section.csv` | PRESENT | 5082 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/usage_by_question.csv` | PRESENT | 86859 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/usage_by_sample.csv` | PRESENT | 97620 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/failure_gallery.md` | PRESENT | 25540 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-019-anthropic-claude-sonnet-4-6-max/summary.csv` | PRESENT | 1344 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-019-anthropic-claude-sonnet-4-6-max/usage_by_family.csv` | PRESENT | 2899 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-019-anthropic-claude-sonnet-4-6-max/usage_by_section.csv` | PRESENT | 5498 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-019-anthropic-claude-sonnet-4-6-max/usage_by_question.csv` | PRESENT | 90674 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-019-anthropic-claude-sonnet-4-6-max/usage_by_sample.csv` | PRESENT | 95190 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-019-anthropic-claude-sonnet-4-6-max/failure_gallery.md` | PRESENT | 31889 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-2-5-flash-lite/summary.csv` | PRESENT | 1315 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-2-5-flash-lite/usage_by_family.csv` | PRESENT | 2594 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-2-5-flash-lite/usage_by_section.csv` | PRESENT | 4888 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-2-5-flash-lite/usage_by_question.csv` | PRESENT | 82589 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-2-5-flash-lite/usage_by_sample.csv` | PRESENT | 93403 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-gemini-2-5-flash-lite/failure_gallery.md` | PRESENT | 20417 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-072-openrouter-152-qwen-qwen-plus/summary.csv` | PRESENT | 1288 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-072-openrouter-152-qwen-qwen-plus/usage_by_family.csv` | PRESENT | 2600 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-072-openrouter-152-qwen-qwen-plus/usage_by_section.csv` | PRESENT | 4806 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-072-openrouter-152-qwen-qwen-plus/usage_by_question.csv` | PRESENT | 81645 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-072-openrouter-152-qwen-qwen-plus/usage_by_sample.csv` | PRESENT | 91842 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-072-openrouter-152-qwen-qwen-plus/failure_gallery.md` | PRESENT | 20740 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-051-registry-openrouter-092-mistralai-devstral-2512/summary.csv` | PRESENT | 1274 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-051-registry-openrouter-092-mistralai-devstral-2512/usage_by_family.csv` | PRESENT | 2755 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-051-registry-openrouter-092-mistralai-devstral-2512/usage_by_section.csv` | PRESENT | 4919 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-051-registry-openrouter-092-mistralai-devstral-2512/usage_by_question.csv` | PRESENT | 84495 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-051-registry-openrouter-092-mistralai-devstral-2512/usage_by_sample.csv` | PRESENT | 95953 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-051-registry-openrouter-092-mistralai-devstral-2512/failure_gallery.md` | PRESENT | 21030 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-099-thinking-openai-gpt-5-4-nano-low/summary.csv` | PRESENT | 1325 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-099-thinking-openai-gpt-5-4-nano-low/usage_by_family.csv` | PRESENT | 2722 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-099-thinking-openai-gpt-5-4-nano-low/usage_by_section.csv` | PRESENT | 4673 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-099-thinking-openai-gpt-5-4-nano-low/usage_by_question.csv` | PRESENT | 79706 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-099-thinking-openai-gpt-5-4-nano-low/usage_by_sample.csv` | PRESENT | 90060 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-099-thinking-openai-gpt-5-4-nano-low/failure_gallery.md` | PRESENT | 21563 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-092-thinking-openai-gpt-5-mini-minimal/summary.csv` | PRESENT | 1290 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-092-thinking-openai-gpt-5-mini-minimal/usage_by_family.csv` | PRESENT | 2530 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-092-thinking-openai-gpt-5-mini-minimal/usage_by_section.csv` | PRESENT | 4472 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-092-thinking-openai-gpt-5-mini-minimal/usage_by_question.csv` | PRESENT | 78540 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-092-thinking-openai-gpt-5-mini-minimal/usage_by_sample.csv` | PRESENT | 90879 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-092-thinking-openai-gpt-5-mini-minimal/failure_gallery.md` | PRESENT | 20299 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/summary.csv` | PRESENT | 1339 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/usage_by_family.csv` | PRESENT | 2955 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/usage_by_section.csv` | PRESENT | 5481 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/usage_by_question.csv` | PRESENT | 90992 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/usage_by_sample.csv` | PRESENT | 101320 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/failure_gallery.md` | PRESENT | 21979 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-035-registry-openrouter-113-minimax-minimax-01/summary.csv` | PRESENT | 1312 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-035-registry-openrouter-113-minimax-minimax-01/usage_by_family.csv` | PRESENT | 2669 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-035-registry-openrouter-113-minimax-minimax-01/usage_by_section.csv` | PRESENT | 4775 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-035-registry-openrouter-113-minimax-minimax-01/usage_by_question.csv` | PRESENT | 82658 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-035-registry-openrouter-113-minimax-minimax-01/usage_by_sample.csv` | PRESENT | 93360 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-035-registry-openrouter-113-minimax-minimax-01/failure_gallery.md` | PRESENT | 20952 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-080-registry-openai-gpt-5-2-none/summary.csv` | PRESENT | 1285 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-080-registry-openai-gpt-5-2-none/usage_by_family.csv` | PRESENT | 2492 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-080-registry-openai-gpt-5-2-none/usage_by_section.csv` | PRESENT | 4431 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-080-registry-openai-gpt-5-2-none/usage_by_question.csv` | PRESENT | 77611 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-080-registry-openai-gpt-5-2-none/usage_by_sample.csv` | PRESENT | 89792 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-080-registry-openai-gpt-5-2-none/failure_gallery.md` | PRESENT | 15694 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-050-openrouter-058-qwen-qwen3-8b/summary.csv` | PRESENT | 1289 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-050-openrouter-058-qwen-qwen3-8b/usage_by_family.csv` | PRESENT | 2642 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-050-openrouter-058-qwen-qwen3-8b/usage_by_section.csv` | PRESENT | 5124 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-050-openrouter-058-qwen-qwen3-8b/usage_by_question.csv` | PRESENT | 78687 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-050-openrouter-058-qwen-qwen3-8b/usage_by_sample.csv` | PRESENT | 101547 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-050-openrouter-058-qwen-qwen3-8b/failure_gallery.md` | PRESENT | 19746 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-006-openai-gpt-5-4-none/summary.csv` | PRESENT | 1267 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-006-openai-gpt-5-4-none/usage_by_family.csv` | PRESENT | 2496 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-006-openai-gpt-5-4-none/usage_by_section.csv` | PRESENT | 4354 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-006-openai-gpt-5-4-none/usage_by_question.csv` | PRESENT | 76639 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-006-openai-gpt-5-4-none/usage_by_sample.csv` | PRESENT | 87911 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-006-openai-gpt-5-4-none/failure_gallery.md` | PRESENT | 12592 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-045-registry-openrouter-171-mistralai-mistral-large-2512/summary.csv` | PRESENT | 1339 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-045-registry-openrouter-171-mistralai-mistral-large-2512/usage_by_family.csv` | PRESENT | 2808 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-045-registry-openrouter-171-mistralai-mistral-large-2512/usage_by_section.csv` | PRESENT | 5024 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-045-registry-openrouter-171-mistralai-mistral-large-2512/usage_by_question.csv` | PRESENT | 86648 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-045-registry-openrouter-171-mistralai-mistral-large-2512/usage_by_sample.csv` | PRESENT | 98040 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-045-registry-openrouter-171-mistralai-mistral-large-2512/failure_gallery.md` | PRESENT | 22016 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/summary.csv` | PRESENT | 1301 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/usage_by_family.csv` | PRESENT | 2655 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/usage_by_section.csv` | PRESENT | 4719 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/usage_by_question.csv` | PRESENT | 81836 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/usage_by_sample.csv` | PRESENT | 92373 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/failure_gallery.md` | PRESENT | 18746 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-002-registry-openrouter-110-google-gemma-3-12b-it/summary.csv` | PRESENT | 1326 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-002-registry-openrouter-110-google-gemma-3-12b-it/usage_by_family.csv` | PRESENT | 2740 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-002-registry-openrouter-110-google-gemma-3-12b-it/usage_by_section.csv` | PRESENT | 4871 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-002-registry-openrouter-110-google-gemma-3-12b-it/usage_by_question.csv` | PRESENT | 83575 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-002-registry-openrouter-110-google-gemma-3-12b-it/usage_by_sample.csv` | PRESENT | 94818 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-002-registry-openrouter-110-google-gemma-3-12b-it/failure_gallery.md` | PRESENT | 21028 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/summary.csv` | PRESENT | 1399 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/usage_by_family.csv` | PRESENT | 3012 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/usage_by_section.csv` | PRESENT | 5493 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/usage_by_question.csv` | PRESENT | 90100 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/usage_by_sample.csv` | PRESENT | 100686 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/failure_gallery.md` | PRESENT | 22299 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-5-nano-minimal/summary.csv` | PRESENT | 1269 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-5-nano-minimal/usage_by_family.csv` | PRESENT | 2518 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-5-nano-minimal/usage_by_section.csv` | PRESENT | 4677 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-5-nano-minimal/usage_by_question.csv` | PRESENT | 79536 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-5-nano-minimal/usage_by_sample.csv` | PRESENT | 91675 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-paper-openai-gpt-5-nano-minimal/failure_gallery.md` | PRESENT | 20121 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/summary.csv` | PRESENT | 1334 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/usage_by_family.csv` | PRESENT | 2837 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/usage_by_section.csv` | PRESENT | 5145 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/usage_by_question.csv` | PRESENT | 88593 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/usage_by_sample.csv` | PRESENT | 99442 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/failure_gallery.md` | PRESENT | 22345 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/summary.csv` | PRESENT | 1337 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_family.csv` | PRESENT | 2899 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_section.csv` | PRESENT | 5207 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_question.csv` | PRESENT | 88335 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_sample.csv` | PRESENT | 100465 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/failure_gallery.md` | PRESENT | 20314 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/summary.csv` | PRESENT | 1292 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_family.csv` | PRESENT | 2898 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_section.csv` | PRESENT | 5194 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_question.csv` | PRESENT | 88364 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_sample.csv` | PRESENT | 100429 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/failure_gallery.md` | PRESENT | 18582 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/summary.csv` | PRESENT | 1352 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/usage_by_family.csv` | PRESENT | 3037 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/usage_by_section.csv` | PRESENT | 5447 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/usage_by_question.csv` | PRESENT | 91949 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/usage_by_sample.csv` | PRESENT | 104044 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/failure_gallery.md` | PRESENT | 20000 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-042-registry-gemini-3-1-flash-lite/summary.csv` | PRESENT | 1298 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-042-registry-gemini-3-1-flash-lite/usage_by_family.csv` | PRESENT | 2605 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-042-registry-gemini-3-1-flash-lite/usage_by_section.csv` | PRESENT | 4876 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-042-registry-gemini-3-1-flash-lite/usage_by_question.csv` | PRESENT | 84175 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-042-registry-gemini-3-1-flash-lite/usage_by_sample.csv` | PRESENT | 93361 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-042-registry-gemini-3-1-flash-lite/failure_gallery.md` | PRESENT | 18790 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/summary.csv` | PRESENT | 1242 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/usage_by_family.csv` | PRESENT | 2546 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/usage_by_section.csv` | PRESENT | 4937 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/usage_by_question.csv` | PRESENT | 84061 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/usage_by_sample.csv` | PRESENT | 102810 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/failure_gallery.md` | PRESENT | 22745 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-095-openrouter-148-qwen-qwen3-coder/summary.csv` | PRESENT | 1368 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-095-openrouter-148-qwen-qwen3-coder/usage_by_family.csv` | PRESENT | 3055 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-095-openrouter-148-qwen-qwen3-coder/usage_by_section.csv` | PRESENT | 5712 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-095-openrouter-148-qwen-qwen3-coder/usage_by_question.csv` | PRESENT | 87952 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-095-openrouter-148-qwen-qwen3-coder/usage_by_sample.csv` | PRESENT | 98433 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-095-openrouter-148-qwen-qwen3-coder/failure_gallery.md` | PRESENT | 23132 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/summary.csv` | PRESENT | 1376 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/usage_by_family.csv` | PRESENT | 3062 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/usage_by_section.csv` | PRESENT | 5320 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/usage_by_question.csv` | PRESENT | 87106 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/usage_by_sample.csv` | PRESENT | 98020 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/failure_gallery.md` | PRESENT | 22558 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/summary.csv` | PRESENT | 1349 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/usage_by_family.csv` | PRESENT | 2884 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/usage_by_section.csv` | PRESENT | 5407 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/usage_by_question.csv` | PRESENT | 89933 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/usage_by_sample.csv` | PRESENT | 100478 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/failure_gallery.md` | PRESENT | 22445 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-061-registry-openrouter-139-qwen-qwen3-coder-plus/summary.csv` | PRESENT | 1329 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-061-registry-openrouter-139-qwen-qwen3-coder-plus/usage_by_family.csv` | PRESENT | 2698 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-061-registry-openrouter-139-qwen-qwen3-coder-plus/usage_by_section.csv` | PRESENT | 4780 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-061-registry-openrouter-139-qwen-qwen3-coder-plus/usage_by_question.csv` | PRESENT | 83589 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-061-registry-openrouter-139-qwen-qwen3-coder-plus/usage_by_sample.csv` | PRESENT | 94806 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-061-registry-openrouter-139-qwen-qwen3-coder-plus/failure_gallery.md` | PRESENT | 21793 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-047-registry-openai-gpt-5-mini-minimal/summary.csv` | PRESENT | 1305 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-047-registry-openai-gpt-5-mini-minimal/usage_by_family.csv` | PRESENT | 2574 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-047-registry-openai-gpt-5-mini-minimal/usage_by_section.csv` | PRESENT | 4610 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-047-registry-openai-gpt-5-mini-minimal/usage_by_question.csv` | PRESENT | 79410 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-047-registry-openai-gpt-5-mini-minimal/usage_by_sample.csv` | PRESENT | 92720 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-047-registry-openai-gpt-5-mini-minimal/failure_gallery.md` | PRESENT | 20676 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/summary.csv` | PRESENT | 1348 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/usage_by_family.csv` | PRESENT | 2876 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/usage_by_section.csv` | PRESENT | 5206 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/usage_by_question.csv` | PRESENT | 88335 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/usage_by_sample.csv` | PRESENT | 100002 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/failure_gallery.md` | PRESENT | 21635 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/summary.csv` | PRESENT | 1266 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/usage_by_family.csv` | PRESENT | 2784 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/usage_by_section.csv` | PRESENT | 5052 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/usage_by_question.csv` | PRESENT | 86644 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/usage_by_sample.csv` | PRESENT | 97652 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/failure_gallery.md` | PRESENT | 31276 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-030-openrouter-037-arcee-ai-trinity-mini/summary.csv` | PRESENT | 1401 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-030-openrouter-037-arcee-ai-trinity-mini/usage_by_family.csv` | PRESENT | 3431 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-030-openrouter-037-arcee-ai-trinity-mini/usage_by_section.csv` | PRESENT | 6495 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-030-openrouter-037-arcee-ai-trinity-mini/usage_by_question.csv` | PRESENT | 98271 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-030-openrouter-037-arcee-ai-trinity-mini/usage_by_sample.csv` | PRESENT | 104232 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-030-openrouter-037-arcee-ai-trinity-mini/failure_gallery.md` | PRESENT | 77488 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-074-registry-openrouter-185-mistralai-mistral-large-2407/summary.csv` | PRESENT | 1325 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-074-registry-openrouter-185-mistralai-mistral-large-2407/usage_by_family.csv` | PRESENT | 2788 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-074-registry-openrouter-185-mistralai-mistral-large-2407/usage_by_section.csv` | PRESENT | 5038 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-074-registry-openrouter-185-mistralai-mistral-large-2407/usage_by_question.csv` | PRESENT | 86529 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-074-registry-openrouter-185-mistralai-mistral-large-2407/usage_by_sample.csv` | PRESENT | 97970 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-074-registry-openrouter-185-mistralai-mistral-large-2407/failure_gallery.md` | PRESENT | 22022 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-024-openrouter-052-z-ai-glm-4-32b/summary.csv` | PRESENT | 1283 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-024-openrouter-052-z-ai-glm-4-32b/usage_by_family.csv` | PRESENT | 2594 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-024-openrouter-052-z-ai-glm-4-32b/usage_by_section.csv` | PRESENT | 4746 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-024-openrouter-052-z-ai-glm-4-32b/usage_by_question.csv` | PRESENT | 81136 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-024-openrouter-052-z-ai-glm-4-32b/usage_by_sample.csv` | PRESENT | 91704 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-024-openrouter-052-z-ai-glm-4-32b/failure_gallery.md` | PRESENT | 20279 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-054-openrouter-143-nousresearch-hermes-4-70b/summary.csv` | PRESENT | 1316 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-054-openrouter-143-nousresearch-hermes-4-70b/usage_by_family.csv` | PRESENT | 2770 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-054-openrouter-143-nousresearch-hermes-4-70b/usage_by_section.csv` | PRESENT | 5142 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-054-openrouter-143-nousresearch-hermes-4-70b/usage_by_question.csv` | PRESENT | 86484 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-054-openrouter-143-nousresearch-hermes-4-70b/usage_by_sample.csv` | PRESENT | 96852 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-054-openrouter-143-nousresearch-hermes-4-70b/failure_gallery.md` | PRESENT | 21628 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-027-registry-openrouter-176-mistralai-mistral-saba/summary.csv` | PRESENT | 1328 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-027-registry-openrouter-176-mistralai-mistral-saba/usage_by_family.csv` | PRESENT | 2709 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-027-registry-openrouter-176-mistralai-mistral-saba/usage_by_section.csv` | PRESENT | 4921 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-027-registry-openrouter-176-mistralai-mistral-saba/usage_by_question.csv` | PRESENT | 83822 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-027-registry-openrouter-176-mistralai-mistral-saba/usage_by_sample.csv` | PRESENT | 95552 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-027-registry-openrouter-176-mistralai-mistral-saba/failure_gallery.md` | PRESENT | 20726 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/summary.csv` | PRESENT | 1318 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/usage_by_family.csv` | PRESENT | 2723 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/usage_by_section.csv` | PRESENT | 5074 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/usage_by_question.csv` | PRESENT | 86543 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/usage_by_sample.csv` | PRESENT | 98187 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/failure_gallery.md` | PRESENT | 21033 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-054-registry-openrouter-175-mistralai-mistral-medium-3/summary.csv` | PRESENT | 1335 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-054-registry-openrouter-175-mistralai-mistral-medium-3/usage_by_family.csv` | PRESENT | 2700 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-054-registry-openrouter-175-mistralai-mistral-medium-3/usage_by_section.csv` | PRESENT | 5000 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-054-registry-openrouter-175-mistralai-mistral-medium-3/usage_by_question.csv` | PRESENT | 85695 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-054-registry-openrouter-175-mistralai-mistral-medium-3/usage_by_sample.csv` | PRESENT | 97445 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-054-registry-openrouter-175-mistralai-mistral-medium-3/failure_gallery.md` | PRESENT | 21600 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-079-registry-openrouter-182-cohere-command-a/summary.csv` | PRESENT | 1289 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-079-registry-openrouter-182-cohere-command-a/usage_by_family.csv` | PRESENT | 2617 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-079-registry-openrouter-182-cohere-command-a/usage_by_section.csv` | PRESENT | 4670 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-079-registry-openrouter-182-cohere-command-a/usage_by_question.csv` | PRESENT | 81298 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-079-registry-openrouter-182-cohere-command-a/usage_by_sample.csv` | PRESENT | 92228 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-079-registry-openrouter-182-cohere-command-a/failure_gallery.md` | PRESENT | 20337 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/summary.csv` | PRESENT | 1275 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/usage_by_family.csv` | PRESENT | 2800 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/usage_by_section.csv` | PRESENT | 5274 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/usage_by_question.csv` | PRESENT | 86645 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/usage_by_sample.csv` | PRESENT | 97439 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/failure_gallery.md` | PRESENT | 22314 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-027-openrouter-056-google-gemma-3n-e4b-it/summary.csv` | PRESENT | 1327 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-027-openrouter-056-google-gemma-3n-e4b-it/usage_by_family.csv` | PRESENT | 2765 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-027-openrouter-056-google-gemma-3n-e4b-it/usage_by_section.csv` | PRESENT | 5090 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-027-openrouter-056-google-gemma-3n-e4b-it/usage_by_question.csv` | PRESENT | 84994 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-027-openrouter-056-google-gemma-3n-e4b-it/usage_by_sample.csv` | PRESENT | 96002 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-027-openrouter-056-google-gemma-3n-e4b-it/failure_gallery.md` | PRESENT | 21010 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-019-registry-openai-gpt-4-1-nano/summary.csv` | PRESENT | 1284 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-019-registry-openai-gpt-4-1-nano/usage_by_family.csv` | PRESENT | 2494 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-019-registry-openai-gpt-4-1-nano/usage_by_section.csv` | PRESENT | 4398 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-019-registry-openai-gpt-4-1-nano/usage_by_question.csv` | PRESENT | 77499 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-019-registry-openai-gpt-4-1-nano/usage_by_sample.csv` | PRESENT | 88484 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-019-registry-openai-gpt-4-1-nano/failure_gallery.md` | PRESENT | 20425 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-026-registry-openrouter-106-meta-llama-llama-4-maverick/summary.csv` | PRESENT | 1347 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-026-registry-openrouter-106-meta-llama-llama-4-maverick/usage_by_family.csv` | PRESENT | 3051 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-026-registry-openrouter-106-meta-llama-llama-4-maverick/usage_by_section.csv` | PRESENT | 5362 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-026-registry-openrouter-106-meta-llama-llama-4-maverick/usage_by_question.csv` | PRESENT | 86651 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-026-registry-openrouter-106-meta-llama-llama-4-maverick/usage_by_sample.csv` | PRESENT | 98150 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-026-registry-openrouter-106-meta-llama-llama-4-maverick/failure_gallery.md` | PRESENT | 21582 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/summary.csv` | PRESENT | 1301 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/usage_by_family.csv` | PRESENT | 2807 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/usage_by_section.csv` | PRESENT | 5293 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/usage_by_question.csv` | PRESENT | 87421 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/usage_by_sample.csv` | PRESENT | 97735 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/failure_gallery.md` | PRESENT | 21324 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/summary.csv` | PRESENT | 1347 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/usage_by_family.csv` | PRESENT | 2916 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/usage_by_section.csv` | PRESENT | 5467 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/usage_by_question.csv` | PRESENT | 89224 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/usage_by_sample.csv` | PRESENT | 99570 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/failure_gallery.md` | PRESENT | 21870 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-034-registry-openrouter-174-mistralai-codestral-2508/summary.csv` | PRESENT | 1331 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-034-registry-openrouter-174-mistralai-codestral-2508/usage_by_family.csv` | PRESENT | 2733 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-034-registry-openrouter-174-mistralai-codestral-2508/usage_by_section.csv` | PRESENT | 4887 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-034-registry-openrouter-174-mistralai-codestral-2508/usage_by_question.csv` | PRESENT | 84736 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-034-registry-openrouter-174-mistralai-codestral-2508/usage_by_sample.csv` | PRESENT | 96534 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-034-registry-openrouter-174-mistralai-codestral-2508/failure_gallery.md` | PRESENT | 21307 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/summary.csv` | PRESENT | 1325 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/usage_by_family.csv` | PRESENT | 2800 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/usage_by_section.csv` | PRESENT | 5170 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/usage_by_question.csv` | PRESENT | 86992 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/usage_by_sample.csv` | PRESENT | 97894 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/failure_gallery.md` | PRESENT | 22786 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/summary.csv` | PRESENT | 1148 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/usage_by_family.csv` | PRESENT | 2278 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/usage_by_section.csv` | PRESENT | 4442 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/usage_by_question.csv` | PRESENT | 82886 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/usage_by_sample.csv` | PRESENT | 97970 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/summary.csv` | PRESENT | 1327 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/usage_by_family.csv` | PRESENT | 2898 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/usage_by_section.csv` | PRESENT | 5310 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/usage_by_question.csv` | PRESENT | 89285 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/usage_by_sample.csv` | PRESENT | 99670 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/failure_gallery.md` | PRESENT | 21843 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/summary.csv` | PRESENT | 1324 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/usage_by_family.csv` | PRESENT | 2811 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/usage_by_section.csv` | PRESENT | 5311 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/usage_by_question.csv` | PRESENT | 87945 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/usage_by_sample.csv` | PRESENT | 98156 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/failure_gallery.md` | PRESENT | 21309 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/summary.csv` | PRESENT | 1321 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/usage_by_family.csv` | PRESENT | 2798 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/usage_by_section.csv` | PRESENT | 5217 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/usage_by_question.csv` | PRESENT | 87003 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/usage_by_sample.csv` | PRESENT | 97275 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/failure_gallery.md` | PRESENT | 21010 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-070-registry-openai-gpt-5-4-mini-none/summary.csv` | PRESENT | 1299 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-070-registry-openai-gpt-5-4-mini-none/usage_by_family.csv` | PRESENT | 2549 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-070-registry-openai-gpt-5-4-mini-none/usage_by_section.csv` | PRESENT | 4549 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-070-registry-openai-gpt-5-4-mini-none/usage_by_question.csv` | PRESENT | 79565 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-070-registry-openai-gpt-5-4-mini-none/usage_by_sample.csv` | PRESENT | 92172 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-070-registry-openai-gpt-5-4-mini-none/failure_gallery.md` | PRESENT | 20952 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/summary.csv` | PRESENT | 1427 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/usage_by_family.csv` | PRESENT | 3441 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/usage_by_section.csv` | PRESENT | 6548 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/usage_by_question.csv` | PRESENT | 99905 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/usage_by_sample.csv` | PRESENT | 105679 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/failure_gallery.md` | PRESENT | 22834 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/summary.csv` | PRESENT | 1285 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/usage_by_family.csv` | PRESENT | 2874 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/usage_by_section.csv` | PRESENT | 5355 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/usage_by_question.csv` | PRESENT | 89255 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/usage_by_sample.csv` | PRESENT | 99885 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/failure_gallery.md` | PRESENT | 21806 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-006-registry-openrouter-111-google-gemma-3-27b-it/summary.csv` | PRESENT | 1362 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-006-registry-openrouter-111-google-gemma-3-27b-it/usage_by_family.csv` | PRESENT | 3184 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-006-registry-openrouter-111-google-gemma-3-27b-it/usage_by_section.csv` | PRESENT | 5796 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-006-registry-openrouter-111-google-gemma-3-27b-it/usage_by_question.csv` | PRESENT | 89574 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-006-registry-openrouter-111-google-gemma-3-27b-it/usage_by_sample.csv` | PRESENT | 99971 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-next-006-registry-openrouter-111-google-gemma-3-27b-it/failure_gallery.md` | PRESENT | 21298 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-024-registry-openai-gpt-4o-mini/summary.csv` | PRESENT | 1283 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-024-registry-openai-gpt-4o-mini/usage_by_family.csv` | PRESENT | 2442 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-024-registry-openai-gpt-4o-mini/usage_by_section.csv` | PRESENT | 4358 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-024-registry-openai-gpt-4o-mini/usage_by_question.csv` | PRESENT | 77179 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-024-registry-openai-gpt-4o-mini/usage_by_sample.csv` | PRESENT | 88560 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-024-registry-openai-gpt-4o-mini/failure_gallery.md` | PRESENT | 21724 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-014-registry-openrouter-093-mistralai-ministral-14b-2512/summary.csv` | PRESENT | 1329 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-014-registry-openrouter-093-mistralai-ministral-14b-2512/usage_by_family.csv` | PRESENT | 2803 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-014-registry-openrouter-093-mistralai-ministral-14b-2512/usage_by_section.csv` | PRESENT | 5029 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-014-registry-openrouter-093-mistralai-ministral-14b-2512/usage_by_question.csv` | PRESENT | 86387 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-014-registry-openrouter-093-mistralai-ministral-14b-2512/usage_by_sample.csv` | PRESENT | 98369 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-014-registry-openrouter-093-mistralai-ministral-14b-2512/failure_gallery.md` | PRESENT | 20974 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-048-openrouter-134-deepseek-deepseek-v3-2/summary.csv` | PRESENT | 1314 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-048-openrouter-134-deepseek-deepseek-v3-2/usage_by_family.csv` | PRESENT | 2686 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-048-openrouter-134-deepseek-deepseek-v3-2/usage_by_section.csv` | PRESENT | 5141 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-048-openrouter-134-deepseek-deepseek-v3-2/usage_by_question.csv` | PRESENT | 85497 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-048-openrouter-134-deepseek-deepseek-v3-2/usage_by_sample.csv` | PRESENT | 95533 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-048-openrouter-134-deepseek-deepseek-v3-2/failure_gallery.md` | PRESENT | 20991 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/summary.csv` | PRESENT | 1366 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/usage_by_family.csv` | PRESENT | 3021 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/usage_by_section.csv` | PRESENT | 5730 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/usage_by_question.csv` | PRESENT | 94200 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/usage_by_sample.csv` | PRESENT | 104469 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/failure_gallery.md` | PRESENT | 22306 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-087-thinking-openai-gpt-5-nano-minimal/summary.csv` | PRESENT | 1308 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-087-thinking-openai-gpt-5-nano-minimal/usage_by_family.csv` | PRESENT | 2537 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-087-thinking-openai-gpt-5-nano-minimal/usage_by_section.csv` | PRESENT | 4469 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-087-thinking-openai-gpt-5-nano-minimal/usage_by_question.csv` | PRESENT | 78384 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-087-thinking-openai-gpt-5-nano-minimal/usage_by_sample.csv` | PRESENT | 91174 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-087-thinking-openai-gpt-5-nano-minimal/failure_gallery.md` | PRESENT | 20139 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/summary.csv` | PRESENT | 1324 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/usage_by_family.csv` | PRESENT | 2799 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/usage_by_section.csv` | PRESENT | 5219 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/usage_by_question.csv` | PRESENT | 87045 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/usage_by_sample.csv` | PRESENT | 97112 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/failure_gallery.md` | PRESENT | 21637 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/summary.csv` | PRESENT | 1365 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/usage_by_family.csv` | PRESENT | 2856 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/usage_by_section.csv` | PRESENT | 5342 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/usage_by_question.csv` | PRESENT | 87219 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/usage_by_sample.csv` | PRESENT | 98298 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/failure_gallery.md` | PRESENT | 21830 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-008-registry-openrouter-094-mistralai-ministral-8b-2512/summary.csv` | PRESENT | 1332 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-008-registry-openrouter-094-mistralai-ministral-8b-2512/usage_by_family.csv` | PRESENT | 2771 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-008-registry-openrouter-094-mistralai-ministral-8b-2512/usage_by_section.csv` | PRESENT | 4990 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-008-registry-openrouter-094-mistralai-ministral-8b-2512/usage_by_question.csv` | PRESENT | 86084 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-008-registry-openrouter-094-mistralai-ministral-8b-2512/usage_by_sample.csv` | PRESENT | 97907 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-008-registry-openrouter-094-mistralai-ministral-8b-2512/failure_gallery.md` | PRESENT | 20979 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/summary.csv` | PRESENT | 1341 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/usage_by_family.csv` | PRESENT | 2848 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/usage_by_section.csv` | PRESENT | 5145 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/usage_by_question.csv` | PRESENT | 87531 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/usage_by_sample.csv` | PRESENT | 98916 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/failure_gallery.md` | PRESENT | 22720 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-037-registry-openai-gpt-5-4-nano-none/summary.csv` | PRESENT | 1300 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-037-registry-openai-gpt-5-4-nano-none/usage_by_family.csv` | PRESENT | 2520 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-037-registry-openai-gpt-5-4-nano-none/usage_by_section.csv` | PRESENT | 4521 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-037-registry-openai-gpt-5-4-nano-none/usage_by_question.csv` | PRESENT | 79560 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-037-registry-openai-gpt-5-4-nano-none/usage_by_sample.csv` | PRESENT | 92496 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-037-registry-openai-gpt-5-4-nano-none/failure_gallery.md` | PRESENT | 20295 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/summary.csv` | PRESENT | 1350 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/usage_by_family.csv` | PRESENT | 3126 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/usage_by_section.csv` | PRESENT | 5440 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/usage_by_question.csv` | PRESENT | 87374 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/usage_by_sample.csv` | PRESENT | 98542 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/failure_gallery.md` | PRESENT | 21095 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/summary.csv` | PRESENT | 1353 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/usage_by_family.csv` | PRESENT | 3308 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/usage_by_section.csv` | PRESENT | 6113 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/usage_by_question.csv` | PRESENT | 95299 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/usage_by_sample.csv` | PRESENT | 106474 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/failure_gallery.md` | PRESENT | 22021 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/summary.csv` | PRESENT | 1295 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/usage_by_family.csv` | PRESENT | 2701 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/usage_by_section.csv` | PRESENT | 4963 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/usage_by_question.csv` | PRESENT | 83929 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/usage_by_sample.csv` | PRESENT | 94881 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/failure_gallery.md` | PRESENT | 21190 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-017-openrouter-121-sao10k-l3-lunaris-8b/summary.csv` | PRESENT | 1305 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-017-openrouter-121-sao10k-l3-lunaris-8b/usage_by_family.csv` | PRESENT | 2701 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-017-openrouter-121-sao10k-l3-lunaris-8b/usage_by_section.csv` | PRESENT | 4999 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-017-openrouter-121-sao10k-l3-lunaris-8b/usage_by_question.csv` | PRESENT | 83942 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-017-openrouter-121-sao10k-l3-lunaris-8b/usage_by_sample.csv` | PRESENT | 94764 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-017-openrouter-121-sao10k-l3-lunaris-8b/failure_gallery.md` | PRESENT | 20394 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/summary.csv` | PRESENT | 1334 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/usage_by_family.csv` | PRESENT | 3358 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/usage_by_section.csv` | PRESENT | 5820 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/usage_by_question.csv` | PRESENT | 93241 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/usage_by_sample.csv` | PRESENT | 104921 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/failure_gallery.md` | PRESENT | 22076 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/summary.csv` | PRESENT | 1348 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/usage_by_family.csv` | PRESENT | 2938 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/usage_by_section.csv` | PRESENT | 5459 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/usage_by_question.csv` | PRESENT | 92084 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/usage_by_sample.csv` | PRESENT | 103376 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/failure_gallery.md` | PRESENT | 22150 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-068-openrouter-074-google-gemma-2-27b-it/summary.csv` | PRESENT | 1267 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-068-openrouter-074-google-gemma-2-27b-it/usage_by_family.csv` | PRESENT | 2673 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-068-openrouter-074-google-gemma-2-27b-it/usage_by_section.csv` | PRESENT | 4961 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-068-openrouter-074-google-gemma-2-27b-it/usage_by_question.csv` | PRESENT | 84589 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-068-openrouter-074-google-gemma-2-27b-it/usage_by_sample.csv` | PRESENT | 95285 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-068-openrouter-074-google-gemma-2-27b-it/failure_gallery.md` | PRESENT | 20916 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/summary.csv` | PRESENT | 1335 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/usage_by_family.csv` | PRESENT | 2877 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/usage_by_section.csv` | PRESENT | 5190 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/usage_by_question.csv` | PRESENT | 88417 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/usage_by_sample.csv` | PRESENT | 99646 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/failure_gallery.md` | PRESENT | 21337 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-012-registry-openrouter-107-meta-llama-llama-4-scout/summary.csv` | PRESENT | 1328 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-012-registry-openrouter-107-meta-llama-llama-4-scout/usage_by_family.csv` | PRESENT | 2743 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-012-registry-openrouter-107-meta-llama-llama-4-scout/usage_by_section.csv` | PRESENT | 4907 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-012-registry-openrouter-107-meta-llama-llama-4-scout/usage_by_question.csv` | PRESENT | 84755 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-012-registry-openrouter-107-meta-llama-llama-4-scout/usage_by_sample.csv` | PRESENT | 96859 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-012-registry-openrouter-107-meta-llama-llama-4-scout/failure_gallery.md` | PRESENT | 21632 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/summary.csv` | PRESENT | 1370 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/usage_by_family.csv` | PRESENT | 2814 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/usage_by_section.csv` | PRESENT | 4976 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/usage_by_question.csv` | PRESENT | 85165 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/usage_by_sample.csv` | PRESENT | 96657 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/failure_gallery.md` | PRESENT | 20763 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/summary.csv` | PRESENT | 1259 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/usage_by_family.csv` | PRESENT | 2770 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/usage_by_section.csv` | PRESENT | 5137 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/usage_by_question.csv` | PRESENT | 86160 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/usage_by_sample.csv` | PRESENT | 97120 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/failure_gallery.md` | PRESENT | 21664 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/summary.csv` | PRESENT | 1323 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/usage_by_family.csv` | PRESENT | 2827 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/usage_by_section.csv` | PRESENT | 5318 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/usage_by_question.csv` | PRESENT | 88041 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/usage_by_sample.csv` | PRESENT | 98914 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/failure_gallery.md` | PRESENT | 21409 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-031-openrouter-133-essentialai-rnj-1-instruct/summary.csv` | PRESENT | 1325 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-031-openrouter-133-essentialai-rnj-1-instruct/usage_by_family.csv` | PRESENT | 2777 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-031-openrouter-133-essentialai-rnj-1-instruct/usage_by_section.csv` | PRESENT | 5145 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-031-openrouter-133-essentialai-rnj-1-instruct/usage_by_question.csv` | PRESENT | 86745 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-031-openrouter-133-essentialai-rnj-1-instruct/usage_by_sample.csv` | PRESENT | 98984 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-031-openrouter-133-essentialai-rnj-1-instruct/failure_gallery.md` | PRESENT | 21491 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/summary.csv` | PRESENT | 1321 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/usage_by_family.csv` | PRESENT | 2910 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/usage_by_section.csv` | PRESENT | 5443 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/usage_by_question.csv` | PRESENT | 88584 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/usage_by_sample.csv` | PRESENT | 100476 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/failure_gallery.md` | PRESENT | 22595 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-077-openrouter-153-deepseek-deepseek-chat/summary.csv` | PRESENT | 1316 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-077-openrouter-153-deepseek-deepseek-chat/usage_by_family.csv` | PRESENT | 2731 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-077-openrouter-153-deepseek-deepseek-chat/usage_by_section.csv` | PRESENT | 5168 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-077-openrouter-153-deepseek-deepseek-chat/usage_by_question.csv` | PRESENT | 85467 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-077-openrouter-153-deepseek-deepseek-chat/usage_by_sample.csv` | PRESENT | 96963 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-077-openrouter-153-deepseek-deepseek-chat/failure_gallery.md` | PRESENT | 21277 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-056-openrouter-068-thedrummer-unslopnemo-12b/summary.csv` | PRESENT | 1316 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-056-openrouter-068-thedrummer-unslopnemo-12b/usage_by_family.csv` | PRESENT | 2743 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-056-openrouter-068-thedrummer-unslopnemo-12b/usage_by_section.csv` | PRESENT | 5112 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-056-openrouter-068-thedrummer-unslopnemo-12b/usage_by_question.csv` | PRESENT | 86103 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-056-openrouter-068-thedrummer-unslopnemo-12b/usage_by_sample.csv` | PRESENT | 97052 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-056-openrouter-068-thedrummer-unslopnemo-12b/failure_gallery.md` | PRESENT | 20983 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/summary.csv` | PRESENT | 1344 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/usage_by_family.csv` | PRESENT | 2930 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/usage_by_section.csv` | PRESENT | 5416 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/usage_by_question.csv` | PRESENT | 89256 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/usage_by_sample.csv` | PRESENT | 100032 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/failure_gallery.md` | PRESENT | 22020 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-001-registry-openrouter-109-google-gemma-3-4b-it/summary.csv` | PRESENT | 1325 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-001-registry-openrouter-109-google-gemma-3-4b-it/usage_by_family.csv` | PRESENT | 2672 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-001-registry-openrouter-109-google-gemma-3-4b-it/usage_by_section.csv` | PRESENT | 4772 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-001-registry-openrouter-109-google-gemma-3-4b-it/usage_by_question.csv` | PRESENT | 82867 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-001-registry-openrouter-109-google-gemma-3-4b-it/usage_by_sample.csv` | PRESENT | 94809 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-001-registry-openrouter-109-google-gemma-3-4b-it/failure_gallery.md` | PRESENT | 20513 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-004-registry-openrouter-095-mistralai-ministral-3b-2512/summary.csv` | PRESENT | 1304 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-004-registry-openrouter-095-mistralai-ministral-3b-2512/usage_by_family.csv` | PRESENT | 2767 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-004-registry-openrouter-095-mistralai-ministral-3b-2512/usage_by_section.csv` | PRESENT | 4997 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-004-registry-openrouter-095-mistralai-ministral-3b-2512/usage_by_question.csv` | PRESENT | 85810 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-004-registry-openrouter-095-mistralai-ministral-3b-2512/usage_by_sample.csv` | PRESENT | 98134 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-004-registry-openrouter-095-mistralai-ministral-3b-2512/failure_gallery.md` | PRESENT | 20928 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-059-openrouter-070-thedrummer-rocinante-12b/summary.csv` | PRESENT | 1299 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-059-openrouter-070-thedrummer-rocinante-12b/usage_by_family.csv` | PRESENT | 2679 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-059-openrouter-070-thedrummer-rocinante-12b/usage_by_section.csv` | PRESENT | 5108 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-059-openrouter-070-thedrummer-rocinante-12b/usage_by_question.csv` | PRESENT | 86025 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-059-openrouter-070-thedrummer-rocinante-12b/usage_by_sample.csv` | PRESENT | 98114 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-059-openrouter-070-thedrummer-rocinante-12b/failure_gallery.md` | PRESENT | 20769 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/summary.csv` | PRESENT | 1331 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/usage_by_family.csv` | PRESENT | 2818 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/usage_by_section.csv` | PRESENT | 5283 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/usage_by_question.csv` | PRESENT | 87800 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/usage_by_sample.csv` | PRESENT | 99897 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/failure_gallery.md` | PRESENT | 21057 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/summary.csv` | PRESENT | 1262 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/usage_by_family.csv` | PRESENT | 2713 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/usage_by_section.csv` | PRESENT | 4887 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/usage_by_question.csv` | PRESENT | 84647 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/usage_by_sample.csv` | PRESENT | 96234 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/failure_gallery.md` | PRESENT | 21191 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-018-openrouter-079-gryphe-mythomax-l2-13b/summary.csv` | PRESENT | 1328 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-018-openrouter-079-gryphe-mythomax-l2-13b/usage_by_family.csv` | PRESENT | 2683 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-018-openrouter-079-gryphe-mythomax-l2-13b/usage_by_section.csv` | PRESENT | 5057 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-018-openrouter-079-gryphe-mythomax-l2-13b/usage_by_question.csv` | PRESENT | 84775 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-018-openrouter-079-gryphe-mythomax-l2-13b/usage_by_sample.csv` | PRESENT | 96774 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-018-openrouter-079-gryphe-mythomax-l2-13b/failure_gallery.md` | PRESENT | 20750 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/summary.csv` | PRESENT | 1320 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/usage_by_family.csv` | PRESENT | 2935 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/usage_by_section.csv` | PRESENT | 5546 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/usage_by_question.csv` | PRESENT | 90979 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/usage_by_sample.csv` | PRESENT | 102341 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/failure_gallery.md` | PRESENT | 21642 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-013-openrouter-159-mistralai-mistral-nemo/summary.csv` | PRESENT | 1298 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-013-openrouter-159-mistralai-mistral-nemo/usage_by_family.csv` | PRESENT | 2745 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-013-openrouter-159-mistralai-mistral-nemo/usage_by_section.csv` | PRESENT | 5101 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-013-openrouter-159-mistralai-mistral-nemo/usage_by_question.csv` | PRESENT | 84578 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-013-openrouter-159-mistralai-mistral-nemo/usage_by_sample.csv` | PRESENT | 95640 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-013-openrouter-159-mistralai-mistral-nemo/failure_gallery.md` | PRESENT | 20500 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/summary.csv` | PRESENT | 1250 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/usage_by_family.csv` | PRESENT | 2627 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/usage_by_section.csv` | PRESENT | 5106 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/usage_by_question.csv` | PRESENT | 86056 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/usage_by_sample.csv` | PRESENT | 105305 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/failure_gallery.md` | PRESENT | 21102 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-028-openrouter-066-microsoft-phi-4/summary.csv` | PRESENT | 1313 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-028-openrouter-066-microsoft-phi-4/usage_by_family.csv` | PRESENT | 2633 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-028-openrouter-066-microsoft-phi-4/usage_by_section.csv` | PRESENT | 4842 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-028-openrouter-066-microsoft-phi-4/usage_by_question.csv` | PRESENT | 82006 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-028-openrouter-066-microsoft-phi-4/usage_by_sample.csv` | PRESENT | 94104 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-028-openrouter-066-microsoft-phi-4/failure_gallery.md` | PRESENT | 21518 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/summary.csv` | PRESENT | 1329 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/usage_by_family.csv` | PRESENT | 2681 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/usage_by_section.csv` | PRESENT | 5098 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/usage_by_question.csv` | PRESENT | 85854 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/usage_by_sample.csv` | PRESENT | 97551 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/failure_gallery.md` | PRESENT | 20894 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-083-openrouter-045-qwen-qwen3-coder-flash/summary.csv` | PRESENT | 1318 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-083-openrouter-045-qwen-qwen3-coder-flash/usage_by_family.csv` | PRESENT | 2676 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-083-openrouter-045-qwen-qwen3-coder-flash/usage_by_section.csv` | PRESENT | 5096 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-083-openrouter-045-qwen-qwen3-coder-flash/usage_by_question.csv` | PRESENT | 86281 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-083-openrouter-045-qwen-qwen3-coder-flash/usage_by_sample.csv` | PRESENT | 97235 bytes |
| `results/summaries/paper-v1-8x28-cost-telemetry-rerun2-20260603/runs/expand222-scaled-083-openrouter-045-qwen-qwen3-coder-flash/failure_gallery.md` | PRESENT | 24556 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/summary.csv` | PRESENT | 1351 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/usage_by_family.csv` | PRESENT | 2902 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/usage_by_section.csv` | PRESENT | 5185 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/usage_by_question.csv` | PRESENT | 88617 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/usage_by_sample.csv` | PRESENT | 100803 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/failure_gallery.md` | PRESENT | 24353 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-005-registry-openrouter-167-rekaai-reka-edge/summary.csv` | PRESENT | 1362 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-005-registry-openrouter-167-rekaai-reka-edge/usage_by_family.csv` | PRESENT | 3021 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-005-registry-openrouter-167-rekaai-reka-edge/usage_by_section.csv` | PRESENT | 5056 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-005-registry-openrouter-167-rekaai-reka-edge/usage_by_question.csv` | PRESENT | 84730 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-005-registry-openrouter-167-rekaai-reka-edge/usage_by_sample.csv` | PRESENT | 97632 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-005-registry-openrouter-167-rekaai-reka-edge/failure_gallery.md` | PRESENT | 20177 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/summary.csv` | PRESENT | 1334 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/usage_by_family.csv` | PRESENT | 2780 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/usage_by_section.csv` | PRESENT | 5219 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/usage_by_question.csv` | PRESENT | 88033 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/usage_by_sample.csv` | PRESENT | 100886 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/failure_gallery.md` | PRESENT | 22524 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-066-registry-openrouter-138-qwen-qwen3-max/summary.csv` | PRESENT | 1233 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-066-registry-openrouter-138-qwen-qwen3-max/usage_by_family.csv` | PRESENT | 2495 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-066-registry-openrouter-138-qwen-qwen3-max/usage_by_section.csv` | PRESENT | 4804 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-066-registry-openrouter-138-qwen-qwen3-max/usage_by_question.csv` | PRESENT | 79205 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-066-registry-openrouter-138-qwen-qwen3-max/usage_by_sample.csv` | PRESENT | 100811 bytes |
| `results/summaries/paper-v1-8x28-current-222-final-20260602/cumulative-cost-runs/expand222-next-066-registry-openrouter-138-qwen-qwen3-max/failure_gallery.md` | PRESENT | 21219 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/summary.csv` | PRESENT | 1400 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/usage_by_family.csv` | PRESENT | 3544 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/usage_by_section.csv` | PRESENT | 6770 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/usage_by_question.csv` | PRESENT | 103900 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/usage_by_sample.csv` | PRESENT | 113289 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/failure_gallery.md` | PRESENT | 27645 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/summary.csv` | PRESENT | 1316 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/usage_by_family.csv` | PRESENT | 2769 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/usage_by_section.csv` | PRESENT | 5295 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/usage_by_question.csv` | PRESENT | 88634 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/usage_by_sample.csv` | PRESENT | 101787 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/failure_gallery.md` | PRESENT | 21298 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/summary.csv` | PRESENT | 1220 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/usage_by_family.csv` | PRESENT | 2554 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/usage_by_section.csv` | PRESENT | 4770 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/usage_by_question.csv` | PRESENT | 85478 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/usage_by_sample.csv` | PRESENT | 100639 bytes |
| `results/summaries/paper-v1-8x28-current-222-20260602-keyed/runs/expand222-next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/failure_gallery.md` | PRESENT | 20980 bytes |
| `results/summaries/paper-v1-8x28-fill-gpt-5-4-mini-low-20260603/runs/expand222-fill-openai-gpt-5-4-mini-low/summary.csv` | PRESENT | 1326 bytes |
| `results/summaries/paper-v1-8x28-fill-gpt-5-4-mini-low-20260603/runs/expand222-fill-openai-gpt-5-4-mini-low/usage_by_family.csv` | PRESENT | 2855 bytes |
| `results/summaries/paper-v1-8x28-fill-gpt-5-4-mini-low-20260603/runs/expand222-fill-openai-gpt-5-4-mini-low/usage_by_section.csv` | PRESENT | 5272 bytes |
| `results/summaries/paper-v1-8x28-fill-gpt-5-4-mini-low-20260603/runs/expand222-fill-openai-gpt-5-4-mini-low/usage_by_question.csv` | PRESENT | 84313 bytes |
| `results/summaries/paper-v1-8x28-fill-gpt-5-4-mini-low-20260603/runs/expand222-fill-openai-gpt-5-4-mini-low/usage_by_sample.csv` | PRESENT | 90462 bytes |
| `results/summaries/paper-v1-8x28-fill-gpt-5-4-mini-low-20260603/runs/expand222-fill-openai-gpt-5-4-mini-low/failure_gallery.md` | PRESENT | 6689 bytes |

## Comparison Artifacts

| Path | Status | Evidence |
| --- | --- | --- |
| `results/summaries/paper-v1-8x28-current-223-final-20260603/comparison/comparison.csv` | PRESENT | 223 row(s), 128239 bytes |
| `results/summaries/paper-v1-8x28-current-223-final-20260603/comparison/family_comparison.csv` | PRESENT | 1784 row(s), 674627 bytes |
| `results/summaries/paper-v1-8x28-current-223-final-20260603/comparison/section_comparison.csv` | PRESENT | 3568 row(s), 1308205 bytes |
| `results/summaries/paper-v1-8x28-current-223-final-20260603/comparison/effort_curve.csv` | PRESENT | 223 row(s), 30265 bytes |
| `results/summaries/paper-v1-8x28-current-223-final-20260603/comparison/metamorphic_consistency.csv` | PRESENT | 223 row(s), 56935 bytes |
| `results/summaries/paper-v1-8x28-current-223-final-20260603/comparison/delta.csv` | PRESENT | 222 row(s), 89920 bytes |

## Report Artifacts

| Path | Status | Evidence |
| --- | --- | --- |
| `docs/reports/2026-06-03-paper-v1-8x28-current-223-final/report.html` | PRESENT | 513274 bytes |
| `docs/reports/2026-06-03-paper-v1-8x28-current-223-final/leaderboard.csv` | PRESENT | 88184 bytes |
| `docs/reports/2026-06-03-paper-v1-8x28-current-223-final/leaderboard.md` | PRESENT | 33103 bytes |
| `docs/reports/2026-06-03-paper-v1-8x28-current-223-final/family-heatmap.csv` | PRESENT | 124997 bytes |

## Promotion Rule

Paper result prose may cite this evidence run only when this audit passes, paper tables and figures are regenerated from the same comparison directory, and `make -C paper internal-review` no longer reports result or analysis placeholder blockers.
