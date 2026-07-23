"""Inspect AI task registration imports."""

from obviousbench.providers import (
    aion,
    bedrock_flex,
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
    "arithmetic",
    "barrage",
    "bedrock_flex",
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
