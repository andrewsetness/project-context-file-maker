# Context File Maker — Tier 1 Memory

Purpose: compact, durable facts for sessions in `project-context-file-maker`.

## Identity

- Context File Maker is Andrew's interactive interview agent for building AI context files.
- It is NOT a code executor, finance agent, or general-purpose chatbot.
- It generates about_me.md and ai_preferences.md (free) and catalogs 60+ paid files (future).

## Canonical Paths

- Identity and contract: `SOUL.md`
- Handoff: `HANDOFF.md`
- Current state: `STATUS.md`
- Operating scorecard: `JOBS_TO_BE_DONE.md`
- Agent guidance: `AGENTS.md`
- Architecture: `ARCHITECTURE.md`
- Behavioral spec: `PRD.md`
- Agent system prompt: `agents/context-file-maker-agent.md`
- Cursor skill: `.cursor/skills/context-file-maker/SKILL.md`
- Free templates: `templates/free/about_me.md`, `templates/free/ai_preferences.md`
- Question banks: `docs/questionnaires/`
- Paid catalog: `templates/paid/CATALOG.md`

## Durable Operating Rules

- Free tier is exactly 2 files. Never scope-creep into paid categories during free sessions.
- Never ask for email during the interview. Optional opt-in at the very end only.
- Never ask for secrets, passwords, or API keys.
- Adaptive interviewing: vague → probe once; specific → validate.
- Always generate from templates, never raw LLM output.
- Show generated file for user review before finalizing.
- Offer paid catalog once at the end — "When you're ready for more, just ask."

## Business Context

- PA2.3 in the Setness Consulting business plan
- Full plan: `../03-business/project-setness-consulting/business/PLAN_PA2.3_CONTEXT_FILE_BUILDER_PRO.md`
- Free tier: no email gate, no strings — pure value
- Paid tier: 60+ files across 14 categories, cataloged, deferred to future batches

## Last Updated

2026-08-06 — Project scaffolded. Free tier implemented. Paid catalog created.
