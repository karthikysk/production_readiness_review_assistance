# Architecture Decision Records (ADRs)

An ADR captures **one significant decision**: the context, the choice, and its consequences, so future contributors understand *why* things are the way they are and can revisit them deliberately.

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-modular-monolith-first.md) | Modular monolith first | Proposed |
| [0003](0003-declarative-checks-with-code-escape-hatch.md) | Declarative checks with a code escape hatch | Proposed |
| [0004](0004-ai-assists-checks-decide.md) | AI assists, deterministic checks decide | Proposed |
| [0005](0005-capability-based-sandboxed-connectors.md) | Capability-based, sandboxed connectors | Proposed |
| [0006](0006-plan-approve-apply-remediation.md) | Remediation is plan, approve, apply, verify (as-code preferred) | Proposed |
| [0007](0007-durable-workflow-engine.md) | Durable workflow engine for long-running work | Proposed |
| [0008](0008-postgres-as-single-system-of-record.md) | PostgreSQL (with pgvector) as the single system of record | Proposed |

**Status values:** Proposed → Accepted → (Superseded by NNNN | Deprecated). Decisions are *Proposed* until the team accepts them in review.

## How to add one

1. Copy [`template.md`](template.md) to `NNNN-short-title.md` (next number).
2. Fill it in; keep it to one page.
3. Open a PR; discussion happens in the PR. Merge when accepted.
4. Never edit an accepted ADR's decision; write a new ADR that supersedes it.
