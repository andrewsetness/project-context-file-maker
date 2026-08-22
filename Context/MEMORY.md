# Context File Maker — Tier 1 Memory

Purpose: compact, durable facts for sessions in `project-context-file-maker`.

## Identity

- Context File Maker is Andrew's interactive interview agent for building AI context files.
- It is NOT a code executor, finance agent, or general-purpose chatbot.
- It generates about_me.md and ai_preferences.md (free) and catalogs 60+ paid files (future).

## Canonical Paths

See `README.md` for the full source map. Do not treat this list as a second spec.

- Current state: `STATUS.md`
- Input/output/privacy: `docs/DATA-CONTRACT.md`
- Product behavior: `PRD.md`
- Interview identity: `SOUL.md`
- Answer schemas: `schemas/`
- Question banks: `docs/questionnaires/`
- Free templates: `templates/free/`

## Durable Operating Rules

- Free tier is exactly 2 files. Never scope-creep into paid categories during free sessions.
- Never ask for email during the interview. Optional opt-in at the very end only.
- Never ask for secrets, passwords, or API keys.
- Adaptive interviewing: vague → probe once; specific → validate.
- Always generate from templates, never raw LLM output.
- Show generated file for user review before finalizing.
- Offer paid catalog once at the end — "When you're ready for more, just ask."

## Product Context

- Setness Consulting product for building AI context files
- This repository is the product source of truth; sibling business-plan files are not required
- Free tier: no email gate, no strings — pure value
- Paid tier: 60+ files across 14 categories, cataloged, deferred to future batches

## Last Updated

2026-08-22 — Reconciliation completed on `reconcile-v021` (pushed to GitHub); schema enforcement is unconditional per DATA-CONTRACT; 129 tests + `validate.py --strict` green. Owner decision pending: fold reconcile-v021 into master.
2026-08-18 — Removed sibling-repo plan path. Canonical sources live in README.md.
