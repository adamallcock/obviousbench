#!/usr/bin/env node

import { mkdir, writeFile } from "node:fs/promises";
import {
  priceCardsFromOpenRouterModels,
  resolvePriceCatalog,
} from "runcost";

const OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models";
const OUTPUT_PATH = argumentValue("--output", "configs/registries/model_registry_v1.yaml");
const TARGET_OPENROUTER_ENTRIES = 185;
const OPENROUTER_REQUESTED_EXPANSION_SOURCE = "openrouter_requested_expansion_2026_07_21";
const REQUESTED_OPENROUTER_EXPANSION_MODEL_IDS = [
  "kwaipilot/kat-coder-air-v2.5",
  "kwaipilot/kat-coder-pro-v2.5",
  "sakana/fugu-ultra",
  "inclusionai/ling-2.6-1t",
  "inclusionai/ring-2.6-1t",
  "bytedance-seed/seed-1.6",
  "bytedance-seed/seed-1.6-flash",
  "bytedance-seed/seed-2.0-mini",
  "bytedance-seed/seed-2.0-lite",
  "deepcogito/cogito-v2.1-671b",
  "inception/mercury-2",
  "morph/morph-v3-fast",
  "morph/morph-v3-large",
  "upstage/solar-pro-3",
  "writer/palmyra-x5",
  "poolside/laguna-m.1",
  "poolside/laguna-xs-2.1",
  "amazon/nova-premier-v1",
  "ai21/jamba-large-1.7",
  "arcee-ai/trinity-large-thinking",
  "arcee-ai/virtuoso-large",
  "baidu/ernie-4.5-vl-424b-a47b",
  "bytedance/ui-tars-1.5-7b",
  "ibm-granite/granite-4.0-h-micro",
  "ibm-granite/granite-4.1-8b",
  "inclusionai/ling-2.6-flash",
  "inflection/inflection-3-productivity",
  "inflection/inflection-3-pi",
  "microsoft/phi-4",
  "microsoft/wizardlm-2-8x22b",
  "nex-agi/nex-n2-mini",
  "nex-agi/nex-n2-pro",
  "nousresearch/hermes-3-llama-3.1-405b",
  "nousresearch/hermes-3-llama-3.1-70b",
  "nousresearch/hermes-4-405b",
  "nousresearch/hermes-4-70b",
  "rekaai/reka-edge",
  "rekaai/reka-flash-3",
  "stepfun/step-3.5-flash",
  "stepfun/step-3.7-flash",
  "tencent/hunyuan-a13b-instruct",
  "xiaomi/mimo-v2.5",
  "xiaomi/mimo-v2.5-pro",
];
const REQUESTED_OPENROUTER_EXPANSION_MODEL_ID_SET = new Set(
  REQUESTED_OPENROUTER_EXPANSION_MODEL_IDS,
);
const REQUESTED_OPENROUTER_DEFAULT_THINKING_DEPTHS = {
  "sakana/fugu-ultra": "xhigh",
  "inclusionai/ring-2.6-1t": "high",
  "bytedance-seed/seed-2.0-mini": "medium",
  "bytedance-seed/seed-2.0-lite": "medium",
  "inception/mercury-2": "medium",
  "stepfun/step-3.7-flash": "medium",
};
const EXCLUDED_OPENROUTER_REQUESTED_EXPANSION_MODEL_ID_SET = new Set([
  "poolside/laguna-xs.2",
]);

// OpenRouter's catalog metadata is useful for discovery, but weight availability
// is a model-family property. These frozen corrections use the manufacturers'
// published checkpoints rather than inferring availability from the transport.
const WEIGHT_STATUS_OVERRIDES = {
  "aion-labs/aion-rp-llama-3.1-8b": {
    openWeight: true,
    sourceRefs: ["https://huggingface.co/aion-labs/Aion-RP-Llama-3.1-8B"],
  },
  "deepcogito/cogito-v2.1-671b": {
    openWeight: true,
    sourceRefs: ["https://huggingface.co/blog/deepcogito/cogito-v2-1"],
  },
  "inclusionai/ling-2.6-1t": {
    openWeight: true,
    sourceRefs: ["https://huggingface.co/inclusionAI/Ling-2.6-1T"],
  },
  "inclusionai/ling-2.6-flash": {
    openWeight: true,
    sourceRefs: ["https://huggingface.co/inclusionAI/Ling-2.6-flash"],
  },
  "inclusionai/ring-2.6-1t": {
    openWeight: true,
    sourceRefs: ["https://huggingface.co/inclusionAI/Ring-2.6-1T"],
  },
  "meituan/longcat-2.0": {
    openWeight: true,
    sourceRefs: ["https://huggingface.co/meituan-longcat/LongCat-2.0"],
  },
  "moonshotai/kimi-k3": {
    // Moonshot announced future release of the checkpoint, but its actual
    // weights are not yet available in the reviewed release window.
    openWeight: false,
    sourceRefs: ["https://platform.kimi.ai/docs/guide/kimi-k3-quickstart"],
  },
};
const LONGCAT_2_0_WEIGHTS_SOURCE = "https://huggingface.co/meituan-longcat/LongCat-2.0";
const AION_RP_WEIGHTS_SOURCE = "https://huggingface.co/aion-labs/Aion-RP-Llama-3.1-8B";
const GLM_5_2_WEIGHTS_SOURCE = "https://huggingface.co/zai-org/GLM-5.2";
// These two provider-default routes demonstrably exhaust the benchmark's
// synthetic 10k safeguard before completing. Preserve their advertised output
// capability as metadata, but omit max_tokens from the wire contract so
// OpenRouter/the selected provider applies its native default instead.
const UNCAPPED_OPENROUTER_PROVIDER_DEFAULT_MODEL_ID_SET = new Set([
  "nousresearch/hermes-3-llama-3.1-70b",
  "rekaai/reka-flash-3",
]);
const DEFAULT_PROFILE = "hard_obvious_8x10";
const DEFAULT_SEED = 20260531;
const OUTPUT_SAFETY_MAX_TOKENS = 10000;
const DEFAULT_GENERATION_SETTINGS = {
  temperature: 0,
  max_tokens: OUTPUT_SAFETY_MAX_TOKENS,
};
const DIRECT_PRICE_OVERRIDES_USD_PER_MTOK = {
  "openai:gpt-5.6-sol": {
    source: "openai_standard_short_context_2026_07_09",
    input: 5.0,
    output: 30.0,
  },
  "openai:gpt-5.6-terra": {
    source: "openai_standard_short_context_2026_07_09",
    input: 2.5,
    output: 15.0,
  },
  "openai:gpt-5.6-luna": {
    source: "openai_standard_short_context_2026_07_09",
    input: 1.0,
    output: 6.0,
  },
  "grok:grok-4.5": {
    source: "xai_grok_4_5_docs_2026_07_08",
    input: 2.0,
    output: 6.0,
  },
};
const VERTEX_GEMINI_SOURCES = [
  "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/",
  "https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash",
  "https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite",
  "https://ai.google.dev/gemini-api/docs/thinking",
  "https://ai.google.dev/gemini-api/docs/flex-inference",
];
const GEMINI_FLEX_SOURCES = [
  "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/",
  "https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash",
  "https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite",
  "https://ai.google.dev/gemini-api/docs/generate-content/thinking",
  "https://ai.google.dev/gemini-api/docs/generate-content/flex-inference",
];
const LONGCAT_SOURCES = [
  "https://longcat.chat/platform/docs/",
];
const AION_SOURCES = [
  "https://www.aionlabs.ai/docs/api-reference/",
];
const BEDROCK_NOVA_SOURCES = [
  "https://aws.amazon.com/bedrock/pricing/",
  "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonBedrock/current/index.json",
];
const COHERE_SOURCES = [
  "https://docs.cohere.com/docs/chat-api",
  "https://docs.cohere.com/docs/reasoning",
  "https://docs.cohere.com/docs/models",
  "https://cohere.com/pricing",
];
const PERPLEXITY_SONAR_SOURCES = [
  "https://docs.perplexity.ai/docs/getting-started/pricing",
  "https://docs.perplexity.ai/docs/sonar/models/sonar",
  "https://docs.perplexity.ai/docs/sonar/models/sonar-pro",
  "https://docs.perplexity.ai/docs/sonar/models/sonar-reasoning-pro",
];
const ZAI_GLM_5_2_SOURCES = [
  "https://docs.z.ai/api-reference/llm/chat-completion",
  "https://docs.z.ai/guides/capabilities/thinking",
  "https://docs.z.ai/guides/overview/pricing",
];

