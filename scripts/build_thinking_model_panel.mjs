#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { defaultPriceCards } from "runcost";

const OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models";
const OUTPUT_YAML = "configs/model_thinking_settings_v1.yaml";
const OUTPUT_CSV = "docs/research/2026-06-01-thinking-model-settings-costs.csv";
const OUTPUT_MD = "docs/research/2026-06-01-thinking-model-settings-costs.md";
const BARRAGE_PATH = "data/barrages/hard_obvious_8x10_seed_20260531.jsonl";
const PROFILE = "hard_obvious_8x10";
const SEED = 20260531;
const VISIBLE_OUTPUT_TOKENS_PER_SAMPLE = 8;
const TARGET_OPENROUTER_MODELS = 35;
const REQUIRED_OPENROUTER_MODEL_IDS = ["minimax/minimax-m3"];

const SOURCE_PRIORITY = ["openrouter", "models.dev", "llm-prices", "litellm"];
const DIRECT_PROVIDER_SOURCES = {
  openai: [
    "https://developers.openai.com/api/docs/models",
    "https://developers.openai.com/api/docs/guides/reasoning",
    "https://developers.openai.com/api/docs/pricing",
  ],
  anthropic: [
    "https://platform.claude.com/docs/en/build-with-claude/extended-thinking",
    "https://platform.claude.com/docs/en/build-with-claude/effort",
  ],
  gemini: [
    "https://ai.google.dev/gemini-api/docs/thinking",
    "https://ai.google.dev/gemini-api/docs/pricing",
  ],
  grok: [
    "https://docs.x.ai/developers/model-capabilities/text/reasoning",
    "https://docs.x.ai/developers/models/grok-4",
  ],
  openrouter: [
    "https://openrouter.ai/api/v1/models",
    "https://openrouter.ai/docs/guides/best-practices/reasoning-tokens",
  ],
};

const CONFIGURED_REASONING_TOKEN_CAPS = {
  openai: {
    none: 0,
    minimal: 64,
    low: 256,
    medium: 1024,
    high: 4096,
    xhigh: 8192,
  },
  anthropic: {
    low: 512,
    medium: 2048,
    high: 8192,
    xhigh: 16384,
    max: 32768,
  },
  grok: {
    none: 0,
    low: 256,
    medium: 1024,
    high: 4096,
    xhigh: 8192,
  },
  openrouter: {
    none: 0,
    minimal: 64,
    low: 512,
    medium: 2048,
    high: 8192,
    xhigh: 16384,
  },
};

const GEMINI_BUDGETS = {
  none: 0,
  minimal: 1024,
  low: 1024,
  medium: 8192,
  high: 24576,
  max: 32768,
};

const CALIBRATED_REASONING_TOKENS = {
  openai: {
    none: 0,
    minimal: 16,
    low: 64,
    medium: 96,
    high: 160,
    xhigh: 320,
    max: 320,
  },
  anthropic: {
    low: 16,
    medium: 48,
    high: 128,
    xhigh: 256,
    max: 384,
  },
  grok: {
    none: 0,
    low: 128,
    medium: 256,
    high: 512,
    xhigh: 1024,
    max: 1024,
  },
  gemini: {
    none: 0,
    minimal: 32,
    low: 64,
    medium: 192,
    high: 384,
    max: 512,
  },
  openrouter_generic: {
    none: 0,
    minimal: 16,
    low: 64,
    medium: 128,
    high: 256,
    xhigh: 512,
    max: 512,
  },
  openrouter_deepseek: {
    none: 0,
    minimal: 64,
    low: 128,
    medium: 384,
    high: 1024,
    xhigh: 1536,
    max: 1536,
  },
};

const CALIBRATION_SOURCE = {
  basis: "measured_usage_with_conservative_buffer",
  historical_summary_glob: "results/summaries/*/usage_by_sample.csv",
  live_probe_path: "results/summaries/thinking-usage-calibration-20260601-live/results.jsonl",
  notes: [
    "Historical hard-obvious and balanced runs show GPT-5.4/5.5 medium/high using tens of reasoning tokens per sample, with high p95 values around 95-116.",
    "The 2026-06-01 live probe measured gpt-5 high at 128 reasoning tokens, Grok 4.3 high at 228, OpenRouter Gemini 3.5 Flash high at 190, and DeepSeek R1 high at the 512-token probe cap.",
    "Configured thinking budgets remain in provider_request_settings as run caps; estimated_usage uses calibrated expected usage for this short-answer benchmark.",
  ],
};

