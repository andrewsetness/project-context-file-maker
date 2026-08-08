# AGENTS.md — Context File Maker

Guidance for AI agents (Cursor, Claude, Grok, etc.) working inside `project-context-file-maker`.

## Identity & Purpose

This project implements the **Context File Maker** — an interview-and-generation toolkit for structured AI context files. It is a Setness Consulting product. This repository is the product source of truth; do not require unpublished sibling repos or business-plan files to understand or validate it.

The interview layer asks questions and produces JSON answers. The generator validates those answers against `schemas/` and renders `templates/free/`.

## Required Reading (Start of Every Session)

1. `STATUS.md` — what is actually implemented now
2. `docs/DATA-CONTRACT.md` — input/output/privacy authority
3. `PRD.md` — product behavior and free-tier requirements
4. `AGENTS.md` — this file
5. `SOUL.md` and `.cursor/skills/context-file-maker/SKILL.md` — only when changing interview identity or UX

Canonical field/output sources are listed in `README.md`. Do not invent a second spec in session notes.

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

## Product Context

Free tier: 2 files (`about_me.md`, `ai_preferences.md`) — no email gate, no strings.
Paid tier (future): 60+ files across 14 categories, cataloged in `templates/paid/CATALOG.md`.

Commercial planning that lives outside this repository is optional context for the owner. It is not required to clone, understand, or validate the product.

## Agent Behavior

- Think before coding: surface assumptions when interview behavior is ambiguous; never invent product decisions (free tier first, see Core Mandate).
- Surgical changes: output must stay template-driven — change templates only when the task requires (see Core Mandate).
- Verify before claiming done: run the interview flow and show the generated files before declaring completion.
