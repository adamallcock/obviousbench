"""Canonical ObviousBench prompt rendering."""

FINAL_ANSWER_ONLY_V0 = "final_answer_only_v0"
MULTIPLE_CHOICE_LETTER_V0 = "multiple_choice_letter_v0"
SUPPORTED_PROMPT_TEMPLATE_IDS = frozenset(
    {FINAL_ANSWER_ONLY_V0, MULTIPLE_CHOICE_LETTER_V0}
)


def render_prompt(
    template_id: str,
    question: str,
    choices: list[str] | None = None,
) -> str:
    """Render a canonical v0 prompt."""
    if template_id == FINAL_ANSWER_ONLY_V0:
        return (
            "Answer the question. Return only the final answer, with no explanation.\n\n"
            f"Question: {question}\n"
            "Answer:"
        )

    if template_id == MULTIPLE_CHOICE_LETTER_V0:
        if choices is None or len(choices) != 4:
            raise ValueError("multiple_choice_letter_v0 requires exactly four choices")
        if any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("multiple_choice_letter_v0 choices must be non-empty strings")
        return (
            "Answer the question. Return only the letter of the correct option.\n\n"
            f"Question: {question}\n\n"
            f"A. {choices[0]}\n"
            f"B. {choices[1]}\n"
            f"C. {choices[2]}\n"
            f"D. {choices[3]}\n\n"
            "Answer:"
        )

    raise ValueError(f"Unknown prompt template: {template_id}")