async function main() {
  const generatedAt = new Date().toISOString();
  const [openRouterModels, priceCards, profileStats] = await Promise.all([
    fetchOpenRouterModels(),
    Promise.resolve(defaultPriceCards()),
    readProfileStats(),
  ]);
  const priceIndex = buildPriceIndex(priceCards);
  const sourceCounts = countBy(priceCards, (card) => card.source?.name ?? "unknown");
  const directEntries = buildDirectEntries(priceIndex, profileStats);
  const openRouterEntries = buildOpenRouterEntries(openRouterModels, profileStats);
  const entries = dedupeEntries([...directEntries, ...openRouterEntries]);
  const totals = summarize(entries);

  const panel = {
    schema_version: "model-thinking-settings-v1",
    generated_at: generatedAt,
    run_status: "planned_not_run",
    source_registry: "configs/model_registry_v1.yaml",
    defaults: {
      task: "obviousbench/tasks/barrage.py",
      profile: PROFILE,
      seed: SEED,
      inspect_args: ["--no-log-model-api", "--no-log-realtime"],
    },
    estimation_profile: {
      barrage_path: BARRAGE_PATH,
      sample_count: profileStats.sampleCount,
      input_tokens_total: profileStats.inputTokensTotal,
      input_tokens_per_sample_avg: round(profileStats.inputTokensTotal / profileStats.sampleCount, 2),
      visible_output_tokens_per_sample: VISIBLE_OUTPUT_TOKENS_PER_SAMPLE,
      visible_output_tokens_total: profileStats.sampleCount * VISIBLE_OUTPUT_TOKENS_PER_SAMPLE,
      method: [
        "Full-panel estimate only; no full-panel model calls are made.",
        "Input tokens are approximated from the hard-obvious barrage prompt text length divided by four.",
        "Visible output assumes short final answers of 8 output tokens per sample, based on measured final-answer runs.",
        "Thinking costs use calibrated expected reasoning usage for this benchmark, not the configured provider thinking budget cap.",
        "Configured thinking budgets remain in provider_request_settings so real runs can still exercise the requested depth.",
        "Reasoning or thinking tokens are billed at the output-token rate unless the live source exposes a separate reasoning-token price.",
      ],
    },
    sources: {
      openrouter_models_api: {
        url: OPENROUTER_MODELS_URL,
        fetched_model_count: openRouterModels.length,
        selected_model_count: unique(openRouterEntries.map((entry) => entry.model_id)).length,
        selected_setting_count: openRouterEntries.length,
      },
      runcost_default_price_cards: {
        package: "runcost",
        card_count: priceCards.length,
        source_counts: sourceCounts,
      },
      usage_calibration: CALIBRATION_SOURCE,
      provider_docs: DIRECT_PROVIDER_SOURCES,
    },
    selection_policy: {
      summary: "Frontier and benchmark-regular thinking settings separated from the broad small/free failure registry.",
      emphasis: [
        "OpenAI GPT-5 family and newer reasoning efforts, with GPT-5.0 none excluded.",
        "Claude Sonnet and Opus 4.5+ thinking controls.",
        "Grok 4+ reasoning controls.",
        "Gemini 2.5+ thinking budgets and Gemini 3 thinking levels.",
        "MiniMax M3 via OpenRouter with multiple reasoning budgets.",
        "OpenRouter models that expose reasoning controls and regularly appear in frontier or open-weight comparisons.",
      ],
      exclusions: [
        "OpenAI Pro research-system variants such as gpt-5-pro, gpt-5.5-pro, gpt-5.4-pro, and gpt-5.2-pro.",
        "OpenRouter Claude Opus fast variants for 4.8, 4.7, and 4.6.",
      ],
      caution: [
        "This panel is intentionally more expensive than the broad model registry.",
        "Run a smoke subset before a full sweep because provider support for reasoning controls changes frequently.",
        "Cost estimates are planning estimates, not provider invoices.",
      ],
    },
    totals,
    entries,
  };

  await mkdir("configs", { recursive: true });
  await mkdir("docs/research", { recursive: true });
  await writeFile(OUTPUT_YAML, `${toYaml(panel)}\n`, "utf8");
  await writeFile(OUTPUT_CSV, renderCsv(entries), "utf8");
  await writeFile(OUTPUT_MD, renderMarkdown(panel), "utf8");
  console.log(`Wrote ${entries.length} thinking settings to ${OUTPUT_YAML}`);
  console.log(`Wrote estimates to ${OUTPUT_CSV} and ${OUTPUT_MD}`);
}

