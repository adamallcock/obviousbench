# Prompt Policy

ObviousBench v0.1 uses native provider mode:

- No explicit system prompt.
- One user message where possible.
- Temperature `0` or the nearest provider-equivalent deterministic setting.
- No chain-of-thought request.
- No "be careful" instruction.
- No tool calling.
- No browsing.

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

