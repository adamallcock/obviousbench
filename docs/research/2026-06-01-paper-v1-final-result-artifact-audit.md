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

- Final sweep manifest: `configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv`
- Comparison directory: `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison`
- Report directory: `docs/reports/2026-06-02-paper-v1-combined-234-overline`
- Planned models: 234
- Summary files present: 1404/1404
- Comparison files present: 6/6
- Report files present: 4/4
- Structural issues: 0

## Planned Models

| Label | Model | Summary directory |
| --- | --- | --- |
| OpenAI GPT-5 nano minimal | `openai/gpt-5-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-5-nano-minimal` |
| OpenAI GPT-4.1 | `openai/gpt-4.1` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1` |
| OpenAI GPT-4.1 mini | `openai/gpt-4.1-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1-mini` |
| Anthropic Claude Sonnet 4.6 | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-sonnet-4-6` |
| Anthropic Claude Haiku 4.5 | `anthropic/claude-haiku-4-5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-haiku-4-5` |
| Gemini 3.5 Flash | `google/gemini-3.5-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-3-5-flash` |
| Gemini 2.5 Flash-Lite | `google/gemini-2.5-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-2-5-flash-lite` |
| Grok 4.3 | `grok/grok-4.3` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-grok-4-3` |
| Xiaomi MiMo-V2-Flash | `openrouter/xiaomi/mimo-v2-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-xiaomi-mimo-v2-flash` |
| NVIDIA Nemotron 3 Nano 30B A3B | `openrouter/nvidia/nemotron-3-nano-30b-a3b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-nemotron-3-nano` |
| OpenAI GPT-OSS 20B | `openrouter/openai/gpt-oss-20b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-gpt-oss-20b` |
| Qwen3 Next 80B A3B Instruct | `openrouter/qwen/qwen3-next-80b-a3b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-qwen3-next` |
| Mistral: Mistral Nemo | `openrouter/mistralai/mistral-nemo` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-013-openrouter-159-mistralai-mistral-nemo` |
| Llama Guard 3 8B | `openrouter/meta-llama/llama-guard-3-8b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-014-openrouter-063-meta-llama-llama-guard-3-8b` |
| Meta: Llama 3 8B Instruct | `openrouter/meta-llama/llama-3-8b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct` |
| Meta: Llama 3.1 8B Instruct | `openrouter/meta-llama/llama-3.1-8b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct` |
| Sao10K: Llama 3 8B Lunaris | `openrouter/sao10k/l3-lunaris-8b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-017-openrouter-121-sao10k-l3-lunaris-8b` |
| MythoMax 13B | `openrouter/gryphe/mythomax-l2-13b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-018-openrouter-079-gryphe-mythomax-l2-13b` |
| Mistral: Mistral Small 3 | `openrouter/mistralai/mistral-small-24b-instruct-2501` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501` |
| Qwen: Qwen2.5 7B Instruct | `openrouter/qwen/qwen-2.5-7b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct` |
| IBM: Granite 4.1 8B | `openrouter/ibm-granite/granite-4.1-8b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-021-openrouter-026-ibm-granite-granite-4-1-8b` |
| Qwen: Qwen3 235B A22B Instruct 2507 | `openrouter/qwen/qwen3-235b-a22b-2507` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507` |
| Qwen: Qwen3 235B A22B Thinking 2507 | `openrouter/qwen/qwen3-235b-a22b-thinking-2507` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507` |
| Z.ai: GLM 4 32B | `openrouter/z-ai/glm-4-32b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-024-openrouter-052-z-ai-glm-4-32b` |
| IBM: Granite 4.0 Micro | `openrouter/ibm-granite/granite-4.0-h-micro` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro` |
| LiquidAI: LFM2-24B-A2B | `openrouter/liquid/lfm-2-24b-a2b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-026-openrouter-030-liquid-lfm-2-24b-a2b` |
| Google: Gemma 3n 4B | `openrouter/google/gemma-3n-e4b-it` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-027-openrouter-056-google-gemma-3n-e4b-it` |
| Microsoft: Phi 4 | `openrouter/microsoft/phi-4` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-028-openrouter-066-microsoft-phi-4` |
| NousResearch: Hermes 2 Pro - Llama-3 8B | `openrouter/nousresearch/hermes-2-pro-llama-3-8b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b` |
| Arcee AI: Trinity Mini | `openrouter/arcee-ai/trinity-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-030-openrouter-037-arcee-ai-trinity-mini` |
| EssentialAI: Rnj 1 Instruct | `openrouter/essentialai/rnj-1-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-031-openrouter-133-essentialai-rnj-1-instruct` |
| NVIDIA: Nemotron Nano 9B V2 | `openrouter/nvidia/nemotron-nano-9b-v2` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2` |
| Qwen: Qwen3 30B A3B Instruct 2507 | `openrouter/qwen/qwen3-30b-a3b-instruct-2507` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507` |
| OpenAI: gpt-oss-120b | `openrouter/openai/gpt-oss-120b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-034-openrouter-048-openai-gpt-oss-120b` |
| DeepSeek: DeepSeek V4 Flash | `openrouter/deepseek/deepseek-v4-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-035-openrouter-027-deepseek-deepseek-v4-flash` |
| Meta: Llama 3.2 1B Instruct | `openrouter/meta-llama/llama-3.2-1b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct` |
| Tencent: Hy3 preview | `openrouter/tencent/hy3-preview` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-038-openrouter-126-tencent-hy3-preview` |
| Qwen: Qwen3 14B | `openrouter/qwen/qwen3-14b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-039-openrouter-059-qwen-qwen3-14b` |
| Qwen: Qwen3 Coder 30B A3B Instruct | `openrouter/qwen/qwen3-coder-30b-a3b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct` |
| Qwen: Qwen3 32B | `openrouter/qwen/qwen3-32b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-041-openrouter-060-qwen-qwen3-32b` |
| DeepSeek: R1 Distill Qwen 32B | `openrouter/deepseek/deepseek-r1-distill-qwen-32b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b` |
| OpenAI: gpt-oss-safeguard-20b | `openrouter/openai/gpt-oss-safeguard-20b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-043-openrouter-039-openai-gpt-oss-safeguard-20b` |
| StepFun: Step 3.5 Flash | `openrouter/stepfun/step-3.5-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-044-openrouter-032-stepfun-step-3-5-flash` |
| Nous: Hermes 3 70B Instruct | `openrouter/nousresearch/hermes-3-llama-3.1-70b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-045-openrouter-156-nousresearch-hermes-3-llama-3-1-70b` |
| Meta: Llama 3.3 70B Instruct | `openrouter/meta-llama/llama-3.3-70b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct` |
| Meta: Llama 3.2 3B Instruct | `openrouter/meta-llama/llama-3.2-3b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-047-openrouter-071-meta-llama-llama-3-2-3b-instruct` |
| DeepSeek: DeepSeek V3.2 | `openrouter/deepseek/deepseek-v3.2` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-048-openrouter-134-deepseek-deepseek-v3-2` |
| Microsoft: Phi 4 Mini Instruct | `openrouter/microsoft/phi-4-mini-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-049-openrouter-042-microsoft-phi-4-mini-instruct` |
| Qwen: Qwen3 8B | `openrouter/qwen/qwen3-8b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-050-openrouter-058-qwen-qwen3-8b` |
| Z.ai: GLM 4.7 Flash | `openrouter/z-ai/glm-4.7-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-051-openrouter-033-z-ai-glm-4-7-flash` |
| Qwen: Qwen3 30B A3B Thinking 2507 | `openrouter/qwen/qwen3-30b-a3b-thinking-2507` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507` |
| NVIDIA: Llama 3.3 Nemotron Super 49B V1.5 | `openrouter/nvidia/llama-3.3-nemotron-super-49b-v1.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5` |
| Nous: Hermes 4 70B | `openrouter/nousresearch/hermes-4-70b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-054-openrouter-143-nousresearch-hermes-4-70b` |
| Qwen2.5 72B Instruct | `openrouter/qwen/qwen-2.5-72b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct` |
| TheDrummer: UnslopNemo 12B | `openrouter/thedrummer/unslopnemo-12b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-056-openrouter-068-thedrummer-unslopnemo-12b` |
| Meta: Llama 3.1 70B Instruct | `openrouter/meta-llama/llama-3.1-70b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct` |
| DeepSeek: DeepSeek V3.2 Exp | `openrouter/deepseek/deepseek-v3.2-exp` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp` |
| TheDrummer: Rocinante 12B | `openrouter/thedrummer/rocinante-12b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-059-openrouter-070-thedrummer-rocinante-12b` |
| NVIDIA: Nemotron 3 Super | `openrouter/nvidia/nemotron-3-super-120b-a12b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b` |
| Qwen: Qwen3 30B A3B | `openrouter/qwen/qwen3-30b-a3b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-061-openrouter-057-qwen-qwen3-30b-a3b` |
| Nex AGI: DeepSeek V3.1 Nex N1 | `openrouter/nex-agi/deepseek-v3.1-nex-n1` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1` |
| AllenAI: Olmo 3 32B Think | `openrouter/allenai/olmo-3-32b-think` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-063-openrouter-038-allenai-olmo-3-32b-think` |
| TheDrummer: Cydonia 24B V4.1 | `openrouter/thedrummer/cydonia-24b-v4.1` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1` |
| Tencent: Hunyuan A13B Instruct | `openrouter/tencent/hunyuan-a13b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct` |
| WizardLM-2 8x22B | `openrouter/microsoft/wizardlm-2-8x22b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b` |
| ReMM SLERP 13B | `openrouter/undi95/remm-slerp-l2-13b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-067-openrouter-078-undi95-remm-slerp-l2-13b` |
| Google: Gemma 2 27B | `openrouter/google/gemma-2-27b-it` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-068-openrouter-074-google-gemma-2-27b-it` |
| Meta: Llama 3 70B Instruct | `openrouter/meta-llama/llama-3-70b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct` |
| DeepSeek: DeepSeek V3 0324 | `openrouter/deepseek/deepseek-chat-v3-0324` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324` |
| Qwen: Qwen3 Next 80B A3B Thinking | `openrouter/qwen/qwen3-next-80b-a3b-thinking` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking` |
| Qwen: Qwen-Plus | `openrouter/qwen/qwen-plus` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-072-openrouter-152-qwen-qwen-plus` |
| Qwen: Qwen Plus 0728 | `openrouter/qwen/qwen-plus-2025-07-28` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28` |
| DeepSeek: DeepSeek V3.1 | `openrouter/deepseek/deepseek-chat-v3.1` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1` |
| Qwen: Qwen3 Coder Next | `openrouter/qwen/qwen3-coder-next` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-075-openrouter-130-qwen-qwen3-coder-next` |
| TheDrummer: Skyfall 36B V2 | `openrouter/thedrummer/skyfall-36b-v2` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-076-openrouter-151-thedrummer-skyfall-36b-v2` |
| DeepSeek: DeepSeek V3 | `openrouter/deepseek/deepseek-chat` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-077-openrouter-153-deepseek-deepseek-chat` |
| Z.ai: GLM 4.5 Air | `openrouter/z-ai/glm-4.5-air` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-078-openrouter-147-z-ai-glm-4-5-air` |
| DeepSeek: DeepSeek V4 Pro | `openrouter/deepseek/deepseek-v4-pro` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-079-openrouter-125-deepseek-deepseek-v4-pro` |
| Xiaomi: MiMo-V2.5-Pro | `openrouter/xiaomi/mimo-v2.5-pro` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro` |
| DeepSeek: DeepSeek V3.1 Terminus | `openrouter/deepseek/deepseek-v3.1-terminus` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus` |
| MiniMax: MiniMax M2.1 | `openrouter/minimax/minimax-m2.1` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-082-openrouter-034-minimax-minimax-m2-1` |
| Qwen: Qwen3 Coder Flash | `openrouter/qwen/qwen3-coder-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-083-openrouter-045-qwen-qwen3-coder-flash` |
| MiniMax: MiniMax M2 | `openrouter/minimax/minimax-m2` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-084-openrouter-040-minimax-minimax-m2` |
| Qwen2.5 Coder 32B Instruct | `openrouter/qwen/qwen-2.5-coder-32b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-085-openrouter-067-qwen-qwen-2-5-coder-32b-instruct` |
| Nous: Hermes 3 405B Instruct | `openrouter/nousresearch/hermes-3-llama-3.1-405b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b` |
| Prime Intellect: INTELLECT-3 | `openrouter/prime-intellect/intellect-3` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-087-openrouter-135-prime-intellect-intellect-3` |
| Baidu: ERNIE 4.5 300B A47B | `openrouter/baidu/ernie-4.5-300b-a47b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b` |
| MiniMax: MiniMax M2.5 | `openrouter/minimax/minimax-m2.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-089-openrouter-031-minimax-minimax-m2-5` |
| MiniMax: MiniMax M2.7 | `openrouter/minimax/minimax-m2.7` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-090-openrouter-028-minimax-minimax-m2-7` |
| AionLabs: Aion-1.0-Mini | `openrouter/aion-labs/aion-1.0-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-091-openrouter-119-aion-labs-aion-1-0-mini` |
| AionLabs: Aion-RP 1.0 (8B) | `openrouter/aion-labs/aion-rp-llama-3.1-8b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b` |
| Z.ai: GLM 4.6 | `openrouter/z-ai/glm-4.6` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-093-openrouter-136-z-ai-glm-4-6` |
| Z.ai: GLM 4.7 | `openrouter/z-ai/glm-4.7` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-094-openrouter-131-z-ai-glm-4-7` |
| Qwen: Qwen3 Coder 480B A35B | `openrouter/qwen/qwen3-coder` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-095-openrouter-148-qwen-qwen3-coder` |
| Qwen: Qwen3 235B A22B | `openrouter/qwen/qwen3-235b-a22b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-096-openrouter-061-qwen-qwen3-235b-a22b` |
| Z.ai: GLM 5 | `openrouter/z-ai/glm-5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-097-openrouter-129-z-ai-glm-5` |
| Z.ai: GLM 4.5 | `openrouter/z-ai/glm-4.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-098-openrouter-146-z-ai-glm-4-5` |
| MoonshotAI: Kimi K2 0711 | `openrouter/moonshotai/kimi-k2` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-099-openrouter-149-moonshotai-kimi-k2` |
| MoonshotAI: Kimi K2 0905 | `openrouter/moonshotai/kimi-k2-0905` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-100-openrouter-142-moonshotai-kimi-k2-0905` |
| Google: Gemma 3 4B | `openrouter/google/gemma-3-4b-it` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-001-registry-openrouter-109-google-gemma-3-4b-it` |
| Google: Gemma 3 12B | `openrouter/google/gemma-3-12b-it` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-002-registry-openrouter-110-google-gemma-3-12b-it` |
| Qwen: Qwen3.5-9B | `openrouter/qwen/qwen3.5-9b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-003-registry-openrouter-086-qwen-qwen3-5-9b` |
| Mistral: Ministral 3 3B 2512 | `openrouter/mistralai/ministral-3b-2512` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-004-registry-openrouter-095-mistralai-ministral-3b-2512` |
| Reka Edge | `openrouter/rekaai/reka-edge` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-005-registry-openrouter-167-rekaai-reka-edge` |
| Google: Gemma 3 27B | `openrouter/google/gemma-3-27b-it` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-006-registry-openrouter-111-google-gemma-3-27b-it` |
| Mistral: Mistral Small 3.2 24B | `openrouter/mistralai/mistral-small-3.2-24b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct` |
| Mistral: Ministral 3 8B 2512 | `openrouter/mistralai/ministral-8b-2512` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-008-registry-openrouter-094-mistralai-ministral-8b-2512` |
| ByteDance: UI-TARS 7B | `openrouter/bytedance/ui-tars-1.5-7b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b` |
| Qwen: Qwen3.5-Flash | `openrouter/qwen/qwen3.5-flash-02-23` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23` |
| Meta: Llama Guard 4 12B | `openrouter/meta-llama/llama-guard-4-12b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b` |
| Meta: Llama 4 Scout | `openrouter/meta-llama/llama-4-scout` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-012-registry-openrouter-107-meta-llama-llama-4-scout` |
| Google: Gemma 4 26B A4B | `openrouter/google/gemma-4-26b-a4b-it` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it` |
| Mistral: Ministral 3 14B 2512 | `openrouter/mistralai/ministral-14b-2512` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-014-registry-openrouter-093-mistralai-ministral-14b-2512` |
| Mistral: Voxtral Small 24B 2507 | `openrouter/mistralai/voxtral-small-24b-2507` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507` |
| Xiaomi: MiMo-V2.5 | `openrouter/xiaomi/mimo-v2.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-016-registry-openrouter-163-xiaomi-mimo-v2-5` |
| Google: Gemma 4 31B | `openrouter/google/gemma-4-31b-it` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-017-registry-openrouter-165-google-gemma-4-31b-it` |
| Meta: Llama 3.2 11B Vision Instruct | `openrouter/meta-llama/llama-3.2-11b-vision-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct` |
| OpenAI GPT-4.1 nano | `openai/gpt-4.1-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-019-registry-openai-gpt-4-1-nano` |
| Qwen: Qwen3 VL 32B Instruct | `openrouter/qwen/qwen3-vl-32b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-020-registry-openrouter-097-qwen-qwen3-vl-32b-instruct` |
| Qwen: Qwen3 VL 8B Instruct | `openrouter/qwen/qwen3-vl-8b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct` |
| Qwen: Qwen3 VL 30B A3B Instruct | `openrouter/qwen/qwen3-vl-30b-a3b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct` |
| Baidu: ERNIE 4.5 VL 28B A3B | `openrouter/baidu/ernie-4.5-vl-28b-a3b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-023-registry-openrouter-101-baidu-ernie-4-5-vl-28b-a3b` |
| OpenAI GPT-4o mini | `openai/gpt-4o-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-024-registry-openai-gpt-4o-mini` |
| Mistral: Mistral Small 4 | `openrouter/mistralai/mistral-small-2603` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-025-registry-openrouter-085-mistralai-mistral-small-2603` |
| Meta: Llama 4 Maverick | `openrouter/meta-llama/llama-4-maverick` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-026-registry-openrouter-106-meta-llama-llama-4-maverick` |
| Mistral: Saba | `openrouter/mistralai/mistral-saba` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-027-registry-openrouter-176-mistralai-mistral-saba` |
| Mistral: Mistral Small 3.1 24B | `openrouter/mistralai/mistral-small-3.1-24b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-028-registry-openrouter-108-mistralai-mistral-small-3-1-24b-instruct` |
| Qwen: Qwen2.5 VL 72B Instruct | `openrouter/qwen/qwen2.5-vl-72b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct` |
| Qwen: Qwen3 VL 235B A22B Instruct | `openrouter/qwen/qwen3-vl-235b-a22b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct` |
| Qwen: Qwen3.6 35B A3B | `openrouter/qwen/qwen3.6-35b-a3b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b` |
| Qwen: Qwen3.5-35B-A3B | `openrouter/qwen/qwen3.5-35b-a3b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b` |
| Z.ai: GLM 4.6V | `openrouter/z-ai/glm-4.6v` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-033-registry-openrouter-170-z-ai-glm-4-6v` |
| Mistral: Codestral 2508 | `openrouter/mistralai/codestral-2508` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-034-registry-openrouter-174-mistralai-codestral-2508` |
| MiniMax: MiniMax-01 | `openrouter/minimax/minimax-01` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-035-registry-openrouter-113-minimax-minimax-01` |
| Qwen: Qwen3.6 Flash | `openrouter/qwen/qwen3.6-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-036-registry-openrouter-081-qwen-qwen3-6-flash` |
| OpenAI GPT-5.4 nano no thinking | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-037-registry-openai-gpt-5-4-nano-none` |
| Qwen: Qwen3 VL 8B Thinking | `openrouter/qwen/qwen3-vl-8b-thinking` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking` |
| MiniMax: MiniMax M3 | `openrouter/minimax/minimax-m3` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-039-registry-openrouter-080-minimax-minimax-m3` |
| Baidu: ERNIE 4.5 VL 424B A47B | `openrouter/baidu/ernie-4.5-vl-424b-a47b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b` |
| Qwen: Qwen3 VL 30B A3B Thinking | `openrouter/qwen/qwen3-vl-30b-a3b-thinking` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking` |
| Gemini 3.1 Flash-Lite | `google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-042-registry-gemini-3-1-flash-lite` |
| Qwen: Qwen3.5-27B | `openrouter/qwen/qwen3.5-27b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-043-registry-openrouter-088-qwen-qwen3-5-27b` |
| Qwen: Qwen3.5 Plus 2026-02-15 | `openrouter/qwen/qwen3.5-plus-02-15` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15` |
| Mistral: Mistral Large 3 2512 | `openrouter/mistralai/mistral-large-2512` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-045-registry-openrouter-171-mistralai-mistral-large-2512` |
| Qwen: Qwen3.5 Plus 2026-04-20 | `openrouter/qwen/qwen3.5-plus-20260420` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420` |
| OpenAI GPT-5 mini minimal | `openai/gpt-5-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-047-registry-openai-gpt-5-mini-minimal` |
| Qwen: Qwen3.6 Plus | `openrouter/qwen/qwen3.6-plus` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-048-registry-openrouter-166-qwen-qwen3-6-plus` |
| MoonshotAI: Kimi K2.5 | `openrouter/moonshotai/kimi-k2.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-049-registry-openrouter-169-moonshotai-kimi-k2-5` |
| Qwen: Qwen3.5-122B-A10B | `openrouter/qwen/qwen3.5-122b-a10b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b` |
| Mistral: Devstral 2 2512 | `openrouter/mistralai/devstral-2512` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-051-registry-openrouter-092-mistralai-devstral-2512` |
| Mistral: Mistral Medium 3.1 | `openrouter/mistralai/mistral-medium-3.1` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-052-registry-openrouter-172-mistralai-mistral-medium-3-1` |
| Z.ai: GLM 4.5V | `openrouter/z-ai/glm-4.5v` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-053-registry-openrouter-173-z-ai-glm-4-5v` |
| Mistral: Mistral Medium 3 | `openrouter/mistralai/mistral-medium-3` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-054-registry-openrouter-175-mistralai-mistral-medium-3` |
| Qwen: Qwen3.5 397B A17B | `openrouter/qwen/qwen3.5-397b-a17b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b` |
| Gemini 2.5 Flash | `google/gemini-2.5-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-056-registry-gemini-2-5-flash` |
| Qwen: Qwen3 VL 235B A22B Thinking | `openrouter/qwen/qwen3-vl-235b-a22b-thinking` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking` |
| Grok Build 0.1 | `grok/grok-build-0.1` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-058-registry-grok-build-0-1` |
| Qwen: Qwen3.6 27B | `openrouter/qwen/qwen3.6-27b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-059-registry-openrouter-083-qwen-qwen3-6-27b` |
| Gemini 3 Flash Preview | `google/gemini-3-flash-preview` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-060-registry-gemini-3-flash-preview` |
| Qwen: Qwen3 Coder Plus | `openrouter/qwen/qwen3-coder-plus` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-061-registry-openrouter-139-qwen-qwen3-coder-plus` |
| Nous: Hermes 4 405B | `openrouter/nousresearch/hermes-4-405b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-062-registry-openrouter-144-nousresearch-hermes-4-405b` |
| Z.ai: GLM 5.1 | `openrouter/z-ai/glm-5.1` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-063-registry-openrouter-128-z-ai-glm-5-1` |
| MoonshotAI Kimi Latest | `openrouter/~moonshotai/kimi-latest` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-064-registry-openrouter-161-moonshotai-kimi-latest` |
| MoonshotAI: Kimi K2.6 | `openrouter/moonshotai/kimi-k2.6` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-065-registry-openrouter-164-moonshotai-kimi-k2-6` |
| Qwen: Qwen3 Max | `openrouter/qwen/qwen3-max` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-066-registry-openrouter-138-qwen-qwen3-max` |
| Qwen: Qwen3.7 Max | `openrouter/qwen/qwen3.7-max` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-067-registry-openrouter-178-qwen-qwen3-7-max` |
| Z.ai: GLM 5 Turbo | `openrouter/z-ai/glm-5-turbo` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-068-registry-openrouter-180-z-ai-glm-5-turbo` |
| Z.ai: GLM 5V Turbo | `openrouter/z-ai/glm-5v-turbo` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-069-registry-openrouter-184-z-ai-glm-5v-turbo` |
| OpenAI GPT-5.4 mini no thinking | `openai/gpt-5.4-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-070-registry-openai-gpt-5-4-mini-none` |
| Qwen: Qwen3.6 Max Preview | `openrouter/qwen/qwen3.6-max-preview` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-071-registry-openrouter-179-qwen-qwen3-6-max-preview` |
| Magnum v4 72B | `openrouter/anthracite-org/magnum-v4-72b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b` |
| Mistral: Mixtral 8x22B Instruct | `openrouter/mistralai/mixtral-8x22b-instruct` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct` |
| Mistral Large 2407 | `openrouter/mistralai/mistral-large-2407` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-074-registry-openrouter-185-mistralai-mistral-large-2407` |
| Mistral: Mistral Medium 3.5 | `openrouter/mistralai/mistral-medium-3-5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-075-registry-openrouter-183-mistralai-mistral-medium-3-5` |
| AI21: Jamba Large 1.7 | `openrouter/ai21/jamba-large-1.7` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-076-registry-openrouter-181-ai21-jamba-large-1-7` |
| OpenAI GPT-5 minimal | `openai/gpt-5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-077-registry-openai-gpt-5-minimal` |
| OpenAI GPT-4o | `openai/gpt-4o` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-078-registry-openai-gpt-4o` |
| Cohere: Command A | `openrouter/cohere/command-a` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-079-registry-openrouter-182-cohere-command-a` |
| OpenAI GPT-5.2 no thinking | `openai/gpt-5.2` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-080-registry-openai-gpt-5-2-none` |
| OpenAI GPT-5.4 no thinking | `openai/gpt-5.4` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-081-registry-openai-gpt-5-4-none` |
| Anthropic Claude Opus 4.6 | `anthropic/claude-opus-4-6` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-082-registry-anthropic-claude-opus-4-6` |
| Anthropic Claude Opus 4.7 | `anthropic/claude-opus-4-7` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-083-registry-anthropic-claude-opus-4-7` |
| Anthropic Claude Opus 4.8 | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-084-registry-anthropic-claude-opus-4-8` |
| OpenAI GPT-5.5 low | `openai/gpt-5.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-085-registry-openai-gpt-5-5-low` |
| OpenAI GPT-5.5 no thinking | `openai/gpt-5.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-086-registry-openai-gpt-5-5-none` |
| OpenAI GPT-5 nano minimal | `openai/gpt-5-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-087-thinking-openai-gpt-5-nano-minimal` |
| OpenAI GPT-5 nano low | `openai/gpt-5-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-088-thinking-openai-gpt-5-nano-low` |
| Gemini 2.5 Flash-Lite low_budget_1024 | `google/gemini-2.5-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-089-thinking-gemini-gemini-2-5-flash-lite-low` |
| OpenAI GPT-5 nano medium | `openai/gpt-5-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-090-thinking-openai-gpt-5-nano-medium` |
| DeepSeek: R1 Distill Qwen 32B low_budget_512 | `openrouter/deepseek/deepseek-r1-distill-qwen-32b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-091-thinking-openrouter-deepseek-deepseek-r1-distill-qwen-32b-low` |
| OpenAI GPT-5 mini minimal | `openai/gpt-5-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-092-thinking-openai-gpt-5-mini-minimal` |
| Gemini 3.1 Flash-Lite minimal_budget_1024 | `google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-093-thinking-gemini-gemini-3-1-flash-lite-minimal` |
| Google: Gemini 3.1 Flash Lite minimal | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal` |
| Google: Gemini 3.1 Flash Lite Preview minimal | `openrouter/google/gemini-3.1-flash-lite-preview` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal` |
| Qwen: Qwen3.6 35B A3B low_budget_512 | `openrouter/qwen/qwen3.6-35b-a3b` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low` |
| Gemini 2.5 Flash-Lite medium_budget_8192 | `google/gemini-2.5-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-097-thinking-gemini-gemini-2-5-flash-lite-medium` |
| Qwen: Qwen3.6 Flash low_budget_512 | `openrouter/qwen/qwen3.6-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-098-thinking-openrouter-qwen-qwen3-6-flash-low` |
| OpenAI GPT-5.4 nano low | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-099-thinking-openai-gpt-5-4-nano-low` |
| OpenAI: GPT-5.4 Nano low | `openrouter/openai/gpt-5.4-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-100-thinking-openrouter-openai-gpt-5-4-nano-low` |
| OpenAI GPT-5.5 none | `openai/gpt-5.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-001-openai-gpt-5-5-none` |
| OpenAI GPT-5.5 low | `openai/gpt-5.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-002-openai-gpt-5-5-low` |
| OpenAI GPT-5.5 medium | `openai/gpt-5.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-003-openai-gpt-5-5-medium` |
| OpenAI GPT-5.5 high | `openai/gpt-5.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-004-openai-gpt-5-5-high` |
| OpenAI GPT-5.5 xhigh | `openai/gpt-5.5` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-005-openai-gpt-5-5-xhigh` |
| OpenAI GPT-5.4 none | `openai/gpt-5.4` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-006-openai-gpt-5-4-none` |
| OpenAI GPT-5.4 low | `openai/gpt-5.4` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-007-openai-gpt-5-4-low` |
| OpenAI GPT-5.4 medium | `openai/gpt-5.4` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-008-openai-gpt-5-4-medium` |
| OpenAI GPT-5.4 high | `openai/gpt-5.4` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-009-openai-gpt-5-4-high` |
| OpenAI GPT-5.4 xhigh | `openai/gpt-5.4` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-010-openai-gpt-5-4-xhigh` |
| Claude Opus 4.8 low | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-011-anthropic-claude-opus-4-8-low` |
| Claude Opus 4.8 medium | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-012-anthropic-claude-opus-4-8-medium` |
| Claude Opus 4.8 high | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-013-anthropic-claude-opus-4-8-high` |
| Claude Opus 4.8 xhigh | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-014-anthropic-claude-opus-4-8-xhigh` |
| Claude Opus 4.8 max | `anthropic/claude-opus-4-8` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-015-anthropic-claude-opus-4-8-max` |
| Claude Sonnet 4.6 low | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-016-anthropic-claude-sonnet-4-6-low` |
| Claude Sonnet 4.6 medium | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-017-anthropic-claude-sonnet-4-6-medium` |
| Claude Sonnet 4.6 high | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-018-anthropic-claude-sonnet-4-6-high` |
| Claude Sonnet 4.6 max | `anthropic/claude-sonnet-4-6` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-019-anthropic-claude-sonnet-4-6-max` |
| Google: Gemini 3.5 Flash minimal | `openrouter/google/gemini-3.5-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-028-openrouter-google-gemini-3-5-flash-minimal` |
| Google: Gemini 3.5 Flash low | `openrouter/google/gemini-3.5-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-029-openrouter-google-gemini-3-5-flash-low` |
| Google: Gemini 3.5 Flash medium | `openrouter/google/gemini-3.5-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-030-openrouter-google-gemini-3-5-flash-medium` |
| Google: Gemini 3.5 Flash high | `openrouter/google/gemini-3.5-flash` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-031-openrouter-google-gemini-3-5-flash-high` |
| Google: Gemini 3.1 Pro Preview Custom Tools low | `openrouter/google/gemini-3.1-pro-preview-customtools` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low` |
| Google: Gemini 3.1 Pro Preview Custom Tools high | `openrouter/google/gemini-3.1-pro-preview-customtools` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high` |
| Google: Gemini 3.1 Flash Lite minimal | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal` |
| Google: Gemini 3.1 Flash Lite low | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low` |
| Google: Gemini 3.1 Flash Lite medium | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium` |
| Google: Gemini 3.1 Flash Lite high | `openrouter/google/gemini-3.1-flash-lite` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high` |
| OpenAI GPT-5.4 nano medium | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-002-openai-gpt-5-4-nano-medium` |
| OpenAI GPT-5.4 nano high | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-003-openai-gpt-5-4-nano-high` |
| OpenAI GPT-5.4 mini medium | `openai/gpt-5.4-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-004-openai-gpt-5-4-mini-medium` |
| OpenAI GPT-5.4 mini high | `openai/gpt-5.4-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-005-openai-gpt-5-4-mini-high` |
| OpenAI GPT-5.4 nano xhigh | `openai/gpt-5.4-nano` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-006-openai-gpt-5-4-nano-xhigh` |
| OpenAI GPT-5.4 mini xhigh | `openai/gpt-5.4-mini` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-007-openai-gpt-5-4-mini-xhigh` |

## Summary Artifacts

| Path | Status | Evidence |
| --- | --- | --- |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-5-nano-minimal/summary.csv` | PRESENT | 1206 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-5-nano-minimal/usage_by_family.csv` | PRESENT | 2336 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-5-nano-minimal/usage_by_section.csv` | PRESENT | 3908 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-5-nano-minimal/usage_by_question.csv` | PRESENT | 29407 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-5-nano-minimal/usage_by_sample.csv` | PRESENT | 33439 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-5-nano-minimal/failure_gallery.md` | PRESENT | 10547 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1/summary.csv` | PRESENT | 1194 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1/usage_by_family.csv` | PRESENT | 2180 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1/usage_by_section.csv` | PRESENT | 3687 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1/usage_by_question.csv` | PRESENT | 28230 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1/usage_by_sample.csv` | PRESENT | 31716 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1/failure_gallery.md` | PRESENT | 12958 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1-mini/summary.csv` | PRESENT | 1200 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1-mini/usage_by_family.csv` | PRESENT | 2313 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1-mini/usage_by_section.csv` | PRESENT | 3908 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1-mini/usage_by_question.csv` | PRESENT | 29045 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1-mini/usage_by_sample.csv` | PRESENT | 32482 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openai-gpt-4-1-mini/failure_gallery.md` | PRESENT | 9963 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-sonnet-4-6/summary.csv` | PRESENT | 1194 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-sonnet-4-6/usage_by_family.csv` | PRESENT | 2435 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-sonnet-4-6/usage_by_section.csv` | PRESENT | 4118 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-sonnet-4-6/usage_by_question.csv` | PRESENT | 30391 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-sonnet-4-6/usage_by_sample.csv` | PRESENT | 33806 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-sonnet-4-6/failure_gallery.md` | PRESENT | 10665 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-haiku-4-5/summary.csv` | PRESENT | 1201 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-haiku-4-5/usage_by_family.csv` | PRESENT | 2386 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-haiku-4-5/usage_by_section.csv` | PRESENT | 4046 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-haiku-4-5/usage_by_question.csv` | PRESENT | 30101 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-haiku-4-5/usage_by_sample.csv` | PRESENT | 33792 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-anthropic-claude-haiku-4-5/failure_gallery.md` | PRESENT | 18796 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-3-5-flash/summary.csv` | PRESENT | 1252 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-3-5-flash/usage_by_family.csv` | PRESENT | 2930 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-3-5-flash/usage_by_section.csv` | PRESENT | 5118 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-3-5-flash/usage_by_question.csv` | PRESENT | 35694 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-3-5-flash/usage_by_sample.csv` | PRESENT | 37246 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-3-5-flash/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-2-5-flash-lite/summary.csv` | PRESENT | 1223 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-2-5-flash-lite/usage_by_family.csv` | PRESENT | 2471 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-2-5-flash-lite/usage_by_section.csv` | PRESENT | 4147 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-2-5-flash-lite/usage_by_question.csv` | PRESENT | 30400 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-2-5-flash-lite/usage_by_sample.csv` | PRESENT | 34083 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-gemini-2-5-flash-lite/failure_gallery.md` | PRESENT | 18124 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-grok-4-3/summary.csv` | PRESENT | 1230 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-grok-4-3/usage_by_family.csv` | PRESENT | 2678 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-grok-4-3/usage_by_section.csv` | PRESENT | 4555 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-grok-4-3/usage_by_question.csv` | PRESENT | 32356 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-grok-4-3/usage_by_sample.csv` | PRESENT | 34652 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-grok-4-3/failure_gallery.md` | PRESENT | 26842 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-xiaomi-mimo-v2-flash/summary.csv` | PRESENT | 1228 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-xiaomi-mimo-v2-flash/usage_by_family.csv` | PRESENT | 2501 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-xiaomi-mimo-v2-flash/usage_by_section.csv` | PRESENT | 4221 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-xiaomi-mimo-v2-flash/usage_by_question.csv` | PRESENT | 31121 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-xiaomi-mimo-v2-flash/usage_by_sample.csv` | PRESENT | 34456 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-xiaomi-mimo-v2-flash/failure_gallery.md` | PRESENT | 6042 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-nemotron-3-nano/summary.csv` | PRESENT | 1327 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-nemotron-3-nano/usage_by_family.csv` | PRESENT | 3315 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-nemotron-3-nano/usage_by_section.csv` | PRESENT | 5639 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-nemotron-3-nano/usage_by_question.csv` | PRESENT | 39447 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-nemotron-3-nano/usage_by_sample.csv` | PRESENT | 40296 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-nemotron-3-nano/failure_gallery.md` | PRESENT | 2723 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-gpt-oss-20b/summary.csv` | PRESENT | 1398 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-gpt-oss-20b/usage_by_family.csv` | PRESENT | 3963 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-gpt-oss-20b/usage_by_section.csv` | PRESENT | 6489 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-gpt-oss-20b/usage_by_question.csv` | PRESENT | 38037 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-gpt-oss-20b/usage_by_sample.csv` | PRESENT | 39151 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-gpt-oss-20b/failure_gallery.md` | PRESENT | 3416 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-qwen3-next/summary.csv` | PRESENT | 1239 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-qwen3-next/usage_by_family.csv` | PRESENT | 2712 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-qwen3-next/usage_by_section.csv` | PRESENT | 4570 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-qwen3-next/usage_by_question.csv` | PRESENT | 32984 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-qwen3-next/usage_by_sample.csv` | PRESENT | 36507 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/paper-openrouter-qwen3-next/failure_gallery.md` | PRESENT | 16840 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-013-openrouter-159-mistralai-mistral-nemo/summary.csv` | PRESENT | 1230 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-013-openrouter-159-mistralai-mistral-nemo/usage_by_family.csv` | PRESENT | 2504 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-013-openrouter-159-mistralai-mistral-nemo/usage_by_section.csv` | PRESENT | 4274 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-013-openrouter-159-mistralai-mistral-nemo/usage_by_question.csv` | PRESENT | 31068 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-013-openrouter-159-mistralai-mistral-nemo/usage_by_sample.csv` | PRESENT | 34912 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-013-openrouter-159-mistralai-mistral-nemo/failure_gallery.md` | PRESENT | 19968 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-014-openrouter-063-meta-llama-llama-guard-3-8b/summary.csv` | PRESENT | 1147 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-014-openrouter-063-meta-llama-llama-guard-3-8b/usage_by_family.csv` | PRESENT | 1337 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-014-openrouter-063-meta-llama-llama-guard-3-8b/usage_by_section.csv` | PRESENT | 1423 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-014-openrouter-063-meta-llama-llama-guard-3-8b/usage_by_question.csv` | PRESENT | 2314 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-014-openrouter-063-meta-llama-llama-guard-3-8b/usage_by_sample.csv` | PRESENT | 2645 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-014-openrouter-063-meta-llama-llama-guard-3-8b/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/summary.csv` | PRESENT | 1241 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/usage_by_family.csv` | PRESENT | 2683 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/usage_by_section.csv` | PRESENT | 4535 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/usage_by_question.csv` | PRESENT | 32433 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/usage_by_sample.csv` | PRESENT | 36305 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-015-openrouter-076-meta-llama-llama-3-8b-instruct/failure_gallery.md` | PRESENT | 22573 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/summary.csv` | PRESENT | 1247 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/usage_by_family.csv` | PRESENT | 2691 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/usage_by_section.csv` | PRESENT | 4605 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/usage_by_question.csv` | PRESENT | 32714 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/usage_by_sample.csv` | PRESENT | 36499 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-016-openrouter-073-meta-llama-llama-3-1-8b-instruct/failure_gallery.md` | PRESENT | 18754 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-017-openrouter-121-sao10k-l3-lunaris-8b/summary.csv` | PRESENT | 1224 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-017-openrouter-121-sao10k-l3-lunaris-8b/usage_by_family.csv` | PRESENT | 2481 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-017-openrouter-121-sao10k-l3-lunaris-8b/usage_by_section.csv` | PRESENT | 4234 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-017-openrouter-121-sao10k-l3-lunaris-8b/usage_by_question.csv` | PRESENT | 30902 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-017-openrouter-121-sao10k-l3-lunaris-8b/usage_by_sample.csv` | PRESENT | 34592 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-017-openrouter-121-sao10k-l3-lunaris-8b/failure_gallery.md` | PRESENT | 15259 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-018-openrouter-079-gryphe-mythomax-l2-13b/summary.csv` | PRESENT | 1232 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-018-openrouter-079-gryphe-mythomax-l2-13b/usage_by_family.csv` | PRESENT | 2501 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-018-openrouter-079-gryphe-mythomax-l2-13b/usage_by_section.csv` | PRESENT | 4242 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-018-openrouter-079-gryphe-mythomax-l2-13b/usage_by_question.csv` | PRESENT | 31210 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-018-openrouter-079-gryphe-mythomax-l2-13b/usage_by_sample.csv` | PRESENT | 35284 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-018-openrouter-079-gryphe-mythomax-l2-13b/failure_gallery.md` | PRESENT | 23606 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/summary.csv` | PRESENT | 1273 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/usage_by_family.csv` | PRESENT | 2829 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/usage_by_section.csv` | PRESENT | 4864 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/usage_by_question.csv` | PRESENT | 34732 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/usage_by_sample.csv` | PRESENT | 38174 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-019-openrouter-065-mistralai-mistral-small-24b-instruct-2501/failure_gallery.md` | PRESENT | 17439 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/summary.csv` | PRESENT | 1216 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/usage_by_family.csv` | PRESENT | 2613 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/usage_by_section.csv` | PRESENT | 4385 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/usage_by_question.csv` | PRESENT | 31693 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/usage_by_sample.csv` | PRESENT | 35414 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-020-openrouter-069-qwen-qwen-2-5-7b-instruct/failure_gallery.md` | PRESENT | 17559 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/summary.csv` | PRESENT | 1240 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/usage_by_family.csv` | PRESENT | 2584 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/usage_by_section.csv` | PRESENT | 4450 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/usage_by_question.csv` | PRESENT | 31858 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/usage_by_sample.csv` | PRESENT | 35585 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-021-openrouter-026-ibm-granite-granite-4-1-8b/failure_gallery.md` | PRESENT | 19503 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/summary.csv` | PRESENT | 1292 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/usage_by_family.csv` | PRESENT | 2907 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/usage_by_section.csv` | PRESENT | 4830 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/usage_by_question.csv` | PRESENT | 32573 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/usage_by_sample.csv` | PRESENT | 35952 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-022-openrouter-053-qwen-qwen3-235b-a22b-2507/failure_gallery.md` | PRESENT | 9718 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/summary.csv` | PRESENT | 1404 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/usage_by_family.csv` | PRESENT | 3752 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/usage_by_section.csv` | PRESENT | 6398 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/usage_by_question.csv` | PRESENT | 40924 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/usage_by_sample.csv` | PRESENT | 41390 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-023-openrouter-118-qwen-qwen3-235b-a22b-thinking-2507/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-024-openrouter-052-z-ai-glm-4-32b/summary.csv` | PRESENT | 1213 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-024-openrouter-052-z-ai-glm-4-32b/usage_by_family.csv` | PRESENT | 2385 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-024-openrouter-052-z-ai-glm-4-32b/usage_by_section.csv` | PRESENT | 4022 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-024-openrouter-052-z-ai-glm-4-32b/usage_by_question.csv` | PRESENT | 29873 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-024-openrouter-052-z-ai-glm-4-32b/usage_by_sample.csv` | PRESENT | 33443 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-024-openrouter-052-z-ai-glm-4-32b/failure_gallery.md` | PRESENT | 10935 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/summary.csv` | PRESENT | 1250 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/usage_by_family.csv` | PRESENT | 2661 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/usage_by_section.csv` | PRESENT | 4505 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/usage_by_question.csv` | PRESENT | 32890 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/usage_by_sample.csv` | PRESENT | 36373 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-025-openrouter-041-ibm-granite-granite-4-0-h-micro/failure_gallery.md` | PRESENT | 13304 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/summary.csv` | PRESENT | 1224 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/usage_by_family.csv` | PRESENT | 2508 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/usage_by_section.csv` | PRESENT | 4193 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/usage_by_question.csv` | PRESENT | 30914 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/usage_by_sample.csv` | PRESENT | 34598 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-026-openrouter-030-liquid-lfm-2-24b-a2b/failure_gallery.md` | PRESENT | 15607 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-027-openrouter-056-google-gemma-3n-e4b-it/summary.csv` | PRESENT | 1229 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-027-openrouter-056-google-gemma-3n-e4b-it/usage_by_family.csv` | PRESENT | 2507 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-027-openrouter-056-google-gemma-3n-e4b-it/usage_by_section.csv` | PRESENT | 4213 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-027-openrouter-056-google-gemma-3n-e4b-it/usage_by_question.csv` | PRESENT | 31259 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-027-openrouter-056-google-gemma-3n-e4b-it/usage_by_sample.csv` | PRESENT | 35017 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-027-openrouter-056-google-gemma-3n-e4b-it/failure_gallery.md` | PRESENT | 21103 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-028-openrouter-066-microsoft-phi-4/summary.csv` | PRESENT | 1214 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-028-openrouter-066-microsoft-phi-4/usage_by_family.csv` | PRESENT | 2391 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-028-openrouter-066-microsoft-phi-4/usage_by_section.csv` | PRESENT | 4076 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-028-openrouter-066-microsoft-phi-4/usage_by_question.csv` | PRESENT | 30180 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-028-openrouter-066-microsoft-phi-4/usage_by_sample.csv` | PRESENT | 34416 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-028-openrouter-066-microsoft-phi-4/failure_gallery.md` | PRESENT | 24714 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/summary.csv` | PRESENT | 1259 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/usage_by_family.csv` | PRESENT | 2714 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/usage_by_section.csv` | PRESENT | 4670 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/usage_by_question.csv` | PRESENT | 33404 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/usage_by_sample.csv` | PRESENT | 37329 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-029-openrouter-075-nousresearch-hermes-2-pro-llama-3-8b/failure_gallery.md` | PRESENT | 23851 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-030-openrouter-037-arcee-ai-trinity-mini/summary.csv` | PRESENT | 1300 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-030-openrouter-037-arcee-ai-trinity-mini/usage_by_family.csv` | PRESENT | 3246 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-030-openrouter-037-arcee-ai-trinity-mini/usage_by_section.csv` | PRESENT | 5532 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-030-openrouter-037-arcee-ai-trinity-mini/usage_by_question.csv` | PRESENT | 38287 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-030-openrouter-037-arcee-ai-trinity-mini/usage_by_sample.csv` | PRESENT | 39357 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-030-openrouter-037-arcee-ai-trinity-mini/failure_gallery.md` | PRESENT | 64940 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-031-openrouter-133-essentialai-rnj-1-instruct/summary.csv` | PRESENT | 1228 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-031-openrouter-133-essentialai-rnj-1-instruct/usage_by_family.csv` | PRESENT | 2529 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-031-openrouter-133-essentialai-rnj-1-instruct/usage_by_section.csv` | PRESENT | 4326 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-031-openrouter-133-essentialai-rnj-1-instruct/usage_by_question.csv` | PRESENT | 31987 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-031-openrouter-133-essentialai-rnj-1-instruct/usage_by_sample.csv` | PRESENT | 36081 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-031-openrouter-133-essentialai-rnj-1-instruct/failure_gallery.md` | PRESENT | 26412 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/summary.csv` | PRESENT | 1326 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/usage_by_family.csv` | PRESENT | 3260 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/usage_by_section.csv` | PRESENT | 5629 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/usage_by_question.csv` | PRESENT | 38658 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/usage_by_sample.csv` | PRESENT | 39780 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-032-openrouter-047-nvidia-nemotron-nano-9b-v2/failure_gallery.md` | PRESENT | 13878 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/summary.csv` | PRESENT | 1307 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/usage_by_family.csv` | PRESENT | 3077 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/usage_by_section.csv` | PRESENT | 5175 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/usage_by_question.csv` | PRESENT | 35396 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/usage_by_sample.csv` | PRESENT | 39217 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-033-openrouter-051-qwen-qwen3-30b-a3b-instruct-2507/failure_gallery.md` | PRESENT | 24338 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-034-openrouter-048-openai-gpt-oss-120b/summary.csv` | PRESENT | 1456 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-034-openrouter-048-openai-gpt-oss-120b/usage_by_family.csv` | PRESENT | 3570 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-034-openrouter-048-openai-gpt-oss-120b/usage_by_section.csv` | PRESENT | 5781 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-034-openrouter-048-openai-gpt-oss-120b/usage_by_question.csv` | PRESENT | 37616 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-034-openrouter-048-openai-gpt-oss-120b/usage_by_sample.csv` | PRESENT | 38688 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-034-openrouter-048-openai-gpt-oss-120b/failure_gallery.md` | PRESENT | 1734 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-035-openrouter-027-deepseek-deepseek-v4-flash/summary.csv` | PRESENT | 1321 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-035-openrouter-027-deepseek-deepseek-v4-flash/usage_by_family.csv` | PRESENT | 3257 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-035-openrouter-027-deepseek-deepseek-v4-flash/usage_by_section.csv` | PRESENT | 5583 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-035-openrouter-027-deepseek-deepseek-v4-flash/usage_by_question.csv` | PRESENT | 36887 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-035-openrouter-027-deepseek-deepseek-v4-flash/usage_by_sample.csv` | PRESENT | 38523 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-035-openrouter-027-deepseek-deepseek-v4-flash/failure_gallery.md` | PRESENT | 4797 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/summary.csv` | PRESENT | 1226 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/usage_by_family.csv` | PRESENT | 2681 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/usage_by_section.csv` | PRESENT | 4523 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/usage_by_question.csv` | PRESENT | 32562 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/usage_by_sample.csv` | PRESENT | 37084 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-037-openrouter-155-meta-llama-llama-3-2-1b-instruct/failure_gallery.md` | PRESENT | 23600 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-038-openrouter-126-tencent-hy3-preview/summary.csv` | PRESENT | 1264 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-038-openrouter-126-tencent-hy3-preview/usage_by_family.csv` | PRESENT | 3167 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-038-openrouter-126-tencent-hy3-preview/usage_by_section.csv` | PRESENT | 5450 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-038-openrouter-126-tencent-hy3-preview/usage_by_question.csv` | PRESENT | 36838 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-038-openrouter-126-tencent-hy3-preview/usage_by_sample.csv` | PRESENT | 37853 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-038-openrouter-126-tencent-hy3-preview/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-039-openrouter-059-qwen-qwen3-14b/summary.csv` | PRESENT | 1293 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-039-openrouter-059-qwen-qwen3-14b/usage_by_family.csv` | PRESENT | 3066 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-039-openrouter-059-qwen-qwen3-14b/usage_by_section.csv` | PRESENT | 5281 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-039-openrouter-059-qwen-qwen3-14b/usage_by_question.csv` | PRESENT | 37101 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-039-openrouter-059-qwen-qwen3-14b/usage_by_sample.csv` | PRESENT | 37825 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-039-openrouter-059-qwen-qwen3-14b/failure_gallery.md` | PRESENT | 4228 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/summary.csv` | PRESENT | 1251 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/usage_by_family.csv` | PRESENT | 2695 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/usage_by_section.csv` | PRESENT | 4539 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/usage_by_question.csv` | PRESENT | 32862 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/usage_by_sample.csv` | PRESENT | 36871 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-040-openrouter-050-qwen-qwen3-coder-30b-a3b-instruct/failure_gallery.md` | PRESENT | 24864 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-041-openrouter-060-qwen-qwen3-32b/summary.csv` | PRESENT | 1400 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-041-openrouter-060-qwen-qwen3-32b/usage_by_family.csv` | PRESENT | 3214 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-041-openrouter-060-qwen-qwen3-32b/usage_by_section.csv` | PRESENT | 5393 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-041-openrouter-060-qwen-qwen3-32b/usage_by_question.csv` | PRESENT | 37151 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-041-openrouter-060-qwen-qwen3-32b/usage_by_sample.csv` | PRESENT | 38028 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-041-openrouter-060-qwen-qwen3-32b/failure_gallery.md` | PRESENT | 10443 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/summary.csv` | PRESENT | 1334 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/usage_by_family.csv` | PRESENT | 3401 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/usage_by_section.csv` | PRESENT | 5808 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/usage_by_question.csv` | PRESENT | 40195 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/usage_by_sample.csv` | PRESENT | 42684 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-042-openrouter-120-deepseek-deepseek-r1-distill-qwen-32b/failure_gallery.md` | PRESENT | 31086 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-043-openrouter-039-openai-gpt-oss-safeguard-20b/summary.csv` | PRESENT | 1329 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-043-openrouter-039-openai-gpt-oss-safeguard-20b/usage_by_family.csv` | PRESENT | 3239 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-043-openrouter-039-openai-gpt-oss-safeguard-20b/usage_by_section.csv` | PRESENT | 3765 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-043-openrouter-039-openai-gpt-oss-safeguard-20b/usage_by_question.csv` | PRESENT | 14404 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-043-openrouter-039-openai-gpt-oss-safeguard-20b/usage_by_sample.csv` | PRESENT | 15580 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-043-openrouter-039-openai-gpt-oss-safeguard-20b/failure_gallery.md` | PRESENT | 1787 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-044-openrouter-032-stepfun-step-3-5-flash/summary.csv` | PRESENT | 1307 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-044-openrouter-032-stepfun-step-3-5-flash/usage_by_family.csv` | PRESENT | 3231 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-044-openrouter-032-stepfun-step-3-5-flash/usage_by_section.csv` | PRESENT | 5547 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-044-openrouter-032-stepfun-step-3-5-flash/usage_by_question.csv` | PRESENT | 38432 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-044-openrouter-032-stepfun-step-3-5-flash/usage_by_sample.csv` | PRESENT | 39095 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-044-openrouter-032-stepfun-step-3-5-flash/failure_gallery.md` | PRESENT | 1118 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-045-openrouter-156-nousresearch-hermes-3-llama-3-1-70b/summary.csv` | PRESENT | 1270 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-045-openrouter-156-nousresearch-hermes-3-llama-3-1-70b/usage_by_family.csv` | PRESENT | 2442 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-045-openrouter-156-nousresearch-hermes-3-llama-3-1-70b/usage_by_section.csv` | PRESENT | 3956 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-045-openrouter-156-nousresearch-hermes-3-llama-3-1-70b/usage_by_question.csv` | PRESENT | 26683 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-045-openrouter-156-nousresearch-hermes-3-llama-3-1-70b/usage_by_sample.csv` | PRESENT | 31079 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-045-openrouter-156-nousresearch-hermes-3-llama-3-1-70b/failure_gallery.md` | PRESENT | 44241 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/summary.csv` | PRESENT | 1249 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/usage_by_family.csv` | PRESENT | 2734 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/usage_by_section.csv` | PRESENT | 4655 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/usage_by_question.csv` | PRESENT | 33101 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/usage_by_sample.csv` | PRESENT | 36686 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-046-openrouter-154-meta-llama-llama-3-3-70b-instruct/failure_gallery.md` | PRESENT | 17999 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-047-openrouter-071-meta-llama-llama-3-2-3b-instruct/summary.csv` | PRESENT | 1258 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-047-openrouter-071-meta-llama-llama-3-2-3b-instruct/usage_by_family.csv` | PRESENT | 2388 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-047-openrouter-071-meta-llama-llama-3-2-3b-instruct/usage_by_section.csv` | PRESENT | 2816 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-047-openrouter-071-meta-llama-llama-3-2-3b-instruct/usage_by_question.csv` | PRESENT | 14242 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-047-openrouter-071-meta-llama-llama-3-2-3b-instruct/usage_by_sample.csv` | PRESENT | 16626 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-047-openrouter-071-meta-llama-llama-3-2-3b-instruct/failure_gallery.md` | PRESENT | 6468 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-048-openrouter-134-deepseek-deepseek-v3-2/summary.csv` | PRESENT | 1235 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-048-openrouter-134-deepseek-deepseek-v3-2/usage_by_family.csv` | PRESENT | 2510 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-048-openrouter-134-deepseek-deepseek-v3-2/usage_by_section.csv` | PRESENT | 4310 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-048-openrouter-134-deepseek-deepseek-v3-2/usage_by_question.csv` | PRESENT | 31531 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-048-openrouter-134-deepseek-deepseek-v3-2/usage_by_sample.csv` | PRESENT | 34954 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-048-openrouter-134-deepseek-deepseek-v3-2/failure_gallery.md` | PRESENT | 13064 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/summary.csv` | PRESENT | 1253 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/usage_by_family.csv` | PRESENT | 2659 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/usage_by_section.csv` | PRESENT | 4508 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/usage_by_question.csv` | PRESENT | 32357 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/usage_by_sample.csv` | PRESENT | 36353 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-049-openrouter-042-microsoft-phi-4-mini-instruct/failure_gallery.md` | PRESENT | 24007 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-050-openrouter-058-qwen-qwen3-8b/summary.csv` | PRESENT | 1297 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-050-openrouter-058-qwen-qwen3-8b/usage_by_family.csv` | PRESENT | 2803 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-050-openrouter-058-qwen-qwen3-8b/usage_by_section.csv` | PRESENT | 4704 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-050-openrouter-058-qwen-qwen3-8b/usage_by_question.csv` | PRESENT | 33423 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-050-openrouter-058-qwen-qwen3-8b/usage_by_sample.csv` | PRESENT | 35650 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-050-openrouter-058-qwen-qwen3-8b/failure_gallery.md` | PRESENT | 14082 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-051-openrouter-033-z-ai-glm-4-7-flash/summary.csv` | PRESENT | 1299 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-051-openrouter-033-z-ai-glm-4-7-flash/usage_by_family.csv` | PRESENT | 3175 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-051-openrouter-033-z-ai-glm-4-7-flash/usage_by_section.csv` | PRESENT | 5432 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-051-openrouter-033-z-ai-glm-4-7-flash/usage_by_question.csv` | PRESENT | 37658 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-051-openrouter-033-z-ai-glm-4-7-flash/usage_by_sample.csv` | PRESENT | 38597 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-051-openrouter-033-z-ai-glm-4-7-flash/failure_gallery.md` | PRESENT | 8086 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/summary.csv` | PRESENT | 1329 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/usage_by_family.csv` | PRESENT | 3395 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/usage_by_section.csv` | PRESENT | 5846 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/usage_by_question.csv` | PRESENT | 40091 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/usage_by_sample.csv` | PRESENT | 40689 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-052-openrouter-117-qwen-qwen3-30b-a3b-thinking-2507/failure_gallery.md` | PRESENT | 1147 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/summary.csv` | PRESENT | 1334 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/usage_by_family.csv` | PRESENT | 2692 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/usage_by_section.csv` | PRESENT | 4511 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/usage_by_question.csv` | PRESENT | 33046 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/usage_by_sample.csv` | PRESENT | 37031 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-001-openrouter-nvidia-llama-3-3-nemotron-super-49b-v1-5/failure_gallery.md` | PRESENT | 3705 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-054-openrouter-143-nousresearch-hermes-4-70b/summary.csv` | PRESENT | 1239 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-054-openrouter-143-nousresearch-hermes-4-70b/usage_by_family.csv` | PRESENT | 2603 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-054-openrouter-143-nousresearch-hermes-4-70b/usage_by_section.csv` | PRESENT | 4386 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-054-openrouter-143-nousresearch-hermes-4-70b/usage_by_question.csv` | PRESENT | 31829 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-054-openrouter-143-nousresearch-hermes-4-70b/usage_by_sample.csv` | PRESENT | 35335 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-054-openrouter-143-nousresearch-hermes-4-70b/failure_gallery.md` | PRESENT | 11424 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/summary.csv` | PRESENT | 1240 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/usage_by_family.csv` | PRESENT | 2553 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/usage_by_section.csv` | PRESENT | 4363 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/usage_by_question.csv` | PRESENT | 32047 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/usage_by_sample.csv` | PRESENT | 35723 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-055-openrouter-072-qwen-qwen-2-5-72b-instruct/failure_gallery.md` | PRESENT | 21988 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-056-openrouter-068-thedrummer-unslopnemo-12b/summary.csv` | PRESENT | 1230 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-056-openrouter-068-thedrummer-unslopnemo-12b/usage_by_family.csv` | PRESENT | 2579 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-056-openrouter-068-thedrummer-unslopnemo-12b/usage_by_section.csv` | PRESENT | 4348 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-056-openrouter-068-thedrummer-unslopnemo-12b/usage_by_question.csv` | PRESENT | 31676 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-056-openrouter-068-thedrummer-unslopnemo-12b/usage_by_sample.csv` | PRESENT | 35411 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-056-openrouter-068-thedrummer-unslopnemo-12b/failure_gallery.md` | PRESENT | 17441 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/summary.csv` | PRESENT | 1247 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/usage_by_family.csv` | PRESENT | 2683 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/usage_by_section.csv` | PRESENT | 4598 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/usage_by_question.csv` | PRESENT | 33047 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/usage_by_sample.csv` | PRESENT | 36572 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-057-openrouter-158-meta-llama-llama-3-1-70b-instruct/failure_gallery.md` | PRESENT | 13450 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/summary.csv` | PRESENT | 1240 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/usage_by_family.csv` | PRESENT | 2573 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/usage_by_section.csv` | PRESENT | 4426 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/usage_by_question.csv` | PRESENT | 32010 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/usage_by_sample.csv` | PRESENT | 35518 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-058-openrouter-137-deepseek-deepseek-v3-2-exp/failure_gallery.md` | PRESENT | 13060 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-059-openrouter-070-thedrummer-rocinante-12b/summary.csv` | PRESENT | 1240 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-059-openrouter-070-thedrummer-rocinante-12b/usage_by_family.csv` | PRESENT | 2556 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-059-openrouter-070-thedrummer-rocinante-12b/usage_by_section.csv` | PRESENT | 4358 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-059-openrouter-070-thedrummer-rocinante-12b/usage_by_question.csv` | PRESENT | 31702 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-059-openrouter-070-thedrummer-rocinante-12b/usage_by_sample.csv` | PRESENT | 35617 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-059-openrouter-070-thedrummer-rocinante-12b/failure_gallery.md` | PRESENT | 23751 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/summary.csv` | PRESENT | 1277 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/usage_by_family.csv` | PRESENT | 3278 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/usage_by_section.csv` | PRESENT | 5703 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/usage_by_question.csv` | PRESENT | 38216 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/usage_by_sample.csv` | PRESENT | 40076 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-060-openrouter-029-nvidia-nemotron-3-super-120b-a12b/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-061-openrouter-057-qwen-qwen3-30b-a3b/summary.csv` | PRESENT | 1305 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-061-openrouter-057-qwen-qwen3-30b-a3b/usage_by_family.csv` | PRESENT | 3121 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-061-openrouter-057-qwen-qwen3-30b-a3b/usage_by_section.csv` | PRESENT | 5401 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-061-openrouter-057-qwen-qwen3-30b-a3b/usage_by_question.csv` | PRESENT | 37770 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-061-openrouter-057-qwen-qwen3-30b-a3b/usage_by_sample.csv` | PRESENT | 38490 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-061-openrouter-057-qwen-qwen3-30b-a3b/failure_gallery.md` | PRESENT | 3098 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/summary.csv` | PRESENT | 1245 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/usage_by_family.csv` | PRESENT | 2649 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/usage_by_section.csv` | PRESENT | 4524 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/usage_by_question.csv` | PRESENT | 32851 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/usage_by_sample.csv` | PRESENT | 35970 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-062-openrouter-132-nex-agi-deepseek-v3-1-nex-n1/failure_gallery.md` | PRESENT | 7803 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-063-openrouter-038-allenai-olmo-3-32b-think/summary.csv` | PRESENT | 1141 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-063-openrouter-038-allenai-olmo-3-32b-think/usage_by_family.csv` | PRESENT | 1776 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-063-openrouter-038-allenai-olmo-3-32b-think/usage_by_section.csv` | PRESENT | 1897 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-063-openrouter-038-allenai-olmo-3-32b-think/usage_by_question.csv` | PRESENT | 2707 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-063-openrouter-038-allenai-olmo-3-32b-think/usage_by_sample.csv` | PRESENT | 3105 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-063-openrouter-038-allenai-olmo-3-32b-think/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/summary.csv` | PRESENT | 1244 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/usage_by_family.csv` | PRESENT | 2647 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/usage_by_section.csv` | PRESENT | 4467 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/usage_by_question.csv` | PRESENT | 32459 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/usage_by_sample.csv` | PRESENT | 35873 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-064-openrouter-044-thedrummer-cydonia-24b-v4-1/failure_gallery.md` | PRESENT | 12423 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/summary.csv` | PRESENT | 1237 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/usage_by_family.csv` | PRESENT | 2654 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/usage_by_section.csv` | PRESENT | 4502 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/usage_by_question.csv` | PRESENT | 32346 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/usage_by_sample.csv` | PRESENT | 36065 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-065-openrouter-054-tencent-hunyuan-a13b-instruct/failure_gallery.md` | PRESENT | 17728 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/summary.csv` | PRESENT | 1300 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/usage_by_family.csv` | PRESENT | 2764 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/usage_by_section.csv` | PRESENT | 4629 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/usage_by_question.csv` | PRESENT | 32594 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/usage_by_sample.csv` | PRESENT | 36248 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-066-openrouter-077-microsoft-wizardlm-2-8x22b/failure_gallery.md` | PRESENT | 27384 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/summary.csv` | PRESENT | 1229 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/usage_by_family.csv` | PRESENT | 2530 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/usage_by_section.csv` | PRESENT | 4300 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/usage_by_question.csv` | PRESENT | 31547 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/usage_by_sample.csv` | PRESENT | 35569 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-067-openrouter-078-undi95-remm-slerp-l2-13b/failure_gallery.md` | PRESENT | 23663 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-068-openrouter-074-google-gemma-2-27b-it/summary.csv` | PRESENT | 1225 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-068-openrouter-074-google-gemma-2-27b-it/usage_by_family.csv` | PRESENT | 2477 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-068-openrouter-074-google-gemma-2-27b-it/usage_by_section.csv` | PRESENT | 4204 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-068-openrouter-074-google-gemma-2-27b-it/usage_by_question.csv` | PRESENT | 31151 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-068-openrouter-074-google-gemma-2-27b-it/usage_by_sample.csv` | PRESENT | 34748 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-068-openrouter-074-google-gemma-2-27b-it/failure_gallery.md` | PRESENT | 15838 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/summary.csv` | PRESENT | 1245 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/usage_by_family.csv` | PRESENT | 2714 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/usage_by_section.csv` | PRESENT | 4601 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/usage_by_question.csv` | PRESENT | 32866 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/usage_by_sample.csv` | PRESENT | 36343 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-069-openrouter-160-meta-llama-llama-3-70b-instruct/failure_gallery.md` | PRESENT | 12522 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/summary.csv` | PRESENT | 1235 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/usage_by_family.csv` | PRESENT | 2646 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/usage_by_section.csv` | PRESENT | 4546 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/usage_by_question.csv` | PRESENT | 32594 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/usage_by_sample.csv` | PRESENT | 36618 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-070-openrouter-150-deepseek-deepseek-chat-v3-0324/failure_gallery.md` | PRESENT | 26824 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/summary.csv` | PRESENT | 1337 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/usage_by_family.csv` | PRESENT | 3398 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/usage_by_section.csv` | PRESENT | 5902 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/usage_by_question.csv` | PRESENT | 40461 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/usage_by_sample.csv` | PRESENT | 40923 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-071-openrouter-116-qwen-qwen3-next-80b-a3b-thinking/failure_gallery.md` | PRESENT | 3311 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-072-openrouter-152-qwen-qwen-plus/summary.csv` | PRESENT | 1218 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-072-openrouter-152-qwen-qwen-plus/usage_by_family.csv` | PRESENT | 2371 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-072-openrouter-152-qwen-qwen-plus/usage_by_section.csv` | PRESENT | 4071 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-072-openrouter-152-qwen-qwen-plus/usage_by_question.csv` | PRESENT | 30137 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-072-openrouter-152-qwen-qwen-plus/usage_by_sample.csv` | PRESENT | 33543 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-072-openrouter-152-qwen-qwen-plus/failure_gallery.md` | PRESENT | 9269 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/summary.csv` | PRESENT | 1231 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/usage_by_family.csv` | PRESENT | 2548 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/usage_by_section.csv` | PRESENT | 4368 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/usage_by_question.csv` | PRESENT | 31886 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/usage_by_sample.csv` | PRESENT | 35472 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-073-openrouter-141-qwen-qwen-plus-2025-07-28/failure_gallery.md` | PRESENT | 17973 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/summary.csv` | PRESENT | 1247 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/usage_by_family.csv` | PRESENT | 2583 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/usage_by_section.csv` | PRESENT | 4432 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/usage_by_question.csv` | PRESENT | 32160 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/usage_by_sample.csv` | PRESENT | 35706 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-074-openrouter-145-deepseek-deepseek-chat-v3-1/failure_gallery.md` | PRESENT | 15709 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-075-openrouter-130-qwen-qwen3-coder-next/summary.csv` | PRESENT | 1226 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-075-openrouter-130-qwen-qwen3-coder-next/usage_by_family.csv` | PRESENT | 2539 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-075-openrouter-130-qwen-qwen3-coder-next/usage_by_section.csv` | PRESENT | 4274 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-075-openrouter-130-qwen-qwen3-coder-next/usage_by_question.csv` | PRESENT | 31255 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-075-openrouter-130-qwen-qwen3-coder-next/usage_by_sample.csv` | PRESENT | 34559 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-075-openrouter-130-qwen-qwen3-coder-next/failure_gallery.md` | PRESENT | 7082 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/summary.csv` | PRESENT | 1228 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/usage_by_family.csv` | PRESENT | 2553 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/usage_by_section.csv` | PRESENT | 4431 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/usage_by_question.csv` | PRESENT | 32129 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/usage_by_sample.csv` | PRESENT | 35536 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-076-openrouter-151-thedrummer-skyfall-36b-v2/failure_gallery.md` | PRESENT | 12085 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-077-openrouter-153-deepseek-deepseek-chat/summary.csv` | PRESENT | 1232 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-077-openrouter-153-deepseek-deepseek-chat/usage_by_family.csv` | PRESENT | 2577 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-077-openrouter-153-deepseek-deepseek-chat/usage_by_section.csv` | PRESENT | 4357 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-077-openrouter-153-deepseek-deepseek-chat/usage_by_question.csv` | PRESENT | 31602 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-077-openrouter-153-deepseek-deepseek-chat/usage_by_sample.csv` | PRESENT | 35446 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-077-openrouter-153-deepseek-deepseek-chat/failure_gallery.md` | PRESENT | 24620 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-078-openrouter-147-z-ai-glm-4-5-air/summary.csv` | PRESENT | 1300 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-078-openrouter-147-z-ai-glm-4-5-air/usage_by_family.csv` | PRESENT | 3161 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-078-openrouter-147-z-ai-glm-4-5-air/usage_by_section.csv` | PRESENT | 5383 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-078-openrouter-147-z-ai-glm-4-5-air/usage_by_question.csv` | PRESENT | 35915 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-078-openrouter-147-z-ai-glm-4-5-air/usage_by_sample.csv` | PRESENT | 37537 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-078-openrouter-147-z-ai-glm-4-5-air/failure_gallery.md` | PRESENT | 15160 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-079-openrouter-125-deepseek-deepseek-v4-pro/summary.csv` | PRESENT | 1324 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-079-openrouter-125-deepseek-deepseek-v4-pro/usage_by_family.csv` | PRESENT | 3268 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-079-openrouter-125-deepseek-deepseek-v4-pro/usage_by_section.csv` | PRESENT | 5595 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-079-openrouter-125-deepseek-deepseek-v4-pro/usage_by_question.csv` | PRESENT | 37505 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-079-openrouter-125-deepseek-deepseek-v4-pro/usage_by_sample.csv` | PRESENT | 38736 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-079-openrouter-125-deepseek-deepseek-v4-pro/failure_gallery.md` | PRESENT | 8200 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/summary.csv` | PRESENT | 1315 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/usage_by_family.csv` | PRESENT | 3244 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/usage_by_section.csv` | PRESENT | 5529 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/usage_by_question.csv` | PRESENT | 38460 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/usage_by_sample.csv` | PRESENT | 39051 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-080-openrouter-127-xiaomi-mimo-v2-5-pro/failure_gallery.md` | PRESENT | 3591 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/summary.csv` | PRESENT | 1250 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/usage_by_family.csv` | PRESENT | 2664 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/usage_by_section.csv` | PRESENT | 4580 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/usage_by_question.csv` | PRESENT | 32837 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/usage_by_sample.csv` | PRESENT | 36395 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-081-openrouter-140-deepseek-deepseek-v3-1-terminus/failure_gallery.md` | PRESENT | 16861 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-082-openrouter-034-minimax-minimax-m2-1/summary.csv` | PRESENT | 1305 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-082-openrouter-034-minimax-minimax-m2-1/usage_by_family.csv` | PRESENT | 3210 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-082-openrouter-034-minimax-minimax-m2-1/usage_by_section.csv` | PRESENT | 5455 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-082-openrouter-034-minimax-minimax-m2-1/usage_by_question.csv` | PRESENT | 37969 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-082-openrouter-034-minimax-minimax-m2-1/usage_by_sample.csv` | PRESENT | 38874 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-082-openrouter-034-minimax-minimax-m2-1/failure_gallery.md` | PRESENT | 3471 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-083-openrouter-045-qwen-qwen3-coder-flash/summary.csv` | PRESENT | 1234 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-083-openrouter-045-qwen-qwen3-coder-flash/usage_by_family.csv` | PRESENT | 2549 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-083-openrouter-045-qwen-qwen3-coder-flash/usage_by_section.csv` | PRESENT | 4301 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-083-openrouter-045-qwen-qwen3-coder-flash/usage_by_question.csv` | PRESENT | 31319 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-083-openrouter-045-qwen-qwen3-coder-flash/usage_by_sample.csv` | PRESENT | 35250 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-083-openrouter-045-qwen-qwen3-coder-flash/failure_gallery.md` | PRESENT | 24909 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-084-openrouter-040-minimax-minimax-m2/summary.csv` | PRESENT | 1309 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-084-openrouter-040-minimax-minimax-m2/usage_by_family.csv` | PRESENT | 3190 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-084-openrouter-040-minimax-minimax-m2/usage_by_section.csv` | PRESENT | 5460 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-084-openrouter-040-minimax-minimax-m2/usage_by_question.csv` | PRESENT | 37843 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-084-openrouter-040-minimax-minimax-m2/usage_by_sample.csv` | PRESENT | 38527 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-084-openrouter-040-minimax-minimax-m2/failure_gallery.md` | PRESENT | 2862 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-085-openrouter-067-qwen-qwen-2-5-coder-32b-instruct/summary.csv` | PRESENT | 1307 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-085-openrouter-067-qwen-qwen-2-5-coder-32b-instruct/usage_by_family.csv` | PRESENT | 2383 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-085-openrouter-067-qwen-qwen-2-5-coder-32b-instruct/usage_by_section.csv` | PRESENT | 2548 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-085-openrouter-067-qwen-qwen-2-5-coder-32b-instruct/usage_by_question.csv` | PRESENT | 6892 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-085-openrouter-067-qwen-qwen-2-5-coder-32b-instruct/usage_by_sample.csv` | PRESENT | 8077 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-085-openrouter-067-qwen-qwen-2-5-coder-32b-instruct/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/summary.csv` | PRESENT | 1259 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/usage_by_family.csv` | PRESENT | 2709 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/usage_by_section.csv` | PRESENT | 4624 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/usage_by_question.csv` | PRESENT | 33364 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/usage_by_sample.csv` | PRESENT | 36909 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-086-openrouter-157-nousresearch-hermes-3-llama-3-1-405b/failure_gallery.md` | PRESENT | 9789 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-087-openrouter-135-prime-intellect-intellect-3/summary.csv` | PRESENT | 1322 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-087-openrouter-135-prime-intellect-intellect-3/usage_by_family.csv` | PRESENT | 3303 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-087-openrouter-135-prime-intellect-intellect-3/usage_by_section.csv` | PRESENT | 5643 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-087-openrouter-135-prime-intellect-intellect-3/usage_by_question.csv` | PRESENT | 39270 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-087-openrouter-135-prime-intellect-intellect-3/usage_by_sample.csv` | PRESENT | 39960 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-087-openrouter-135-prime-intellect-intellect-3/failure_gallery.md` | PRESENT | 5869 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/summary.csv` | PRESENT | 1237 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/usage_by_family.csv` | PRESENT | 2539 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/usage_by_section.csv` | PRESENT | 4413 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/usage_by_question.csv` | PRESENT | 31888 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/usage_by_sample.csv` | PRESENT | 35553 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-088-openrouter-055-baidu-ernie-4-5-300b-a47b/failure_gallery.md` | PRESENT | 22546 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-089-openrouter-031-minimax-minimax-m2-5/summary.csv` | PRESENT | 1415 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-089-openrouter-031-minimax-minimax-m2-5/usage_by_family.csv` | PRESENT | 4035 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-089-openrouter-031-minimax-minimax-m2-5/usage_by_section.csv` | PRESENT | 6763 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-089-openrouter-031-minimax-minimax-m2-5/usage_by_question.csv` | PRESENT | 40612 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-089-openrouter-031-minimax-minimax-m2-5/usage_by_sample.csv` | PRESENT | 41565 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-089-openrouter-031-minimax-minimax-m2-5/failure_gallery.md` | PRESENT | 6297 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-090-openrouter-028-minimax-minimax-m2-7/summary.csv` | PRESENT | 1410 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-090-openrouter-028-minimax-minimax-m2-7/usage_by_family.csv` | PRESENT | 4134 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-090-openrouter-028-minimax-minimax-m2-7/usage_by_section.csv` | PRESENT | 6811 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-090-openrouter-028-minimax-minimax-m2-7/usage_by_question.csv` | PRESENT | 39695 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-090-openrouter-028-minimax-minimax-m2-7/usage_by_sample.csv` | PRESENT | 40535 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-090-openrouter-028-minimax-minimax-m2-7/failure_gallery.md` | PRESENT | 6986 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-091-openrouter-119-aion-labs-aion-1-0-mini/summary.csv` | PRESENT | 1312 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-091-openrouter-119-aion-labs-aion-1-0-mini/usage_by_family.csv` | PRESENT | 2619 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-091-openrouter-119-aion-labs-aion-1-0-mini/usage_by_section.csv` | PRESENT | 4409 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-091-openrouter-119-aion-labs-aion-1-0-mini/usage_by_question.csv` | PRESENT | 27971 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-091-openrouter-119-aion-labs-aion-1-0-mini/usage_by_sample.csv` | PRESENT | 30734 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-091-openrouter-119-aion-labs-aion-1-0-mini/failure_gallery.md` | PRESENT | 9660 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/summary.csv` | PRESENT | 1249 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/usage_by_family.csv` | PRESENT | 2603 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/usage_by_section.csv` | PRESENT | 4410 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/usage_by_question.csv` | PRESENT | 32336 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/usage_by_sample.csv` | PRESENT | 36840 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-092-openrouter-064-aion-labs-aion-rp-llama-3-1-8b/failure_gallery.md` | PRESENT | 27578 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-093-openrouter-136-z-ai-glm-4-6/summary.csv` | PRESENT | 1293 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-093-openrouter-136-z-ai-glm-4-6/usage_by_family.csv` | PRESENT | 3122 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-093-openrouter-136-z-ai-glm-4-6/usage_by_section.csv` | PRESENT | 5326 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-093-openrouter-136-z-ai-glm-4-6/usage_by_question.csv` | PRESENT | 36947 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-093-openrouter-136-z-ai-glm-4-6/usage_by_sample.csv` | PRESENT | 37596 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-093-openrouter-136-z-ai-glm-4-6/failure_gallery.md` | PRESENT | 1935 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-094-openrouter-131-z-ai-glm-4-7/summary.csv` | PRESENT | 1294 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-094-openrouter-131-z-ai-glm-4-7/usage_by_family.csv` | PRESENT | 3074 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-094-openrouter-131-z-ai-glm-4-7/usage_by_section.csv` | PRESENT | 5280 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-094-openrouter-131-z-ai-glm-4-7/usage_by_question.csv` | PRESENT | 36841 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-094-openrouter-131-z-ai-glm-4-7/usage_by_sample.csv` | PRESENT | 37702 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-094-openrouter-131-z-ai-glm-4-7/failure_gallery.md` | PRESENT | 10043 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-095-openrouter-148-qwen-qwen3-coder/summary.csv` | PRESENT | 1264 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-095-openrouter-148-qwen-qwen3-coder/usage_by_family.csv` | PRESENT | 2899 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-095-openrouter-148-qwen-qwen3-coder/usage_by_section.csv` | PRESENT | 4882 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-095-openrouter-148-qwen-qwen3-coder/usage_by_question.csv` | PRESENT | 32817 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-095-openrouter-148-qwen-qwen3-coder/usage_by_sample.csv` | PRESENT | 36383 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-095-openrouter-148-qwen-qwen3-coder/failure_gallery.md` | PRESENT | 18870 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-096-openrouter-061-qwen-qwen3-235b-a22b/summary.csv` | PRESENT | 1301 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-096-openrouter-061-qwen-qwen3-235b-a22b/usage_by_family.csv` | PRESENT | 3214 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-096-openrouter-061-qwen-qwen3-235b-a22b/usage_by_section.csv` | PRESENT | 5481 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-096-openrouter-061-qwen-qwen3-235b-a22b/usage_by_question.csv` | PRESENT | 38297 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-096-openrouter-061-qwen-qwen3-235b-a22b/usage_by_sample.csv` | PRESENT | 39010 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-096-openrouter-061-qwen-qwen3-235b-a22b/failure_gallery.md` | PRESENT | 12445 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-097-openrouter-129-z-ai-glm-5/summary.csv` | PRESENT | 1288 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-097-openrouter-129-z-ai-glm-5/usage_by_family.csv` | PRESENT | 3005 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-097-openrouter-129-z-ai-glm-5/usage_by_section.csv` | PRESENT | 5226 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-097-openrouter-129-z-ai-glm-5/usage_by_question.csv` | PRESENT | 36652 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-097-openrouter-129-z-ai-glm-5/usage_by_sample.csv` | PRESENT | 37262 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-097-openrouter-129-z-ai-glm-5/failure_gallery.md` | PRESENT | 1701 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-098-openrouter-146-z-ai-glm-4-5/summary.csv` | PRESENT | 1298 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-098-openrouter-146-z-ai-glm-4-5/usage_by_family.csv` | PRESENT | 3125 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-098-openrouter-146-z-ai-glm-4-5/usage_by_section.csv` | PRESENT | 5319 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-098-openrouter-146-z-ai-glm-4-5/usage_by_question.csv` | PRESENT | 37000 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-098-openrouter-146-z-ai-glm-4-5/usage_by_sample.csv` | PRESENT | 37681 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-098-openrouter-146-z-ai-glm-4-5/failure_gallery.md` | PRESENT | 4608 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-099-openrouter-149-moonshotai-kimi-k2/summary.csv` | PRESENT | 1205 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-099-openrouter-149-moonshotai-kimi-k2/usage_by_family.csv` | PRESENT | 2442 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-099-openrouter-149-moonshotai-kimi-k2/usage_by_section.csv` | PRESENT | 4094 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-099-openrouter-149-moonshotai-kimi-k2/usage_by_question.csv` | PRESENT | 29804 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-099-openrouter-149-moonshotai-kimi-k2/usage_by_sample.csv` | PRESENT | 33708 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-099-openrouter-149-moonshotai-kimi-k2/failure_gallery.md` | PRESENT | 8484 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-100-openrouter-142-moonshotai-kimi-k2-0905/summary.csv` | PRESENT | 1222 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-100-openrouter-142-moonshotai-kimi-k2-0905/usage_by_family.csv` | PRESENT | 2528 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-100-openrouter-142-moonshotai-kimi-k2-0905/usage_by_section.csv` | PRESENT | 4319 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-100-openrouter-142-moonshotai-kimi-k2-0905/usage_by_question.csv` | PRESENT | 31543 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-100-openrouter-142-moonshotai-kimi-k2-0905/usage_by_sample.csv` | PRESENT | 34825 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/scaled-100-openrouter-142-moonshotai-kimi-k2-0905/failure_gallery.md` | PRESENT | 5072 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-001-registry-openrouter-109-google-gemma-3-4b-it/summary.csv` | PRESENT | 1227 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-001-registry-openrouter-109-google-gemma-3-4b-it/usage_by_family.csv` | PRESENT | 2484 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-001-registry-openrouter-109-google-gemma-3-4b-it/usage_by_section.csv` | PRESENT | 4177 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-001-registry-openrouter-109-google-gemma-3-4b-it/usage_by_question.csv` | PRESENT | 30759 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-001-registry-openrouter-109-google-gemma-3-4b-it/usage_by_sample.csv` | PRESENT | 34794 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-001-registry-openrouter-109-google-gemma-3-4b-it/failure_gallery.md` | PRESENT | 21888 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-002-registry-openrouter-110-google-gemma-3-12b-it/summary.csv` | PRESENT | 1226 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-002-registry-openrouter-110-google-gemma-3-12b-it/usage_by_family.csv` | PRESENT | 2496 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-002-registry-openrouter-110-google-gemma-3-12b-it/usage_by_section.csv` | PRESENT | 4236 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-002-registry-openrouter-110-google-gemma-3-12b-it/usage_by_question.csv` | PRESENT | 31020 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-002-registry-openrouter-110-google-gemma-3-12b-it/usage_by_sample.csv` | PRESENT | 34708 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-002-registry-openrouter-110-google-gemma-3-12b-it/failure_gallery.md` | PRESENT | 16490 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-003-registry-openrouter-086-qwen-qwen3-5-9b/summary.csv` | PRESENT | 1381 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-003-registry-openrouter-086-qwen-qwen3-5-9b/usage_by_family.csv` | PRESENT | 3102 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-003-registry-openrouter-086-qwen-qwen3-5-9b/usage_by_section.csv` | PRESENT | 4639 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-003-registry-openrouter-086-qwen-qwen3-5-9b/usage_by_question.csv` | PRESENT | 28597 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-003-registry-openrouter-086-qwen-qwen3-5-9b/usage_by_sample.csv` | PRESENT | 29238 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-003-registry-openrouter-086-qwen-qwen3-5-9b/failure_gallery.md` | PRESENT | 882 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-004-registry-openrouter-095-mistralai-ministral-3b-2512/summary.csv` | PRESENT | 1242 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-004-registry-openrouter-095-mistralai-ministral-3b-2512/usage_by_family.csv` | PRESENT | 2589 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-004-registry-openrouter-095-mistralai-ministral-3b-2512/usage_by_section.csv` | PRESENT | 4395 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-004-registry-openrouter-095-mistralai-ministral-3b-2512/usage_by_question.csv` | PRESENT | 31764 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-004-registry-openrouter-095-mistralai-ministral-3b-2512/usage_by_sample.csv` | PRESENT | 35859 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-004-registry-openrouter-095-mistralai-ministral-3b-2512/failure_gallery.md` | PRESENT | 22232 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-005-registry-openrouter-167-rekaai-reka-edge/summary.csv` | PRESENT | 1270 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-005-registry-openrouter-167-rekaai-reka-edge/usage_by_family.csv` | PRESENT | 2800 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-005-registry-openrouter-167-rekaai-reka-edge/usage_by_section.csv` | PRESENT | 4732 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-005-registry-openrouter-167-rekaai-reka-edge/usage_by_question.csv` | PRESENT | 33494 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-005-registry-openrouter-167-rekaai-reka-edge/usage_by_sample.csv` | PRESENT | 37870 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-005-registry-openrouter-167-rekaai-reka-edge/failure_gallery.md` | PRESENT | 22070 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-006-registry-openrouter-111-google-gemma-3-27b-it/summary.csv` | PRESENT | 1283 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-006-registry-openrouter-111-google-gemma-3-27b-it/usage_by_family.csv` | PRESENT | 2874 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-006-registry-openrouter-111-google-gemma-3-27b-it/usage_by_section.csv` | PRESENT | 4846 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-006-registry-openrouter-111-google-gemma-3-27b-it/usage_by_question.csv` | PRESENT | 31820 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-006-registry-openrouter-111-google-gemma-3-27b-it/usage_by_sample.csv` | PRESENT | 35667 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-006-registry-openrouter-111-google-gemma-3-27b-it/failure_gallery.md` | PRESENT | 22143 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/summary.csv` | PRESENT | 1314 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/usage_by_family.csv` | PRESENT | 3086 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/usage_by_section.csv` | PRESENT | 5130 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/usage_by_question.csv` | PRESENT | 34561 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/usage_by_sample.csv` | PRESENT | 38476 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-007-registry-openrouter-104-mistralai-mistral-small-3-2-24b-instruct/failure_gallery.md` | PRESENT | 23179 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-008-registry-openrouter-094-mistralai-ministral-8b-2512/summary.csv` | PRESENT | 1220 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-008-registry-openrouter-094-mistralai-ministral-8b-2512/usage_by_family.csv` | PRESENT | 2612 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-008-registry-openrouter-094-mistralai-ministral-8b-2512/usage_by_section.csv` | PRESENT | 4400 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-008-registry-openrouter-094-mistralai-ministral-8b-2512/usage_by_question.csv` | PRESENT | 31937 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-008-registry-openrouter-094-mistralai-ministral-8b-2512/usage_by_sample.csv` | PRESENT | 35809 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-008-registry-openrouter-094-mistralai-ministral-8b-2512/failure_gallery.md` | PRESENT | 22337 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/summary.csv` | PRESENT | 1231 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/usage_by_family.csv` | PRESENT | 2552 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/usage_by_section.csv` | PRESENT | 4285 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/usage_by_question.csv` | PRESENT | 31337 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/usage_by_sample.csv` | PRESENT | 35249 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-009-registry-openrouter-102-bytedance-ui-tars-1-5-7b/failure_gallery.md` | PRESENT | 19275 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/summary.csv` | PRESENT | 1319 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/usage_by_family.csv` | PRESENT | 3254 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/usage_by_section.csv` | PRESENT | 5606 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/usage_by_question.csv` | PRESENT | 38232 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/usage_by_sample.csv` | PRESENT | 39118 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-010-registry-openrouter-090-qwen-qwen3-5-flash-02-23/failure_gallery.md` | PRESENT | 2698 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/summary.csv` | PRESENT | 1185 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/usage_by_family.csv` | PRESENT | 2473 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/usage_by_section.csv` | PRESENT | 4258 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/usage_by_question.csv` | PRESENT | 31701 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/usage_by_sample.csv` | PRESENT | 36992 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-011-registry-openrouter-105-meta-llama-llama-guard-4-12b/failure_gallery.md` | PRESENT | 22464 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-012-registry-openrouter-107-meta-llama-llama-4-scout/summary.csv` | PRESENT | 1236 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-012-registry-openrouter-107-meta-llama-llama-4-scout/usage_by_family.csv` | PRESENT | 2547 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-012-registry-openrouter-107-meta-llama-llama-4-scout/usage_by_section.csv` | PRESENT | 4302 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-012-registry-openrouter-107-meta-llama-llama-4-scout/usage_by_question.csv` | PRESENT | 31380 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-012-registry-openrouter-107-meta-llama-llama-4-scout/usage_by_sample.csv` | PRESENT | 35430 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-012-registry-openrouter-107-meta-llama-llama-4-scout/failure_gallery.md` | PRESENT | 23573 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/summary.csv` | PRESENT | 1265 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/usage_by_family.csv` | PRESENT | 2807 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/usage_by_section.csv` | PRESENT | 4627 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/usage_by_question.csv` | PRESENT | 31963 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/usage_by_sample.csv` | PRESENT | 35402 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-013-registry-openrouter-084-google-gemma-4-26b-a4b-it/failure_gallery.md` | PRESENT | 6928 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-014-registry-openrouter-093-mistralai-ministral-14b-2512/summary.csv` | PRESENT | 1247 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-014-registry-openrouter-093-mistralai-ministral-14b-2512/usage_by_family.csv` | PRESENT | 2582 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-014-registry-openrouter-093-mistralai-ministral-14b-2512/usage_by_section.csv` | PRESENT | 4416 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-014-registry-openrouter-093-mistralai-ministral-14b-2512/usage_by_question.csv` | PRESENT | 31997 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-014-registry-openrouter-093-mistralai-ministral-14b-2512/usage_by_sample.csv` | PRESENT | 35906 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-014-registry-openrouter-093-mistralai-ministral-14b-2512/failure_gallery.md` | PRESENT | 22385 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/summary.csv` | PRESENT | 1252 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/usage_by_family.csv` | PRESENT | 2692 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/usage_by_section.csv` | PRESENT | 4594 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/usage_by_question.csv` | PRESENT | 32784 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/usage_by_sample.csv` | PRESENT | 36541 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-015-registry-openrouter-096-mistralai-voxtral-small-24b-2507/failure_gallery.md` | PRESENT | 16726 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-016-registry-openrouter-163-xiaomi-mimo-v2-5/summary.csv` | PRESENT | 1305 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-016-registry-openrouter-163-xiaomi-mimo-v2-5/usage_by_family.csv` | PRESENT | 3181 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-016-registry-openrouter-163-xiaomi-mimo-v2-5/usage_by_section.csv` | PRESENT | 5419 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-016-registry-openrouter-163-xiaomi-mimo-v2-5/usage_by_question.csv` | PRESENT | 37267 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-016-registry-openrouter-163-xiaomi-mimo-v2-5/usage_by_sample.csv` | PRESENT | 38055 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-016-registry-openrouter-163-xiaomi-mimo-v2-5/failure_gallery.md` | PRESENT | 1949 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-017-registry-openrouter-165-google-gemma-4-31b-it/summary.csv` | PRESENT | 1255 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-017-registry-openrouter-165-google-gemma-4-31b-it/usage_by_family.csv` | PRESENT | 2590 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-017-registry-openrouter-165-google-gemma-4-31b-it/usage_by_section.csv` | PRESENT | 4383 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-017-registry-openrouter-165-google-gemma-4-31b-it/usage_by_question.csv` | PRESENT | 31275 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-017-registry-openrouter-165-google-gemma-4-31b-it/usage_by_sample.csv` | PRESENT | 34617 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-017-registry-openrouter-165-google-gemma-4-31b-it/failure_gallery.md` | PRESENT | 6061 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/summary.csv` | PRESENT | 1267 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/usage_by_family.csv` | PRESENT | 2864 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/usage_by_section.csv` | PRESENT | 4806 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/usage_by_question.csv` | PRESENT | 34207 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/usage_by_sample.csv` | PRESENT | 37840 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-018-registry-openrouter-177-meta-llama-llama-3-2-11b-vision-instruct/failure_gallery.md` | PRESENT | 16463 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-019-registry-openai-gpt-4-1-nano/summary.csv` | PRESENT | 1196 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-019-registry-openai-gpt-4-1-nano/usage_by_family.csv` | PRESENT | 2288 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-019-registry-openai-gpt-4-1-nano/usage_by_section.csv` | PRESENT | 3876 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-019-registry-openai-gpt-4-1-nano/usage_by_question.csv` | PRESENT | 28759 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-019-registry-openai-gpt-4-1-nano/usage_by_sample.csv` | PRESENT | 32453 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-019-registry-openai-gpt-4-1-nano/failure_gallery.md` | PRESENT | 11378 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-020-registry-openrouter-097-qwen-qwen3-vl-32b-instruct/summary.csv` | PRESENT | 1323 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-020-registry-openrouter-097-qwen-qwen3-vl-32b-instruct/usage_by_family.csv` | PRESENT | 2638 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-020-registry-openrouter-097-qwen-qwen3-vl-32b-instruct/usage_by_section.csv` | PRESENT | 4099 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-020-registry-openrouter-097-qwen-qwen3-vl-32b-instruct/usage_by_question.csv` | PRESENT | 23273 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-020-registry-openrouter-097-qwen-qwen3-vl-32b-instruct/usage_by_sample.csv` | PRESENT | 26298 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-020-registry-openrouter-097-qwen-qwen3-vl-32b-instruct/failure_gallery.md` | PRESENT | 6054 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/summary.csv` | PRESENT | 1292 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/usage_by_family.csv` | PRESENT | 2603 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/usage_by_section.csv` | PRESENT | 4400 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/usage_by_question.csv` | PRESENT | 31706 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/usage_by_sample.csv` | PRESENT | 35469 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-021-registry-openrouter-098-qwen-qwen3-vl-8b-instruct/failure_gallery.md` | PRESENT | 20764 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/summary.csv` | PRESENT | 1225 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/usage_by_family.csv` | PRESENT | 2667 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/usage_by_section.csv` | PRESENT | 4550 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/usage_by_question.csv` | PRESENT | 32468 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/usage_by_sample.csv` | PRESENT | 36238 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-022-registry-openrouter-099-qwen-qwen3-vl-30b-a3b-instruct/failure_gallery.md` | PRESENT | 20858 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-023-registry-openrouter-101-baidu-ernie-4-5-vl-28b-a3b/summary.csv` | PRESENT | 1149 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-023-registry-openrouter-101-baidu-ernie-4-5-vl-28b-a3b/usage_by_family.csv` | PRESENT | 2262 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-023-registry-openrouter-101-baidu-ernie-4-5-vl-28b-a3b/usage_by_section.csv` | PRESENT | 2415 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-023-registry-openrouter-101-baidu-ernie-4-5-vl-28b-a3b/usage_by_question.csv` | PRESENT | 7402 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-023-registry-openrouter-101-baidu-ernie-4-5-vl-28b-a3b/usage_by_sample.csv` | PRESENT | 8671 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-023-registry-openrouter-101-baidu-ernie-4-5-vl-28b-a3b/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-024-registry-openai-gpt-4o-mini/summary.csv` | PRESENT | 1205 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-024-registry-openai-gpt-4o-mini/usage_by_family.csv` | PRESENT | 2275 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-024-registry-openai-gpt-4o-mini/usage_by_section.csv` | PRESENT | 3841 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-024-registry-openai-gpt-4o-mini/usage_by_question.csv` | PRESENT | 28716 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-024-registry-openai-gpt-4o-mini/usage_by_sample.csv` | PRESENT | 32497 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-024-registry-openai-gpt-4o-mini/failure_gallery.md` | PRESENT | 19242 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-025-registry-openrouter-085-mistralai-mistral-small-2603/summary.csv` | PRESENT | 1246 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-025-registry-openrouter-085-mistralai-mistral-small-2603/usage_by_family.csv` | PRESENT | 2631 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-025-registry-openrouter-085-mistralai-mistral-small-2603/usage_by_section.csv` | PRESENT | 4473 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-025-registry-openrouter-085-mistralai-mistral-small-2603/usage_by_question.csv` | PRESENT | 32227 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-025-registry-openrouter-085-mistralai-mistral-small-2603/usage_by_sample.csv` | PRESENT | 35852 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-025-registry-openrouter-085-mistralai-mistral-small-2603/failure_gallery.md` | PRESENT | 15260 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-026-registry-openrouter-106-meta-llama-llama-4-maverick/summary.csv` | PRESENT | 1288 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-026-registry-openrouter-106-meta-llama-llama-4-maverick/usage_by_family.csv` | PRESENT | 3020 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-026-registry-openrouter-106-meta-llama-llama-4-maverick/usage_by_section.csv` | PRESENT | 5150 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-026-registry-openrouter-106-meta-llama-llama-4-maverick/usage_by_question.csv` | PRESENT | 33460 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-026-registry-openrouter-106-meta-llama-llama-4-maverick/usage_by_sample.csv` | PRESENT | 37227 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-026-registry-openrouter-106-meta-llama-llama-4-maverick/failure_gallery.md` | PRESENT | 20159 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-027-registry-openrouter-176-mistralai-mistral-saba/summary.csv` | PRESENT | 1233 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-027-registry-openrouter-176-mistralai-mistral-saba/usage_by_family.csv` | PRESENT | 2545 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-027-registry-openrouter-176-mistralai-mistral-saba/usage_by_section.csv` | PRESENT | 4291 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-027-registry-openrouter-176-mistralai-mistral-saba/usage_by_question.csv` | PRESENT | 31183 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-027-registry-openrouter-176-mistralai-mistral-saba/usage_by_sample.csv` | PRESENT | 34900 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-027-registry-openrouter-176-mistralai-mistral-saba/failure_gallery.md` | PRESENT | 17462 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-028-registry-openrouter-108-mistralai-mistral-small-3-1-24b-instruct/summary.csv` | PRESENT | 1207 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-028-registry-openrouter-108-mistralai-mistral-small-3-1-24b-instruct/usage_by_family.csv` | PRESENT | 2498 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-028-registry-openrouter-108-mistralai-mistral-small-3-1-24b-instruct/usage_by_section.csv` | PRESENT | 2942 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-028-registry-openrouter-108-mistralai-mistral-small-3-1-24b-instruct/usage_by_question.csv` | PRESENT | 12344 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-028-registry-openrouter-108-mistralai-mistral-small-3-1-24b-instruct/usage_by_sample.csv` | PRESENT | 14384 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-028-registry-openrouter-108-mistralai-mistral-small-3-1-24b-instruct/failure_gallery.md` | PRESENT | 1885 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/summary.csv` | PRESENT | 1282 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/usage_by_family.csv` | PRESENT | 2916 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/usage_by_section.csv` | PRESENT | 4869 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/usage_by_question.csv` | PRESENT | 32690 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/usage_by_sample.csv` | PRESENT | 36234 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-029-registry-openrouter-112-qwen-qwen2-5-vl-72b-instruct/failure_gallery.md` | PRESENT | 10850 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/summary.csv` | PRESENT | 1231 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/usage_by_family.csv` | PRESENT | 2685 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/usage_by_section.csv` | PRESENT | 4611 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/usage_by_question.csv` | PRESENT | 32918 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/usage_by_sample.csv` | PRESENT | 36398 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-030-registry-openrouter-100-qwen-qwen3-vl-235b-a22b-instruct/failure_gallery.md` | PRESENT | 10663 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/summary.csv` | PRESENT | 1300 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/usage_by_family.csv` | PRESENT | 3204 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/usage_by_section.csv` | PRESENT | 5488 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/usage_by_question.csv` | PRESENT | 37382 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/usage_by_sample.csv` | PRESENT | 38436 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-031-registry-openrouter-082-qwen-qwen3-6-35b-a3b/failure_gallery.md` | PRESENT | 3633 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/summary.csv` | PRESENT | 1305 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/usage_by_family.csv` | PRESENT | 3213 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/usage_by_section.csv` | PRESENT | 5573 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/usage_by_question.csv` | PRESENT | 37702 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/usage_by_sample.csv` | PRESENT | 38610 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-032-registry-openrouter-087-qwen-qwen3-5-35b-a3b/failure_gallery.md` | PRESENT | 5139 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-033-registry-openrouter-170-z-ai-glm-4-6v/summary.csv` | PRESENT | 1249 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-033-registry-openrouter-170-z-ai-glm-4-6v/usage_by_family.csv` | PRESENT | 3078 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-033-registry-openrouter-170-z-ai-glm-4-6v/usage_by_section.csv` | PRESENT | 5274 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-033-registry-openrouter-170-z-ai-glm-4-6v/usage_by_question.csv` | PRESENT | 36125 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-033-registry-openrouter-170-z-ai-glm-4-6v/usage_by_sample.csv` | PRESENT | 37132 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-033-registry-openrouter-170-z-ai-glm-4-6v/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-034-registry-openrouter-174-mistralai-codestral-2508/summary.csv` | PRESENT | 1231 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-034-registry-openrouter-174-mistralai-codestral-2508/usage_by_family.csv` | PRESENT | 2562 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-034-registry-openrouter-174-mistralai-codestral-2508/usage_by_section.csv` | PRESENT | 4326 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-034-registry-openrouter-174-mistralai-codestral-2508/usage_by_question.csv` | PRESENT | 31506 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-034-registry-openrouter-174-mistralai-codestral-2508/usage_by_sample.csv` | PRESENT | 35319 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-034-registry-openrouter-174-mistralai-codestral-2508/failure_gallery.md` | PRESENT | 21291 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-035-registry-openrouter-113-minimax-minimax-01/summary.csv` | PRESENT | 1227 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-035-registry-openrouter-113-minimax-minimax-01/usage_by_family.csv` | PRESENT | 2518 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-035-registry-openrouter-113-minimax-minimax-01/usage_by_section.csv` | PRESENT | 4242 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-035-registry-openrouter-113-minimax-minimax-01/usage_by_question.csv` | PRESENT | 30999 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-035-registry-openrouter-113-minimax-minimax-01/usage_by_sample.csv` | PRESENT | 34342 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-035-registry-openrouter-113-minimax-minimax-01/failure_gallery.md` | PRESENT | 11038 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-036-registry-openrouter-081-qwen-qwen3-6-flash/summary.csv` | PRESENT | 1307 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-036-registry-openrouter-081-qwen-qwen3-6-flash/usage_by_family.csv` | PRESENT | 3151 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-036-registry-openrouter-081-qwen-qwen3-6-flash/usage_by_section.csv` | PRESENT | 5442 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-036-registry-openrouter-081-qwen-qwen3-6-flash/usage_by_question.csv` | PRESENT | 37468 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-036-registry-openrouter-081-qwen-qwen3-6-flash/usage_by_sample.csv` | PRESENT | 38282 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-036-registry-openrouter-081-qwen-qwen3-6-flash/failure_gallery.md` | PRESENT | 2619 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-037-registry-openai-gpt-5-4-nano-none/summary.csv` | PRESENT | 1190 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-037-registry-openai-gpt-5-4-nano-none/usage_by_family.csv` | PRESENT | 2379 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-037-registry-openai-gpt-5-4-nano-none/usage_by_section.csv` | PRESENT | 3983 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-037-registry-openai-gpt-5-4-nano-none/usage_by_question.csv` | PRESENT | 29678 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-037-registry-openai-gpt-5-4-nano-none/usage_by_sample.csv` | PRESENT | 33927 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-037-registry-openai-gpt-5-4-nano-none/failure_gallery.md` | PRESENT | 13316 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/summary.csv` | PRESENT | 1323 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/usage_by_family.csv` | PRESENT | 3288 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/usage_by_section.csv` | PRESENT | 5657 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/usage_by_question.csv` | PRESENT | 37917 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/usage_by_sample.csv` | PRESENT | 39084 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-038-registry-openrouter-122-qwen-qwen3-vl-8b-thinking/failure_gallery.md` | PRESENT | 19468 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-039-registry-openrouter-080-minimax-minimax-m3/summary.csv` | PRESENT | 1270 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-039-registry-openrouter-080-minimax-minimax-m3/usage_by_family.csv` | PRESENT | 2984 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-039-registry-openrouter-080-minimax-minimax-m3/usage_by_section.csv` | PRESENT | 5133 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-039-registry-openrouter-080-minimax-minimax-m3/usage_by_question.csv` | PRESENT | 35728 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-039-registry-openrouter-080-minimax-minimax-m3/usage_by_sample.csv` | PRESENT | 37129 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-039-registry-openrouter-080-minimax-minimax-m3/failure_gallery.md` | PRESENT | 1105 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/summary.csv` | PRESENT | 1242 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/usage_by_family.csv` | PRESENT | 2610 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/usage_by_section.csv` | PRESENT | 4503 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/usage_by_question.csv` | PRESENT | 32381 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/usage_by_sample.csv` | PRESENT | 35849 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-040-registry-openrouter-103-baidu-ernie-4-5-vl-424b-a47b/failure_gallery.md` | PRESENT | 66319 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/summary.csv` | PRESENT | 1334 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/usage_by_family.csv` | PRESENT | 3393 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/usage_by_section.csv` | PRESENT | 5800 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/usage_by_question.csv` | PRESENT | 39211 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/usage_by_sample.csv` | PRESENT | 40183 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-041-registry-openrouter-123-qwen-qwen3-vl-30b-a3b-thinking/failure_gallery.md` | PRESENT | 7791 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-042-registry-gemini-3-1-flash-lite/summary.csv` | PRESENT | 1211 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-042-registry-gemini-3-1-flash-lite/usage_by_family.csv` | PRESENT | 2412 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-042-registry-gemini-3-1-flash-lite/usage_by_section.csv` | PRESENT | 4127 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-042-registry-gemini-3-1-flash-lite/usage_by_question.csv` | PRESENT | 30417 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-042-registry-gemini-3-1-flash-lite/usage_by_sample.csv` | PRESENT | 33916 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-042-registry-gemini-3-1-flash-lite/failure_gallery.md` | PRESENT | 10305 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-043-registry-openrouter-088-qwen-qwen3-5-27b/summary.csv` | PRESENT | 1281 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-043-registry-openrouter-088-qwen-qwen3-5-27b/usage_by_family.csv` | PRESENT | 3167 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-043-registry-openrouter-088-qwen-qwen3-5-27b/usage_by_section.csv` | PRESENT | 5391 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-043-registry-openrouter-088-qwen-qwen3-5-27b/usage_by_question.csv` | PRESENT | 37210 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-043-registry-openrouter-088-qwen-qwen3-5-27b/usage_by_sample.csv` | PRESENT | 37949 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-043-registry-openrouter-088-qwen-qwen3-5-27b/failure_gallery.md` | PRESENT | 1693 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/summary.csv` | PRESENT | 1310 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/usage_by_family.csv` | PRESENT | 2414 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/usage_by_section.csv` | PRESENT | 4089 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/usage_by_question.csv` | PRESENT | 30330 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/usage_by_sample.csv` | PRESENT | 34302 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-044-registry-openrouter-168-qwen-qwen3-5-plus-02-15/failure_gallery.md` | PRESENT | 4536 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-045-registry-openrouter-171-mistralai-mistral-large-2512/summary.csv` | PRESENT | 1250 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-045-registry-openrouter-171-mistralai-mistral-large-2512/usage_by_family.csv` | PRESENT | 2614 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-045-registry-openrouter-171-mistralai-mistral-large-2512/usage_by_section.csv` | PRESENT | 4466 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-045-registry-openrouter-171-mistralai-mistral-large-2512/usage_by_question.csv` | PRESENT | 32162 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-045-registry-openrouter-171-mistralai-mistral-large-2512/usage_by_sample.csv` | PRESENT | 35937 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-045-registry-openrouter-171-mistralai-mistral-large-2512/failure_gallery.md` | PRESENT | 102407 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/summary.csv` | PRESENT | 1316 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/usage_by_family.csv` | PRESENT | 3291 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/usage_by_section.csv` | PRESENT | 5701 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/usage_by_question.csv` | PRESENT | 38137 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/usage_by_sample.csv` | PRESENT | 39132 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-046-registry-openrouter-162-qwen-qwen3-5-plus-20260420/failure_gallery.md` | PRESENT | 1129 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-047-registry-openai-gpt-5-mini-minimal/summary.csv` | PRESENT | 1217 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-047-registry-openai-gpt-5-mini-minimal/usage_by_family.csv` | PRESENT | 2345 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-047-registry-openai-gpt-5-mini-minimal/usage_by_section.csv` | PRESENT | 4015 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-047-registry-openai-gpt-5-mini-minimal/usage_by_question.csv` | PRESENT | 29643 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-047-registry-openai-gpt-5-mini-minimal/usage_by_sample.csv` | PRESENT | 34053 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-047-registry-openai-gpt-5-mini-minimal/failure_gallery.md` | PRESENT | 10547 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-048-registry-openrouter-166-qwen-qwen3-6-plus/summary.csv` | PRESENT | 1263 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-048-registry-openrouter-166-qwen-qwen3-6-plus/usage_by_family.csv` | PRESENT | 3123 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-048-registry-openrouter-166-qwen-qwen3-6-plus/usage_by_section.csv` | PRESENT | 5416 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-048-registry-openrouter-166-qwen-qwen3-6-plus/usage_by_question.csv` | PRESENT | 37324 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-048-registry-openrouter-166-qwen-qwen3-6-plus/usage_by_sample.csv` | PRESENT | 38040 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-048-registry-openrouter-166-qwen-qwen3-6-plus/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-049-registry-openrouter-169-moonshotai-kimi-k2-5/summary.csv` | PRESENT | 1259 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-049-registry-openrouter-169-moonshotai-kimi-k2-5/usage_by_family.csv` | PRESENT | 3173 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-049-registry-openrouter-169-moonshotai-kimi-k2-5/usage_by_section.csv` | PRESENT | 5443 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-049-registry-openrouter-169-moonshotai-kimi-k2-5/usage_by_question.csv` | PRESENT | 37402 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-049-registry-openrouter-169-moonshotai-kimi-k2-5/usage_by_sample.csv` | PRESENT | 38326 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-049-registry-openrouter-169-moonshotai-kimi-k2-5/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/summary.csv` | PRESENT | 1312 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/usage_by_family.csv` | PRESENT | 3267 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/usage_by_section.csv` | PRESENT | 5602 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/usage_by_question.csv` | PRESENT | 37984 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/usage_by_sample.csv` | PRESENT | 38806 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-050-registry-openrouter-089-qwen-qwen3-5-122b-a10b/failure_gallery.md` | PRESENT | 4307 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-051-registry-openrouter-092-mistralai-devstral-2512/summary.csv` | PRESENT | 1239 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-051-registry-openrouter-092-mistralai-devstral-2512/usage_by_family.csv` | PRESENT | 2555 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-051-registry-openrouter-092-mistralai-devstral-2512/usage_by_section.csv` | PRESENT | 4318 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-051-registry-openrouter-092-mistralai-devstral-2512/usage_by_question.csv` | PRESENT | 31496 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-051-registry-openrouter-092-mistralai-devstral-2512/usage_by_sample.csv` | PRESENT | 35195 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-051-registry-openrouter-092-mistralai-devstral-2512/failure_gallery.md` | PRESENT | 19441 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/summary.csv` | PRESENT | 1248 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/usage_by_family.csv` | PRESENT | 2617 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/usage_by_section.csv` | PRESENT | 4433 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/usage_by_question.csv` | PRESENT | 32132 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/usage_by_sample.csv` | PRESENT | 35912 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-052-registry-openrouter-172-mistralai-mistral-medium-3-1/failure_gallery.md` | PRESENT | 20540 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-053-registry-openrouter-173-z-ai-glm-4-5v/summary.csv` | PRESENT | 1292 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-053-registry-openrouter-173-z-ai-glm-4-5v/usage_by_family.csv` | PRESENT | 3088 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-053-registry-openrouter-173-z-ai-glm-4-5v/usage_by_section.csv` | PRESENT | 5264 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-053-registry-openrouter-173-z-ai-glm-4-5v/usage_by_question.csv` | PRESENT | 36196 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-053-registry-openrouter-173-z-ai-glm-4-5v/usage_by_sample.csv` | PRESENT | 37514 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-053-registry-openrouter-173-z-ai-glm-4-5v/failure_gallery.md` | PRESENT | 22081 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-054-registry-openrouter-175-mistralai-mistral-medium-3/summary.csv` | PRESENT | 1239 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-054-registry-openrouter-175-mistralai-mistral-medium-3/usage_by_family.csv` | PRESENT | 2541 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-054-registry-openrouter-175-mistralai-mistral-medium-3/usage_by_section.csv` | PRESENT | 4346 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-054-registry-openrouter-175-mistralai-mistral-medium-3/usage_by_question.csv` | PRESENT | 31808 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-054-registry-openrouter-175-mistralai-mistral-medium-3/usage_by_sample.csv` | PRESENT | 35696 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-054-registry-openrouter-175-mistralai-mistral-medium-3/failure_gallery.md` | PRESENT | 23184 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/summary.csv` | PRESENT | 1310 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/usage_by_family.csv` | PRESENT | 3261 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/usage_by_section.csv` | PRESENT | 5576 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/usage_by_question.csv` | PRESENT | 38131 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/usage_by_sample.csv` | PRESENT | 38858 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-055-registry-openrouter-091-qwen-qwen3-5-397b-a17b/failure_gallery.md` | PRESENT | 875 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-056-registry-gemini-2-5-flash/summary.csv` | PRESENT | 1292 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-056-registry-gemini-2-5-flash/usage_by_family.csv` | PRESENT | 2965 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-056-registry-gemini-2-5-flash/usage_by_section.csv` | PRESENT | 5089 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-056-registry-gemini-2-5-flash/usage_by_question.csv` | PRESENT | 35037 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-056-registry-gemini-2-5-flash/usage_by_sample.csv` | PRESENT | 37035 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-056-registry-gemini-2-5-flash/failure_gallery.md` | PRESENT | 9951 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/summary.csv` | PRESENT | 1330 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/usage_by_family.csv` | PRESENT | 3383 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/usage_by_section.csv` | PRESENT | 5851 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/usage_by_question.csv` | PRESENT | 39661 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/usage_by_sample.csv` | PRESENT | 40427 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-057-registry-openrouter-124-qwen-qwen3-vl-235b-a22b-thinking/failure_gallery.md` | PRESENT | 1147 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-058-registry-grok-build-0-1/summary.csv` | PRESENT | 1248 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-058-registry-grok-build-0-1/usage_by_family.csv` | PRESENT | 2740 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-058-registry-grok-build-0-1/usage_by_section.csv` | PRESENT | 4723 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-058-registry-grok-build-0-1/usage_by_question.csv` | PRESENT | 33254 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-058-registry-grok-build-0-1/usage_by_sample.csv` | PRESENT | 35461 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-058-registry-grok-build-0-1/failure_gallery.md` | PRESENT | 15137 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-059-registry-openrouter-083-qwen-qwen3-6-27b/summary.csv` | PRESENT | 1290 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-059-registry-openrouter-083-qwen-qwen3-6-27b/usage_by_family.csv` | PRESENT | 3170 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-059-registry-openrouter-083-qwen-qwen3-6-27b/usage_by_section.csv` | PRESENT | 5309 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-059-registry-openrouter-083-qwen-qwen3-6-27b/usage_by_question.csv` | PRESENT | 36729 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-059-registry-openrouter-083-qwen-qwen3-6-27b/usage_by_sample.csv` | PRESENT | 37731 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-059-registry-openrouter-083-qwen-qwen3-6-27b/failure_gallery.md` | PRESENT | 4388 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-060-registry-gemini-3-flash-preview/summary.csv` | PRESENT | 1251 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-060-registry-gemini-3-flash-preview/usage_by_family.csv` | PRESENT | 3113 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-060-registry-gemini-3-flash-preview/usage_by_section.csv` | PRESENT | 5277 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-060-registry-gemini-3-flash-preview/usage_by_question.csv` | PRESENT | 36164 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-060-registry-gemini-3-flash-preview/usage_by_sample.csv` | PRESENT | 37814 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-060-registry-gemini-3-flash-preview/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-061-registry-openrouter-139-qwen-qwen3-coder-plus/summary.csv` | PRESENT | 1227 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-061-registry-openrouter-139-qwen-qwen3-coder-plus/usage_by_family.csv` | PRESENT | 2513 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-061-registry-openrouter-139-qwen-qwen3-coder-plus/usage_by_section.csv` | PRESENT | 4290 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-061-registry-openrouter-139-qwen-qwen3-coder-plus/usage_by_question.csv` | PRESENT | 31133 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-061-registry-openrouter-139-qwen-qwen3-coder-plus/usage_by_sample.csv` | PRESENT | 34719 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-061-registry-openrouter-139-qwen-qwen3-coder-plus/failure_gallery.md` | PRESENT | 14917 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-062-registry-openrouter-144-nousresearch-hermes-4-405b/summary.csv` | PRESENT | 1233 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-062-registry-openrouter-144-nousresearch-hermes-4-405b/usage_by_family.csv` | PRESENT | 2578 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-062-registry-openrouter-144-nousresearch-hermes-4-405b/usage_by_section.csv` | PRESENT | 4362 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-062-registry-openrouter-144-nousresearch-hermes-4-405b/usage_by_question.csv` | PRESENT | 31765 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-062-registry-openrouter-144-nousresearch-hermes-4-405b/usage_by_sample.csv` | PRESENT | 35300 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-062-registry-openrouter-144-nousresearch-hermes-4-405b/failure_gallery.md` | PRESENT | 8708 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-063-registry-openrouter-128-z-ai-glm-5-1/summary.csv` | PRESENT | 1252 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-063-registry-openrouter-128-z-ai-glm-5-1/usage_by_family.csv` | PRESENT | 3059 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-063-registry-openrouter-128-z-ai-glm-5-1/usage_by_section.csv` | PRESENT | 5283 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-063-registry-openrouter-128-z-ai-glm-5-1/usage_by_question.csv` | PRESENT | 36326 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-063-registry-openrouter-128-z-ai-glm-5-1/usage_by_sample.csv` | PRESENT | 37150 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-063-registry-openrouter-128-z-ai-glm-5-1/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-064-registry-openrouter-161-moonshotai-kimi-latest/summary.csv` | PRESENT | 1312 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-064-registry-openrouter-161-moonshotai-kimi-latest/usage_by_family.csv` | PRESENT | 3257 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-064-registry-openrouter-161-moonshotai-kimi-latest/usage_by_section.csv` | PRESENT | 5545 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-064-registry-openrouter-161-moonshotai-kimi-latest/usage_by_question.csv` | PRESENT | 37940 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-064-registry-openrouter-161-moonshotai-kimi-latest/usage_by_sample.csv` | PRESENT | 38814 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-064-registry-openrouter-161-moonshotai-kimi-latest/failure_gallery.md` | PRESENT | 907 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-065-registry-openrouter-164-moonshotai-kimi-k2-6/summary.csv` | PRESENT | 1268 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-065-registry-openrouter-164-moonshotai-kimi-k2-6/usage_by_family.csv` | PRESENT | 3199 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-065-registry-openrouter-164-moonshotai-kimi-k2-6/usage_by_section.csv` | PRESENT | 5469 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-065-registry-openrouter-164-moonshotai-kimi-k2-6/usage_by_question.csv` | PRESENT | 37320 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-065-registry-openrouter-164-moonshotai-kimi-k2-6/usage_by_sample.csv` | PRESENT | 38303 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-065-registry-openrouter-164-moonshotai-kimi-k2-6/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-066-registry-openrouter-138-qwen-qwen3-max/summary.csv` | PRESENT | 1212 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-066-registry-openrouter-138-qwen-qwen3-max/usage_by_family.csv` | PRESENT | 2311 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-066-registry-openrouter-138-qwen-qwen3-max/usage_by_section.csv` | PRESENT | 3844 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-066-registry-openrouter-138-qwen-qwen3-max/usage_by_question.csv` | PRESENT | 28915 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-066-registry-openrouter-138-qwen-qwen3-max/usage_by_sample.csv` | PRESENT | 33459 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-066-registry-openrouter-138-qwen-qwen3-max/failure_gallery.md` | PRESENT | 6716 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-067-registry-openrouter-178-qwen-qwen3-7-max/summary.csv` | PRESENT | 1256 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-067-registry-openrouter-178-qwen-qwen3-7-max/usage_by_family.csv` | PRESENT | 3117 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-067-registry-openrouter-178-qwen-qwen3-7-max/usage_by_section.csv` | PRESENT | 5374 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-067-registry-openrouter-178-qwen-qwen3-7-max/usage_by_question.csv` | PRESENT | 36783 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-067-registry-openrouter-178-qwen-qwen3-7-max/usage_by_sample.csv` | PRESENT | 37661 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-067-registry-openrouter-178-qwen-qwen3-7-max/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-068-registry-openrouter-180-z-ai-glm-5-turbo/summary.csv` | PRESENT | 1296 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-068-registry-openrouter-180-z-ai-glm-5-turbo/usage_by_family.csv` | PRESENT | 3123 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-068-registry-openrouter-180-z-ai-glm-5-turbo/usage_by_section.csv` | PRESENT | 5347 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-068-registry-openrouter-180-z-ai-glm-5-turbo/usage_by_question.csv` | PRESENT | 36665 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-068-registry-openrouter-180-z-ai-glm-5-turbo/usage_by_sample.csv` | PRESENT | 37692 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-068-registry-openrouter-180-z-ai-glm-5-turbo/failure_gallery.md` | PRESENT | 1738 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-069-registry-openrouter-184-z-ai-glm-5v-turbo/summary.csv` | PRESENT | 1301 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-069-registry-openrouter-184-z-ai-glm-5v-turbo/usage_by_family.csv` | PRESENT | 3132 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-069-registry-openrouter-184-z-ai-glm-5v-turbo/usage_by_section.csv` | PRESENT | 5422 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-069-registry-openrouter-184-z-ai-glm-5v-turbo/usage_by_question.csv` | PRESENT | 36966 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-069-registry-openrouter-184-z-ai-glm-5v-turbo/usage_by_sample.csv` | PRESENT | 38044 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-069-registry-openrouter-184-z-ai-glm-5v-turbo/failure_gallery.md` | PRESENT | 7950 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-070-registry-openai-gpt-5-4-mini-none/summary.csv` | PRESENT | 1216 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-070-registry-openai-gpt-5-4-mini-none/usage_by_family.csv` | PRESENT | 2351 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-070-registry-openai-gpt-5-4-mini-none/usage_by_section.csv` | PRESENT | 3989 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-070-registry-openai-gpt-5-4-mini-none/usage_by_question.csv` | PRESENT | 29677 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-070-registry-openai-gpt-5-4-mini-none/usage_by_sample.csv` | PRESENT | 33859 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-070-registry-openai-gpt-5-4-mini-none/failure_gallery.md` | PRESENT | 11726 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/summary.csv` | PRESENT | 1268 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/usage_by_family.csv` | PRESENT | 3248 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/usage_by_section.csv` | PRESENT | 5608 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/usage_by_question.csv` | PRESENT | 38305 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/usage_by_sample.csv` | PRESENT | 39081 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-071-registry-openrouter-179-qwen-qwen3-6-max-preview/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/summary.csv` | PRESENT | 1230 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/usage_by_family.csv` | PRESENT | 2592 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/usage_by_section.csv` | PRESENT | 4405 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/usage_by_question.csv` | PRESENT | 32175 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/usage_by_sample.csv` | PRESENT | 35735 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-072-registry-openrouter-114-anthracite-org-magnum-v4-72b/failure_gallery.md` | PRESENT | 10488 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/summary.csv` | PRESENT | 1243 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/usage_by_family.csv` | PRESENT | 2643 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/usage_by_section.csv` | PRESENT | 4538 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/usage_by_question.csv` | PRESENT | 32791 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/usage_by_sample.csv` | PRESENT | 36502 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-073-registry-openrouter-115-mistralai-mixtral-8x22b-instruct/failure_gallery.md` | PRESENT | 18177 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-074-registry-openrouter-185-mistralai-mistral-large-2407/summary.csv` | PRESENT | 1249 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-074-registry-openrouter-185-mistralai-mistral-large-2407/usage_by_family.csv` | PRESENT | 2621 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-074-registry-openrouter-185-mistralai-mistral-large-2407/usage_by_section.csv` | PRESENT | 4420 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-074-registry-openrouter-185-mistralai-mistral-large-2407/usage_by_question.csv` | PRESENT | 32083 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-074-registry-openrouter-185-mistralai-mistral-large-2407/usage_by_sample.csv` | PRESENT | 35865 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-074-registry-openrouter-185-mistralai-mistral-large-2407/failure_gallery.md` | PRESENT | 107691 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/summary.csv` | PRESENT | 1269 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/usage_by_family.csv` | PRESENT | 2749 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/usage_by_section.csv` | PRESENT | 4577 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/usage_by_question.csv` | PRESENT | 32398 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/usage_by_sample.csv` | PRESENT | 36038 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-075-registry-openrouter-183-mistralai-mistral-medium-3-5/failure_gallery.md` | PRESENT | 14091 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-076-registry-openrouter-181-ai21-jamba-large-1-7/summary.csv` | PRESENT | 1225 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-076-registry-openrouter-181-ai21-jamba-large-1-7/usage_by_family.csv` | PRESENT | 2494 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-076-registry-openrouter-181-ai21-jamba-large-1-7/usage_by_section.csv` | PRESENT | 4224 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-076-registry-openrouter-181-ai21-jamba-large-1-7/usage_by_question.csv` | PRESENT | 30890 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-076-registry-openrouter-181-ai21-jamba-large-1-7/usage_by_sample.csv` | PRESENT | 34668 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-076-registry-openrouter-181-ai21-jamba-large-1-7/failure_gallery.md` | PRESENT | 23298 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-077-registry-openai-gpt-5-minimal/summary.csv` | PRESENT | 1194 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-077-registry-openai-gpt-5-minimal/usage_by_family.csv` | PRESENT | 2297 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-077-registry-openai-gpt-5-minimal/usage_by_section.csv` | PRESENT | 3884 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-077-registry-openai-gpt-5-minimal/usage_by_question.csv` | PRESENT | 29027 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-077-registry-openai-gpt-5-minimal/usage_by_sample.csv` | PRESENT | 33206 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-077-registry-openai-gpt-5-minimal/failure_gallery.md` | PRESENT | 6357 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-078-registry-openai-gpt-4o/summary.csv` | PRESENT | 1182 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-078-registry-openai-gpt-4o/usage_by_family.csv` | PRESENT | 2208 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-078-registry-openai-gpt-4o/usage_by_section.csv` | PRESENT | 3743 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-078-registry-openai-gpt-4o/usage_by_question.csv` | PRESENT | 28082 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-078-registry-openai-gpt-4o/usage_by_sample.csv` | PRESENT | 31652 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-078-registry-openai-gpt-4o/failure_gallery.md` | PRESENT | 16655 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-079-registry-openrouter-182-cohere-command-a/summary.csv` | PRESENT | 1215 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-079-registry-openrouter-182-cohere-command-a/usage_by_family.csv` | PRESENT | 2375 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-079-registry-openrouter-182-cohere-command-a/usage_by_section.csv` | PRESENT | 4085 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-079-registry-openrouter-182-cohere-command-a/usage_by_question.csv` | PRESENT | 30236 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-079-registry-openrouter-182-cohere-command-a/usage_by_sample.csv` | PRESENT | 33799 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-079-registry-openrouter-182-cohere-command-a/failure_gallery.md` | PRESENT | 10782 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-080-registry-openai-gpt-5-2-none/summary.csv` | PRESENT | 1206 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-080-registry-openai-gpt-5-2-none/usage_by_family.csv` | PRESENT | 2286 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-080-registry-openai-gpt-5-2-none/usage_by_section.csv` | PRESENT | 3901 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-080-registry-openai-gpt-5-2-none/usage_by_question.csv` | PRESENT | 28996 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-080-registry-openai-gpt-5-2-none/usage_by_sample.csv` | PRESENT | 33045 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-080-registry-openai-gpt-5-2-none/failure_gallery.md` | PRESENT | 8640 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-081-registry-openai-gpt-5-4-none/summary.csv` | PRESENT | 1182 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-081-registry-openai-gpt-5-4-none/usage_by_family.csv` | PRESENT | 2256 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-081-registry-openai-gpt-5-4-none/usage_by_section.csv` | PRESENT | 3842 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-081-registry-openai-gpt-5-4-none/usage_by_question.csv` | PRESENT | 28925 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-081-registry-openai-gpt-5-4-none/usage_by_sample.csv` | PRESENT | 32955 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-081-registry-openai-gpt-5-4-none/failure_gallery.md` | PRESENT | 6360 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-082-registry-anthropic-claude-opus-4-6/summary.csv` | PRESENT | 1205 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-082-registry-anthropic-claude-opus-4-6/usage_by_family.csv` | PRESENT | 2338 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-082-registry-anthropic-claude-opus-4-6/usage_by_section.csv` | PRESENT | 4016 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-082-registry-anthropic-claude-opus-4-6/usage_by_question.csv` | PRESENT | 29990 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-082-registry-anthropic-claude-opus-4-6/usage_by_sample.csv` | PRESENT | 33373 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-082-registry-anthropic-claude-opus-4-6/failure_gallery.md` | PRESENT | 7710 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-083-registry-anthropic-claude-opus-4-7/summary.csv` | PRESENT | 1188 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-083-registry-anthropic-claude-opus-4-7/usage_by_family.csv` | PRESENT | 2368 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-083-registry-anthropic-claude-opus-4-7/usage_by_section.csv` | PRESENT | 4075 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-083-registry-anthropic-claude-opus-4-7/usage_by_question.csv` | PRESENT | 30015 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-083-registry-anthropic-claude-opus-4-7/usage_by_sample.csv` | PRESENT | 33324 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-083-registry-anthropic-claude-opus-4-7/failure_gallery.md` | PRESENT | 4054 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-084-registry-anthropic-claude-opus-4-8/summary.csv` | PRESENT | 1202 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-084-registry-anthropic-claude-opus-4-8/usage_by_family.csv` | PRESENT | 2366 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-084-registry-anthropic-claude-opus-4-8/usage_by_section.csv` | PRESENT | 4018 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-084-registry-anthropic-claude-opus-4-8/usage_by_question.csv` | PRESENT | 29998 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-084-registry-anthropic-claude-opus-4-8/usage_by_sample.csv` | PRESENT | 33375 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-084-registry-anthropic-claude-opus-4-8/failure_gallery.md` | PRESENT | 5046 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-085-registry-openai-gpt-5-5-low/summary.csv` | PRESENT | 1180 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-085-registry-openai-gpt-5-5-low/usage_by_family.csv` | PRESENT | 2486 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-085-registry-openai-gpt-5-5-low/usage_by_section.csv` | PRESENT | 4286 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-085-registry-openai-gpt-5-5-low/usage_by_question.csv` | PRESENT | 30892 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-085-registry-openai-gpt-5-5-low/usage_by_sample.csv` | PRESENT | 32726 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-085-registry-openai-gpt-5-5-low/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-086-registry-openai-gpt-5-5-none/summary.csv` | PRESENT | 1197 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-086-registry-openai-gpt-5-5-none/usage_by_family.csv` | PRESENT | 2261 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-086-registry-openai-gpt-5-5-none/usage_by_section.csv` | PRESENT | 3866 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-086-registry-openai-gpt-5-5-none/usage_by_question.csv` | PRESENT | 28841 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-086-registry-openai-gpt-5-5-none/usage_by_sample.csv` | PRESENT | 32859 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-086-registry-openai-gpt-5-5-none/failure_gallery.md` | PRESENT | 4784 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-087-thinking-openai-gpt-5-nano-minimal/summary.csv` | PRESENT | 1216 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-087-thinking-openai-gpt-5-nano-minimal/usage_by_family.csv` | PRESENT | 2316 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-087-thinking-openai-gpt-5-nano-minimal/usage_by_section.csv` | PRESENT | 3933 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-087-thinking-openai-gpt-5-nano-minimal/usage_by_question.csv` | PRESENT | 29261 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-087-thinking-openai-gpt-5-nano-minimal/usage_by_sample.csv` | PRESENT | 33469 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-087-thinking-openai-gpt-5-nano-minimal/failure_gallery.md` | PRESENT | 13802 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-088-thinking-openai-gpt-5-nano-low/summary.csv` | PRESENT | 1222 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-088-thinking-openai-gpt-5-nano-low/usage_by_family.csv` | PRESENT | 2577 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-088-thinking-openai-gpt-5-nano-low/usage_by_section.csv` | PRESENT | 4349 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-088-thinking-openai-gpt-5-nano-low/usage_by_question.csv` | PRESENT | 30982 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-088-thinking-openai-gpt-5-nano-low/usage_by_sample.csv` | PRESENT | 33320 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-088-thinking-openai-gpt-5-nano-low/failure_gallery.md` | PRESENT | 2501 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-089-thinking-gemini-gemini-2-5-flash-lite-low/summary.csv` | PRESENT | 1295 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-089-thinking-gemini-gemini-2-5-flash-lite-low/usage_by_family.csv` | PRESENT | 3014 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-089-thinking-gemini-gemini-2-5-flash-lite-low/usage_by_section.csv` | PRESENT | 5209 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-089-thinking-gemini-gemini-2-5-flash-lite-low/usage_by_question.csv` | PRESENT | 35651 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-089-thinking-gemini-gemini-2-5-flash-lite-low/usage_by_sample.csv` | PRESENT | 37893 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-089-thinking-gemini-gemini-2-5-flash-lite-low/failure_gallery.md` | PRESENT | 12483 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-090-thinking-openai-gpt-5-nano-medium/summary.csv` | PRESENT | 1235 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-090-thinking-openai-gpt-5-nano-medium/usage_by_family.csv` | PRESENT | 2642 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-090-thinking-openai-gpt-5-nano-medium/usage_by_section.csv` | PRESENT | 4453 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-090-thinking-openai-gpt-5-nano-medium/usage_by_question.csv` | PRESENT | 32014 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-090-thinking-openai-gpt-5-nano-medium/usage_by_sample.csv` | PRESENT | 34166 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-090-thinking-openai-gpt-5-nano-medium/failure_gallery.md` | PRESENT | 1881 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-091-thinking-openrouter-deepseek-deepseek-r1-distill-qwen-32b-low/summary.csv` | PRESENT | 1415 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-091-thinking-openrouter-deepseek-deepseek-r1-distill-qwen-32b-low/usage_by_family.csv` | PRESENT | 3401 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-091-thinking-openrouter-deepseek-deepseek-r1-distill-qwen-32b-low/usage_by_section.csv` | PRESENT | 5846 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-091-thinking-openrouter-deepseek-deepseek-r1-distill-qwen-32b-low/usage_by_question.csv` | PRESENT | 34520 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-091-thinking-openrouter-deepseek-deepseek-r1-distill-qwen-32b-low/usage_by_sample.csv` | PRESENT | 36871 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-091-thinking-openrouter-deepseek-deepseek-r1-distill-qwen-32b-low/failure_gallery.md` | PRESENT | 30578 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-092-thinking-openai-gpt-5-mini-minimal/summary.csv` | PRESENT | 1214 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-092-thinking-openai-gpt-5-mini-minimal/usage_by_family.csv` | PRESENT | 2364 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-092-thinking-openai-gpt-5-mini-minimal/usage_by_section.csv` | PRESENT | 3958 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-092-thinking-openai-gpt-5-mini-minimal/usage_by_question.csv` | PRESENT | 29333 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-092-thinking-openai-gpt-5-mini-minimal/usage_by_sample.csv` | PRESENT | 33380 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-092-thinking-openai-gpt-5-mini-minimal/failure_gallery.md` | PRESENT | 9045 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/summary.csv` | PRESENT | 1155 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/usage_by_family.csv` | PRESENT | 2205 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/usage_by_section.csv` | PRESENT | 3773 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/usage_by_question.csv` | PRESENT | 29218 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/usage_by_sample.csv` | PRESENT | 33402 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-093-thinking-gemini-gemini-3-1-flash-lite-minimal/failure_gallery.md` | PRESENT | 10305 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/summary.csv` | PRESENT | 1248 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_family.csv` | PRESENT | 2660 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_section.csv` | PRESENT | 4581 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_question.csv` | PRESENT | 32738 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_sample.csv` | PRESENT | 36809 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-094-thinking-openrouter-google-gemini-3-1-flash-lite-minimal/failure_gallery.md` | PRESENT | 10701 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/summary.csv` | PRESENT | 1260 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/usage_by_family.csv` | PRESENT | 2789 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/usage_by_section.csv` | PRESENT | 4807 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/usage_by_question.csv` | PRESENT | 33997 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/usage_by_sample.csv` | PRESENT | 38074 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-095-thinking-openrouter-google-gemini-3-1-flash-lite-preview-minimal/failure_gallery.md` | PRESENT | 10989 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/summary.csv` | PRESENT | 1310 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/usage_by_family.csv` | PRESENT | 3213 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/usage_by_section.csv` | PRESENT | 5486 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/usage_by_question.csv` | PRESENT | 37703 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/usage_by_sample.csv` | PRESENT | 38555 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-096-thinking-openrouter-qwen-qwen3-6-35b-a3b-low/failure_gallery.md` | PRESENT | 2625 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-097-thinking-gemini-gemini-2-5-flash-lite-medium/summary.csv` | PRESENT | 1292 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-097-thinking-gemini-gemini-2-5-flash-lite-medium/usage_by_family.csv` | PRESENT | 3034 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-097-thinking-gemini-gemini-2-5-flash-lite-medium/usage_by_section.csv` | PRESENT | 5241 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-097-thinking-gemini-gemini-2-5-flash-lite-medium/usage_by_question.csv` | PRESENT | 35753 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-097-thinking-gemini-gemini-2-5-flash-lite-medium/usage_by_sample.csv` | PRESENT | 37946 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-097-thinking-gemini-gemini-2-5-flash-lite-medium/failure_gallery.md` | PRESENT | 14140 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-098-thinking-openrouter-qwen-qwen3-6-flash-low/summary.csv` | PRESENT | 1303 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-098-thinking-openrouter-qwen-qwen3-6-flash-low/usage_by_family.csv` | PRESENT | 3157 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-098-thinking-openrouter-qwen-qwen3-6-flash-low/usage_by_section.csv` | PRESENT | 5470 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-098-thinking-openrouter-qwen-qwen3-6-flash-low/usage_by_question.csv` | PRESENT | 37455 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-098-thinking-openrouter-qwen-qwen3-6-flash-low/usage_by_sample.csv` | PRESENT | 38226 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-098-thinking-openrouter-qwen-qwen3-6-flash-low/failure_gallery.md` | PRESENT | 898 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-099-thinking-openai-gpt-5-4-nano-low/summary.csv` | PRESENT | 1232 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-099-thinking-openai-gpt-5-4-nano-low/usage_by_family.csv` | PRESENT | 2443 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-099-thinking-openai-gpt-5-4-nano-low/usage_by_section.csv` | PRESENT | 4028 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-099-thinking-openai-gpt-5-4-nano-low/usage_by_question.csv` | PRESENT | 29908 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-099-thinking-openai-gpt-5-4-nano-low/usage_by_sample.csv` | PRESENT | 33085 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-099-thinking-openai-gpt-5-4-nano-low/failure_gallery.md` | PRESENT | 9413 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-100-thinking-openrouter-openai-gpt-5-4-nano-low/summary.csv` | PRESENT | 1302 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-100-thinking-openrouter-openai-gpt-5-4-nano-low/usage_by_family.csv` | PRESENT | 2858 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-100-thinking-openrouter-openai-gpt-5-4-nano-low/usage_by_section.csv` | PRESENT | 4595 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-100-thinking-openrouter-openai-gpt-5-4-nano-low/usage_by_question.csv` | PRESENT | 32611 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-100-thinking-openrouter-openai-gpt-5-4-nano-low/usage_by_sample.csv` | PRESENT | 35760 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/next-100-thinking-openrouter-openai-gpt-5-4-nano-low/failure_gallery.md` | PRESENT | 7834 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-001-openai-gpt-5-5-none/summary.csv` | PRESENT | 1197 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-001-openai-gpt-5-5-none/usage_by_family.csv` | PRESENT | 2232 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-001-openai-gpt-5-5-none/usage_by_section.csv` | PRESENT | 3762 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-001-openai-gpt-5-5-none/usage_by_question.csv` | PRESENT | 28450 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-001-openai-gpt-5-5-none/usage_by_sample.csv` | PRESENT | 32206 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-001-openai-gpt-5-5-none/failure_gallery.md` | PRESENT | 5566 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-002-openai-gpt-5-5-low/summary.csv` | PRESENT | 1175 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-002-openai-gpt-5-5-low/usage_by_family.csv` | PRESENT | 2449 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-002-openai-gpt-5-5-low/usage_by_section.csv` | PRESENT | 4239 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-002-openai-gpt-5-5-low/usage_by_question.csv` | PRESENT | 30345 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-002-openai-gpt-5-5-low/usage_by_sample.csv` | PRESENT | 32046 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-002-openai-gpt-5-5-low/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-003-openai-gpt-5-5-medium/summary.csv` | PRESENT | 1179 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-003-openai-gpt-5-5-medium/usage_by_family.csv` | PRESENT | 2484 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-003-openai-gpt-5-5-medium/usage_by_section.csv` | PRESENT | 4196 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-003-openai-gpt-5-5-medium/usage_by_question.csv` | PRESENT | 30635 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-003-openai-gpt-5-5-medium/usage_by_sample.csv` | PRESENT | 32556 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-003-openai-gpt-5-5-medium/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-004-openai-gpt-5-5-high/summary.csv` | PRESENT | 1179 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-004-openai-gpt-5-5-high/usage_by_family.csv` | PRESENT | 2478 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-004-openai-gpt-5-5-high/usage_by_section.csv` | PRESENT | 4199 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-004-openai-gpt-5-5-high/usage_by_question.csv` | PRESENT | 30645 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-004-openai-gpt-5-5-high/usage_by_sample.csv` | PRESENT | 32231 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-004-openai-gpt-5-5-high/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-005-openai-gpt-5-5-xhigh/summary.csv` | PRESENT | 1191 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-005-openai-gpt-5-5-xhigh/usage_by_family.csv` | PRESENT | 2515 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-005-openai-gpt-5-5-xhigh/usage_by_section.csv` | PRESENT | 4248 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-005-openai-gpt-5-5-xhigh/usage_by_question.csv` | PRESENT | 30758 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-005-openai-gpt-5-5-xhigh/usage_by_sample.csv` | PRESENT | 32423 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-005-openai-gpt-5-5-xhigh/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-006-openai-gpt-5-4-none/summary.csv` | PRESENT | 1202 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-006-openai-gpt-5-4-none/usage_by_family.csv` | PRESENT | 2218 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-006-openai-gpt-5-4-none/usage_by_section.csv` | PRESENT | 3791 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-006-openai-gpt-5-4-none/usage_by_question.csv` | PRESENT | 28483 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-006-openai-gpt-5-4-none/usage_by_sample.csv` | PRESENT | 32339 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-006-openai-gpt-5-4-none/failure_gallery.md` | PRESENT | 8784 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-007-openai-gpt-5-4-low/summary.csv` | PRESENT | 1220 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-007-openai-gpt-5-4-low/usage_by_family.csv` | PRESENT | 2461 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-007-openai-gpt-5-4-low/usage_by_section.csv` | PRESENT | 4250 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-007-openai-gpt-5-4-low/usage_by_question.csv` | PRESENT | 30093 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-007-openai-gpt-5-4-low/usage_by_sample.csv` | PRESENT | 32132 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-007-openai-gpt-5-4-low/failure_gallery.md` | PRESENT | 2437 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-008-openai-gpt-5-4-medium/summary.csv` | PRESENT | 1226 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-008-openai-gpt-5-4-medium/usage_by_family.csv` | PRESENT | 2471 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-008-openai-gpt-5-4-medium/usage_by_section.csv` | PRESENT | 4296 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-008-openai-gpt-5-4-medium/usage_by_question.csv` | PRESENT | 30790 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-008-openai-gpt-5-4-medium/usage_by_sample.csv` | PRESENT | 32656 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-008-openai-gpt-5-4-medium/failure_gallery.md` | PRESENT | 1667 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-009-openai-gpt-5-4-high/summary.csv` | PRESENT | 1219 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-009-openai-gpt-5-4-high/usage_by_family.csv` | PRESENT | 2497 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-009-openai-gpt-5-4-high/usage_by_section.csv` | PRESENT | 4273 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-009-openai-gpt-5-4-high/usage_by_question.csv` | PRESENT | 30782 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-009-openai-gpt-5-4-high/usage_by_sample.csv` | PRESENT | 32352 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-009-openai-gpt-5-4-high/failure_gallery.md` | PRESENT | 1667 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-010-openai-gpt-5-4-xhigh/summary.csv` | PRESENT | 1221 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-010-openai-gpt-5-4-xhigh/usage_by_family.csv` | PRESENT | 2540 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-010-openai-gpt-5-4-xhigh/usage_by_section.csv` | PRESENT | 4275 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-010-openai-gpt-5-4-xhigh/usage_by_question.csv` | PRESENT | 31028 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-010-openai-gpt-5-4-xhigh/usage_by_sample.csv` | PRESENT | 32532 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-010-openai-gpt-5-4-xhigh/failure_gallery.md` | PRESENT | 845 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-011-anthropic-claude-opus-4-8-low/summary.csv` | PRESENT | 1202 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-011-anthropic-claude-opus-4-8-low/usage_by_family.csv` | PRESENT | 2351 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-011-anthropic-claude-opus-4-8-low/usage_by_section.csv` | PRESENT | 4018 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-011-anthropic-claude-opus-4-8-low/usage_by_question.csv` | PRESENT | 29947 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-011-anthropic-claude-opus-4-8-low/usage_by_sample.csv` | PRESENT | 33354 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-011-anthropic-claude-opus-4-8-low/failure_gallery.md` | PRESENT | 5046 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-012-anthropic-claude-opus-4-8-medium/summary.csv` | PRESENT | 1202 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-012-anthropic-claude-opus-4-8-medium/usage_by_family.csv` | PRESENT | 2351 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-012-anthropic-claude-opus-4-8-medium/usage_by_section.csv` | PRESENT | 4018 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-012-anthropic-claude-opus-4-8-medium/usage_by_question.csv` | PRESENT | 29967 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-012-anthropic-claude-opus-4-8-medium/usage_by_sample.csv` | PRESENT | 33360 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-012-anthropic-claude-opus-4-8-medium/failure_gallery.md` | PRESENT | 5046 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-013-anthropic-claude-opus-4-8-high/summary.csv` | PRESENT | 1204 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-013-anthropic-claude-opus-4-8-high/usage_by_family.csv` | PRESENT | 2363 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-013-anthropic-claude-opus-4-8-high/usage_by_section.csv` | PRESENT | 4018 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-013-anthropic-claude-opus-4-8-high/usage_by_question.csv` | PRESENT | 29931 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-013-anthropic-claude-opus-4-8-high/usage_by_sample.csv` | PRESENT | 33347 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-013-anthropic-claude-opus-4-8-high/failure_gallery.md` | PRESENT | 5046 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-014-anthropic-claude-opus-4-8-xhigh/summary.csv` | PRESENT | 1204 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-014-anthropic-claude-opus-4-8-xhigh/usage_by_family.csv` | PRESENT | 2336 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-014-anthropic-claude-opus-4-8-xhigh/usage_by_section.csv` | PRESENT | 4017 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-014-anthropic-claude-opus-4-8-xhigh/usage_by_question.csv` | PRESENT | 29934 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-014-anthropic-claude-opus-4-8-xhigh/usage_by_sample.csv` | PRESENT | 33350 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-014-anthropic-claude-opus-4-8-xhigh/failure_gallery.md` | PRESENT | 5330 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-015-anthropic-claude-opus-4-8-max/summary.csv` | PRESENT | 1212 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-015-anthropic-claude-opus-4-8-max/usage_by_family.csv` | PRESENT | 2373 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-015-anthropic-claude-opus-4-8-max/usage_by_section.csv` | PRESENT | 4074 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-015-anthropic-claude-opus-4-8-max/usage_by_question.csv` | PRESENT | 29954 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-015-anthropic-claude-opus-4-8-max/usage_by_sample.csv` | PRESENT | 33452 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-015-anthropic-claude-opus-4-8-max/failure_gallery.md` | PRESENT | 10203 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-016-anthropic-claude-sonnet-4-6-low/summary.csv` | PRESENT | 1216 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-016-anthropic-claude-sonnet-4-6-low/usage_by_family.csv` | PRESENT | 2424 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-016-anthropic-claude-sonnet-4-6-low/usage_by_section.csv` | PRESENT | 4132 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-016-anthropic-claude-sonnet-4-6-low/usage_by_question.csv` | PRESENT | 30255 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-016-anthropic-claude-sonnet-4-6-low/usage_by_sample.csv` | PRESENT | 33682 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-016-anthropic-claude-sonnet-4-6-low/failure_gallery.md` | PRESENT | 7493 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-017-anthropic-claude-sonnet-4-6-medium/summary.csv` | PRESENT | 1198 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-017-anthropic-claude-sonnet-4-6-medium/usage_by_family.csv` | PRESENT | 2437 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-017-anthropic-claude-sonnet-4-6-medium/usage_by_section.csv` | PRESENT | 4113 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-017-anthropic-claude-sonnet-4-6-medium/usage_by_question.csv` | PRESENT | 30247 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-017-anthropic-claude-sonnet-4-6-medium/usage_by_sample.csv` | PRESENT | 33708 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-017-anthropic-claude-sonnet-4-6-medium/failure_gallery.md` | PRESENT | 8466 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-018-anthropic-claude-sonnet-4-6-high/summary.csv` | PRESENT | 1207 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-018-anthropic-claude-sonnet-4-6-high/usage_by_family.csv` | PRESENT | 2383 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-018-anthropic-claude-sonnet-4-6-high/usage_by_section.csv` | PRESENT | 4122 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-018-anthropic-claude-sonnet-4-6-high/usage_by_question.csv` | PRESENT | 30268 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-018-anthropic-claude-sonnet-4-6-high/usage_by_sample.csv` | PRESENT | 33785 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-018-anthropic-claude-sonnet-4-6-high/failure_gallery.md` | PRESENT | 12632 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-019-anthropic-claude-sonnet-4-6-max/summary.csv` | PRESENT | 1212 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-019-anthropic-claude-sonnet-4-6-max/usage_by_family.csv` | PRESENT | 2397 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-019-anthropic-claude-sonnet-4-6-max/usage_by_section.csv` | PRESENT | 4138 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-019-anthropic-claude-sonnet-4-6-max/usage_by_question.csv` | PRESENT | 30254 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-019-anthropic-claude-sonnet-4-6-max/usage_by_sample.csv` | PRESENT | 33989 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-019-anthropic-claude-sonnet-4-6-max/failure_gallery.md` | PRESENT | 22540 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/summary.csv` | PRESENT | 1234 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/usage_by_family.csv` | PRESENT | 2606 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/usage_by_section.csv` | PRESENT | 4386 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/usage_by_question.csv` | PRESENT | 31947 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/usage_by_sample.csv` | PRESENT | 35940 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-028-openrouter-google-gemini-3-5-flash-minimal/failure_gallery.md` | PRESENT | 6818 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-029-openrouter-google-gemini-3-5-flash-low/summary.csv` | PRESENT | 1214 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-029-openrouter-google-gemini-3-5-flash-low/usage_by_family.csv` | PRESENT | 2825 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-029-openrouter-google-gemini-3-5-flash-low/usage_by_section.csv` | PRESENT | 4870 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-029-openrouter-google-gemini-3-5-flash-low/usage_by_question.csv` | PRESENT | 34213 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-029-openrouter-google-gemini-3-5-flash-low/usage_by_sample.csv` | PRESENT | 35499 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-029-openrouter-google-gemini-3-5-flash-low/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-030-openrouter-google-gemini-3-5-flash-medium/summary.csv` | PRESENT | 1272 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-030-openrouter-google-gemini-3-5-flash-medium/usage_by_family.csv` | PRESENT | 2851 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-030-openrouter-google-gemini-3-5-flash-medium/usage_by_section.csv` | PRESENT | 4930 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-030-openrouter-google-gemini-3-5-flash-medium/usage_by_question.csv` | PRESENT | 34608 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-030-openrouter-google-gemini-3-5-flash-medium/usage_by_sample.csv` | PRESENT | 36039 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-030-openrouter-google-gemini-3-5-flash-medium/failure_gallery.md` | PRESENT | 863 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-031-openrouter-google-gemini-3-5-flash-high/summary.csv` | PRESENT | 1220 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-031-openrouter-google-gemini-3-5-flash-high/usage_by_family.csv` | PRESENT | 2848 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-031-openrouter-google-gemini-3-5-flash-high/usage_by_section.csv` | PRESENT | 4896 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-031-openrouter-google-gemini-3-5-flash-high/usage_by_question.csv` | PRESENT | 34434 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-031-openrouter-google-gemini-3-5-flash-high/usage_by_sample.csv` | PRESENT | 35699 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-031-openrouter-google-gemini-3-5-flash-high/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/summary.csv` | PRESENT | 1276 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/usage_by_family.csv` | PRESENT | 3112 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/usage_by_section.csv` | PRESENT | 5379 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/usage_by_question.csv` | PRESENT | 37083 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/usage_by_sample.csv` | PRESENT | 38422 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-032-openrouter-google-gemini-3-1-pro-preview-customtools-low/failure_gallery.md` | PRESENT | 2923 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/summary.csv` | PRESENT | 1260 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/usage_by_family.csv` | PRESENT | 3118 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/usage_by_section.csv` | PRESENT | 5379 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/usage_by_question.csv` | PRESENT | 37208 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/usage_by_sample.csv` | PRESENT | 38529 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-033-openrouter-google-gemini-3-1-pro-preview-customtools-high/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/summary.csv` | PRESENT | 1246 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_family.csv` | PRESENT | 2667 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_section.csv` | PRESENT | 4592 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_question.csv` | PRESENT | 32691 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/usage_by_sample.csv` | PRESENT | 36785 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-034-openrouter-google-gemini-3-1-flash-lite-minimal/failure_gallery.md` | PRESENT | 10701 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/summary.csv` | PRESENT | 1280 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/usage_by_family.csv` | PRESENT | 2921 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/usage_by_section.csv` | PRESENT | 5000 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/usage_by_question.csv` | PRESENT | 35113 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/usage_by_sample.csv` | PRESENT | 36448 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-035-openrouter-google-gemini-3-1-flash-lite-low/failure_gallery.md` | PRESENT | 2568 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/summary.csv` | PRESENT | 1242 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/usage_by_family.csv` | PRESENT | 2934 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/usage_by_section.csv` | PRESENT | 5066 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/usage_by_question.csv` | PRESENT | 35363 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/usage_by_sample.csv` | PRESENT | 36832 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-036-openrouter-google-gemini-3-1-flash-lite-medium/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/summary.csv` | PRESENT | 1237 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/usage_by_family.csv` | PRESENT | 2961 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/usage_by_section.csv` | PRESENT | 5058 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/usage_by_question.csv` | PRESENT | 35310 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/usage_by_sample.csv` | PRESENT | 36549 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/top-thinking-037-openrouter-google-gemini-3-1-flash-lite-high/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-002-openai-gpt-5-4-nano-medium/summary.csv` | PRESENT | 1241 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-002-openai-gpt-5-4-nano-medium/usage_by_family.csv` | PRESENT | 2523 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-002-openai-gpt-5-4-nano-medium/usage_by_section.csv` | PRESENT | 4181 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-002-openai-gpt-5-4-nano-medium/usage_by_question.csv` | PRESENT | 30582 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-002-openai-gpt-5-4-nano-medium/usage_by_sample.csv` | PRESENT | 33424 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-002-openai-gpt-5-4-nano-medium/failure_gallery.md` | PRESENT | 2608 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-003-openai-gpt-5-4-nano-high/summary.csv` | PRESENT | 1187 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-003-openai-gpt-5-4-nano-high/usage_by_family.csv` | PRESENT | 2485 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-003-openai-gpt-5-4-nano-high/usage_by_section.csv` | PRESENT | 4140 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-003-openai-gpt-5-4-nano-high/usage_by_question.csv` | PRESENT | 30614 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-003-openai-gpt-5-4-nano-high/usage_by_sample.csv` | PRESENT | 33073 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-003-openai-gpt-5-4-nano-high/failure_gallery.md` | PRESENT | 31 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-004-openai-gpt-5-4-mini-medium/summary.csv` | PRESENT | 1238 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-004-openai-gpt-5-4-mini-medium/usage_by_family.csv` | PRESENT | 2577 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-004-openai-gpt-5-4-mini-medium/usage_by_section.csv` | PRESENT | 4457 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-004-openai-gpt-5-4-mini-medium/usage_by_question.csv` | PRESENT | 31842 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-004-openai-gpt-5-4-mini-medium/usage_by_sample.csv` | PRESENT | 33552 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-004-openai-gpt-5-4-mini-medium/failure_gallery.md` | PRESENT | 1701 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-005-openai-gpt-5-4-mini-high/summary.csv` | PRESENT | 1237 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-005-openai-gpt-5-4-mini-high/usage_by_family.csv` | PRESENT | 2608 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-005-openai-gpt-5-4-mini-high/usage_by_section.csv` | PRESENT | 4430 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-005-openai-gpt-5-4-mini-high/usage_by_question.csv` | PRESENT | 31917 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-005-openai-gpt-5-4-mini-high/usage_by_sample.csv` | PRESENT | 33297 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-005-openai-gpt-5-4-mini-high/failure_gallery.md` | PRESENT | 2484 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-006-openai-gpt-5-4-nano-xhigh/summary.csv` | PRESENT | 1238 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-006-openai-gpt-5-4-nano-xhigh/usage_by_family.csv` | PRESENT | 2615 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-006-openai-gpt-5-4-nano-xhigh/usage_by_section.csv` | PRESENT | 4389 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-006-openai-gpt-5-4-nano-xhigh/usage_by_question.csv` | PRESENT | 31332 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-006-openai-gpt-5-4-nano-xhigh/usage_by_sample.csv` | PRESENT | 33361 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-006-openai-gpt-5-4-nano-xhigh/failure_gallery.md` | PRESENT | 1736 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-007-openai-gpt-5-4-mini-xhigh/summary.csv` | PRESENT | 1236 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-007-openai-gpt-5-4-mini-xhigh/usage_by_family.csv` | PRESENT | 2595 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-007-openai-gpt-5-4-mini-xhigh/usage_by_section.csv` | PRESENT | 4465 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-007-openai-gpt-5-4-mini-xhigh/usage_by_question.csv` | PRESENT | 31961 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-007-openai-gpt-5-4-mini-xhigh/usage_by_sample.csv` | PRESENT | 33489 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/runs/overline-007-openai-gpt-5-4-mini-xhigh/failure_gallery.md` | PRESENT | 3264 bytes |

## Comparison Artifacts

| Path | Status | Evidence |
| --- | --- | --- |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison/comparison.csv` | PRESENT | 234 row(s), 113829 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison/family_comparison.csv` | PRESENT | 1866 row(s), 665925 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison/section_comparison.csv` | PRESENT | 3227 row(s), 1188513 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison/effort_curve.csv` | PRESENT | 234 row(s), 26263 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison/metamorphic_consistency.csv` | PRESENT | 230 row(s), 59614 bytes |
| `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison/delta.csv` | PRESENT | 0 row(s), 689 bytes |

## Report Artifacts

| Path | Status | Evidence |
| --- | --- | --- |
| `docs/reports/2026-06-02-paper-v1-combined-234-overline/report.html` | PRESENT | 528729 bytes |
| `docs/reports/2026-06-02-paper-v1-combined-234-overline/leaderboard.csv` | PRESENT | 92609 bytes |
| `docs/reports/2026-06-02-paper-v1-combined-234-overline/leaderboard.md` | PRESENT | 34876 bytes |
| `docs/reports/2026-06-02-paper-v1-combined-234-overline/family-heatmap.csv` | PRESENT | 129965 bytes |

## Promotion Rule

Paper result prose may cite this evidence run only when this audit passes, paper tables and figures are regenerated from the same comparison directory, and `make -C paper internal-review` no longer reports result or analysis placeholder blockers.