function buildDirectEntries(priceIndex, profileStats) {
  const specs = [
    openAiSpec("gpt-5.5", "OpenAI GPT-5.5", ["none", "low", "medium", "high", "xhigh"]),
    openAiSpec("gpt-5.4", "OpenAI GPT-5.4", ["none", "low", "medium", "high", "xhigh"]),
    openAiSpec("gpt-5.4-mini", "OpenAI GPT-5.4 mini", ["none", "low", "medium", "high", "xhigh"]),
    openAiSpec("gpt-5.4-nano", "OpenAI GPT-5.4 nano", ["none", "low", "medium", "high", "xhigh"]),
    openAiSpec("gpt-5.2", "OpenAI GPT-5.2", ["none", "low", "medium", "high", "xhigh"]),
    openAiSpec("gpt-5", "OpenAI GPT-5", ["minimal", "low", "medium", "high"]),
    openAiSpec("gpt-5-mini", "OpenAI GPT-5 mini", ["minimal", "low", "medium", "high"]),
    openAiSpec("gpt-5-nano", "OpenAI GPT-5 nano", ["minimal", "low", "medium", "high"]),
    anthropicAdaptiveSpec("claude-opus-4-8", "Claude Opus 4.8", ["low", "medium", "high", "xhigh", "max"]),
    anthropicAdaptiveSpec("claude-opus-4-7", "Claude Opus 4.7", ["low", "medium", "high", "xhigh", "max"]),
    anthropicAdaptiveSpec("claude-opus-4-6", "Claude Opus 4.6", ["low", "medium", "high", "max"]),
    anthropicManualSpec("claude-opus-4-5", "Claude Opus 4.5", ["low", "medium", "high", "max"]),
    anthropicAdaptiveSpec("claude-sonnet-4-6", "Claude Sonnet 4.6", ["low", "medium", "high", "max"]),
    anthropicManualSpec("claude-sonnet-4-5", "Claude Sonnet 4.5", ["low", "medium", "high", "max"]),
    geminiBudgetSpec("gemini-2.5-pro", "Gemini 2.5 Pro", ["low", "medium", "high", "max"]),
    geminiBudgetSpec("gemini-2.5-flash", "Gemini 2.5 Flash", ["none", "low", "medium", "high"]),
    geminiBudgetSpec("gemini-2.5-flash-lite", "Gemini 2.5 Flash-Lite", ["none", "low", "medium", "high"]),
    geminiLevelSpec("gemini-3.1-pro-preview", "Gemini 3.1 Pro Preview", ["low", "high"]),
    geminiLevelSpec("gemini-3.5-flash", "Gemini 3.5 Flash", ["minimal", "low", "medium", "high"]),
    geminiLevelSpec("gemini-3-flash-preview", "Gemini 3 Flash Preview", ["minimal", "low", "medium", "high"]),
    geminiLevelSpec("gemini-3.1-flash-lite", "Gemini 3.1 Flash-Lite", ["minimal", "low", "medium", "high"]),
    grokSpec("grok-4.3", "Grok 4.3", ["none", "low", "medium", "high"], "xai:grok-4.3"),
    grokSpec(
      "grok-4.20-multi-agent",
      "Grok 4.20 Multi-Agent",
      ["low", "medium", "high", "xhigh"],
      null,
      { input: 2, output: 6, source: "openrouter_models_api_proxy_price" },
    ),
  ];

  return specs.flatMap((spec) =>
    spec.depths.map((depth) =>
      enrichEntry(entryFromSpec(spec, depth, profileStats), priceIndex),
    ),
  );
}

function openAiSpec(modelId, label, efforts) {
  return {
    provider_route: "openai",
    upstream_provider: "openai",
    provider_api: "openai_responses",
    inspect_model: `openai/${modelId}`,
    model_id: modelId,
    price_provider: "openai",
    price_model: modelId,
    label,
    control_style: "openai_reasoning_effort",
    source_refs: DIRECT_PROVIDER_SOURCES.openai,
    tags: ["direct-provider", "frontier", "openai", "thinking"],
    depths: efforts.map((effort) => effortDepth("openai", effort)),
  };
}

function anthropicAdaptiveSpec(modelId, label, efforts) {
  return {
    provider_route: "anthropic",
    upstream_provider: "anthropic",
    provider_api: "anthropic_messages",
    inspect_model: `anthropic/${modelId}`,
    model_id: modelId,
    price_provider: "anthropic",
    price_model: modelId,
    label,
    control_style: "anthropic_adaptive_thinking_effort",
    source_refs: DIRECT_PROVIDER_SOURCES.anthropic,
    tags: ["direct-provider", "frontier", "anthropic", "thinking"],
    depths: efforts.map((effort) => effortDepth("anthropic", effort)),
  };
}

function anthropicManualSpec(modelId, label, efforts) {
  return {
    provider_route: "anthropic",
    upstream_provider: "anthropic",
    provider_api: "anthropic_messages",
    inspect_model: `anthropic/${modelId}`,
    model_id: modelId,
    price_provider: "anthropic",
    price_model: modelId,
    label,
    control_style: "anthropic_manual_thinking_budget",
    source_refs: DIRECT_PROVIDER_SOURCES.anthropic,
    tags: ["direct-provider", "frontier", "anthropic", "thinking"],
    depths: efforts.map((effort) => budgetDepth(effort, CONFIGURED_REASONING_TOKEN_CAPS.anthropic[effort])),
  };
}

function geminiBudgetSpec(modelId, label, budgetIds) {
  return {
    provider_route: "gemini",
    upstream_provider: "google",
    provider_api: "gemini_generate_content",
    inspect_model: `google/${modelId}`,
    model_id: modelId,
    price_provider: "google",
    price_model: modelId,
    label,
    control_style: "gemini_thinking_budget",
    source_refs: DIRECT_PROVIDER_SOURCES.gemini,
    tags: ["direct-provider", "gemini", "thinking"],
    depths: budgetIds.map((depthId) => budgetDepth(depthId, GEMINI_BUDGETS[depthId])),
  };
}

function geminiLevelSpec(modelId, label, levels) {
  return {
    provider_route: "gemini",
    upstream_provider: "google",
    provider_api: "gemini_generate_content",
    inspect_model: `google/${modelId}`,
    model_id: modelId,
    price_provider: "google",
    price_model: modelId,
    label,
    control_style: "gemini_thinking_level",
    source_refs: DIRECT_PROVIDER_SOURCES.gemini,
    tags: ["direct-provider", "gemini", "thinking"],
    depths: levels.map((level) => budgetDepth(level, GEMINI_BUDGETS[level])),
  };
}

