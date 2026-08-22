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

# scripts dir is already importable via conftest; this is for subprocess paths.
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'

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
            if isinstance(value, str) and len(value) > 3:
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


class TestExampleOutputsAreGenerated:
    """Example outputs must be byte-faithful to the engine output, so they
    can't drift from what users actually get."""

    def test_about_me_example_is_generated_output(self, project_root, about_me_answers):
        from pathlib import Path
        from template_engine import fill_template

        template = (project_root / 'templates' / 'free' / 'about_me.md').read_text(encoding='utf-8')
        generated = fill_template(template, about_me_answers)
        example = (project_root / 'output-examples' / 'about_me_example.md').read_text(encoding='utf-8')
        assert example == generated, "about_me_example.md drifted from engine output — regenerate it"

    def test_ai_preferences_example_is_generated_output(self, project_root, ai_preferences_answers):
        from pathlib import Path
        from template_engine import fill_template

        template = (project_root / 'templates' / 'free' / 'ai_preferences.md').read_text(encoding='utf-8')
        generated = fill_template(template, ai_preferences_answers)
        example = (project_root / 'output-examples' / 'ai_preferences_example.md').read_text(encoding='utf-8')
        assert example == generated, "ai_preferences_example.md drifted from engine output — regenerate it"


class TestSchemaValidation:
    """Test JSON answer fixtures against their schemas."""

    def test_about_me_fixture_valid(self, about_me_answers, project_root):
        jsonschema = pytest.importorskip('jsonschema')
        schema_path = project_root / 'schemas' / 'about_me_answers.schema.json'
        schema = json.loads(schema_path.read_text(encoding='utf-8'))

        jsonschema.validate(about_me_answers, schema)

    def test_ai_preferences_fixture_valid(self, ai_preferences_answers, project_root):
        jsonschema = pytest.importorskip('jsonschema')
        schema_path = project_root / 'schemas' / 'ai_preferences_answers.schema.json'
        schema = json.loads(schema_path.read_text(encoding='utf-8'))

        jsonschema.validate(ai_preferences_answers, schema)

    def test_minimal_about_me_fixture_valid(self, about_me_minimal, project_root):
        jsonschema = pytest.importorskip('jsonschema')
        schema_path = project_root / 'schemas' / 'about_me_answers.schema.json'
        schema = json.loads(schema_path.read_text(encoding='utf-8'))

        jsonschema.validate(about_me_minimal, schema)

    def test_minimal_ai_preferences_fixture_valid(self, ai_preferences_minimal,
                                                  project_root):
        jsonschema = pytest.importorskip('jsonschema')
        schema_path = project_root / 'schemas' / 'ai_preferences_answers.schema.json'
        schema = json.loads(schema_path.read_text(encoding='utf-8'))

        jsonschema.validate(ai_preferences_minimal, schema)


