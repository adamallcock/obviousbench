"""Inspect task definitions."""

from obviousbench.tasks.archetype_expansions import archetype_expansions
from obviousbench.tasks.arithmetic import arithmetic
from obviousbench.tasks.barrage import barrage
from obviousbench.tasks.character_count import character_count
from obviousbench.tasks.constraint_awareness import constraint_awareness
from obviousbench.tasks.format_compliance import format_compliance
from obviousbench.tasks.negation import negation
from obviousbench.tasks.ordering import ordering
from obviousbench.tasks.smoke import smoke
from obviousbench.tasks.spelling_transform import spelling_transform
from obviousbench.tasks.word_count import word_count

__all__ = [
    "archetype_expansions",
    "arithmetic",
    "barrage",
    "character_count",
    "constraint_awareness",
    "format_compliance",
    "negation",
    "ordering",
    "smoke",
    "spelling_transform",
    "word_count",
]
