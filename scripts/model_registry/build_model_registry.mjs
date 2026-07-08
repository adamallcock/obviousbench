#!/usr/bin/env node

import { mkdir, writeFile } from "node:fs/promises";
import { defaultPriceCards } from "runcost";

const OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models";
const OUTPUT_PATH = "configs/registries/model_registry_v1.yaml";
const TARGET_OPENROUTER_ENTRIES = 185;
const DEFAULT_PROFILE = "balanced_8x5";
const DEFAULT_SEED = 20260531;
const OUTPUT_SAFETY_MAX_TOKENS = 10000;
const DEFAULT_GENERATION_SETTINGS = {
  temperature: 0,
  max_tokens: OUTPUT_SAFETY_MAX_TOKENS,
};
const DIRECT_PRICE_OVERRIDES_USD_PER_MTOK = {
  "grok:grok-4.5": {
    source: "xai_grok_4_5_docs_2026_07_08",
    input: 2.0,
    output: 6.0,
  },
};

const SOURCE_PRIORITY = ["openrouter", "models.dev", "llm-prices", "litellm"];
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

const DIRECT_PROVIDER_ENTRIES = [
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
];

const PINNED_OPENROUTER_ENTRIES = [
  openRouterPinned(
    "openrouter-pinned-tencent-hy3-free",
    "Tencent: Hy3 (free endpoint; paid-equivalent pricing)",
    "tencent/hy3:free",
    {
      priced_as_model_id: "tencent/hy3",
      canonical_slug: "tencent/hy3",
      context_window_tokens: 262144,
      max_output_tokens: 0,
      input_price_per_mtok_usd: 0.2,
      output_price_per_mtok_usd: 0.8,
      cache_read_price_per_mtok_usd: 0.5,
      source: "curated_openrouter_release_pin",
      priority: "release-pin",
      tags: [
        "open-weight",
        "free-endpoint",
        "paid-equivalent-pricing",
        "cheap",
        "text-only",
        "non-thinking-candidate",
        "tools-supported",
        "reasoning-parameter-supported",
      ],
    },
  ),
];

async function main() {
  const generatedAt = new Date().toISOString();
  const [openRouterModels, priceCards] = await Promise.all([
    fetchOpenRouterModels(),
    Promise.resolve(defaultPriceCards()),
  ]);
  const priceIndex = buildPriceIndex(priceCards);
  const sourceCounts = countBy(priceCards, (card) => card.source?.name ?? "unknown");
  const eligibleOpenRouterModels = openRouterModels.filter(isEligibleOpenRouterModel);
  const openRouterEntries = eligibleOpenRouterModels
    .map((model) => openRouterEntry(model, priceIndex))
    .sort(compareRankedEntries)
    .slice(0, TARGET_OPENROUTER_ENTRIES)
    .map((entry, index) => ({
      ...withoutScore(entry),
      id: `openrouter-${String(index + 1).padStart(3, "0")}-${slug(entry.model_id)}`,
    }));
  const directEntries = DIRECT_PROVIDER_ENTRIES.map((entry) =>
    enrichDirectEntry(entry, priceIndex),
  );
  const selectedOpenRouterIds = new Set(openRouterEntries.map((entry) => entry.model_id));
  const pinnedOpenRouterEntries = PINNED_OPENROUTER_ENTRIES.filter(
    (entry) => !selectedOpenRouterIds.has(entry.model_id),
  );
  const entries = [...openRouterEntries, ...pinnedOpenRouterEntries, ...directEntries];
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
        pinned_release_count: pinnedOpenRouterEntries.length,
      },
      runcost_default_price_cards: {
        package: "runcost",
        card_count: priceCards.length,
        source_counts: sourceCounts,
      },
    },
    selection_policy: {
      target_openrouter_entries: TARGET_OPENROUTER_ENTRIES,
      emphasis: [
        "free OpenRouter endpoints",
        "open-weight or open-source families",
        "small, lite, mini, nano, flash, and cheap models",
        "non-thinking defaults where generation settings can suppress reasoning",
        "a small direct-provider baseline for existing OpenAI, Anthropic, Gemini, and Grok credentials",
        "pinned current release routes whose aggregate rows are published before the next full registry refresh",
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
  console.log(`OpenRouter selected: ${openRouterEntries.length}`);
  console.log(`Pinned OpenRouter entries: ${pinnedOpenRouterEntries.length}`);
  console.log(`Direct-provider selected: ${directEntries.length}`);
  console.log(
    `Free OpenRouter entries: ${entries.filter((entry) => entry.tags.includes("free")).length}`,
  );
}

function direct(id, label, providerRoute, inspectModel, modelId, settings, tags) {
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
    tags: unique(["direct-provider", ...tags]),
    priority: tags.includes("prior-baseline") ? "baseline" : "secondary",
    source: "curated_direct_provider_baseline",
  };
}

function openRouterPinned(id, label, modelId, overrides) {
  return {
    id,
    label,
    provider_route: "openrouter",
    upstream_provider: modelId.split("/")[0],
    inspect_model: `openrouter/${modelId}`,
    model_id: modelId,
    profile: DEFAULT_PROFILE,
    seed: DEFAULT_SEED,
    generation_settings: generationSettings(overrides.max_output_tokens),
    pricing_source: "openrouter_models_api",
    runcost_price_card_id: null,
    runcost_price_source: null,
    ...overrides,
    tags: unique(["openrouter", ...overrides.tags]),
  };
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

  return {
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
    generation_settings: generationSettings(maxOutputTokens),
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
  };
}

function generationSettings(maxOutputTokens, overrides = {}) {
  return {
    ...DEFAULT_GENERATION_SETTINGS,
    max_tokens: outputSafetyCap(maxOutputTokens),
    ...overrides,
  };
}

function outputSafetyCap(maxOutputTokens) {
  if (Number.isFinite(maxOutputTokens) && maxOutputTokens > 0) {
    return Math.min(OUTPUT_SAFETY_MAX_TOKENS, maxOutputTokens);
  }
  return OUTPUT_SAFETY_MAX_TOKENS;
}

function enrichDirectEntry(entry, priceIndex) {
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
    pricing_source: runcostCard ? "runcost_default_price_cards" : "manual_lookup_required",
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
