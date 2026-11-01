# 0002 · Modular monolith first

- **Status:** Proposed
- **Date:** 2026-10-31
- **Deciders:** Architecture, Tech leads

## Context
The HLD shows a dozen logical services (Review, Design Intelligence, Blueprint, Check Engine, Remediation, Evidence, Notification, Identity…). A small team must deliver an MVP quickly. Premature microservices bring distributed-systems cost (deployments, versioning, tracing, consistency) before we know where the real boundaries and scaling needs are.

## Decision
Ship v1 as **one deployable "modular monolith"** with strictly separated modules (own packages, own tables/schemas, in-process interfaces only). Keep **connectors** and **workers** as separate processes because their isolation and scaling needs are already clear (sandboxing, egress control, queue-driven load).

Module boundaries are enforced by tooling (import-linter / architecture tests) so any module can be extracted later without a rewrite.

## Consequences
- **Good:** faster delivery, simple local development and debugging, transactional consistency inside the core, lower operational load.
- **Bad:** one deployment unit to scale; discipline needed to avoid coupling; a bad module release affects the whole core.
- **Follow-ups:** add architecture fitness tests in CI; revisit extraction when a module has independent scaling or team-ownership needs (candidates: Design Intelligence, Check Engine).

## Alternatives considered
| Option | Why not (now) |
|---|---|
| Microservices from day one | Operational overhead exceeds benefit at this stage |
| Single unstructured monolith | Boundary erosion; harder to split later |
| Serverless functions per capability | Awkward for long-running workflows and stateful orchestration |
