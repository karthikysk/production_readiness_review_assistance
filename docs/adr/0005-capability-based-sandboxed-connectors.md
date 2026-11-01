# 0005 · Capability-based, sandboxed connectors

- **Status:** Proposed
- **Date:** 2026-10-31
- **Deciders:** Architecture, Security, Integration lead

## Context
Organisations use different tools, and tools change. We need extensibility without forking the core. Connectors hold or use powerful credentials and run third-party-influenced code.

## Decision
The core depends on **capability interfaces** (`change_management`, `logs`, `metrics`, `dashboards`, `alerting`, `oncall`, `cicd`, `source`, `cloud`, `catalog`, `docs`, `traces`), never on products. Each connector declares a **manifest** (capabilities, scopes, config schema, rate limits, egress allow-list), runs **sandboxed** (separate process/pod, NetworkPolicy egress allow-list), and receives **short-lived credentials** from a broker per call. Read and write operations are separate and policy-gated.

## Consequences
- **Good:** swap tools by configuration; least privilege; consistent error semantics; testable via record/replay.
- **Bad:** designing stable capability interfaces is hard; lowest-common-denominator risk (mitigated with optional extension fields).
- **Follow-ups:** versioned capability schemas with deprecation policy; contract-test suite per capability.

## Alternatives considered
| Option | Why not |
|---|---|
| Hard-coded integrations | Fast at first, painful to extend; coupling everywhere |
| Generic HTTP "webhook" connector only | Pushes complexity to every author; weak safety/typing |
| Run connectors in-process | No isolation for credentials or egress |
