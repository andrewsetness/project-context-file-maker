"""
Integration tests for the Context File Maker system.

Tests end-to-end flows:
  - Full template generation from fixture data
  - Round-trip: JSON → markdown (valid, complete)
  - Example output consistency with templates
  - Schema validation against answer fixtures
  - CLI tool behavior
"""

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

from template_engine import fill_template


class TestEndToEndGeneration:
    """Full integration tests from fixture data → markdown output."""

    def test_about_me_generation_complete(self, about_me_template, about_me_answers):
        """Generate about_me.md from full fixture data and verify all sections."""
        result = fill_template(about_me_template, about_me_answers)

        required_sections = [
            '## Identity',
            '## What I Do',
            '## Current Focus',
            '## Biggest Challenge',
            '## Goals',
            '## Technical',
            '## Preferences',
            '## Personal',
        ]
        for section in required_sections:
            assert section in result, f"Missing section: {section}"

    def test_about_me_contains_all_filled_fields(self, about_me_template, about_me_answers):
        """Every required field value should appear in the output."""
        result = fill_template(about_me_template, about_me_answers)

        for key, value in about_me_answers.items():
            if value is None or key in ('preferred_name',):
                continue
            # The value or a reasonable substring should appear
            if isinstance(value, str) and len(value) > 3:
                # Check at least the first 20 chars appear
                snippet = value[:20]
                assert snippet in result, f"Value for '{key}' not found: '{snippet}'"

    def test_ai_preferences_generation_complete(self, ai_preferences_template, ai_preferences_answers):
        """Generate ai_preferences.md from full fixture data and verify all sections."""
        result = fill_template(ai_preferences_template, ai_preferences_answers)

        required_sections = [
            '## Communication',
            '## Code Style',
            '## Naming & Patterns',
            '## Workflow',
            '## Constraints',
            '## Pet Peeves & Non-Negotiables',
        ]
        for section in required_sections:
            assert section in result, f"Missing section: {section}"

    def test_ai_preferences_contains_all_filled_fields(self, ai_preferences_template, ai_preferences_answers):
        """Every required field value should appear in the output."""
        result = fill_template(ai_preferences_template, ai_preferences_answers)

        for key, value in ai_preferences_answers.items():
            if value is None:
                continue
            if isinstance(value, str) and len(value) > 3:
                snippet = value[:20]
                assert snippet in result, f"Value for '{key}' not found: '{snippet}'"


class TestExampleOutputConsistency:
    """Verify example outputs are consistent with generated outputs."""

    def test_example_about_me_matches_template_sections(self, project_root):
        """The example about_me.md should have the same sections as a generated file."""
        example = (project_root / 'output-examples' / 'about_me_example.md').read_text(encoding='utf-8')
        template = (project_root / 'templates' / 'free' / 'about_me.md').read_text(encoding='utf-8')

        import re
        template_sections = set(re.findall(r'^## (.+)$', template, re.MULTILINE))
        example_sections = set(re.findall(r'^## (.+)$', example, re.MULTILINE))

        missing = template_sections - example_sections
        assert not missing, f"Example missing sections: {missing}"

    def test_example_ai_preferences_matches_template_sections(self, project_root):
        """The example ai_preferences.md should have the same sections as a generated file."""
        example = (project_root / 'output-examples' / 'ai_preferences_example.md').read_text(encoding='utf-8')
        template = (project_root / 'templates' / 'free' / 'ai_preferences.md').read_text(encoding='utf-8')

        import re
        template_sections = set(re.findall(r'^## (.+)$', template, re.MULTILINE))
        example_sections = set(re.findall(r'^## (.+)$', example, re.MULTILINE))

        missing = template_sections - example_sections
        assert not missing, f"Example missing sections: {missing}"


