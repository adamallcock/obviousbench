---
title: ObviousBench Launch Essay Working Draft
date: 2026-06-07
type: draft
status: working
---

# ObviousBench Launch Essay Working Draft

This is the human-authored voice layer for the fast public launch. The paper is
the evidence spine; this draft is where Adam's motivation, interpretation, and
plain-language explanation should live.

## How To Use This Draft

Write roughly. Use bullets, fragments, or paragraphs. Do not worry about making
it sound like a paper.

After the rough pass, Codex should:

1. preserve strong personal phrasing where possible;
2. separate factual claims from author interpretation;
3. check factual claims against the frozen release snapshot;
4. produce website copy, a launch essay, README opening copy, and an X/Twitter
   thread.

Claim labels for editing:

- `SUPPORTED`: backed by the paper, report, release config, or local audit.
- `AUTHOR_VIEW`: Adam's interpretation, motivation, or lesson.
- `NEEDS_CHECK`: likely true but needs a source, live URL, or fresh audit.
- `SOFTEN`: too broad, too leaderboard-like, or too easy to misread.

## Fixed Facts For This Launch

Use these unless the frozen snapshot changes.

- Name: ObviousBench.
- Tagline: Catch obvious AI mistakes before users do.
- Release target: `v0.1.0-paper-v1`.
- Dataset split: `paper_v1`.
- Snapshot date: 2026-06-03.
- Questions: 224.
- Model/settings rows: 223.
- Unique model identifiers in the paper abstract: 178.
- Perfect answer-correct rows: 3.
- Rows at or above 95% answer correctness: 80.
- Rows below 80% answer correctness: 40.
- Primary score: answer correctness.
- Secondary diagnostics: format accuracy and strict correctness.
- Scoring: deterministic Python scorers, not an LLM judge.
- Human baseline: not measured in v0.1.
- Intended use: preflight, regression testing, failure inspection, model and
  setting comparison under a frozen snapshot.

Do not claim:

- global model ranking;
- general intelligence measurement;
- measured human accuracy or response time;
- contamination-resistant public leaderboard;
- that one failure proves a model is generally bad;
- that reported reasoning-token telemetry always equals billed hidden thinking.

## Paper In One Page

The paper says ObviousBench is a compact benchmark for short prompts that a
careful human should find easy but that public-facing language models can still
miss. The tasks are intentionally narrow: character counting, spelling
transforms, small arithmetic, ordering, negation, format compliance, word
counting, and constraint awareness.

The benchmark is built around deterministic scoring. The paper separates
answer correctness from format compliance so a model can be credited for
finding the right answer while still being marked as failing the requested
interface.

The core result is a frozen 2026-06-03 snapshot: 224 questions, 223
model/settings rows, and 178 unique model identifiers. Three rows answered
everything correctly, but many model/settings rows still made visible mistakes.
The most concentrated failures were in character counting and spelling
transforms.

The paper's main caution is that this is a narrow, public, frozen snapshot. It
is useful for reliability preflight and regression testing, not for crowning a
permanent universal winner.

## Rough Notes From Adam

### Why I Built This

It is no secret that large language models (LLMs) and agentic systems can complete some tasks that humans could only dream of, such as summarizing thousands of pages of text.

However, at the same time, LLMs suffer inherent limitations in certain areas such as spelling, counting and basic deduction that would otherwise be considered trivial to humans. Unfortunately for the tech companies selling this technology, these expected failures are often embarassing and undermining for their mission.


- thinking (compute) is a general antidote to these simpler problems though not a cure all, and is not suitable in all use cases. Ie the difference between gpt-5.5 nano is x % improvement but at a y% increase in cost


### The Moment The Problem Felt Real

Examples, screenshots, posts, demos, product moments, or recurring annoyances:

For example, Google’s AI Overview being unable to spell ‘Google'.

- https://techcrunch.com/2026/05/27/why-googles-ai-cant-spell-google-or-anything-else/
https://www.makeuseof.com/chatgpt-still-cant-answer-this-simple-question/

### What Surprised Me

-Compute (ie thinking depth) appears to be a clear antidote, suggesting that in many cases, it is an active choice (tradeoff) for companies to allow these failure models
-Model size appears to be highly correlated with scores, suggesting that similarly, model size (or potentially number of active experts) can help make cross connections similar to humans

### What I Think People Get Wrong About Benchmarks

 -
-Benchmarks and model research is a sicence, but ultimately user experience is typically an art, ie vibes. Two models cn score nearly identically on benchmarks but lead to very different user experiences, and ultimately adoption and commercial success
-

### What I Do Not Want ObviousBench To Be

- not a shame board

- not a global ranking

- not a claim that models are bad, substandard or insufficient

-  not a replacement for broad evals.

- The intention of ObviousBench is not to embarrass or humiliate,


### What I Do Want It To Be

Examples: preflight, regression check, failure gallery, product QA signal,
simple reproducible surface.

- The intention of ObviousBench is not to embarrass or humiliate, but to provide a simple, fast way for model developers to get a sense of how likely a given model and thinking setting is going to be susceptible to these types of ‘obvious’ errors and make eyes wide open tradeoffs

- As training does improve the model’s performance in these high visibility areas, get a measure of progress

-


-

### How A Product Team Should Use This

Write a concrete "next Monday" workflow:

- Get a clear sense of how your models and thinking depths perform, and are likely to be a source of potential embarrassment. Make an active tradeoff.
- Measure progress towards improvements and monitor for repression.

### What v0.1 Proves

Keep this modest and evidence-backed:

-

### What v0.1 Does Not Prove

This is where credibility comes from:

-

### What I Want To Improve In v0.2

Possible themes: human baseline, hidden/private splits, stronger
item review, `pass^k` reliability, contribution process, hosted static site,
provider drift policy.

-

## Essay Shape

### Working Title Options

- ObviousBench: Catch obvious AI mistakes before users do
- Where obvious tasks still break language models
- The small AI failures users notice immediately

### Draft Outline

1. Some AI failures are small, but users notice them instantly.
2. I built ObviousBench to make those failures easy to test before launch.
3. The benchmark uses short prompts, objective answers, and deterministic
   scorers.
4. v0.1 freezes 224 questions across 223 model/settings rows.
5. Three rows got everything right; many others still missed visible tasks.
6. The interesting failures were not obscure: letter counts and spelling edits
   were among the hardest families.
7. The point is preflight and regression testing, not shaming models or naming a
   permanent winner.
8. Here is how to inspect the report, run the code, and use it in your own
   model-selection workflow.

## X/Twitter Thread Draft

1. I built ObviousBench to test obvious AI mistakes before users find them.
2. v0.1 is a frozen 224-question snapshot across 223 model/settings rows.
3. The tasks are short and objective: count letters, edit strings, follow simple
   constraints, return the requested format.
4. Three rows answered every question correctly. Forty rows scored below 80%.
5. The hardest families were not exotic: character counting and spelling
   transforms still caught many model/settings rows.
6. ObviousBench uses deterministic Python scorers, not an LLM judge.
7. The goal is not to shame models or declare a permanent universal winner.
8. The goal is preflight: catch visible failures before they reach users.
9. Links: website, GitHub, static report, dataset/card if live.

## Website Opening Draft

ObviousBench catches obvious AI mistakes before users do.

It is a compact reliability benchmark for short, objective prompts: letter
counts, spelling transforms, small arithmetic, ordering, negation, format
compliance, word counting, and simple constraint awareness. v0.1 is a frozen
224-question snapshot across 223 model/settings rows, scored with deterministic
Python scorers and released as a static report.

Use it as a preflight and regression check, not as a permanent global model
ranking.
