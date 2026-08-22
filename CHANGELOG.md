# Changelog

All notable changes to the Context File Maker project.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] — 2026-08-22

### Fixed
- CLI: `--verbose` diagnostics (optional-field notes, unknown-field warnings)
  now go to **stderr** — redirecting stdout (`> file.md`) no longer corrupts
  the generated markdown
- CLI: missing optional fields are listed in sorted (deterministic) order
- CLI: a corrupt answer-schema JSON now fails validation (`--validate`)
  instead of silently skipping it
- CLI: unknown-answer-field typo warnings work even when `jsonschema` is not
  installed; non-object JSON payloads fail with a clear error instead of a
  traceback; `--json --output` writes the JSON payload to the file instead of
  silently ignoring `--output`
- Engine: inline (same-line) `{{#any:f1,f2}}...{{/any}}` blocks no longer leak
  raw syntax into output
- Engine: list/tuple values render as comma-separated text instead of Python
  repr; empty collections count as "no value" for conditionals
- Docs: corrected 8 broken business-plan path references across README,
  AGENTS, HANDOFF, PRD, docs/README, Context/MEMORY, and paid CATALOG;
  fixed stale test counts in STATUS/HANDOFF; removed stale "(v0.1)" label in
  PRD Out of Scope
- Config: fixed broken paths in `profile.yaml` (workspace, soul, tier1 user
  file) so they resolve relative to the project root

### Added
- Validator: schema↔question-bank cross-check — warns when an asked field is
  missing from its answer schema or a schema field has no question
- `scripts/common.py`: single source for optional-interview-field lists and
  Windows console setup (deduplicated from generate.py/checklist.py)
- `requirements-dev.txt` documenting test dependencies and Python 3.9+ floor
- Tests: +15 (stderr routing, deterministic ordering, inline any-blocks,
  list rendering, schema/question-bank mapping, fail-closed schemas,
  jsonschema-independent typo detection, `--json --output`, non-object
  payload rejection); jsonschema-dependent tests now skip gracefully when the
  library is absent (121 total)

## [0.2.0] — 2026-08-08

### Added
- Template engine: `{{~field}}` renders `[not provided]` for empty/missing values
- Template engine: `{{#any:f1,f2}}...{{/any}}` section gates — sections with no
  populated fields are omitted entirely (e.g. Personal, Pet Peeves)
- Template engine: line-isolated conditional blocks removed without leaving
  stray blank lines (fixes broken markdown lists)
- CLI: `--validate` flag validates answers against JSON schemas before generating
- CLI: `--json` machine-readable output mode
- CLI: `--force`/`-f` overwrite flag and interactive overwrite prompt
- CLI: `--verbose`/`-v` diagnostics (unfilled optional fields)
- CLI: UTF-8 console output on Windows (em-dashes render correctly)
- CLI: exit code 2 for validation failures
- Validator: understands `{{~field}}` and `{{#any:...}}` syntax; reuses the
  engine's tokenizer so validation can't drift from what the engine understands
- Templates: `[not provided]` affordances for missing values; conditional
  company line; section gates for Personal / Pet Peeves & Non-Negotiables
- Interviewer checklist tool (`scripts/checklist.py`): renders question-bank
  checklists and flags missing fields from partial answers
- Example outputs regenerated from the engine and enforced byte-faithful by
  both the test suite and the validator (drift guard)
- Tests: 28 new tests (missing-value placeholders, any-sections, line
  conditionals, CLI flags, checklist tool, example fidelity, unknown fields)

### Fixed
- Minimal answer payloads no longer render orphan `~`, blank labels, or empty
  section headers
- Empty optional sections (`## Personal`, `## Pet Peeves & Non-Negotiables`)
  are now omitted instead of rendering as blank headers

## [0.1.3] — 2026-08-18

### Changed
- Public clone is self-contained: removed unpublished sibling-repo plan paths and named canonical spec files in README.
- Documented license and GitHub Release process as an unresolved owner decision.

### Added
- `scripts/validate.py` now checks JSON Schema contracts against question banks, templates, and fixtures.
- Regression tests for sibling-local path leakage and schema-contract mismatches.

## [0.1.0] — 2026-08-06

### Added
- Phase 1a root documents: README.md, SOUL.md, AGENTS.md, HANDOFF.md, STATUS.md, JOBS_TO_BE_DONE.md, ARCHITECTURE.md, SKILL.md, PRD.md
- Free tier agent system prompt (`agents/context-file-maker-agent.md`)
- `about_me.md` template, question bank, and example output
- `ai_preferences.md` template, question bank, and example output
- Paid tier catalog: 60+ files across 14 categories (`templates/paid/CATALOG.md`)
- Cursor integration: `.cursor/rules/` and `.cursor/skills/`
- Agent memory: `Context/MEMORY.md`
- Template engine: `scripts/template_engine.py` (Mustache-style, conditional blocks)
- Validation tool: `scripts/validate.py` (syntax checking, placeholder-field mapping)
- CLI generator: `scripts/generate.py` (JSON → markdown)
- JSON answer schemas: `schemas/about_me_answers.schema.json`, `schemas/ai_preferences_answers.schema.json`
- Comprehensive test suite: unit tests, validation tests, integration tests
- Test fixtures: full and minimal answer payloads
- Standard project files: `profile.yaml`, `.code-workspace`, `CONTRIBUTING.md`
- GitHub repo: `andrewsetness/project-context-file-maker`

### Fixed
- Template-question bank mismatch: added `favorite_tools` and `tools_avoid` to about_me.md template (v0.1.1 patch)
- Fixed `current_projects` from Mustache block to simple text field for consistency
- Example outputs aligned to template format and URL footer