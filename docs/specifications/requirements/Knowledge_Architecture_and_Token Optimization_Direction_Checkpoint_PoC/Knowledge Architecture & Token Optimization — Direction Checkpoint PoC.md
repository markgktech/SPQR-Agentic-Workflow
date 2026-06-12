---

---
## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — storage, mutation, retrieval, and the agent load model

**Document status:** In Progress

**Phase:** PoC (conceptual direction map; pre-build)

**Date:** 2026-06-07

**Session scope:** High-level direction brainstorm — no code, no execution output

**Purpose:** Checkpoint for independent-agent review of the proposed solution direction

**Status legend:** decided · leaning · mixed · open

---

# Overview

This PoC consolidates a high-level direction for how SPQR should store, evolve, retrieve, and load project knowledge — with the goal of cutting token cost, eliminating decision drift, and staying portable across tools and models. In scope: the conceptual architecture (the layer model, the problem themes, the agent load model). Out of scope: implementation, file-level design, and migration mechanics — those are downstream of the decisions captured here.

# Motivation

Three pressures triggered this exploration:

- **Token cost** — agents hold too much in context just in case, and prose retrieval over MCP is expensive and non-deterministic.
- **Decision drift** — decisions made in one place do not reliably flow back to the source of truth, so the record goes stale and self-contradictory.
- **Lock-in** — machine-truth living in Notion, and the workflow being Claude-runtime-specific, deepens dependence on tools that should be replaceable.

Doing nothing keeps the workflow functional but increasingly expensive to run and to trust: the record drifts, the token bill scales with the wrong things, and the system stays welded to specific vendors.

# Findings

- **The knowledge layer is the real target, not the skill layer.** SPQR already loads stage-skills with discipline; project knowledge (conventions, decisions, docs) still loads as monoliths. The payoff is bringing knowledge-load up to the discipline that skill-load already has.
- **Token cost has two independent axes:** context volume and judgment density. Each archetype needs a different lever — volume reduction for high-volume roles, model-tier for high-judgment roles — not a blanket downgrade.
- **The deterministic robot layer is the zero-cost endpoint.** Whatever needs no judgment (folding, validation, sync, manifest resolution) moves out of the LLM entirely and costs zero tokens.
- **The per-stage load model has two halves:** an ALLOW side (minimal necessary, serves tokens) and a DENY side (forbidden context, serves independence). Review agents must be shielded from the reasoning they are meant to independently re-derive.
- **Demand-driven warehouse:** its shape follows what consumers retrieve, not what is convenient to store. The agent is the warehouse primary consumer; the human is served by a projection.
- **Document-graph beats both Neo4j and embedding-RAG for these constraints.** The most future-proof graph here is plain markdown with stable IDs and links — portable, diffable, model-readable, no server.
- **Append-only decisions + derived projection removes drift structurally** — one write path, deterministic fold; out-of-band changes surface as detectable divergence, not silent corruption.
- **The independent-review tier is already minimal-load by design** (fresh eyes), so token thrift and review independence point the same way there. Waste concentrates at the DELIBERATE and EXECUTE tiers.

# Breakdown

## Layer model — WHY / WHAT / HOW

Keep three layers separate so the path from where, to where, by what means stays visible: if a HOW fails, the WHY and WHAT remain stable and only the HOW is re-picked. The same typed-node and link structure used for the knowledge base is used for this map — the structure is self-similar.

## WHY — durable goals

- **W1 — Token optimization:** context volume + judgment density + cheaper models where proven.
- **W2 — Drift-free knowledge:** decisions reliably flow back to the source of truth.
- **W3 — Self-reliance / portability:** no deepening dependence on Notion, the Claude runtime, or infra.

## WHAT / HOW — problem themes

| # | Problem | Where we landed | Status |
| --- | --- | --- | --- |
| A | Knowledge form | Document-graph; semi-structured / ADR (frontmatter + prose body); git-native; Notion becomes a projection. Node + edge schema fixed (S3); per-file target structure + migration-readiness (S5); storage substrate fixed (S7): markdown source-of-truth + derived disposable SQLite index, embeddings deferred behind a measured trigger | Decided |
| B | Mutation model | Decisions append-only; state as a derived projection; superseded is derived from an incoming edge, never a written field (S3 invariant). Scope-discipline cost closed (S6): accepted trade — monotonic growth, retired nodes hidden by the S4 active-filter, node/scope count = bleed monitor | Mixed |
| C | Retrieval | Deterministic (manifest + graph traversal + agentic); not embedding now; load model done at altitude. Query protocol contract fixed (S4). Runtime fixed (S7): embedded SQLite derived index; FTS5/BM25 finder side-door; dense embedding deferred behind a measured trigger (S4 trace WRONG-ENTRY/ABSENT rates) | Decided |
| D | Knowledge types | Three kinds (decision/constraint/lesson); spec excluded as source-of-intent; single logical store, derived views. Decided — Session 3; existing files restructured into kinds — conventions axis, lessons linkage, invariant trace, a01–a22 gap-fill (Session 5) | Mixed |
| E | Determinism line | LLM for judgment, robot for the rest; the line moves right as the gate allows | Decided (principle) |
| F | Audit layer | Two-tier auditor (continuous robot tripwires + periodic owner-driven semantic audit), flag-only, never mutates. Flag = append-only audit-node on a separate plane, derived open/resolved status. Severity closed (S6): hybrid emergent (frequency × damage) + fixed floor for categorically-critical | Leaning |
| G | Promotion gate | Frequency × damage threshold. Closed (S6): per-risk-tier (not global, not literal per-check); promotes checks (LLM→robot) and proposal classes (skip Senate → auto-ingest); reversible (post-promotion flag demotes); owner-driven trigger for now | Leaning |
| H | Build vs buy | Own, git-native; third party only if it outgrows manual maintenance. Closed (S7): embedded SQLite (no server, single file, derived/disposable); Postgres + pgvector documented as the upgrade path if scale or multi-project sharing forces it | Decided |
| I | Runtime portability | Clean seam, do not abstract early, lean on MCP / A2A. Open: how real the resell scenario is | Leaning |
| J | Independence vs continuity | Independence wins for now; the DENY-side load constraint is critical. Open: full treatment later | Mixed |