function grokSpec(modelId, label, efforts, priceKeyOverride, manualPrices = null) {
  return {
    provider_route: "grok",
    upstream_provider: "xai",
    provider_api: "xai_responses",
    inspect_model: `grok/${modelId}`,
    model_id: modelId,
    price_provider: priceKeyOverride ? priceKeyOverride.split(":")[0] : "xai",
    price_model: priceKeyOverride ? priceKeyOverride.split(":")[1] : modelId,
    label,
    control_style: "xai_reasoning_effort",
    source_refs: DIRECT_PROVIDER_SOURCES.grok,
    tags: ["direct-provider", "grok", "thinking"],
    manual_prices: manualPrices,
    depths: efforts.map((effort) => effortDepth("grok", effort)),
  };
}

function buildOpenRouterEntries(openRouterModels, profileStats) {
  const selected = selectOpenRouterModels(openRouterModels);
  return selected.flatMap((model) => {
    const spec = openRouterSpec(model);
    return spec.depths.map((depth) => enrichOpenRouterEntry(entryFromSpec(spec, depth, profileStats), model));
  });
}

function selectOpenRouterModels(models) {
  const candidates = models
    .filter((model) => isTextModel(model) && !isExpired(model.expiration_date))
    .filter((model) => !isExcludedOpenRouterThinkingModel(model))
    .filter((model) => (model.supported_parameters ?? []).includes("reasoning"))
    .map((model) => ({ model, score: openRouterScore(model) }))
    .filter((row) => row.score > 0)
    .sort((left, right) => (
      right.score - left.score ||
      Number(right.model.created ?? 0) - Number(left.model.created ?? 0) ||
      left.model.id.localeCompare(right.model.id)
    ))
    .map((row) => row.model);
  const selected = selectBalancedOpenRouterModels(candidates).slice(0, TARGET_OPENROUTER_MODELS);
  return includeRequiredOpenRouterModels(candidates, selected);
}

function selectBalancedOpenRouterModels(candidates) {
  const caps = {
    openai: 11,
    anthropic: 7,
    google: 5,
    "x-ai": 3,
    qwen: 4,
    deepseek: 4,
    moonshotai: 2,
    minimax: 2,
    "z-ai": 2,
    mistralai: 2,
    nvidia: 2,
  };
  const counts = new Map();
  const selected = [];
  const seen = new Set();

  for (const model of candidates) {
    const family = openRouterFamily(model);
    const count = counts.get(family) ?? 0;
    const cap = caps[family] ?? 2;
    if (count >= cap) {
      continue;
    }
    selected.push(model);
    seen.add(model.id);
    counts.set(family, count + 1);
    if (selected.length >= TARGET_OPENROUTER_MODELS) {
      return selected;
    }
  }

  for (const model of candidates) {
    if (seen.has(model.id)) {
      continue;
    }
    selected.push(model);
    if (selected.length >= TARGET_OPENROUTER_MODELS) {
      return selected;
    }
  }
  return selected;
}

function openRouterFamily(model) {
  return model.id.split("/")[0];
}

function includeRequiredOpenRouterModels(candidates, selected) {
  const byId = new Map(candidates.map((model) => [model.id, model]));
  const seen = new Set(selected.map((model) => model.id));
  const withRequired = [...selected];
  for (const id of REQUIRED_OPENROUTER_MODEL_IDS) {
    if (!seen.has(id) && byId.has(id)) {
      withRequired.push(byId.get(id));
      seen.add(id);
    }
  }
  return withRequired;
}

function isExcludedOpenRouterThinkingModel(model) {
  const id = model.id.toLowerCase();
  return (
    /^openai\/gpt-5(?:\.(5|4|2))?-pro(?:$|:|-)/.test(id) ||
    /^anthropic\/claude-opus-4\.(8|7|6)-fast(?:$|:|-)/.test(id)
  );
}

function openRouterScore(model) {
  const haystack = `${model.id} ${model.name ?? ""}`.toLowerCase();
  const createdScore = Math.min(Number(model.created ?? 0) / 1000000000, 2);
  const freeScore = Number(model.pricing?.prompt ?? 1) === 0 && Number(model.pricing?.completion ?? 1) === 0 ? 8 : 0;
  const patterns = [
    [/openai\/gpt-5\.(5|4|2)|openai\/gpt-5($|-)|openai\/o[134]/, 40],
    [/anthropic\/claude-(opus|sonnet)-4(\.|-|$)/, 39],
    [/x-ai\/grok-4/, 38],
    [/google\/gemini-(3|2\.5)/, 37],
    [/qwen\/qwen3\.(7|6|5)|qwen\/qwen3-235b|qwen\/qwen3-coder/, 30],
    [/deepseek\/deepseek-r1/, 29],
    [/moonshotai\/kimi-k2/, 27],
    [/minimax\/minimax-m3/, 27],
    [/z-ai\/glm-(5|4\.5)/, 26],
    [/mistralai\/(mistral-medium|magistral|mistral-large)/, 22],
    [/nvidia\/.*reasoning|nemotron.*reasoning/, 18],
  ];
  const matchScore = patterns.reduce((score, [pattern, value]) => (
    pattern.test(haystack) ? Math.max(score, value) : score
  ), 0);
  return matchScore + createdScore + freeScore;
}

