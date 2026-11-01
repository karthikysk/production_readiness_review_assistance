# 03 · High-Level Design (HLD)

> Audience: architects, engineers, SREs, engineering managers.
> Companion: [Low-Level Design](lld.md) · [Observability Blueprint](../04-observability-blueprint.md) · [ADRs](../adr/README.md)

---

## 1. System context (who talks to whom)

PRRA sits **between people and the tools they already use**. It reads from them, scores what it finds, and (when approved) writes back.

```mermaid
flowchart TB
    subgraph People
        DEV["Developer<br/>requests review, fixes gaps"]
        SRE["SRE reviewer<br/>approves readiness"]
        CM["Change manager<br/>CRQ quality"]
        MGR["Engineering manager<br/>portfolio view"]
    end

    PRRA(["PRRA<br/>Production Readiness Review Assistant"])

    subgraph Systems_of_record["Systems of record"]
        SN["ServiceNow<br/>CRQ, tasks, CMDB"]
        DOCS["Design docs<br/>Confluence, GitHub, uploads"]
        CAT["Service catalogue / CMDB"]
    end

    subgraph Observability_tools["Observability and ops tools"]
        SPL["Splunk<br/>logs, saved searches, alerts"]
        GRA["Grafana / Datadog / CloudWatch<br/>dashboards, metrics, alerts"]
        TRC["Tracing<br/>Jaeger, Tempo, X-Ray"]
        PD["PagerDuty / Opsgenie<br/>on-call, escalation"]
    end

    subgraph Delivery_and_platform["Delivery and platform"]
        CI["CI/CD<br/>GitHub Actions, Jenkins, ArgoCD"]
        AWS["Cloud and runtime<br/>AWS, Kubernetes"]
        KAF["Data platforms<br/>Kafka, Postgres, ..."]
    end

    LLM["LLM provider<br/>policy-controlled"]

    DEV --> PRRA
    SRE --> PRRA
    CM --> PRRA
    MGR --> PRRA

    PRRA <--> SN
    PRRA --> DOCS
    PRRA --> CAT
    PRRA --> SPL
    PRRA <--> GRA
    PRRA --> TRC
    PRRA <--> PD
    PRRA --> CI
    PRRA --> AWS
    PRRA --> KAF
    PRRA -. redacted prompts .-> LLM
```

**Arrow meaning:** a single arrow is mostly *read*; a double arrow includes *write* (remediation or CRQ write-back), which is always approval-gated.

---

## 2. The big picture in four stages

```mermaid
flowchart LR
    subgraph S1["1 UNDERSTAND"]
        A1["Read CRQ"] --> A2["Read HLD / LLD"] --> A3["Component graph<br/>+ availability tier"]
    end
    subgraph S2["2 PLAN"]
        B1["Pattern library<br/>per component type"] --> B2["Observability<br/>blueprint"]
    end
    subgraph S3["3 VERIFY"]
        C1["Run checks<br/>via connectors"] --> C2["Scorecard<br/>+ evidence"]
    end
    subgraph S4["4 FIX"]
        D1["Remediation plan"] --> D2["Approve"] --> D3["Apply + re-verify"]
    end
    S1 --> S2 --> S3 --> S4
    S4 -. loop until ready .-> S3
```

---

## 3. Container view (deployable pieces)

