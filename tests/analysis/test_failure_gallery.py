from obviousbench.analysis.build_failure_gallery import FailureGalleryEntry, build_failure_gallery


def test_failure_gallery_limits_and_renders_stable_markdown():
    entries = [
        FailureGalleryEntry(
            model="model/a",
            family="character_count",
            sample_id="obviousbench.char_count.en.v0.public.000001",
            question="How many r's are in strawberry?",
            expected_answer="3",
            extracted_answer="2",
            raw_output="There are 2 r's.",
            failure_type="incorrect_count",
            human_triviality="H0",
            source_type="public_archetype",
            why_obvious="Humans can count the visible letters directly.",
        ),
        FailureGalleryEntry(
            model="model/a",
            family="format_compliance",
            sample_id="obviousbench.format.en.v0.public.000001",
            question="Return only the number: how many letters are in cat?",
            expected_answer="3",
            extracted_answer="There are 3.",
            raw_output="There are 3.",
            failure_type="verbose_noncompliance",
            human_triviality="H0",
            source_type="generated_variant",
            why_obvious="The instruction asks for only a number.",
        ),
    ]

    markdown = build_failure_gallery(entries, limit=1)

    assert markdown.count("## Failure") == 1
    assert "How many r's are in strawberry?" in markdown
    assert "Return only the number" not in markdown

