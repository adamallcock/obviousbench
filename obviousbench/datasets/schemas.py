"""Pydantic schemas for ObviousBench datasets."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StrictStr, field_validator

from obviousbench.prompts import SUPPORTED_PROMPT_TEMPLATE_IDS


class Family(StrEnum):
    CHARACTER_COUNT = "character_count"
    SPELLING_TRANSFORM = "spelling_transform"
    ARITHMETIC = "arithmetic"
    WORD_COUNT = "word_count"
    ORDERING = "ordering"
    FORMAT_COMPLIANCE = "format_compliance"
    NEGATION = "negation"
    CONSTRAINT_AWARENESS = "constraint_awareness"


class AnswerType(StrEnum):
    INTEGER = "integer"
    DECIMAL = "decimal"
    STRING = "string"
    LIST = "list"
    MULTIPLE_CHOICE = "multiple_choice"
    JSON = "json"


class ScorerName(StrEnum):
    EXACT_INTEGER = "exact_integer_extract_first_v0"
    EXACT_STRING = "exact_string_trim_v0"
    NORMALIZED_STRING = "normalized_string_v0"
    NORMALIZED_LIST = "normalized_list_v0"
    MULTIPLE_CHOICE = "multiple_choice_letter_v0"
    REGEX_MATCH = "regex_match_v0"
    JSON_EXACT_FIELD = "json_exact_field_v0"
    WORD_COUNT = "word_count_v0"


class ReviewStatus(StrEnum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    RETIRED = "retired"


class HumanTriviality(StrEnum):
    H0 = "H0"
    H1 = "H1"
    H2 = "H2"
    H3 = "H3"


class SourceType(StrEnum):
    PUBLIC_ARCHETYPE = "public_archetype"
    GENERATED_VARIANT = "generated_variant"
    HAND_AUTHORED = "hand_authored"
    CALIBRATION = "calibration"


class RightsStatus(StrEnum):
    LINK_ONLY = "link_only_do_not_republish"
    PARAPHRASE_ONLY = "paraphrase_only"
    PERMISSIONED = "permissioned"
    PUBLIC_DOMAIN = "public_domain"
    INTERNAL_ONLY = "internal_only"
    USER_PROVIDED_SCREENSHOT = "user_provided_screenshot_do_not_republish"


class FailureType(StrEnum):
    NONE = "none"
    INCORRECT_COUNT = "incorrect_count"
    INCORRECT_CHARACTER_POSITION = "incorrect_character_position"
    WRONG_LETTER_OR_SUBSTRING = "wrong_letter_or_substring"
    STRING_TRANSFORM_ERROR = "string_transform_error"
    ARITHMETIC_ERROR = "arithmetic_error"
    NUMERIC_COMPARISON_ERROR = "numeric_comparison_error"
    LIST_COUNT_ERROR = "list_count_error"
    ORDERING_ERROR = "ordering_error"
    NEGATION_ERROR = "negation_error"
    FORMAT_NONCOMPLIANCE = "format_noncompliance"
    JSON_MALFORMED = "json_malformed"
    VERBOSE_NONCOMPLIANCE = "verbose_noncompliance"
    REFUSAL_OR_SAFETY_OVERTRIGGER = "refusal_or_safety_overtrigger"
    NON_ANSWER = "non_answer"
    AMBIGUOUS_OUTPUT = "ambiguous_output"
    PROVIDER_ERROR = "provider_error"
    TIMEOUT = "timeout"


FAMILY_SHORT_NAMES: dict[str, str] = {
    "character_count": "char_count",
    "spelling_transform": "spell",
    "arithmetic": "arith",
    "word_count": "word_count",
    "ordering": "ordering",
    "format_compliance": "format",
    "negation": "negation",
    "constraint_awareness": "constraint",
}
SHORT_NAME_FAMILIES = {value: key for key, value in FAMILY_SHORT_NAMES.items()}
SPLIT_SHORT_NAMES = {
    "public_v0": "public",
    "calibration_v0": "calibration",
    "private_v0": "private",
    "retired_v0": "retired",
}
SHORT_NAME_SPLITS = {value: key for key, value in SPLIT_SHORT_NAMES.items()}


class BenchmarkMetadata(BaseModel):
    """Common required metadata, with family-specific fields allowed."""

    model_config = ConfigDict(extra="allow")

    generated: bool = False
    variant_of: str | None = None
    prompt_template_id: StrictStr
    system_prompt: str | None = None
    choices: list[str] | None = None
    generator: str | None = None
    seed: int | None = None
    strict_format: bool = False
    why_obvious: str | None = None

    @field_validator("prompt_template_id")
    @classmethod
    def known_prompt_template(cls, value: str) -> str:
        if value not in SUPPORTED_PROMPT_TEMPLATE_IDS:
            raise ValueError(f"Unknown prompt template: {value}")
        return value

    @property
    def extra(self) -> dict[str, Any]:
        return dict(self.model_extra or {})


class BenchmarkItem(BaseModel):
    """Canonical benchmark item."""

    model_config = ConfigDict(use_enum_values=True)

    id: StrictStr
    family: Family
    subfamily: StrictStr
    prompt: StrictStr
    question: StrictStr
    target: StrictStr
    answer_type: AnswerType
    scorer: ScorerName
    split: StrictStr
    source_type: SourceType
    source_refs: list[StrictStr]
    human_triviality: HumanTriviality
    review_status: ReviewStatus
    metadata: BenchmarkMetadata

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> BenchmarkItem:
        return cls.model_validate(record)

    @field_validator("source_refs")
    @classmethod
    def source_refs_are_strings(cls, value: list[str]) -> list[str]:
        if any(not source_ref.strip() for source_ref in value):
            raise ValueError("source_refs cannot contain blank values")
        return value


class EngagementSignal(BaseModel):
    likes: int | None = None
    shares: int | None = None
    comments: int | None = None


class SourceRecord(BaseModel):
    """Source lead metadata. Sources are evidence leads, not benchmark truth."""

    model_config = ConfigDict(use_enum_values=True)

    source_id: StrictStr
    platform: StrictStr
    url: HttpUrl | None = None
    date_seen: StrictStr
    author_or_handle: str | None = None
    original_prompt: StrictStr
    claimed_model: str | None = None
    claimed_output: str | None = None
    failure_description: StrictStr
    engagement_signal: EngagementSignal = Field(default_factory=EngagementSignal)
    media_type: Literal["text", "screenshot", "video", "article"]
    rights_status: RightsStatus
    notes: StrictStr = ""

    @field_validator("date_seen")
    @classmethod
    def date_seen_is_iso_date(cls, value: str) -> str:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("date_seen must use YYYY-MM-DD")
        return value


@dataclass(frozen=True)
class ParsedItemId:
    family_short: str
    language: str
    version: str
    split_short: str
    index: int


_ID_RE = re.compile(
    r"^obviousbench\."
    r"(?P<family_short>[a-z_]+)\."
    r"(?P<language>en)\."
    r"(?P<version>v0)\."
    r"(?P<split_short>[a-z_]+)\."
    r"(?P<index>\d{6})$"
)


def parse_item_id(sample_id: str) -> ParsedItemId:
    """Parse and validate a stable ObviousBench item ID."""
    match = _ID_RE.fullmatch(sample_id)
    if not match:
        raise ValueError(f"Invalid ObviousBench item ID: {sample_id}")

    family_short = match.group("family_short")
    split_short = match.group("split_short")
    if family_short not in SHORT_NAME_FAMILIES:
        raise ValueError(f"Unknown family short name: {family_short}")
    if split_short not in SHORT_NAME_SPLITS:
        raise ValueError(f"Unknown split short name: {split_short}")

    return ParsedItemId(
        family_short=family_short,
        language=match.group("language"),
        version=match.group("version"),
        split_short=split_short,
        index=int(match.group("index")),
    )