const VERTEX_GEMINI_STANDARD_PRICES = {
  "gemini-3.6-flash": {
    input: 1.5,
    output: 7.5,
    source: "vertex_gemini_standard_pricing_2026_07_21",
  },
  "gemini-3.5-flash-lite": {
    input: 0.3,
    output: 2.5,
    source: "vertex_gemini_standard_pricing_2026_07_21",
  },
};
const GEMINI_API_STANDARD_PRICES = {
  "gemini-3.6-flash": {
    input: 1.5,
    cached_input: 0.15,
    output: 7.5,
    source: "gemini_api_standard_pricing_2026_07_21",
  },
  "gemini-3.5-flash-lite": {
    input: 0.3,
    cached_input: 0.03,
    output: 2.5,
    source: "gemini_api_standard_pricing_2026_07_21",
  },
};
const LONGCAT_2_0_NORMAL_PRICES = {
  input: 0.75,
  output: 2.95,
  source: "longcat_normal_pricing_2026_07_21",
};
const AION_DIRECT_PRICES = {
  "aion-labs/aion-2.0": { input: 0.8, cached_input: 0.2, output: 1.6 },
  "aion-labs/aion-2.5": { input: 1, cached_input: 0.35, output: 3 },
  "aion-labs/aion-3.0": { input: 3, cached_input: 0.75, output: 6 },
  "aion-labs/aion-3.0-mini": { input: 0.7, cached_input: 0.18, output: 1.4 },
  "aion-labs/aion-rp-llama-3.1-8b": { input: 0.8, cached_input: null, output: 1.6 },
};
const COHERE_DIRECT_PUBLIC_PRICES = {
  "command-a-03-2025": { input: 2.5, output: 10 },
  // The release ledger deliberately prices these current Cohere rows at the
  // user-supplied standard-equivalent rate even where current access is free
  // or rate-limited. This preserves comparable public cost accounting.
  "command-a-plus-05-2026": {
    input: 2.5,
    output: 10,
    source: "cohere_user_supplied_standard_equivalent_pricing_2026_07_21",
  },
  "command-a-reasoning-08-2025": {
    input: 2.5,
    output: 10,
    source: "cohere_user_supplied_standard_equivalent_pricing_2026_07_21",
  },
  "command-a-translate-08-2025": {
    input: 2.5,
    output: 10,
    source: "cohere_user_supplied_standard_equivalent_pricing_2026_07_21",
  },
  "command-a-vision-07-2025": {
    input: 2.5,
    output: 10,
    source: "cohere_user_supplied_standard_equivalent_pricing_2026_07_21",
  },
  "command-r7b-12-2024": { input: 0.0375, output: 0.15 },
  "command-r-08-2024": { input: 0.15, output: 0.6 },
  "command-r-plus-08-2024": { input: 2.5, output: 10 },
  "c4ai-aya-expanse-32b": { input: 0.5, output: 1.5 },
  // The public direct API price card explicitly lists this as a free model.
  // Retain the zero rate as a real provider condition, not as an inferred
  // price for the other unpriced Cohere catalogue entries.
  "north-mini-code-1-0": {
    input: 0,
    output: 0,
    source: "cohere_north_mini_code_public_free_pricing_2026_07_21",
  },
};
// Cohere's V2 Chat endpoint rejects a cap above a model's maximum output,
// rather than silently clipping it. These limits were verified against the
// provider in the 2026-07-21 credentialed smoke, and keep the generic
// benchmark profile from emitting its otherwise-default 10k cap.
const COHERE_MODEL_MAX_OUTPUT_TOKENS = {
  "command-a-03-2025": 8192,
  "command-r7b-12-2024": 4096,
  "command-a-translate-08-2025": 8000,
  "command-a-vision-07-2025": 8192,
  "command-r-08-2024": 4096,
  "command-r-plus-08-2024": 4096,
  "tiny-aya-global": 8192,
  "tiny-aya-earth": 8192,
  "tiny-aya-fire": 8192,
  "tiny-aya-water": 8192,
  "c4ai-aya-expanse-32b": 4096,
  "c4ai-aya-vision-32b": 4096,
  // Keep the benchmark-wide output safety ceiling even though the provider
  // accepts a larger maximum for this model.
  "north-mini-code-1-0": 10000,
};
const BEDROCK_NOVA_US_GEO_STANDARD_PRICES = {
  "us.amazon.nova-micro-v1:0": { input: 0.035, cached_input: 0.00875, output: 0.14 },
  "us.amazon.nova-lite-v1:0": { input: 0.06, cached_input: 0.015, output: 0.24 },
  "us.amazon.nova-pro-v1:0": { input: 0.8, cached_input: 0.2, output: 3.2 },
  "us.amazon.nova-2-lite-v1:0": { input: 0.33, cached_input: 0.0825, output: 2.75 },
};
const PERPLEXITY_SONAR_STANDARD_PRICES = {
  sonar: { input: 1, output: 1, request_fee_usd_per_1k: 5 },
  "sonar-pro": { input: 3, output: 15, request_fee_usd_per_1k: 6 },
  "sonar-reasoning-pro": { input: 2, output: 8, request_fee_usd_per_1k: 6 },
};
const ZAI_GLM_5_2_STANDARD_PRICES = {
  input: 1.4,
  output: 4.4,
  source: "zai_glm_5_2_standard_pricing_2026_07_21",
};

const SOURCE_PRIORITY = ["openrouter", "genai-prices", "models.dev", "litellm"];
const OPEN_WEIGHT_PATTERNS = [
  "baichuan",
  "cognitivecomputations",
  "deepseek",
  "devstral",
  "dolphin",
  "gemma",
  "glm",
  "gpt-oss",
  "hermes",
  "internlm",
  "kimi",
  "llama",
  "magistral",
  "ministral",
  "mistral",
  "mixtral",
  "moonshotai/kimi",
  "nemotron",
  "olmo",
  "openai/gpt-oss",
  "phi",
  "qwen",
  "qwq",
  "reka",
  "sarvam",
  "yi",
  "z-ai",
];
const SMALL_MODEL_PATTERNS = [
  "0.5b",
  "1.2b",
  "1.5b",
  "2b",
  "3b",
  "4b",
  "7b",
  "8b",
  "9b",
  "12b",
  "14b",
  "20b",
  "24b",
  "27b",
  "30b",
  "32b",
  "flash",
  "haiku",
  "lite",
  "micro",
  "mini",
  "nano",
  "small",
  "tiny",
  "xs",
];
const THINKING_PATTERNS = [
  "reasoning",
  "thinking",
  "r1",
  "qwq",
  "z1",
  "o1",
  "o3",
  "o4",
];
const META_MODEL_API_SOURCES = [
  "https://developer.meta.com/ai/resources/blog/build-with-muse-spark/",
  "https://dev.meta.ai/docs/getting-started/sdks",
  "https://dev.meta.ai/docs/getting-started/models",
  "https://dev.meta.ai/docs/features/reasoning",
  "https://dev.meta.ai/docs/getting-started/pricing-rate-limits",
  "https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/",
];
const META_MUSE_SPARK_1_1_PRICE = {
  input: 1.25,
  output: 4.25,
  source: "meta_model_api_blog_2026_07_09",
};
const NVIDIA_NIM_SOURCES = [
  "https://docs.api.nvidia.com/nim/reference/llm-apis",
  "https://build.nvidia.com/nvidia/nemotron-3-nano-30b-a3b",
  "https://build.nvidia.com/nvidia/nemotron-3-nano-30b-a3b/modelcard",
];
const DEEPSEEK_V4_SOURCES = [
  "https://api-docs.deepseek.com/",
  "https://api-docs.deepseek.com/quick_start/pricing",
  "https://api-docs.deepseek.com/guides/thinking_mode/",
];
const DEEPSEEK_V4_PRICES = {
  flash: {
    input: 0.14,
    output: 0.28,
    source: "deepseek_v4_pricing_2026_07_14",
  },
  pro: {
    input: 0.435,
    output: 0.87,
    source: "deepseek_v4_pricing_2026_07_14",
  },
};
const TINKER_INKLING_SOURCES = [
  "https://tinker-docs.thinkingmachines.ai/tinker/models/",
  "https://tinker-docs.thinkingmachines.ai/tinker/compatible-apis/openai/",
];
const TINKER_INKLING_UNDISCOUNTED_PRICES = {
  input: 3.74,
  output: 9.36,
  source: "tinker_inkling_undiscounted_pricing_2026_07_15",
};
const KIMI_K3_SOURCES = [
  "https://platform.kimi.ai/docs/guide/kimi-k3-quickstart",
  "https://platform.kimi.ai/docs/guide/use-thinking-effort",
  "https://platform.kimi.ai/docs/pricing/chat-k3",
];
const KIMI_K3_STANDARD_PRICES = {
  input: 3.0,
  output: 15.0,
  source: "kimi_k3_standard_pricing_2026_07_16",
};

