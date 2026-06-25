from obviousbench.datasets.schemas import ScorerName
from obviousbench.scorers import get_scorer


def test_all_schema_scorers_resolve():
    for scorer_name in ScorerName:
        assert callable(get_scorer(scorer_name.value))

