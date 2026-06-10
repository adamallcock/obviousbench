---
title: Paper V1 Human Baseline Form
date: 2026-06-01
type: research
status: draft
---

# Paper V1 Human Baseline Form

Use this form to collect timed human answers for the paper candidate split.
Do not show expected-answer fields or item-card derivations to participants.

Record one CSV row per participant response with these columns:

`item_id,participant_id,answer,seconds,correct,notes`

Total items: 80

## Item 1: obviousbench.char_count.en.v0.public.000040

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many a's are in alphabetical?
Answer:
```

## Item 2: obviousbench.spell.en.v0.public.000002

- Family: `spelling_transform`
- Subfamily: `remove_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Write strawberry without the letter e.
Answer:
```

## Item 3: obviousbench.arith.en.v0.public.000023

- Family: `arithmetic`
- Subfamily: `numeric_comparison`
- Answer type: `decimal`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Which is larger, 3.05 or 3.5?
Answer:
```

## Item 4: obviousbench.word_count.en.v0.public.000045

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: north, south, east, west?
Answer:
```

## Item 5: obviousbench.ordering.en.v0.public.000048

- Family: `ordering`
- Subfamily: `numeric_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these numbers from smallest to largest: -1, 4, 0, -3.
Answer:
```

## Item 6: obviousbench.format.en.v0.public.000047

- Family: `format_compliance`
- Subfamily: `exact_json_schema`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with exactly one key, "answer", whose value is "17".
Answer:
```

## Item 7: obviousbench.negation.en.v0.public.000034

- Family: `negation`
- Subfamily: `without_constraint`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Choose the month that is not in winter in the northern hemisphere: January, July, February, December.
Answer:
```

## Item 8: obviousbench.constraint.en.v0.public.000040

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The engraving kiosk is 50 feet away. If I want my name engraved on my metal water bottle, should I drink from the fountain or bring the bottle?

A. Drink from the fountain
B. Bring the bottle
C. Bring only my name written down
D. It is impossible

Answer:
```

## Item 9: obviousbench.char_count.en.v0.public.000030

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many h's are in alphabetical?
Answer:
```

## Item 10: obviousbench.spell.en.v0.public.000005

- Family: `spelling_transform`
- Subfamily: `remove_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Write necessary without the letter e.
Answer:
```

## Item 11: obviousbench.arith.en.v0.public.000021

- Family: `arithmetic`
- Subfamily: `numeric_comparison`
- Answer type: `decimal`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Which is larger, 9.9 or 9.11?
Answer:
```

## Item 12: obviousbench.word_count.en.v0.public.000033

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: red, blue, green, yellow?
Answer:
```

## Item 13: obviousbench.ordering.en.v0.public.000049

- Family: `ordering`
- Subfamily: `numeric_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these numbers from smallest to largest: 12, 2, 21, 1.
Answer:
```

## Item 14: obviousbench.format.en.v0.public.000048

- Family: `format_compliance`
- Subfamily: `exact_json_schema`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with exactly one key, "answer", whose value is "cat".
Answer:
```

## Item 15: obviousbench.negation.en.v0.public.000033

- Family: `negation`
- Subfamily: `without_constraint`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Choose the shape that does not have corners: square, triangle, circle, rectangle.
Answer:
```

## Item 16: obviousbench.constraint.en.v0.public.000003

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The mechanic is two blocks away. If I want my car's oil changed, should I walk there or drive the car there?

A. Walk there
B. Drive the car there
C. Take the bus there
D. It is impossible

Answer:
```

## Item 17: obviousbench.char_count.en.v0.public.000029

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many g's are in rearrangement?
Answer:
```

## Item 18: obviousbench.spell.en.v0.public.000020

- Family: `spelling_transform`
- Subfamily: `remove_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Write committee without the letter e.
Answer:
```

## Item 19: obviousbench.arith.en.v0.public.000022

- Family: `arithmetic`
- Subfamily: `numeric_comparison`
- Answer type: `decimal`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Which is larger, 7.2 or 7.12?
Answer:
```

