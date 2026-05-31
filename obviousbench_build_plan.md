# ObviousBench Build Plan

**Working title:** ObviousBench  
**Internal thesis:** embarrassment-avoidance benchmark for public-facing LLM failures  
**Public thesis:** a lightweight reliability benchmark for obvious, human-trivial questions that users expect AI systems to answer correctly every time  
**Primary implementation:** Inspect AI  
**Initial dataset format:** local JSONL  
**Initial benchmark mode:** native provider mode, no explicit system prompt  
**Initial scoring:** deterministic Python scorers only  
**Not needed for v0:** Hugging Face hosting, OpenAI Evals adapter, multi-mode prompting, LLM-as-judge, custom leaderboard infrastructure

---

## 1. Executive summary

We are building a benchmark for the class of LLM failures that look absurd, funny, or embarrassing when they are screenshotted in public: counting letters in `strawberry`, simple spelling transforms, basic arithmetic/comparison mistakes, trivial list/counting tasks, format-following failures, and simple constraint-awareness questions.

The benchmark should not be positioned as “LLMs are dumb” or as a gotcha game. The public framing should be:

> **Catch obvious AI mistakes before users do.**

The benchmark should help model providers, AI application companies, and enterprise AI teams identify low-level reliability failures that are disproportionately reputationally damaging because humans view them as trivial.

The first version should be simple:

- Use **Inspect AI** as the canonical runner.
- Use **local JSONL** datasets.
- Use **one standard evaluation path**: native provider mode, no explicit system prompt.
- Use **deterministic scoring**.
- Build an initial seed set from known public/viral examples, then generate clean variants.
- Publish a failure gallery and “obvious failure rate,” not just accuracy.

The benchmark’s unique value is not technical complexity. It is careful curation of examples that are:

1. Human-trivial.
2. Publicly embarrassing when failed.
3. Deterministically scorable or transformable into deterministic variants.
4. Reproducible across models and providers.
5. Easy for non-technical audiences to understand.

---

## 2. Original intention and updated focus

The original intention was to build an LLM benchmark around “easy things” that models should not get wrong, such as:

- How many `r`s are in `strawberry`?
- Basic counting.
- Simple arithmetic.
- Spelling.
- Small string transformations.
- Other tasks humans consider obvious.

The updated focus is sharper:

> Build a benchmark from the kinds of simple failures that become viral screenshots on LinkedIn, X/Twitter, Reddit, Hacker News, blogs, and news articles — failures that make companies look careless even when the underlying model is strong.

This makes the benchmark more marketable and more useful for companies. It becomes a **public-facing AI preflight check** rather than a generic academic benchmark.

---

## 3. Branding strategy

### 3.1 Internal brand

Internally, the project can be described as:

- Embarrassment-avoidance benchmark.
- Screenshot-risk benchmark.
- Public-failure preflight check.
- “Don’t ship the strawberry bug” suite.

This language is useful for understanding the wedge, but it is too negative for public-facing branding.

### 3.2 Public brand options

Preferred public names:

1. **ObviousBench**
2. **ObviousCheck**
3. **Basic Reliability Suite**
4. **Everyday Reliability Benchmark**
5. **AI Preflight Benchmark**
6. **Public-Facing Reliability Check**
7. **CommonSense Microbench**

### 3.3 Recommended name

Use **ObviousBench** for now.

Why:

- Clear.
- Short.
- Memorable.
- Not insulting.
- Communicates the benchmark’s purpose.
- Compatible with both open-source and enterprise messaging.

### 3.4 Tagline options

Primary tagline:

> **Catch obvious AI mistakes before users do.**

Other options:

- “A preflight check for public-facing AI.”
- “Benchmarking the questions users screenshot when models get them wrong.”
- “A reliability test for human-trivial AI tasks.”
- “Small tasks. Big reputational risk.”
- “The benchmark for mistakes that should never ship.”

### 3.5 Tone guidance

Avoid public language like:

- “Embarrassing benchmark”
- “Dumb AI test”
- “AI humiliation”
- “Gotcha benchmark”
- “Shame leaderboard”

Use language like:

- Reliability
- Preflight
- Regression testing
- User trust
- Public-facing QA
- Obvious failure prevention
- Human-trivial checks
- Screenshot risk

Companies are more likely to adopt and publish results if the framing is constructive.

---

## 4. Product / market positioning

### 4.1 Who this is for

Primary users:

- AI product teams.
- Model evaluation teams.
- AI safety/reliability teams.
- Enterprise AI adoption teams.
- Developer relations teams at model providers.
- Independent benchmark watchers and AI commentators.

### 4.2 Why they care

Many AI failures are not technically catastrophic, but they are reputationally damaging because they look ridiculous to normal users. A model can score highly on advanced reasoning benchmarks and still fail a simple question that becomes a viral screenshot.

ObviousBench gives teams a cheap way to ask:

> “Are we about to ship something that users will mock publicly?”

