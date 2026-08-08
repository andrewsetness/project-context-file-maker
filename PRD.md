# PRD — Context File Maker

**Version:** 1.0
**Version:** 1.0
**Status:** v0.2.1 implementation active
**Last updated:** 2026-08-22

This file is the canonical product-behavior spec (user stories, functional/non-functional requirements, out of scope). It is not the field/output contract.

- Interview questions: `docs/questionnaires/`
- Answer JSON: `schemas/`
- Output structure: `templates/free/`
- Privacy/output rules: `docs/DATA-CONTRACT.md`
- Current implementation state: `STATUS.md`

## Problem

AI coding assistants (Cursor, Claude Code, Copilot, Windsurf, etc.) perform dramatically better when they have structured context about the user — who they are, what they do, how they prefer to work. But most users don't know:
- What context files an AI agent can consume
- How to structure those files effectively
- What's even possible to configure

The result: AI agents start every session blind. Users re-explain themselves constantly. The quality gap between a well-configured agent and a blank-slate agent is immense — and mostly unexploited.

## Solution

**Context File Maker** — an interactive interview agent that interviews users and generates polished, structured markdown context files.

### Free Tier (v0.1)
- `about_me.md` — 4-phase interview covering identity, work, technical, and personal context
- `ai_preferences.md` — 5-section interview covering communication, code, workflow, constraints, and pet peeves
- No email gate. No account. Pure value.

### Paid Tier (Future Batches)
- 60+ context files across 14 categories
- Agent soul, session continuity, memory architecture, agent profiles, project foundation, code conventions, decisions, policies, skills, cross-tool adapters
- Adaptive triage: ranks categories by user needs

## Target Users

- **Primary:** AI tool users (Cursor, Claude Code, Copilot, Windsurf) who want AI to understand them better
- **Secondary:** Developers and teams setting up AI-assisted workflows for the first time
- **Tertiary:** Potential Setness Consulting leads — the interview naturally surfaces role, tech stack, AI maturity, and pain points

## User Stories

### Free Tier
1. As a Cursor user, I want an AI to interview me and generate an about_me.md file so my AI assistant understands who I am and what I do.
2. As a Claude Code user, I want to define my AI preferences (tone, code style, constraints) so the AI's output matches how I like to work.
3. As a new AI tool user, I want a guided experience that tells me what's possible, not a blank page.

### Paid Tier (Future)
1. As a power user with multiple AI agents, I want to create soul files for each agent so they maintain consistent identity and behavior.
2. As a developer, I want session continuity files so my AI picks up where it left off every session.
3. As a team lead, I want agent profile and routing files so I can orchestrate multiple agents across domains.

## Functional Requirements (Free Tier)

| ID | Requirement |
|----|------------|
| FR1 | Agent conducts a structured 4-phase interview for about_me.md |
| FR2 | Agent conducts a structured 5-section interview for ai_preferences.md |
| FR3 | Agent adapts questions based on user responses (vague → probe, specific → validate) |
| FR4 | Agent generates markdown from defined templates, not raw LLM output |
| FR5 | Agent shows generated file to user for review and editing before finalizing |
| FR6 | User can request either file independently or both in sequence |
| FR7 | No email gate — user downloads or copies output directly |
| FR8 | Agent can show the paid tier catalog on request |
| FR9 | Agent respects hard limits (no secrets, no email ask, no scope creep) |

## Non-Functional Requirements

| ID | Requirement |
|----|------------|
| NFR1 | Free tier interview completes in ≤5 minutes |
| NFR2 | Generated files are consistently formatted (template-driven) |
| NFR3 | Agent tone is warm, professional, and encouraging |
| NFR4 | Adaptive follow-ups feel conversational, not form-like |
| NFR5 | All documentation (SOUL.md, AGENTS.md, HANDOFF.md, STATUS.md, etc.) kept current |

## Out of Scope (v0.1)

- Paid tier implementation (cataloged, deferred)
- File system writes (agent shows output; user saves manually)
- Email delivery
- CRM integration
- Multi-user/team support
- Codebase scanning/analysis
- Real-time sync

## Success Metrics

| Metric | Target |
|--------|--------|
| Interview completion rate | >80% of starts complete both files |
| User satisfaction (qualitative) | Users report feeling understood, not interrogated |
| Template fidelity | 100% of generated files match template structure |
| Paid catalog interest | >20% of users ask to see the catalog after free tier |