function openRouterSpec(model) {
  const depthPlan = openRouterDepthPlan(model);
  return {
    provider_route: "openrouter",
    upstream_provider: model.id.split("/")[0],
    provider_api: "openrouter_chat_completions",
    inspect_model: `openrouter/${model.id}`,
    model_id: model.id,
    price_provider: "openrouter",
    price_model: model.id,
    label: model.name ?? model.id,
    control_style: depthPlan.controlStyle,
    source_refs: DIRECT_PROVIDER_SOURCES.openrouter,
    tags: unique([
      "openrouter",
      "thinking",
      "frontier-or-benchmark-regular",
      model.pricing?.prompt === "0" && model.pricing?.completion === "0" ? "free" : null,
      model.id.includes("qwen") || model.id.includes("deepseek") || model.id.includes("glm") || model.id.includes("kimi") ? "open-weight-or-open-family" : null,
    ]),
    depths: depthPlan.depths,
  };
}

function openRouterDepthPlan(model) {
  const id = model.id.toLowerCase();
  if (id.includes("gemini-2.5-pro")) {
    return {
      controlStyle: "openrouter_reasoning_max_tokens",
      depths: ["low", "medium", "high", "max"].map((name) => budgetDepth(name, GEMINI_BUDGETS[name])),
    };
  }
  if (id.includes("gemini-2.5")) {
    return {
      controlStyle: "openrouter_reasoning_max_tokens",
      depths: ["none", "low", "medium", "high"].map((name) => budgetDepth(name, GEMINI_BUDGETS[name])),
    };
  }
  if (id.includes("gemini-3.1-pro")) {
    return {
      controlStyle: "openrouter_reasoning_effort",
      depths: ["low", "high"].map((name) => effortDepth("openrouter", name)),
    };
  }
  if (id.includes("gemini-3")) {
    return {
      controlStyle: "openrouter_reasoning_effort",
      depths: ["minimal", "low", "medium", "high"].map((name) => effortDepth("openrouter", name)),
    };
  }
  if (id.includes("gpt-5") || id.includes("grok-4.3")) {
    const efforts = id.includes("gpt-5") && !id.includes("gpt-5.2") && !id.includes("gpt-5.4") && !id.includes("gpt-5.5")
      ? ["minimal", "low", "medium", "high"]
      : ["none", "low", "medium", "high", "xhigh"];
    return {
      controlStyle: "openrouter_reasoning_effort",
      depths: efforts.map((name) => effortDepth("openrouter", name)),
    };
  }
  if (id.includes("grok-4.20-multi-agent")) {
    return {
      controlStyle: "openrouter_reasoning_effort",
      depths: ["low", "medium", "high", "xhigh"].map((name) => effortDepth("openrouter", name)),
    };
  }
  return {
    controlStyle: "openrouter_reasoning_max_tokens",
    depths: ["low", "medium", "high"].map((name) => budgetDepth(name, CONFIGURED_REASONING_TOKEN_CAPS.openrouter[name])),
  };
}

function entryFromSpec(spec, depth, profileStats) {
  const basis = estimationBasisFor(spec, depth);
  const maxTokens = maxTokensFor(depth.configured_reasoning_tokens_per_sample);
  const providerSettings = providerRequestSettings(spec, depth, maxTokens);
  return {
    id: `${spec.provider_route}-${slug(spec.model_id)}-${slug(depth.id)}`,
    label: `${spec.label} ${depth.label}`,
    provider_route: spec.provider_route,
    upstream_provider: spec.upstream_provider,
    provider_api: spec.provider_api,
    inspect_model: spec.inspect_model,
    model_id: spec.model_id,
    profile: PROFILE,
    seed: SEED,
    run_status: "planned",
    control_style: spec.control_style,
    thinking_depth: depth.id,
    configured_reasoning_tokens_per_sample: depth.configured_reasoning_tokens_per_sample,
    generation_settings: generationSettings(spec, depth, maxTokens),
    provider_request_settings: providerSettings,
    estimated_usage: estimatedUsage(profileStats, basis.reasoningTokensPerSample, basis.source),
    source_refs: spec.source_refs,
    tags: unique([...spec.tags, depth.id, depth.configured_reasoning_tokens_per_sample === 0 ? "reasoning-disabled" : "reasoning-enabled"]),
    price_provider: spec.price_provider,
    price_model: spec.price_model,
    manual_prices: spec.manual_prices ?? null,
  };
}

function generationSettings(spec, depth, maxTokens) {
  const settings = {
    max_tokens: maxTokens,
  };
  if (spec.control_style.includes("effort")) {
    if (spec.provider_route === "anthropic") {
      settings.effort = depth.id;
    } else {
      settings.reasoning_effort = depth.id;
    }
  }
  if (spec.control_style.includes("budget") || spec.control_style.includes("max_tokens")) {
    settings.reasoning_tokens = depth.configured_reasoning_tokens_per_sample;
  }
  return settings;
}