### 4.3 Benchmark positioning

ObviousBench is not intended to replace MMLU, GPQA, SWE-bench, HELM, SimpleQA, or other broad benchmarks. It is a narrow reliability benchmark for human-trivial tasks and public embarrassment avoidance.

The correct analogy is not an academic exam. It is closer to:

- Unit tests.
- Smoke tests.
- Preflight checks.
- Regression tests.
- Public-facing QA.

---

## 5. Evidence and source inspiration

The benchmark should draw inspiration from public examples where LLMs or AI products failed in ways that were easy for humans to recognize.

Known source categories include:

1. **Character-counting failures**  
   The `strawberry` / “how many r’s?” example became a widely discussed demonstration of LLMs failing at letter-level tasks. Public coverage includes TechCrunch, Inc., LinkedIn posts, Reddit threads, OpenAI community posts, and academic work on why LLMs struggle with letter counting.

2. **Simple reasoning / user-intent failures**  
   The viral “car wash” question asks whether someone should walk or drive to a nearby car wash when they want to wash their car. The obvious answer is to drive, because the car must be there. Public discussion has framed this as a test of constraint awareness and intent understanding.

3. **Public AI product blunders**  
   Google AI Overviews went viral for answers such as suggesting glue for pizza or eating rocks. These are not all directly suitable for deterministic benchmark questions, but they are strong evidence that seemingly ridiculous AI outputs can become reputational events.

4. **Existing “easy problems” benchmarks**  
   The “Easy Problems That LLMs Get Wrong” paper and GitHub repository are important prior art for small sets of questions that humans find easy but models fail.

5. **LMentry-like prior art**  
   LMentry is conceptually close: trivial human tasks used as a compact model test. Its infrastructure is stale, but the idea of using elementary tasks as a model unit test is useful precedent.

Important distinction:

> Viral examples should be treated as **leads and archetypes**, not automatically as benchmark items.

Before an item enters the benchmark, it must be cleaned, reproduced, reviewed for ambiguity, and converted into a deterministic or near-deterministic task.

---

## 6. Scope for v0

The v0 benchmark should stay narrow. Do not build a large platform before proving that the item set is interesting.

### 6.1 Include in v0

Include tasks that are:

- Simple.
- Short.
- English-language initially.
- Deterministically scorable.
- Understandable to non-technical users.
- Inspired by known public failure patterns.
- Not dependent on obscure factual knowledge.
- Not reliant on LLM-as-judge scoring.

### 6.2 Exclude from v0

Do not include yet:

- Long-context tasks.
- Subjective writing quality tasks.
- Domain-specific expert knowledge.
- Complex multi-step math.
- LLM-as-judge evaluations.
- Tool-use evaluations.
- Browsing/RAG evaluations.
- Multi-turn agent tasks.
- Safety-policy jailbreak tests.
- Full hallucination/factuality benchmarks.
- A hosted leaderboard.
- Hugging Face dataset hosting.
- OpenAI Evals compatibility.

Those can come later if needed.

---

## 7. Initial task families

The first benchmark should consist of task families, not just a pile of memes. The viral examples provide the seed; the benchmark should generalize them.

### 7.1 Character counting

Inspired by:

- `How many r's are in strawberry?`
- Variants like `raspberry`, `cranberry`, `bookkeeper`, `mississippi`, `committee`, etc.

Example questions:

- How many `r`s are in `strawberry`?
- How many `s`s are in `mississippi`?
- How many times does the letter `e` appear in `bookkeeper`?
- How many lowercase `a`s are in `banana`?
- How many `l`s are in `parallel`?

Expected answer type:

- Integer.

Scorer:

- Extract first integer, compare to target.

Why it matters:

- Extremely easy for humans.
- Highly legible failure.
- Known public example.
- Tests character-level reliability in tokenized models.

### 7.2 Substring and position counting

Example questions:

- How many times does `ana` appear in `banana`?
- What is the third letter of `planet`?
- What is the second-to-last character in `orange`?
- In `committee`, what character appears twice in a row?

Expected answer type:

- Integer or short string.

Scorer:

- Exact integer or exact normalized string.

### 7.3 Spelling transforms

Example questions:

- Spell `strawberry` backwards.
- Remove every `e` from `sentence`.
- Replace every `a` in `banana` with `@`.
- Write `necessary` without the letter `s`.
- Sort the letters in `cab` alphabetically.

Expected answer type:

- Exact string.

Scorer:

- Exact string after whitespace trimming.

### 7.4 Simple arithmetic and numeric comparison

Example questions:

- What is 17 + 8 - 3?
- Which is larger, 9.9 or 9.11?
- What is 6 × 7?
- What is half of 42?
- Sort these numbers from smallest to largest: 12, 3, 9.

Expected answer type:

- Integer, decimal, or normalized list.

Scorer:

- Exact numeric comparison or exact normalized list.

### 7.5 Word and list counting

Example questions:

