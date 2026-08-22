# STATUS — Context File Maker

- **Purpose:** Interview-and-generation toolkit for AI context files.
- **Overall Status:** v0.2.1 — deterministic free-tier generation with polished template output, hardened CLI, schema/question-bank validation, 129-test suite, and CI. Conversational Cursor interview still needs an end-to-end product test. Reconciliation of local v0.2.x with origin/master completed on `reconcile-v021` (pushed).
- **Last Updated:** 2026-08-22
- **Blocker:** None for CLI generation; do not expand paid-tier scope before the free interview path is validated. Owner decision pending: fold `reconcile-v021` into `master`.

## Current runtime

- Free-tier templates: `about_me.md` + `ai_preferences.md`
- Question banks for both free-tier files
- JSON answer schemas under `schemas/`
- Template engine (`scripts/template_engine.py`) — Mustache-style filling: `{{field}}`, `{{~field}}` for `[not provided]`, `{{#field}}` conditionals, `{{#any:f1,f2}}` section gates; line-isolated and inline blocks; list values rendered as text
- CLI generator (`scripts/generate.py`) — JSON answers → markdown with `--validate`, `--json`, `--force`, `--verbose`; diagnostics to stderr so stdout stays clean markdown
- **Runtime schema enforcement before rendering/writing** — invalid payloads fail closed
- Template/question/schema/fixture validator (`scripts/validate.py`) — placeholder-field mapping, schema↔question-bank cross-check, example drift guard; reuses the engine's tokenizer
- Interviewer checklist (`scripts/checklist.py`) — question-bank checklists, missing-field flags
- Shared CLI config (`scripts/common.py`) + `requirements-dev.txt`
- GitHub Actions quality gate (pytest + `validate.py --strict`)
- Unit/integration/regression tests (129), including invalid-payload rejection
- Synthetic full/minimal test fixtures
- Synthetic example outputs under `output-examples/`
- Data/privacy/output contract: `docs/DATA-CONTRACT.md`

Not yet proven:

- full conversational interview UX in Cursor from first prompt through user-selected output;
- measured interview duration/usability;
- paid-tier context-file generation.

## Data boundary

`output-examples/` and `tests/fixtures/` are synthetic tracked data only. Real user answers and generated profiles must be written to an explicitly selected private/user-owned destination and must not be committed to this repository.

The generator validates structured JSON and renders deterministic templates. It does not infer missing required facts from conversation history.

Current tracked files are synthetic. Git history predating the 2026-08-18 fixture cleanup has not been rewritten; deciding whether that historical personal-looking fixture material warrants a destructive history purge is an explicit owner/privacy decision.

## Recent milestones

- 2026-08-06: Project scaffolded. All Phase 1a root documents created. Free tier agent prompt, templates, question banks, paid catalog implemented.
- 2026-08-06 v0.1.1: Critical review completed. Template engine, validator, CLI, JSON schemas, and 78-test suite built.
- 2026-08-08 v0.2: Product polish pass. `{{~field}}` / `{{#any:...}}` template syntax, line-aware conditional removal, CLI flags (`--validate`/`--json`/`--force`/`--verbose`), checklist tool, drift-guarded example outputs, 106 tests.
- 2026-08-18 v0.1.3 (remote line): Self-contained clone, DATA-CONTRACT.md, schema-enforced generation, synthetic fixtures replacing personal data, CI quality gate.
- 2026-08-22 v0.2.1: Maintenance pass — stderr diagnostics routing, inline any-block support, deterministic field ordering, fail-closed schema validation, jsonschema-independent typo detection, schema↔question-bank cross-check, shared config dedupe, docs path fixes, 121 tests.
- 2026-08-22 reconciliation: The two divergent lines (local v0.2.x and remote v0.1.3) were reconciled per owner decision (Option A: rebase local onto origin/master). Remote's CI/synthetic fixtures/DATA-CONTRACT kept as base; v0.2 feature set re-applied on top. Completed on `reconcile-v021` (tip `f7ef557`, pushed to GitHub); schema enforcement now unconditional per DATA-CONTRACT, 129 tests passing, `validate.py --strict` clean.

## Open Items

- [ ] **Owner decision:** fold `reconcile-v021` into `master` (fast-forward master to `f7ef557`, delete branch) or keep `reconcile-v021` as the working line. `master` is still the pre-rebase v0.2 line.
- [ ] Test the free-tier conversational interview end-to-end in Cursor, including explicit output destination and cancellation/resume behavior.
- [ ] Measure the actual interview time before presenting the ~3 min / ~2 min figures as validated user-facing claims.
- [ ] Decide whether interview answer JSON should have a supported local resume format; if so, define its ignored/private storage lifecycle first.
- [ ] Reconcile `profile.yaml` / cross-agent discovery only if this agent is intentionally promoted into the shared portfolio runtime.
- [ ] Decide which paid category to implement **after** the free-tier interview path is proven (B — Agent Soul & Identity recommended).
- [ ] Optionally: add a `--tone`/theme variant for generated files (personal vs business).
- [ ] **Owner/privacy decision:** decide whether to rewrite Git history to purge the pre-2026-08-18 personal-looking fixture history. Do not rewrite history implicitly; current tracked fixtures/examples are already synthetic.
- [ ] **Owner decision:** choose a license and, if desired, a GitHub Release process. Do not invent either.

## Definition of done for the free tier

The free tier is product-validated when:

1. a fresh user can start the Cursor interview from README instructions;
2. required/optional answers are collected without schema mismatch;
3. cancellation/resume behavior is explicit;
4. output destination is explicit and private by default;
5. both generated files pass schema/template validation;
6. no real user data is written into tracked examples/fixtures;
7. the actual interview duration is measured and documented.

## Verification

```powershell
python -m pytest -q
python scripts/validate.py --strict
```

Passing these checks verifies deterministic generation and repository consistency; it does **not** prove the conversational UX has been tested.
