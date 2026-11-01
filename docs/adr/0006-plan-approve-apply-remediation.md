# 0006 · Remediation is plan → approve → apply → verify (as-code preferred)

- **Status:** Proposed
- **Date:** 2026-10-31
- **Deciders:** Architecture, SRE lead, Security

## Context
"Create it for me" is a major value driver but also the riskiest feature: it writes to production tooling. Many teams manage dashboards and alerts as code, so out-of-band changes cause drift.

## Decision
Every remediation follows **plan → approve → apply → verify**:
1. Build a **plan** (exact objects, target, diff, risk, idempotency key).
2. Require **approval** per org policy (requester, SRE, or both; separation of duties).
3. **Apply** idempotently; record results; roll back where possible.
4. **Verify** by re-running the originating check.

Where the team uses IaC/Git, **the default delivery is a pull request** to their repository (Terraform / Jsonnet / provisioning YAML); direct API changes are an option per policy. Defaults are **create-only**, **non-prod first**, and **feature-flagged per remediation type**.

## Consequences
- **Good:** safe, auditable, drift-aware; fits GitOps culture.
- **Bad:** PR-based delivery is slower than a direct API call; requires repo write access for the connector.
- **Follow-ups:** blast-radius limits; per-template dry-run.

## Alternatives considered
| Option | Why not |
|---|---|
| Direct API changes without approval | Unacceptable risk |
| Suggestions only (no apply) | Loses the key productivity benefit |