- How many words are in `The small dog ran home`?
- How many items are in this list: `red, blue, green, yellow`?
- How many words in this sentence start with `s`?
- How many comma-separated values are shown here: `A, B, C, D, E`?

Expected answer type:

- Integer.

Scorer:

- Exact integer.

Important:

- The benchmark must define what counts as a word/item. Avoid ambiguous punctuation at v0.

### 7.6 Alphabetical ordering

Example questions:

- Sort these words alphabetically: pear, apple, banana.
- Which comes first alphabetically: `cat` or `car`?
- Put these letters in alphabetical order: d, a, c, b.

Expected answer type:

- Exact normalized list or short string.

Scorer:

- Normalized list comparison.

### 7.7 Format compliance

Example questions:

- Answer with only `YES` or `NO`: Is 5 greater than 3?
- Return exactly one word: What color is a banana?
- Return a JSON object with one key, `answer`, whose value is `3`.
- Return only the number, with no punctuation: How many letters are in `cat`?

Expected answer type:

- Constrained output.

Scorer:

- Regex, JSON parser, exact string, or word-count checker.

Why it matters:

- Format failures are common in production AI systems.
- Easy to score.
- Useful to enterprise teams.

### 7.8 Negation and exclusion

Example questions:

- Which word does **not** contain the letter `e`: tree, stone, cat, green?
- Which number is **not** even: 4, 8, 11, 20?
- Which item is not a fruit: apple, banana, carrot, pear?

Expected answer type:

- Exact string or multiple-choice letter.

Scorer:

- Exact string or exact choice.

Caution:

- Avoid questions that rely on borderline category membership. Keep v0 examples obvious.

### 7.9 Simple constraint-awareness / “car wash” style questions

Inspired by:

- The viral car-wash prompt: a person wants to wash a car at a car wash a short distance away and asks whether to walk or drive.

Example archetypes:

- I need to wash my car at a car wash 50 meters away. Should I walk or drive?
- I need to take my bicycle to a bike repair shop one block away. Should I walk there without the bike or bring the bike?

Expected answer type:

- Short answer, often multiple-choice.

Scorer:

- Prefer multiple-choice for v0.

Caution:

- These are more semantically subtle than letter-counting tasks. Include them only if the wording is unambiguous and human review confirms near-universal agreement.

### 7.10 Mixed obvious tasks

Example questions:

- Remove every `e` from `green`, then count the remaining letters.
- Sort `9, 2, 5`, then return the second number.
- Count the `r`s in `strawberry`, then add 1.

Expected answer type:

- Integer or exact string.

Use sparingly in v0. Mixed tasks are useful, but the strongest marketing story comes from models failing single-operation tasks.

---

## 8. Benchmark item lifecycle

Every benchmark item should pass through a lifecycle.

### 8.1 Source discovery

Find candidate examples from:

- X/Twitter.
- LinkedIn.
- Reddit.
- Hacker News.
- Blog posts.
- News coverage.
- AI community forums.
- Existing papers and GitHub repos.

Candidate source record:

```json
{
  "source_id": "src_2026_000001",
  "platform": "linkedin",
  "url": "https://...",
  "date_seen": "2026-05-30",
  "author_or_handle": "optional_or_redacted",
  "original_prompt": "How many r's are in strawberry?",
  "claimed_model": "ChatGPT / Claude / Gemini / unknown",
  "claimed_output": "Two",
  "failure_description": "Incorrect letter count",
  "engagement_signal": {
    "likes": null,
    "shares": null,
    "comments": null
  },
  "media_type": "text|screenshot|video|article",
  "rights_status": "link_only_do_not_republish",
  "notes": "Treat as lead; reproduce independently."
}
```

### 8.2 Reproduction

A candidate should not enter the benchmark just because someone posted a screenshot.

Reproduction process:

1. Reconstruct the prompt.
2. Run it against a small model panel.
3. Record raw outputs.
4. Determine whether the failure is still reproducible.
5. Determine whether it is model-specific, provider-specific, or broadly observed.
6. Determine whether the prompt is ambiguous or adversarial.

### 8.3 Generalization

Do not rely only on exact viral prompts, because they may become contaminated or patched.

Instead:

- Preserve the original as a public “seed example.”
- Generate clean variants.
- Include variants in the benchmark.
- Keep some variants private until retirement.

Example:

```text
Seed: How many r's are in strawberry?
Family: character_count
Generated variants:
  How many s's are in mississippi?
  How many e's are in bookkeeper?
  How many r's are in cranberry?
  How many t's are in committee?
```

### 8.4 Review

Each candidate benchmark item should be reviewed for:

- Single correct answer.
- Human-triviality.
- Scorer reliability.
- Ambiguity.
- Reproducibility.
- Copyright/social-media risk.
- Whether it is too famous and likely contaminated.
- Whether variants are better than the original.

### 8.5 Inclusion

Only include items that pass review.

Each included item should have:

