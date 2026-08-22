"""Regression tests for schema enforcement in the CLI generator.

Schema enforcement is unconditional per docs/DATA-CONTRACT.md: invalid
payloads must fail before any output is written, with or without --validate,
and with or without jsonschema installed.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from generate import validate_answers


def test_about_me_missing_required_field_fails() -> None:
    valid, msgs = validate_answers(
        "about_me",
        {
            "job_title": "Product Manager",
            "primary_work": "I build software products.",
            "biggest_challenge": "Prioritization.",
        },
    )
    assert not valid
    assert any("full_name" in m and "required" in m for m in msgs)


def test_ai_preferences_wrong_type_fails() -> None:
    valid, msgs = validate_answers(
        "ai_preferences",
        {
            "tone": "Direct",
            "verbosity": 3,
            "test_policy": "Test critical paths",
            "secrets_policy": "Never expose secrets",
        },
    )
    assert not valid
    assert any("'verbosity'" in m and "string" in m for m in msgs)


def test_schema_allows_unspecified_additional_fields() -> None:
    # The current JSON schemas do not set additionalProperties=false.
    valid, msgs = validate_answers(
        "about_me",
        {
            "full_name": "Avery Chen",
            "job_title": "Product Manager",
            "primary_work": "I build workflow software.",
            "biggest_challenge": "Prioritization.",
            "future_schema_field": "Preserve current JSON Schema behavior.",
        },
    )
    assert valid
    assert msgs == []


def test_enforcement_is_unconditional_without_validate_flag(tmp_path: Path) -> None:
    """Invalid payloads fail even when --validate is not passed."""
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
    assert "biggest_challenge" in result.stderr
    assert not output.exists()


def test_enforcement_holds_without_jsonschema_installed(monkeypatch) -> None:
    """Required/type checks are dependency-free; a missing jsonschema must not
    downgrade enforcement to skip."""
    import generate

    answers = {
        "job_title": "Product Manager",
        "primary_work": "I build software products.",
        "biggest_challenge": "Prioritization.",
    }
    monkeypatch.setitem(sys.modules, "jsonschema", None)  # forces ImportError

    valid, msgs = generate.validate_answers("about_me", answers)

    assert not valid
    assert any("full_name" in m and "required" in m for m in msgs)