function providerRequestSettings(spec, depth, maxTokens) {
  if (spec.provider_route === "openai") {
    return {
      max_output_tokens: maxTokens,
      reasoning: { effort: depth.id },
    };
  }
  if (spec.provider_route === "anthropic") {
    if (spec.control_style.includes("adaptive")) {
      return {
        max_tokens: maxTokens,
        thinking: { type: "adaptive", display: "omitted" },
        output_config: { effort: depth.id },
      };
    }
    return {
      max_tokens: maxTokens,
      thinking: {
        type: "enabled",
        budget_tokens: depth.configured_reasoning_tokens_per_sample,
        display: "omitted",
      },
    };
  }
  if (spec.provider_route === "gemini") {
    const thinkingConfig = spec.control_style.includes("level")
      ? { thinkingLevel: geminiLevel(depth.id) }
      : { thinkingBudget: depth.configured_reasoning_tokens_per_sample };
    return {
      generationConfig: {
        maxOutputTokens: maxTokens,
        thinkingConfig,
      },
    };
  }
  if (spec.provider_route === "grok") {
    return {
      max_output_tokens: maxTokens,
      reasoning: { effort: depth.id },
    };
  }
  if (spec.provider_route === "openrouter") {
    const reasoning = spec.control_style.includes("effort")
      ? { effort: depth.id, exclude: true }
      : { max_tokens: depth.configured_reasoning_tokens_per_sample, exclude: true };
    return {
      max_tokens: maxTokens,
      include_reasoning: false,
      reasoning,
    };
  }
  return { max_tokens: maxTokens };
}

function effortDepth(provider, effort) {
  return {
    id: effort,
    label: effort,
    configured_reasoning_tokens_per_sample: CONFIGURED_REASONING_TOKEN_CAPS[provider][effort],
  };
}

function budgetDepth(id, tokens) {
  return {
    id,
    label: id === "none" ? "thinking_budget_0" : `${id}_budget_${tokens}`,
    configured_reasoning_tokens_per_sample: tokens,
  };
}

function geminiLevel(depthId) {
  if (depthId === "minimal") {
    return "minimal";
  }
  if (depthId === "medium") {
    return "medium";
  }
  return depthId === "high" ? "high" : "low";
}

function estimationBasisFor(spec, depth) {
  const sourceKey = calibrationKeyFor(spec);
  const calibrated = CALIBRATED_REASONING_TOKENS[sourceKey] ?? CALIBRATED_REASONING_TOKENS.openrouter_generic;
  return {
    reasoningTokensPerSample: calibrated[depth.id] ?? CALIBRATED_REASONING_TOKENS.openrouter_generic[depth.id] ?? 128,
    source: `${CALIBRATION_SOURCE.basis}:${sourceKey}`,
  };
}

function calibrationKeyFor(spec) {
  if (spec.provider_route !== "openrouter") {
    return spec.provider_route === "gemini" ? "gemini" : spec.provider_route;
  }
  const id = spec.model_id.toLowerCase();
  if (id.startsWith("openai/")) {
    return "openai";
  }
  if (id.startsWith("anthropic/")) {
    return "anthropic";
  }
  if (id.startsWith("google/")) {
    return "gemini";
  }
  if (id.startsWith("x-ai/")) {
    return "grok";
  }
  if (id.startsWith("deepseek/")) {
    return "openrouter_deepseek";
  }
  return "openrouter_generic";
}

function estimatedUsage(profileStats, reasoningTokensPerSample, calibrationSource) {
  const samples = profileStats.sampleCount;
  const visibleOutputTokens = samples * VISIBLE_OUTPUT_TOKENS_PER_SAMPLE;
  const reasoningTokens = samples * reasoningTokensPerSample;
  return {
    sample_count: samples,
    input_tokens: profileStats.inputTokensTotal,
    visible_output_tokens: visibleOutputTokens,
    reasoning_tokens: reasoningTokens,
    output_tokens_billed: visibleOutputTokens + reasoningTokens,
    total_tokens: profileStats.inputTokensTotal + visibleOutputTokens + reasoningTokens,
    reasoning_tokens_per_sample: reasoningTokensPerSample,
    calibration_source: calibrationSource,
  };
}

function enrichEntry(entry, priceIndex) {
  if (entry.manual_prices) {
    return enrichWithPrices(entry, {
      inputPrice: entry.manual_prices.input,
      outputPrice: entry.manual_prices.output,
      reasoningPrice: entry.manual_prices.output,
      pricingSource: entry.manual_prices.source,
      priceCardId: null,
      priceCardSource: null,
    });
  }
  const card = findPriceCard(priceIndex, entry.price_provider, entry.price_model);
  const inputPrice = componentPricePerMillion(card, "input_uncached_tokens");
  const outputPrice = componentPricePerMillion(card, "output_text_tokens");
  return enrichWithPrices(entry, {
    inputPrice,
    outputPrice,
    reasoningPrice: outputPrice,
    pricingSource: card ? "runcost_default_price_cards" : "manual_lookup_required",
    priceCardId: card?.id ?? null,
    priceCardSource: card?.source?.name ?? null,
  });
}

function enrichOpenRouterEntry(entry, model) {
  const inputPrice = perMillion(model.pricing?.prompt);
  const outputPrice = perMillion(model.pricing?.completion);
  const reasoningPrice = perMillion(model.pricing?.internal_reasoning) ?? outputPrice;
  return enrichWithPrices(entry, {
    inputPrice,
    outputPrice,
    reasoningPrice,
    pricingSource: "openrouter_models_api",
    priceCardId: null,
    priceCardSource: null,
    contextWindow: numberOrNull(model.context_length),
    maxOutputTokens: numberOrNull(model.top_provider?.max_completion_tokens),
    supportedParameters: model.supported_parameters ?? [],
  });
}

