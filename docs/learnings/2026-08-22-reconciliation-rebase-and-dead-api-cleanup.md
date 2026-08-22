---
project: project-context-file-maker
type: learning
status: raw
tags: [git, rebase, reconciliation, testing, api-drift]
source: opencode-session
created: 2026-08-22
last_updated: 2026-08-22
promoted_to_obsidian: false
---

## Context

We executed the long-deferred owner decision to reconcile two divergent lines in project-context-file-maker: the local v0.2.x line (template engine, CLI, validator, 121 tests) and `origin/master` (v0.1.3 remote line with CI, synthetic fixtures, DATA-CONTRACT). Per STATUS.md the decision was Option A: rebase local v0.2.x onto origin/master, keeping the remote base and re-applying v0.2 features on top. The rebase was done on a dedicated branch `reconcile-v021`.

## Learning

- When a rebase replays a local feature line onto a remote base, the two lines often have **divergent test files and fixtures**. The rebase base silently reintroduced `tests/test_generate_validation.py` and the `TestInputContractValidation` class from the remote line — both testing a dead API (`AnswerValidationError`, `validate_input_contract`) that the v0.2.x code had already replaced (`validate_answers` returning `(valid, msgs)`, `validate_schema_question_mapping`). Post-rebase, pytest collection failed on those orphaned tests.
- Fix pattern: after a line reconciliation rebase, verify which side won per file (`git diff <old> <new> --stat` against both parents), then delete/port tests that reference APIs no longer present, and make assertions fixture-agnostic (assert on `fixture['full_name']`, not a hardcoded owner name) so tests survive fixture swaps.
- A rebase can be continued by a concurrent process (reflog showed `rebase (continue)` + `rebase (finish)` happening mid-session). Working-tree edits can be reverted underneath you. Always re-verify `git status`, the committed blobs (`git rev-parse HEAD:<file>`), and the final test suite before committing, instead of assuming your staged resolutions won.
- `validate.py --strict` example drift guard is the fast signal for stale example outputs after an engine change: regenerate `output-examples/` with `python scripts/generate.py <name> --answers tests/fixtures/<name>_answers.json --output output-examples/<name>_example.md --force`.

## Reuse

Read this before doing another line reconciliation (or any cross-line rebase) in this project, and before touching `tests/` after an engine/CLI change — it explains why the suite may contain dead-API tests and how to make it green again.