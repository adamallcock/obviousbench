"""Evolver external-adapter request/response bridge for ObviousBench scorers."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from obviousbench.datasets.load import load_benchmark_jsonl
from obviousbench.datasets.schemas import BenchmarkItem
from obviousbench.scorers.dynamic import score_by_name

STRICT_SCORERS = {
    "exact_string_trim_v0",
    "multiple_choice_letter_v0",
    "regex_match_v0",
    "json_exact_field_v0",
}
SCORER_PROMPT_HINTS = {
    "exact_integer_extract_first_v0": "integer only",
    "word_count_v0": "integer only",
    "exact_string_trim_v0": "exact answer only",
    "normalized_string_v0": "exact answer only",
    "multiple_choice_letter_v0": "letter only",
    "normalized_list_v0": "comma list only",
    "regex_match_v0": "match the required pattern exactly",
    "json_exact_field_v0": "json object only",
}


@dataclass(frozen=True)
class CompletionResult:
    text: str
    token_usage: dict[str, int] = field(default_factory=dict)
    cost_usd: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TokenCostRates:
    input_per_million: float | None = None
    output_per_million: float | None = None
    reasoning_per_million: float | None = None

    def estimate_cost(self, token_usage: dict[str, int]) -> float | None:
        total = 0.0
        has_rate = False
        if self.input_per_million is not None:
            total += token_usage.get("input_tokens", 0) * self.input_per_million / 1_000_000
            has_rate = True
        if self.output_per_million is not None:
            total += token_usage.get("output_tokens", 0) * self.output_per_million / 1_000_000
            has_rate = True
        if self.reasoning_per_million is not None:
            total += (
                token_usage.get("reasoning_tokens", 0)
                * self.reasoning_per_million
                / 1_000_000
            )
            has_rate = True
        return total if has_rate else None


@dataclass(frozen=True)
class PromptEvalBudget:
    max_provider_requests: int | None = None
    max_total_cost_usd: float | None = None
    token_cost_rates: TokenCostRates | None = None


@dataclass
class _BudgetState:
    budget: PromptEvalBudget | None
    provider_requests: int = 0
    total_cost_usd: float = 0.0

    def before_provider_call(self) -> None:
        if self.budget is None:
            self.provider_requests += 1
            return
        if (
            self.budget.max_provider_requests is not None
            and self.provider_requests >= self.budget.max_provider_requests
        ):
            raise ValueError(
                "provider request budget exceeded: "
                f"{self.provider_requests}/{self.budget.max_provider_requests}."
            )
        self.provider_requests += 1

    def after_provider_call(self, result: CompletionResult) -> CompletionResult:
        if self.budget is None:
            return result
        cost_usd = result.cost_usd
        if cost_usd is None and self.budget.token_cost_rates is not None:
            cost_usd = self.budget.token_cost_rates.estimate_cost(result.token_usage)
        if self.budget.max_total_cost_usd is not None and cost_usd is None:
            raise ValueError(
                "Cost budget requires provider cost_usd or explicit token price rates."
            )
        if cost_usd is not None:
            self.total_cost_usd += cost_usd
            if (
                self.budget.max_total_cost_usd is not None
                and self.total_cost_usd > self.budget.max_total_cost_usd
            ):
                raise ValueError(
                    "Provider cost budget exceeded: "
                    f"{self.total_cost_usd:.6f}>{self.budget.max_total_cost_usd:.6f}."
                )
            return CompletionResult(
                text=result.text,
                token_usage=result.token_usage,
                cost_usd=cost_usd,
                metadata=result.metadata,
            )
        return result

    def diagnostics(self) -> dict[str, Any]:
        data: dict[str, Any] = {"provider_requests": self.provider_requests}
        if self.total_cost_usd:
            data["total_cost_usd"] = self.total_cost_usd
        return data


class OpenAIResponsesCompletionProvider:
    """Completion provider for paid/cached prompt-eval runs through Responses API."""

    def __init__(self, *, model: str, client: Any | None = None) -> None:
        self.model = _openai_model_name(model)
        if client is None:
            from openai import OpenAI

            client = OpenAI()
        self.client = client

    def __call__(
        self,
        *,
        system_prompt: str,
        item: dict[str, Any],
        model_settings: dict[str, Any],
    ) -> CompletionResult:
        response = self.client.responses.create(
            **_openai_response_kwargs(
                model=self.model,
                system_prompt=system_prompt,
                item=item,
                model_settings=model_settings,
            )
        )
        return CompletionResult(
            text=_response_text(response),
            token_usage=_response_usage(response),
            cost_usd=None,
            metadata={"response_id": getattr(response, "id", None)},
        )


def evaluate_prompt_eval_request(
    request_path: Path,
    response_path: Path,
    *,
    mode: str = "mock",
    completion_provider: Any | None = None,
    model_settings_override: dict[str, Any] | None = None,
    budget: PromptEvalBudget | None = None,
) -> None:
    """Evaluate an Evolver prompt-eval request and write an Evolver-compatible response.

    Mock mode is intentionally no-cost. Provider mode is the paid/cached hook for
    actual student-model runs.
    """
    request = json.loads(request_path.read_text(encoding="utf-8"))
    model_settings = dict(request.get("model_settings") or {})
    model_settings.update(model_settings_override or {})
    if mode == "provider" and completion_provider is None:
        raise ValueError("Provider mode requires a completion_provider.")
    if mode not in {"mock", "provider"}:
        raise ValueError(f"Unsupported prompt-eval mode: {mode}")
    budget_state = _BudgetState(budget)
    results = [
        _score_item(
            item,
            prompt=_prompt_text(request.get("prompt", {})),
            prompt_id=_prompt_id(request.get("prompt", {})),
            default_split=str(model_settings.get("split", "validation")),
            mode=mode,
            completion_provider=completion_provider,
            model_settings=model_settings,
            budget_state=budget_state,
        )
        for item in request.get("items", [])
    ]
    response_path.parent.mkdir(parents=True, exist_ok=True)
    response_path.write_text(
        json.dumps({"results": results}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_evolver_manifest(
    *,
    dataset_paths: Iterable[Path],
    output_path: Path,
    train_count: int,
    validation_count: int,
    holdout_count: int = 0,
    families: Iterable[str] | None = None,
) -> int:
    """Export real ObviousBench rows into Evolver's external item manifest shape."""
    if train_count < 0 or validation_count < 0 or holdout_count < 0:
        raise ValueError("Split counts must be non-negative.")
    total_count = train_count + validation_count + holdout_count
    if total_count <= 0:
        raise ValueError("At least one split count must be positive.")
    family_filter = set(families or ())
    items: list[BenchmarkItem] = []
    for dataset_path in dataset_paths:
        for item in load_benchmark_jsonl(dataset_path):
            if family_filter and item.family not in family_filter:
                continue
            if _mock_settings_for_item(item) is not None:
                items.append(item)
    if len(items) < total_count:
        raise ValueError(
            f"Need {total_count} supported item(s), but only found {len(items)}."
        )
    split_names = (
        ["train"] * train_count
        + ["validation"] * validation_count
        + ["holdout"] * holdout_count
    )
    rows = [
        _evolver_manifest_row(item, split=split)
        for item, split in zip(items[:total_count], split_names, strict=True)
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    return len(rows)


def _score_item(
    item: dict[str, Any],
    *,
    prompt: str,
    prompt_id: str,
    default_split: str,
    mode: str,
    completion_provider: Any | None,
    model_settings: dict[str, Any],
    budget_state: _BudgetState,
) -> dict[str, Any]:
    metadata = dict(item.get("metadata") or {})
    scorer_name = str(metadata.get("scorer") or item.get("scorer") or "exact_string_trim_v0")
    target = str(item.get("expected", item.get("target", "")))
    completion_result = _completion_for_item(
        mode=mode,
        completion_provider=completion_provider,
        prompt=prompt,
        item=item,
        metadata=metadata,
        model_settings=model_settings,
        budget_state=budget_state,
    )
    decision = score_by_name(
        scorer_name,
        completion_result.text,
        target,
        accepted_targets=tuple(metadata.get("accepted_targets") or ()),
    )
    passed = decision.strict_correct if scorer_name in STRICT_SCORERS else decision.correct
    score = 1.0 if passed else 0.0
    required_hint = metadata.get("required_prompt_hint") or metadata.get("required_hint")
    diagnostics = {
        "scorer": scorer_name,
        "explanation": decision.explanation,
        "answer_correct": decision.answer_correct,
        "format_correct": decision.resolved_format_correct,
        "strict_correct": decision.strict_correct,
        "completion_provider": mode,
    }
    if required_hint:
        diagnostics["required_hint"] = str(required_hint)
        if not passed:
            diagnostics["feedback"] = f"Add instruction: {required_hint}"
    if mode == "provider":
        diagnostics["budget"] = budget_state.diagnostics()
    return {
        "item_id": str(item["id"]),
        "family": str(item.get("family", metadata.get("family", "unknown"))),
        "split": str(metadata.get("split") or item.get("split") or default_split),
        "prompt_id": prompt_id,
        "score": score,
        "parsed_answer": decision.extracted,
        "objective_scores": {"accuracy": score},
        "failure_type": "none" if passed else decision.failure_type,
        "scorer_diagnostics": diagnostics,
        "trace_uri": completion_result.metadata.get("response_id"),
        "token_usage": completion_result.token_usage,
        "cost_usd": completion_result.cost_usd,
    }


def _evolver_manifest_row(item: BenchmarkItem, *, split: str) -> dict[str, Any]:
    mock_settings = _mock_settings_for_item(item)
    if mock_settings is None:
        raise ValueError(f"Unsupported scorer for Evolver export: {item.scorer}")
    required_hint, passing_completion, failing_completion = mock_settings
    return {
        "id": item.id,
        "family": item.family,
        "input": item.prompt,
        "expected": item.target,
        "metadata": {
            "split": split,
            "source_split": item.split,
            "subfamily": item.subfamily,
            "answer_type": item.answer_type,
            "scorer": item.scorer,
            "required_prompt_hint": required_hint,
            "passing_completion": passing_completion,
            "failing_completion": failing_completion,
        },
    }


def _mock_settings_for_item(item: BenchmarkItem) -> tuple[str, str, str] | None:
    required_hint = SCORER_PROMPT_HINTS.get(item.scorer)
    if required_hint is None:
        return None
    passing_completion = _passing_completion_for_item(item)
    if passing_completion is None or not _completion_passes(
        item.scorer,
        passing_completion,
        item.target,
    ):
        return None
    failing_completion = _failing_completion_for_item(item)
    if _completion_passes(item.scorer, failing_completion, item.target):
        failing_completion = "not sure"
    return required_hint, passing_completion, failing_completion


def _passing_completion_for_item(item: BenchmarkItem) -> str | None:
    if item.scorer == "json_exact_field_v0":
        return json.dumps({"answer": item.target}, sort_keys=True)
    if item.scorer == "regex_match_v0":
        return _regex_passing_completion(item.target)
    return item.target


def _failing_completion_for_item(item: BenchmarkItem) -> str:
    if item.scorer == "multiple_choice_letter_v0":
        return f"The answer is {item.target}."
    if item.scorer in {"exact_string_trim_v0", "normalized_string_v0"}:
        return f"The answer is {item.target}."
    if item.scorer == "json_exact_field_v0":
        return item.target
    return "not sure"


def _regex_passing_completion(pattern: str) -> str | None:
    candidates = ("YES", "NO", "A", "B", "C", "D", "true", "false", "1", "0", "OK")
    for candidate in candidates:
        if re.fullmatch(pattern, candidate):
            return candidate
    return None


def _completion_passes(scorer_name: str, completion: str, target: str) -> bool:
    decision = score_by_name(scorer_name, completion, target)
    return decision.strict_correct if scorer_name in STRICT_SCORERS else decision.correct


def _completion_for_item(
    *,
    mode: str,
    completion_provider: Any | None,
    prompt: str,
    item: dict[str, Any],
    metadata: dict[str, Any],
    model_settings: dict[str, Any],
    budget_state: _BudgetState,
) -> CompletionResult:
    if mode == "mock":
        return CompletionResult(
            text=_mock_completion_for_prompt(prompt, metadata),
            token_usage={"input_tokens": 0, "output_tokens": 0},
            cost_usd=0.0,
        )
    if completion_provider is None:
        raise ValueError("Provider mode requires a completion_provider.")
    budget_state.before_provider_call()
    result = completion_provider(
        system_prompt=prompt,
        item=item,
        model_settings=model_settings,
    )
    if isinstance(result, CompletionResult):
        return budget_state.after_provider_call(result)
    return budget_state.after_provider_call(CompletionResult(text=str(result)))


def _mock_completion_for_prompt(prompt: str, metadata: dict[str, Any]) -> str:
    if metadata.get("mock_completion") is not None:
        return str(metadata["mock_completion"])
    required_hint = metadata.get("required_prompt_hint") or metadata.get("required_hint")
    if required_hint is not None:
        prompt_has_hint = str(required_hint).casefold() in prompt.casefold()
        key = "passing_completion" if prompt_has_hint else "failing_completion"
        if metadata.get(key) is not None:
            return str(metadata[key])
    raise ValueError(
        "prompt-eval mock mode requires metadata.mock_completion or "
        "metadata.required_prompt_hint with passing_completion/failing_completion."
    )


def _prompt_text(prompt: Any) -> str:
    if isinstance(prompt, dict):
        return str(prompt.get("text", ""))
    return str(prompt)


def _prompt_id(prompt: Any) -> str:
    if isinstance(prompt, dict):
        return str(prompt.get("id", "prompt"))
    return "prompt"


def _openai_model_name(model: str) -> str:
    return model.removeprefix("openai/")


def _openai_response_kwargs(
    *,
    model: str,
    system_prompt: str,
    item: dict[str, Any],
    model_settings: dict[str, Any],
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "model": model,
        "instructions": system_prompt,
        "input": str(item.get("input", "")),
    }
    if model_settings.get("max_output_tokens") is not None:
        kwargs["max_output_tokens"] = int(model_settings["max_output_tokens"])
    if model_settings.get("temperature") is not None:
        kwargs["temperature"] = float(model_settings["temperature"])
    if model_settings.get("reasoning_effort") is not None:
        kwargs["reasoning"] = {"effort": model_settings["reasoning_effort"]}
    return kwargs


def _response_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text is not None:
        return str(output_text)
    if isinstance(response, dict) and response.get("output_text") is not None:
        return str(response["output_text"])
    raise ValueError("OpenAI response did not include output_text.")


def _response_usage(response: Any) -> dict[str, int]:
    usage = getattr(response, "usage", None)
    if usage is None and isinstance(response, dict):
        usage = response.get("usage")
    fields = {
        "input_tokens": _usage_value(usage, "input_tokens"),
        "output_tokens": _usage_value(usage, "output_tokens"),
        "total_tokens": _usage_value(usage, "total_tokens"),
    }
    reasoning_tokens = _nested_usage_value(usage, "output_tokens_details", "reasoning_tokens")
    if reasoning_tokens is not None:
        fields["reasoning_tokens"] = reasoning_tokens
    return {key: value for key, value in fields.items() if value is not None}


def _usage_value(usage: Any, field_name: str) -> int | None:
    if usage is None:
        return None
    value = usage.get(field_name) if isinstance(usage, dict) else getattr(usage, field_name, None)
    return int(value) if value is not None else None


def _nested_usage_value(usage: Any, container_name: str, field_name: str) -> int | None:
    if usage is None:
        return None
    if isinstance(usage, dict):
        container = usage.get(container_name)
    else:
        container = getattr(usage, container_name, None)
    return _usage_value(container, field_name)
