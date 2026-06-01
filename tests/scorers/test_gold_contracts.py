from pathlib import Path

import pytest

from obviousbench.analysis.rescore import rescore_output
from obviousbench.datasets.schemas import ScorerName
from obviousbench.scorers.gold import load_gold_examples

FIXTURE_DIR = Path(__file__).parents[1] / "fixtures" / "scorer_gold"
GOLD_EXAMPLES = load_gold_examples(sorted(FIXTURE_DIR.glob("*.yaml")))


def test_load_gold_examples_validates_duplicate_ids(tmp_path: Path):
    fixture = tmp_path / "gold.yaml"
    fixture.write_text(
        """
examples:
  - id: duplicate
    scorer: exact_string_trim_v0
    target: "yes"
    output: "yes"
    expected:
      answer_correct: true
      format_correct: true
      strict_correct: true
      failure_type: none
  - id: duplicate
    scorer: exact_string_trim_v0
    target: "yes"
    output: "yes"
    expected:
      answer_correct: true
      format_correct: true
      strict_correct: true
      failure_type: none
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate scorer gold example id"):
        load_gold_examples([fixture])


def test_load_gold_examples_validates_unknown_scorer(tmp_path: Path):
    fixture = tmp_path / "gold.yaml"
    fixture.write_text(
        """
examples:
  - id: unknown.scorer
    scorer: hallucinated_scorer_v0
    target: "yes"
    output: "yes"
    expected:
      answer_correct: true
      format_correct: true
      strict_correct: true
      failure_type: none
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unknown scorer in scorer gold example"):
        load_gold_examples([fixture])


def test_load_gold_examples_requires_expected_booleans(tmp_path: Path):
    fixture = tmp_path / "gold.yaml"
    fixture.write_text(
        """
examples:
  - id: missing.expected.boolean
    scorer: exact_string_trim_v0
    target: "yes"
    output: "yes"
    expected:
      answer_correct: true
      strict_correct: true
      failure_type: none
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="format_correct"):
        load_gold_examples([fixture])


@pytest.mark.parametrize("example", GOLD_EXAMPLES, ids=lambda example: example.id)
def test_scorer_gold_contract(example):
    decision = rescore_output(
        scorer_name=example.scorer,
        output=example.output,
        target=example.target,
    )

    assert decision.answer_correct is example.expected.answer_correct
    assert decision.resolved_format_correct is example.expected.format_correct
    assert decision.strict_correct is example.expected.strict_correct
    assert decision.failure_type == example.expected.failure_type
    assert decision.extracted == example.expected.extracted


def test_gold_fixtures_cover_every_active_scorer_with_reviewable_examples():
    counts = {scorer.value: 0 for scorer in ScorerName}
    for example in GOLD_EXAMPLES:
        counts[example.scorer] += 1
        assert example.notes

    assert all(count >= 20 for count in counts.values())
