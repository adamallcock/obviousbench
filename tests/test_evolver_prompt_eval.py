import json

from obviousbench.cli import main
from obviousbench.evolver_prompt_eval import (
    CompletionResult,
    PromptEvalBudget,
    TokenCostRates,
    evaluate_prompt_eval_request,
    write_evolver_manifest,
)
from tests.datasets.test_schemas import valid_record


def test_evaluate_prompt_eval_request_scores_prompt_conditioned_mock_outputs(tmp_path):
    request_path = tmp_path / "request.json"
    response_path = tmp_path / "response.json"
    request_path.write_text(
        json.dumps(
            {
                "prompt": {
                    "id": "prompt_strong",
                    "text": "Be concise. Respond with integer only.",
                    "role": "system",
                },
                "items": [
                    {
                        "id": "obviousbench.arith.en.v0.public.000001",
                        "family": "arithmetic",
                        "input": "Question: 2 + 3\nAnswer:",
                        "expected": "5",
                        "metadata": {
                            "split": "validation",
                            "scorer": "exact_integer_extract_first_v0",
                            "required_prompt_hint": "integer only",
                            "passing_completion": "5",
                            "failing_completion": "five apples",
                        },
                    }
                ],
                "model_settings": {"split": "validation"},
                "capture_traces": True,
            }
        ),
        encoding="utf-8",
    )

    evaluate_prompt_eval_request(request_path, response_path)

    response = json.loads(response_path.read_text(encoding="utf-8"))
    result = response["results"][0]
    assert result["item_id"] == "obviousbench.arith.en.v0.public.000001"
    assert result["family"] == "arithmetic"
    assert result["split"] == "validation"
    assert result["prompt_id"] == "prompt_strong"
    assert result["score"] == 1.0
    assert result["parsed_answer"] == "5"
    assert result["objective_scores"] == {"accuracy": 1.0}
    assert result["failure_type"] == "none"
    assert result["scorer_diagnostics"]["scorer"] == "exact_integer_extract_first_v0"
    assert result["scorer_diagnostics"]["required_hint"] == "integer only"
    assert result["token_usage"] == {"input_tokens": 0, "output_tokens": 0}
    assert result["cost_usd"] == 0.0


