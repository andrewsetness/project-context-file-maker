# Learnings

Project learnings captured during development and operational use.

## Format

Each learning is a dated markdown file: `YYYY-MM-DD-topic.md`

## Template

```markdown
# [Topic]

- **Date:** YYYY-MM-DD
- **Context:** What was happening
- **Learning:** What was learned
- **Action:** What changed as a result
- **Tags:** tag1, tag2
```

## Learnings Log

| Date | Topic | Summary |
|------|-------|---------|
| 2026-08-22 | [Reconciliation rebase & dead-API cleanup](2026-08-22-reconciliation-rebase-and-dead-api-cleanup.md) | Rebase of v0.2.x onto origin/master reintroduced remote-line tests that tested a dead API; delete/port tests and make assertions fixture-agnostic after a line reconciliation. |