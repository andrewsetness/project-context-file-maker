# about_me.md — Question Bank

Full question bank for the about_me.md interview. The agent uses these as the base script, applying adaptive follow-ups based on user responses.

---

## Phase 1: Identity & Role

| # | Field | Primary Question | Adaptive Follow-ups |
|---|-------|-----------------|---------------------|
| 1 | full_name | What name should AI assistants use for you? | — |
| 2 | preferred_name | Any nickname or short form you prefer? | — |
| 3 | job_title | What's your current job title? | "What does your day-to-day actually look like in that role?" |
| 4 | company | What company or organization do you work for? | — |
| 5 | company_size | Roughly how many people work there? | "Solo, small team, mid-size, or large enterprise?" (offer ranges if needed) |
| 6 | industry | What industry are you in? | "What drew you to that industry?" (rapport-building, optional) |
| 7 | years_experience | How many years of professional experience do you have? | — |

## Phase 2: Work & Projects

| # | Field | Primary Question | Adaptive Follow-ups |
|---|-------|-----------------|---------------------|
| 8 | primary_work | In 2–3 sentences, what do you actually do day-to-day? | — |
| 9 | current_projects | What are you working on right now? (top 1–3) | "What's your role in that project?" or "Which of those is the most important right now?" |
| 10 | biggest_challenge | What's the hardest part of your work right now? | **Critical question.** If vague: "Is it the volume, the complexity, a specific technology, a team dynamic, or something else?" |
| 11 | goals_6mo | What do you want to accomplish in the next 6 months? | "Is there a specific milestone or outcome?" |
| 12 | goals_2yr | Where do you want to be in 2 years? | "Same role, bigger scope? Different role? Different industry?" |

## Phase 3: Technical & AI

| # | Field | Primary Question | Adaptive Follow-ups |
|---|-------|-----------------|---------------------|
| 13 | tech_stack | What programming languages, frameworks, or tools do you use most? | "What's your go-to stack?" or "Any tools you're excited about learning?" |
| 14 | ai_tools | Which AI tools do you currently use? (Cursor, Copilot, ChatGPT, Claude, etc.) | If none: "What made you interested in building context files today?" |
| 15 | ai_proficiency | How comfortable are you with AI tools? Beginner, intermediate, or advanced? | "What's your most-used AI workflow?" (if advanced) or "What would you like to use AI for more?" (if beginner) |
| 16 | ai_pain_points | What frustrates you most about current AI tools? | "Is it accuracy, understanding your context, speed, or something else?" |
| 17 | favorite_tools | Any tools you love and why? | — |
| 18 | tools_avoid | Any tools you've tried and disliked? | "What didn't work about it?" |

## Phase 4: Personal & Preferences

| # | Field | Primary Question | Adaptive Follow-ups |
|---|-------|-----------------|---------------------|
| 19 | location | What timezone or city are you in? | — |
| 20 | work_hours | When do you typically work? | "Early bird, night owl, or standard 9–5?" |
| 21 | communication_style | How do you like to communicate? Direct and concise, detailed and thorough, casual, formal? | "For example, I personally prefer direct — tell me what you think. What works for you?" |
| 22 | learning_style | How do you learn best? Reading docs, hands-on doing, watching videos, discussing with others? | — |
| 23 | hobbies | Any hobbies or interests outside of work? (optional) | — |
| 24 | fun_fact | One interesting thing about you? (optional) | "Anything people are surprised to learn about you?" |

## Interview Cadence

- **Pacing:** 3–4 questions per exchange. Don't firehose the user.
- **Validation:** After every 3–4 answers, summarize: "So far I have: you're a [role] at [company], working on [project], and your biggest challenge is [X]. Sound right?"
- **Transition:** Signal phase changes clearly: "Great. Now let's talk about your tools."
- **Completion:** After all 4 phases, show the full generated file.