def test_evaluate_prompt_eval_request_reports_failures_for_missing_hint(tmp_path):
    request_path = tmp_path / "request.json"
    response_path = tmp_path / "response.json"
    request_path.write_text(
        json.dumps(
            {
                "prompt": {"id": "prompt_base", "text": "Be concise."},
                "items": [
                    {
                        "id": "choice_1",
                        "family": "format_compliance",
                        "input": "Pick A.",
                        "expected": "A",
                        "metadata": {
                            "split": "train",
                            "scorer": "multiple_choice_letter_v0",
                            "required_prompt_hint": "letter only",
                            "passing_completion": "A",
                            "failing_completion": "The answer is A.",
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    evaluate_prompt_eval_request(request_path, response_path)

    result = json.loads(response_path.read_text(encoding="utf-8"))["results"][0]
    assert result["score"] == 0.0
    assert result["failure_type"] != "none"
    assert result["scorer_diagnostics"]["required_hint"] == "letter only"


def test_cli_prompt_eval_writes_evolver_contract_response(tmp_path):
    request_path = tmp_path / "request.json"
    response_path = tmp_path / "response.json"
    request_path.write_text(
        json.dumps(
            {
                "prompt": {"id": "prompt_base", "text": "Be concise."},
                "items": [
                    {
                        "id": "string_1",
                        "family": "format_compliance",
                        "input": "Return CAT.",
                        "expected": "CAT",
                        "metadata": {
                            "split": "validation",
                            "scorer": "exact_string_trim_v0",
                            "mock_completion": "CAT",
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(
        ["prompt-eval", "--request", str(request_path), "--response", str(response_path)]
    )

    assert exit_code == 0
    response = json.loads(response_path.read_text(encoding="utf-8"))
    assert response["results"][0]["score"] == 1.0


def test_evaluate_prompt_eval_request_can_use_completion_provider(tmp_path):
    request_path = tmp_path / "request.json"
    response_path = tmp_path / "response.json"
    request_path.write_text(
        json.dumps(
            {
                "prompt": {
                    "id": "prompt_model",
                    "text": "Return only the final answer.",
                },
                "items": [
                    {
                        "id": "arith_1",
                        "family": "arithmetic",
                        "input": "Question: 2 + 3\nAnswer:",
                        "expected": "5",
                        "metadata": {
                            "split": "validation",
                            "scorer": "exact_integer_extract_first_v0",
                        },
                    }
                ],
                "model_settings": {
                    "model": "openai/gpt-5.4-mini",
                    "reasoning_effort": "none",
                    "max_output_tokens": 16,
                },
            }
        ),
        encoding="utf-8",
    )
    calls = []

    def fake_provider(*, system_prompt, item, model_settings):
        calls.append(
            {
                "system_prompt": system_prompt,
                "item": item,
                "model_settings": model_settings,
            }
        )
        return CompletionResult(
            text="5",
            token_usage={"input_tokens": 11, "output_tokens": 1, "total_tokens": 12},
            cost_usd=0.000001,
            metadata={"response_id": "resp_123"},
        )

    evaluate_prompt_eval_request(
        request_path,
        response_path,
        mode="provider",
        completion_provider=fake_provider,
    )

    response = json.loads(response_path.read_text(encoding="utf-8"))
    result = response["results"][0]
    assert calls[0]["system_prompt"] == "Return only the final answer."
    assert calls[0]["item"]["input"] == "Question: 2 + 3\nAnswer:"
    assert calls[0]["model_settings"]["reasoning_effort"] == "none"
    assert result["score"] == 1.0
    assert result["parsed_answer"] == "5"
    assert result["token_usage"] == {
        "input_tokens": 11,
        "output_tokens": 1,
        "total_tokens": 12,
    }
    assert result["cost_usd"] == 0.000001
    assert result["scorer_diagnostics"]["completion_provider"] == "provider"
    assert result["trace_uri"] == "resp_123"


def test_evaluate_prompt_eval_request_enforces_request_and_cost_budget(tmp_path):
    request_path = tmp_path / "request.json"
    response_path = tmp_path / "response.json"
    request_path.write_text(
        json.dumps(
            {
                "prompt": {"id": "prompt_model", "text": "Return only the answer."},
                "items": [
                    {
                        "id": "arith_1",
                        "family": "arithmetic",
                        "input": "Question: 2 + 3\nAnswer:",
                        "expected": "5",
                        "metadata": {
                            "split": "validation",
                            "scorer": "exact_integer_extract_first_v0",
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    def fake_provider(*, system_prompt, item, model_settings):
        return CompletionResult(
            text="5",
            token_usage={
                "input_tokens": 1_000,
                "output_tokens": 100,
                "reasoning_tokens": 50,
            },
        )

    evaluate_prompt_eval_request(
        request_path,
        response_path,
        mode="provider",
        completion_provider=fake_provider,
        budget=PromptEvalBudget(
            max_provider_requests=1,
            max_total_cost_usd=0.01,
            token_cost_rates=TokenCostRates(
                input_per_million=1.0,
                output_per_million=10.0,
                reasoning_per_million=20.0,
            ),
        ),
    )

    result = json.loads(response_path.read_text(encoding="utf-8"))["results"][0]
    assert result["cost_usd"] == 0.003
    assert result["scorer_diagnostics"]["budget"]["provider_requests"] == 1


def test_evaluate_prompt_eval_request_refuses_over_budget_provider_calls(tmp_path):
    request_path = tmp_path / "request.json"
    response_path = tmp_path / "response.json"
    request_path.write_text(
        json.dumps(
            {
                "prompt": {"id": "prompt_model", "text": "Return only the answer."},
                "items": [
                    {
                        "id": "arith_1",
                        "family": "arithmetic",
                        "input": "Question: 2 + 3\nAnswer:",
                        "expected": "5",
                        "metadata": {
                            "split": "validation",
                            "scorer": "exact_integer_extract_first_v0",
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    def fake_provider(*, system_prompt, item, model_settings):
        raise AssertionError("provider should not be called when request budget is zero")

    try:
        evaluate_prompt_eval_request(
            request_path,
            response_path,
            mode="provider",
            completion_provider=fake_provider,
            budget=PromptEvalBudget(max_provider_requests=0),
        )
    except ValueError as exc:
        assert "provider request budget" in str(exc)
    else:
        raise AssertionError("expected provider request budget failure")


def test_cli_prompt_eval_openai_mode_builds_provider(monkeypatch, tmp_path):
    request_path = tmp_path / "request.json"
    response_path = tmp_path / "response.json"
    request_path.write_text(
        json.dumps(
            {
                "prompt": {"id": "prompt_model", "text": "Return only the answer."},
                "items": [
                    {
                        "id": "arith_1",
                        "family": "arithmetic",
                        "input": "Question: 2 + 3\nAnswer:",
                        "expected": "5",
                        "metadata": {
                            "split": "validation",
                            "scorer": "exact_integer_extract_first_v0",
                        },
                    }
                ],
                "model_settings": {"model": "openai/gpt-5.4-mini"},
            }
        ),
        encoding="utf-8",
    )
    provider_kwargs = {}

    class FakeOpenAIProvider:
        def __init__(self, **kwargs):
            provider_kwargs.update(kwargs)

        def __call__(self, *, system_prompt, item, model_settings):
            assert system_prompt == "Return only the answer."
            assert model_settings["reasoning_effort"] == "low"
            return CompletionResult(
                text="5",
                token_usage={"input_tokens": 10, "output_tokens": 1},
                cost_usd=None,
                metadata={"response_id": "resp_cli"},
            )

    monkeypatch.setattr("obviousbench.cli.OpenAIResponsesCompletionProvider", FakeOpenAIProvider)

    exit_code = main(
        [
            "prompt-eval",
            "--mode",
            "openai",
            "--request",
            str(request_path),
            "--response",
            str(response_path),
            "--model",
            "openai/gpt-5.4-mini",
            "--generation-setting",
            "reasoning_effort=low",
            "--generation-setting",
            "max_output_tokens=16",
            "--max-provider-requests",
            "1",
            "--max-total-cost-usd",
            "0.01",
            "--input-price-per-million",
            "1.0",
            "--output-price-per-million",
            "10.0",
        ]
    )

    assert exit_code == 0
    assert provider_kwargs == {"model": "openai/gpt-5.4-mini"}
    response = json.loads(response_path.read_text(encoding="utf-8"))
    assert response["results"][0]["trace_uri"] == "resp_cli"
    assert response["results"][0]["score"] == 1.0
    assert response["results"][0]["scorer_diagnostics"]["budget"]["provider_requests"] == 1


def test_write_evolver_manifest_exports_prompt_conditioned_real_items(tmp_path):
    dataset_path = tmp_path / "items.jsonl"
    dataset_path.write_text(
        "\n".join(
            [
                json.dumps(valid_record(id="obviousbench.char_count.en.v0.public.000001")),
                json.dumps(
                    valid_record(
                        id="obviousbench.negation.en.v0.public.000001",
                        family="negation",
                        subfamily="not_choice",
                        answer_type="multiple_choice",
                        scorer="multiple_choice_letter_v0",
                        target="C",
                        prompt=(
                            "Answer the question. Return only the letter of the correct option.\n\n"
                            "Question: Which word does not contain e?\n\n"
                            "A. tree\nB. stone\nC. cat\nD. green\n\nAnswer:"
                        ),
                        question="Which word does not contain e?",
                        metadata={
                            "choices": ["tree", "stone", "cat", "green"],
                            "generated": False,
                            "prompt_template_id": "multiple_choice_letter_v0",
                            "system_prompt": None,
                            "strict_format": True,
                        },
                    )
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    out = tmp_path / "evolver-items.jsonl"

    count = write_evolver_manifest(
        dataset_paths=[dataset_path],
        output_path=out,
        train_count=1,
        validation_count=1,
    )

    assert count == 2
    rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["id"] == "obviousbench.char_count.en.v0.public.000001"
    assert rows[0]["input"].startswith("Answer the question.")
    assert rows[0]["expected"] == "3"
    assert rows[0]["metadata"]["split"] == "train"
    assert rows[0]["metadata"]["source_split"] == "public_v0"
    assert rows[0]["metadata"]["scorer"] == "exact_integer_extract_first_v0"
    assert rows[0]["metadata"]["required_prompt_hint"] == "integer only"
    assert rows[0]["metadata"]["passing_completion"] == "3"
    assert rows[0]["metadata"]["failing_completion"] != "3"
    assert rows[1]["metadata"]["split"] == "validation"
    assert rows[1]["metadata"]["required_prompt_hint"] == "letter only"
    assert rows[1]["metadata"]["passing_completion"] == "C"
    assert rows[1]["metadata"]["failing_completion"] == "The answer is C."


def test_write_evolver_manifest_uses_requested_item_count(tmp_path):
    dataset_path = tmp_path / "items.jsonl"
    dataset_path.write_text(
        "\n".join(
            json.dumps(
                valid_record(id=f"obviousbench.char_count.en.v0.public.{index:06d}")
            )
            for index in range(1, 5)
        )
        + "\n",
        encoding="utf-8",
    )
    out = tmp_path / "evolver-items.jsonl"

    count = write_evolver_manifest(
        dataset_paths=[dataset_path],
        output_path=out,
        train_count=1,
        validation_count=1,
    )

    rows = out.read_text(encoding="utf-8").splitlines()
    assert count == 2
    assert len(rows) == 2


def test_cli_export_evolver_manifest_writes_manifest(tmp_path, capsys):
    dataset_path = tmp_path / "items.jsonl"
    dataset_path.write_text(
        "\n".join(
            [
                json.dumps(valid_record(id="obviousbench.char_count.en.v0.public.000001")),
                json.dumps(valid_record(id="obviousbench.char_count.en.v0.public.000002")),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    out = tmp_path / "manifest.jsonl"

    exit_code = main(
        [
            "export-evolver-manifest",
            "--dataset",
            str(dataset_path),
            "--out",
            str(out),
            "--train-count",
            "1",
            "--validation-count",
            "1",
        ]
    )

    assert exit_code == 0
    assert len(out.read_text(encoding="utf-8").splitlines()) == 2
    assert "Wrote 2 Evolver item(s)" in capsys.readouterr().out
