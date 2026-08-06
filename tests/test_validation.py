"""
Tests for the validation/linting tool.

Tests that the validator correctly:
  - Checks template syntax for unmatched brackets
  - Maps placeholders to question bank fields
  - Reports mismatches as warnings
  - Passes on correctly-mapped templates
"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

from validate import Validator


class TestTemplateSyntaxValidation:
    """Test template syntax checking."""

    def test_valid_template_passes(self, tmp_path, project_root):
        template = tmp_path / 'valid.md'
        template.write_text('# Title\n{{field}}\n{{#opt}}optional{{/opt}}\n', encoding='utf-8')

        validator = Validator(root=tmp_path)
        placeholders = validator.validate_template_syntax(template)
        assert len(validator.errors) == 0
        assert 'field' in placeholders
        assert 'opt' in placeholders

    def test_unmatched_braces_detected(self, tmp_path):
        template = tmp_path / 'bad.md'
        template.write_text('Hello {{name', encoding='utf-8')

        validator = Validator(root=tmp_path)
        placeholders = validator.validate_template_syntax(template)
        assert len(validator.errors) > 0

    def test_unmatched_section_block_detected(self, tmp_path):
        template = tmp_path / 'bad.md'
        template.write_text('{{#name}}Hello', encoding='utf-8')  # Missing {{/name}}

        validator = Validator(root=tmp_path)
        placeholders = validator.validate_template_syntax(template)
        assert len(validator.errors) > 0


class TestQuestionFieldExtraction:
    """Test parsing question bank markdown tables."""

    def test_extracts_fields_from_table(self, tmp_path):
        qb = tmp_path / 'questions.md'
        qb.write_text("""# Questions
| # | Field | Question | Guidance |
|---|-------|----------|----------|
| 1 | name | What is your name? | — |
| 2 | role | What do you do? | — |
""", encoding='utf-8')

        validator = Validator(root=tmp_path)
        fields = validator.extract_question_fields(qb)
        assert fields == {'name', 'role'}

    def test_ignores_header_row(self, tmp_path):
        qb = tmp_path / 'questions.md'
        qb.write_text("""# Questions
| # | Field | Primary Question |
|---|-------|-----------------|
| 1 | tone | How should AI talk? |
""", encoding='utf-8')

        validator = Validator(root=tmp_path)
        fields = validator.extract_question_fields(qb)
        assert 'Field' not in fields
        assert 'tone' in fields


class TestPlaceholderFieldMapping:
    """Test the mapping between template placeholders and question bank fields."""

    def test_fully_mapped_passes(self, tmp_path):
        template = tmp_path / 'template.md'
        template.write_text('# About\n**Name:** {{name}}\n**Role:** {{role}}\n', encoding='utf-8')

        qb = tmp_path / 'questions.md'
        qb.write_text("""# Questions
| # | Field | Question |
|---|-------|----------|
| 1 | name | What is your name? |
| 2 | role | What do you do? |
""", encoding='utf-8')

        validator = Validator(root=tmp_path)
        validator.validate_placeholder_field_mapping(template, qb)
        # No errors should be raised for a perfectly mapped set
        assert len(validator.errors) == 0

    def test_extra_question_fields_warned(self, tmp_path):
        template = tmp_path / 'template.md'
        template.write_text('# About\n**Name:** {{name}}\n', encoding='utf-8')

        qb = tmp_path / 'questions.md'
        qb.write_text("""# Questions
| # | Field | Question |
|---|-------|----------|
| 1 | name | Your name? |
| 2 | role | Your role? |
""", encoding='utf-8')

        validator = Validator(root=tmp_path)
        validator.validate_placeholder_field_mapping(template, qb)
        assert len(validator.warnings) >= 1
        assert any('role' in str(w) for w in validator.warnings)

    def test_extra_template_placeholders_warned(self, tmp_path):
        template = tmp_path / 'template.md'
        template.write_text('# About\n**Name:** {{name}}\n**Tag:** {{tagline}}\n', encoding='utf-8')

        qb = tmp_path / 'questions.md'
        qb.write_text("""# Questions
| # | Field | Question |
|---|-------|----------|
| 1 | name | Your name? |
""", encoding='utf-8')

        validator = Validator(root=tmp_path)
        validator.validate_placeholder_field_mapping(template, qb)
        assert len(validator.warnings) >= 1
        assert any('tagline' in str(w) for w in validator.warnings)


class TestRealProjectValidation:
    """Test validation against the actual project files."""

    def test_about_me_template_valid(self, project_root):
        """The actual about_me.md template should pass syntax validation."""
        validator = Validator(root=project_root)
        placeholders = validator.validate_template_syntax(
            project_root / 'templates' / 'free' / 'about_me.md'
        )
        assert len(validator.errors) == 0
        assert 'full_name' in placeholders
        assert 'hobbies' in placeholders

    def test_ai_preferences_template_valid(self, project_root):
        """The actual ai_preferences.md template should pass syntax validation."""
        validator = Validator(root=project_root)
        placeholders = validator.validate_template_syntax(
            project_root / 'templates' / 'free' / 'ai_preferences.md'
        )
        assert len(validator.errors) == 0
        assert 'tone' in placeholders
        assert 'test_policy' in placeholders

    def test_validate_all_runs_without_errors(self, project_root):
        """The full validation should pass for the actual project."""
        validator = Validator(root=project_root)
        passed = validator.validate_all(check_examples=False)
        # Should pass (no errors, warnings are OK)
        assert passed

    def test_about_me_mapping_no_missing_fields(self, project_root):
        """All about_me question bank fields should have template placeholders."""
        validator = Validator(root=project_root)
        validator.validate_placeholder_field_mapping(
            project_root / 'templates' / 'free' / 'about_me.md',
            project_root / 'docs' / 'questionnaires' / 'about_me_questions.md'
        )
        # Check that favorite_tools and tools_avoid are NOT in missing warnings
        missing_warnings = [w for w in validator.warnings if 'no placeholder' in w.message.lower()]
        assert len(missing_warnings) == 0, f"Missing template placeholders: {[str(w) for w in missing_warnings]}"

    def test_ai_preferences_mapping_no_missing_fields(self, project_root):
        """All ai_preferences question bank fields should have template placeholders."""
        validator = Validator(root=project_root)
        validator.validate_placeholder_field_mapping(
            project_root / 'templates' / 'free' / 'ai_preferences.md',
            project_root / 'docs' / 'questionnaires' / 'ai_preferences_questions.md'
        )
        missing_warnings = [w for w in validator.warnings if 'no placeholder' in w.message.lower()]
        assert len(missing_warnings) == 0, f"Missing template placeholders: {[str(w) for w in missing_warnings]}"
