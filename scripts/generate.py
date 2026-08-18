#!/usr/bin/env python3
"""
Context File Maker — CLI Generator

Generates context files from schema-validated JSON answer payloads.

Usage:
    python scripts/generate.py about_me --answers data/about_me.json
    python scripts/generate.py ai_preferences --answers data/prefs.json
    python scripts/generate.py all --about data/about.json --prefs data/prefs.json
    python scripts/generate.py about_me --answers data/about.json --output my_about.md
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from template_engine import fill_template


PROJECT_ROOT = Path(__file__).resolve().parent.parent

TEMPLATES = {
    "about_me": PROJECT_ROOT / "templates" / "free" / "about_me.md",
    "ai_preferences": PROJECT_ROOT / "templates" / "free" / "ai_preferences.md",
}

SCHEMAS = {
    "about_me": PROJECT_ROOT / "schemas" / "about_me_answers.schema.json",
    "ai_preferences": PROJECT_ROOT / "schemas" / "ai_preferences_answers.schema.json",
}


class AnswerValidationError(ValueError):
    """Raised when an answer payload violates its checked-in JSON schema."""


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object, with helpful errors for malformed input."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError as exc:
        raise AnswerValidationError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AnswerValidationError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise AnswerValidationError(
            f"Answer payload must be a JSON object: {path}"
        )
    return payload


def load_schema(template_name: str) -> dict[str, Any]:
    """Load the checked-in answer schema for a supported template."""
    schema_path = SCHEMAS.get(template_name)
    if schema_path is None:
        raise AnswerValidationError(
            f"No schema configured for template '{template_name}'"
        )
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AnswerValidationError(f"Schema not found: {schema_path}") from exc
    except json.JSONDecodeError as exc:
        raise AnswerValidationError(
            f"Invalid JSON schema in {schema_path}: {exc}"
        ) from exc
    if not isinstance(schema, dict):
        raise AnswerValidationError(f"Schema must be a JSON object: {schema_path}")
    return schema


def validate_answers(template_name: str, answers: dict[str, Any]) -> None:
    """Validate the schema subset used by the free-tier answer contracts.

    The checked-in schemas are the source of truth. The runtime intentionally
    implements only the constructs those schemas currently use: an object with
    named properties, required fields, and scalar property types. If the schema
    grows beyond this subset, validation fails closed rather than silently
    accepting an unsupported rule.
    """
    schema = load_schema(template_name)
    if schema.get("type") != "object":
        raise AnswerValidationError(
            f"Unsupported schema root for '{template_name}': expected type=object"
        )

    required = schema.get("required", [])
    properties = schema.get("properties", {})
    if not isinstance(required, list) or not isinstance(properties, dict):
        raise AnswerValidationError(
            f"Unsupported schema structure for '{template_name}'"
        )

    errors: list[str] = []
    for field in required:
        if not isinstance(field, str):
            raise AnswerValidationError(
                f"Unsupported non-string required field in '{template_name}' schema"
            )
        if field not in answers:
            errors.append(f"missing required field '{field}'")

    type_map: dict[str, type] = {
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
        "object": dict,
        "array": list,
    }
    for field, value in answers.items():
        rule = properties.get(field)
        # Current schemas allow additional properties because they do not set
        # additionalProperties=false. Preserve that JSON Schema behavior.
        if rule is None:
            continue
        if not isinstance(rule, dict):
            raise AnswerValidationError(
                f"Unsupported schema rule for '{template_name}.{field}'"
            )
        expected_name = rule.get("type")
        if expected_name is None:
            continue
        expected = type_map.get(expected_name)
        if expected is None:
            raise AnswerValidationError(
                f"Unsupported schema type '{expected_name}' for '{template_name}.{field}'"
            )
        # bool is a subclass of int in Python; do not accept it as number/integer.
        wrong_type = not isinstance(value, expected)
        if expected_name in {"number", "integer"} and isinstance(value, bool):
            wrong_type = True
        if wrong_type:
            errors.append(
                f"field '{field}' must be {expected_name}, got {type(value).__name__}"
            )

    if errors:
        raise AnswerValidationError(
            f"Invalid {template_name} answers: " + "; ".join(errors)
        )


def generate(
    template_name: str,
    answers: dict[str, Any],
    output_path: Path | None = None,
) -> str:
    """Validate answers, render a template, and optionally write the result."""
    if template_name not in TEMPLATES:
        raise AnswerValidationError(
            f"Unknown template '{template_name}'. Available: {list(TEMPLATES.keys())}"
        )

    template_path = TEMPLATES[template_name]
    if not template_path.exists():
        raise AnswerValidationError(f"Template not found: {template_path}")

    validate_answers(template_name, answers)
    template_str = template_path.read_text(encoding="utf-8")
    result = fill_template(template_str, answers)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding="utf-8")
        print(f"Generated: {output_path}")
    else:
        print(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate AI context files from schema-validated JSON answer payloads"
    )
    subparsers = parser.add_subparsers(dest="command", help="What to generate")

    about_parser = subparsers.add_parser("about_me", help="Generate about_me.md")
    about_parser.add_argument(
        "--answers", required=True, type=Path, help="JSON file with about_me answers"
    )
    about_parser.add_argument(
        "--output", "-o", type=Path, help="Output file path (default: stdout)"
    )

    prefs_parser = subparsers.add_parser(
        "ai_preferences", help="Generate ai_preferences.md"
    )
    prefs_parser.add_argument(
        "--answers",
        required=True,
        type=Path,
        help="JSON file with ai_preferences answers",
    )
    prefs_parser.add_argument(
        "--output", "-o", type=Path, help="Output file path (default: stdout)"
    )

    all_parser = subparsers.add_parser("all", help="Generate both files")
    all_parser.add_argument(
        "--about", required=True, type=Path, help="JSON file with about_me answers"
    )
    all_parser.add_argument(
        "--prefs",
        required=True,
        type=Path,
        help="JSON file with ai_preferences answers",
    )
    all_parser.add_argument(
        "--outdir",
        "-d",
        type=Path,
        default=Path("."),
        help="Output directory (default: current dir)",
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "all":
            about_data = load_json(args.about)
            prefs_data = load_json(args.prefs)
            generate("about_me", about_data, args.outdir / "about_me.md")
            generate(
                "ai_preferences", prefs_data, args.outdir / "ai_preferences.md"
            )
        elif args.command == "about_me":
            generate("about_me", load_json(args.answers), args.output)
        elif args.command == "ai_preferences":
            generate("ai_preferences", load_json(args.answers), args.output)
    except AnswerValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
