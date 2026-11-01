# 0001 · Record architecture decisions

- **Status:** Accepted
- **Date:** 2026-10-31
- **Deciders:** Architecture

## Context
PRRA has many hard-to-reverse choices (integration model, AI boundaries, workflow engine, data store). New contributors, and our future selves, need to know *why* each was made.

## Decision
We record significant decisions as lightweight ADRs in `docs/adr/`, reviewed through pull requests like code.

## Consequences
- **Good:** shared memory, faster onboarding, deliberate reversals.
- **Bad:** small ongoing writing overhead.
- **Follow-ups:** reference ADRs from the HLD/LLD where they apply.

## Alternatives considered
| Option | Why not |
|---|---|
| Wiki pages | Drift away from code, no review trail |
| Decisions only in chat/meetings | Lost quickly |
