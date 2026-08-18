"""
Unit tests for the template engine.

Tests that the template engine correctly:
  - Fills simple {{field}} placeholders
  - Handles {{#field}}...{{/field}} conditional blocks
  - Omits empty/falsy optional fields
  - Cleans up whitespace from removed blocks
  - Handles edge cases (empty templates, missing fields, None values)
"""

import pytest

from template_engine import fill_template, extract_placeholders


class TestFillSimpleFields:
    """Test basic {{field}} substitution."""

    def test_single_field(self):
        result = fill_template("Hello {{name}}!", {"name": "World"})
        assert result == "Hello World!\n"

    def test_multiple_fields(self):
        template = "{{greeting}} {{name}}. You are a {{role}}."
        data = {"greeting": "Hi", "name": "Andrew", "role": "Product Manager"}
        result = fill_template(template, data)
        assert result == "Hi Andrew. You are a Product Manager.\n"

    def test_missing_field_returns_empty(self):
        result = fill_template("Hello {{name}}!", {})
        assert result == "Hello !\n"

    def test_none_field_returns_empty(self):
        result = fill_template("Hello {{name}}!", {"name": None})
        assert result == "Hello !\n"

    def test_multiline_field(self):
        template = "Bio:\n{{bio}}"
        data = {"bio": "Line 1\nLine 2\nLine 3"}
        result = fill_template(template, data)
        assert "Line 1\nLine 2\nLine 3" in result


class TestConditionalBlocks:
    """Test {{#field}}...{{/field}} conditional block handling."""

    def test_truthy_field_includes_block(self):
        template = "{{#name}}Name: {{name}}{{/name}}"
        data = {"name": "Andrew"}
        result = fill_template(template, data)
        assert "Name: Andrew" in result

    def test_falsy_field_excludes_block(self):
        template = "Before\n{{#name}}Name: {{name}}{{/name}}\nAfter"
        data = {"name": ""}
        result = fill_template(template, data)
        assert "Name:" not in result
        assert "After" in result

    def test_none_field_excludes_block(self):
        template = "Before\n{{#name}}Name: {{name}}{{/name}}\nAfter"
        data = {"name": None}
        result = fill_template(template, data)
        assert "Name:" not in result
        assert "After" in result

    def test_missing_field_excludes_block(self):
        template = "Before\n{{#name}}Name: {{name}}{{/name}}\nAfter"
        data = {}
        result = fill_template(template, data)
        assert "Name:" not in result
        assert "After" in result

    def test_whitespace_only_field_excludes_block(self):
        template = "{{#bio}}Bio: {{bio}}{{/bio}}"
        data = {"bio": "   "}
        result = fill_template(template, data)
        assert "Bio:" not in result

    def test_conditional_block_keeps_inner_placeholders(self):
        template = "{{#has_name}}**{{name}}**{{/has_name}}"
        data = {"has_name": "yes", "name": "Andrew"}
        result = fill_template(template, data)
        assert "**Andrew**" in result


class TestWhitespaceCleanup:
    """Test whitespace handling after conditional removal."""

    def test_removes_triple_blank_lines(self):
        template = "A\n\n\n{{#empty}}block{{/empty}}\n\n\nB"
        data = {"empty": ""}
        result = fill_template(template, data)
        assert "\n\n\n\n" not in result
        assert "A\n\nB" in result

    def test_strips_trailing_whitespace(self):
        result = fill_template("Hello {{name}}", {"name": "World"})
        assert result.endswith("World\n")

    def test_empty_template(self):
        result = fill_template("", {"name": "World"})
        assert result == "\n"


