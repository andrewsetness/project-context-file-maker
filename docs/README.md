# Context File Maker — Documentation Index

All supporting documentation for the project.

## Core Docs

This repository is self-contained. Start with the canonical-source table in `../README.md`.

| Doc | Path | Purpose |
|-----|------|---------|
| Canonical source map | `../README.md` | Which file owns which concern |
| Data contract | `DATA-CONTRACT.md` | Input/output, privacy, examples |
| PRD | `../PRD.md` | Product requirements |
| Status | `../STATUS.md` | What is implemented now |
| Architecture | `../ARCHITECTURE.md` | System design (narrative; defer to the data contract) |

## Interview Resources

| Doc | Path | Purpose |
|-----|------|---------|
| about_me.md Question Bank | `questionnaires/about_me_questions.md` | Full question list with adaptive follow-ups |
| ai_preferences.md Question Bank | `questionnaires/ai_preferences_questions.md` | Full question list with options and guidance |

## Templates

| Template | Path | Purpose |
|----------|------|---------|
| about_me.md | `../templates/free/about_me.md` | Output template for about_me.md |
| ai_preferences.md | `../templates/free/ai_preferences.md` | Output template for ai_preferences.md |
| Paid Catalog | `../templates/paid/CATALOG.md` | Full paid tier catalog (60+ files, 14 categories) |

## Agent Config

| File | Path | Purpose |
|------|------|---------|
| Agent System Prompt | `../agents/context-file-maker-agent.md` | LLM system prompt |
| Cursor Skill | `../.cursor/skills/context-file-maker/SKILL.md` | Cursor execution protocol |
| Cursor Rule | `../.cursor/rules/context-file-maker-core.mdc` | Cursor auto-load rule |

## Examples

| File | Path | Purpose |
|------|------|---------|
| about_me Example | `../output-examples/about_me_example.md` | Example generated about_me.md |
| ai_preferences Example | `../output-examples/ai_preferences_example.md` | Example generated ai_preferences.md |

## Tooling

| Tool | Path | Purpose |
|------|------|---------|
| Template Engine | `../scripts/template_engine.py` | Mustache-style template filling (`{{field}}`, `{{~field}}`, `{{#field}}`, `{{#any:...}}`) |
| Validator | `../scripts/validate.py` | Template/question-bank consistency checks, schema/question-bank cross-check, example drift guard |
| CLI Generator | `../scripts/generate.py` | JSON answers → markdown context files (`--validate`, `--json`, `--force`, `--verbose`) |
| Interview Checklist | `../scripts/checklist.py` | Renders question-bank checklists; flags missing fields from partial answers |
| Shared CLI Config | `../scripts/common.py` | Single source for optional-field lists and Windows console setup |
| Answer Schemas | `../schemas/` | JSON schema validation for answer payloads |

## Dev Setup

| File | Path | Purpose |
|------|------|---------|
| Test dependencies | `../requirements-dev.txt` | `pip install -r requirements-dev.txt` (pytest, jsonschema) |