## Item 20: obviousbench.word_count.en.v0.public.000070

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: Monday, Tuesday, Wednesday, Thursday?
Answer:
```

## Item 21: obviousbench.ordering.en.v0.public.000046

- Family: `ordering`
- Subfamily: `numeric_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these numbers from smallest to largest: 7, 2, 10, 1.
Answer:
```

## Item 22: obviousbench.format.en.v0.public.000049

- Family: `format_compliance`
- Subfamily: `exact_json_schema`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with exactly one key, "answer", whose value is "north".
Answer:
```

## Item 23: obviousbench.negation.en.v0.public.000031

- Family: `negation`
- Subfamily: `without_constraint`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Choose the word without the letter e: peach, melon, plum, cherry.
Answer:
```

## Item 24: obviousbench.constraint.en.v0.public.000038

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The embroidery booth is at the end of the hall. If I want my baseball cap embroidered, should I go bareheaded or wear or bring the cap?

A. Go bareheaded
B. Wear or bring the cap
C. Bring only the logo idea
D. It is impossible

Answer:
```

## Item 25: obviousbench.char_count.en.v0.public.000017

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many e's are in responsiveness?
Answer:
```

## Item 26: obviousbench.spell.en.v0.public.000022

- Family: `spelling_transform`
- Subfamily: `remove_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Write parallel without the letter e.
Answer:
```

## Item 27: obviousbench.arith.en.v0.public.000024

- Family: `arithmetic`
- Subfamily: `unit_conversion_and_small_calc`
- Answer type: `decimal`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Convert 3 miles to kilometers using 1 mile = 1.609 km.
Answer:
```

## Item 28: obviousbench.word_count.en.v0.public.000015

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: red, blue, green, yellow?
Answer:
```

## Item 29: obviousbench.ordering.en.v0.public.000050

- Family: `ordering`
- Subfamily: `numeric_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these numbers from smallest to largest: 5.5, 5.05, 5.15.
Answer:
```

## Item 30: obviousbench.format.en.v0.public.000046

- Family: `format_compliance`
- Subfamily: `exact_json_schema`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with exactly one key, "answer", whose value is "blue".
Answer:
```

## Item 31: obviousbench.negation.en.v0.public.000035

- Family: `negation`
- Subfamily: `without_constraint`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Choose the number that is not greater than 10: 14, 22, 9, 18.
Answer:
```

## Item 32: obviousbench.constraint.en.v0.public.000036

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The bike shop is around the corner. If my helmet needs a new buckle, should I walk over in a cap or wear or bring the helmet?

A. Walk over in a cap
B. Wear or bring the helmet
C. Bring only the bike
D. It is impossible

Answer:
```

## Item 33: obviousbench.char_count.en.v0.public.000046

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many t's are in accessibility?
Answer:
```

## Item 34: obviousbench.spell.en.v0.public.000008

- Family: `spelling_transform`
- Subfamily: `remove_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Write the word "sentence" after deleting every letter "e".
Answer:
```

## Item 35: obviousbench.arith.en.v0.public.000025

- Family: `arithmetic`
- Subfamily: `unit_conversion_and_small_calc`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many minutes are in 3.5 hours?
Answer:
```

## Item 36: obviousbench.word_count.en.v0.public.000051

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: red, blue, green, yellow?
Answer:
```

## Item 37: obviousbench.ordering.en.v0.public.000047

- Family: `ordering`
- Subfamily: `numeric_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these numbers from smallest to largest: 3.1, 3.01, 3.2.
Answer:
```

## Item 38: obviousbench.format.en.v0.public.000050

- Family: `format_compliance`
- Subfamily: `exact_json_schema`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with exactly one key, "answer", whose value is "true".
Answer:
```

## Item 39: obviousbench.negation.en.v0.public.000032

- Family: `negation`
- Subfamily: `without_constraint`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Choose the item that is not made of metal: spoon, nail, paper, coin.
Answer:
```

## Item 40: obviousbench.constraint.en.v0.public.000032

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The sunglasses repair kiosk is in the mall. If my sunglasses need a new hinge, should I wear regular glasses and leave the sunglasses behind, or bring the sunglasses?

A. Wear regular glasses and leave the sunglasses behind
B. Bring the sunglasses
C. Bring only the case
D. It is impossible

Answer:
```

