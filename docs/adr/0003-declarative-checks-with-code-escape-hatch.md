# 0003 · Declarative checks with a code escape hatch

- **Status:** Proposed
- **Date:** 2026-10-31
- **Deciders:** Architecture, SRE lead

## Context
SREs, not only developers, own the meaning of "ready". Most checks are simple (a field is populated, an alert exists). A few need multi-call logic. Checks must be reviewable, versionable, testable and explainable.

## Decision
Checks are defined in **YAML with a small expression language** (id, severity, inputs, capability, rule, messages, why, fix hint, remediation, evidence). Where YAML is insufficient, a check may be written as a **Python function** against the same SDK interface. Both produce the same result object and are tested with recorded fixtures.

## Consequences
- **Good:** SREs can contribute without writing code; uniform output; easy diffing and review; packs can be signed and versioned.
- **Bad:** we must design and maintain a safe expression evaluator (no arbitrary code execution, bounded runtime).
- **Follow-ups:** conformance tests for the evaluator; lint rules for every check (must have why, fix hint, fixture).

## Alternatives considered
| Option | Why not |
|---|---|
| Code-only checks | Excludes SRE contributors; harder to review semantics |
| Generic policy engine (OPA/Rego) for everything | Powerful but steep for authors; evidence and explanation model still needed; may adopt later for policy gates |
| LLM-evaluated checks | Non-deterministic, not auditable (see ADR-0004) |
