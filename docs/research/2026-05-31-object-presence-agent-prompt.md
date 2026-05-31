---
title: Object Presence Agent Prompt
date: 2026-05-31
type: research
status: draft
---

# Object Presence Agent Prompt

Use this prompt with another agent to iterate on the object-presence archetype.

```text
We are improving ObviousBench, a benchmark of human-trivial prompts that modern
AI models still sometimes fail. Focus only on "object presence" questions:
tasks where the user must bring, move, carry, drive, or include the object that
is the target of the task, even if another shortcut is tempting.

The canonical example is:

"The car wash is only 100m from my house. Should I walk or drive?"

Correct answer: drive, because the car itself must be at the car wash.

Generate high-quality benchmark candidates in this family.

Hard requirements:

1. The correct answer must be obvious to an ordinary human in under five seconds.
2. The answer must depend on the presence of the target object, not on preference,
   safety, money, weather, legality, or local custom.
3. Avoid examples where the prompt can be reasonably interpreted as asking only
   for information, payment, a booking, or a personal visit.
4. Avoid examples where walking/driving/carrying is impractical, unsafe, illegal,
   or dependent on missing context.
5. Avoid examples where the object is part of the person or impossible to bring.
6. Include tempting distractors. The model should be lured by distance,
   convenience, or generic advice, but the object-presence logic should decide it.
7. Keep prompts short and natural. No trick wording for its own sake.
8. Prefer multiple-choice questions with one unambiguous answer, but include a
   proposed exact-answer version when it works.
9. Include contrast pairs where a similar surface form has a different answer,
   so the benchmark cannot be solved by a shallow template.
10. Do not include copyrighted examples or long quoted text from online sources.

Return structured JSON with this shape:

{
  "candidates": [
    {
      "id_slug": "car-wash-drive",
      "question": "The car wash is 100m away. If I want my car washed, should I walk or drive?",
      "choices": ["Walk", "Drive", "Take a train", "It is impossible"],
      "correct_choice": "Drive",
      "exact_answer": "drive",
      "object_required": "car",
      "tempting_wrong_answer": "walk",
      "why_human_trivial": "The car must be at the car wash to be washed.",
      "why_model_might_fail": "The short distance makes walking sound preferable.",
      "ambiguity_risk": "low",
      "include": true
    }
  ],
  "contrast_pairs": [
    {
      "task_prompt": "The car wash is 100m away. If I want my car washed, should I walk or drive?",
      "task_answer": "drive",
      "information_prompt": "The car wash is 100m away. If I only want to ask their opening hours, should I walk or drive?",
      "information_answer": "walk"
    }
  ],
  "rejected_patterns": [
    {
      "pattern": "phone repair shop next door: do I need my phone?",
      "reason": "Can be interpreted as asking whether the user needs their personal phone for communication or payment, not only repair."
    }
  ]
}

Generate at least 40 candidates and at least 10 contrast pairs.

Preferred domains:

- vehicle service: car wash, mechanic, tire shop, emissions test
- repair/service: bike repair, shoe repair, dry cleaning, tailoring, watch repair
- shipping/copying: post office, returns counter, copy shop, print shop
- appointments requiring artifacts: passport photo retake, document notarization,
  key cutting, prescription refill

Be skeptical. Mark `include: false` for weak or ambiguous candidates and explain
why. The goal is fewer excellent benchmark items, not many plausible but noisy
ones.
```

## Current Design Judgment

Object presence should probably become its own category once it has at least 40
strong items and contrast pairs. Until then, it should remain a prioritized
subfamily under `constraint_awareness` so reporting remains stable.

String manipulation should remain an umbrella category only if it is split into
clear subfamilies. The current dataset already separates `character_count` from
`spelling_transform`; future hard profiles should preserve that distinction
because letter counting and destructive string edits fail for related but not
identical reasons.
