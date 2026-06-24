from pathlib import Path

import yaml


def test_model_matrix_uses_real_inspect_model_strings():
    matrix = yaml.safe_load(Path("configs/model_panels/models_v0.example.yaml").read_text())

    assert set(matrix) >= {"comparison_panel", "smoke_panel", "local_plumbing"}

    labels = {
        model["label"]
        for group in matrix.values()
        for model in group
        if isinstance(model, dict)
    }
    model_strings = {
        model["inspect_model"]
        for group in matrix.values()
        for model in group
        if isinstance(model, dict)
    }

    assert {"gpt-4.1", "gpt-4o", "gpt-5.5 none", "mockllm"}.issubset(labels)
    assert "<provider/" not in Path("configs/model_panels/models_v0.example.yaml").read_text()
    assert "openai/gpt-4.1" in model_strings
    assert "openai/gpt-4o" in model_strings
    assert "openai/gpt-5.5" in model_strings
    assert "mockllm/model" in model_strings


def test_model_matrix_documents_recruiter_safe_usage():
    matrix = yaml.safe_load(Path("configs/model_panels/models_v0.example.yaml").read_text())

    for group in matrix.values():
        for model in group:
            if not isinstance(model, dict):
                continue
            assert "external_note" in model
            assert "api" not in model["external_note"].lower()
            assert "key" not in model["external_note"].lower()
