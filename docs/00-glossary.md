# 00 · Glossary (plain English)

New to production operations? Start here. Terms are grouped by theme.

## The process

| Term | Meaning |
|---|---|
| **Production ("prod")** | The live system real customers use. Mistakes here cost money and trust. |
| **Release** | A set of changes being delivered to production. |
| **Production Readiness Review (PRR)** | A structured "are we really ready?" check before a release goes live. |
| **CRQ / Change Request** | A formal record (usually in ServiceNow) describing what will change, when, why, how to undo it, and who approved it. |
| **Backout (rollback) plan** | The tested steps to return to the previous working state if the release goes wrong. |
| **CAB** | Change Advisory Board: the group that approves risky changes. |
| **Change window / freeze** | Allowed times for changes / periods when changes are prohibited (e.g. holiday peak). |
| **Waiver** | A documented, time-limited exception: "we know this check fails; here's why it is acceptable and who approved it." |

## The people

| Term | Meaning |
|---|---|
| **SRE (Site Reliability Engineer)** | Engineer focused on keeping production reliable. Often the final reviewer of readiness. |
| **On-call** | The person (or rotation) who gets alerted, day or night, when production breaks. |

## Design

| Term | Meaning |
|---|---|
| **HLD (High-Level Design)** | The big picture: components and how they connect. |
| **LLD (Low-Level Design)** | The details: data models, APIs, flows. |
| **Component** | One building block (an API, a database, a message queue…). |
| **Component graph** | The design turned into data: components (dots) and connections (lines). |
| **Availability tier (T0-T3)** | How critical a service is; stricter tiers need stronger monitoring and redundancy. |
| **Multi-AZ** | Running in more than one data-centre zone so one failure doesn't take it all down. |
| **RTO / RPO** | *Recovery Time Objective*: how fast we must recover. *Recovery Point Objective*: how much recent data we can afford to lose. |

## Observability: "can we see what is happening?"

| Term | Meaning |
|---|---|
| **Observability** | Being able to understand what a system is doing from the outside, using logs, metrics and traces. |
| **Logs** | A diary of events ("order 123 failed because…"). |
| **Metrics** | Numbers over time (requests per second, error rate, memory used). |
| **Traces** | The path of one request through many services, with timing. |
| **Alert** | An automatic notification when something looks wrong. |
| **Dashboard** | A screen of charts showing system health at a glance. |
| **Runbook** | Step-by-step instructions for handling a specific problem. |
| **SLO / SLI / error budget** | *Service Level Objective*: the target (e.g. 99.95 % of requests succeed). *Indicator*: what we measure. *Error budget*: how much failure the target allows. |
| **Burn-rate alert** | An alert that fires when the error budget is being used up too fast. |
| **Synthetic check / golden-path probe** | A robot that regularly performs a key user journey to prove it works. |
| **Golden signals** | The four essentials for a service: latency, traffic, errors, saturation. |

## Technology

| Term | Meaning |
|---|---|
| **Kafka** | A system for streaming messages between services. **Consumer lag** = how far behind a reader is. |
| **Postgres / RDS** | A popular database / its managed version on AWS. **Replication lag** = how far a copy is behind the main one. |
| **ECS Fargate / ALB** | AWS services for running containers / spreading traffic across them. |
| **Splunk, Grafana, PagerDuty, ServiceNow** | Tools for log search, dashboards and alerts, paging people, and change management. |
| **Connector** | A plug-in that lets PRRA talk to one tool. |
| **Pattern** | A reusable recipe: "for a Postgres database, these things must be monitored." |
| **Check** | One automated yes/no question about readiness, with evidence. |
| **Blueprint** | The list of what a specific design needs. |
| **Overlay diagram** | The second diagram: the design with each component's monitoring status on top. |
| **Remediation / "Create it for me"** | PRRA creating the missing item (after a plan and approval). |
| **Evidence** | The recorded proof behind each result (what was asked, what came back, when). |
| **IaC (Infrastructure as code)** | Defining infrastructure in files so it can be reviewed and repeated. |

---

Back to [README](../README.md)
