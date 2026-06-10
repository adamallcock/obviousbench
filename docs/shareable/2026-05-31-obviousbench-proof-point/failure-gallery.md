---
title: ObviousBench Failure Gallery
date: 2026-05-31
type: gallery
status: shareable
---

# ObviousBench Failure Gallery

Curated examples from summarized local runs. Raw Inspect logs and provider payloads are intentionally excluded.

## Example 1: GPT-5 Nano minimal

- Model: `openai/gpt-5-nano`
- Sample ID: `obviousbench.arith.en.v0.public.000021`
- Question: Which is larger, 9.9 or 9.11?
- Expected answer: `9.9`
- Extracted answer: `9.11`
- Raw model answer: `9.11`
- Failure type: `wrong_letter_or_substring`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: A person can answer this by direct inspection or simple mental work.

## Example 2: GPT-4.1 none

- Model: `openai/gpt-4.1`
- Sample ID: `obviousbench.char_count.en.v0.public.000029`
- Question: How many g's are in rearrangement?
- Expected answer: `1`
- Extracted answer: `2`
- Raw model answer: `2`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 3: GPT-4o none

- Model: `openai/gpt-4o`
- Sample ID: `obviousbench.char_count.en.v0.public.000029`
- Question: How many g's are in rearrangement?
- Expected answer: `1`
- Extracted answer: `2`
- Raw model answer: `2`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 4: GPT-5.2 none

- Model: `openai/gpt-5.2`
- Sample ID: `obviousbench.char_count.en.v0.public.000008`
- Question: How many r's are in raspberry?
- Expected answer: `3`
- Extracted answer: `2`
- Raw model answer: `2`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 5: GPT-5 low

- Model: `openai/gpt-5`
- Sample ID: `obviousbench.constraint.en.v0.public.000013`
- Question: I need to wash my car at a car wash 50 meters away. Should I walk or drive?

A. Walk
B. Drive
C. Take a train
D. It is impossible
- Expected answer: `B`
- Extracted answer: `A`
- Raw model answer: `A`
- Failure type: `negation_error`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: A person can answer this by direct inspection or simple mental work.

## Example 6: GPT-5.4 none

- Model: `openai/gpt-5.4`
- Sample ID: `obviousbench.char_count.en.v0.public.000017`
- Question: How many e's are in responsiveness?
- Expected answer: `3`
- Extracted answer: `2`
- Raw model answer: `2`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 7: GPT-5.4 low

- Model: `openai/gpt-5.4`
- Sample ID: `obviousbench.char_count.en.v0.public.000054`
- Question: How many g's are in bookkeeping?
- Expected answer: `1`
- Extracted answer: `0`
- Raw model answer: `0`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 8: GPT-5.4 medium

- Model: `openai/gpt-5.4`
- Sample ID: `obviousbench.spell.en.v0.public.000002`
- Question: Write strawberry without the letter e.
- Expected answer: `strawbrry`
- Extracted answer: `strawberry`
- Raw model answer: `strawberry`
- Failure type: `wrong_letter_or_substring`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: A person can answer this by direct inspection or simple mental work.

## Example 9: GPT-5.4 high

- Model: `openai/gpt-5.4`
- Sample ID: `obviousbench.spell.en.v0.public.000022`
- Question: Write parallel without the letter e.
- Expected answer: `paralll`
- Extracted answer: `parallel`
- Raw model answer: `parallel`
- Failure type: `wrong_letter_or_substring`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: A person can answer this by direct inspection or simple mental work.

## Example 10: GPT-5.5 none

- Model: `openai/gpt-5.5`
- Sample ID: `obviousbench.char_count.en.v0.public.000008`
- Question: How many r's are in raspberry?
- Expected answer: `3`
- Extracted answer: `2`
- Raw model answer: `2`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 11: Claude Haiku 4.5

- Model: `anthropic/claude-haiku-4-5`
- Sample ID: `obviousbench.char_count.en.v0.public.000017`
- Question: How many e's are in responsiveness?
- Expected answer: `3`
- Extracted answer: `4`
- Raw model answer: `4`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 12: Claude Sonnet 4.6

- Model: `anthropic/claude-sonnet-4-6`
- Sample ID: `obviousbench.char_count.en.v0.public.000029`
- Question: How many g's are in rearrangement?
- Expected answer: `1`
- Extracted answer: `3`
- Raw model answer: `3`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.