const DIRECT_PROVIDER_ENTRIES = [
  direct("openai-gpt-5-6-sol-medium", "OpenAI GPT-5.6 Sol medium", "openai", "openai/gpt-5.6-sol", "gpt-5.6-sol", {
    reasoning_effort: "medium",
    reasoning_summary: "none",
    extra_body: { service_tier: "flex" },
  }, ["frontier", "reasoning-comparison", "flex-execution"]),
  direct("openai-gpt-5-6-terra-medium", "OpenAI GPT-5.6 Terra medium", "openai", "openai/gpt-5.6-terra", "gpt-5.6-terra", {
    reasoning_effort: "medium",
    reasoning_summary: "none",
    extra_body: { service_tier: "flex" },
  }, ["frontier", "reasoning-comparison", "flex-execution"]),
  direct("openai-gpt-5-6-luna-medium", "OpenAI GPT-5.6 Luna medium", "openai", "openai/gpt-5.6-luna", "gpt-5.6-luna", {
    reasoning_effort: "medium",
    reasoning_summary: "none",
    extra_body: { service_tier: "flex" },
  }, ["small", "reasoning-comparison", "flex-execution"]),
  direct("openai-gpt-5-5-none", "OpenAI GPT-5.5 no thinking", "openai", "openai/gpt-5.5", "gpt-5.5", {
    reasoning_effort: "none",
    reasoning_summary: "none",
  }, ["frontier", "reasoning-disabled", "prior-baseline"]),
  direct("openai-gpt-5-5-low", "OpenAI GPT-5.5 low", "openai", "openai/gpt-5.5", "gpt-5.5", {
    reasoning_effort: "low",
    reasoning_summary: "none",
  }, ["frontier", "reasoning-comparison", "prior-baseline"]),
  direct("openai-gpt-5-4-none", "OpenAI GPT-5.4 no thinking", "openai", "openai/gpt-5.4", "gpt-5.4", {
    reasoning_effort: "none",
    reasoning_summary: "none",
  }, ["frontier", "reasoning-disabled", "prior-baseline"]),
  direct("openai-gpt-5-4-mini-none", "OpenAI GPT-5.4 mini no thinking", "openai", "openai/gpt-5.4-mini", "gpt-5.4-mini", {
    reasoning_effort: "none",
    reasoning_summary: "none",
  }, ["small", "reasoning-disabled"]),
  direct("openai-gpt-5-4-nano-none", "OpenAI GPT-5.4 nano no thinking", "openai", "openai/gpt-5.4-nano", "gpt-5.4-nano", {
    reasoning_effort: "none",
    reasoning_summary: "none",
  }, ["small", "reasoning-disabled"]),
  direct("openai-gpt-5-2-none", "OpenAI GPT-5.2 no thinking", "openai", "openai/gpt-5.2", "gpt-5.2", {
    reasoning_effort: "none",
    reasoning_summary: "none",
  }, ["frontier", "reasoning-disabled", "prior-baseline"]),
  direct("openai-gpt-5-minimal", "OpenAI GPT-5 minimal", "openai", "openai/gpt-5", "gpt-5", {
    reasoning_effort: "minimal",
    reasoning_summary: "none",
  }, ["frontier", "reasoning-minimal", "prior-baseline"]),
  direct("openai-gpt-5-mini-minimal", "OpenAI GPT-5 mini minimal", "openai", "openai/gpt-5-mini", "gpt-5-mini", {
    reasoning_effort: "minimal",
    reasoning_summary: "none",
  }, ["small", "reasoning-minimal"]),
  direct("openai-gpt-5-nano-minimal", "OpenAI GPT-5 nano minimal", "openai", "openai/gpt-5-nano", "gpt-5-nano", {
    reasoning_effort: "minimal",
    reasoning_summary: "none",
  }, ["small", "cheap", "prior-baseline"]),
  direct("openai-gpt-4-1", "OpenAI GPT-4.1", "openai", "openai/gpt-4.1", "gpt-4.1", {}, ["non-thinking", "prior-baseline"]),
  direct("openai-gpt-4-1-mini", "OpenAI GPT-4.1 mini", "openai", "openai/gpt-4.1-mini", "gpt-4.1-mini", {}, ["small", "non-thinking"]),
  direct("openai-gpt-4-1-nano", "OpenAI GPT-4.1 nano", "openai", "openai/gpt-4.1-nano", "gpt-4.1-nano", {}, ["small", "non-thinking", "cheap"]),
  direct("openai-gpt-4o", "OpenAI GPT-4o", "openai", "openai/gpt-4o", "gpt-4o", {}, ["non-thinking", "prior-baseline"]),
  direct("openai-gpt-4o-mini", "OpenAI GPT-4o mini", "openai", "openai/gpt-4o-mini", "gpt-4o-mini", {}, ["small", "non-thinking", "cheap"]),
  direct("openai-gpt-oss-120b", "OpenAI GPT-OSS 120B", "openai", "openai/gpt-oss-120b", "gpt-oss-120b", {}, ["open-weight"]),
  direct("openai-gpt-oss-20b", "OpenAI GPT-OSS 20B", "openai", "openai/gpt-oss-20b", "gpt-oss-20b", {}, ["open-weight", "small"]),
  direct("anthropic-claude-opus-4-8", "Anthropic Claude Opus 4.8", "anthropic", "anthropic/claude-opus-4-8", "claude-opus-4-8", {}, ["frontier", "prior-baseline"]),
  direct("anthropic-claude-sonnet-4-6", "Anthropic Claude Sonnet 4.6", "anthropic", "anthropic/claude-sonnet-4-6", "claude-sonnet-4-6", {}, ["frontier", "prior-baseline"]),
  direct("anthropic-claude-haiku-4-5", "Anthropic Claude Haiku 4.5", "anthropic", "anthropic/claude-haiku-4-5", "claude-haiku-4-5", {}, ["small", "prior-baseline"]),
  direct("anthropic-claude-opus-4-7", "Anthropic Claude Opus 4.7", "anthropic", "anthropic/claude-opus-4-7", "claude-opus-4-7", {}, ["frontier", "prior-baseline"]),
  direct("anthropic-claude-opus-4-6", "Anthropic Claude Opus 4.6", "anthropic", "anthropic/claude-opus-4-6", "claude-opus-4-6", {}, ["frontier", "prior-baseline"]),
  direct("gemini-3-5-flash", "Gemini 3.5 Flash", "gemini", "google/gemini-3.5-flash", "gemini-3.5-flash", {}, ["small", "flash", "prior-baseline"]),
  direct("gemini-3-1-flash-lite", "Gemini 3.1 Flash-Lite", "gemini", "google/gemini-3.1-flash-lite", "gemini-3.1-flash-lite", {}, ["small", "flash-lite", "prior-baseline"]),
  direct("gemini-3-flash-preview", "Gemini 3 Flash Preview", "gemini", "google/gemini-3-flash-preview", "gemini-3-flash-preview", {}, ["small", "preview", "prior-baseline"]),
  direct("gemini-2-5-flash-lite", "Gemini 2.5 Flash-Lite", "gemini", "google/gemini-2.5-flash-lite", "gemini-2.5-flash-lite", {}, ["small", "flash-lite"]),
  direct("gemini-2-5-flash", "Gemini 2.5 Flash", "gemini", "google/gemini-2.5-flash", "gemini-2.5-flash", {}, ["small", "flash"]),
  direct("grok-4-5", "Grok 4.5", "grok", "grok/grok-4.5", "grok-4.5", {}, ["frontier"]),
  direct("grok-4-3", "Grok 4.3", "grok", "grok/grok-4.3", "grok-4.3", {}, ["frontier", "prior-baseline"]),
  direct("grok-build-0-1", "Grok Build 0.1", "grok", "grok/grok-build-0.1", "grok-build-0.1", {}, ["coding", "fast"]),
  direct("grok-4-20", "Grok 4.20", "grok", "grok/grok-4.20", "grok-4.20", {}, ["frontier", "prior-baseline"]),
  ...["minimal", "low", "medium", "high", "xhigh"].map((effort) =>
    direct(
      `meta-muse-spark-1-1-${effort}`,
      `Meta Muse Spark 1.1 ${effort}`,
      "meta",
      "meta/muse-spark-1.1",
      "muse-spark-1.1",
      { reasoning_effort: effort },
      ["frontier", "thinking", "api-preview"],
      {
        provider_api: "meta_model_api_openai_compatible",
        run_status: "api_preview_available",
        source_refs: META_MODEL_API_SOURCES,
        access_status: "public_preview",
        manual_prices: META_MUSE_SPARK_1_1_PRICE,
      },
    )
  ),
  direct(
    "nvidia-nemotron-3-nano-30b-a3b-no-thinking",
    "NVIDIA Nemotron 3 Nano 30B A3B no thinking",
    "nvidia",
    "nvidia/nemotron-3-nano-30b-a3b",
    "nvidia/nemotron-3-nano-30b-a3b",
    {
      extra_body: {
        top_k: 1,
        chat_template_kwargs: { enable_thinking: false },
      },
    },
    ["open-weight", "small", "non-thinking", "free-endpoint"],
    {
        provider_api: "nvidia_nim_openai_compatible",
        run_status: "free_endpoint_available",
        source_refs: NVIDIA_NIM_SOURCES,
        access_status: "api_key_required",
        manual_prices: {
          input: 0,
          output: 0,
          source: "nvidia_nim_free_endpoint_pricing_2026_07_21",
        },
    },
  ),
  direct(
    "deepseek-v4-flash-no-thinking",
    "DeepSeek V4 Flash no thinking",
    "deepseek",
    "deepseek/deepseek-v4-flash",
    "deepseek-v4-flash",
    { extra_body: { thinking: { type: "disabled" } } },
    ["open-weight", "small", "cheap", "non-thinking"],
    {
      provider_api: "deepseek_openai_compatible",
      run_status: "api_available",
      source_refs: DEEPSEEK_V4_SOURCES,
      access_status: "api_key_required",
      manual_prices: DEEPSEEK_V4_PRICES.flash,
    },
  ),
  direct(
    "deepseek-v4-flash-high",
    "DeepSeek V4 Flash high",
    "deepseek",
    "deepseek/deepseek-v4-flash",
    "deepseek-v4-flash",
    {
      reasoning_effort: "high",
      extra_body: { thinking: { type: "enabled" } },
    },
    ["open-weight", "small", "cheap", "thinking", "reasoning-high"],
    {
      provider_api: "deepseek_openai_compatible",
      run_status: "api_available",
      source_refs: DEEPSEEK_V4_SOURCES,
      access_status: "api_key_required",
      manual_prices: DEEPSEEK_V4_PRICES.flash,
    },
  ),
  direct(
    "deepseek-v4-pro-high",
    "DeepSeek V4 Pro high",
    "deepseek",
    "deepseek/deepseek-v4-pro",
    "deepseek-v4-pro",
    {
      reasoning_effort: "high",
      extra_body: { thinking: { type: "enabled" } },
    },
    ["open-weight", "frontier", "thinking", "reasoning-high"],
    {
      provider_api: "deepseek_openai_compatible",
      run_status: "api_available",
      source_refs: DEEPSEEK_V4_SOURCES,
      access_status: "api_key_required",
      manual_prices: DEEPSEEK_V4_PRICES.pro,
    },
  ),
  ...["none", "minimal", "low", "medium", "high", "xhigh"].map((effort) =>
    direct(
      `tinker-inkling-${effort}`,
      `Thinking Machines Inkling ${effort}`,
      "tinker",
      "tinker/thinkingmachines/Inkling",
      "thinkingmachines/Inkling",
      { reasoning_effort: effort },
      [
        "open-weight",
        "large",
        effort === "none" ? "non-thinking" : "thinking",
        `reasoning-${effort}`,
        "beta",
      ],
      {
        upstream_provider: "thinkingmachines",
        provider_api: "tinker_openai_compatible",
        run_status: "beta_testing_available",
        source_refs: TINKER_INKLING_SOURCES,
        access_status: "api_key_required",
        cached_input_price_per_mtok_usd: 0.748,
        pricing_note: "Undiscounted estimate: twice Tinker's listed limited-time 50% discounted Inkling rates; cached prefill retains the documented 80% cache discount.",
        manual_prices: TINKER_INKLING_UNDISCOUNTED_PRICES,
      },
    )
  ),
  direct(
    "kimi-k3-max",
    "Moonshot AI Kimi K3 max",
    "kimi",
    "kimi/kimi-k3",
    "kimi-k3",
    { reasoning_effort: "max" },
    ["frontier", "thinking", "always-reasoning", "reasoning-max"],
    {
      upstream_provider: "moonshotai",
      provider_api: "kimi_openai_compatible",
      run_status: "api_available",
      source_refs: KIMI_K3_SOURCES,
      access_status: "api_key_required",
      cached_input_price_per_mtok_usd: 0.3,
      pricing_note: "Public standard Kimi K3 pricing; batch discounts are excluded from benchmark pricing.",
      manual_prices: KIMI_K3_STANDARD_PRICES,
      generation_settings: {
        max_tokens: OUTPUT_SAFETY_MAX_TOKENS,
        reasoning_effort: "max",
      },
    },
  ),
  ...[
    {
      id: "vertex-gemini-3-6-flash-medium",
      label: "Vertex Gemini 3.6 Flash medium",
      modelId: "gemini-3.6-flash",
      defaultThinkingLevel: "medium",
    },
    {
      id: "vertex-gemini-3-5-flash-lite-minimal",
      label: "Vertex Gemini 3.5 Flash-Lite minimal",
      modelId: "gemini-3.5-flash-lite",
      defaultThinkingLevel: "minimal",
    },
  ].map(({ id, label, modelId, defaultThinkingLevel }) =>
    direct(
      id,
      label,
      "vertex",
      `vertex/${modelId}`,
      modelId,
      { reasoning_effort: defaultThinkingLevel },
      ["gemini", "thinking", "vertex-flex", "standard-price-accounting"],
      {
        upstream_provider: "google",
        provider_api: "vertex_gemini_generate_content",
        run_status: "blocked_billing_disabled",
        access_status: "vertex_project_billing_required",
        source_refs: VERTEX_GEMINI_SOURCES,
        control_style: "vertex_gemini_thinking_level",
        thinking_depth: defaultThinkingLevel,
        reasoning_effort_label: defaultThinkingLevel,
        thinking_default_expected: defaultThinkingLevel,
        inspect_args: ["-M", "execution_mode=flex"],
        execution_service_tier: "flex",
        public_pricing_service_tier: "standard",
        provider_preflight_status: "billing_disabled_2026_07_21",
        provider_preflight_note: "Retained as blocked evidence; benchmark execution uses the separately registered direct Gemini Flex route.",
        manual_prices: VERTEX_GEMINI_STANDARD_PRICES[modelId],
      },
    )
  ),
  ...[
    {
      id: "gemini-flex-gemini-3-6-flash-medium",
      label: "Gemini 3.6 Flash Flex medium",
      modelId: "gemini-3.6-flash",
      defaultThinkingLevel: "medium",
    },
    {
      id: "gemini-flex-gemini-3-5-flash-lite-minimal",
      label: "Gemini 3.5 Flash-Lite Flex minimal",
      modelId: "gemini-3.5-flash-lite",
      defaultThinkingLevel: "minimal",
    },
  ].map(({ id, label, modelId, defaultThinkingLevel }) =>
    direct(
      id,
      label,
      "gemini-flex",
      `gemini-flex/${modelId}`,
      modelId,
      { reasoning_effort: defaultThinkingLevel },
      ["gemini", "thinking", "flex-execution", "standard-price-accounting"],
      {
        upstream_provider: "google",
        provider_api: "gemini_generate_content_flex",
        run_status: "preflight_succeeded",
        access_status: "api_key_required",
        source_refs: GEMINI_FLEX_SOURCES,
        control_style: "gemini_flex_thinking_level",
        thinking_depth: defaultThinkingLevel,
        reasoning_effort_label: defaultThinkingLevel,
        thinking_default_expected: defaultThinkingLevel,
        execution_service_tier: "flex",
        public_pricing_service_tier: "standard",
        provider_preflight_status: "direct_flex_all_documented_levels_succeeded_2026_07_21",
        manual_prices: GEMINI_API_STANDARD_PRICES[modelId],
      },
    )
  ),
  ...["disabled", "enabled"].map((thinkingType) =>
    direct(
      `longcat-longcat-2-0-thinking-${thinkingType}`,
      `LongCat 2.0 thinking ${thinkingType}`,
      "longcat",
      "longcat/LongCat-2.0",
      "LongCat-2.0",
      { extra_body: { thinking: { type: thinkingType } } },
      ["open-weight", "thinking", `thinking-${thinkingType}`],
      {
        upstream_provider: "meituan",
        provider_api: "longcat_openai_compatible",
        run_status: "planned",
        access_status: "api_key_required",
        source_refs: LONGCAT_SOURCES,
        control_style: "longcat_thinking_type",
        thinking_depth: thinkingType === "disabled" ? "none" : "enabled",
        reasoning_effort_label: thinkingType,
        thinking_request_type: thinkingType,
        cached_input_price_per_mtok_usd: 0.015,
        weight_status: "open_weights",
        weight_status_source_refs: [LONGCAT_2_0_WEIGHTS_SOURCE],
        pricing_note: "Normal LongCat 2.0 rate card; no temporary discount is used for benchmark accounting.",
        manual_prices: LONGCAT_2_0_NORMAL_PRICES,
      },
    )
  ),
  ...["none", "low", "medium", "high"].map((effort) => {
    const price = AION_DIRECT_PRICES["aion-labs/aion-2.0"];
    return direct(
      `aion-aion-labs-aion-2-0-${effort}`,
      `AionLabs Aion 2.0 ${effort}`,
      "aion",
      "aion/aion-labs/aion-2.0",
      "aion-labs/aion-2.0",
      { reasoning_effort: effort },
      ["thinking", `reasoning-${effort}`],
      {
        upstream_provider: "aion-labs",
        provider_api: "aion_openai_compatible",
        run_status: "planned",
        access_status: "api_key_required",
        source_refs: AION_SOURCES,
        control_style: "aion_2_0_reasoning_effort",
        thinking_depth: effort,
        reasoning_effort_label: effort,
        cached_input_price_per_mtok_usd: price.cached_input,
        manual_prices: {
          input: price.input,
          output: price.output,
          source: "aionlabs_direct_pricing_2026_07_21",
        },
      },
    );
  }),
  ...[
    ["aion-labs/aion-2.5", "AionLabs Aion 2.5"],
    ["aion-labs/aion-3.0", "AionLabs Aion 3.0"],
    ["aion-labs/aion-3.0-mini", "AionLabs Aion 3.0 Mini"],
  ].map(([modelId, label]) => {
    const price = AION_DIRECT_PRICES[modelId];
    return direct(
      `aion-${slug(modelId)}-provider-default`,
      `${label} provider default`,
      "aion",
      `aion/${modelId}`,
      modelId,
      {},
      ["provider-default", "thinking-unmeasured"],
      providerDefaultMetadata({
        upstream_provider: "aion-labs",
        provider_api: "aion_openai_compatible",
        run_status: "planned",
        access_status: "api_key_required",
        source_refs: AION_SOURCES,
        cached_input_price_per_mtok_usd: price.cached_input,
        manual_prices: {
          input: price.input,
          output: price.output,
          source: "aionlabs_direct_pricing_2026_07_21",
        },
      }),
    );
  }),
  (() => {
    const modelId = "aion-labs/aion-rp-llama-3.1-8b";
    const price = AION_DIRECT_PRICES[modelId];
    return direct(
      "aion-aion-labs-aion-rp-llama-3-1-8b-provider-default",
      "AionLabs Aion RP Llama 3.1 8B provider default",
      "aion",
      `aion/${modelId}`,
      modelId,
      {},
      ["open-weight", "provider-default", "non-thinking"],
      nonThinkingDefaultMetadata({
        upstream_provider: "aion-labs",
        provider_api: "aion_openai_compatible",
        run_status: "planned",
        access_status: "api_key_required",
        source_refs: AION_SOURCES,
        cached_input_price_per_mtok_usd: price.cached_input,
        cached_input_pricing: "not_offered",
        weight_status: "open_weights",
        weight_status_source_refs: [AION_RP_WEIGHTS_SOURCE],
        manual_prices: {
          input: price.input,
          output: price.output,
          source: "aionlabs_direct_pricing_2026_07_21",
        },
      }),
    );
  })(),
  ...[
    "command-a-plus-05-2026",
    "command-a-reasoning-08-2025",
  ].flatMap((modelId) => [
    {
      id: "none",
      label: "none",
      settings: { extra_body: { thinking: { type: "disabled" } } },
      maxOutputTokens: OUTPUT_SAFETY_MAX_TOKENS,
      thinking: { type: "disabled" },
    },
    {
      id: "low_budget_512",
      label: "low_budget_512",
      settings: {
        max_tokens: 1536,
        extra_body: { thinking: { type: "enabled", token_budget: 512 } },
      },
      maxOutputTokens: 1536,
      thinking: { type: "enabled", token_budget: 512 },
    },
    {
      id: "medium_budget_2048",
      label: "medium_budget_2048",
      settings: {
        max_tokens: 3072,
        extra_body: { thinking: { type: "enabled", token_budget: 2048 } },
      },
      maxOutputTokens: 3072,
      thinking: { type: "enabled", token_budget: 2048 },
    },
    {
      id: "high_budget_8192",
      label: "high_budget_8192",
      settings: {
        max_tokens: 9216,
        extra_body: { thinking: { type: "enabled", token_budget: 8192 } },
      },
      maxOutputTokens: 9216,
      thinking: { type: "enabled", token_budget: 8192 },
    },
  ].map(({ id, label, settings, maxOutputTokens, thinking }) => {
    const price = COHERE_DIRECT_PUBLIC_PRICES[modelId];
    const metadata = {
      provider_api: "cohere_chat_v2",
      run_status: "planned",
      access_status: "api_key_required",
      source_refs: COHERE_SOURCES,
      control_style: "cohere_native_thinking_token_budget",
      thinking_depth: id,
      reasoning_effort_label: label,
      max_output_tokens: maxOutputTokens,
      provider_request_settings: { max_tokens: maxOutputTokens, thinking },
      ...(price
        ? {
            manual_prices: price,
            pricing_note:
              "User supplied the standard-equivalent $2.50/$10.00 per 1M input/output ledger rate; record it even when provider access is free or rate-limited.",
          }
        : manualPriceLookupMetadata({
            pricing_note:
              "No verified direct public rate was supplied for this current Cohere model; retain it as manual lookup required.",
          })),
    };
    return direct(
      `cohere-${slug(modelId)}-${slug(id)}`,
      `Cohere ${modelId} ${label}`,
      "cohere",
      `cohere/${modelId}`,
      modelId,
      settings,
      ["thinking", "cohere-native-thinking", id === "none" ? "reasoning-disabled" : "reasoning-enabled"],
      metadata,
    );
  })),
  ...[
    "command-a-03-2025",
    "command-r7b-12-2024",
    "command-a-translate-08-2025",
    "command-a-vision-07-2025",
    "command-r-08-2024",
    "command-r-plus-08-2024",
    "tiny-aya-global",
    "tiny-aya-earth",
    "tiny-aya-fire",
    "tiny-aya-water",
    "c4ai-aya-expanse-32b",
    "c4ai-aya-vision-32b",
    "north-mini-code-1-0",
  ].map((modelId) => {
    const confirmedPrice = COHERE_DIRECT_PUBLIC_PRICES[modelId];
    const maxOutputTokens = COHERE_MODEL_MAX_OUTPUT_TOKENS[modelId];
    if (!Number.isInteger(maxOutputTokens) || maxOutputTokens <= 0) {
      throw new Error(`Missing a verified Cohere output cap for ${modelId}`);
    }
    const priceMetadata = confirmedPrice
      ? {
        manual_prices: {
          ...confirmedPrice,
          source: confirmedPrice.source || "cohere_direct_public_pricing_2026_07_21",
        },
      }
      : manualPriceLookupMetadata({
        pricing_note: "No verified direct public rate was supplied for this current Cohere model; retain it as manual lookup required.",
      });
    const metadata = providerDefaultMetadata({
      provider_api: "cohere_chat_v2",
      run_status: "planned",
      access_status: "api_key_required",
      source_refs: COHERE_SOURCES,
      max_output_tokens: maxOutputTokens,
      provider_request_settings: { max_tokens: maxOutputTokens },
      ...priceMetadata,
    });
    if (modelId === "command-a-translate-08-2025") {
      metadata.control_style = "cohere_translate_no_sampling_parameters";
    }
    return direct(
      `cohere-${slug(modelId)}-provider-default`,
      `Cohere ${modelId} provider default`,
      "cohere",
      `cohere/${modelId}`,
      modelId,
      { max_tokens: maxOutputTokens },
      ["provider-default", "thinking-unmeasured"],
      metadata,
    );
  }),
  ...[
    ["us.amazon.nova-micro-v1:0", "Amazon Nova Micro", "bedrock-standard", "bedrock_converse_standard_direct"],
    ["us.amazon.nova-lite-v1:0", "Amazon Nova Lite", "bedrock-standard", "bedrock_converse_standard_direct"],
  ].map(([modelId, label, route, providerApi]) => {
    const price = BEDROCK_NOVA_US_GEO_STANDARD_PRICES[modelId];
    return direct(
      `bedrock-${slug(modelId)}-provider-default`,
      `${label} Standard provider default`,
      route,
      `${route}/${modelId}`,
      modelId,
      {},
      ["amazon-nova", "standard-execution", "non-thinking"],
      nonThinkingDefaultMetadata({
          upstream_provider: "amazon",
          provider_api: providerApi,
          run_status: "planned",
          access_status: "aws_credentials_or_bedrock_api_key_required",
          source_refs: BEDROCK_NOVA_SOURCES,
          execution_service_tier: "standard",
          public_pricing_service_tier: "standard",
          cached_input_price_per_mtok_usd: price.cached_input,
          manual_prices: {
            input: price.input,
            output: price.output,
            source: "bedrock_nova_us_geo_standard_pricing_2026_07_21",
          },
          pricing_note: "US Geo inference-profile standard Bedrock pricing. This direct Standard route uses the matching US Geo runtime model ID and supports Bedrock API-key bearer authentication.",
        },
      ),
    )
  }),
  direct(
    "bedrock-flex-us-amazon-nova-pro-v1-0-provider-default",
    "Amazon Nova Pro Flex provider default",
    "bedrock-flex",
    "bedrock-flex/us.amazon.nova-pro-v1:0",
    "us.amazon.nova-pro-v1:0",
    {},
    ["amazon-nova", "flex-execution", "non-thinking"],
    nonThinkingDefaultMetadata({
        upstream_provider: "amazon",
        provider_api: "bedrock_converse_flex",
        run_status: "planned",
        access_status: "aws_credentials_or_bedrock_api_key_required",
        source_refs: BEDROCK_NOVA_SOURCES,
        execution_service_tier: "flex",
        public_pricing_service_tier: "standard",
        provider_request_settings: { serviceTier: { type: "flex" } },
        cached_input_price_per_mtok_usd: BEDROCK_NOVA_US_GEO_STANDARD_PRICES["us.amazon.nova-pro-v1:0"].cached_input,
        manual_prices: {
          input: BEDROCK_NOVA_US_GEO_STANDARD_PRICES["us.amazon.nova-pro-v1:0"].input,
          output: BEDROCK_NOVA_US_GEO_STANDARD_PRICES["us.amazon.nova-pro-v1:0"].output,
          source: "bedrock_nova_us_geo_standard_pricing_2026_07_21",
        },
        pricing_note: "Flex execution is deliberately costed at US Geo standard Bedrock pricing for this runtime model ID.",
      },
    ),
  ),
  direct(
    "bedrock-flex-us-amazon-nova-premier-v1-0-provider-default",
    "Amazon Nova Premier Flex (blocked native route)",
    "bedrock-flex",
    "bedrock-flex/us.amazon.nova-premier-v1:0",
    "us.amazon.nova-premier-v1:0",
    {},
    ["amazon-nova", "flex-execution", "blocked-native-route", "use-openrouter-route"],
    nonThinkingDefaultMetadata({
      upstream_provider: "amazon",
      provider_api: "bedrock_converse_flex",
      run_status: "blocked_http_404",
      access_status: "aws_credentials_or_bedrock_api_key_required",
      source_refs: BEDROCK_NOVA_SOURCES,
      execution_service_tier: "flex",
      public_pricing_service_tier: "standard",
      provider_preflight_status: "current_bedrock_api_key_us_geo_flex_http_404_2026_07_21",
      provider_preflight_note: "The approved release route is openrouter/amazon/nova-premier-v1; retain this row only as native-route failure evidence.",
      provider_request_settings: { serviceTier: { type: "flex" } },
      pricing_note: "Not selected for execution or pricing. The approved OpenRouter Nova Premier row carries the release price.",
    }),
  ),
  direct(
    "bedrock-flex-us-amazon-nova-2-lite-v1-0-none-omitted",
    "Amazon Nova 2 Lite Flex none (omitted)",
    "bedrock-flex",
    "bedrock-flex/us.amazon.nova-2-lite-v1:0",
    "us.amazon.nova-2-lite-v1:0",
    {},
    ["amazon-nova", "flex-execution", "reasoning-disabled"],
    {
      upstream_provider: "amazon",
      provider_api: "bedrock_converse_flex",
      run_status: "planned",
      access_status: "aws_credentials_or_bedrock_api_key_required",
      source_refs: BEDROCK_NOVA_SOURCES,
      control_style: "bedrock_nova_2_lite_reasoning_effort",
      reasoning_effort: "provider_default",
      reasoning_effort_label: "none_omitted",
      thinking_depth: "none",
      thinking_default_expected: "omitted",
      reasoning_token_estimate_status: "not_estimated",
      execution_service_tier: "flex",
      public_pricing_service_tier: "standard",
      provider_request_settings: { serviceTier: { type: "flex" } },
      cached_input_price_per_mtok_usd: BEDROCK_NOVA_US_GEO_STANDARD_PRICES["us.amazon.nova-2-lite-v1:0"].cached_input,
      manual_prices: {
        input: BEDROCK_NOVA_US_GEO_STANDARD_PRICES["us.amazon.nova-2-lite-v1:0"].input,
        output: BEDROCK_NOVA_US_GEO_STANDARD_PRICES["us.amazon.nova-2-lite-v1:0"].output,
        source: "bedrock_nova_us_geo_standard_pricing_2026_07_21",
      },
      pricing_note: "The none condition omits reasoningConfig. Flex execution is deliberately costed at US Geo standard Bedrock pricing for this runtime model ID.",
    },
  ),
  ...["low", "medium", "high"].map((effort) => {
    const high = effort === "high";
    return direct(
      `bedrock-flex-us-amazon-nova-2-lite-v1-0-${effort}`,
      `Amazon Nova 2 Lite Flex ${effort}`,
      "bedrock-flex",
      "bedrock-flex/us.amazon.nova-2-lite-v1:0",
      "us.amazon.nova-2-lite-v1:0",
      { reasoning_effort: effort },
      ["amazon-nova", "flex-execution", "thinking", `reasoning-${effort}`],
      {
        upstream_provider: "amazon",
        provider_api: "bedrock_converse_flex",
        run_status: "planned",
        access_status: "aws_credentials_or_bedrock_api_key_required",
        source_refs: BEDROCK_NOVA_SOURCES,
        control_style: "bedrock_nova_2_lite_reasoning_effort",
        thinking_depth: effort,
        reasoning_effort_label: effort,
        execution_service_tier: "flex",
        public_pricing_service_tier: "standard",
        provider_request_settings: {
          serviceTier: { type: "flex" },
          additionalModelRequestFields: {
            reasoningConfig: { type: "enabled", maxReasoningEffort: effort },
          },
        },
        ...(high ? { generation_settings: { reasoning_effort: "high" } } : {}),
        ...(high
          ? {
              omit_generation_settings: [
                "max_tokens",
                "temperature",
                "top_p",
                "top_k",
              ],
            }
          : {}),
        // AWS requires maxTokens to be omitted at high effort. Preserve that
        // unconstrained wire contract rather than inventing a cost-only cap.
        cached_input_price_per_mtok_usd: BEDROCK_NOVA_US_GEO_STANDARD_PRICES["us.amazon.nova-2-lite-v1:0"].cached_input,
        manual_prices: {
          input: BEDROCK_NOVA_US_GEO_STANDARD_PRICES["us.amazon.nova-2-lite-v1:0"].input,
          output: BEDROCK_NOVA_US_GEO_STANDARD_PRICES["us.amazon.nova-2-lite-v1:0"].output,
          source: "bedrock_nova_us_geo_standard_pricing_2026_07_21",
        },
        pricing_note: "Flex execution is deliberately costed at US Geo standard Bedrock pricing for this runtime model ID.",
      },
    );
  }),
  ...["sonar", "sonar-pro", "sonar-reasoning-pro"].map((modelId) => {
    const price = PERPLEXITY_SONAR_STANDARD_PRICES[modelId];
    return direct(
      `perplexity-${slug(modelId)}-provider-default`,
      `Perplexity ${modelId} provider default`,
      "perplexity",
      `perplexity/${modelId}`,
      modelId,
      {},
      ["native-sonar", "provider-default", "thinking-unmeasured"],
      providerDefaultMetadata({
          provider_api: "inspect_native_perplexity_sonar",
          run_status: "planned",
          access_status: "api_key_required",
          source_refs: PERPLEXITY_SONAR_SOURCES,
          manual_prices: {
            input: price.input,
            output: price.output,
            source: "perplexity_sonar_standard_pricing_2026_07_21",
          },
          request_fee_usd_per_1k: price.request_fee_usd_per_1k,
          request_fee_context_label: "low search context size (provider default)",
          cost_accounting: "token_prices_plus_low_context_request_fee",
          pricing_note: "Standard Sonar token prices plus the documented low search-context request fee; low is the provider default and no Pro Search option is set.",
        },
      ),
    )
  }),
  ...[
    {
      id: "none",
      label: "none",
      settings: { extra_body: { thinking: { type: "disabled" } } },
      thinking: { type: "disabled" },
    },
    {
      id: "high",
      label: "high",
      settings: {
        reasoning_effort: "high",
        extra_body: { thinking: { type: "enabled" } },
      },
      thinking: { type: "enabled" },
    },
    {
      id: "xhigh",
      label: "xhigh",
      settings: {
        reasoning_effort: "xhigh",
        extra_body: { thinking: { type: "enabled" } },
      },
      thinking: { type: "enabled" },
    },
  ].map(({ id, label, settings, thinking }) =>
    direct(
      `zai-glm-5-2-${id}`,
      `Z.AI GLM-5.2 ${label}`,
      "zai",
      "zai/glm-5.2",
      "glm-5.2",
      settings,
      [
        "open-weight",
        "thinking",
        id === "none" ? "reasoning-disabled" : "reasoning-enabled",
        `reasoning-${id}`,
      ],
      {
        upstream_provider: "z-ai",
        provider_api: "zai_openai_compatible",
        run_status: "planned",
        access_status: "api_key_required",
        source_refs: ZAI_GLM_5_2_SOURCES,
        control_style: "zai_glm_5_2_thinking_type_and_effort",
        thinking_depth: id,
        reasoning_effort_label: label,
        provider_request_settings: { thinking, ...(id === "none" ? {} : { reasoning_effort: id }) },
        context_window_tokens: 1_000_000,
        max_output_tokens: 128_000,
        cached_input_price_per_mtok_usd: 0.26,
        weight_status: "open_weights",
        weight_status_source_refs: [GLM_5_2_WEIGHTS_SOURCE],
        manual_prices: ZAI_GLM_5_2_STANDARD_PRICES,
      },
    )
  ),
];