## Item 41: obviousbench.char_count.en.v0.public.000054

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many g's are in bookkeeping?
Answer:
```

## Item 42: obviousbench.spell.en.v0.public.000028

- Family: `spelling_transform`
- Subfamily: `remove_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Write reliability without the letter e.
Answer:
```

## Item 43: obviousbench.arith.en.v0.public.000028

- Family: `arithmetic`
- Subfamily: `unit_conversion_and_small_calc`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: What is 42 + 29 - 11?
Answer:
```

## Item 44: obviousbench.word_count.en.v0.public.000036

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: north, south, east, west?
Answer:
```

## Item 45: obviousbench.ordering.en.v0.public.000012

- Family: `ordering`
- Subfamily: `alphabetical_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these items alphabetically: cat, car, cap.
Answer:
```

## Item 46: obviousbench.format.en.v0.public.000028

- Family: `format_compliance`
- Subfamily: `json_field`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with one key, "answer", whose value is "3".
Answer:
```

## Item 47: obviousbench.negation.en.v0.public.000018

- Family: `negation`
- Subfamily: `not_choice`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: Which number is not even?

A. 4
B. 8
C. 11
D. 20

Answer:
```

## Item 48: obviousbench.constraint.en.v0.public.000028

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The tailor is next door. If my pants are already pinned for hemming, should I wear shorts there or bring the pinned pants?

A. Wear shorts there
B. Bring the pinned pants
C. Bring only a measuring tape
D. It is impossible

Answer:
```

## Item 49: obviousbench.char_count.en.v0.public.000008

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many r's are in raspberry?
Answer:
```

## Item 50: obviousbench.spell.en.v0.public.000017

- Family: `spelling_transform`
- Subfamily: `remove_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Write orange without the letter e.
Answer:
```

## Item 51: obviousbench.arith.en.v0.public.000027

- Family: `arithmetic`
- Subfamily: `unit_conversion_and_small_calc`
- Answer type: `decimal`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Convert 750 grams to kilograms.
Answer:
```

## Item 52: obviousbench.word_count.en.v0.public.000042

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: red, blue, green, yellow?
Answer:
```

## Item 53: obviousbench.ordering.en.v0.public.000055

- Family: `ordering`
- Subfamily: `alphabetical_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these words alphabetically: blue, black, brown, beige.
Answer:
```

## Item 54: obviousbench.format.en.v0.public.000020

- Family: `format_compliance`
- Subfamily: `json_field`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with one key, "answer", whose value is "3".
Answer:
```

## Item 55: obviousbench.negation.en.v0.public.000020

- Family: `negation`
- Subfamily: `not_choice`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: Which word is not lowercase?

A. cat
B. dog
C. USA
D. sun

Answer:
```

## Item 56: obviousbench.constraint.en.v0.public.000025

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The music shop is next door. If my guitar case needs a new handle, should I carry the guitar without its case or bring the guitar case?

A. Carry the guitar without its case
B. Bring the guitar case
C. Bring only guitar picks
D. It is impossible

Answer:
```

## Item 57: obviousbench.char_count.en.v0.public.000038

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many c's are in coconut?
Answer:
```

## Item 58: obviousbench.spell.en.v0.public.000025

- Family: `spelling_transform`
- Subfamily: `remove_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Write bookkeeper without the letter e.
Answer:
```

## Item 59: obviousbench.arith.en.v0.public.000026

- Family: `arithmetic`
- Subfamily: `unit_conversion_and_small_calc`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: What is 18 multiplied by 7?
Answer:
```

## Item 60: obviousbench.word_count.en.v0.public.000027

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: north, south, east, west?
Answer:
```

## Item 61: obviousbench.ordering.en.v0.public.000025

- Family: `ordering`
- Subfamily: `alphabetical_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these items alphabetically: red, blue, green.
Answer:
```

## Item 62: obviousbench.format.en.v0.public.000008

- Family: `format_compliance`
- Subfamily: `json_field`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with one key, "answer", whose value is "3".
Answer:
```

## Item 63: obviousbench.negation.en.v0.public.000019

- Family: `negation`
- Subfamily: `not_choice`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: Which item is not a fruit?

A. apple
B. banana
C. carrot
D. pear

