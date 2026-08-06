# Context File Maker

An interactive agent that interviews users and generates structured AI context files — starting with the free tier: `about_me.md` and `ai_preferences.md`.

**Status:** v0.1 — Free tier implemented. Paid tier catalog ready for future batches.
**Repo:** `andrewsetness/project-context-file-maker`
**Plan:** `../03-business/project-setness-consulting/business/PLAN_PA2.3_CONTEXT_FILE_BUILDER_PRO.md`

## Quick Start

1. Open this workspace in Cursor
2. Say: `build my context files` or `create an about me file`
3. The agent interviews you and generates the files
4. Files appear in `output-examples/` — copy `about_me.md` and `ai_preferences.md` to any project

## What This Agent Does

The Context File Maker agent conducts a structured interview across multiple phases, then generates polished markdown context files that AI assistants (Cursor, Claude Code, Copilot, Windsurf, etc.) use to understand you and your preferences.

### Free Tier (Implemented)

| File | Purpose | Interview Time |
|------|---------|---------------|
| `about_me.md` | Identity, role, tech stack, goals, pain points | ~3 min |
| `ai_preferences.md` | Tone, verbosity, code style, constraints, pet peeves | ~2 min |

### Paid Tier (Cataloged — Future Batches)

60+ context files across 14 categories. See `templates/paid/CATALOG.md` for the full catalog. See `../03-business/project-setness-consulting/business/PLAN_PA2.3_CONTEXT_FILE_BUILDER_PRO.md` for the full business plan.

## Required Reading

1. `SOUL.md` — Identity and operating contract
2. `AGENTS.md` — Agent guidance
3. `HANDOFF.md` — State and workspace handoff
4. `STATUS.md` — Current state and open items
5. `JOBS_TO_BE_DONE.md` — Operating scorecard
6. `ARCHITECTURE.md` — System design and data flow
7. `PRD.md` — Full behavioral specification
8. `.cursor/skills/context-file-maker/SKILL.md` — Execution sequence
9. `agents/context-file-maker-agent.md` — Agent system prompt

## Project Structure

```
project-context-file-maker/
├── README.md                              # This file
├── SOUL.md                                # Identity and operating contract
├── AGENTS.md                              # Agent guidance
├── HANDOFF.md                             # Session handoff
├── STATUS.md                              # Current state
├── JOBS_TO_BE_DONE.md                     # Operating scorecard
├── ARCHITECTURE.md                        # System design
├── SKILL.md                               # Agent skill definition
├── PRD.md                                 # Full behavioral spec
├── .cursor/
│   ├── rules/context-file-maker-core.mdc   # Cursor rule (auto-loads SOUL.md)
│   └── skills/context-file-maker/SKILL.md  # Execution protocol
├── Context/
│   └── MEMORY.md                           # Durable agent memory
├── agents/
│   └── context-file-maker-agent.md         # LLM system prompt
├── templates/
│   ├── free/                               # Free tier templates
│   │   ├── about_me.md
│   │   └── ai_preferences.md
│   └── paid/
│       └── CATALOG.md                      # Full paid tier catalog
├── docs/
│   ├── README.md                           # Docs index
│   └── questionnaires/                     # Full question banks
│       ├── about_me_questions.md
│       └── ai_preferences_questions.md
└── output-examples/                        # Example generated outputs
    ├── about_me_example.md
    └── ai_preferences_example.md
```
