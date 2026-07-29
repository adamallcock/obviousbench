# ObviousBench v0.2 Launch Essay Draft

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-07-28`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


Large language models can now do things that would have sounded absurd a few
years ago. They can summarize thousands of pages in seconds, write simple
applications in minutes, and plan entire businesses in hours.

And yet, the same class of system can show up in a flagship product and get
basic arithmetic wrong, make obvious contradictions, or even fail to spell its
own name. These are the kinds of mistakes that can cause users to lose trust in
the technology, the product, and the company behind it.

Larger models and deeper reasoning can reduce these failures, but they also add
cost and latency. Product teams still need to know what visible mistakes become
more likely when they choose a smaller model, cheaper route, or shorter
reasoning budget.

ObviousBench makes that tradeoff visible. It is not a smart-versus-dumb ranking;
it is a way to compare capability, visible brittleness, and cost before those
choices reach users. It uses short, plain prompts with objective answers across
eight families of high-visibility failures: arithmetic, character counting,
spelling transforms, ordering, negation, format compliance, word counting, and
simple constraint awareness.

## Design Decisions

While most benchmarks seek to test harder and harder capabilities,
ObviousBench aims to be saturatable by top models. It is designed to provide
contrast between model sizes and reasoning depths, not to remain unsolved at the
frontier.

ObviousBench also reports `pass^3` because the product question is not only
whether a model got one sampled attempt right. For screenshot-prone failures,
the more useful question is whether the model is reliably unlikely to make the
mistake across repeated attempts.

Finally, pass rates should be read alongside cost, latency, and reasoning
effort. The benchmark is meant to make the tradeoff visible, not to imply that
the most expensive or highest-effort setting is automatically the right product
choice.

## Result Notes To Fold In

The most powerful models saturate or near-saturate the private set, which is
evidence that the questions are solvable rather than ambiguous. At the same
time, small, no-reasoning, or lower-test-time-compute rows still expose a large
visible failure surface.

The most vivid example is `openai/gpt-5-nano`: answer pass^3 moves from 37.5%
at minimal effort to 91.0% at low, 95.1% at medium, and 97.2% at high. That is
the benchmark's product story in miniature: the same model family can look
risky or reliable depending on the reasoning budget.

Several frontier or high-compute rows saturate or nearly saturate the benchmark,
including `openai/gpt-5.5` at medium/xhigh, `openai/gpt-5` at medium/high,
`openai/o3` at medium/high, `google/gemma-4-31b-it` at low/high, and xAI's
`grok-build-0.1` on answer pass^3. Claude Opus 4.8 is near-saturating rather
than perfectly saturated in this snapshot: its best row is max at 99.3% answer
pass^3.

The OpenAI no-reasoning/minimal progression is a useful historical line:
`gpt-4` none is 72.9%, `gpt-4.1` none is 75.7%, the 2024 GPT-4o rows sit around
70.8%-77.1%, `gpt-5` minimal is 72.2%, `gpt-5.2` none is 67.4%, `gpt-5.4` none
is 75.0%, and `gpt-5.5` none is 84.0%. The higher-effort GPT-5-family rows then
move close to or all the way to saturation.

Google's Gemma 4 result is one of the biggest positive surprises. Gemma 4 31B
reaches 100.0% answer and strict pass^3 at both low and high, with the medium
row at 99.3%, and does so at very low estimated run cost in this dataset.

The older OpenAI reasoning models remain surprisingly strong. `o1`, despite its
2024 vintage, reaches 96.5%-98.6% answer pass^3 across low/medium/high, albeit
at very high cost. `o3` from April 2025 reaches 100.0% at medium/high with much
lower cost than `o1`, while `o3-mini` and `o4-mini` also remain competitive.

No-reasoning Grok rows are weak relative to their reasoning rows. `x-ai/grok-4.3`
none is 48.6% answer pass^3, while high and xhigh are 98.6% and 97.9%.
`x-ai/grok-4.20` none is 56.9%, while explicit reasoning rows are around
97.2%-98.6% answer pass^3. The strict scores for some Grok reasoning rows are
much lower because the models often provide the right answer in a non-compliant
format.

Gemini 3.5 Flash is worth calling out carefully. Its low setting already reaches
99.3% answer pass^3 and high reaches 100.0%, while minimal is 83.3%. The low row
does report substantial reasoning-token telemetry in this run, so this should
not be framed as proof that a consumer product is using no reasoning. The safer
claim is that Gemini 3.5 Flash appears to get most of the benefit before the
highest setting on this benchmark.

Pricing changes the interpretation. `o1` is still strong, but its high row costs
about $16.20 for this run. By contrast, several near-saturating rows cost under
$1, and Gemma 4's strongest rows are dramatically cheaper in this snapshot.
ObviousBench should therefore be read as an accuracy/cost/reasoning tradeoff
surface, not a single leaderboard.

Potential regressions should be described as snapshot behavior, not permanent
provider truths. In this run, Opus 4.7 is weaker than Opus 4.6 and Opus 4.8,
while Opus 4.5's explicit budget rows are very strong. That is worth flagging
for follow-up, but not over-interpreting without provider/version context.
