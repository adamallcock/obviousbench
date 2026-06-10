#!/usr/bin/env node

import { calculateCost, defaultPriceCards } from "runcost";

const input = await readStdin();
const payload = JSON.parse(input || "{}");
const priceCards = normalizeDecimalValues(defaultPriceCards());
const records = [];

for (const record of payload.records ?? []) {
  const usageLedger = buildUsageLedger(record);
  try {
    const ledger = calculateCost({
      usageLedger,
      priceCards,
      priceSourcePriority: ["models-dev", "llm-prices", "litellm"],
    });
    records.push({
      sample_id: record.sample_id,
      model: record.model,
      cost_source: "runcost",
      estimated_cost_usd: Number(ledger.total),
      ledger,
      warnings: ledger.warnings ?? [],
    });
  } catch (error) {
    records.push({
      sample_id: record.sample_id,
      model: record.model,
      cost_source: "runcost",
      estimated_cost_usd: null,
      ledger: null,
      warnings: [
        {
          code: "runcost_error",
          message: error instanceof Error ? error.message : String(error),
        },
      ],
    });
  }
}

process.stdout.write(
  JSON.stringify(
    {
      cost_source: "runcost",
      records,
    },
    null,
    2,
  ),
);

function buildUsageLedger(record) {
  const usage = record.usage ?? {};
  const inputTokens = numberValue(usage.input_tokens);
  const cacheReadTokens = numberValue(usage.cache_read_tokens);
  const cacheWriteTokens = numberValue(usage.cache_write_tokens);
  const reasoningTokens = numberValue(usage.reasoning_tokens);
  const outputTokens = numberValue(usage.output_tokens);
  const uncachedInputTokens = Math.max(
    inputTokens - cacheReadTokens - cacheWriteTokens,
    0,
  );
  const separateReasoningTokens = shouldPriceReasoningSeparately(record)
    ? reasoningTokens
    : 0;
  // `output_tokens` is the provider's authoritative, billing-inclusive total: it
  // already contains any billed thinking/reasoning tokens, charged at the output
  // rate for Anthropic, OpenAI, and the OpenRouter models we price. Direct
  // Gemini is the exception in our normalized Inspect logs: `output_tokens`
  // excludes reported thinking tokens, so we pass those as a separate
  // `output_reasoning_tokens` component and let runcost price them.
  //
  // The previous code carved `output_text = output_tokens - reasoning_tokens`
  // and priced a separate `output_reasoning_tokens` line. That was unsafe for two
  // reasons: (1) for Anthropic Claude 4.x `reasoning_tokens` is the re-tokenized
  // *summary* length, not billed thinking, and can even exceed `output_tokens`;
  // (2) when a price card has no reasoning rate (e.g.
  // anthropic:claude-opus-4-8:models-dev) runcost silently dropped that
  // component, under-charging reasoning-heavy rows (~36% on Opus 4.8 max).
  // `reasoning_tokens` is retained in raw_usage / metadata for observability only.
  const outputTextTokens = outputTokens;

  return {
    schema_version: "0.1",
    provider: record.provider,
    surface: record.surface ?? "normalized.usage",
    model: {
      requested: record.model,
      billed: billedModel(record.model),
      alias_resolution: "user_exact",
    },
    components: [
      component("input_uncached_tokens", uncachedInputTokens),
      component("input_cache_read_tokens", cacheReadTokens),
      component("input_cache_write_tokens", cacheWriteTokens),
      component("output_text_tokens", outputTextTokens),
      component("output_reasoning_tokens", separateReasoningTokens),
    ].filter((entry) => Number(entry.quantity) > 0),
    raw_usage: usage,
    metadata: {
      sample_id: record.sample_id,
      reasoning_tokens: reasoningTokens,
      reasoning_token_treatment:
        separateReasoningTokens > 0
          ? "priced_as_output_reasoning_tokens"
          : "observability_only",
    },
  };
}

function shouldPriceReasoningSeparately(record) {
  const usage = record.usage ?? {};
  if (numberValue(usage.reasoning_tokens) <= 0) {
    return false;
  }
  const provider = String(record.provider ?? "").toLowerCase();
  const model = String(record.model ?? "").toLowerCase();
  const surface = String(record.surface ?? "").toLowerCase();
  return (
    ((provider === "google" ||
      provider === "vertex" ||
      provider === "google-vertex") &&
      model.includes("gemini")) ||
    surface.includes("gemini.generate_content")
  );
}

function billedModel(model) {
  return String(model).includes("/") ? String(model).split("/").slice(1).join("/") : model;
}

function component(name, quantity) {
  return {
    name,
    quantity: String(quantity),
    unit: "token",
  };
}

function numberValue(value) {
  return Number(value ?? 0);
}

function normalizeDecimalValues(value) {
  if (Array.isArray(value)) {
    return value.map((entry) => normalizeDecimalValues(entry));
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([key, entry]) => [
        key,
        normalizeDecimalValues(entry),
      ]),
    );
  }
  if (typeof value === "number" && Number.isFinite(value)) {
    return decimalString(value);
  }
  if (typeof value === "string" && /^-?\d+(?:\.\d+)?e-?\d+$/i.test(value)) {
    return decimalString(Number(value));
  }
  return value;
}

function decimalString(value) {
  const text = String(value);
  if (!text.includes("e")) {
    return text;
  }
  return value.toFixed(24).replace(/0+$/, "").replace(/\.$/, "");
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}
