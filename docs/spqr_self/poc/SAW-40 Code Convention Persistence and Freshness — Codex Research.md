---
type: poc
title: "SAW-40 Code Convention Persistence and Freshness — Codex Research"
decides: "Treat SAW-40 as a convention capture, promotion, retrieval, and freshness layer on the existing warehouse, not as a separate store."
status: draft
date: 2026-06-21
tags: [poc, saw-40, warehouse, conventions, codex-research]
---

# SAW-40 Code Convention Persistence and Freshness — Codex Research

## Context / question

Battle-tested code conventions currently remain implicit in code or individual sessions. Later agents must rediscover them and may introduce inconsistent patterns. The warehouse already supplies durable typed nodes, provenance, governed ingest, retrieval, append-only supersession, and flags. SAW-40 must decide whether conventions require another store or a governed lifecycle on this substrate, and how to prevent stale or low-quality knowledge from being trusted.

## Findings

- Do not create a parallel convention store. A convention is normally a warehouse `decision` (project-chosen rule), `constraint` (externally imposed rule), or `lesson` (observed evidence not yet promoted).
- The warehouse solves persistence and retrieval, but not convention discovery, semantic promotion, delivery to the right agent, or code-to-knowledge freshness.
- Graph retrieval cannot establish freshness. Freshness is an evidence and verification problem: compare an active assertion with code, enforcement, dependencies, and superseding decisions.
- Do not ingest code-derived registries or current inventories. Store the durable rule, rationale, applicability boundary, exceptions, provenance, and verification method; keep code as the implementation truth.
- A convention node should contain one independently referenceable and supersedable assertion. Initially keep applicability, evidence, exceptions, and verification guidance in a canonical body template; add schema fields only when a robot must filter, validate, or audit them.
- Use a maturity path: `observed pattern` → `repeated candidate` → `adopted convention` → `enforced convention`. Agents may detect and propose; Senate/owner performs semantic promotion.
- Freshness should be event-driven, not a blind time-to-live: relevant scope changes, conflicting implementations, source/platform changes, removed enforcement, or superseded dependencies trigger review.
- A stale-risk finding should create an audit-plane flag; it must not mutate the convention node. Review then fixes the code, records an exception, or ingests a new node that `supersedes` the old one.

## Recommendation / decision

Implement SAW-40 as a distinct workflow lane built on the existing warehouse, with no second knowledge system and no initial warehouse schema change.

Minimum first slice:

1. Add a focused `convention-capture` skill; keep `warehouse-ingest` as the mechanical proposal contract and link the two.
2. Define capture criteria, non-candidates, maturity levels, required evidence, applicability boundaries, exceptions, and promotion rules.
3. Add a short mandatory ticket output such as `convention_impact: none | followed | candidate | changed | violated`, including referenced node/proposal IDs where applicable.
4. Assign responsibilities: Praetor detects candidates; Probator validates implementation evidence; Curator checks convention compliance/drift; Censura identifies repeated cross-ticket patterns; Senate/owner accepts, revises, rejects, or keeps a finding as a lesson.
5. Require scope-based convention queries before implementation/review and read-before-propose duplicate checks before capture.
6. Pilot the policy against three completed development tickets. Measure useful candidates, false candidates, implicit conventions, duplicate rediscovery, retrieval usefulness, and available freshness evidence.
7. Start freshness as an owner-driven semantic review using the existing flag plane. Add deterministic code scanners or new schema fields only for predicates proven by the pilot.

Expected impact if adopted: a new convention skill; targeted updates to agent mandates/session starters, ticket receipt/handover, retro/Censura output, and Senate ingest judgment. The query verbs and warehouse storage should remain unchanged in the first slice; robot audit or schema extensions are later, evidence-driven work.
