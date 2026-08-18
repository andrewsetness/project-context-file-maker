# Changelog

All notable changes to the Context File Maker project.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