```mermaid
flowchart TB
    UI["Web UI<br/>React / TypeScript"]
    CLI["CLI and API clients"]

    subgraph Edge
        GW["API Gateway / BFF<br/>authN, authZ, rate limit"]
    end

    subgraph Core["PRRA core (modular services)"]
        RS["Review Service<br/>lifecycle, roles, verdicts"]
        DI["Design Intelligence Service<br/>ingest, parse, graph"]
        BP["Blueprint Service<br/>pattern library, generator"]
        CE["Check Engine<br/>scheduler, workers, scoring"]
        RM["Remediation Service<br/>plan, approve, apply, verify"]
        ER["Evidence and Report Service<br/>evidence store, reports, write-back"]
        NS["Notification Service"]
        ID["Identity and Policy<br/>RBAC, audit"]
    end

    subgraph Plugins["Connector runtime (sandboxed)"]
        CH["Connector Hub<br/>registry, creds broker, health"]
        C1["ServiceNow"]
        C2["Splunk"]
        C3["Grafana"]
        C4["GitHub Actions"]
        C5["PagerDuty"]
        C6["AWS"]
        CN["... SDK plug-ins"]
    end

    subgraph Data["Data plane"]
        PG[("PostgreSQL<br/>core data + pgvector")]
        OBJ[("Object storage<br/>evidence, reports, docs")]
        Q[["Workflow engine<br/>Temporal + queue"]]
        RD[("Redis<br/>cache, locks")]
        VT[/"Vault / Secrets Manager"/]
    end

    LLMGW["LLM Gateway<br/>redaction, routing, budget, cache"]
    OTEL["OpenTelemetry Collector<br/>PRRA observes itself"]

    UI --> GW
    CLI --> GW
    GW --> RS
    GW --> DI
    GW --> BP
    GW --> CE
    GW --> RM
    GW --> ER

    RS --> PG
    DI --> PG
    DI --> LLMGW
    BP --> PG
    CE --> Q
    RM --> Q
    CE --> CH
    RM --> CH
    ER --> OBJ
    ER --> PG
    ER --> CH
    CH --> C1
    CH --> C2
    CH --> C3
    CH --> C4
    CH --> C5
    CH --> C6
    CH --> CN
    CH --> VT
    RS --> NS
    ID --- GW
    Core -.-> OTEL
    CE --> RD
```

### Container responsibilities

| Container | Responsibility | State | Scales by |
|---|---|---|---|
| **Web UI** | Review pages, interactive diagrams, approvals | none | CDN / replicas |
| **API Gateway / BFF** | OIDC login, RBAC enforcement, request shaping, rate limiting | none | replicas |
| **Review Service** | Review entity, lifecycle state machine, roles, verdict | Postgres | replicas |
| **Design Intelligence** | Ingest documents, extract component graph with citations, version designs | Postgres, object store, pgvector | workers |
| **Blueprint Service** | Pattern Library; generate requirements per graph + tier; diagram overlay model | Postgres | replicas |
| **Check Engine** | Resolve which checks apply, schedule, execute in parallel, score | workflow state | workers |
| **Remediation Service** | Build plans, enforce approvals, apply idempotent actions, verify, roll back | workflow state | workers |
| **Evidence & Report** | Immutable evidence, report rendering, CRQ write-back | object store + Postgres | workers |
| **Connector Hub + connectors** | Uniform capability API in front of external tools; credential brokering; health | stateless (+ cache) | per connector |
| **LLM Gateway** | Redact, route, budget, cache and log all model calls | Redis, Postgres | replicas |
| **Identity & Policy** | Users, roles, team scoping, audit trail | Postgres | replicas |
| **Notification** | Email / Slack / Teams / webhooks | queue | workers |

> **Start simple:** v1 ships as a **modular monolith** (single deployable with these modules, separate packages) plus separate **connector** and **worker** processes. Boundaries are enforced in code so any module can be split later. See [ADR-0002](../adr/0002-modular-monolith-first.md).

---

## 4. Key flows

### 4.1 End-to-end review (happy path)

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    actor SRE as SRE reviewer
    participant UI as Web UI
    participant RS as Review Service
    participant DI as Design Intelligence
    participant BP as Blueprint Service
    participant CE as Check Engine
    participant CH as Connectors
    participant RM as Remediation
    participant ER as Evidence and Report

    Dev->>UI: Start review (service, CRQ, design link)
    UI->>RS: create review
    RS->>DI: ingest design
    DI-->>RS: component graph (with citations)
    Dev->>UI: confirm / edit graph
    RS->>BP: generate blueprint (graph + tier)
    BP-->>UI: blueprint + overlay diagram
    UI->>CE: run checks
    CE->>CH: query ServiceNow, Splunk, Grafana, CI, PagerDuty, AWS
    CH-->>CE: facts
    CE-->>ER: store evidence
    CE-->>UI: scorecard + findings
    Dev->>UI: Create it for me (missing dashboard)
    UI->>RM: build plan
    RM-->>UI: plan + diff + risk
    SRE->>UI: approve plan
    RM->>CH: apply (idempotent)
    RM->>CE: re-verify
    CE-->>UI: updated scorecard
    SRE->>UI: set verdict (Ready / Conditional)
    UI->>RS: verdict
    RS->>ER: write back to CRQ + evidence pack