async function main() {
  const generatedAt = new Date().toISOString();
  const [openRouterModels, directPriceResolution] = await Promise.all([
    fetchOpenRouterModels(),
    resolvePriceCatalog(),
  ]);
  const openRouterPriceCards = priceCardsFromOpenRouterModels(
    { data: openRouterModels },
    {
      retrievedAt: generatedAt,
      sourceUrl: OPENROUTER_MODELS_URL,
    },
  );
  const priceCards = [
    ...openRouterPriceCards,
    ...directPriceResolution.price_cards,
  ];
  const priceIndex = buildPriceIndex(priceCards);
  const sourceCounts = countBy(priceCards, (card) => card.source?.name ?? "unknown");
  const eligibleOpenRouterModels = openRouterModels.filter(isEligibleOpenRouterModel);
  const automaticallySelectedOpenRouterEntries = eligibleOpenRouterModels
    .filter((model) => (
      !REQUESTED_OPENROUTER_EXPANSION_MODEL_ID_SET.has(model.id) &&
      !EXCLUDED_OPENROUTER_REQUESTED_EXPANSION_MODEL_ID_SET.has(model.id)
    ))
    .map((model) => openRouterEntry(model, priceIndex))
    .sort(compareRankedEntries)
    .slice(0, TARGET_OPENROUTER_ENTRIES)
    .map((entry, index) => ({
      ...withoutScore(entry),
      id: `openrouter-${String(index + 1).padStart(3, "0")}-${slug(entry.model_id)}`,
    }));
  const requestedOpenRouterEntries = requiredOpenRouterModels(
    openRouterModels,
    REQUESTED_OPENROUTER_EXPANSION_MODEL_IDS,
    "requested OpenRouter expansion",
  ).map((model) => requestedOpenRouterEntry(model, priceIndex));
  const openRouterEntries = [
    ...automaticallySelectedOpenRouterEntries,
    ...requestedOpenRouterEntries,
  ];
  const directEntries = DIRECT_PROVIDER_ENTRIES.map((entry) =>
    enrichDirectEntry(entry, priceIndex),
  );
  const entries = [...openRouterEntries, ...directEntries];
  const registry = {
    schema_version: "model-registry-v1",
    generated_at: generatedAt,
    defaults: {
      task: "obviousbench/tasks/barrage.py",
      profile: DEFAULT_PROFILE,
      seed: DEFAULT_SEED,
      generation_settings: DEFAULT_GENERATION_SETTINGS,
      inspect_args: ["--no-log-model-api", "--no-log-realtime"],
      cost_estimation: "obviousbench estimate-cost",
    },
    sources: {
      openrouter_models_api: {
        url: OPENROUTER_MODELS_URL,
        fetched_model_count: openRouterModels.length,
        eligible_text_model_count: eligibleOpenRouterModels.length,
        selected_count: openRouterEntries.length,
        automatically_selected_count: automaticallySelectedOpenRouterEntries.length,
      },
      [OPENROUTER_REQUESTED_EXPANSION_SOURCE]: {
        checked_on: "2026-07-21",
        source_refs: [
          OPENROUTER_MODELS_URL,
          "https://openrouter.ai/docs/guides/best-practices/reasoning-tokens",
        ],
        declared_model_ids: REQUESTED_OPENROUTER_EXPANSION_MODEL_IDS,
        excluded_model_ids: {
          "poolside/laguna-xs.2": "not_a_current_OpenRouter_model_id",
        },
        revalidated_model_ids: {
          "poolside/laguna-xs-2.1": "current_catalog_listed_after_prior_xs_2_1_omission",
          "arcee-ai/virtuoso-large": "current_catalog_listed_after_prior_live_smoke_http_400",
          "inflection/inflection-3-productivity": "current_catalog_listed_after_prior_live_smoke_http_526",
          "inflection/inflection-3-pi": "current_catalog_listed_after_prior_live_smoke_http_404",
        },
        pricing_source: "current_openrouter_models_api",
      },
      direct_provider_expansion_2026_07_21: {
        checked_on: "2026-07-21",
        vertex_gemini: {
          sources: VERTEX_GEMINI_SOURCES,
          execution_service_tier: "flex",
          public_pricing_service_tier: "standard",
          emitted_thinking_levels: ["minimal", "low", "medium", "high"],
          preflight_status: "blocked_billing_disabled",
          retained_as: "historical_provider_preflight_evidence",
        },
        gemini_flex: {
          sources: GEMINI_FLEX_SOURCES,
          execution_service_tier: "flex",
          public_pricing_service_tier: "standard",
          authentication: "Gemini_Developer_API_key",
          emitted_thinking_levels: ["minimal", "low", "medium", "high"],
          thinking_off_support: "not_supported; minimal_is_not_labeled_as_off",
        },
        longcat: {
          sources: LONGCAT_SOURCES,
          emitted_thinking_types: ["disabled", "enabled"],
          pricing_semantics: "normal_undiscounted",
        },
        aion: {
          sources: AION_SOURCES,
          catalog_scope: "five_active_text_models",
          emitted_reasoning_efforts_for_aion_2: ["none", "low", "medium", "high"],
        },
        cohere: {
          sources: COHERE_SOURCES,
          native_reasoning_models: [
            "command-a-plus-05-2026",
            "command-a-reasoning-08-2025",
          ],
          budget_labels: ["low_budget_512", "medium_budget_2048", "high_budget_8192"],
          direct_pricing_status: "user_supplied_standard_equivalent_for_command_a_family",
        },
        bedrock: {
          sources: BEDROCK_NOVA_SOURCES,
          standard_models: [
            "us.amazon.nova-micro-v1:0",
            "us.amazon.nova-lite-v1:0",
          ],
          flex_models: [
            "us.amazon.nova-pro-v1:0",
            "us.amazon.nova-2-lite-v1:0",
          ],
          native_nova_premier: {
            status: "blocked_current_bearer_key_http_404",
            approved_release_route: "openrouter/amazon/nova-premier-v1",
          },
          public_pricing_service_tier: "standard",
          pricing_region_and_inference_profile: "US Geo runtime model IDs",
        },
        perplexity: {
          sources: PERPLEXITY_SONAR_SOURCES,
          default_search_context_size: "low",
          cost_accounting: "token_prices_plus_low_context_request_fee",
        },
        zai_glm_5_2: {
          sources: ZAI_GLM_5_2_SOURCES,
          api_base_url: "https://api.z.ai/api/paas/v4/",
          context_window_tokens: 1_000_000,
          max_output_tokens: 128_000,
          emitted_reasoning_rows: ["none", "high", "xhigh"],
        },
      },
      runcost_external_price_resolution: {
        package: "runcost",
        mode: "runtime_external_sources",
        selected_direct_source: directPriceResolution.selected_source,
        direct_source_states: directPriceResolution.sources,
        openrouter_card_count: openRouterPriceCards.length,
        card_count: priceCards.length,
        source_counts: sourceCounts,
      },
      openai_gpt_5_6: {
        model_guide: "https://developers.openai.com/api/docs/guides/latest-model",
        pricing: "https://developers.openai.com/api/docs/pricing",
        checked_on: "2026-07-09",
        execution_service_tier: "flex",
        public_pricing_service_tier: "standard",
      },
      deepseek_v4: {
        quick_start: "https://api-docs.deepseek.com/",
        pricing: "https://api-docs.deepseek.com/quick_start/pricing",
        thinking: "https://api-docs.deepseek.com/guides/thinking_mode/",
        checked_on: "2026-07-14",
        input_price_semantics: "cache_miss",
      },
      tinker_inkling: {
        models_and_pricing: TINKER_INKLING_SOURCES[0],
        openai_compatible_api: TINKER_INKLING_SOURCES[1],
        checked_on: "2026-07-15",
        model_id: "thinkingmachines/Inkling",
        list_price_semantics: "Listed Inkling rates carry a limited-time 50% discount; registry prices intentionally double them. Cached prefill remains 80% below the undiscounted input rate.",
      },
      kimi_k3: {
        quick_start: KIMI_K3_SOURCES[0],
        thinking_effort: KIMI_K3_SOURCES[1],
        pricing: KIMI_K3_SOURCES[2],
        checked_on: "2026-07-16",
        model_id: "kimi-k3",
        reasoning_effort: "max",
        public_pricing_service_tier: "standard",
        batch_discount_included_in_registry_price: false,
      },
    },
    selection_policy: {
      target_openrouter_entries: TARGET_OPENROUTER_ENTRIES,
      emphasis: [
        "free OpenRouter endpoints",
        "open-weight or open-source families",
        "small, lite, mini, nano, flash, and cheap models",
        "non-thinking defaults where generation settings can suppress reasoning",
        "the reviewed 2026-07-21 OpenRouter request expansion is declared independently of automatic ranking",
        "a small direct-provider baseline for existing OpenAI, Anthropic, Gemini, Grok, Meta, NVIDIA NIM, DeepSeek, and Tinker credentials",
        "reviewed direct-provider declarations for Vertex, LongCat, AionLabs, Cohere, Amazon Bedrock, Perplexity, and Z.AI; frozen registries receive them only through the declared-ID merge workflow",
      ],
      exclusions: [
        "image-only models",
        "audio-only models",
        "embedding-only models",
        "expired model endpoints",
        "extra high-cost frontier duplicates beyond the direct-provider baseline",
      ],
    },
    entries,
  };

  await mkdir("configs", { recursive: true });
  await writeFile(OUTPUT_PATH, `${toYaml(registry)}\n`, "utf8");
  console.log(`Wrote ${entries.length} entries to ${OUTPUT_PATH}`);
  console.log(
    `OpenRouter selected: ${openRouterEntries.length} (${automaticallySelectedOpenRouterEntries.length} automatic, ${requestedOpenRouterEntries.length} requested)`,
  );
  console.log(`Direct-provider selected: ${directEntries.length}`);
  console.log(
    `Free OpenRouter entries: ${entries.filter((entry) => entry.tags.includes("free")).length}`,
  );
}