- Stable ID.
- Family.
- Subfamily.
- Prompt.
- Target.
- Scorer.
- Source/inspiration metadata.
- Prompt template ID.
- Dataset version.
- Review status.

---

## 9. Data format

Use JSONL as the canonical dataset format.

Example benchmark item:

```json
{
  "id": "obviousbench.char_count.en.v0.public.000001",
  "family": "character_count",
  "subfamily": "single_letter_count",
  "prompt": "Answer the question. Return only the final answer, with no explanation.\n\nQuestion: How many r's are in strawberry?\nAnswer:",
  "question": "How many r's are in strawberry?",
  "target": "3",
  "answer_type": "integer",
  "scorer": "exact_integer_extract_first_v0",
  "split": "public_v0",
  "source_type": "public_archetype",
  "source_refs": [
    "src_strawberry_public_discussion"
  ],
  "human_triviality": "H0",
  "review_status": "reviewed",
  "metadata": {
    "word": "strawberry",
    "character": "r",
    "case_sensitive": false,
    "generated": false,
    "variant_of": null,
    "prompt_template_id": "final_answer_only_v0",
    "system_prompt": null
  }
}
```

Generated variant example:

```json
{
  "id": "obviousbench.char_count.en.v0.public.000137",
  "family": "character_count",
  "subfamily": "single_letter_count",
  "prompt": "Answer the question. Return only the final answer, with no explanation.\n\nQuestion: How many s's are in mississippi?\nAnswer:",
  "question": "How many s's are in mississippi?",
  "target": "4",
  "answer_type": "integer",
  "scorer": "exact_integer_extract_first_v0",
  "split": "public_v0",
  "source_type": "generated_variant",
  "source_refs": [
    "src_strawberry_public_discussion"
  ],
  "human_triviality": "H0",
  "review_status": "reviewed",
  "metadata": {
    "word": "mississippi",
    "character": "s",
    "case_sensitive": false,
    "generated": true,
    "variant_of": "obviousbench.char_count.en.v0.public.000001",
    "generator": "character_count_generator_v0",
    "seed": 98231,
    "prompt_template_id": "final_answer_only_v0",
    "system_prompt": null
  }
}
```

---

## 10. Prompt policy for v0

Do not create many modes initially.

### 10.1 Primary policy

Use **native provider mode**:

- No explicit system prompt.
- Send a single user message where possible.
- Use one canonical user prompt template.
- Use temperature `0` or nearest provider-equivalent deterministic setting.
- Ask for final answer only.
- Do not ask for chain-of-thought.
- Do not add special “be careful” instructions.
- Do not use tool-calling.
- Do not use web browsing.

Canonical prompt:

```text
Answer the question. Return only the final answer, with no explanation.

Question: {question}
Answer:
```

Multiple-choice prompt:

```text
Answer the question. Return only the letter of the correct option.

Question: {question}

A. {choice_a}
B. {choice_b}
C. {choice_c}
D. {choice_d}

Answer:
```

### 10.2 System prompt

For v0:

```text
System prompt: none
```

If a provider or interface requires a system field, use the provider minimum/default behavior and record it in metadata. Do not add `You are a helpful assistant` in v0 unless forced by the interface.

Rationale:

- The goal is to test normal public-facing behavior.
- A custom system prompt introduces another variable.
- The first benchmark should be simple and easy to explain.

### 10.3 What not to do

Do not use prompts like:

```text
Think step by step.
Be very careful.
This is a trick question.
Many models get this wrong.
Count each letter one by one.
```

Those prompts may be useful for later research, but they weaken the v0 benchmark’s core claim.

---

## 11. Scoring policy

### 11.1 Core principle

Use deterministic scorers only.

The benchmark should not depend on another LLM to decide whether an answer is correct.

### 11.2 Scorer types

Initial scorer set:

1. `exact_integer_extract_first_v0`
2. `exact_string_trim_v0`
3. `normalized_string_v0`
4. `normalized_list_v0`
5. `multiple_choice_letter_v0`
6. `regex_match_v0`
7. `json_exact_field_v0`
8. `word_count_v0`

### 11.3 Reasonable extraction

For non-format tasks, accept reasonable answer wrappers.

Example:

- Target: `3`
- Output: `There are 3.`
- Score: correct

For format-compliance tasks, be strict.

Example:

- Instruction: `Return only the number.`
- Target: `3`
- Output: `There are 3.`
- Score: incorrect for format compliance.

### 11.4 Output record

Each model response should produce:

```json
{
  "sample_id": "obviousbench.char_count.en.v0.public.000001",
  "model": "provider/model-name",
  "raw_output": "There are 2 r's.",
  "extracted_answer": "2",
  "target": "3",
  "score": 0,
  "failure_type": "incorrect_count",
  "scorer": "exact_integer_extract_first_v0",
  "prompt_template_id": "final_answer_only_v0",
  "system_prompt": null
}
```

---