Answer:
```

## Item 64: obviousbench.constraint.en.v0.public.000033

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The jeweler is across the hall. If my ring needs resizing, should I wear a different ring or wear or bring the ring that needs resizing?

A. Wear a different ring
B. Wear or bring the ring that needs resizing
C. Bring only the box
D. It is impossible

Answer:
```

## Item 65: obviousbench.char_count.en.v0.public.000062

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many p's are in responsiveness?
Answer:
```

## Item 66: obviousbench.spell.en.v0.public.000014

- Family: `spelling_transform`
- Subfamily: `remove_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Write planet without the letter e.
Answer:
```

## Item 67: obviousbench.arith.en.v0.public.000007

- Family: `arithmetic`
- Subfamily: `small_integer_arithmetic`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: What is 9 + 14 - 1?
Answer:
```

## Item 68: obviousbench.word_count.en.v0.public.000024

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: red, blue, green, yellow?
Answer:
```

## Item 69: obviousbench.ordering.en.v0.public.000045

- Family: `ordering`
- Subfamily: `alphabetical_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these items alphabetically: red, blue, green.
Answer:
```

## Item 70: obviousbench.format.en.v0.public.000030

- Family: `format_compliance`
- Subfamily: `json_field`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with one key, "answer", whose value is "3".
Answer:
```

## Item 71: obviousbench.negation.en.v0.public.000012

- Family: `negation`
- Subfamily: `not_choice`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: Which word is not lowercase?

A. cat
B. dog
C. USA
D. sun

Answer:
```

## Item 72: obviousbench.constraint.en.v0.public.000021

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The luggage repair shop is across the street. If my suitcase zipper needs fixing, should I carry my clothes in a tote or roll or bring the suitcase?

A. Carry my clothes in a tote
B. Roll or bring the suitcase
C. Bring only the luggage tag
D. It is impossible

Answer:
```

## Item 73: obviousbench.char_count.en.v0.public.000057

- Family: `character_count`
- Subfamily: `single_letter_count`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many r's are in terracotta?
Answer:
```

## Item 74: obviousbench.spell.en.v0.public.000015

- Family: `spelling_transform`
- Subfamily: `replace_letter`
- Answer type: `string`
- Scorer: `exact_string_trim_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Replace every a in planet with @.
Answer:
```

## Item 75: obviousbench.arith.en.v0.public.000020

- Family: `arithmetic`
- Subfamily: `small_integer_arithmetic`
- Answer type: `integer`
- Scorer: `exact_integer_extract_first_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: What is 22 + 27 - 2?
Answer:
```

## Item 76: obviousbench.word_count.en.v0.public.000052

- Family: `word_count`
- Subfamily: `comma_list_count`
- Answer type: `integer`
- Scorer: `word_count_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many comma-separated values are shown here: A, B, C, D, E?
Answer:
```

## Item 77: obviousbench.ordering.en.v0.public.000036

- Family: `ordering`
- Subfamily: `alphabetical_sort`
- Answer type: `list`
- Scorer: `normalized_list_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Sort these items alphabetically: pear, apple, banana.
Answer:
```

## Item 78: obviousbench.format.en.v0.public.000026

- Family: `format_compliance`
- Subfamily: `json_field`
- Answer type: `json`
- Scorer: `json_exact_field_v0`

Prompt shown to participant:

```text
Answer the question. Return only the final answer, with no explanation.

Question: Return a JSON object with one key, "answer", whose value is "3".
Answer:
```

## Item 79: obviousbench.negation.en.v0.public.000016

- Family: `negation`
- Subfamily: `not_choice`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: Which word is not lowercase?

A. cat
B. dog
C. USA
D. sun

Answer:
```

## Item 80: obviousbench.constraint.en.v0.public.000008

- Family: `constraint_awareness`
- Subfamily: `object_must_be_present`
- Answer type: `multiple_choice`
- Scorer: `multiple_choice_letter_v0`

Prompt shown to participant:

```text
Answer the question. Return only the letter of the correct option.

Question: The window tinting shop is 100m away. If I want the windows on my car tinted, should I walk there or drive the car there?

A. Walk there
B. Drive the car there
C. Bring only the appointment card
D. It is impossible

Answer:
```