function direct(id, label, providerRoute, inspectModel, modelId, settings, tags, metadata = {}) {
  return {
    id,
    label,
    provider_route: providerRoute,
    upstream_provider: providerRoute === "grok" ? "xai" : providerRoute,
    inspect_model: inspectModel,
    model_id: modelId,
    profile: DEFAULT_PROFILE,
    seed: DEFAULT_SEED,
    generation_settings: generationSettings(null, settings),
    ...metadata,
    tags: unique(["direct-provider", ...tags]),
    priority: metadata.priority ?? (tags.includes("prior-baseline") ? "baseline" : "secondary"),
    source: metadata.source ?? "curated_direct_provider_baseline",
  };
}

function manualPriceLookupMetadata(metadata = {}) {
  return {
    ...metadata,
    manual_price_lookup_required: true,
  };
}

function providerDefaultMetadata(metadata = {}) {
  return {
    ...metadata,
    control_style: "provider_default_unmeasured",
    reasoning_effort: "provider_default",
    reasoning_effort_label: "Default",
    thinking_depth: "provider_default",
    thinking_default_expected: "unmeasured",
    reasoning_token_estimate_status: "not_estimated",
  };
}

function nonThinkingDefaultMetadata(metadata = {}) {
  return {
    ...metadata,
    control_style: "provider_default_non_thinking",
    reasoning_effort: "provider_default",
    reasoning_effort_label: "none",
    thinking_depth: "none",
    thinking_default_expected: "non_thinking",
    reasoning_token_estimate_status: "not_applicable",
  };
}

