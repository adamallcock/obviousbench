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
  const outputTextTokens = Math.max(outputTokens - reasoningTokens, 0);

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
      component("output_reasoning_tokens", reasoningTokens),
    ].filter((entry) => Number(entry.quantity) > 0),
    raw_usage: usage,
    metadata: {
      sample_id: record.sample_id,
    },
  };
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