class TestCLIInterface:
    """Test the CLI generate tool."""

    def test_generate_about_me_stdout(self, tmp_path, about_me_answers):
        import subprocess

        answers_file = tmp_path / 'answers.json'
        answers_file.write_text(json.dumps(about_me_answers), encoding='utf-8')

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert about_me_answers['full_name'] in result.stdout

    def test_generate_to_file(self, tmp_path, about_me_answers):
        import subprocess

        answers_file = tmp_path / 'answers.json'
        answers_file.write_text(json.dumps(about_me_answers), encoding='utf-8')
        output_file = tmp_path / 'output.md'

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file), '--output', str(output_file)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert output_file.exists()
        content = output_file.read_text(encoding='utf-8')
        assert about_me_answers['full_name'] in content

    def test_generate_both_files(self, tmp_path, about_me_answers, ai_preferences_answers):
        import subprocess

        about_file = tmp_path / 'about.json'
        prefs_file = tmp_path / 'prefs.json'
        about_file.write_text(json.dumps(about_me_answers), encoding='utf-8')
        prefs_file.write_text(json.dumps(ai_preferences_answers), encoding='utf-8')
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

    def test_generate_with_validation_passes(self, tmp_path, about_me_answers):
        """--validate should accept a schema-valid payload."""
        import subprocess

        answers_file = tmp_path / 'answers.json'
        answers_file.write_text(json.dumps(about_me_answers))

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file), '--validate'],
            capture_output=True, text=True
        )
        assert result.returncode == 0

    def test_generate_validation_failure_exit_code(self, tmp_path):
        """Invalid answers (missing required field) should exit 2."""
        pytest.importorskip('jsonschema')
        import subprocess

        bad_file = tmp_path / 'bad.json'
        bad_file.write_text(json.dumps({'full_name': 'Incomplete'}))

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(bad_file), '--validate'],
            capture_output=True, text=True
        )
        assert result.returncode == 2
        assert 'Validation error' in result.stderr

    def test_generate_json_mode(self, tmp_path, about_me_answers):
        """--json should emit a machine-readable payload with the file content."""
        import subprocess

        answers_file = tmp_path / 'answers.json'
        answers_file.write_text(json.dumps(about_me_answers))

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file), '--json'],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        payload = json.loads(result.stdout)
        assert payload['name'] == 'about_me.md'
        assert 'Andrew Setness' in payload['file']

    def test_generate_force_overwrites(self, tmp_path, about_me_answers):
        """--force should overwrite an existing output file."""
        import subprocess

        answers_file = tmp_path / 'answers.json'
        answers_file.write_text(json.dumps(about_me_answers))
        output_file = tmp_path / 'output.md'
        output_file.write_text('old content')

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file),
             '--output', str(output_file), '--force'],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert 'Andrew Setness' in output_file.read_text(encoding='utf-8')

    def test_generate_warns_on_unknown_fields(self, tmp_path):
        """Typo'd answer keys should produce a verbose warning on stderr."""
        import subprocess

        answers_file = tmp_path / 'answers.json'
        answers_file.write_text(json.dumps({
            'full_name': 'A', 'full_naem': 'B',  # typo
            'job_title': 'X', 'primary_work': 'Y', 'biggest_challenge': 'Z',
        }))

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file),
             '--validate', '--verbose'],
            capture_output=True, text=True, encoding='utf-8'
        )
        assert result.returncode == 0
        assert 'unknown answer fields' in result.stderr
        assert 'full_naem' in result.stderr

    def test_verbose_notes_do_not_pollute_stdout(self, tmp_path, about_me_minimal):
        """Verbose diagnostics must go to stderr so stdout stays clean
        markdown even when output is redirected to a file."""
        import subprocess

        answers_file = tmp_path / 'minimal.json'
        answers_file.write_text(json.dumps(about_me_minimal))

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file), '--verbose'],
            capture_output=True, text=True, encoding='utf-8'
        )
        assert result.returncode == 0
        assert 'Note: optional fields not provided' in result.stderr
        assert 'Note:' not in result.stdout
        assert result.stdout.startswith('# About Me')

    def test_missing_optional_fields_sorted_deterministically(self, tmp_path,
                                                              about_me_minimal):
        """The missing-optional note should list fields in sorted order."""
        import subprocess

        answers_file = tmp_path / 'minimal.json'
        answers_file.write_text(json.dumps(about_me_minimal))

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file), '--verbose'],
            capture_output=True, text=True, encoding='utf-8'
        )
        line = next(l for l in result.stderr.splitlines()
                    if l.startswith('Note: optional fields'))
        fields = line.split('not provided: ', 1)[1].split(', ')
        assert fields == sorted(fields)

    def test_rejects_non_object_answers_json(self, tmp_path):
        """A JSON array/string payload should fail with a clear error."""
        import subprocess

        bad_file = tmp_path / 'list.json'
        bad_file.write_text('["not", "answers"]')

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(bad_file)],
            capture_output=True, text=True, encoding='utf-8'
        )
        assert result.returncode != 0
        assert 'JSON object' in result.stderr

    def test_generate_json_mode_with_output_writes_payload(self, tmp_path,
                                                           about_me_answers):
        """--json --output writes the JSON payload to the file."""
        import subprocess

        answers_file = tmp_path / 'answers.json'
        answers_file.write_text(json.dumps(about_me_answers))
        output_file = tmp_path / 'payload.json'

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'generate.py'),
             'about_me', '--answers', str(answers_file), '--json',
             '--output', str(output_file)],
            capture_output=True, text=True, encoding='utf-8'
        )
        assert result.returncode == 0
        payload = json.loads(output_file.read_text(encoding='utf-8'))
        assert payload['name'] == 'about_me.md'
        assert 'Andrew Setness' in payload['file']

    def test_validate_answers_fails_closed_on_broken_schema(self, tmp_path,
                                                            monkeypatch):
        """A corrupt schema JSON must fail validation, not skip it."""
        import generate

        broken_schema = tmp_path / 'broken.schema.json'
        broken_schema.write_text('{not valid json', encoding='utf-8')
        monkeypatch.setitem(generate.SCHEMAS, 'about_me', broken_schema)

        valid, msgs = generate.validate_answers('about_me', {'full_name': 'X'})
        assert not valid
        assert msgs and 'Invalid schema JSON' in msgs[0]

    def test_validate_answers_warns_unknown_fields_without_jsonschema(
            self, tmp_path, monkeypatch, capsys):
        """Typo detection must work even when jsonschema is unavailable."""
        import generate

        schema = tmp_path / 'mini.schema.json'
        schema.write_text(json.dumps({
            'type': 'object',
            'properties': {'full_name': {'type': 'string'}},
        }), encoding='utf-8')
        monkeypatch.setitem(generate.SCHEMAS, 'about_me', schema)
        monkeypatch.setitem(sys.modules, 'jsonschema', None)  # forces ImportError

        valid, msgs = generate.validate_answers(
            'about_me', {'full_name': 'X', 'full_naem': 'typo'}, verbose=True)
        captured = capsys.readouterr()
        assert valid and msgs == []
        assert 'skipping schema validation' in captured.err
        assert 'unknown answer fields' in captured.err
        assert 'full_naem' in captured.err


