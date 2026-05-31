# ObviousBench Failure Gallery

Curated examples from summarized local runs. Raw Inspect logs and provider payloads are intentionally excluded.

## Example 1: gpt-4.1

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

## Example 2: gpt-4.1

- Model: `openai/gpt-4.1`
- Sample ID: `obviousbench.char_count.en.v0.public.000030`
- Question: How many h's are in alphabetical?
- Expected answer: `1`
- Extracted answer: `2`
- Raw model answer: `2`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 3: gpt-4.1

- Model: `openai/gpt-4.1`
- Sample ID: `obviousbench.char_count.en.v0.public.000046`
- Question: How many t's are in accessibility?
- Expected answer: `1`
- Extracted answer: `2`
- Raw model answer: `2`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 4: gpt-4.1

- Model: `openai/gpt-4.1`
- Sample ID: `obviousbench.char_count.en.v0.public.000054`
- Question: How many g's are in bookkeeping?
- Expected answer: `1`
- Extracted answer: `2`
- Raw model answer: `2`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 5: gpt-4.1

- Model: `openai/gpt-4.1`
- Sample ID: `obviousbench.char_count.en.v0.public.000062`
- Question: How many p's are in responsiveness?
- Expected answer: `1`
- Extracted answer: `0`
- Raw model answer: `0`
- Failure type: `incorrect_count`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: Humans can count the visible letters directly.

## Example 6: gpt-4.1

- Model: `openai/gpt-4.1`
- Sample ID: `obviousbench.constraint.en.v0.public.000004`
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

## Example 7: gpt-4.1

- Model: `openai/gpt-4.1`
- Sample ID: `obviousbench.constraint.en.v0.public.000007`
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

## Example 8: gpt-4.1

- Model: `openai/gpt-4.1`
- Sample ID: `obviousbench.constraint.en.v0.public.000008`
- Question: I need to take my bicycle to a bike repair shop one block away. What should I bring?

A. Only my wallet
B. The bicycle
C. Nothing
D. A suitcase
- Expected answer: `B`
- Extracted answer: `B. THE BICYCLE`
- Raw model answer: `B. The bicycle`
- Failure type: `verbose_noncompliance`
- Human triviality: `H0`
- Source type: `generated_variant`
- Why humans find it obvious: A person can answer this by direct inspection or simple mental work.