## 12. Metrics

### 12.1 Primary metric: Obvious Failure Rate

Report:

```text
Obvious Failure Rate = failures / total questions
```

Prefer this over accuracy in public materials.

Example:

```text
99.2% accuracy = 8 obvious failures per 1,000 questions.
```

This is more memorable and better aligned with the benchmark’s purpose.

### 12.2 Secondary metrics

Include:

- Accuracy.
- Failures per 1,000 questions.
- Per-family failure rate.
- Format failure rate.
- Refusal/non-answer rate.
- Verbose noncompliance rate.
- Public-archetype failures vs generated-variant failures.
- Worst 10 failures by obviousness.

### 12.3 Failure gallery

The failure gallery is as important as the leaderboard.

Each entry should show:

```text
Model:
Task family:
Question:
Expected answer:
Model answer:
Failure type:
Why humans find it obvious:
Source archetype:
```

This is the main marketing asset.

---

## 13. Human-triviality labels

Use a simple labeling system.

```text
H0 = near-universal human-trivial task
H1 = easy but attention-sensitive
H2 = trick-prone or ambiguity-prone
H3 = exclude from benchmark
```

For v0, use internal review.

For v1, add lightweight human validation:

- At least 20–50 human respondents.
- Measure correctness and time-to-answer.
- Retire or rewrite items with unexpected human disagreement.

Headline benchmark should use mostly H0 items.

---

## 14. Inspect AI implementation

### 14.1 Why Inspect AI

Use Inspect AI because it already supports:

- Tasks as dataset + solver + scorer.
- JSON/JSONL datasets.
- Broad model provider compatibility.
- Evaluation logs.
- Running sets of evaluations.
- Custom scorers.

Do not spend v0 effort rebuilding provider adapters.

### 14.2 Repo structure

```text
obviousbench/
  README.md
  pyproject.toml
  LICENSE

  obviousbench/
    __init__.py

    tasks/
      __init__.py
      character_count.py
      spelling_transform.py
      arithmetic.py
      word_count.py
      ordering.py
      format_compliance.py
      negation.py
      constraint_awareness.py

    scorers/
      __init__.py
      exact_integer.py
      exact_string.py
      normalized_list.py
      multiple_choice.py
      regex_match.py
      json_field.py
      failure_types.py

    datasets/
      load.py
      schemas.py

    generators/
      character_count.py
      spelling_transform.py
      arithmetic.py
      variants.py

    analysis/
      summarize_results.py
      build_failure_gallery.py
      leaderboard.py
      export_csv.py

  data/
    source_catalog/
      sources_v0.jsonl
    public_v0/
      character_count.jsonl
      spelling_transform.jsonl
      arithmetic.jsonl
      word_count.jsonl
      ordering.jsonl
      format_compliance.jsonl
      negation.jsonl
      constraint_awareness.jsonl
    calibration_v0/
      smoke_test.jsonl

  configs/
    models_v0.yaml
    run_v0.yaml

  results/
    raw/
    summaries/
    failure_gallery/

  docs/
    methodology.md
    prompt_policy.md
    scoring_policy.md
    source_policy.md
    benchmark_card.md
    branding.md
```

### 14.3 Minimal Inspect task pattern

Example shape:

```python
from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.solver import generate
from obviousbench.scorers.exact_integer import exact_integer_extract_first

@task
def character_count(split: str = "public_v0"):
    return Task(
        dataset=json_dataset(f"data/{split}/character_count.jsonl"),
        solver=[generate()],
        scorer=exact_integer_extract_first(),
    )
```

### 14.4 Model configuration

`configs/models_v0.yaml` should include a small model panel first.

Example target categories:

```yaml
frontier:
  - openai/<current_flagship>
  - anthropic/<current_flagship>
  - google/<current_flagship>
  - grok/<current_flagship>

cost_effective:
  - openai/<cheap_fast_model>
  - anthropic/<cheap_fast_model>
  - google/<cheap_fast_model>

open_or_local:
  - ollama/<local_model>
  - vllm/<open_model>
```

Do not hard-code exact model names in the benchmark spec. Model names change quickly. The run config should capture the actual provider/model string at run time.

---

## 15. Dataset sizing

### 15.1 v0 smoke test

Goal:

```text
50–100 total items
3–5 task families
1–3 models
```

Purpose:

- Validate Inspect integration.
- Validate scorers.
- Validate output logs.
- Validate failure-gallery generation.

### 15.2 v0 public prototype

Goal:

```text
300–500 total items
5–8 task families
5–8 models
```

Recommended starting distribution:

```text
character_count:       100
spelling_transform:     75
arithmetic:             75
word_count/list_count:  75
format_compliance:      75
ordering:               50
negation/exclusion:     50
constraint_awareness:   25
```

### 15.3 v1

Goal:

```text
1,000–2,000 public items
10+ task families
10–20 models
human-triviality validation
private/internal holdout optional
```

---