```

### 4.2 Data flow and trust boundaries

```mermaid
flowchart LR
    subgraph Untrusted["Untrusted inputs"]
        D["Design documents<br/>(may contain prompt injection)"]
        X["External tool responses"]
    end
    subgraph Trusted["PRRA trust zone"]
        SAN["Sanitise and parse"]
        RED["Redact secrets / PII"]
        LG["LLM Gateway"]
        VAL["Schema validation<br/>+ human confirmation"]
        DB[("Core data")]
    end
    D --> SAN --> RED --> LG --> VAL --> DB
    X --> SAN
    LG -. never gets credentials .- X
```

Key point: **LLM output is treated as a *suggestion* that must pass schema validation and (for design extraction) human confirmation** before it influences any check. See [Security](../07-security-and-compliance.md).

---

## 5. Architectural characteristics (what we optimise for)

| Characteristic | How the design supports it |
|---|---|
| **Trustworthiness** | Deterministic checks; evidence for every result; AI only assists |
| **Extensibility** | Connector SDK, check DSL, pattern packs, all versioned plug-ins |
| **Safety** | Read-only default; plan → approve → apply; idempotent actions; audit |
| **Explainability** | Findings carry why / how / owner; AI statements cite sources |
| **Operability** | OpenTelemetry everywhere; SLOs for PRRA itself; runbooks |
| **Portability** | Kubernetes + Postgres + S3-compatible storage; no cloud lock-in |
| **Simplicity first** | Modular monolith; boring tech; split only when measured |

## 6. Technology choices (proposed, see ADRs)

| Concern | Choice | Why | Alternatives considered |
|---|---|---|---|
| Backend language | **Python 3.12 + FastAPI** | Best ecosystem for LLM + integrations; fast to build connectors | TypeScript (NestJS), Go, Java |
| Frontend | **React + TypeScript** | Mature; rich diagram libs | Vue, Svelte |
| Diagrams | **Mermaid** (docs + rendering) and **React Flow** (interactive) | Text-diff friendly; GitHub-native | PlantUML, draw.io |
| Primary DB | **PostgreSQL 16 + pgvector** | Relational integrity + embeddings in one store | Separate vector DB |
| Workflow | **Temporal** | Durable long-running remediation / retries / human approval waits | Celery, custom state machine |
| Object store | **S3-compatible** | Evidence, reports | filesystem |
| Cache/locks | **Redis** | Rate-limit, short cache | in-DB |
| Secrets | **Vault / cloud secrets manager** | No secrets in DB | KMS-encrypted columns |
| AuthN | **OIDC/SAML SSO** | Enterprise default | local users (dev only) |
| Telemetry | **OpenTelemetry** → org's backend | Standard | vendor SDKs |
| IaC | **Terraform + Helm** | Common in SRE orgs | Pulumi, CDK |
| LLM | Provider-agnostic gateway; Claude, others configurable | Avoid lock-in; data policy per org | single vendor SDK |

## 7. Cross-cutting concerns (summary)

- **Multi-tenancy:** `org_id` on every row, enforced by row-level security; tenant-scoped connector credentials.
- **Idempotency:** every write carries an idempotency key `(review_id, remediation_item_id, version)`.
- **Rate-limit awareness:** per-connector token buckets; back-off with jitter.
- **Time:** all timestamps UTC; display in user's zone.
- **Config:** 12-factor; feature flags for connectors and remediation types.
- **Failure policy:** *unknown ≠ pass*. Failure to evaluate yields `error`/`skip` and blocks a "Ready" recommendation unless waived.
- **Versioning:** designs, patterns, checks, connectors and reports are all versioned; a review pins the versions it was evaluated with so results are reproducible.

## 8. Risks and mitigations (architecture level)

| Risk | Impact | Mitigation |
|---|---|---|
| LLM mis-reads a design | Wrong blueprint | Human confirmation step; citations; confidence; structured manifest alternative |
| Over-privileged connector credentials | Security incident | Read-only default; scoped tokens; sandbox; audit; short-lived creds where supported |
| Connector API changes / rate limits | Flaky checks | Contract tests with recorded fixtures; back-off; `error` ≠ `fail` |
| Teams game the checks | False confidence | Evidence over attestations; sample deep checks; waiver visibility |
| Tool becomes a bottleneck itself | Slower releases | Manual fallback path; SLO; async design; clear "unknown" handling |
| Pattern library rots | Stale guidance | Ownership, versioning, review cadence, usage analytics |
| Cost of LLM calls | Budget overrun | Gateway budgets, caching, small models for extraction, deterministic fast paths |

Next → [Low-Level Design](lld.md)
