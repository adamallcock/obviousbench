"""Inspect AI task registration imports."""

from obviousbench.providers import (
    aion,
    anthropic_opus5,
    bedrock_flex,
    celeris,
    cohere,
    gemini_flex,
    longcat,
    zai,
)
from obviousbench.tasks import (
    arithmetic,
    barrage,
    character_count,
    constraint_awareness,
    format_compliance,
    negation,
    ordering,
    smoke,
    spelling_transform,
    word_count,
)

__all__ = [
    "aion",
    "anthropic_opus5",
    "arithmetic",
    "barrage",
    "bedrock_flex",
    "celeris",
    "character_count",
    "cohere",
    "constraint_awareness",
    "format_compliance",
    "gemini_flex",
    "longcat",
    "negation",
    "ordering",
    "smoke",
    "spelling_transform",
    "word_count",
    "zai",
]
