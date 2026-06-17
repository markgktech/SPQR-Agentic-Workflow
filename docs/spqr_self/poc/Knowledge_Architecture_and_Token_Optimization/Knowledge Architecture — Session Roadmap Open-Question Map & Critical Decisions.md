---

---
## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — session planning, open-question grouping, decision sequencing

**Document status:** In Progress

**Phase:** PoC — planning artifact (between Session 2 and Session 3)

**Date:** 2026-06-10

**Usage: **claude-fable-5:  3.6k input, 15.6k output, 410.7k cache read, 57.5k cache write ($1.95)

**Session scope:** Roadmap only — no new architecture decisions are made on this page

**Purpose:** Groups every open question from Session 1, Session 2, and the raw preparation notes into dependency-ordered sessions runnable in separate (Sonnet) contexts

**Status legend:** decided · leaning · mixed · open

---

# Overview

This page consolidates all open or partially open questions across the three existing documents into six dependency-ordered work sessions plus one parked strategic lane. It is a routing map, not a decision record: each session has a scope, a list of **fixed inputs** (decided items it must not re-litigate), the open questions it **owns**, and an expected output. The parent checkpoint page remains the single source of truth for direction status — this page only sequences the work, and each finished session folds its results back into the parent direction table.

# Findings

- **One unreconciled contradiction exists between the documents.** Session 1 commits to a git-native markdown document-graph ("portable, diffable, no server"), while the preparation notes assume a database substrate (Postgres + pgvector, BM25, recursive CTE traversal). The two are reconcilable — markdown as source of truth, DB as a derived query index, which matches the append-only + derived-projection principle — but this has not been decided anywhere. It is the most critical open decision; owned by Session 7.
- **The open questions cluster into six groups with a clear dependency spine:** node schema → query contract → content restructuring → write path & audit → storage substrate → migration. Theme-only grouping (as in the preparation notes) hides these dependencies; running sessions out of order forces later sessions to guess at unmade upstream decisions.
- **Session 1 strategic leftovers are not warehouse-internal.** CONSULT role scope, independence-vs-continuity (J), runtime portability (I), and Curator value revision are SPQR-level questions. They are parked in a separate strategic lane so they do not bloat warehouse sessions.
- **The Session 2 open items (K6–K8) survive the independent regrouping unchanged** — they genuinely form the query-contract core and stay together in one session.
- **Session 3 (node schema) is the highest-leverage session.** Every downstream session consumes its output; an error there propagates everywhere. It is the one session where a higher judgment tier (Opus rather than Sonnet) is worth considering.

# Breakdown — the session map

## Session 3 — Node schema & graph ontology (foundation) — ✅ CLOSED (see Session 3 doc)

- **Scope:** the shape of a node and an edge; nothing about storage technology or retrieval.
- **Fixed inputs:** append-only + supersede (decided); atomic assertion principle; deterministic retrieval spine (C, decided); decisions-based spine (K2, leaning); schema-driven enforcement preferred (K10, leaning).
- **Owns:** universal node type vs. typed nodes — final close (S1-D first half); the schema-driven validation field set per type (K10); ID schema (stable IDs); edge ontology (supersedes / relates-to / derived-from / constrains…); provenance fields (who, when, which run); layering — one bucket with layers vs. separate stores (S1-D second half); the "everything is a decision" boundary — where inherited knowledge (Swift naming, Apple guidelines) lives.
- **Output:** node + edge schema draft; closes S1-D and K10.

## Session 4 — Query interface contract — ✅ CLOSED (see Session 4 doc)

- **Fixed inputs:** deterministic spine (C, decided); expanding-window direction; finder-embedding role (K1, decided); intent declaration before each round (K9, leaning — confirm here); Session 3 schema.
- **Owns:** K6 — what triggers the next round (robot zero-results vs. LLM judges insufficient); K7 — results per round, N-bounded vs. scope-bounded; K8 — INDEX/manifest-first vs. expanding-search-only navigation; round-count parameterisation; deep-dig vs. high-altitude query modes (they need different data shapes); central query budget so the LLM cannot burn tokens unboundedly; mapping the archetype DENY side onto query permissions.
- **Output:** the query protocol contract; closes K6–K9.

## Session 5 — Knowledge base restructuring (can run parallel to Session 4) — ✅ CLOSED (see Session 5 doc)