function argumentValue(name, fallback) {
  const index = process.argv.indexOf(name);
  if (index === -1) {
    return fallback;
  }
  if (!process.argv[index + 1]) {
    throw new Error(`${name} requires a path`);
  }
  return process.argv[index + 1];
}

async function fetchOpenRouterModels() {
  const response = await fetch(OPENROUTER_MODELS_URL, {
    headers: {
      accept: "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(`OpenRouter models request failed: ${response.status}`);
  }
  const payload = await response.json();
  if (!Array.isArray(payload.data)) {
    throw new Error("OpenRouter models response did not include a data array.");
  }
  return payload.data;
}

function isEligibleOpenRouterModel(model) {
  const inputModalities = model.architecture?.input_modalities ?? [];
  const outputModalities = model.architecture?.output_modalities ?? [];
  return (
    inputModalities.includes("text") &&
    outputModalities.includes("text") &&
    !isExpired(model.expiration_date)
  );
}

function isExpired(expirationDate) {
  if (!expirationDate) {
    return false;
  }
  const timestamp = Date.parse(expirationDate);
  return Number.isFinite(timestamp) && timestamp < Date.now();
}

function requiredOpenRouterModels(models, ids, description) {
  const byId = new Map(models.map((model) => [model.id, model]));
  const missing = ids.filter((id) => !byId.has(id));
  if (missing.length > 0) {
    throw new Error(`${description} missing from the OpenRouter Models API: ${missing.join(", ")}`);
  }
  const ineligible = ids.filter((id) => !isEligibleOpenRouterModel(byId.get(id)));
  if (ineligible.length > 0) {
    throw new Error(`${description} is not currently a live text-to-text OpenRouter model: ${ineligible.join(", ")}`);
  }
  return ids.map((id) => byId.get(id));
}

function requestedOpenRouterEntry(model, priceIndex) {
  const entry = withoutScore(openRouterEntry(model, priceIndex));
  const expectedDefaultThinking = REQUESTED_OPENROUTER_DEFAULT_THINKING_DEPTHS[model.id] ?? "unmeasured";
  return applyWeightStatusOverride({
    ...entry,
    id: `openrouter-requested-2026-07-21-${slug(model.id)}`,
    source: OPENROUTER_REQUESTED_EXPANSION_SOURCE,
    source_refs: [
      OPENROUTER_MODELS_URL,
      "https://openrouter.ai/docs/guides/best-practices/reasoning-tokens",
    ],
    control_style: "openrouter_provider_default",
    reasoning_effort: "provider_default",
    reasoning_effort_label: "Default",
    thinking_depth: "provider_default",
    thinking_default_expected: expectedDefaultThinking,
    reasoning_token_estimate_status: "not_estimated",
    priority: "requested-expansion",
    tags: unique([...entry.tags, "requested-expansion"]),
  });
}

function openRouterEntry(model, priceIndex) {
  const inputPerMtok = perMillion(model.pricing?.prompt);
  const outputPerMtok = perMillion(model.pricing?.completion);
  const hasTokenPrices = inputPerMtok !== null && outputPerMtok !== null;
  const free = hasTokenPrices && inputPerMtok === 0 && outputPerMtok === 0;
  const openWeight = hasPattern(model, OPEN_WEIGHT_PATTERNS) || Boolean(model.hugging_face_id);
  const small = hasPattern(model, SMALL_MODEL_PATTERNS);
  const thinkingNamed = hasPattern(model, THINKING_PATTERNS);
  const cheap = hasTokenPrices && (free || (inputPerMtok <= 1 && outputPerMtok <= 5));
  const textOnly = (model.architecture?.input_modalities ?? []).length === 1;
  const runcostCard = findPriceCard(priceIndex, "openrouter", model.id);
  const maxOutputTokens = numberOrNull(model.top_provider?.max_completion_tokens);
  const omitDefaultOutputCap = UNCAPPED_OPENROUTER_PROVIDER_DEFAULT_MODEL_ID_SET.has(
    model.id,
  );
  const tags = unique([
    "openrouter",
    free ? "free" : null,
    openWeight ? "open-weight" : null,
    small ? "small" : null,
    cheap ? "cheap" : null,
    textOnly ? "text-only" : "multimodal",
    thinkingNamed ? "thinking-named" : "non-thinking-candidate",
    model.supported_parameters?.includes("tools") ? "tools-supported" : null,
    model.supported_parameters?.includes("reasoning") ? "reasoning-parameter-supported" : null,
  ]);
  const score =
    (free ? 10000 : 0) +
    (openWeight ? 3000 : 0) +
    (small ? 1800 : 0) +
    (!thinkingNamed ? 1200 : 0) +
    (cheap ? 900 : 0) +
    (textOnly ? 200 : 0) +
    Math.min(Math.max(Number(model.created ?? 0) / 100000000, 0), 1000) -
    (hasTokenPrices && (inputPerMtok > 5 || outputPerMtok > 20) ? 700 : 0);

  return applyWeightStatusOverride({
    _score: score,
    _created: Number(model.created ?? 0),
    label: model.name,
    provider_route: "openrouter",
    upstream_provider: model.id.split("/")[0],
    inspect_model: `openrouter/${model.id}`,
    model_id: model.id,
    canonical_slug: model.canonical_slug ?? model.id,
    profile: DEFAULT_PROFILE,
    seed: DEFAULT_SEED,
    generation_settings: generationSettings(maxOutputTokens, {}, {
      omitMaxTokens: omitDefaultOutputCap,
    }),
    ...(omitDefaultOutputCap
      ? { omit_generation_settings: ["max_tokens"] }
      : {}),
    context_window_tokens: numberOrNull(model.context_length),
    max_output_tokens: maxOutputTokens,
    input_price_per_mtok_usd: inputPerMtok,
    output_price_per_mtok_usd: outputPerMtok,
    pricing_source: "openrouter_models_api",
    runcost_price_card_id: runcostCard?.id ?? null,
    runcost_price_source: runcostCard?.source?.name ?? null,
    source: "openrouter_models_api",
    priority: free ? "free-first" : openWeight || small ? "stress-candidate" : "coverage",
    tags,
  });
}

function applyWeightStatusOverride(entry) {
  const override = WEIGHT_STATUS_OVERRIDES[entry.model_id];
  if (!override) return entry;
  const tagsWithoutWeightStatus = entry.tags.filter((tag) => tag !== "open-weight");
  return {
    ...entry,
    tags: unique([
      ...tagsWithoutWeightStatus,
      override.openWeight ? "open-weight" : null,
    ]),
    weight_status: override.openWeight ? "open_weights" : "proprietary",
    weight_status_source_refs: override.sourceRefs,
  };
}

function generationSettings(
  maxOutputTokens,
  overrides = {},
  { omitMaxTokens = false } = {},
) {
  const settings = {
    ...DEFAULT_GENERATION_SETTINGS,
    max_tokens: outputSafetyCap(maxOutputTokens),
    ...overrides,
  };
  if (omitMaxTokens) {
    delete settings.max_tokens;
  }
  return settings;
}

function outputSafetyCap(maxOutputTokens) {
  if (Number.isFinite(maxOutputTokens) && maxOutputTokens > 0) {
    return Math.min(OUTPUT_SAFETY_MAX_TOKENS, maxOutputTokens);
  }
  return OUTPUT_SAFETY_MAX_TOKENS;
}

function enrichDirectEntry(entry, priceIndex) {
  if (entry.manual_prices) {
    const { manual_prices, ...rest } = entry;
    return {
      ...rest,
      input_price_per_mtok_usd: manual_prices.input,
      ...(manual_prices.cached_input === undefined
        ? {}
        : { cached_input_price_per_mtok_usd: manual_prices.cached_input }),
      output_price_per_mtok_usd: manual_prices.output,
      pricing_source: manual_prices.source,
      runcost_price_card_id: null,
      runcost_price_source: null,
    };
  }
  if (entry.manual_price_lookup_required) {
    return {
      ...entry,
      input_price_per_mtok_usd: null,
      output_price_per_mtok_usd: null,
      pricing_source: "manual_lookup_required",
      runcost_price_card_id: null,
      runcost_price_source: null,
    };
  }
  const runcostProvider = {
    gemini: "google",
    grok: "xai",
  }[entry.provider_route] ?? entry.provider_route;
  const manualPrice = DIRECT_PRICE_OVERRIDES_USD_PER_MTOK[
    `${entry.provider_route}:${entry.model_id}`
  ];
  if (manualPrice) {
    return {
      ...entry,
      input_price_per_mtok_usd: manualPrice.input,
      output_price_per_mtok_usd: manualPrice.output,
      pricing_source: manualPrice.source,
      runcost_price_card_id: null,
      runcost_price_source: null,
    };
  }
  const runcostCard = findPriceCard(priceIndex, runcostProvider, entry.model_id);
  return {
    ...entry,
    input_price_per_mtok_usd: componentPricePerMillion(
      runcostCard,
      "input_uncached_tokens",
    ),
    output_price_per_mtok_usd: componentPricePerMillion(
      runcostCard,
      "output_text_tokens",
    ),
    pricing_source: runcostCard
      ? "runcost_external_price_resolution"
      : "manual_lookup_required",
    runcost_price_card_id: runcostCard?.id ?? null,
    runcost_price_source: runcostCard?.source?.name ?? null,
  };
}

function buildPriceIndex(priceCards) {
  const byProviderModel = new Map();
  for (const card of priceCards) {
    const key = priceKey(card.provider, card.model);
    const existing = byProviderModel.get(key);
    if (!existing || sourceRank(card) < sourceRank(existing)) {
      byProviderModel.set(key, card);
    }
  }
  return byProviderModel;
}

function findPriceCard(index, provider, model) {
  const candidates = [
    priceKey(provider, model),
    priceKey(provider, model.replace(/^google\//, "")),
    priceKey(provider, model.replace(/^xai\//, "")),
    priceKey(provider, `${provider}/${model}`),
  ];
  for (const candidate of candidates) {
    const card = index.get(candidate);
    if (card) {
      return card;
    }
  }
  return null;
}

function priceKey(provider, model) {
  return `${provider}:${model}`;
}

function sourceRank(card) {
  const name = card.source?.name ?? "";
  const rank = SOURCE_PRIORITY.indexOf(name);
  return rank === -1 ? SOURCE_PRIORITY.length : rank;
}

function componentPricePerMillion(card, usageComponent) {
  const component = card?.components?.find(
    (entry) => entry.usage_component === usageComponent,
  );
  if (!component) {
    return null;
  }
  return normalizePricePerMillion(component.price?.amount, component.price?.per);
}

function normalizePricePerMillion(amount, per) {
  const amountNumber = Number(amount);
  const perNumber = Number(per);
  if (!Number.isFinite(amountNumber) || !Number.isFinite(perNumber) || perNumber === 0) {
    return null;
  }
  return roundMoney((amountNumber / perNumber) * 1000000);
}

function perMillion(value) {
  const numeric = Number(value ?? 0);
  if (!Number.isFinite(numeric)) {
    return null;
  }
  return roundMoney(numeric * 1000000);
}

function roundMoney(value) {
  if (value === null) {
    return null;
  }
  return Number(value.toFixed(8));
}

function hasPattern(model, patterns) {
  const haystack = `${model.id} ${model.name ?? ""} ${model.hugging_face_id ?? ""}`.toLowerCase();
  return patterns.some((pattern) => haystack.includes(pattern));
}

function compareRankedEntries(left, right) {
  return (
    right._score - left._score ||
    right._created - left._created ||
    left.model_id.localeCompare(right.model_id)
  );
}

function withoutScore(entry) {
  const { _score, _created, ...rest } = entry;
  return rest;
}

function countBy(values, keyFn) {
  return Object.fromEntries(
    Object.entries(
      values.reduce((counts, value) => {
        const key = keyFn(value);
        counts[key] = (counts[key] ?? 0) + 1;
        return counts;
      }, {}),
    ).sort((left, right) => left[0].localeCompare(right[0])),
  );
}

function numberOrNull(value) {
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : null;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function slug(value) {
  return String(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

function toYaml(value, indent = 0) {
  const pad = " ".repeat(indent);
  if (Array.isArray(value)) {
    if (value.length === 0) {
      return "[]";
    }
    return value
      .map((item) => {
        if (isScalar(item)) {
          return `${pad}- ${formatScalar(item)}`;
        }
        return `${pad}-\n${toYaml(item, indent + 2)}`;
      })
      .join("\n");
  }
  if (value && typeof value === "object") {
    const entries = Object.entries(value).filter(([, entryValue]) => entryValue !== undefined);
    if (entries.length === 0) {
      return "{}";
    }
    return entries
      .map(([key, entryValue]) => {
        if (isScalar(entryValue) || isEmptyCollection(entryValue)) {
          return `${pad}${key}: ${formatScalar(entryValue)}`;
        }
        return `${pad}${key}:\n${toYaml(entryValue, indent + 2)}`;
      })
      .join("\n");
  }
  return `${pad}${formatScalar(value)}`;
}

function isScalar(value) {
  return value === null || ["string", "number", "boolean"].includes(typeof value);
}

function isEmptyCollection(value) {
  return (
    (Array.isArray(value) && value.length === 0) ||
    (value && typeof value === "object" && Object.keys(value).length === 0)
  );
}

function formatScalar(value) {
  if (value === null) {
    return "null";
  }
  if (Array.isArray(value) && value.length === 0) {
    return "[]";
  }
  if (value && typeof value === "object" && Object.keys(value).length === 0) {
    return "{}";
  }
  if (typeof value === "string") {
    return JSON.stringify(value);
  }
  return String(value);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
