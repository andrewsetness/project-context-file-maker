"""Regression tests for schema validation in the CLI generator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from generate import AnswerValidationError, validate_answers


def test_about_me_missing_required_field_fails() -> None:
    with pytest.raises(AnswerValidationError, match="missing required field 'full_name'"):
        validate_answers(
            "about_me",
            {
                "job_title": "Product Manager",
                "primary_work": "I build software products.",
                "biggest_challenge": "Prioritization.",
            },
        )


def test_ai_preferences_wrong_type_fails() -> None:
    with pytest.raises(AnswerValidationError, match="field 'verbosity' must be string"):
        validate_answers(
            "ai_preferences",
            {
                "tone": "Direct",
                "verbosity": 3,
                "test_policy": "Test critical paths",
                "secrets_policy": "Never expose secrets",
            },
        )


def test_schema_allows_unspecified_additional_fields() -> None:
    # The current JSON schemas do not set additionalProperties=false.
    validate_answers(
        "about_me",
        {
            "full_name": "Avery Chen",
            "job_title": "Product Manager",
            "primary_work": "I build workflow software.",
            "biggest_challenge": "Prioritization.",
            "future_schema_field": "Preserve current JSON Schema behavior.",
        },
    )


def test_cli_rejects_invalid_payload_before_writing(tmp_path: Path) -> None:
    answers = tmp_path / "invalid.json"
    output = tmp_path / "should-not-exist.md"
    answers.write_text(
        json.dumps(
            {
                "full_name": "Avery Chen",
                "job_title": "Product Manager",
                "primary_work": "I build workflow software.",
                # biggest_challenge intentionally missing
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "generate.py"),
            "about_me",
            "--answers",
            str(answers),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "missing required field 'biggest_challenge'" in result.stderr
    assert not output.exists()