## Archetypes — the agent load model

| Archetype | Who | Needs (knowledge) | Load profile | Judgment |
| --- | --- | --- | --- | --- |
| DELIBERATE | Senate:Consilium | Problem + relevant prior decisions + high-level state; not conventions | Broad access, high-altitude load | Highest — Opus |
| EXECUTE | Praetor, Quaestor | Mandate + scope decisions / domain patterns + current state + conventions | Scoped to the ticket blast radius | Medium |
| SCRUTINIZE | Tribunus, Probator, Curator | The diff + mandate trail + checklist; not prior reasoning | Deliberately minimal (fresh eyes) | Medium-low |
| SYNTHESIZE | Senate:Censura, Retrospector | The record across the run(s): output, comment history, lessons, churn | High volume, record layer | High to medium |
| CONSULT (missing 5th) | Currently owner-filled | Big picture + reality-check + routing | High judgment, state-aware, light per call | High — orchestrator ancestor |
| ROBOT (zero point) | Deterministic layer | Reads the warehouse deterministically | Zero — holds nothing in context | None |

## Cross-cutting concepts

- **Model-tiering** is the objective (serves W1) and is measured by the audit layer: flag rate times severity, calibrated by a periodic semantic audit.
- **Two-axis cost:** volume times judgment; pick the lever per archetype.
- **Robot offload:** push every judgment-free task into the deterministic layer; that work then costs zero tokens.
- **C3 has two halves:** ALLOW (token) and DENY (independence); review agents must not auto-load journey-memory.
- **Obsidian as substrate:** a HOW under the knowledge-form and the human-projection surface; serves W3 — it uses the data, does not own it.
- **Dependency model:** generic and local SPQR stay connected by an umbilical cord — versioned, non-destructive updates; breaking changes need migration, not just a swap.
- **Warehouse boundary:** project-warehouse vs SPQR-warehouse vs SPQR-spec; the warehouse schema is generic (the seed), the content is local (it grows per project).

# Recommendations

- **Do now:** Treat the warehouse as the spine — git-native document-graph, append-only decisions, derived state projection; give DELIBERATE and EXECUTE agents scoped knowledge-queries; shield review agents from journey-memory.
- **Do now:** Kick off Obsidian in parallel (new vault, docs and spec first) without migrating — prove value before adopting; keep Notion as system-of-record during the trial.
- **Defer:** CONSULT role scope and its orchestrator lineage; full treatment of independence-vs-continuity (J); Curator value revision; embedding finder (only if deterministic retrieval proves insufficient).
- **Defer:** Fine-grained per-stage query design — downstream of the warehouse existing.
- **Discard (for now):** Naive embedding-RAG as primary retrieval; Neo4j / graph-DB; premature runtime abstraction; machine-truth living in Notion.

# Descoped

- Implementation and file-level design — not here, not now.
- Migration mechanics (Notion to Obsidian; project docs to generic) — staged later, after the conceptual map is validated.
- Quantitative token telemetry — proxy signals (flags) first.

# References

- SPQR agent definitions — generic repo docs/agents (Senate, Quaestor, Praetor, Tribunus, Probator, Curator), docs/retro/retrospector, docs/upgrade/upgrade-agent
- AGENT_LAWS — the four laws (Stay in Character, Anti Meeseeks, Don't be Dory, Be like Spock)
- Retro #2 — First OPUS runs (source of the metadata-header pattern)
- Prior PoC — Sequential Agent Workflow, 2026 Upgrade

[https://www.notion.so/Knowledge-Architecture-Token-Optimization-Direction-Checkpoint-PoC-37868d5de1e8817fa17de0a18b592178?source=copy_link](https://www.notion.so/Knowledge-Architecture-Token-Optimization-Direction-Checkpoint-PoC-37868d5de1e8817fa17de0a18b592178)

[https://www.notion.so/Knowledge-Architecture-Token-Optimization-Direction-Checkpoint-PoC-37868d5de1e8817fa17de0a18b592178?source=copy_link](https://www.notion.so/Knowledge-Architecture-Token-Optimization-Direction-Checkpoint-PoC-37868d5de1e8817fa17de0a18b592178)

[https://www.notion.so/Knowledge-Architecture-Token-Optimization-Direction-Checkpoint-PoC-37868d5de1e8817fa17de0a18b592178?source=copy_link](https://www.notion.so/Knowledge-Architecture-Token-Optimization-Direction-Checkpoint-PoC-37868d5de1e8817fa17de0a18b592178)

[[Separate preparation for warehouse]]

[[Knowledge Architecture — Session 2 Node Structure, Query Interface & Knowledge Base Restructuring]]

[[Knowledge Architecture — Session Roadmap Open-Question Map & Critical Decisions]]

[[Knowledge Architecture — Session 3 Node Schema & Graph Ontology]]

[[Knowledge Architecture — Session 4 Query Interface Contract]]

[[Knowledge Architecture — Session 5 Knowledge Base Restructuring]]

[[Knowledge Architecture — Session 6 Write Path, Antechamber & Audit]]

[[Knowledge Architecture — Session 7 Storage Substrate & Retrieval Runtime]]

[[Knowledge Architecture — Session 8 Migration]]