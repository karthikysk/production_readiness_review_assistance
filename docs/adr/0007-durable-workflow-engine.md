# 0007 · Durable workflow engine for long-running work

- **Status:** Proposed
- **Date:** 2026-10-31
- **Deciders:** Architecture, Platform

## Context
Check runs fan out to many slow, rate-limited external calls; remediation waits for human approval (minutes to days) and must resume after restarts; actions must be idempotent and resumable (NFR-05).

## Decision
Use a **durable workflow engine (Temporal, managed or self-hosted)** for check runs, remediation and report generation. Activities are idempotent; human approvals are signals; timeouts, retries and backoff use the engine's policies.

## Consequences
- **Good:** reliability, visibility of long-running state, simple retries, clear audit of progress.
- **Bad:** new infrastructure and a learning curve; determinism rules for workflow code.
- **Follow-ups:** a thin internal abstraction so the engine could be swapped; operational runbooks.

## Alternatives considered
| Option | Why not |
|---|---|
| Celery / queue only | Hand-rolled state for approvals and resumption |
| Custom state machine in Postgres | Reinvents durable timers, retries, versioning |
| Step Functions | Cloud lock-in (NFR-12 portability) |