- **Fixed inputs:** four categories are not the right structure (S2 finding); decisions a01–a22 are the prototype; [ARCHITECTURE.md](http://architecture.md/) dissolves into ADRs (K3, leaning); [CONVENTIONS.md](http://conventions.md/) must be restructured before migration (K4); Session 3 schema.
- **Owns:** the conventions restructuring axis — by consumer agent, by change rate, or by derivability from ADRs; lessons linkage model (related ADRs + agent + ticket); verifying the three architecture invariants trace to explicit ADRs; the a01–a22 gap-fill plan (supersedes links, provenance, auto-generated index replacing manual [INDEX.md](http://index.md/)).
- **Output:** target structure per existing file; migration-readiness list.

## Session 6 — Write path, antechamber & audit  — ✅ CLOSED (see Session 6 doc)

- **Fixed inputs:** two-phase commit direction (small agents propose, Senate evaluates and ingests); auditor flags but never mutates; Session 3 schema.
- **Owns:** proposal-antechamber lifecycle (proposed → evaluated → ingested / rejected), Run ID / Session ID binding; antechamber visibility for in-sequence agents and delta/aggregation view for expensive agents; concurrency handling; pre-ingest query check (what does this connect to — and is a missed back-link an audit case?); auditor mandate detail — contradiction flagging, orphan-node watch; the flag maintenance process (who clears flags, when — retro candidate); severity fixed vs. emergent (S1-F); promotion gate per-robot vs. global (S1-G); cost of scope discipline in the append-only model (S1-B).
- **Output:** write-path state machine + audit policy; closes S1-B, S1-F, S1-G.

## Session 7 — Storage substrate & retrieval runtime  — ✅ CLOSED (see Session 7 doc)

- **Fixed inputs:** Session 3 schema; Session 4 query contract; Neo4j discarded; naive embedding-RAG discarded; ~10k node planning assumption.
- **Owns:** **resolve the markdown-vs-database contradiction** (git-native markdown as truth + derived DB index is the candidate reconciliation); Postgres + pgvector vs. in-house build; hybrid retrieval (BM25 + dense + RRF + graph) vs. graph-lookup-only; recursive CTE traversal design; hosting (docker); worker measurement — Ragas vs. TruLens, golden query set (context relevance / groundedness / answer relevance).
- **Output:** substrate decision + runtime sketch.

## Session 8 — Migration   — ✅ CLOSED (see Session 8 doc)

- **Fixed inputs:** everything above; divide-and-conquer direction (decided in preparation notes).
- **Owns:** chunking discipline (2–3 pages per pass, strict prompt, JSON structured output that doubles as the normal ingestion format); dedup strategy; schema versioning; surfacing inherited / never-explicitly-decided knowledge during migration; volume and LLM-limit handling.
- **Output:** migration runbook draft.

## Strategic lane — parked, not warehouse sessions

Independence vs. continuity full treatment (J) · CONSULT role scope + orchestrator lineage · runtime portability / resell reality (I) · Curator value revision · model-tiering measurement (depends on Session 6 audit layer).

# Recommendations

- **Keep the session split — but consolidation is not a deferred step.** Every session ends by folding its closed items back into the parent checkpoint's direction table (status column) in the same session. Deferring consolidation reproduces exactly the drift problem (W2) this project exists to kill: the session docs are the append-only log, the parent page is the derived projection — apply the system's own principle to its own design process.
- **Every session starts with a session-starter block:** scope, fixed inputs ("treat as decided — do not re-litigate"), owned questions, expected output, descoped. This is the main guard against re-litigation drift across separate Sonnet contexts.
- **Run in dependency order 3 → 8;** Session 5 may run parallel to Session 4 (both depend only on Session 3).
- **Consider Opus for Session 3 only** — it is the foundation every other session consumes; the rest are scoped enough for Sonnet.
- **Each session doc follows the Session 2 template** (Metadata / Overview / Findings / Breakdown / Recommendations / Descoped / References).

# Descoped

- No architecture decisions on this page — it routes them to sessions.
- Implementation and code — still downstream of all of the above.
- Strategic-lane items — parked until the warehouse sessions close.

# References

- Session 1 checkpoint: Knowledge Architecture & Token Optimization — Direction Checkpoint PoC (parent page)
- Session 2: Node Structure, Query Interface & Knowledge Base Restructuring (sibling page)
- Separate preparation for warehouse — raw notes (sibling page) and Lookup guides
- SPQR AGENT_LAWS — Law 3 (the external record is truth) underpins the fold-back-per-session rule