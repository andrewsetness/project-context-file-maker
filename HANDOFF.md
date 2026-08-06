# Context File Maker — Handoff

**Workspace:** `project-context-file-maker` (parent folder: `Cursor Projects`)
**Repo:** `andrewsetness/project-context-file-maker`
**Business plan:** `../03-business/project-setness-consulting/business/PLAN_PA2.3_CONTEXT_FILE_BUILDER_PRO.md`

## Resume Prompt

```
I'm continuing work on project-context-file-maker — the interactive interview agent
that builds AI context files for users.

This project implements PA2.3 from the Setness Consulting business plan.
Current phase: v0.1 — free tier (about_me.md + ai_preferences.md).

Read SOUL.md, AGENTS.md, HANDOFF.md, STATUS.md, JOBS_TO_BE_DONE.md,
ARCHITECTURE.md, and PRD.md.

The agent system prompt lives in agents/context-file-maker-agent.md.
Output templates are in templates/free/.
Full question banks are in docs/questionnaires/.

The paid tier catalog exists in templates/paid/CATALOG.md but implementation
is deferred to future batches.
```

## How to Start a Chat

Open this project in Cursor and say one of:

- `build my context files` — Full free tier interview
- `create an about me file` — about_me.md only
- `create ai preferences` — ai_preferences.md only
- `show paid catalog` — Browse paid tier catalog

The `context-file-maker-core.mdc` rule loads automatically and points to `SOUL.md`.

## Current State

- **Phase:** v0.1 — Free tier implementation active
- **Scope:** 2 free files (about_me.md, ai_preferences.md)
- **Paid:** 60+ files cataloged in `templates/paid/CATALOG.md` — deferred to future batches
- **Business plan:** Scoped and detailed in `PLAN_PA2.3_CONTEXT_FILE_BUILDER_PRO.md`

## File Map

```
project-context-file-maker/
├── SOUL.md                                    # Identity and operating contract
├── HANDOFF.md                                 # This file
├── STATUS.md                                  # Current state and open items
├── JOBS_TO_BE_DONE.md                          # Operating scorecard
├── AGENTS.md                                  # Agent guidance
├── ARCHITECTURE.md                            # System design and data flow
├── SKILL.md                                   # Agent skill definition
├── PRD.md                                     # Full behavioral specification
├── .cursor/
│   ├── rules/context-file-maker-core.mdc       # Cursor rule (auto-loads SOUL.md)
│   └── skills/context-file-maker/SKILL.md      # Execution protocol
├── Context/
│   └── MEMORY.md                               # Durable agent memory
├── agents/
│   └── context-file-maker-agent.md             # LLM system prompt
├── templates/
│   ├── free/
│   │   ├── about_me.md                          # about_me.md output template
│   │   └── ai_preferences.md                    # ai_preferences.md output template
│   └── paid/
│       └── CATALOG.md                           # Full paid tier catalog
├── docs/
│   ├── README.md                                # Docs index
│   └── questionnaires/
│       ├── about_me_questions.md                # about_me.md question bank
│       └── ai_preferences_questions.md          # ai_preferences.md question bank
└── output-examples/                             # Example generated outputs
    ├── about_me_example.md
    └── ai_preferences_example.md
```