## 16. Source and rights policy

Because examples may come from LinkedIn, X/Twitter, Reddit, and news coverage, handle sources carefully.

### 16.1 Rules

1. Use public posts as leads.
2. Store source URLs and metadata.
3. Do not republish private information.
4. Do not republish screenshots without permission.
5. Do not depend on screenshots as ground truth.
6. Reproduce prompts independently.
7. Prefer generated variants over copied viral prompts.
8. Keep attribution for source archetypes where appropriate.
9. Avoid naming private individuals in the public benchmark unless they are public authors or news sources.
10. Respect platform terms and API limits.

### 16.2 Source metadata

Source records should include:

- URL.
- Platform.
- Date observed.
- Prompt text.
- Claimed model.
- Claimed answer.
- Correct answer.
- Failure type.
- Engagement signal if available.
- Whether the source can be linked publicly.
- Whether content should be paraphrased only.

---

## 17. Agentic source-mining system concept

This can be built later, but the design should be anticipated now.

### 17.1 Purpose

Build an agentic pipeline that continuously finds, normalizes, reproduces, and proposes new ObviousBench candidate items from public discourse.

### 17.2 Agent roles

#### Agent A: Source discovery agent

Searches for candidate examples using queries like:

```text
"LLM can't count"
"ChatGPT strawberry r"
"Claude simple math fail"
"Gemini spelling fail"
"AI failed simple question"
"car wash test LLM"
"AI embarrassing answer"
"AI overview glue pizza"
"LLM basic reasoning fail"
"how many letters AI wrong"
```

Target platforms:

- X/Twitter.
- LinkedIn.
- Reddit.
- Hacker News.
- YouTube Shorts / TikTok summaries if available through web coverage.
- Blogs.
- News sites.
- AI forums.

Output:

- Source candidate JSONL.

#### Agent B: Prompt extraction agent

Extracts:

- Original prompt.
- Model answer.
- Correct answer.
- Model name if claimed.
- Whether screenshot/video evidence exists.
- Whether the question is deterministic.

Output:

- Normalized source record.

#### Agent C: Reproduction agent

Runs candidate prompts through current model panel.

Output:

- Reproduction report.
- Raw model outputs.
- Reproducibility score.

#### Agent D: Variant generation agent

Creates clean benchmark variants that preserve the failure pattern but avoid overfitting to famous examples.

Output:

- Candidate benchmark samples.

#### Agent E: Scorer synthesis agent

Proposes or validates deterministic scorers.

Output:

- Scorer proposal and test cases.

#### Agent F: Review agent

Flags ambiguity, policy concerns, copyright concerns, and weak candidates.

Output:

- Include / revise / reject decision.

### 17.3 Human review remains required

The agentic system should propose items, not automatically publish them. Final benchmark inclusion should remain human-reviewed.

---

## 18. Failure taxonomy

Use a stable failure taxonomy from the beginning.

Initial failure types:

```text
incorrect_count
incorrect_character_position
wrong_letter_or_substring
string_transform_error
arithmetic_error
numeric_comparison_error
list_count_error
ordering_error
negation_error
format_noncompliance
json_malformed
verbose_noncompliance
refusal_or_safety_overtrigger
non_answer
ambiguous_output
provider_error
timeout
```

For each failure, store:

```json
{
  "failure_type": "incorrect_count",
  "failure_severity": "high_public_legibility",
  "human_obviousness": "H0",
  "screenshot_risk": "high"
}
```

---

## 19. Public reporting

### 19.1 Main report sections

The public report should include:

1. What ObviousBench measures.
2. What it does not measure.
3. Model panel.
4. Dataset summary.
5. Prompt policy.
6. Scoring policy.
7. Obvious failure rate leaderboard.
8. Per-family breakdown.
9. Failure gallery.
10. Methodology and reproducibility instructions.

### 19.2 Primary table

Use this style:

```text
Model | Obvious Failure Rate | Failures / 1,000 | Worst Family | Format Failures | Notes
```

### 19.3 Failure gallery

This should be visual and shareable.

Example:

```text
Question: How many r's are in strawberry?
Expected: 3
Model answered: 2
Family: character counting
Why it matters: humans view this as mechanically obvious.
```

### 19.4 Public tone

Use constructive framing:

```text
These failures are not proof that a model is useless. They are evidence that production systems need preflight checks for obvious public-facing mistakes.
```

---

## 20. Milestones

### Milestone 0: Repository skeleton

Deliverables:

- `pyproject.toml`
- Inspect dependency installed.
- Basic repo structure.
- One task family.
- One scorer.
- One tiny JSONL dataset.
- One successful Inspect run.

Success criterion:

- Can run 10 character-count examples against one model and get a score report.

### Milestone 1: Seed catalog

Deliverables:

- `data/source_catalog/sources_v0.jsonl`
- At least 25 public source leads.
- Source categories tagged.
- At least 5 source archetypes selected.

