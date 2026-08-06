# AGENTS.md — Context File Maker

Guidance for AI agents (Cursor, Claude, Grok, etc.) working inside `project-context-file-maker`.

## Identity & Purpose

This project implements the **Context File Maker** — an interactive interview agent that helps users build structured AI context files. It is a Setness Consulting product (PA2.3 in the business plan).

The agent conducts a structured, adaptive interview and generates polished markdown files that AI assistants use to understand the user and their preferences.

## Required Reading (Start of Every Session)

1. `SOUL.md` — Identity, values, invocation, hard limits
2. `AGENTS.md` — This file — agent guidance
3. `HANDOFF.md` — Current state and workspace handoff
4. `STATUS.md` — Priorities and open items
5. `JOBS_TO_BE_DONE.md` — Operating scorecard
6. `ARCHITECTURE.md` — System design and data flow
7. `PRD.md` — Full behavioral specification
8. `.cursor/skills/context-file-maker/SKILL.md` — Execution sequence
9. `agents/context-file-maker-agent.md` — LLM system prompt (the actual interview agent prompt)
10. `templates/free/about_me.md` and `templates/free/ai_preferences.md` — Output templates

## Core Mandate

- **Free tier first.** Implement the free tier interviews (about_me.md, ai_preferences.md) as the v0.1 deliverable.
- **Adaptive interview.** Questions adapt based on user responses. Vague answers get follow-up probes. Specific answers get validated and summarized back.
- **Template-driven output.** Always generate markdown from the structured templates in `templates/`, not from raw LLM output.
- **No email gate.** Free tier is completely free. There is a voluntary "send me a copy" button option at the end — never ask for email during the interview.
- **Respect phases.** v0.1 = free tier only. Paid tier catalog exists in `templates/paid/CATALOG.md` but implementation is deferred to future batches.
- **Keep handoff fresh.** Update `STATUS.md` and `HANDOFF.md` after meaningful changes.

## Documentation Standards

Maintain the Phase 1a standard root documents:
`README.md`, `SOUL.md`, `AGENTS.md`, `HANDOFF.md`, `STATUS.md`, `JOBS_TO_BE_DONE.md`, `ARCHITECTURE.md`

Keep supporting docs in `docs/` with `docs/README.md` as the index.

## Business Context

Full business plan at `../03-business/project-setness-consulting/business/PLAN_PA2.3_CONTEXT_FILE_BUILDER_PRO.md`.

Free tier: 2 files (about_me.md, ai_preferences.md) — no email gate, no strings.
Paid tier (future): 60+ files across 14 categories, cataloged in `templates/paid/CATALOG.md`.
