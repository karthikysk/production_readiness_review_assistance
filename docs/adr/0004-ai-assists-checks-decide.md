# 0004 · AI assists, deterministic checks decide

- **Status:** Proposed
- **Date:** 2026-10-31
- **Deciders:** Architecture, Security, Product

## Context
Design documents are messy; extracting components from prose and diagrams is where AI helps most. But a readiness gate that depends on non-deterministic output cannot be trusted, audited or defended. Designs are also an untrusted input (prompt injection).

## Decision
- AI is used to **propose** (a) the component graph from design documents and (b) plain-language **explanations** of already-computed results.
- AI output is always a **proposal with citations and confidence**, validated against a strict schema and **confirmed by a human** before use.
- **Pass/fail is computed only by deterministic checks** against real systems. The recommendation is computed by fixed rules; the verdict is a human decision.
- AI components have **no credentials** and **no write tools**.
- A fully non-AI path (structured service manifest) is always available.

## Consequences
- **Good:** trust, auditability, reproducibility, reduced prompt-injection blast radius, works in orgs that forbid LLMs.
- **Bad:** a human confirmation step adds friction; less "magic" than an autonomous agent.
- **Follow-ups:** extraction evaluation harness with real, labelled designs; prompt-injection test suite.

## Alternatives considered
| Option | Why not |
|---|---|
| Autonomous AI agent decides readiness | Not auditable; risk of silent errors |
| No AI at all | Leaves design-to-blueprint manual, the biggest time sink |