class TestSchemaValidation:
    """Test JSON answer fixtures against their schemas."""

    def test_about_me_fixture_valid(self, about_me_answers, project_root):
        schema_path = project_root / 'schemas' / 'about_me_answers.schema.json'
        schema = json.loads(schema_path.read_text(encoding='utf-8'))

        import jsonschema
        jsonschema.validate(about_me_answers, schema)

    def test_ai_preferences_fixture_valid(self, ai_preferences_answers, project_root):
        schema_path = project_root / 'schemas' / 'ai_preferences_answers.schema.json'
        schema = json.loads(schema_path.read_text(encoding='utf-8'))

        import jsonschema
        jsonschema.validate(ai_preferences_answers, schema)

    def test_minimal_about_me_fixture_valid(self, about_me_minimal, project_root):
        schema_path = project_root / 'schemas' / 'about_me_answers.schema.json'
        schema = json.loads(schema_path.read_text(encoding='utf-8'))

        import jsonschema
        jsonschema.validate(about_me_minimal, schema)

    def test_minimal_ai_preferences_fixture_valid(self, ai_preferences_minimal, project_root):
        schema_path = project_root / 'schemas' / 'ai_preferences_answers.schema.json'
        schema = json.loads(schema_path.read_text(encoding='utf-8'))

        import jsonschema
        jsonschema.validate(ai_preferences_minimal, schema)


class TestCLIInterface:
    """Test the CLI generate tool."""

    def test_generate_about_me_stdout(self, tmp_path, about_me_answers, capsys):
        import subprocess

        answers_file = tmp_path / 'answers.json'
        answers_file.write_text(json.dumps(about_me_answers))

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert 'Andrew Setness' in result.stdout

    def test_generate_to_file(self, tmp_path, about_me_answers):
        import subprocess

        answers_file = tmp_path / 'answers.json'
        answers_file.write_text(json.dumps(about_me_answers))
        output_file = tmp_path / 'output.md'

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file), '--output', str(output_file)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert output_file.exists()
        content = output_file.read_text(encoding='utf-8')
        assert 'Andrew Setness' in content

    def test_generate_both_files(self, tmp_path, about_me_answers, ai_preferences_answers):
        import subprocess

        about_file = tmp_path / 'about.json'
        prefs_file = tmp_path / 'prefs.json'
        about_file.write_text(json.dumps(about_me_answers))
        prefs_file.write_text(json.dumps(ai_preferences_answers))
        outdir = tmp_path / 'output'
        outdir.mkdir()

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'all', '--about', str(about_file), '--prefs', str(prefs_file),
             '--outdir', str(outdir)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert (outdir / 'about_me.md').exists()
        assert (outdir / 'ai_preferences.md').exists()

    def test_generate_handles_missing_file(self):
        import subprocess

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', '/nonexistent/path.json'],
            capture_output=True, text=True
        )
        assert result.returncode != 0


class TestFileIntegrity:
    """Verify that all expected files exist and are non-empty."""

    REQUIRED_FILES = [
        'README.md', 'SOUL.md', 'AGENTS.md', 'HANDOFF.md', 'STATUS.md',
        'JOBS_TO_BE_DONE.md', 'ARCHITECTURE.md', 'SKILL.md', 'PRD.md',
        '.gitignore',
        'agents/context-file-maker-agent.md',
        'templates/free/about_me.md',
        'templates/free/ai_preferences.md',
        'templates/paid/CATALOG.md',
        'docs/README.md',
        'docs/questionnaires/about_me_questions.md',
        'docs/questionnaires/ai_preferences_questions.md',
        'Context/MEMORY.md',
        'output-examples/about_me_example.md',
        'output-examples/ai_preferences_example.md',
        '.cursor/rules/context-file-maker-core.mdc',
        '.cursor/skills/context-file-maker/SKILL.md',
        'scripts/template_engine.py',
        'scripts/validate.py',
        'scripts/generate.py',
        'schemas/about_me_answers.schema.json',
        'schemas/ai_preferences_answers.schema.json',
    ]

    @pytest.mark.parametrize('filepath', REQUIRED_FILES)
    def test_file_exists_and_nonempty(self, project_root, filepath):
        full_path = project_root / filepath
        assert full_path.exists(), f"Missing: {filepath}"
        content = full_path.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, f"Empty: {filepath}"
