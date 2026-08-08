# Context File Maker — Handoff

# Context File Maker — Handoff

**Repo:** `andrewsetness/project-context-file-maker`  
**Current state:** `STATUS.md`  
**Canonical sources:** `README.md` (map) and `docs/DATA-CONTRACT.md` (input/output)

## Resume Prompt

```
I'm continuing work on project-context-file-maker — the interview-and-generation
toolkit for AI context files.

This repository is self-contained. Do not require sibling repos to understand
or validate the product.

Current phase: v0.1.3 — free tier (about_me.md + ai_preferences.md) with
schema-validated generation, validator, tests, and CI.

Read STATUS.md, docs/DATA-CONTRACT.md, PRD.md, AGENTS.md, and CONTRIBUTING.md.
Use README.md for the canonical-source map. Only read interview prompt/skill
files when changing conversational UX.

Tooling:
- scripts/template_engine.py — Mustache-style template filling
- scripts/validate.py — schema/question/template/fixture contract checks
- scripts/generate.py — CLI: JSON answers → markdown files

Testing:
- python -m pytest -q
- python scripts/validate.py --strict

The paid tier catalog exists in templates/paid/CATALOG.md but implementation
is deferred until the free-tier interview path is proven.
```

## How to Start a Chat

Open this project and say one of:

- `build my context files` — Full free tier interview
- `create an about me file` — about_me.md only
- `create ai preferences` — ai_preferences.md only
- `show paid catalog` — Browse paid tier catalog

The `context-file-maker-core.mdc` rule loads automatically and points to `SOUL.md`.

## Current State

See `STATUS.md`. This file is session orientation only; do not copy product rules here.

- **Phase:** v0.1.3 — deterministic free-tier generation implemented
- **Scope:** 2 free files (`about_me.md`, `ai_preferences.md`)
- **Paid:** cataloged in `templates/paid/CATALOG.md` — deferred
- **License/releases:** unresolved owner decision; see README

## File Map

See the project structure and canonical-source table in `README.md`. Do not maintain a second tree here.