function enrichWithPrices(entry, prices) {
  const estimated = estimateCost(entry.estimated_usage, prices);
  const { price_provider, price_model, manual_prices, ...rest } = entry;
  return {
    ...rest,
    context_window_tokens: prices.contextWindow ?? null,
    max_output_tokens: prices.maxOutputTokens ?? null,
    supported_parameters: prices.supportedParameters ?? null,
    input_price_per_mtok_usd: prices.inputPrice,
    output_price_per_mtok_usd: prices.outputPrice,
    reasoning_price_per_mtok_usd: prices.reasoningPrice,
    pricing_source: prices.pricingSource,
    runcost_price_card_id: prices.priceCardId,
    runcost_price_source: prices.priceCardSource,
    estimated_cost_usd: estimated.cost,
    estimated_cost_per_sample_usd: estimated.cost === null ? null : round(estimated.cost / entry.estimated_usage.sample_count, 8),
    cost_warnings: estimated.warnings,
  };
}

function estimateCost(usage, prices) {
  const warnings = [];
  if (prices.inputPrice === null || prices.outputPrice === null || prices.reasoningPrice === null) {
    warnings.push("missing price component; estimate unavailable");
    return { cost: null, warnings };
  }
  const inputCost = usage.input_tokens * prices.inputPrice / 1000000;
  const visibleOutputCost = usage.visible_output_tokens * prices.outputPrice / 1000000;
  const reasoningCost = usage.reasoning_tokens * prices.reasoningPrice / 1000000;
  return {
    cost: roundMoney(inputCost + visibleOutputCost + reasoningCost),
    warnings,
  };
}

