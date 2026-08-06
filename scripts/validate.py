#!/usr/bin/env python3
"""
Context File Maker — Validator

Checks template-question bank consistency:
  - All question bank fields have corresponding template placeholders
  - All template placeholders have corresponding question bank fields
  - Templates have valid syntax
  - Example outputs are consistent with templates

Usage:
    python scripts/validate.py
    python scripts/validate.py --strict  # also check example outputs
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


PROJECT_ROOT = Path(__file__).resolve().parent.parent


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
        # Skip common template-internal fields
        internal_fields = {'name', 'description'}
        missing_in_question = placeholders - fields - internal_fields
        for field in sorted(missing_in_question):
            self.warn(str(rel_t),
                      f"Placeholder '{{{{{field}}}}}' has no question in {rel_q.name}")

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
        # Templates and their question banks
        mappings = [
            ('templates/free/about_me.md', 'docs/questionnaires/about_me_questions.md'),
            ('templates/free/ai_preferences.md', 'docs/questionnaires/ai_preferences_questions.md'),
        ]

        for template_rel, question_rel in mappings:
            template_path = self.root / template_rel
            question_path = self.root / question_rel

            if not template_path.exists():
                self.error(template_rel, "Template file not found")
                continue
            if not question_path.exists():
                self.error(question_rel, "Question bank file not found")
                continue

            self.validate_placeholder_field_mapping(template_path, question_path)

        # Check example outputs
        if check_examples:
            example_mappings = [
                ('output-examples/about_me_example.md', 'templates/free/about_me.md'),
                ('output-examples/ai_preferences_example.md', 'templates/free/ai_preferences.md'),
            ]
            for ex_rel, tmpl_rel in example_mappings:
                ex_path = self.root / ex_rel
                tmpl_path = self.root / tmpl_rel
                if ex_path.exists() and tmpl_path.exists():
                    self.check_example_consistency(ex_path, tmpl_path)

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
