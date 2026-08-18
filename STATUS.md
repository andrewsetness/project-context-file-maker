# STATUS — Context File Maker

- **Purpose:** Interview-and-generation toolkit for AI context files.
- **Overall Status:** v0.1.3 — deterministic free-tier generation implemented; conversational Cursor interview still needs an end-to-end product test.
- **Last Updated:** 2026-08-18
- **Blocker:** None for CLI generation; do not expand paid-tier scope before the free interview path is validated.

## Current runtime

Implemented:

- Free-tier templates: `about_me.md` + `ai_preferences.md`
- Question banks for both free-tier files
- JSON answer schemas under `schemas/`
- Template engine (`scripts/template_engine.py`)
- CLI generator (`scripts/generate.py`)
- **Runtime schema enforcement before rendering/writing**
- Template/question/schema/fixture validator (`scripts/validate.py`)
- GitHub Actions quality gate (pytest + `validate.py --strict`)
- Unit/integration/regression tests, including invalid-payload rejection
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

## Recent remediation — 2026-08-18

- Added `docs/DATA-CONTRACT.md` defining question → answer JSON → schema validation → template → explicit output flow.
- Added schema validation to `scripts/generate.py`; invalid required fields/types now fail before output is written.
- Added generator validation regression tests.
- Replaced personal-looking tracked full fixtures/examples with explicitly fictional data.
- Corrected README language that previously described `output-examples/` as the destination for generated user files.
- Removed the stale open item to create examples; the examples already existed.
- Made the public repo self-contained: dropped unpublished sibling-plan paths, named canonical spec files, documented license/release as an owner decision, and extended `validate.py` to enforce the answer-schema contract in CI.

## Open Items

- [ ] Test the free-tier conversational interview end-to-end in Cursor, including explicit output destination and cancellation/resume behavior.
- [ ] Measure the actual interview time before presenting the ~3 min / ~2 min figures as validated user-facing claims.
- [ ] Decide whether interview answer JSON should have a supported local resume format; if so, define its ignored/private storage lifecycle first.
- [ ] Reconcile `profile.yaml` / cross-agent discovery only if this agent is intentionally promoted into the shared portfolio runtime.
- [ ] Decide which paid category to implement **after** the free-tier interview path is proven.
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
