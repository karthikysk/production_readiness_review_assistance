# Contributing to PRRA

Thanks for helping! This project is in its **design phase**, so most contributions are to documents, diagrams and the backlog.

## Ways to contribute

| You are… | Great contributions |
|---|---|
| An **SRE** | Review the [pattern library](docs/04-observability-blueprint.md#5-pattern-library) and [checks](docs/05-checks-catalog.md); propose missing signals or wrong thresholds |
| An **engineer** | Challenge the [HLD](docs/03-architecture/hld.md)/[LLD](docs/03-architecture/lld.md); propose or review [ADRs](docs/adr/README.md) |
| A **security person** | Review the [threat model](docs/07-security-and-compliance.md#3-threat-model-stride-summary) |
| A **designer / writer** | Improve [UX](docs/09-ux-and-journeys.md), diagrams, readability |
| An **integrator** | Draft capability interfaces for your tool ([SDK](docs/06-connector-sdk.md)) |

## Workflow

1. Open or comment on an **issue** first for anything non-trivial.
2. Branch from `main`: `docs/<topic>`, `feat/<topic>` or `fix/<topic>`.
3. Keep PRs small and focused; link the issue (`Closes #n`) and the requirement ID (`FR-xxx`).
4. Reviews are by at least one maintainer. Docs and ADRs are reviewed like code.

## Documentation conventions

- **Diagrams as code** (Mermaid) so they diff and render on GitHub. Keep node labels in quotes; use `<br/>` for line breaks.
- Write for a **mixed audience**: lead with plain language, then detail. Define jargon in the [glossary](docs/00-glossary.md).
- Requirements use stable IDs (`FR-`, `NFR-`, `REQ-`, `OBS-`, `REM-`); don't renumber.
- A decision that is hard to reverse needs an **ADR** (copy [`docs/adr/template.md`](docs/adr/template.md)).
- Check that Mermaid renders in the PR preview before requesting review.

## Commit messages

Short imperative subject, optional body explaining *why*. Example: `docs: add Redis pattern to observability blueprint`.

## Code of conduct

Be kind, assume good intent, critique ideas not people.