class TestExtractPlaceholders:
    """Test placeholder extraction from templates."""

    def test_extracts_simple_fields(self):
        template = "{{name}} is a {{role}} at {{company}}"
        placeholders = extract_placeholders(template)
        assert placeholders == {"name": False, "role": False, "company": False}

    def test_extracts_conditional_fields(self):
        template = "{{#hobbies}}{{hobbies}}{{/hobbies}}"
        placeholders = extract_placeholders(template)
        assert placeholders == {"hobbies": True}

    def test_extracts_mixed_fields(self):
        template = "**{{name}}**{{#role}} ({{role}}){{/role}}"
        placeholders = extract_placeholders(template)
        assert placeholders == {"name": False, "role": True}


class TestRealTemplates:
    """Integration-style tests using the actual project templates."""

    def test_about_me_full(self, about_me_template, about_me_answers):
        result = fill_template(about_me_template, about_me_answers)
        assert about_me_answers["full_name"] in result
        assert about_me_answers["company"] in result
        assert "## What I Do" in result
        assert "## Biggest Challenge" in result
        assert "## Goals" in result
        assert "## Technical" in result
        assert "## Preferences" in result
        assert "## Personal" in result
        assert "Favorite Tools:" in result
        assert "setnessconsulting.com" in result

    def test_about_me_minimal(self, about_me_template, about_me_minimal):
        result = fill_template(about_me_template, about_me_minimal)
        assert "Jane Minimal" in result
        assert "Software Engineer" in result
        # Optional fields should be absent
        assert "Fun Fact:" not in result
        assert "Interests:" not in result
        assert "Favorite Tools:" not in result
        assert "Tools Avoided:" not in result

    def test_about_me_omits_empty_optional_fields(self, about_me_template, about_me_answers):
        answers = dict(about_me_answers)
        answers["tools_avoid"] = ""
        result = fill_template(about_me_template, answers)
        assert "Tools Avoided:" not in result

    def test_ai_preferences_full(self, ai_preferences_template, ai_preferences_answers):
        result = fill_template(ai_preferences_template, ai_preferences_answers)
        assert "## Communication" in result
        assert "## Code Style" in result
        assert "## Naming & Patterns" in result
        assert "## Workflow" in result
        assert "## Constraints" in result
        assert "## Pet Peeves & Non-Negotiables" in result
        assert ai_preferences_answers["tone"] in result
        assert ai_preferences_answers["test_policy"] in result
        assert ai_preferences_answers["pet_peeves"] in result

    def test_ai_preferences_minimal(self, ai_preferences_template, ai_preferences_minimal):
        result = fill_template(ai_preferences_template, ai_preferences_minimal)
        assert "Casual" in result
        assert "When requested" in result
        # Optional pet peeve sections should be absent
        assert "Pet peeves:" not in result
        assert "Past frustrations:" not in result
        assert "Must-haves:" not in result
        assert "Never do:" not in result

    def test_generated_output_is_valid_markdown(self, about_me_template, about_me_answers,
                                                  ai_preferences_template, ai_preferences_answers):
        """Generated output must be syntactically valid markdown."""
        about_result = fill_template(about_me_template, about_me_answers)
        prefs_result = fill_template(ai_preferences_template, ai_preferences_answers)

        # Must start with a heading
        assert about_result.startswith('# ')
        assert prefs_result.startswith('# ')

        # Must not have unmatched {{ or }}
        assert '{{' not in about_result
        assert '}}' not in about_result
        assert '{{' not in prefs_result
        assert '}}' not in prefs_result

    def test_no_placeholders_left_unfilled(self, about_me_template, about_me_answers,
                                             ai_preferences_template, ai_preferences_answers):
        """All placeholders should be replaced — no raw {{...}} in output."""
        about_result = fill_template(about_me_template, about_me_answers)
        prefs_result = fill_template(ai_preferences_template, ai_preferences_answers)

        import re
        about_matches = re.findall(r'\{\{.*?\}\}', about_result)
        prefs_matches = re.findall(r'\{\{.*?\}\}', prefs_result)

        assert not about_matches, f"Unfilled placeholders in about_me output: {about_matches}"
        assert not prefs_matches, f"Unfilled placeholders in ai_preferences output: {prefs_matches}"
