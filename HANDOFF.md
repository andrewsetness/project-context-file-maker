# Context File Maker — Handoff

**Last closeout:** 2026-08-22 (reconciliation rebase completed — reconcile-v021 pushed to GitHub)

**Repo:** `andrewsetness/project-context-file-maker`  
**Current state:** `STATUS.md`  
**Canonical sources:** `README.md` (map) and `docs/DATA-CONTRACT.md` (input/output)

## Recent session (2026-08-22 — reconciliation & test-suite fix)

The v0.2.x ↔ origin/master reconciliation was executed and finished here:

- Rebased the local v0.2 line (5 commits through v0.2.1) onto `origin/master`
  (`01a0681`) on branch **`reconcile-v021`**; conflicts resolved, all picks
  replayed, result **pushed to GitHub** (`reconcile-v021`, tip `0b45894`).
- Kept remote base (CI, synthetic fixtures `Avery Chen`, `docs/DATA-CONTRACT.md`,
  self-contained docs) and re-applied the v0.2.1 feature set (template engine,
  CLI, validator, checklist) per the documented owner decision (Option A).
- `scripts/generate.py`: schema enforcement is now **unconditional** per
  `docs/DATA-CONTRACT.md` — required/type checks run without `jsonschema`;
  `--validate` is accepted for compatibility and is a no-op.
- Removed the dead remote-only `AnswerValidationError` API test; rewrote
  `tests/test_generate_validation.py` against the `validate_answers` API.
- Dropped the dead `TestInputContractValidation` class (remote-only validator
  API); its real-project contract test moved into `TestRealProjectValidation`.
- Made CLI test assertions fixture-agnostic (synthetic `Avery Chen`, not owner
  name); regenerated `output-examples/` byte-faithful to engine output.
- **State:** 129 tests pass; `python scripts/validate.py --strict` passes
  (0 errors, 0 warnings).
- **Blockers:** none.

## Next session (top priorities)

1. Validate the free-tier conversational interview end-to-end in Cursor
   (explicit output destination, cancellation/resume) — the core remaining
   product question.
2. Owner decision: fold `reconcile-v021` into `master` (fast-forward master to
   `0b45894` and delete the branch) OR keep `reconcile-v021` as the working
   line. `master` is still at `10f6754` (old v0.2 line, 5 ahead / 13 behind
   origin).
3. Owner decision: license + GitHub Release process (unresolved; do not
   invent one).

## Resume Prompt

```
I'm continuing work on project-context-file-maker — the interview-and-generation
toolkit for AI context files.

This repository is self-contained. Do not require sibling repos to understand
or validate the product.

Current phase: v0.2.1 — free tier (about_me.md + ai_preferences.md) with
polished template output ([not provided] affordances, section gates), hardened
CLI, schema/question-bank validation, tests, and CI.

Working branch: reconcile-v021 (pushed to GitHub). master is the pre-rebase
v0.2 line and needs an owner decision on folding reconcile-v021 in.

Read STATUS.md, docs/DATA-CONTRACT.md, PRD.md, AGENTS.md, and CONTRIBUTING.md.
Use README.md for the canonical-source map. Only read interview prompt/skill
files when changing conversational UX.

Tooling:
- scripts/template_engine.py — Mustache-style template filling ({{field}},
  {{~field}} for [not provided], {{#field}} conditionals, {{#any:...}} section
  gates; inline blocks and list values supported)
- scripts/validate.py — schema/question/template/fixture contract checks +
  placeholder-field mapping; reuses the engine's tokenizer
- scripts/generate.py — CLI: JSON answers → markdown files (--validate, --json,
  --force, --verbose flags); diagnostics to stderr, markdown to stdout
- scripts/checklist.py — interview checklist from question banks
- scripts/common.py — shared optional-field config + console setup

Testing:
- pip install -r requirements-dev.txt
- python -m pytest tests/ -v  (129 tests)
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

- **Phase:** v0.2.1 — deterministic free-tier generation with polished output
- **Scope:** 2 free files (`about_me.md`, `ai_preferences.md`)
- **Paid:** cataloged in `templates/paid/CATALOG.md` — deferred
- **License/releases:** unresolved owner decision; see README

## File Map

See the project structure and canonical-source table in `README.md`. Do not maintain a second tree here.
