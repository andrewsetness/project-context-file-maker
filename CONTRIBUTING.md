# Contributing to Context File Maker

Thanks for contributing. This repository is self-contained: a clone plus the commands below is enough to understand and validate the product.

## Phase 1a Document Standards

Every change should keep these 7 root documents current:
- `README.md` — Quick start and project map
- `SOUL.md` — Identity and operating contract
- `AGENTS.md` — Agent guidance
- `HANDOFF.md` — Session handoff
- `STATUS.md` — Current state and open items
- `JOBS_TO_BE_DONE.md` — Operating scorecard
- `ARCHITECTURE.md` — System design

## Development Setup

Requires **Python 3.9+**.

```bash
# Clone the repo
git clone https://github.com/andrewsetness/project-context-file-maker.git

# Install test dependencies (jsonschema is used by fixture tests;
# scripts/generate.py itself is dependency-free)
pip install -r requirements-dev.txt
# (equivalent: pip install pytest jsonschema)

# Run tests
python -m pytest tests/ -v

# Run validation
python scripts/validate.py

# Run validation with examples check
python scripts/validate.py --strict
```

## Code Conventions

- Python: Follow PEP 8. Use type hints where practical.
- Markdown: Standard markdown. Templates use Mustache-like `{{field}}` syntax.
- Commits: Conventional Commits format (`feat:`, `fix:`, `docs:`, `test:`, `chore:`)

## Adding New Templates

1. Create the template in `templates/free/` or `templates/paid/`
2. Create the question bank in `docs/questionnaires/`
3. Add a JSON schema in `schemas/`
4. Add test fixtures in `tests/fixtures/`
5. Add tests in `tests/`
6. Update `templates/paid/CATALOG.md` if paid
7. If you change a template or fixture, regenerate the example outputs so
   they stay byte-faithful to engine output:
   ```bash
   python scripts/generate.py about_me --answers tests/fixtures/about_me_answers.json --output output-examples/about_me_example.md --force
   python scripts/generate.py ai_preferences --answers tests/fixtures/ai_preferences_answers.json --output output-examples/ai_preferences_example.md --force
   ```
8. Run `python scripts/validate.py --strict`
9. Run `python -m pytest tests/ -v`

## Interviewer Checklist Tool

`scripts/checklist.py` renders the full interview checklist from the question
banks and can flag missing fields against a partial answers file:

```bash
python scripts/checklist.py about_me --answers data/partial.json
```

## Running the Test Suite

```bash
# All tests
python -m pytest tests/ -v

# Template engine tests only
python -m pytest tests/test_template_engine.py -v

# Validation tests only
python -m pytest tests/test_validation.py -v

# Integration tests only
python -m pytest tests/test_integration.py -v
```

## Validation

Before committing, always run:
```bash
python scripts/validate.py --strict
python -m pytest tests/ -v
```

Both must pass. The validator checks JSON Schema contracts, template syntax, and placeholder-field mapping. The test suite covers template engine correctness, validation logic, and end-to-end generation. CI runs the same two commands on `master`.

## License

License and GitHub Release process are an unresolved owner decision. Do not add a LICENSE file or invent reuse terms. See `README.md`.
