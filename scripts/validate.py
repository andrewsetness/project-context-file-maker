#!/usr/bin/env python3
"""
Context File Maker — Validator

Checks that the free-tier input/output contract agrees with itself:
  - JSON answer schemas are valid and use only supported constructs
  - Schema fields match question-bank fields and template placeholders
  - Synthetic fixtures satisfy the schema
  - Templates have valid syntax
  - Example outputs are consistent with templates (--strict / --examples)

Usage:
    python scripts/validate.py
    python scripts/validate.py --strict  # also check example outputs
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

from generate import AnswerValidationError, validate_answers


PROJECT_ROOT = Path(__file__).resolve().parent.parent

FREE_TIER_CONTRACTS = [
    {
        "name": "about_me",
        "template": "templates/free/about_me.md",
        "questions": "docs/questionnaires/about_me_questions.md",
        "schema": "schemas/about_me_answers.schema.json",
        "example": "output-examples/about_me_example.md",
        "fixtures": [
            "tests/fixtures/about_me_answers.json",
            "tests/fixtures/about_me_minimal.json",
        ],
    },
    {
        "name": "ai_preferences",
        "template": "templates/free/ai_preferences.md",
        "questions": "docs/questionnaires/ai_preferences_questions.md",
        "schema": "schemas/ai_preferences_answers.schema.json",
        "example": "output-examples/ai_preferences_example.md",
        "fixtures": [
            "tests/fixtures/ai_preferences_answers.json",
            "tests/fixtures/ai_preferences_minimal.json",
        ],
    },
]

SUPPORTED_SCHEMA_KEYS = {
    "$schema",
    "title",
    "description",
    "type",
    "properties",
    "required",
}
SUPPORTED_PROPERTY_KEYS = {"type", "description"}
SUPPORTED_TYPES = {"string", "number", "integer", "boolean", "object", "array"}
INTERNAL_TEMPLATE_FIELDS = {"name", "description"}


class ValidationError:
    def __init__(self, file: str, message: str, severity: str = 'error'):
        self.file = file
        self.message = message
        self.severity = severity

    def __str__(self):
        return f"[{self.severity.upper()}] {self.file}: {self.message}"


class Validator:
    def __init__(self, root: Path = None):
        self.root = root or PROJECT_ROOT
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    def error(self, file: str, message: str):
        self.errors.append(ValidationError(file, message, 'error'))

    def warn(self, file: str, message: str):
        self.warnings.append(ValidationError(file, message, 'warning'))

    def validate_template_syntax(self, template_path: Path) -> Set[str]:
        """Check template for valid Mustache-like syntax. Return placeholder names."""
        content = template_path.read_text(encoding='utf-8')
        placeholders: Set[str] = set()

        # Check for unmatched {{ without }}
        opens = len(re.findall(r'\{\{', content))
        closes = len(re.findall(r'\}\}', content))
        if opens != closes:
            rel = template_path.relative_to(self.root)
            self.error(str(rel), f"Unmatched {{{{ / }}}}: {opens} opens vs {closes} closes")

        # Check {{#...}} has matching {{/...}}
        section_opens = re.findall(r'\{\{#(\w+)\}\}', content)
        section_closes = re.findall(r'\{\{/(\w+)\}\}', content)
        if sorted(section_opens) != sorted(section_closes):
            rel = template_path.relative_to(self.root)
            self.error(str(rel),
                       f"Unmatched section blocks: opens={section_opens}, closes={section_closes}")

        # Extract simple placeholders
        for match in re.finditer(r'\{\{(\w+)\}\}', content):
            placeholders.add(match.group(1))

        # Extract conditional placeholders (also simple names)
        for match in re.finditer(r'\{\{#(\w+)\}\}', content):
            placeholders.add(match.group(1))

        return placeholders

    def extract_question_fields(self, question_bank_path: Path) -> Set[str]:
        """Extract field names from a question bank markdown table."""
        content = question_bank_path.read_text(encoding='utf-8')
        fields: Set[str] = set()

        # Parse markdown table rows: | # | field_name | question | ... |
        for line in content.split('\n'):
            match = re.match(r'\|\s*\d+\s*\|\s*(\w+)\s*\|', line)
            if match:
                fields.add(match.group(1))

        return fields

    def validate_placeholder_field_mapping(
        self, template_path: Path, question_bank_path: Path
    ):
        """Check that template placeholders and question bank fields match."""
        placeholders = self.validate_template_syntax(template_path)
        fields = self.extract_question_fields(question_bank_path)

        rel_t = template_path.relative_to(self.root)
        rel_q = question_bank_path.relative_to(self.root)

        # Question bank fields NOT in template
        missing_in_template = fields - placeholders
        for field in sorted(missing_in_template):
            self.warn(str(rel_t),
                      f"Question field '{field}' (from {rel_q.name}) has no placeholder in template")

        # Template placeholders NOT in question bank
        missing_in_question = placeholders - fields - INTERNAL_TEMPLATE_FIELDS
        for field in sorted(missing_in_question):
            self.warn(str(rel_t),
                      f"Placeholder '{{{{{field}}}}}' has no question in {rel_q.name}")

    def load_schema(self, schema_path: Path) -> dict[str, Any] | None:
        """Load a JSON Schema object or record an error and return None."""
        rel = str(schema_path.relative_to(self.root))
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self.error(rel, "Schema file not found")
            return None
        except json.JSONDecodeError as exc:
            self.error(rel, f"Invalid JSON: {exc}")
            return None
        if not isinstance(schema, dict):
            self.error(rel, "Schema must be a JSON object")
            return None
        return schema

    def validate_schema_subset(self, schema_path: Path, schema: dict[str, Any]) -> Set[str]:
        """Reject unsupported JSON Schema constructs. Return property names."""
        rel = str(schema_path.relative_to(self.root))
        unknown_keys = set(schema) - SUPPORTED_SCHEMA_KEYS
        for key in sorted(unknown_keys):
            self.error(
                rel,
                f"Unsupported schema key '{key}'. "
                "Extend the runtime validator with tests or drop the rule.",
            )

        if schema.get("type") != "object":
            self.error(rel, "Schema root must have type=object")

        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            self.error(rel, "Schema properties must be an object")
            return set()

        fields: Set[str] = set()
        for name, rule in properties.items():
            if not isinstance(name, str) or not name.isidentifier():
                self.error(rel, f"Invalid property name '{name}'")
                continue
            fields.add(name)
            if not isinstance(rule, dict):
                self.error(rel, f"Property '{name}' must be an object")
                continue
            unknown_rule_keys = set(rule) - SUPPORTED_PROPERTY_KEYS
            for key in sorted(unknown_rule_keys):
                self.error(
                    rel,
                    f"Unsupported schema key '{name}.{key}'. "
                    "Extend the runtime validator with tests or drop the rule.",
                )
            expected = rule.get("type")
            if expected is not None and expected not in SUPPORTED_TYPES:
                self.error(rel, f"Unsupported type '{expected}' for '{name}'")

        required = schema.get("required", [])
        if required and not isinstance(required, list):
            self.error(rel, "Schema required must be an array of field names")
        elif isinstance(required, list):
            for field in required:
                if field not in fields:
                    self.error(rel, f"Required field '{field}' is not in properties")

        return fields

    def validate_input_contract(self, contract: dict[str, str | list[str]]) -> None:
        """Check schema, questionnaire, template, and fixtures agree."""
        schema_rel = str(contract["schema"])
        schema_path = self.root / schema_rel
        question_path = self.root / str(contract["questions"])
        template_path = self.root / str(contract["template"])
        name = str(contract["name"])

        schema = self.load_schema(schema_path)
        if schema is None:
            return
        schema_fields = self.validate_schema_subset(schema_path, schema)

        if question_path.exists():
            question_fields = self.extract_question_fields(question_path)
            for field in sorted(schema_fields - question_fields):
                self.error(
                    schema_rel,
                    f"Schema field '{field}' has no question in {question_path.name}",
                )
            for field in sorted(question_fields - schema_fields):
                self.error(
                    schema_rel,
                    f"Question field '{field}' is missing from the answer schema",
                )
        else:
            self.error(str(contract["questions"]), "Question bank file not found")

        if template_path.exists():
            placeholders = self.validate_template_syntax(template_path)
            placeholders -= INTERNAL_TEMPLATE_FIELDS
            for field in sorted(schema_fields - placeholders):
                self.error(
                    schema_rel,
                    f"Schema field '{field}' has no placeholder in {template_path.name}",
                )
            for field in sorted(placeholders - schema_fields):
                self.error(
                    str(contract["template"]),
                    f"Placeholder '{{{{{field}}}}}' is missing from the answer schema",
                )
        else:
            self.error(str(contract["template"]), "Template file not found")

        for fixture_rel in contract["fixtures"]:
            fixture_path = self.root / str(fixture_rel)
            rel = str(fixture_rel)
            try:
                payload = json.loads(fixture_path.read_text(encoding="utf-8"))
            except FileNotFoundError:
                self.error(rel, "Fixture file not found")
                continue
            except json.JSONDecodeError as exc:
                self.error(rel, f"Invalid JSON: {exc}")
                continue
            if not isinstance(payload, dict):
                self.error(rel, "Fixture must be a JSON object")
                continue
            try:
                validate_answers(name, payload)
            except AnswerValidationError as exc:
                self.error(rel, str(exc))

    def check_example_consistency(
        self, example_path: Path, template_path: Path
    ):
        """Verify example output contains the same section headers as the template."""
        example = example_path.read_text(encoding='utf-8')
        template = template_path.read_text(encoding='utf-8')

        # Extract section headers from template (markdown ## headings)
        template_sections = set(re.findall(r'^## (.+)$', template, re.MULTILINE))
        example_sections = set(re.findall(r'^## (.+)$', example, re.MULTILINE))

        rel = example_path.relative_to(self.root)

        missing_sections = template_sections - example_sections
        for section in missing_sections:
            self.warn(str(rel), f"Example missing section: ## {section}")

        extra_sections = example_sections - template_sections
        for section in extra_sections:
            self.warn(str(rel), f"Example has extra section not in template: ## {section}")

    def validate_all(self, check_examples: bool = False) -> bool:
        """Run all validations. Returns True if no errors."""
        for contract in FREE_TIER_CONTRACTS:
            template_path = self.root / str(contract["template"])
            question_path = self.root / str(contract["questions"])

            if template_path.exists() and question_path.exists():
                self.validate_placeholder_field_mapping(template_path, question_path)

            self.validate_input_contract(contract)

            if check_examples:
                example_path = self.root / str(contract["example"])
                if example_path.exists() and template_path.exists():
                    self.check_example_consistency(example_path, template_path)

        return len(self.errors) == 0

    def report(self) -> int:
        """Print all errors and warnings. Returns exit code (0 = pass)."""
        for w in self.warnings:
            print(str(w))
        for e in self.errors:
            print(str(e))

        print(f"\n{len(self.errors)} error(s), {len(self.warnings)} warning(s)")

        if self.errors:
            print("VALIDATION FAILED")
            return 1
        elif self.warnings:
            print("VALIDATION PASSED (with warnings)")
            return 0
        else:
            print("VALIDATION PASSED")
            return 0


def main():
    strict = '--strict' in sys.argv
    check_examples = '--examples' in sys.argv or strict

    validator = Validator()
    validator.validate_all(check_examples=check_examples)
    sys.exit(validator.report())


if __name__ == '__main__':
    main()
