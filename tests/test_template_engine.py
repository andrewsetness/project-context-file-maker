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


class TestMissingValuePlaceholders:
    """Test the {{~field}} '[not provided]' syntax."""

    def test_present_field_renders_value(self):
        result = fill_template("Name: {{~name}}", {"name": "Andrew"})
        assert "Name: Andrew" in result

    def test_empty_field_renders_not_provided(self):
        result = fill_template("Name: {{~name}}", {"name": ""})
        assert "Name: [not provided]" in result

    def test_missing_field_renders_not_provided(self):
        result = fill_template("Name: {{~name}}", {})
        assert "Name: [not provided]" in result

    def test_none_field_renders_not_provided(self):
        result = fill_template("Name: {{~name}}", {"name": None})
        assert "Name: [not provided]" in result

    def test_mixed_present_and_missing(self):
        template = "- **A:** {{~a}} | **B:** {{~b}}"
        result = fill_template(template, {"a": "yes", "b": ""})
        assert "- **A:** yes | **B:** [not provided]" in result


class TestAnySections:
    """Test the {{#any:f1,f2}}...{{/any}} section syntax."""

    def test_any_true_keeps_block(self):
        template = "{{#any:hobbies,fun_fact}}## Personal\nHobby: {{hobbies}}\n{{/any}}"
        result = fill_template(template, {"hobbies": "chess"})
        assert "## Personal" in result
        assert "Hobby: chess" in result

    def test_any_false_removes_block(self):
        template = "{{#any:hobbies,fun_fact}}## Personal\nHobby: {{hobbies}}\n{{/any}}"
        result = fill_template(template, {"hobbies": "", "fun_fact": ""})
        assert "## Personal" not in result

    def test_any_with_second_field(self):
        template = "{{#any:hobbies,fun_fact}}## Personal\nFun: {{fun_fact}}\n{{/any}}"
        result = fill_template(template, {"hobbies": "", "fun_fact": "I juggle"})
        assert "## Personal" in result
        assert "I juggle" in result

    def test_any_block_removes_own_lines_cleanly(self):
        template = "Before\n{{#any:a,b}}\n## Section\n- item\n{{/any}}\nAfter"
        result = fill_template(template, {"a": "", "b": ""})
        assert "## Section" not in result
        # No stray blank lines left by the removed block
        assert "Before\n\nAfter" in result or "Before\nAfter" in result


class TestLineIsolatedConditionals:
    """Conditional blocks that sit alone on their own lines should be removed
    without leaving a blank line."""

    def test_line_conditional_removed_cleanly(self):
        template = "A\n{{#x}}\n- X: {{x}}\n{{/x}}\nB"
        result = fill_template(template, {"x": ""})
        assert "X:" not in result
        assert "A\n\nB" in result or "A\nB" in result

    def test_line_conditional_kept(self):
        template = "A\n{{#x}}\n- X: {{x}}\n{{/x}}\nB"
        result = fill_template(template, {"x": "value"})
        assert "- X: value" in result

    def test_inline_conditional_still_works(self):
        template = "**{{#x}}({{x}}){{/x}}**"
        result = fill_template(template, {"x": "Andy"})
        assert "**(Andy)**" in result

    def test_inline_conditional_removed(self):
        template = "**{{#x}}({{x}}){{/x}}**"
        result = fill_template(template, {"x": ""})
        assert "**" in result


class TestSectionGatesInRealTemplates:
    """Verify real templates use section gates so empty optional sections are
    omitted rather than rendered as blank headers."""

    def test_about_me_personal_section_omitted_when_empty(self, about_me_minimal):
        from pathlib import Path
        template = Path(__file__).resolve().parent.parent / 'templates' / 'free' / 'about_me.md'
        result = fill_template(template.read_text(encoding='utf-8'), about_me_minimal)
        assert "## Personal" not in result
        assert "## Preferences" in result  # non-optional section stays

    def test_ai_preferences_peeve_section_omitted_when_empty(self, ai_preferences_minimal):
        from pathlib import Path
        template = Path(__file__).resolve().parent.parent / 'templates' / 'free' / 'ai_preferences.md'
        result = fill_template(template.read_text(encoding='utf-8'), ai_preferences_minimal)
        assert "## Pet Peeves & Non-Negotiables" not in result

    def test_about_me_not_provided_affordance(self, about_me_minimal):
        """Minimal payloads should say [not provided] instead of leaving blank."""
        from pathlib import Path
        template = Path(__file__).resolve().parent.parent / 'templates' / 'free' / 'about_me.md'
        result = fill_template(template.read_text(encoding='utf-8'), about_me_minimal)
        assert "[not provided]" in result
        # No orphan '~' from company_size
        assert "~" not in result.replace("[not provided]", "")

    def test_no_orphan_tilde_when_company_size_missing(self):
        """A bare '~' must never appear when company_size is empty."""
        template = "- **Company Size:** {{~company_size}}"
        result = fill_template(template, {"company_size": ""})
        assert "~" not in result

    def test_company_conditional(self):
        """'at {{company}}' should be omitted when company is missing."""
        template = "- **Role:** {{job_title}}{{#company}} at {{company}}{{/company}}"
        with_company = fill_template(template, {"job_title": "PM", "company": "Acme"})
        assert "PM at Acme" in with_company
        without = fill_template(template, {"job_title": "PM", "company": ""})
        assert "PM at Acme" not in without
        assert "PM" in without

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
