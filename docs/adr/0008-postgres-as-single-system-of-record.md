# 0008 · PostgreSQL (with pgvector) as the single system of record

- **Status:** Proposed
- **Date:** 2026-10-31
- **Deciders:** Architecture, Platform

## Context
We need relational integrity (reviews, graphs, results, waivers), row-level security for multi-tenancy, JSON flexibility for evidence metadata, and embeddings for design retrieval. Operating several data stores adds cost and failure modes.

## Decision
Use **PostgreSQL 16** for core data, JSONB for flexible payloads, **row-level security** for tenant isolation, and **pgvector** for embeddings. Large artifacts (evidence, reports, documents) go to **S3-compatible object storage** with the database holding hashes and metadata. Redis only for cache and locks.

## Consequences
- **Good:** one primary store to operate, back up and secure; strong consistency; ubiquitous skills.
- **Bad:** vector search scale is bounded (acceptable for design-document volumes); need discipline with JSONB.
- **Follow-ups:** index and partitioning strategy for check results; archive policy.

## Alternatives considered
| Option | Why not |
|---|---|
| Separate vector DB | Extra system for modest volumes |
| Document database | Weaker relational integrity for audit and reporting |
