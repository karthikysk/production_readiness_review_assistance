# 09 · Experience: Journeys and Screens

PRRA has to make sense to a developer, an SRE, a change manager and a director. This page shows **who does what** and **what they see**.

---

## 1. User journeys

### Dana (Developer), "What do I still need to do?"

```mermaid
journey
    title Dana prepares a release
    section Start
      Paste CRQ number and design link: 4: Dana
      See traffic-light summary in seconds: 5: Dana
    section Understand
      Confirm the components PRRA found: 4: Dana
      Read what each component needs and why: 5: Dana
    section Fix
      Click Create it for me on a missing alert: 5: Dana
      Review the plan and approve: 4: Dana
      Watch the check turn green: 5: Dana
    section Finish
      Send to SRE for review: 5: Dana
```

### Sam (SRE Reviewer), "Can I trust this release?"

```mermaid
journey
    title Sam reviews a release
    section Review
      Open one scorecard instead of six tools: 5: Sam
      Look at the observability overlay: 5: Sam
      Drill into a failing check and its evidence: 5: Sam
    section Decide
      Grant a time-boxed waiver with follow-up: 4: Sam
      Co-approve a remediation plan: 4: Sam
      Record verdict, result written back to CRQ: 5: Sam
```

### Morgan (Engineering manager), "Where are we weak?"

```mermaid
journey
    title Morgan looks at the portfolio
    section Insight
      Open readiness by team and tier: 5: Morgan
      See the top recurring gaps: 5: Morgan
      Decide where to invest: 4: Morgan
```

---

## 2. Screen map

```mermaid
flowchart TB
    HOME["Home<br/>my reviews, upcoming releases"] --> NEW["New review<br/>CRQ, service, release type"]
    NEW --> DES["Design<br/>upload or link, or fill the manifest"]
    DES --> CONF["Confirm components<br/>edit graph with citations"]
    CONF --> REV["Review page<br/>scorecard + diagrams"]
    REV --> BP["Blueprint overlay<br/>click a component"]
    REV --> CHK["Check detail<br/>evidence, why, fix hint"]
    CHK --> PLAN["Remediation plan<br/>diff, risk, approve"]
    REV --> WAIV["Waiver dialog"]
    REV --> REP["Readiness report<br/>HTML / PDF"]
    HOME --> PORT["Portfolio dashboard"]
    HOME --> ADM["Admin<br/>connectors, packs, policies"]
```

## 3. The review page (wireframe)

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│ orders-api · Release 2026.11.2 · CRQ CHG0123456 · Tier T1        [Re-run checks]│
├───────────────────────────────────────────────────────────────────────────────┤
│  RECOMMENDATION:  🟠 READY WITH CONDITIONS        Score 82 / 100                │
│  "2 major gaps to fix before go-live. No blockers."   (Decision by: Sam, SRE)  │
│                                                                               │
│  CRQ 🟢 11/12     Observability 🟠 19/24     Pipeline 🟢 8/8     Ops 🟠 6/8     │
│  Resilience 🟢 6/6      Security 🟢 6/6      Dependencies 🟠 3/4               │
├───────────────────────────────────────────────────────────────────────────────┤
│  DESIGN                                                                        │
│  [Customers]──▶[ALB]──▶[Orders API]──▶[Postgres]                               │
│                              └──▶[Kafka topic]──▶[Fulfilment consumer]         │
│                                                                               │
│  OBSERVABILITY OVERLAY (click a component)                                     │
│  [ALB ✅]──▶[Orders API ⚠️]──▶[Postgres ❌]                                     │
│                   └──▶[Kafka ⚠️]──▶[Consumer ❌]      Cross-cutting ⏳           │
├───────────────────────────────────────────────────────────────────────────────┤
│  NEXT ACTIONS                                                                  │
│  ❌ Replication lag alert missing (Postgres)        [Create it for me] [Explain]│
│  ❌ Consumer lag alert missing (Consumer)           [Create it for me] [Explain]│
│  ⚠️ Golden-path probe missing (API)                 [Create it for me] [Explain]│
│  ⚠️ CRQ lacks post-implementation monitoring task   [Create task]      [Explain]│
└───────────────────────────────────────────────────────────────────────────────┘
```

## 4. Design principles for the UI

| Principle | In practice |
|---|---|
| **Answer first** | Recommendation and next actions above the fold; detail on demand |
| **Never just a colour** | Icons + text for status (accessibility, WCAG 2.1 AA) |
| **Explain, don't scold** | Every finding: what, why it matters, how to fix, who can |
| **Evidence one click away** | Raw query/response excerpt with timestamp |
| **Unknown looks different from fail** | ⏳ / grey "could not check" with the reason (e.g. "Splunk token expired") |
| **Safe by default** | Remediation always previews a plan; destructive actions need explicit confirmation |
| **Plain language toggle** | "Explain like I'm new" summary for non-engineers |

## 5. "Create it for me": the plan screen

```text
┌─ Remediation plan · REM-AL-012 · Replication lag alert ───────────────────────┐
│ Target: Grafana (prod-observability)  ·  Delivery: Direct API   ·  Risk: LOW  │
│                                                                               │
│ + CREATE alert rule   "orders-db replication lag > 30s"                       │
│     expr: aws_rds_replica_lag_seconds{db="orders-db"} > 30 for 5m             │
│     route: PagerDuty service "orders-api (T1)"   runbook: <link>              │
│ + CREATE folder       "orders-api" (already exists, reused)                   │
│                                                                               │
│ Changes nothing else.  Idempotency key: rev-8842/REM-AL-012/v3                │
│                                                                               │
│ Approvals needed: Requester ✅ (Dana)   SRE ⏳ (Sam)                           │
│                         [Approve]  [Request changes]  [Open as PR instead]    │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

← [Roadmap](08-roadmap.md) · Back to [README](../README.md)