async function fetchOpenRouterModels() {
  const response = await fetch(OPENROUTER_MODELS_URL, {
    headers: { accept: "application/json" },
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

async function readProfileStats() {
  const text = await readFile(BARRAGE_PATH, "utf8");
  const prompts = text
    .split(/\n+/)
    .filter(Boolean)
    .map((line) => JSON.parse(line).prompt ?? "");
  const inputTokens = prompts.map((prompt) => Math.max(Math.round(String(prompt).length / 4), 1));
  return {
    sampleCount: prompts.length,
    inputTokensTotal: inputTokens.reduce((sum, value) => sum + value, 0),
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
  if (value === undefined || value === null) {
    return null;
  }
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    return null;
  }
  return roundMoney(numeric * 1000000);
}

function isTextModel(model) {
  const inputModalities = model.architecture?.input_modalities ?? [];
  const outputModalities = model.architecture?.output_modalities ?? [];
  return inputModalities.includes("text") && outputModalities.includes("text");
}

function isExpired(expirationDate) {
  if (!expirationDate) {
    return false;
  }
  const timestamp = Date.parse(expirationDate);
  return Number.isFinite(timestamp) && timestamp < Date.now();
}

function maxTokensFor(reasoningTokensPerSample) {
  return Math.max(64, Math.min(65536, reasoningTokensPerSample + VISIBLE_OUTPUT_TOKENS_PER_SAMPLE + 64));
}

function dedupeEntries(entries) {
  const seen = new Set();
  const deduped = [];
  for (const entry of entries) {
    let id = entry.id;
    let suffix = 2;
    while (seen.has(id)) {
      id = `${entry.id}-${suffix}`;
      suffix += 1;
    }
    seen.add(id);
    deduped.push({ ...entry, id });
  }
  return deduped;
}

function summarize(entries) {
  const estimatedCosts = entries
    .map((entry) => entry.estimated_cost_usd)
    .filter((cost) => typeof cost === "number");
  return {
    entry_count: entries.length,
    provider_route_counts: countBy(entries, (entry) => entry.provider_route),
    thinking_depth_counts: countBy(entries, (entry) => entry.thinking_depth),
    priced_entry_count: estimatedCosts.length,
    estimated_full_panel_cost_usd: roundMoney(estimatedCosts.reduce((sum, cost) => sum + cost, 0)),
    max_single_entry_estimated_cost_usd: estimatedCosts.length ? roundMoney(Math.max(...estimatedCosts)) : null,
  };
}

function renderCsv(entries) {
  const fieldnames = [
    "id",
    "label",
    "provider_route",
    "inspect_model",
    "model_id",
    "thinking_depth",
    "control_style",
    "input_price_per_mtok_usd",
    "output_price_per_mtok_usd",
    "reasoning_price_per_mtok_usd",
    "configured_reasoning_tokens_per_sample",
    "estimated_reasoning_tokens_per_sample",
    "calibration_source",
    "estimated_cost_usd",
    "estimated_cost_per_sample_usd",
    "pricing_source",
    "cost_warnings",
  ];
  const rows = entries.map((entry) => ({
    id: entry.id,
    label: entry.label,
    provider_route: entry.provider_route,
    inspect_model: entry.inspect_model,
    model_id: entry.model_id,
    thinking_depth: entry.thinking_depth,
    control_style: entry.control_style,
    input_price_per_mtok_usd: cell(entry.input_price_per_mtok_usd),
    output_price_per_mtok_usd: cell(entry.output_price_per_mtok_usd),
    reasoning_price_per_mtok_usd: cell(entry.reasoning_price_per_mtok_usd),
    configured_reasoning_tokens_per_sample: entry.configured_reasoning_tokens_per_sample,
    estimated_reasoning_tokens_per_sample: entry.estimated_usage.reasoning_tokens_per_sample,
    calibration_source: entry.estimated_usage.calibration_source,
    estimated_cost_usd: cell(entry.estimated_cost_usd),
    estimated_cost_per_sample_usd: cell(entry.estimated_cost_per_sample_usd),
    pricing_source: entry.pricing_source,
    cost_warnings: entry.cost_warnings.join("; "),
  }));
  return [
    fieldnames.join(","),
    ...rows.map((row) => fieldnames.map((field) => csvCell(row[field])).join(",")),
    "",
  ].join("\n");
}

function renderMarkdown(panel) {
  const lines = [
    "---",
    "title: Thinking Model Settings And Cost Estimates",
    "date: 2026-06-01",
    "type: research",
    "status: draft",
    "---",
    "",
    "# Thinking Model Settings And Cost Estimates",
    "",
    "Dry-run cost estimates using measured token-usage calibration. The calibration run made a small number of provider calls; the full panel was not run.",
    "",
    "This panel keeps expensive frontier thinking settings separate from the broad small/free failure registry.",
    "",
    "## Sources",
    "",
    "- OpenAI model, reasoning, and pricing docs: https://developers.openai.com/api/docs/models and https://developers.openai.com/api/docs/pricing",
    "- Anthropic extended thinking and effort docs: https://platform.claude.com/docs/en/build-with-claude/extended-thinking and https://platform.claude.com/docs/en/build-with-claude/effort",
    "- Gemini thinking and pricing docs: https://ai.google.dev/gemini-api/docs/thinking and https://ai.google.dev/gemini-api/docs/pricing",
    "- xAI Grok reasoning docs: https://docs.x.ai/developers/model-capabilities/text/reasoning",
    "- OpenRouter live model API and reasoning-token docs: https://openrouter.ai/api/v1/models and https://openrouter.ai/docs/guides/best-practices/reasoning-tokens",
    "- Local npm `runcost` default price cards for normalized provider price lookup.",
    `- Historical usage summaries: \`${panel.sources.usage_calibration.historical_summary_glob}\`.`,
    `- Live calibration probe: \`${panel.sources.usage_calibration.live_probe_path}\`.`,
    "- Calibration note: `docs/research/2026-06-01-thinking-usage-calibration.md`.",
    "",
    "## Estimate Method",
    "",
    `- Profile: \`${panel.defaults.profile}\`, seed \`${panel.defaults.seed}\`, ${panel.estimation_profile.sample_count} samples.`,
    `- Estimated input tokens: ${panel.estimation_profile.input_tokens_total} total, ${panel.estimation_profile.input_tokens_per_sample_avg} per sample.`,
    `- Visible output assumption: ${panel.estimation_profile.visible_output_tokens_per_sample} tokens per sample, calibrated from prior final-answer runs.`,
    "- Thinking token estimates use measured historical runs plus the live calibration probe, with a buffer by provider family and depth.",
    "- The configured provider thinking budget is still preserved as a run cap; it is not treated as expected usage.",
    "- Thinking and reasoning tokens are costed as output tokens unless a live source exposes a separate reasoning-token price.",
    "",
    "## Calibration Notes",
    "",
    ...panel.sources.usage_calibration.notes.map((note) => `- ${note}`),
    "",
    "## Totals",
    "",
    `- Entries: ${panel.totals.entry_count}`,
    `- Priced entries: ${panel.totals.priced_entry_count}`,
    `- Estimated full-panel cost: $${money(panel.totals.estimated_full_panel_cost_usd)}`,
    `- Most expensive single planned setting: $${money(panel.totals.max_single_entry_estimated_cost_usd)}`,
    "",
    "## Settings",
    "",
    "| ID | Model | Route | Depth | Configured cap/sample | Est. reasoning/sample | Estimated cost | Pricing source |",
    "| --- | --- | --- | --- | ---: | ---: | ---: | --- |",
  ];
  for (const entry of panel.entries) {
    lines.push(
      `| ${md(entry.id)} | ${md(entry.label)} | ${md(entry.provider_route)} | ${md(entry.thinking_depth)} | ${entry.configured_reasoning_tokens_per_sample} | ${entry.estimated_usage.reasoning_tokens_per_sample} | $${money(entry.estimated_cost_usd)} | ${md(entry.pricing_source)} |`,
    );
  }
  const warnings = panel.entries.filter((entry) => entry.cost_warnings.length > 0);
  if (warnings.length) {
    lines.push("", "## Warnings", "");
    for (const entry of warnings) {
      lines.push(`- \`${entry.id}\`: ${entry.cost_warnings.join("; ")}`);
    }
  }
  lines.push("");
  return lines.join("\n");
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
    .slice(0, 96);
}

function roundMoney(value) {
  if (value === null || value === undefined) {
    return null;
  }
  return Number(value.toFixed(8));
}

function round(value, places) {
  return Number(value.toFixed(places));
}

function cell(value) {
  return value === null || value === undefined ? "" : String(value);
}

function csvCell(value) {
  const text = cell(value);
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function md(value) {
  return String(value).replaceAll("|", "\\|");
}

function money(value) {
  return value === null || value === undefined ? "unknown" : Number(value).toFixed(6);
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
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  return JSON.stringify(String(value));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