class TestChecklistTool:
    """Test the interviewer checklist tool."""

    def test_checklist_parses_all_questions(self, project_root):
        import subprocess

        result = subprocess.run(
            [sys.executable, str(project_root / 'scripts' / 'checklist.py'), 'about_me'],
            capture_output=True, text=True, encoding='utf-8'
        )
        assert result.returncode == 0
        assert 'interview checklist' in result.stdout
        assert 'What name should AI assistants use for you?' in result.stdout
        assert '24 questions' in result.stdout

    def test_checklist_flags_missing_fields(self, project_root, tmp_path, about_me_minimal):
        import subprocess

        answers_file = tmp_path / 'partial.json'
        answers_file.write_text(json.dumps(about_me_minimal))

        result = subprocess.run(
            [sys.executable, str(project_root / 'scripts' / 'checklist.py'),
             'about_me', '--answers', str(answers_file)],
            capture_output=True, text=True, encoding='utf-8'
        )
        assert result.returncode == 0
        assert 'Missing required fields' in result.stdout
        assert 'tech_stack' in result.stdout

    def test_checklist_all_reports_both(self, project_root):
        import subprocess

        result = subprocess.run(
            [sys.executable, str(project_root / 'scripts' / 'checklist.py'), 'all'],
            capture_output=True, text=True, encoding='utf-8'
        )
        assert result.returncode == 0
        assert 'about_me \u2014 interview checklist' in result.stdout
        assert 'ai_preferences \u2014 interview checklist' in result.stdout


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
        'docs/DATA-CONTRACT.md',
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
