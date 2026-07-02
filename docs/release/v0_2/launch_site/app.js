(function () {
  "use strict";

  const inputRows = Array.isArray(window.OBVIOUSBENCH_ROWS) ? window.OBVIOUSBENCH_ROWS : [];
  const rows = inputRows.filter((row) => row.surface_included);
  const build = window.OBVIOUSBENCH_BUILD || {};
  const providerIcons = window.OBVIOUSBENCH_PROVIDER_ICONS || {};

  const COLORS = {
    "anthropic": "#c15d3a",
    "deepseek": "#2b6cb0",
    "google": "#4285f4",
    "meta-llama": "#0d7bb8",
    "minimax": "#7251b5",
    "mistralai": "#e56b28",
    "moonshotai": "#31343a",
    "nvidia": "#4d8c2b",
    "openai": "#0d8b6f",
    "qwen": "#7c4dce",
    "x-ai": "#1f2937",
    "z-ai": "#d23f72",
    "unclassified": "#77817c"
  };

  const FAMILY_COLORS = [
    "#0d8b6f",
    "#3157d5",
    "#c15d3a",
    "#7c4dce",
    "#e56b28",
    "#0d7bb8",
    "#d23f72",
    "#4d8c2b",
    "#b56a15",
    "#1f2937",
    "#008c95",
    "#8b5cf6",
    "#b91c1c",
    "#64748b",
    "#047857",
    "#9333ea"
  ];

  const EFFORT_LABELS = {
    none: "None / disabled",
    minimal: "Minimal",
    low: "Low",
    medium: "Medium",
    high: "High",
    xhigh: "Xhigh",
    max: "Max",
    reasoning: "Reasoning / dynamic"
  };

  const chartInstances = new Map();
  const rowById = new Map(rows.map((row) => [row.row_id, row]));
  const surfaceRows = rows.filter((row) => row.surface_included);
  const narrativeRows = rows.filter((row) => row.narrative_included !== false);
  const narrativeSurfaceRows = narrativeRows.filter((row) => row.surface_included);

  const numberFormat = new Intl.NumberFormat("en-US");
  const oneDecimal = new Intl.NumberFormat("en-US", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const twoDecimals = new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function formatPct(value, digits) {
    if (!Number.isFinite(Number(value))) return "—";
    const d = digits == null ? 1 : digits;
    const rounded = Number(value);
    if (Math.abs(rounded - Math.round(rounded)) < 0.00005) return `${Math.round(rounded)}%`;
    return `${rounded.toFixed(d)}%`;
  }

  function formatCost(value) {
    const cost = Number(value);
    if (!Number.isFinite(cost)) return "—";
    if (cost < 0.01) return `$${cost.toFixed(4)}`;
    if (cost < 1) return `$${cost.toFixed(3)}`;
    return `$${cost.toFixed(2)}`;
  }

  function formatCostAxis(value) {
    const cost = Number(value);
    if (!Number.isFinite(cost)) return "";
    if (cost < 0.0001) return `$${cost.toFixed(5)}`;
    if (cost < 0.001) return `$${cost.toFixed(4)}`;
    if (cost < 0.01) return `$${cost.toFixed(3)}`;
    if (cost < 1) return `$${cost.toFixed(2)}`;
    return `$${cost.toFixed(0)}`;
  }

  function formatCostAxisCompact(value) {
    const cost = Number(value);
    if (!Number.isFinite(cost)) return "";
    if (Math.abs(cost) < 0.000001) return "$0";
    if (cost < 0.001) return `$${cost.toFixed(4)}`;
    if (cost < 0.01) return `$${cost.toFixed(3)}`;
    if (cost < 1) return `$${cost.toFixed(2)}`;
    if (cost < 10) return `$${cost.toFixed(2)}`;
    return `$${cost.toFixed(0)}`;
  }

  function formatTableCost(value) {
    const cost = Number(value);
    if (!Number.isFinite(cost)) return "—";
    if (cost > 0 && cost < 0.001) return "<$0.001";
    return `$${cost.toFixed(3)}`;
  }

  function formatTokens(value) {
    const tokens = Number(value || 0);
    if (tokens === 0) return "0";
    if (tokens >= 1000000) return `${(tokens / 1000000).toFixed(tokens >= 10000000 ? 0 : 1)}m`;
    if (tokens >= 1000) return `${(tokens / 1000).toFixed(tokens >= 100000 ? 0 : 1)}k`;
    return numberFormat.format(tokens);
  }

  function logCostBounds(inputRows, padding) {
    const costs = inputRows
      .map((row) => Number(row.cost))
      .filter((cost) => Number.isFinite(cost) && cost > 0);
    if (!costs.length) return {};
    const minLog = Math.log10(Math.min(...costs));
    const maxLog = Math.log10(Math.max(...costs));
    const span = Math.max(0.2, maxLog - minLog);
    const pad = padding == null ? 0.12 : padding;
    return {
      min: Math.pow(10, minLog - span * pad),
      max: Math.pow(10, maxLog + span * pad)
    };
  }

  function displayEffort(row) {
    const raw = String(row.configured_effort || row.effort || "none");
    const cleaned = raw
      .replace(/_budget_\d+$/i, "")
      .replace(/_/g, " ")
      .trim();
    if (cleaned === "default" && row.effort === "reasoning") return "Default reasoning";
    if (cleaned === "default" || cleaned === "disabled") return EFFORT_LABELS[row.effort] || "None / disabled";
    return cleaned.charAt(0).toUpperCase() + cleaned.slice(1);
  }

  function displayCompactEffort(row) {
    const label = displayEffort(row);
    return label === "Default reasoning" ? "Default" : label;
  }

  function displayThresholdEffort(row) {
    return displayCompactEffort(row);
  }

  function compactAvailabilityLabel(row) {
    if (row.availability === "open_weights") return "Open";
    if (row.availability === "proprietary") return "Closed";
    return row.availability_label;
  }

  function thresholdAvailabilityLabel(row) {
    return compactAvailabilityLabel(row);
  }

  function shortEffortLabel(effort) {
    const raw = String(effort || "none");
    if (raw === "none") return "None";
    if (raw === "reasoning") return "Dynamic";
    return (EFFORT_LABELS[raw] || raw).replace(" / disabled", "");
  }

  function providerColor(rowOrProvider) {
    const provider = typeof rowOrProvider === "string" ? rowOrProvider : rowOrProvider.provider;
    return COLORS[provider] || COLORS.unclassified;
  }

  function hashText(value) {
    return String(value || "").split("").reduce((hash, char) => {
      return ((hash << 5) - hash + char.charCodeAt(0)) | 0;
    }, 0);
  }

  function familyColor(row) {
    const key = row.model_family || row.model || row.row_id || row.provider;
    return FAMILY_COLORS[Math.abs(hashText(key)) % FAMILY_COLORS.length];
  }

  function activeFrontierProviders() {
    return new Set(frontierState.providers || []);
  }

  function providerFilterIsActive() {
    return activeFrontierProviders().size > 0;
  }

  function rowMatchesFrontierProviders(row) {
    const providers = activeFrontierProviders();
    return !providers.size || providers.has(row.provider);
  }

  function frontierColor(row) {
    return providerFilterIsActive() ? familyColor(row) : providerColor(row);
  }

  function updateFrontierColorLegend() {
    const element = document.getElementById("frontier-color-legend");
    if (!element) return;
    element.textContent = providerFilterIsActive() ? "Color = model family" : "Color = provider";
  }

  function providerIconHtml(row, compact) {
    const icon = providerIcons[row.provider];
    const cls = compact ? "provider-icon provider-icon-compact" : "provider-icon";
    if (icon) {
      return `<span class="${cls}" data-provider="${escapeHtml(row.provider)}" title="${escapeHtml(row.provider_label)}" aria-hidden="true"></span>`;
    }
    const initials = String(row.provider_label || row.provider || "?")
      .split(/\s+/)
      .map((part) => part[0])
      .join("")
      .slice(0, 2)
      .toUpperCase();
    return `<span class="${cls} provider-icon-fallback" title="${escapeHtml(row.provider_label)}">${escapeHtml(initials)}</span>`;
  }

  function providerIconFor(provider, label, compact) {
    return providerIconHtml({ provider, provider_label: label || provider }, compact);
  }

  function installProviderIconStyles() {
    if (!document.head || document.getElementById("provider-icon-styles")) return;
    const style = document.createElement("style");
    style.id = "provider-icon-styles";
    style.textContent = Object.entries(providerIcons).map(([provider, source]) =>
      `.provider-icon[data-provider="${provider}"]{--provider-icon:url("${source}")}`
    ).join("\n");
    document.head.appendChild(style);
  }

  function pickerSearchHtml(placeholder) {
    return `<label class="picker-search"><span class="sr-only">${escapeHtml(placeholder)}</span><input type="search" placeholder="${escapeHtml(placeholder)}"></label>`;
  }

  function setupSearchablePicker(config) {
    const picker = document.getElementById(config.pickerId);
    if (!picker) return;
    const trigger = picker.querySelector(".provider-picker-trigger");
    const menu = picker.querySelector(".provider-picker-menu");
    if (!trigger || !menu) return;

    menu.innerHTML = [
      pickerSearchHtml(config.searchPlaceholder || "Search"),
      `<div class="picker-option-list">`,
      config.options.map((option) => {
        const icon = config.iconForOption ? config.iconForOption(option) : "";
        const active = option.value === config.currentValue();
        return `<button type="button" role="option" data-picker-option="${escapeHtml(option.value)}" data-picker-label="${escapeHtml(option.label)}" aria-selected="${active}" class="${active ? "active" : ""}">${icon}<span>${escapeHtml(option.label)}</span></button>`;
      }).join(""),
      `</div>`
    ].join("");

    const input = menu.querySelector("input");
    const buttons = Array.from(menu.querySelectorAll("[data-picker-option]"));

    function setOpen(open) {
      menu.hidden = !open;
      trigger.setAttribute("aria-expanded", String(open));
      picker.classList.toggle("open", open);
      if (open && input) window.requestAnimationFrame(() => input.focus());
      if (!open && input) {
        input.value = "";
        buttons.forEach((button) => { button.hidden = false; });
      }
    }

    trigger.addEventListener("click", () => setOpen(menu.hidden));
    if (input) {
      input.addEventListener("input", () => {
        const needle = input.value.trim().toLowerCase();
        buttons.forEach((button) => {
          button.hidden = needle && !button.textContent.toLowerCase().includes(needle);
        });
      });
      input.addEventListener("keydown", (event) => {
        if (event.key === "Escape") setOpen(false);
      });
    }
    buttons.forEach((button) => {
      button.addEventListener("click", (event) => {
        config.onSelect(
          button.getAttribute("data-picker-option"),
          button.getAttribute("data-picker-label"),
          event
        );
        setOpen(false);
      });
    });
    document.addEventListener("click", (event) => {
      if (picker.contains(event.target)) return;
      setOpen(false);
    });
    config.onSelect(config.currentValue(), config.currentLabel());
  }

  function findRow(model, effort) {
    return narrativeRows.find((row) => row.model === model && row.effort === effort && row.surface_included)
      || narrativeRows.find((row) => row.model === model && row.effort === effort)
      || null;
  }

  function findSurfaceRow(model, effort) {
    return surfaceRows.find((row) => row.model === model && row.effort === effort)
      || findRow(model, effort);
  }

  function setText(selector, value) {
    document.querySelectorAll(selector).forEach((element) => {
      element.textContent = value;
    });
  }

  function familyBest(inputRows) {
    const map = new Map();
    inputRows.forEach((row) => {
      const current = map.get(row.model_family);
      if (!current || row.answer > current.answer || (row.answer === current.answer && row.cost < current.cost)) {
        map.set(row.model_family, row);
      }
    });
    return Array.from(map.values());
  }

  function cheapestPerFamily(inputRows, threshold, availability) {
    const map = new Map();
    inputRows
      .filter((row) => row.surface_included)
      .filter((row) => Number(row.cost) > 0)
      .filter((row) => row.answer + 1e-9 >= threshold)
      .filter((row) => availability === "all" || row.availability === availability)
      .forEach((row) => {
        const current = map.get(row.model_family);
        if (!current || row.cost < current.cost || (row.cost === current.cost && row.answer > current.answer)) {
          map.set(row.model_family, row);
        }
      });
    return Array.from(map.values()).sort((a, b) => a.cost - b.cost || b.answer - a.answer || a.model_family_label.localeCompare(b.model_family_label));
  }

  function paretoFrontier(inputRows) {
    const sorted = inputRows
      .filter((row) => Number(row.cost) > 0)
      .slice()
      .sort((a, b) => a.cost - b.cost || b.answer - a.answer || a.row_id.localeCompare(b.row_id));
    const frontier = [];
    let bestAnswer = -Infinity;
    sorted.forEach((row) => {
      if (row.answer > bestAnswer + 1e-9) {
        frontier.push(row);
        bestAnswer = row.answer;
      }
    });
    return frontier;
  }

  function tooltipHtml(row) {
    return [
      `<div style="min-width:250px;padding:2px 2px 4px">`,
      `<div style="font-weight:850;font-size:14px;margin-bottom:2px">${escapeHtml(row.model_family_label)}</div>`,
      `<div style="color:#68736d;font-size:12px;margin-bottom:10px">${escapeHtml(row.provider_label)} · ${escapeHtml(displayEffort(row))}</div>`,
      `<div style="display:grid;grid-template-columns:1fr auto;gap:5px 16px;font-size:12px">`,
      `<span>Answer pass^3</span><strong>${formatPct(row.answer)}</strong>`,
      `<span>Estimated run cost</span><strong>${formatCost(row.cost)}</strong>`,
      `<span>Reasoning tokens</span><strong>${numberFormat.format(row.reasoning_tokens)}</strong>`,
      `<span>Weights</span><strong>${escapeHtml(row.availability_label)}</strong>`,
      `</div>`,
      `</div>`
    ].join("");
  }

  function chartBase() {
    return {
      animationDuration: 450,
      animationDurationUpdate: 300,
      textStyle: {
        fontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        color: "#39443f"
      },
      aria: { enabled: true, decal: { show: false } },
      tooltip: {
        trigger: "item",
        confine: true,
        backgroundColor: "rgba(255,253,248,.98)",
        borderColor: "#b9b6aa",
        borderWidth: 1,
        textStyle: { color: "#17201d" },
        extraCssText: "box-shadow:0 16px 42px rgba(23,32,29,.16);border-radius:10px;"
      }
    };
  }

  function mountChart(id, option, updateOptions) {
    const element = document.getElementById(id);
    if (!element) return null;
    if (!window.echarts) {
      element.innerHTML = '<p class="chart-error">Chart library failed to load. The data tables remain available below.</p>';
      return null;
    }
    let chart = chartInstances.get(id);
    if (!chart) {
      chart = window.echarts.init(element, null, { renderer: "canvas", useDirtyRect: true });
      chartInstances.set(id, chart);
    }
    if (updateOptions) {
      chart.setOption(option, updateOptions);
    } else {
      chart.setOption(option, true);
    }
    return chart;
  }

  function lazyRun(elementId, callback, rootMargin) {
    const element = document.getElementById(elementId);
    if (!element) return;
    if (!("IntersectionObserver" in window)) {
      callback();
      return;
    }
    const observer = new IntersectionObserver((entries) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      observer.disconnect();
      callback();
    }, { rootMargin: rootMargin || "600px 0px" });
    observer.observe(element);
  }

  function initBuildStats() {
    document.querySelectorAll("[data-build-stat]").forEach((element) => {
      const key = element.getAttribute("data-build-stat");
      if (build[key] != null) element.textContent = build[key];
    });
    const checksum = document.getElementById("build-checksum");
    if (checksum) checksum.textContent = String(build.source_sha256 || "unknown").slice(0, 12);
  }

  function bindStoryNumbers() {
    const nanoNone = findRow("openai/gpt-5.4-nano", "none");
    const nanoLow = findRow("openai/gpt-5.4-nano", "low");
    const nanoMedium = findRow("openai/gpt-5.4-nano", "medium");
    const nanoHigh = findRow("openai/gpt-5.4-nano", "high");
    const nanoXhigh = findRow("openai/gpt-5.4-nano", "xhigh");
    if (nanoNone) setText('[data-story="nano-none-answer"]', formatPct(nanoNone.answer));
    if (nanoLow) setText('[data-story="nano-low-answer"]', formatPct(nanoLow.answer));
    if (nanoMedium) setText('[data-story="nano-medium-answer"]', formatPct(nanoMedium.answer));
    if (nanoHigh) setText('[data-story="nano-high-answer"]', formatPct(nanoHigh.answer));
    if (nanoXhigh) setText('[data-story="nano-xhigh-answer"]', formatPct(nanoXhigh.answer));

    const best = familyBest(narrativeSurfaceRows);
    const familiesAt95 = best.filter((row) => row.answer >= 95);
    const familiesAt98 = best.filter((row) => row.answer >= 98);
    const strongFamilyIds = new Set(familiesAt95.map((row) => row.model_family));
    const sub80WithinStrongFamilies = narrativeSurfaceRows.filter((row) => strongFamilyIds.has(row.model_family) && row.answer < 80).length;
    setText('[data-story="families-95"]', String(familiesAt95.length));
    setText('[data-story="families-98"]', String(familiesAt98.length));
    setText(
      '[data-story="saturation-contrast"]',
      `${sub80WithinStrongFamilies} lower-setting configurations in those >=95% families still score below 80%, which is why the benchmark is a cost and reasoning tradeoff rather than a one-row leaderboard.`
    );

    const gemmaLow = findRow("google/gemma-4-31b-it", "low");
    const gemmaMedium = findRow("google/gemma-4-31b-it", "medium");
    const gemmaHigh = findRow("google/gemma-4-31b-it", "high");
    if (gemmaLow) setText('[data-story="gemma-low-answer"]', formatPct(gemmaLow.answer));
    if (gemmaMedium) setText('[data-story="gemma-medium-answer"]', formatPct(gemmaMedium.answer));
    if (gemmaLow && gemmaHigh && gemmaMedium) {
      const costs = [gemmaLow.cost, gemmaMedium.cost, gemmaHigh.cost];
      setText('[data-story="gemma-cost-range"]', `${formatCost(Math.min.apply(null, costs))}–${formatCost(Math.max.apply(null, costs))}`);
    }

    const geminiMinimal = findRow("google/gemini-3.5-flash", "minimal");
    const geminiLow = findRow("google/gemini-3.5-flash", "low");
    if (geminiMinimal) setText('[data-story="gemini-minimal-answer"]', formatPct(geminiMinimal.answer));
    if (geminiLow) setText('[data-story="gemini-low-answer"]', formatPct(geminiLow.answer));

    const o1High = findRow("openai/o1", "high");
    if (o1High) setText('[data-story="o1-high-cost"]', formatCost(o1High.cost));
  }

  function renderNanoChart() {
    const effortOrder = ["none", "low", "medium", "high", "xhigh"];
    const dataRows = effortOrder.map((effort) => findRow("openai/gpt-5.4-nano", effort)).filter(Boolean);
    const costs = dataRows.map((row) => Number(row.cost)).filter(Number.isFinite);
    const minCost = Math.min.apply(null, costs);
    const maxCost = Math.max.apply(null, costs);
    const rawCostMax = Number.isFinite(maxCost) ? Math.ceil(maxCost * 100) / 100 : 0.1;
    const costMax = rawCostMax <= 0.1 ? 0.1 : rawCostMax;
    const priceSymbolSize = (row) => {
      const cost = Number(row.cost);
      if (!Number.isFinite(cost) || !Number.isFinite(minCost) || maxCost <= minCost) return 16;
      const normalized = Math.max(0, Math.min(1, (cost - minCost) / (maxCost - minCost)));
      return Math.round(12 + Math.sqrt(normalized) * 18);
    };
    const option = Object.assign(chartBase(), {
      legend: {
        top: 0,
        right: 8,
        itemWidth: 14,
        itemHeight: 10,
        textStyle: { color: "#68736d", fontSize: 11, fontWeight: 700 }
      },
      grid: { left: 62, right: 70, top: 58, bottom: 58 },
      xAxis: {
        type: "category",
        data: dataRows.map((row) => shortEffortLabel(row.effort)),
        boundaryGap: true,
        axisLine: { lineStyle: { color: "#b9b6aa" } },
        axisTick: { show: false },
        axisLabel: { interval: 0, color: "#39443f", fontWeight: 750, margin: 14 }
      },
      yAxis: [
        {
          type: "value",
          min: 30,
          max: 100,
          interval: 10,
          name: "Answer pass^3",
          nameLocation: "middle",
          nameGap: 46,
          nameTextStyle: { color: "#68736d", fontWeight: 750 },
          axisLabel: { formatter: "{value}%", color: "#68736d" },
          splitLine: { lineStyle: { color: "#e4e1d8" } }
        },
        {
          type: "value",
          min: 0,
          max: costMax,
          name: "Run cost",
          nameLocation: "middle",
          nameGap: 48,
          nameTextStyle: { color: "#68736d", fontWeight: 750 },
          interval: costMax <= 0.1 ? 0.02 : undefined,
          axisLabel: { formatter: formatCostAxisCompact, color: "#68736d" },
          splitLine: { show: false }
        }
      ],
      series: [
        {
          name: "Run cost",
          type: "bar",
          yAxisIndex: 1,
          data: dataRows.map((row) => ({ value: row.cost, row })),
          barMaxWidth: 28,
          itemStyle: { color: "rgba(49,87,213,.14)", borderRadius: [6, 6, 0, 0] },
          tooltip: { formatter: (params) => tooltipHtml(params.data.row) }
        },
        {
          name: "Answer pass^3",
          type: "line",
          data: dataRows.map((row) => ({ value: row.answer, row, symbolSize: priceSymbolSize(row) })),
          symbol: "circle",
          lineStyle: { color: "#3157d5", width: 4 },
          itemStyle: { color: "#3157d5", borderColor: "#fff", borderWidth: 3 },
          areaStyle: { color: "rgba(49,87,213,.07)" },
          label: {
            show: true,
            position: "top",
            distance: 10,
            formatter: function (params) {
              return `{score|${formatPct(params.data.row.answer)}}`;
            },
            rich: {
              score: { color: "#17201d", fontSize: 14, fontWeight: 850, lineHeight: 20 }
            }
          },
          tooltip: { formatter: (params) => tooltipHtml(params.data.row) }
        }
      ]
    });
    mountChart("nano-chart", option);
  }

  function renderSaturationChart() {
    const best = familyBest(narrativeSurfaceRows);
    const bands = [
      { label: "Below 70%", test: (value) => value < 70 },
      { label: "70–80%", test: (value) => value >= 70 && value < 80 },
      { label: "80–90%", test: (value) => value >= 80 && value < 90 },
      { label: "90–95%", test: (value) => value >= 90 && value < 95 },
      { label: "95–98%", test: (value) => value >= 95 && value < 98 },
      { label: "98%+", test: (value) => value >= 98 }
    ];
    const bandColors = ["#9aa39f", "#87928e", "#6b7d75", "#4b6d61", "#3157d5", "#10735a"];
    const counts = bands.map((band) => best.filter((row) => band.test(row.answer)).length);
    const option = Object.assign(chartBase(), {
      grid: { left: 54, right: 18, top: 28, bottom: 78 },
      xAxis: {
        type: "category",
        data: bands.map((band) => band.label),
        axisTick: { show: false },
        axisLine: { lineStyle: { color: "#b9b6aa" } },
        axisLabel: {
          interval: 0,
          color: "#68736d",
          fontSize: 10,
          margin: 16,
          rotate: 34,
          align: "right"
        }
      },
      yAxis: {
        type: "value",
        minInterval: 1,
        name: "Model families",
        nameTextStyle: { color: "#68736d", fontWeight: 750 },
        axisLabel: { color: "#68736d" },
        splitLine: { lineStyle: { color: "#e4e1d8" } }
      },
      series: [{
        type: "bar",
        data: counts.map((count, index) => ({
          value: count,
          itemStyle: { color: bandColors[index] }
        })),
        barMaxWidth: 58,
        itemStyle: { borderRadius: [8, 8, 0, 0] },
        label: { show: true, position: "top", color: "#17201d", fontWeight: 850, fontSize: 15 },
        tooltip: {
          formatter: function (params) {
            const band = bands[params.dataIndex];
            const members = best.filter((row) => band.test(row.answer)).sort((a, b) => b.answer - a.answer);
            const sample = members.slice(0, 8).map((row) => escapeHtml(row.model_family_label)).join("<br>");
            return `<strong>${escapeHtml(band.label)}</strong><br>${params.value} model families${sample ? `<div style="margin-top:7px;color:#68736d">${sample}${members.length > 8 ? "<br>…" : ""}</div>` : ""}`;
          }
        }
      }]
    });
    mountChart("saturation-chart", option);
    renderSaturationRoster(best);
  }

  function renderSaturationRoster(bestRows) {
    const roster = document.getElementById("saturation-roster");
    if (!roster) return;
    const visibleLimit = 5;
    const bands = [
      { label: "98%+", test: (value) => value >= 98 },
      { label: "95–98%", test: (value) => value >= 95 && value < 98 }
    ];
    roster.innerHTML = bands.map((band) => {
      const members = bestRows
        .filter((row) => band.test(row.answer))
        .sort((a, b) => b.answer - a.answer || a.cost - b.cost || a.model_family_label.localeCompare(b.model_family_label));
      const chips = members.map((row, index) => [
        `<span class="saturation-chip${index >= visibleLimit ? " saturation-chip-extra" : ""}"${index >= visibleLimit ? " hidden" : ""} title="${escapeHtml(row.model_family_label)} · ${formatPct(row.answer)} · ${formatCost(row.cost)}">`,
        providerIconHtml(row, true),
        `<span>${escapeHtml(row.model_family_label)}</span>`,
        `<small>${formatCost(row.cost)}</small>`,
        `</span>`
      ].join("")).join("");
      const more = members.length > visibleLimit
        ? `<button type="button" class="saturation-more" data-saturation-expand>+${members.length - visibleLimit}</button>`
        : "";
      return [
        `<div class="saturation-band">`,
        `<div><strong>${escapeHtml(band.label)}</strong><span>${members.length} ${members.length === 1 ? "family" : "families"}</span></div>`,
        `<div class="saturation-chip-row">${chips}${more}</div>`,
        `</div>`
      ].join("");
    }).join("");
    roster.querySelectorAll("[data-saturation-expand]").forEach((button) => {
      button.addEventListener("click", () => {
        const row = button.closest(".saturation-chip-row");
        if (!row) return;
        row.querySelectorAll(".saturation-chip-extra").forEach((chip) => {
          chip.hidden = false;
        });
        button.hidden = true;
      });
    });
  }

  const FRONTIER_VIEWS = {
    cost: {
      title: "Cost frontier",
      copy: "The aggregate result is not a winner-take-all ranking. It is a set of increasingly expensive ways to reduce visible failure risk.",
      caption: "All public-surface configurations. Quiet points show the field; the connected points are not beaten on both score and cost. Cheaper rows appear farther right.",
      filter: (row) => row.cost > 0,
      yMin: 10,
      marks: [90, 95, 99]
    },
    open: {
      title: "Open weights",
      copy: "Open-weight candidates occupy meaningful parts of the frontier, including exact-ceiling and near-ceiling rows in this API-pricing snapshot.",
      caption: "Open-weight public-surface configurations at 80%+ answer pass^3. API cost is not self-hosting total cost of ownership.",
      filter: (row) => row.cost > 0 && row.availability === "open_weights" && row.answer >= 80,
      yMin: 75,
      marks: [90, 95, 99]
    },
    "no-reasoning": {
      title: "No reported reasoning",
      copy: "The lower-compute surface is broad and uneven. Zero reported reasoning tokens should be read as a telemetry statement, not proof of zero internal computation.",
      caption: "Rows labeled no reported reasoning or minimal/no reasoning. Provider effort and telemetry conventions differ.",
      filter: (row) => row.cost > 0 && ["no_reported_reasoning", "minimal_no_reasoning"].includes(row.thinking_state),
      yMin: 10,
      marks: [80, 90]
    }
  };

  let activeFrontierView = "cost";
  const frontierState = {
    xAxis: "cost",
    provider: "all",
    providers: [],
    modelFamily: "all",
    effort: "all",
    highlightedFamilies: []
  };

  const DEFAULT_FRONTIER_LABEL_FAMILIES = [
    "openai/gpt-5.5",
    "google/gemma-4-31b-it",
    "openai/gpt-oss-120b",
    "anthropic/claude-opus-4.8",
    "x-ai/grok-build-0.1",
    "google/gemini-3.5-flash",
    "openai/o3",
    "openai/gpt-5.4-mini",
    "openai/gpt-5.4-nano",
    "openai/gpt-5-nano",
    "mistralai/mistral-medium-3.5",
    "mistralai/mistral-nemo",
    "anthropic/claude-sonnet-4.6",
    "anthropic/claude-3-haiku",
    "qwen/qwen3-max"
  ];

  function frontierLabel(row, view, index, frontier, filteredCount) {
    if (filteredCount <= 80) return true;
    if (view === "cost") {
      return index === 0
        || index === frontier.length - 1
        || row.answer >= 98
        || (row.answer >= 95 && row.cost < 0.08)
        || row.row_id === "old-234-openai-gpt-5-4-nano-xhigh"
        || row.row_id === "old-188-openai-gpt-5-nano-low";
    }
    if (view === "open") return row.answer >= 98 || index < 6 || index === frontier.length - 1;
    if (view === "no-reasoning") return index === frontier.length - 1 || row.answer >= 85 || (row.answer >= 75 && row.cost < 0.1);
    return false;
  }

  function frontierModelRows(inputRows, family) {
    return inputRows
      .filter((row) => row.model_family === family)
      .slice()
      .sort((a, b) => a.effort_order - b.effort_order || a.cost - b.cost || b.answer - a.answer);
  }

  function visibleFrontierSelections(inputRows) {
    const visibleFamilies = new Set(inputRows.map((row) => row.model_family));
    const selected = frontierState.highlightedFamilies.filter((family) => visibleFamilies.has(family));
    if (selected.length !== frontierState.highlightedFamilies.length) {
      frontierState.highlightedFamilies = selected;
    }
    return selected;
  }

  function selectedFamilyLabelRows(inputRows, families) {
    return families.map((family) => {
      const familyRows = frontierModelRows(inputRows, family);
      return familyRows
        .slice()
        .sort((a, b) => b.answer - a.answer || a.cost - b.cost || a.effort_order - b.effort_order)[0];
    }).filter(Boolean);
  }

  function addUniqueLabelRow(target, row, selectedFamilies) {
    if (!row || selectedFamilies.has(row.model_family) || target.has(row.row_id)) return;
    target.set(row.row_id, row);
  }

  function bestLabelRow(rowsForLabel) {
    return rowsForLabel
      .slice()
      .sort((a, b) => b.answer - a.answer || a.cost - b.cost || a.effort_order - b.effort_order)[0];
  }

  function defaultFrontierLabelRows(inputRows, selectedFamilies) {
    const selected = new Set(selectedFamilies);
    const labelRows = new Map();
    const byProvider = new Map();

    inputRows.forEach((row) => {
      if (!byProvider.has(row.provider)) byProvider.set(row.provider, []);
      byProvider.get(row.provider).push(row);
    });

    byProvider.forEach((providerRows) => {
      addUniqueLabelRow(labelRows, bestLabelRow(providerRows), selected);
    });

    DEFAULT_FRONTIER_LABEL_FAMILIES.forEach((family) => {
      addUniqueLabelRow(
        labelRows,
        bestLabelRow(inputRows.filter((row) => row.model_family === family)),
        selected
      );
    });

    return Array.from(labelRows.values())
      .sort((a, b) => b.answer - a.answer || a.cost - b.cost || a.model_family_label.localeCompare(b.model_family_label))
      .slice(0, 24);
  }

  function toggleFrontierFamily(family, additive) {
    const selected = new Set(frontierState.highlightedFamilies);
    if (additive) {
      if (selected.has(family)) selected.delete(family);
      else selected.add(family);
    } else if (selected.size === 1 && selected.has(family)) {
      selected.clear();
    } else {
      selected.clear();
      selected.add(family);
    }
    frontierState.highlightedFamilies = Array.from(selected);
  }

  function isAdditiveChartClick(params) {
    const event = params && params.event && (params.event.event || params.event);
    return Boolean(event && (event.altKey || event.shiftKey || event.metaKey || event.ctrlKey));
  }

  function isAdditiveUiEvent(event) {
    return Boolean(event && (event.altKey || event.shiftKey || event.metaKey || event.ctrlKey));
  }

  function shouldShowFamilyConnectors(filteredRows) {
    return activeFrontierProviders().size === 1 && filteredRows.length <= 140;
  }

  function frontierFamilyConnectorSeries(filteredRows, xKey) {
    if (!shouldShowFamilyConnectors(filteredRows)) return [];
    const byFamily = new Map();
    filteredRows.forEach((row) => {
      if (!byFamily.has(row.model_family)) byFamily.set(row.model_family, []);
      byFamily.get(row.model_family).push(row);
    });
    return Array.from(byFamily.values())
      .filter((familyRows) => familyRows.length > 1)
      .map((familyRows) => {
        const sortedRows = familyRows
          .slice()
          .sort((a, b) => a.effort_order - b.effort_order || a[xKey] - b[xKey] || b.answer - a.answer);
        const first = sortedRows[0];
        return {
          id: `frontier-family-trail-${first.model_family}`,
          name: `${first.model_family_label} family trail`,
          type: "line",
          data: sortedRows.map((row) => ({
            value: [row[xKey], row.answer],
            row,
            name: row.model_family_label
          })),
          showSymbol: false,
          silent: true,
          smooth: false,
          lineStyle: {
            color: frontierColor(first),
            width: 1,
            opacity: 0.18
          },
          emphasis: { disabled: true },
          z: 1
        };
      });
  }

  function renderFrontier(viewName) {
    activeFrontierView = viewName || activeFrontierView;
    updateFrontierColorLegend();
    const view = FRONTIER_VIEWS[activeFrontierView];
    const xKey = frontierState.xAxis;
    const filtered = surfaceRows
      .filter(view.filter)
      .filter(rowMatchesFrontierProviders)
      .filter((row) => frontierState.modelFamily === "all" || row.model_family === frontierState.modelFamily)
      .filter((row) => frontierState.effort === "all" || row.effort === frontierState.effort)
      .filter((row) => xKey !== "reasoning_tokens" || row.reasoning_tokens > 0);
    const selectedFamilies = visibleFrontierSelections(filtered);
    const selectedFamilySet = new Set(selectedFamilies);
    const frontier = xKey === "cost" ? paretoFrontier(filtered) : [];
    const familyConnectorSeries = frontierFamilyConnectorSeries(filtered, xKey);
    const labelRows = selectedFamilyLabelRows(filtered, selectedFamilies);
    const defaultLabelRows = defaultFrontierLabelRows(filtered, selectedFamilies);
    const pointData = filtered.map((row) => ({
      value: [row[xKey], row.answer],
      row,
      name: row.model_family_label,
      symbol: row.thinking_state === "thinking_reported" ? "diamond" : "circle",
      symbolSize: row.thinking_state === "thinking_reported" ? 10 : 9,
      itemStyle: {
        color: frontierColor(row),
        opacity: selectedFamilies.length ? (selectedFamilySet.has(row.model_family) ? .86 : .18) : .62,
        borderColor: "#fff",
        borderWidth: 1
      }
    }));
    const frontierData = frontier.map((row, index) => ({
      value: [row[xKey], row.answer],
      row,
      name: row.model_family_label,
      label: { show: frontierLabel(row, activeFrontierView, index, frontier, filtered.length) }
    }));
    const highlightedSeries = selectedFamilies.map((family) => {
      const familyRows = frontierModelRows(filtered, family);
      const color = familyRows.length ? frontierColor(familyRows[0]) : "#3157d5";
      return {
        id: `frontier-highlight-${family}`,
        name: familyRows.length ? familyRows[0].model_family_label : family,
        type: "line",
        data: familyRows.map((row) => ({
          value: [row[xKey], row.answer],
          row,
          name: row.model_family_label,
          label: { show: true }
        })),
        symbol: "circle",
        symbolSize: 14,
        lineStyle: { color, width: 3 },
        itemStyle: { color: "#fff", borderColor: color, borderWidth: 3 },
        label: {
          show: true,
          position: "top",
          distance: 8,
          color: "#17201d",
          fontSize: 10,
          fontWeight: 850,
          formatter: (params) => displayEffort(params.data.row),
          backgroundColor: "rgba(255,253,248,.92)",
          borderRadius: 4,
          padding: [3, 5]
        },
        labelLayout: { hideOverlap: true, moveOverlap: "shiftY" },
        emphasis: { focus: "series" },
        tooltip: { formatter: (params) => tooltipHtml(params.data.row) },
        z: 12
      };
    });
    const selectedLabelData = labelRows.map((row) => ({
      value: [row[xKey], row.answer],
      row,
      name: row.model_family_label,
      label: { show: true }
    }));
    const defaultLabelData = defaultLabelRows.map((row) => ({
      value: [row[xKey], row.answer],
      row,
      name: row.model_family_label,
      label: { show: true }
    }));

    const markLineData = view.marks.map((value) => ({
      yAxis: value,
      name: `${value}%`,
      label: { formatter: `${value}%`, position: "insideEndTop" }
    }));

    const option = Object.assign(chartBase(), {
      animation: false,
      animationDuration: 0,
      animationDurationUpdate: 0,
      grid: { left: 66, right: 40, top: 32, bottom: 70 },
      xAxis: {
        type: "log",
        logBase: 10,
        inverse: xKey === "cost",
        name: xKey === "cost" ? "Estimated cost for the full benchmark run" : "Reported reasoning tokens",
        nameLocation: "middle",
        nameGap: 48,
        nameTextStyle: { color: "#68736d", fontWeight: 750 },
        axisLabel: { color: "#68736d", formatter: xKey === "cost" ? formatCostAxis : formatTokens },
        axisLine: { lineStyle: { color: "#b9b6aa" } },
        splitLine: { show: true, lineStyle: { color: "#e8e5dc" } },
        minorSplitLine: { show: false }
      },
      yAxis: {
        type: "value",
        min: view.yMin,
        max: 100,
        name: "Answer pass^3",
        nameLocation: "middle",
        nameGap: 46,
        nameTextStyle: { color: "#68736d", fontWeight: 750 },
        axisLabel: { color: "#68736d", formatter: "{value}%" },
        splitLine: { lineStyle: { color: "#e8e5dc" } }
      },
      series: [
        ...familyConnectorSeries,
        {
          id: "frontier-configurations",
          name: "Configurations",
          type: "scatter",
          data: pointData,
          emphasis: {
            scale: 1.7,
            itemStyle: { opacity: 1, borderColor: "#17201d", borderWidth: 2 }
          },
          tooltip: { formatter: (params) => tooltipHtml(params.data.row) },
          markLine: {
            animation: false,
            silent: true,
            symbol: "none",
            lineStyle: { color: "#9ca49f", type: "dashed", width: 1 },
            label: { color: "#68736d", fontSize: 10 },
            data: markLineData
          }
        },
        {
          id: "frontier-pareto",
          name: "Pareto frontier",
          type: "line",
          data: frontierData,
          symbol: "circle",
          symbolSize: 13,
          lineStyle: { color: "#17201d", width: 2.5 },
          itemStyle: { color: "#fff", borderColor: "#17201d", borderWidth: 3 },
          label: {
            show: false,
            position: "top",
            distance: 9,
            color: "#17201d",
            fontSize: 10,
            fontWeight: 800,
            formatter: (params) => params.data.row.model_family_label,
            backgroundColor: "rgba(255,253,248,.9)",
            borderRadius: 4,
            padding: [3, 5]
          },
          labelLayout: { hideOverlap: true, moveOverlap: "shiftY" },
          emphasis: { focus: "series" },
          tooltip: { formatter: (params) => tooltipHtml(params.data.row) },
          z: 10
        },
        {
          id: "frontier-default-labels",
          name: "Default model labels",
          type: "scatter",
          silent: true,
          data: defaultLabelData,
          symbolSize: 1,
          itemStyle: { opacity: 0 },
          label: {
            show: true,
            position: "top",
            distance: 9,
            color: "#17201d",
            fontSize: 10,
            fontWeight: 850,
            formatter: (params) => params.data.row.model_family_label,
            backgroundColor: "rgba(255,253,248,.86)",
            borderRadius: 4,
            padding: [3, 5]
          },
          labelLayout: { hideOverlap: true, moveOverlap: "shiftY" },
          tooltip: { formatter: (params) => tooltipHtml(params.data.row) },
          z: 11
        },
        {
          id: "frontier-selected-labels",
          name: "Selected model labels",
          type: "scatter",
          silent: true,
          data: selectedLabelData,
          symbolSize: 1,
          itemStyle: { opacity: 0 },
          label: {
            show: true,
            position: "right",
            distance: 10,
            color: "#17201d",
            fontSize: 11,
            fontWeight: 900,
            formatter: (params) => params.data.row.model_family_label,
            backgroundColor: "rgba(255,253,248,.95)",
            borderRadius: 4,
            padding: [3, 5]
          },
          labelLayout: { hideOverlap: true, moveOverlap: "shiftY" },
          tooltip: { formatter: (params) => tooltipHtml(params.data.row) },
          z: 13
        },
        ...highlightedSeries
      ].filter((series) => (series.name !== "Pareto frontier" || frontierData.length)
        && (series.name !== "Default model labels" || defaultLabelData.length)
        && (series.name !== "Selected model labels" || selectedLabelData.length))
    });
    const chart = mountChart("frontier-chart", option, { notMerge: false, replaceMerge: ["series"], lazyUpdate: true });
    if (chart) {
      chart.dispatchAction({ type: "downplay" });
      chart.off("click");
      chart.on("click", (params) => {
        const row = params && params.data && params.data.row;
        if (!row) return;
        toggleFrontierFamily(row.model_family, isAdditiveChartClick(params));
        renderFrontier(activeFrontierView);
      });
    }

    const title = document.getElementById("frontier-view-title");
    const copy = document.getElementById("frontier-view-copy");
    const caption = document.getElementById("frontier-caption");
    const count = document.getElementById("frontier-row-count");
    const pareto = document.getElementById("frontier-pareto-count");
    const range = document.getElementById("frontier-cost-range");
    const selected = document.getElementById("frontier-selected-series");
    if (title) title.textContent = view.title;
    if (copy) copy.textContent = view.copy;
    if (caption) {
      let captionText = view.caption;
      if (xKey === "reasoning_tokens") {
        captionText = "Rows with reported reasoning tokens only. X-axis shows provider-reported reasoning-token telemetry, not provider-independent compute.";
      }
      if (familyConnectorSeries.length) {
        captionText += " Faint colored lines connect visible settings inside each model family.";
      }
      captionText += " Persistent labels mark frontier or notable rows; click a point to label its model family, or Shift/Alt/Cmd/Ctrl-click to compare several families.";
      caption.textContent = captionText;
    }
    if (count) count.textContent = numberFormat.format(filtered.length);
    if (pareto) pareto.textContent = numberFormat.format(frontier.length);
    if (range && filtered.length) {
      const costs = filtered.map((row) => row.cost);
      range.textContent = `${formatCost(Math.min.apply(null, costs))}–${formatCost(Math.max.apply(null, costs))}`;
    }
    if (range && !filtered.length) range.textContent = "—";
    if (selected) {
      if (labelRows.length) {
        const names = labelRows.map((row) => row.model_family_label);
        selected.textContent = `Selected: ${names.join(", ")}. Colored lines label all visible settings for selected model families.`;
      } else {
        selected.textContent = "Hover or focus a point for details. Click a point to label that model family; Shift/Alt/Cmd/Ctrl-click to compare several families.";
      }
    }

    document.querySelectorAll("[data-frontier-view]").forEach((button) => {
      const active = button.getAttribute("data-frontier-view") === activeFrontierView;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
      button.tabIndex = active ? 0 : -1;
    });
  }

  function setupFrontierTabs() {
    const buttons = Array.from(document.querySelectorAll("[data-frontier-view]"));
    buttons.forEach((button) => {
      button.addEventListener("click", () => renderFrontier(button.getAttribute("data-frontier-view")));
    });
    setupArrowTabs(buttons, (button) => button.click());
    setupFrontierProviderPicker();
    setupFrontierModelPicker();
    setupFrontierEffortPicker();
    setupFrontierProviderStrip();
    const controlBindings = [
      ["frontier-x-axis", "change", (element) => { frontierState.xAxis = element.value; }]
    ];
    controlBindings.forEach(([id, eventName, update]) => {
      const element = document.getElementById(id);
      if (!element) return;
      element.addEventListener(eventName, () => {
        update(element);
        renderFrontier(activeFrontierView);
      });
    });
  }

  function effortOptions() {
    const order = ["none", "minimal", "low", "medium", "high", "xhigh", "max", "reasoning"];
    const present = new Set(narrativeRows.map((row) => row.effort));
    return [
      { value: "all", label: "All efforts" },
      ...order
        .filter((effort) => present.has(effort))
        .map((effort) => ({ value: effort, label: EFFORT_LABELS[effort] || effort }))
    ];
  }

  function modelFamilyOptions() {
    const families = Array.from(new Map(narrativeRows.map((row) => [row.model_family, row])).values())
      .sort((a, b) => a.model_family_label.localeCompare(b.model_family_label))
      .map((row) => ({ value: row.model_family, label: row.model_family_label, row }));
    return [{ value: "all", label: "All models" }, ...families];
  }

  function providerOptions() {
    return [
      { value: "all", label: "All providers" },
      ...Array.from(new Map(rows.map((row) => [row.provider, row.provider_label])).entries())
        .sort((a, b) => a[1].localeCompare(b[1]))
        .map(([value, label]) => ({ value, label }))
    ];
  }

  function providerPickerIcon(option) {
    if (option.value === "all") return '<span class="provider-icon provider-icon-compact provider-icon-all" aria-hidden="true"></span>';
    return providerIconFor(option.value, option.label, true);
  }

  function providerLabelHtml(value, label) {
    return value === "all" ? escapeHtml(label) : `${providerIconFor(value, label, true)}${escapeHtml(label)}`;
  }

  function providerSelectionLabelText() {
    const providers = Array.from(activeFrontierProviders());
    if (!providers.length) return "All providers";
    if (providers.length === 1) {
      return (providerOptions().find((option) => option.value === providers[0]) || {}).label || providers[0];
    }
    return `${providers.length} providers`;
  }

  function providerSelectionLabelHtml() {
    const providers = Array.from(activeFrontierProviders());
    if (!providers.length) return "All providers";
    if (providers.length === 1) {
      const option = providerOptions().find((candidate) => candidate.value === providers[0]);
      return providerLabelHtml(providers[0], option ? option.label : providers[0]);
    }
    return escapeHtml(`${providers.length} providers`);
  }

  function setFrontierProvider(value, label, event) {
    const providers = activeFrontierProviders();
    if (value === "all") {
      providers.clear();
    } else if (isAdditiveUiEvent(event)) {
      if (providers.has(value)) providers.delete(value);
      else providers.add(value);
    } else if (providers.size === 1 && providers.has(value)) {
      providers.clear();
    } else {
      providers.clear();
      providers.add(value);
    }
    frontierState.providers = Array.from(providers);
    frontierState.provider = frontierState.providers.length === 1 ? frontierState.providers[0] : "all";
    const selectedModel = rows.find((row) => row.model_family === frontierState.modelFamily);
    if (selectedModel && providers.size && !providers.has(selectedModel.provider)) {
      setFrontierModel("all", "All models");
    }
    const picker = document.getElementById("frontier-provider-picker");
    const labelElement = document.getElementById("frontier-provider-label");
    if (picker) picker.dataset.value = frontierState.provider;
    if (labelElement) labelElement.innerHTML = providerSelectionLabelHtml();
    document.querySelectorAll("#frontier-provider-picker [data-picker-option]").forEach((button) => {
      const optionValue = button.getAttribute("data-picker-option");
      const active = optionValue === "all" ? !providers.size : providers.has(optionValue);
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
    });
    document.querySelectorAll("[data-frontier-provider-shortcut]").forEach((button) => {
      const active = providers.has(button.getAttribute("data-frontier-provider-shortcut"));
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    updateFrontierColorLegend();
  }

  function setupFrontierProviderPicker() {
    setupSearchablePicker({
      pickerId: "frontier-provider-picker",
      options: providerOptions(),
      iconForOption: providerPickerIcon,
      searchPlaceholder: "Search providers",
      currentValue: () => frontierState.provider,
      currentLabel: providerSelectionLabelText,
      onSelect: (value, label, event) => {
        setFrontierProvider(value, label, event);
        renderFrontier(activeFrontierView);
      }
    });
  }

  function setFrontierModel(value, label) {
    frontierState.modelFamily = value;
    frontierState.highlightedFamilies = value === "all" ? [] : [value];
    const picker = document.getElementById("frontier-model-picker");
    const labelElement = document.getElementById("frontier-model-label");
    if (picker) picker.dataset.value = value;
    if (labelElement) {
      if (value === "all") {
        labelElement.textContent = "All models";
      } else {
        const row = rows.find((candidate) => candidate.model_family === value);
        labelElement.innerHTML = `${row ? providerIconHtml(row, true) : ""}${escapeHtml(label)}`;
      }
    }
    document.querySelectorAll("#frontier-model-picker [data-picker-option]").forEach((button) => {
      const active = button.getAttribute("data-picker-option") === value;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
    });
  }

  function setupFrontierModelPicker() {
    setupSearchablePicker({
      pickerId: "frontier-model-picker",
      options: modelFamilyOptions(),
      iconForOption: (option) => {
        if (option.value === "all") return '<span class="provider-icon provider-icon-compact provider-icon-all" aria-hidden="true"></span>';
        return option.row ? providerIconHtml(option.row, true) : "";
      },
      searchPlaceholder: "Search models",
      currentValue: () => frontierState.modelFamily,
      currentLabel: () => frontierState.modelFamily === "all"
        ? "All models"
        : (rows.find((row) => row.model_family === frontierState.modelFamily) || {}).model_family_label || frontierState.modelFamily,
      onSelect: (value, label) => {
        setFrontierModel(value, label);
        renderFrontier(activeFrontierView);
      }
    });
  }

  function effortLabelHtml(value, label) {
    if (value === "all") return escapeHtml(label);
    return `<span class="effort-dot effort-dot-${escapeHtml(value)}" aria-hidden="true"></span>${escapeHtml(label)}`;
  }

  function setFrontierEffort(value, label) {
    frontierState.effort = value;
    const picker = document.getElementById("frontier-effort-picker");
    const labelElement = document.getElementById("frontier-effort-label");
    if (picker) picker.dataset.value = value;
    if (labelElement) labelElement.innerHTML = effortLabelHtml(value, label);
    document.querySelectorAll("#frontier-effort-picker [data-picker-option]").forEach((button) => {
      const active = button.getAttribute("data-picker-option") === value;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
    });
  }

  function setupFrontierEffortPicker() {
    setupSearchablePicker({
      pickerId: "frontier-effort-picker",
      options: effortOptions(),
      iconForOption: (option) => option.value === "all"
        ? '<span class="provider-icon provider-icon-compact provider-icon-all" aria-hidden="true"></span>'
        : `<span class="effort-dot effort-dot-${escapeHtml(option.value)}" aria-hidden="true"></span>`,
      searchPlaceholder: "Search efforts",
      currentValue: () => frontierState.effort,
      currentLabel: () => frontierState.effort === "all" ? "All efforts" : EFFORT_LABELS[frontierState.effort] || frontierState.effort,
      onSelect: (value, label) => {
        setFrontierEffort(value, label);
        renderFrontier(activeFrontierView);
      }
    });
  }

  function setupFrontierProviderStrip() {
    const container = document.getElementById("frontier-provider-strip");
    if (!container) return;
    const providers = activeFrontierProviders();
    container.innerHTML = providerOptions().filter((option) => option.value !== "all").map((option) => [
      `<button type="button" class="${providers.has(option.value) ? "active" : ""}" data-frontier-provider-shortcut="${escapeHtml(option.value)}" aria-pressed="${providers.has(option.value)}">`,
      providerPickerIcon(option),
      `<span>${escapeHtml(option.label)}</span>`,
      `</button>`
    ].join("")).join("");
    container.querySelectorAll("[data-frontier-provider-shortcut]").forEach((button) => {
      button.addEventListener("click", (event) => {
        const value = button.getAttribute("data-frontier-provider-shortcut");
        const option = providerOptions().find((candidate) => candidate.value === value);
        setFrontierProvider(value, option ? option.label : value, event);
        renderFrontier(activeFrontierView);
      });
    });
  }

  let thresholdState = { threshold: 95, availability: "all" };

  function thresholdRowHtml(row) {
    const weightsClass = row.availability === "open_weights" ? "badge badge-open" : "badge";
    return `<tr>
      <td><div class="model-cell">${providerIconHtml(row)}<span><strong>${escapeHtml(row.model_family_label)}</strong><small>${escapeHtml(row.provider_label)}</small></span></div></td>
      <td>${escapeHtml(displayThresholdEffort(row))}</td>
      <td class="numeric"><strong>${formatPct(row.answer)}</strong></td>
      <td class="numeric"><strong>${formatTableCost(row.cost)}</strong></td>
      <td class="numeric">${numberFormat.format(row.reasoning_tokens)}</td>
      <td><span class="${weightsClass}">${escapeHtml(thresholdAvailabilityLabel(row))}</span></td>
    </tr>`;
  }

  function renderThresholdTable() {
    const dataRows = cheapestPerFamily(narrativeRows, thresholdState.threshold, thresholdState.availability);
    const body = document.getElementById("threshold-table-body");
    if (body) {
      body.innerHTML = dataRows.length
        ? dataRows.map(thresholdRowHtml).join("")
        : '<tr><td colspan="6">No model family clears this threshold under the selected availability filter.</td></tr>';
    }
    const summary = document.getElementById("threshold-summary");
    if (summary) {
      summary.textContent = `${dataRows.length} model ${dataRows.length === 1 ? "family" : "families"} clear ${thresholdState.threshold}%+${thresholdState.availability === "open_weights" ? " with open weights" : ""}.`;
    }
    document.querySelectorAll("[data-threshold]").forEach((button) => {
      const active = Number(button.getAttribute("data-threshold")) === thresholdState.threshold;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    document.querySelectorAll("[data-threshold-weights]").forEach((button) => {
      const active = button.getAttribute("data-threshold-weights") === thresholdState.availability;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
  }

  function setupThresholdControls() {
    document.querySelectorAll("[data-threshold]").forEach((button) => {
      button.addEventListener("click", () => {
        thresholdState.threshold = Number(button.getAttribute("data-threshold"));
        renderThresholdTable();
      });
    });
    document.querySelectorAll("[data-threshold-weights]").forEach((button) => {
      button.addEventListener("click", () => {
        thresholdState.availability = button.getAttribute("data-threshold-weights");
        renderThresholdTable();
      });
    });
  }

  function renderHistoryChart() {
    const sequence = [
      ["openai/gpt-4", "none", "GPT‑4"],
      ["openai/gpt-4o-2024-05-13", "none", "GPT‑4o\nMay 2024"],
      ["openai/gpt-4o-2024-08-06", "none", "GPT‑4o\nAug 2024"],
      ["openai/gpt-4o-2024-11-20", "none", "GPT‑4o\nNov 2024"],
      ["openai/gpt-4.1", "none", "GPT‑4.1"],
      ["openai/gpt-5", "minimal", "GPT‑5 minimal"],
      ["openai/gpt-5.2", "none", "GPT‑5.2 none"],
      ["openai/gpt-5.4", "none", "GPT‑5.4 none"],
      ["openai/gpt-5.5", "none", "GPT‑5.5 none"]
    ];
    const dataRows = sequence.map(([model, effort, label]) => ({ row: findRow(model, effort), label })).filter((item) => item.row);
    const maxCost = Math.max(...dataRows.map((item) => item.row.cost || 0), 0.01);
    const costMax = Math.ceil(maxCost * 20) / 20;
    const option = Object.assign(chartBase(), {
      legend: {
        show: true,
        top: 6,
        right: 16,
        itemWidth: 14,
        itemHeight: 10,
        textStyle: { color: "#68736d", fontSize: 11, fontWeight: 700 }
      },
      grid: { left: 64, right: 82, top: 56, bottom: 86 },
      xAxis: {
        type: "category",
        data: dataRows.map((item) => item.label),
        axisTick: { show: false },
        axisLine: { lineStyle: { color: "#b9b6aa" } },
        axisLabel: {
          interval: 0,
          color: "#68736d",
          fontSize: 10,
          lineHeight: 13,
          margin: 12
        }
      },
      yAxis: [
        {
          type: "value",
          min: 60,
          max: 90,
          interval: 5,
          name: "Answer pass^3",
          nameLocation: "middle",
          nameGap: 42,
          axisLabel: { formatter: "{value}%", color: "#68736d" },
          splitLine: { lineStyle: { color: "#e8e5dc" } }
        },
        {
          type: "value",
          min: 0,
          max: costMax,
          name: "Run cost",
          nameLocation: "middle",
          nameGap: 52,
          axisLabel: { formatter: formatCostAxisCompact, color: "#68736d" },
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false }
        }
      ],
      series: [
        {
          name: "Run cost",
          type: "bar",
          yAxisIndex: 1,
          data: dataRows.map((item) => ({
            value: item.row.cost,
            row: item.row
          })),
          barMaxWidth: 22,
          itemStyle: { color: "rgba(49, 87, 213, .13)", borderRadius: [8, 8, 0, 0] },
          tooltip: { formatter: (params) => tooltipHtml(params.data.row) }
        },
        {
          name: "Answer pass^3",
          type: "line",
          data: dataRows.map((item, index) => ({
            value: item.row.answer,
            row: item.row,
            labelText: formatPct(item.row.answer),
            label: {
              show: true,
              position: index === dataRows.length - 1 ? "right" : "top"
            }
          })),
          symbol: "circle",
          symbolSize: 10,
          lineStyle: { color: "#3157d5", width: 3 },
          itemStyle: { color: "#3157d5", borderColor: "#fff", borderWidth: 2 },
          label: {
            show: true,
            color: "#17201d",
            fontWeight: 820,
            formatter: (params) => params.data.labelText
          },
          labelLayout: { hideOverlap: true, moveOverlap: "shiftY" },
          emphasis: { focus: "series" },
          tooltip: { formatter: (params) => tooltipHtml(params.data.row) }
        }
      ]
    });
    mountChart("history-chart", option);
  }

  function renderGeminiChart() {
    const effortOrder = ["none", "minimal", "low", "medium", "high"];
    const specs = [
      { model: "google/gemini-2.5-flash", label: "Gemini 2.5 Flash", color: "#87928e" },
      { model: "google/gemini-3-flash-preview", label: "Gemini 3 Flash", color: "#3157d5" },
      { model: "google/gemini-3.5-flash", label: "Gemini 3.5 Flash", color: "#10735a" }
    ];
    const series = specs.map((spec) => {
      const dataRows = effortOrder.map((effort) => findRow(spec.model, effort)).filter(Boolean);
      const labelIndexes = progressLabelIndexes(dataRows);
      return {
        name: spec.label,
        type: "line",
        data: dataRows.map((row, index) => progressPoint(row, index, labelIndexes, dataRows)),
        symbol: "circle",
        symbolSize: 12,
        lineStyle: { color: spec.color, width: 3 },
        itemStyle: { color: spec.color, borderColor: "#fff", borderWidth: 2 },
        label: {
          show: false,
          color: spec.color,
          fontWeight: 820,
          formatter: (params) => shortEffortLabel(params.data.row.effort)
        },
        labelLayout: { hideOverlap: true, moveOverlap: "shiftY" },
        emphasis: { focus: "series" },
        tooltip: { formatter: (params) => tooltipHtml(params.data.row) }
      };
    }).filter((seriesItem) => seriesItem.data.length);
    const allProgressRows = series.flatMap((seriesItem) => seriesItem.data.map((point) => point.row));
    const costBounds = logCostBounds(allProgressRows, 0.08);
    const option = Object.assign(chartBase(), {
      legend: { top: 0, right: 8, textStyle: { color: "#68736d" } },
      grid: { left: 64, right: 30, top: 56, bottom: 68 },
      xAxis: {
        type: "log",
        inverse: true,
        min: costBounds.min,
        max: costBounds.max,
        name: "Estimated run cost",
        nameLocation: "middle",
        nameGap: 44,
        axisLabel: { formatter: formatCostAxisCompact, color: "#68736d" },
        splitLine: { lineStyle: { color: "#e8e5dc" } }
      },
      yAxis: {
        type: "value",
        min: 60,
        max: 100,
        interval: 10,
        name: "Answer pass^3",
        nameLocation: "middle",
        nameGap: 44,
        axisLabel: { formatter: "{value}%", color: "#68736d" },
        splitLine: { lineStyle: { color: "#e8e5dc" } }
      },
      series
    });
    mountChart("gemini-chart", option);
  }

  function renderGPT5FamilyChart() {
    const effortOrder = ["none", "minimal", "low", "medium", "high", "xhigh"];
    const specs = [
      { model: "openai/gpt-5", label: "GPT‑5", color: "#87928e" },
      { model: "openai/gpt-5.2", label: "GPT‑5.2", color: "#3157d5" },
      { model: "openai/gpt-5.4", label: "GPT‑5.4", color: "#b6572d" },
      { model: "openai/gpt-5.5", label: "GPT‑5.5", color: "#10735a" }
    ];
    const series = specs.map((spec) => {
      const dataRows = effortOrder
        .map((effort) => findRow(spec.model, effort))
        .filter(Boolean)
        .sort((a, b) => a.cost - b.cost || a.effort_order - b.effort_order);
      const labelIndexes = progressLabelIndexes(dataRows);
      return {
        name: spec.label,
        type: "line",
        data: dataRows.map((row, index) => progressPoint(row, index, labelIndexes, dataRows)),
        symbol: "circle",
        symbolSize: 12,
        lineStyle: { color: spec.color, width: 3 },
        itemStyle: { color: spec.color, borderColor: "#fff", borderWidth: 2 },
        label: {
          show: false,
          color: spec.color,
          fontWeight: 820,
          formatter: (params) => displayEffort(params.data.row)
        },
        labelLayout: { hideOverlap: true, moveOverlap: "shiftY" },
        emphasis: { focus: "series" },
        tooltip: { formatter: (params) => tooltipHtml(params.data.row) }
      };
    }).filter((seriesItem) => seriesItem.data.length);
    const allProgressRows = series.flatMap((seriesItem) => seriesItem.data.map((point) => point.row));
    const costBounds = logCostBounds(allProgressRows, 0.08);
    const option = Object.assign(chartBase(), {
      legend: { top: 0, right: 8, textStyle: { color: "#68736d" } },
      grid: { left: 64, right: 30, top: 58, bottom: 68 },
      xAxis: {
        type: "log",
        inverse: true,
        min: costBounds.min,
        max: costBounds.max,
        name: "Estimated run cost",
        nameLocation: "middle",
        nameGap: 45,
        axisLabel: { formatter: formatCostAxisCompact, color: "#68736d" },
        splitLine: { lineStyle: { color: "#e8e5dc" } }
      },
      yAxis: {
        type: "value",
        min: 60,
        max: 100,
        interval: 5,
        name: "Answer pass^3",
        nameLocation: "middle",
        nameGap: 44,
        axisLabel: { formatter: "{value}%", color: "#68736d" },
        splitLine: { lineStyle: { color: "#e8e5dc" } }
      },
      series
    });
    mountChart("gpt5-family-chart", option);
  }

  function renderOSeriesChart() {
    const modelSpecs = [
      { model: "openai/o1", label: "o1", color: "#b6572d" },
      { model: "openai/o3", label: "o3", color: "#3157d5" },
      { model: "openai/gpt-5.5", label: "GPT‑5.5", color: "#10735a" }
    ];
    const series = modelSpecs.map((spec) => {
      const dataRows = narrativeSurfaceRows
        .filter((row) => row.model === spec.model)
        .sort((a, b) => a.effort_order - b.effort_order);
      const labelIndexes = progressLabelIndexes(dataRows);
      return {
        name: spec.label,
        type: "line",
        data: dataRows.map((row, index) => progressPoint(row, index, labelIndexes, dataRows)),
        symbol: "circle",
        symbolSize: 13,
        lineStyle: { color: spec.color, width: 3 },
        itemStyle: { color: spec.color, borderColor: "#fff", borderWidth: 2 },
        label: {
          show: false,
          color: spec.color,
          fontWeight: 820,
          formatter: (params) => shortEffortLabel(params.data.row.effort)
        },
        labelLayout: { hideOverlap: true, moveOverlap: "shiftY" },
        emphasis: { focus: "series" },
        tooltip: { formatter: (params) => tooltipHtml(params.data.row) }
      };
    });
    const allProgressRows = series.flatMap((seriesItem) => seriesItem.data.map((point) => point.row));
    const costBounds = logCostBounds(allProgressRows, 0.08);
    const option = Object.assign(chartBase(), {
      legend: { top: 0, right: 8, textStyle: { color: "#68736d" } },
      grid: { left: 64, right: 28, top: 54, bottom: 68 },
      xAxis: {
        type: "log",
        inverse: true,
        min: costBounds.min,
        max: costBounds.max,
        name: "Estimated run cost",
        nameLocation: "middle",
        nameGap: 45,
        axisLabel: { formatter: formatCostAxisCompact, color: "#68736d" },
        splitLine: { lineStyle: { color: "#e8e5dc" } }
      },
      yAxis: {
        type: "value",
        min: 80,
        max: 100,
        interval: 5,
        name: "Answer pass^3",
        nameLocation: "middle",
        nameGap: 44,
        axisLabel: { formatter: "{value}%", color: "#68736d" },
        splitLine: { lineStyle: { color: "#e8e5dc" } }
      },
      series
    });
    mountChart("o-series-chart", option);
  }

  function makeCostPointSizer(inputRows, minSize, maxSize) {
    const costs = inputRows
      .map((row) => Number(row.cost))
      .filter((cost) => Number.isFinite(cost) && cost > 0);
    if (!costs.length) return () => minSize;
    const minLog = Math.log10(Math.min(...costs));
    const maxLog = Math.log10(Math.max(...costs));
    if (Math.abs(maxLog - minLog) < 0.0001) return () => (minSize + maxSize) / 2;
    return (row) => {
      const cost = Math.max(Number(row.cost) || 0, 0.000001);
      const t = (Math.log10(cost) - minLog) / (maxLog - minLog);
      return minSize + Math.max(0, Math.min(1, t)) * (maxSize - minSize);
    };
  }

  function progressLabelIndexes(dataRows) {
    if (!dataRows.length) return new Set();
    const selected = new Set();
    let bestIndex = 0;
    let weakestIndex = 0;
    dataRows.forEach((row, index) => {
      if (
        row.answer > dataRows[bestIndex].answer
        || (row.answer === dataRows[bestIndex].answer && row.cost < dataRows[bestIndex].cost)
      ) {
        bestIndex = index;
      }
      if (
        row.answer < dataRows[weakestIndex].answer
        || (row.answer === dataRows[weakestIndex].answer && row.cost > dataRows[weakestIndex].cost)
      ) {
        weakestIndex = index;
      }
    });
    selected.add(weakestIndex);
    if (dataRows[bestIndex].answer < 95) selected.add(bestIndex);
    return selected;
  }

  function progressLabelPosition(row, dataRows) {
    const costs = dataRows
      .map((item) => Number(item.cost))
      .filter((cost) => Number.isFinite(cost) && cost > 0);
    if (costs.length < 2) return "top";
    const minLog = Math.log10(Math.min(...costs));
    const maxLog = Math.log10(Math.max(...costs));
    if (Math.abs(maxLog - minLog) < 0.001) return "top";
    const rowLog = Math.log10(Math.max(Number(row.cost) || 0, 0.000001));
    const t = (rowLog - minLog) / (maxLog - minLog);
    if (t < 0.18) return "left";
    if (t > 0.82) return "right";
    return "top";
  }

  function progressPoint(row, index, labelIndexes, dataRows) {
    return {
      value: [row.cost, row.answer],
      row,
      label: {
        show: labelIndexes.has(index),
        position: progressLabelPosition(row, dataRows)
      }
    };
  }

  function renderClaudeProgressChart(config) {
    const series = config.specs.map((spec) => {
      const dataRows = config.efforts.map((effort) => findSurfaceRow(spec.model, effort)).filter(Boolean);
      const labelIndexes = progressLabelIndexes(dataRows);
      return {
        name: spec.label,
        type: "line",
        connectNulls: false,
        data: dataRows.map((row, index) => progressPoint(row, index, labelIndexes, dataRows)),
        symbol: "circle",
        symbolSize: 11,
        lineStyle: { color: spec.color, width: 3 },
        itemStyle: { color: spec.color, borderColor: "#fff", borderWidth: 2 },
        label: {
          show: false,
          color: spec.color,
          fontWeight: 820,
          formatter: (params) => shortEffortLabel(params.data.row.effort)
        },
        labelLayout: { hideOverlap: true, moveOverlap: "shiftY" },
        emphasis: { focus: "series" },
        tooltip: { formatter: (params) => tooltipHtml(params.data.row) }
      };
    }).filter((seriesItem) => seriesItem.data.some(Boolean));
    const allProgressRows = series.flatMap((seriesItem) => seriesItem.data.map((point) => point.row));
    const costBounds = logCostBounds(allProgressRows, 0.08);
    const option = Object.assign(chartBase(), {
      legend: { top: 0, right: 8, textStyle: { color: "#68736d" } },
      grid: { left: 64, right: 30, top: 56, bottom: 68 },
      xAxis: {
        type: "log",
        inverse: true,
        min: costBounds.min,
        max: costBounds.max,
        name: "Estimated run cost",
        nameLocation: "middle",
        nameGap: 44,
        axisLabel: { formatter: formatCostAxisCompact, color: "#68736d" },
        splitLine: { lineStyle: { color: "#e8e5dc" } }
      },
      yAxis: {
        type: "value",
        min: config.yMin,
        max: config.yMax || 100,
        interval: config.interval || 5,
        name: "Answer pass^3",
        nameLocation: "middle",
        nameGap: 44,
        axisLabel: { formatter: "{value}%", color: "#68736d" },
        splitLine: { lineStyle: { color: "#e8e5dc" } }
      },
      series
    });
    mountChart(config.chartId, option);
  }

  function renderOpusChart() {
    renderClaudeProgressChart({
      chartId: "opus-chart",
      efforts: ["none", "low", "medium", "high", "xhigh", "max"],
      yMin: 80,
      specs: [
        { model: "anthropic/claude-opus-4.5", label: "Opus 4.5", color: "#87928e" },
        { model: "anthropic/claude-opus-4-6", label: "Opus 4.6", color: "#3157d5" },
        { model: "anthropic/claude-opus-4-7", label: "Opus 4.7", color: "#b6572d" },
        { model: "anthropic/claude-opus-4.8", label: "Opus 4.8", color: "#10735a" }
      ]
    });
  }

  function renderSonnetChart() {
    renderClaudeProgressChart({
      chartId: "sonnet-chart",
      efforts: ["none", "low", "medium", "high", "xhigh", "max"],
      yMin: 50,
      specs: [
        { model: "anthropic/claude-sonnet-4", label: "Sonnet 4", color: "#87928e" },
        { model: "anthropic/claude-sonnet-4.5", label: "Sonnet 4.5", color: "#3157d5" },
        { model: "anthropic/claude-sonnet-4.6", label: "Sonnet 4.6", color: "#10735a" },
        { model: "anthropic/claude-sonnet-5", label: "Sonnet 5", color: "#b6572d" }
      ]
    });
  }

  function renderHaikuChart() {
    renderClaudeProgressChart({
      chartId: "haiku-chart",
      efforts: ["none", "low", "medium", "high", "xhigh"],
      yMin: 40,
      specs: [
        { model: "anthropic/claude-3-haiku", label: "Haiku 3", color: "#87928e" },
        { model: "anthropic/claude-3.5-haiku", label: "Haiku 3.5", color: "#3157d5" },
        { model: "anthropic/claude-haiku-4.5", label: "Haiku 4.5", color: "#10735a" }
      ]
    });
  }

  const comparisonRenderers = {
    history: renderHistoryChart,
    "gpt5-family": renderGPT5FamilyChart,
    gemini: renderGeminiChart,
    "o-series": renderOSeriesChart,
    opus: renderOpusChart,
    sonnet: renderSonnetChart,
    haiku: renderHaikuChart
  };

  function activateComparison(name) {
    document.querySelectorAll("[data-comparison]").forEach((button) => {
      const active = button.getAttribute("data-comparison") === name;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
      button.tabIndex = active ? 0 : -1;
    });
    document.querySelectorAll("[data-comparison-panel]").forEach((panel) => {
      const active = panel.getAttribute("data-comparison-panel") === name;
      panel.hidden = !active;
      panel.classList.toggle("active", active);
    });
    window.requestAnimationFrame(() => {
      comparisonRenderers[name]();
      const chartId = {
        history: "history-chart",
        "gpt5-family": "gpt5-family-chart",
        gemini: "gemini-chart",
        "o-series": "o-series-chart",
        opus: "opus-chart",
        sonnet: "sonnet-chart",
        haiku: "haiku-chart"
      }[name];
      const chart = chartInstances.get(chartId);
      if (chart) chart.resize();
    });
  }

  function setupComparisonTabs() {
    const buttons = Array.from(document.querySelectorAll("[data-comparison]"));
    buttons.forEach((button) => {
      button.addEventListener("click", () => activateComparison(button.getAttribute("data-comparison")));
    });
    setupArrowTabs(buttons, (button) => button.click());
  }

  function hydrateComparisonTabs() {
    document.querySelectorAll("[data-comparison][data-comparison-provider]").forEach((button) => {
      if (button.dataset.hydrated === "true") return;
      const label = button.textContent.trim();
      const provider = button.getAttribute("data-comparison-provider");
      const providerLabel = button.getAttribute("data-comparison-provider-label") || provider;
      button.innerHTML = `${providerIconFor(provider, providerLabel, true)}<span>${escapeHtml(label)}</span>`;
      button.dataset.hydrated = "true";
    });
  }

  function setupArrowTabs(buttons, activate) {
    buttons.forEach((button, index) => {
      button.addEventListener("keydown", (event) => {
        let next = null;
        if (event.key === "ArrowRight") next = (index + 1) % buttons.length;
        if (event.key === "ArrowLeft") next = (index - 1 + buttons.length) % buttons.length;
        if (event.key === "Home") next = 0;
        if (event.key === "End") next = buttons.length - 1;
        if (next == null) return;
        event.preventDefault();
        buttons[next].focus();
        activate(buttons[next]);
      });
    });
  }

  const explorerState = {
    search: "",
    modelFamily: "all",
    provider: "all",
    availability: "all",
    effort: "all",
    minScore: 0,
    sortKey: "answer",
    sortDirection: "desc"
  };

  let currentExplorerRows = [];
  let explorerRendered = false;

  function explorerFilteredRows() {
    const needle = explorerState.search.trim().toLowerCase();
    return rows
      .filter((row) => explorerState.modelFamily === "all" || row.model_family === explorerState.modelFamily)
      .filter((row) => explorerState.provider === "all" || row.provider === explorerState.provider)
      .filter((row) => explorerState.availability === "all" || row.availability === explorerState.availability)
      .filter((row) => explorerState.effort === "all" || row.effort === explorerState.effort)
      .filter((row) => row.answer >= explorerState.minScore)
      .filter((row) => {
        if (!needle) return true;
        return [
          row.model_family_label,
          row.model,
          row.label,
          row.provider_label,
          row.configured_effort,
          row.availability_label,
          row.surface_note
        ].join(" ").toLowerCase().includes(needle);
      })
      .sort((a, b) => {
        const key = explorerState.sortKey;
        let av = a[key];
        let bv = b[key];
        if (typeof av === "string") {
          const result = av.localeCompare(String(bv));
          return explorerState.sortDirection === "asc" ? result : -result;
        }
        av = Number(av || 0);
        bv = Number(bv || 0);
        const result = av - bv;
        if (result === 0) return a.model_family_label.localeCompare(b.model_family_label);
        return explorerState.sortDirection === "asc" ? result : -result;
      });
  }

  function explorerRowHtml(row) {
    return `<tr>
      <td><div class="model-cell">${providerIconHtml(row)}<span><strong>${escapeHtml(row.model_family_label)}</strong><small>${escapeHtml(row.model)}</small></span></div></td>
      <td><span class="provider-cell">${providerIconHtml(row, true)}${escapeHtml(row.provider_label)}</span></td>
      <td title="${escapeHtml(displayEffort(row))}">${escapeHtml(displayCompactEffort(row))}</td>
      <td class="numeric"><strong>${formatPct(row.answer)}</strong></td>
      <td class="numeric">${formatTableCost(row.cost)}</td>
      <td class="numeric">${numberFormat.format(row.reasoning_tokens)}</td>
      <td><span class="${row.availability === "open_weights" ? "badge badge-open" : "badge"}" title="${escapeHtml(row.availability_label)}">${escapeHtml(compactAvailabilityLabel(row))}</span></td>
    </tr>`;
  }

  function renderExplorer() {
    explorerRendered = true;
    currentExplorerRows = explorerFilteredRows();
    const body = document.getElementById("explorer-table-body");
    if (body) {
      body.innerHTML = currentExplorerRows.length
        ? currentExplorerRows.map(explorerRowHtml).join("")
        : '<tr><td colspan="7">No aggregate rows match the current filters.</td></tr>';
    }
    const count = document.getElementById("explorer-count");
    if (count) {
      count.textContent = `${numberFormat.format(currentExplorerRows.length)} rows shown.`;
    }
    document.querySelectorAll("[data-sort]").forEach((button) => {
      button.removeAttribute("data-active-sort");
      if (button.getAttribute("data-sort") === explorerState.sortKey) {
        button.setAttribute("data-active-sort", explorerState.sortDirection);
      }
    });
  }

  function setupExplorer() {
    setupExplorerModelPicker();
    setupExplorerProviderPicker();

    const bindings = [
      ["explorer-search", "input", (element) => { explorerState.search = element.value; }],
      ["explorer-weights", "change", (element) => { explorerState.availability = element.value; }],
      ["explorer-effort", "change", (element) => { explorerState.effort = element.value; }],
      ["explorer-min-score", "change", (element) => { explorerState.minScore = Number(element.value); }]
    ];
    bindings.forEach(([id, eventName, update]) => {
      const element = document.getElementById(id);
      if (!element) return;
      element.addEventListener(eventName, () => {
        update(element);
        renderExplorer();
      });
    });

    document.querySelectorAll("[data-sort]").forEach((button) => {
      button.addEventListener("click", () => {
        const key = button.getAttribute("data-sort");
        if (explorerState.sortKey === key) {
          explorerState.sortDirection = explorerState.sortDirection === "asc" ? "desc" : "asc";
        } else {
          explorerState.sortKey = key;
          explorerState.sortDirection = ["model_family_label", "provider_label", "availability_label"].includes(key) ? "asc" : "desc";
        }
        renderExplorer();
      });
    });

    const reset = document.getElementById("explorer-reset");
    if (reset) reset.addEventListener("click", () => {
      Object.assign(explorerState, {
        search: "",
        modelFamily: "all",
        provider: "all",
        availability: "all",
        effort: "all",
        minScore: 0,
        sortKey: "answer",
        sortDirection: "desc"
      });
      document.getElementById("explorer-search").value = "";
      setExplorerModel("all", "All models");
      setExplorerProvider("all", "All providers");
      document.getElementById("explorer-weights").value = "all";
      document.getElementById("explorer-effort").value = "all";
      document.getElementById("explorer-min-score").value = "0";
      renderExplorer();
    });

    lazyRun("explorer", renderExplorer, "900px 0px");
  }

  function setExplorerProvider(value, label) {
    explorerState.provider = value;
    const picker = document.getElementById("explorer-provider-picker");
    const labelElement = document.getElementById("explorer-provider-label");
    if (picker) picker.dataset.value = value;
    if (labelElement) {
      labelElement.innerHTML = value === "all"
        ? "All providers"
        : `${providerIconFor(value, label, true)}${escapeHtml(label)}`;
    }
    document.querySelectorAll("#explorer-provider-picker [data-picker-option]").forEach((button) => {
      const active = button.getAttribute("data-picker-option") === value;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
    });
  }

  function setExplorerModel(value, label) {
    explorerState.modelFamily = value;
    const picker = document.getElementById("explorer-model-picker");
    const labelElement = document.getElementById("explorer-model-label");
    if (picker) picker.dataset.value = value;
    if (labelElement) {
      if (value === "all") {
        labelElement.textContent = "All models";
      } else {
        const row = rows.find((candidate) => candidate.model_family === value);
        labelElement.innerHTML = `${row ? providerIconHtml(row, true) : ""}${escapeHtml(label)}`;
      }
    }
    document.querySelectorAll("#explorer-model-picker [data-picker-option]").forEach((button) => {
      const active = button.getAttribute("data-picker-option") === value;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
    });
  }

  function setupExplorerProviderPicker() {
    setupSearchablePicker({
      pickerId: "explorer-provider-picker",
      options: providerOptions(),
      iconForOption: providerPickerIcon,
      searchPlaceholder: "Search providers",
      currentValue: () => explorerState.provider,
      currentLabel: () => explorerState.provider === "all"
        ? "All providers"
        : (rows.find((row) => row.provider === explorerState.provider) || {}).provider_label || explorerState.provider,
      onSelect: (value, label) => {
        setExplorerProvider(value, label);
        renderExplorer();
      }
    });
  }

  function setupExplorerModelPicker() {
    const families = Array.from(new Map(rows.map((row) => [row.model_family, row])).values())
      .sort((a, b) => a.model_family_label.localeCompare(b.model_family_label))
      .map((row) => ({ value: row.model_family, label: row.model_family_label, row }));
    setupSearchablePicker({
      pickerId: "explorer-model-picker",
      options: [{ value: "all", label: "All models" }, ...families],
      iconForOption: (option) => {
        if (option.value === "all") return '<span class="provider-icon provider-icon-compact provider-icon-all" aria-hidden="true"></span>';
        return option.row ? providerIconHtml(option.row, true) : "";
      },
      searchPlaceholder: "Search models",
      currentValue: () => explorerState.modelFamily,
      currentLabel: () => explorerState.modelFamily === "all"
        ? "All models"
        : (rows.find((row) => row.model_family === explorerState.modelFamily) || {}).model_family_label || explorerState.modelFamily,
      onSelect: (value, label) => {
        setExplorerModel(value, label);
        renderExplorer();
      }
    });
  }

  function init() {
    if (!rows.length) {
      document.body.insertAdjacentHTML("afterbegin", '<div class="data-error">The results data did not load. Re-run <code>python build_site.py</code>.</div>');
      return;
    }
    installProviderIconStyles();
    initBuildStats();
    bindStoryNumbers();
    lazyRun("nano-chart", renderNanoChart);
    renderSaturationChart();
    setupFrontierTabs();
    lazyRun("frontier-chart", () => renderFrontier("cost"));
    setupThresholdControls();
    lazyRun("thresholds", renderThresholdTable, "700px 0px");
    hydrateComparisonTabs();
    setupComparisonTabs();
    lazyRun("comparisons", () => activateComparison("history"), "700px 0px");
    setupExplorer();

    window.addEventListener("resize", () => {
      chartInstances.forEach((chart) => chart.resize());
    }, { passive: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