Success criterion:

- Team can explain where the benchmark examples came from and why they are reputationally relevant.

### Milestone 2: v0 dataset

Deliverables:

- 300–500 benchmark items.
- 5–8 task families.
- Deterministic scorer for every item.
- Human/internal review labels.

Success criterion:

- No item lacks a target, scorer, family, or stable ID.

### Milestone 3: model run

Deliverables:

- Run v0 against 5–8 models.
- Export raw logs.
- Export summary CSV.
- Export per-family breakdown.
- Generate failure gallery.

Success criterion:

- At least some models produce interesting and fair failures.

### Milestone 4: public prototype

Deliverables:

- README.
- Methodology doc.
- Prompt policy.
- Scoring policy.
- Source policy.
- v0 results.
- Failure gallery.

Success criterion:

- Another agent or developer can clone the repo, run the benchmark, and reproduce at least one public result.

### Milestone 5: v1 planning

Deliverables:

- Decision on whether to add private holdout.
- Decision on human validation.
- Decision on public leaderboard.
- Decision on Hugging Face hosting.
- Decision on Inspect Evals registration.

Success criterion:

- v1 scope is based on evidence from v0, not speculation.

---

## 21. Assignments for build agents

### Agent 1: Research and source catalog

Tasks:

- Find public examples of embarrassing/simple LLM failures.
- Create `sources_v0.jsonl`.
- Categorize by failure type.
- Mark whether each source can be linked publicly.
- Identify source archetypes worth converting into benchmark families.

Output:

- Source catalog JSONL.
- Short markdown summary of top archetypes.

### Agent 2: Dataset schema and validation

Tasks:

- Define JSON schema for benchmark items.
- Create validation script.
- Reject missing IDs, targets, scorers, families, and prompt template IDs.
- Validate no duplicate IDs.

Output:

- `obviousbench/datasets/schemas.py`
- `scripts/validate_dataset.py`

### Agent 3: Scorers

Tasks:

- Implement deterministic scorers.
- Add unit tests.
- Handle extraction vs strict scoring.
- Emit failure types.

Output:

- `obviousbench/scorers/`
- Test suite.

### Agent 4: Inspect runner

Tasks:

- Implement Inspect tasks.
- Load JSONL datasets.
- Configure model runs.
- Save logs to stable directories.

Output:

- `obviousbench/tasks/`
- `configs/models_v0.yaml`
- CLI instructions.

### Agent 5: Dataset generation

Tasks:

- Generate variants for character-counting, spelling, arithmetic, ordering, word counting, and format compliance.
- Ensure generator metadata is written.
- Avoid ambiguous examples.

Output:

- `obviousbench/generators/`
- Generated JSONL datasets.

### Agent 6: Analysis and reporting

Tasks:

- Parse Inspect logs.
- Produce summary CSV.
- Produce per-family score table.
- Produce failure gallery markdown.
- Compute obvious failure rate.

Output:

- `obviousbench/analysis/`
- `results/summaries/`
- `results/failure_gallery/`

### Agent 7: Branding and docs

Tasks:

- Write README.
- Write methodology.
- Write scoring policy.
- Write source policy.
- Refine public language to avoid shaming companies.

Output:

- `README.md`
- `docs/benchmark_card.md`
- `docs/methodology.md`
- `docs/branding.md`

---

## 22. Technical non-goals for v0

Do not build these yet:

- Hosted leaderboard.
- User accounts.
- Web dashboard.
- Hugging Face dataset package.
- OpenAI Evals adapter.
- lm-evaluation-harness adapter.
- Lighteval adapter.
- Prompt-robustness mode.
- Deliberate reasoning mode.
- Multi-turn evals.
- LLM-as-judge scoring.
- Tool-use benchmark.
- RAG benchmark.
- Long-context benchmark.

The v0 goal is to prove that a small, well-curated set of obvious failures produces useful signal.

---

## 23. Risks and mitigations

### Risk 1: The benchmark looks like a gotcha test

Mitigation:

- Use constructive branding.
- Include generated variants.
- Avoid trick wording.
- Explain that the benchmark is a preflight check, not a general intelligence test.

### Risk 2: Famous prompts are contaminated

Mitigation:

- Use viral prompts as archetypes.
- Generate variants.
- Track whether an item is a public archetype or generated variant.
- Consider private variants in v1.

### Risk 3: Social screenshots are unreliable

Mitigation:

- Treat public posts as leads.
- Reproduce independently.
- Store raw reproduction outputs.
- Do not rely on screenshots as truth.

### Risk 4: Companies avoid publishing results

Mitigation:

- Frame as reliability/preflight.
- Allow private self-assessment.
- Publish public model runs separately from customer/private runs.
- Avoid “shame” language.

### Risk 5: Items are ambiguous

Mitigation:

- Require deterministic scorer.
- Add human review.
- Reject ambiguous questions.
- Prefer multiple-choice for semantic constraint tasks.

