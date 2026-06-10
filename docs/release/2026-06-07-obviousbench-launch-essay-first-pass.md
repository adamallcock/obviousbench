---
title: ObviousBench Launch Essay First Pass
date: 2026-06-07
type: draft
status: working
---

# ObviousBench Launch Essay First Pass

## Tagline Direction

The current tagline, "Catch obvious AI mistakes before users do," is close but
probably not quite right. The user-facing risk is not that a task is
philosophically "obvious"; it is that some failures are instantly legible,
reputationally costly, and hard for a product team to explain once they appear
in public.

Stronger tagline candidates:

1. Measure the AI failures users notice first.
2. Catch high-visibility AI failures before users do.
3. Preflight user-visible AI failures.
4. Find the AI failures users will screenshot.
5. A deterministic benchmark for user-visible AI brittleness.
6. Small tasks. Objective scores. Failures users see.
7. Measure exposure to visible model failures.

My current recommendation is to separate the serious hero line from the sharper
launch hook:

> Measure the AI failures users notice first.

That is probably the cleanest website tagline. "Catch high-visibility AI
failures before users do" is still a strong X/thread hook because it has more
urgency, but "measure" sounds less adversarial and better matches the benchmark.

## Essay Draft

Large language models can now do things that would have sounded absurd a few
years ago. They can summarize thousands of pages in seconds, write simple
applications in minutes, and plan entire businesses in hours.

And yet, the same class of system can show up in a flagship product and get
basic arithmetic wrong, make an obvious contradiction, or even fail to spell its
own name. These are the kinds of mistakes that can cause users to lose trust in
the technology, the product, and the company behind it.

Many of these failures can be reduced by using larger models or giving models
more time to think, but that is not always computationally or commercially
viable. Product teams making active tradeoffs toward lighter models, cheaper
routes, or shorter thinking settings still have to ask what user-visible
mistakes become more likely. Which of those mistakes are harmless quirks, and
which ones undermine customer trust?

If you are putting a model in front of users, you should be able to ask whether
more reasoning effort reduces that exposure, whether a larger model lowers the
failure rate enough to justify added latency or cost, and whether a cheaper path
is an intentional product tradeoff or an unmeasured risk.

ObviousBench is about visualizing that tradeoff: not between "smart" and
"dumb," but between impressive capability, visible brittleness, and cost. It
uses short, plain prompts with objective answers across eight families of
high-visibility failures: character counting, spelling transforms, small
arithmetic, ordering, negation, format compliance, word counting, and simple
constraint awareness.

A missed prompt here does not prove that a model is generally bad. The better
question is more practical: before a model reaches users, where is it likely to
make visible, reputation-undermining mistakes, and how much does it cost to
reduce that exposure?

## Design Decisions

ObviousBench separates answer correctness from format correctness because those
failures mean different things. A model that gives the right answer inside a
verbose explanation has a format-adherence problem, while a model that gives the
wrong answer has an answer problem. Both can break a product flow, but they
should not be collapsed into the same error.

ObviousBench also reports `pass^3` because the product question is not only
whether a model got one sampled attempt right. For screenshot-prone failures,
the more useful question is whether the model is reliably unlikely to make the
mistake across repeated attempts.

Finally, pass rates should be read alongside cost, latency, and reasoning
effort. The benchmark is meant to make the tradeoff visible, not to imply that
the most expensive or highest-effort setting is automatically the right product
choice.

## Results

The v0.1 release covers 224 short questions across 223 model/settings rows.
Three rows answer all 224 questions correctly. Eighty reach at least 95% answer
correctness. Forty fall below 80%.

The fuller results section should add the strongest quantified evidence once the
final release snapshot is fixed: which families remain most brittle, how much
reasoning effort changes the pass rate, where format failures diverge from
answer failures, and how much improvement costs in latency or tokens.


What ObviousBench shows is that high-visibility failures are measurable. They
can be scored without an LLM judge. They can be tracked by task family, model
setting, cost, and format compliance. Most importantly, they can become a
product-quality conversation before they become a screenshot.

## Notes For Next Revision

- Decide whether to keep "obvious" in the benchmark name while moving the
  tagline toward "high-visibility" or "user-visible" failures.
- Replace the generic compute paragraph with actual quantified deltas once the
  chosen effort/cost result is ready for public use.
- Add one concrete public example only if source/citation and copyright posture
  are clean.
- Keep the internal idea of screenshot-ready exposure, but use public language
  about product quality, visible brittleness, and release risk rather than
  loaded shame language.
