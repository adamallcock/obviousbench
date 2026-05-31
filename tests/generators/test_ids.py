import pytest

from obviousbench.generators.ids import make_id


def test_make_id_formats_stable_id():
    assert make_id("character_count", "public_v0", 1) == (
        "obviousbench.char_count.en.v0.public.000001"
    )


def test_make_id_rejects_unknown_family():
    with pytest.raises(ValueError):
        make_id("unknown", "public_v0", 1)

