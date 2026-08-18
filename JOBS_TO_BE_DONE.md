# Context File Maker — Jobs To Be Done

Use this as the agent's operating scorecard. Identity: `SOUL.md`.

## Primary Jobs

| Job | Success Signal |
|-----|---------------|
| Interview users for about_me.md | User completes all 4 phases in ≤3 minutes; feels understood, not interrogated |
| Interview users for ai_preferences.md | User covers all 5 sections in ≤2 minutes; generated file captures their actual preferences |
| Generate polished markdown output | Files are consistently formatted from templates; no raw LLM output |
| Maintain free tier purity | No email gate, no paid upsell during interview, no scope creep |
| Show paid catalog on request | User can browse all 14 categories with file descriptions |
| Keep docs current | HANDOFF.md and STATUS.md updated after meaningful changes |

## Confirmation Tokens

No external system mutations in v0.1. Generated files are shown in-chat; user saves them manually.

## Standard Commands

Natural language in this workspace:

- `build my context files` — Full free tier interview
- `create an about me file` — about_me.md only
- `create ai preferences` — ai_preferences.md only
- `show paid catalog` — Browse paid catalog

## Current Priorities

See `STATUS.md` for the live list. Do not treat this file as a second backlog.

1. Validate the free-tier conversational interview end-to-end
2. Keep questionnaires, schemas, and templates in sync (`scripts/validate.py --strict`)
3. Do not start paid-tier generation before the free interview path is proven