### Risk 6: Benchmark becomes too broad

Mitigation:

- Keep v0 focused on obvious failures.
- Exclude factuality, RAG, agentic tasks, and expert knowledge.
- Maintain a strict inclusion checklist.

---

## 24. Inclusion checklist

A benchmark item may be included only if the answer to all of these is yes:

```text
1. Is there exactly one intended answer?
2. Is the answer human-trivial?
3. Can the answer be scored deterministically?
4. Is the wording non-adversarial?
5. Is the task short?
6. Is the correct answer independent of obscure facts?
7. Is the source/inspiration recorded?
8. Is the item assigned to a task family?
9. Does the item have a stable ID?
10. Has the item passed validation?
```

Reject or revise otherwise.

---

## 25. First build target

The immediate target is:

```text
ObviousBench v0.1
300–500 examples
5–8 task families
5–8 models
Inspect AI runner
Local JSONL datasets
Deterministic scorers
Native provider mode only
No explicit system prompt
Failure gallery
Summary CSV
README + methodology
```

The first public story should be:

> We collected and generalized the simple AI failures that become viral screenshots, then turned them into a deterministic reliability benchmark. Here are the obvious mistakes current models still make.

---

## 26. Suggested README opening

```markdown
# ObviousBench

ObviousBench is a lightweight reliability benchmark for public-facing AI systems. It tests short, human-trivial questions that users expect models to answer correctly every time: letter counting, spelling transforms, simple arithmetic, list counting, ordering, format compliance, and other obvious tasks.

The goal is not to prove that models are bad. The goal is to catch obvious mistakes before users screenshot them.

ObviousBench is built on Inspect AI, uses deterministic scorers, and runs in native provider mode with no explicit system prompt.
```

---

## 27. Source links and prior art

Core framework:

- Inspect AI providers: https://inspect.aisi.org.uk/providers.html
- Inspect AI tasks: https://inspect.aisi.org.uk/tasks.html
- Inspect AI datasets: https://inspect.aisi.org.uk/datasets.html
- Inspect AI scorers: https://inspect.aisi.org.uk/scorers.html
- Inspect AI eval logs: https://inspect.aisi.org.uk/eval-logs.html
- Inspect AI eval sets: https://inspect.aisi.org.uk/eval-sets.html

Public failure examples and discussion:

- TechCrunch, “Why AI can’t spell strawberry”: https://techcrunch.com/2024/08/27/why-ai-cant-spell-strawberry/
- Inc., “How Many R’s in ‘Strawberry’? This AI Doesn’t Know”: https://www.inc.com/kit-eaton/how-many-rs-in-strawberry-this-ai-cant-tell-you.html
- OpenAI community bug report on strawberry counting: https://community.openai.com/t/incorrect-count-of-r-characters-in-the-word-strawberry/829618
- IBM discussion of the viral car-wash challenge: https://www.ibm.com/think/news/viral-car-wash-llm-challenge
- Cybernews coverage of the car-wash test: https://cybernews.com/ai-news/ai-car-wash-test/
- Guardian coverage of Google AI Overviews glue/rocks issue: https://www.theguardian.com/technology/article/2024/may/31/google-ai-summaries-sge-changes
- Business Insider glue pizza coverage: https://www.businessinsider.com/google-ai-glue-pizza-i-tried-it-2024-5
- Wired coverage of Google AI Overview issues: https://www.wired.com/story/google-ai-overview-search-issues
- AP coverage of Google fixes after viral AI Overview errors: https://apnews.com/article/33060569d6cc01abe6c63d21665330d8

Related benchmark/prior art:

- Easy Problems That LLMs Get Wrong paper: https://arxiv.org/abs/2405.19616
- Easy Problems That LLMs Get Wrong GitHub: https://github.com/autogenai/easy-problems-that-llms-get-wrong
- LMentry paper: https://aclanthology.org/2023.findings-acl.666/
- LMentry GitHub: https://github.com/aviaefrat/lmentry
- Why LLMs Struggle to Count Letters paper: https://arxiv.org/abs/2412.18626
- Strawberry Problem / character-level understanding paper: https://arxiv.org/abs/2505.14172

---

## 28. Final recommendation

Build the first version as a focused **ObviousBench v0.1**:

- Inspect AI only.
- Local JSONL only.
- Native provider mode only.
- No explicit system prompt.
- Deterministic scorers only.
- Social/news examples as source archetypes.
- Generated variants for actual benchmark coverage.
- Failure gallery as the main output.
- Public framing around reliability and preflight testing, not shame.

The north-star deliverable is not a platform. It is a clean, credible repo that lets another agent or developer run:

```bash
inspect eval obviousbench/tasks --model <provider/model>
```

…and produce:

```text
Obvious Failure Rate
Per-family breakdown
Raw outputs
Failure gallery
```

The benchmark succeeds if people immediately understand the failures and companies see it as a practical pre-release QA tool rather than an attack.
