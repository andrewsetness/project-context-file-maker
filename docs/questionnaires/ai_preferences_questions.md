# ai_preferences.md — Question Bank

Full question bank for the ai_preferences.md interview. The agent uses these as the base script, applying adaptive follow-ups based on user responses.

---

## Section 1: Communication Style

| # | Field | Primary Question | Options / Guidance |
|---|-------|-----------------|-------------------|
| 1 | tone | How should AI talk to you? | Professional, casual, direct, encouraging, Socratic (asks questions back), or something else? |
| 2 | verbosity | How detailed should AI responses be? | Concise (just the answer), balanced (answer + brief reasoning), thorough (full explanation), exhaustive (every detail)? |
| 3 | explain_reasoning | When AI gives code, should it explain the reasoning? | Always, only when asked, never, or only for complex things? |
| 4 | clarification_policy | Should AI ask clarifying questions or make reasonable assumptions? | Ask when uncertain, make reasonable assumptions, or always confirm? |

## Section 2: Code & Technical Preferences

| # | Field | Primary Question | Options / Guidance |
|---|-------|-----------------|-------------------|
| 5 | comments_policy | Should AI add comments to code? | Always, sparingly (complex logic only), never, or only docstrings/JSDoc? |
| 6 | error_handling | Preferred error handling style? | Try/catch, result types (Ok/Err), assertions, let it crash, or depends on language? |
| 7 | test_policy | Should AI write tests? | Always with code, when requested, never, or for critical paths only? |
| 8 | formatting_preferences | Any formatting preferences? | Tabs vs spaces, line length, single vs double quotes, semicolons vs none? |
| 9 | naming_conventions | Preferred naming conventions? | camelCase, snake_case, PascalCase, kebab-case, or language-idiomatic? |
| 10 | design_patterns | Preferred design patterns? | Functional, OOP, composition over inheritance, depends on context? |
| 11 | stack_preferences | Preferred languages or frameworks? Any to avoid? | "What's your go-to stack? Any tools you specifically want AI to avoid?" |

## Section 3: Workflow Preferences

| # | Field | Primary Question | Options / Guidance |
|---|-------|-----------------|-------------------|
| 12 | approach | Should AI plan first or just start coding? | Plan/discuss first, jump straight to code, or depends on complexity? |
| 13 | iteration_style | How should AI handle iterations? | Small incremental changes, big-bang rewrites, or depends? |
| 14 | file_editing | Should AI edit files directly or show code first? | Edit directly, show code first for approval, or ask first for every change? |
| 15 | git_policy | How should AI handle git? | Auto-commit with messages, suggest commits without executing, or never touch git? |
| 16 | documentation_policy | Should AI update docs with code changes? | Always, when relevant, or never? |
| 17 | scope_policy | Only do what's asked, or anticipate related needs? | Only what's explicitly asked, suggest related improvements, or ask before expanding scope? |

## Section 4: Constraints & Boundaries

| # | Field | Primary Question | Options / Guidance |
|---|-------|-----------------|-------------------|
| 18 | secrets_policy | How should AI handle secrets/keys? | Never generate, always use env vars, warn if detected in code? |
| 19 | external_services_policy | Can AI suggest external APIs or services? | Yes freely, only free/open-source options, or no — keep it internal? |
| 20 | no_touch_files | Any file types or directories AI should never touch? | "Config files, generated code, certain directories, legacy modules?" |
| 21 | breaking_changes_tolerance | Tolerance for breaking changes? | Avoid at all costs, OK with clear explanation, fine — just get it done? |
| 22 | dependencies_policy | Can AI add new dependencies? | Yes with justification, only well-known libraries, no — ask first? |
| 23 | cost_sensitivity | Cost-conscious about API calls? | Very (minimize tokens), somewhat, or not at all — quality over cost? |

## Section 5: Pet Peeves & Dealbreakers

| # | Field | Primary Question | Adaptive Follow-ups |
|---|-------|-----------------|---------------------|
| 24 | pet_peeves | What do AI assistants do that drives you crazy? | Examples: unsolicited documentation, over-explaining, not reading existing code, making assumptions? |
| 25 | past_frustrations | Any bad experiences with AI tools you want to avoid? | "What happened? What would have prevented it?" |
| 26 | must_haves | What's non-negotiable for a good AI interaction? | "What does an AI assistant absolutely need to get right for you?" |
| 27 | never_do | What should AI absolutely never do? | "What's the one thing that would make you stop using an AI tool?" |

## Interview Cadence

- **Pacing:** 4–5 questions per section. Don't list all options at once — offer 2–3 and let the user respond naturally.
- **Options presentation:** For questions with fixed choices, pick the top 2–3 most relevant options and offer them. Don't read all 5+ options.
- **Validation:** After each section: "So for communication: [tone] tone, [verbosity] verbosity, explain reasoning [when]. That feel right?"
- **Guidance:** If user is stuck: "Don't overthink this. Most people start with a few preferences and refine over time. You can always update this file later."
