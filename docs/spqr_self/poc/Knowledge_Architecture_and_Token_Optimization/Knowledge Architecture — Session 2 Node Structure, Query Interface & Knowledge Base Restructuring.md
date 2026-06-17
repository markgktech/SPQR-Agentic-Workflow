---

---
## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — node structure, query interface, knowledge base restructuring

**Document status:** In Progress

**Phase:** PoC — Session 2 (continuation of Session 1 checkpoint)

**Date:** 2026-06-10

**Session scope:** Dense embedding role · knowledge base category analysis · node-type exploration · query interface design

**Purpose:** Captures new decisions, leanings, and open questions that go beyond the Session 1 direction map

**Status legend:** decided · leaning · mixed · open

---

# Overview

This document captures the Session 2 exploration, which went deeper into three areas left open or unaddressed in Session 1: the role of dense embedding, whether the existing four knowledge-base categories (Architecture, Conventions, Lessons, Decisions) are the right structure, and how the query interface between the LLM and the robot warehouse should work. Several Session 1 items were clarified or partially resolved; new open questions emerged around the query protocol.

# Findings

- **Dense embedding is not categorically wrong — the finder vs. retrieval distinction is the key.** Using lightweight semantic search to find the right entry-point node (1–3 IDs) is defensible. Using it as the primary content retrieval mechanism (naive RAG) is not. The two are different systems with different drift and lock-in profiles.
- **The four existing knowledge-base categories are not the right structure.** Architecture was a pre-system snapshot, not a standing separate type. Conventions is an oversized prose blob covering heterogeneous content at very different change rates. Lessons are observations, not decisions. Only Decisions (a01–a22) are close to warehouse-ready.
- **The right question for node-type is not "how many types" but "what does the robot need to read to do its job without asking anything else."** This reframes node-type as a consumer-demand question, not a categorisation exercise.
- **Schema-driven type enforcement is better than application-logic enforcement.** If a decision node must have a scope field, the schema should require it — not a robot if-else block. This is true even with a single universal node type: the type metadata field drives validation rules.
- **"Everything is a decision" is directionally right but needs a boundary.** Some knowledge was never explicitly decided — it was inherited (Swift naming conventions, Apple guidelines) or emerged incrementally. These still need to live somewhere queryable; the proposal-antechamber handles new gaps going forward, but migration must surface them.
- **The query interface is the missing contract.** The expanding-window retrieval pattern (narrow → broader → broadest) is the right direction, but three specific questions about it remain open and block implementation.
- [**LESSONS.md**](http://lessons.md/)** is the most warehouse-ready file today** — already append-only, one entry per run. Its weakness: no links to the decisions or agents it relates to.

# Breakdown

## Session 1 items revisited

| Item | Session 1 status | Session 2 update |
| --- | --- | --- |
| Dense embedding | Discard (as primary) | Clarified: finder use is defended; discard applies to primary retrieval only |
| Node-type | Mixed — one type vs. three | Reframed: schema-driven enforcement preferred; full resolution deferred |
| Retrieval spine | Decided — deterministic | Confirmed; expanding-window layered on top |
| Knowledge base categories | Not addressed | Analysed — four categories are not the right structure; decisions-based spine leaning |

## New topics — where we landed

| # | Topic | Where we landed | Status |
| --- | --- | --- | --- |
| K1 | Dense embedding role | Finder (entry point, 1–3 node IDs) is defensible alongside BM25; primary content retrieval = discard | Decided |
| K2 | Knowledge base spine | Decisions-based; conventions = decisions about code consistency; architecture = not a separate category. Confirmed — Session 3 (3 kinds: decision/constraint/lesson) | Leaning |
| K3 | [ARCHITECTURE.md](http://architecture.md/) | Pre-system snapshot; will not survive as a separate warehouse category; content absorbed into ADRs | Leaning |
| K4 | [CONVENTIONS.md](http://conventions.md/) | Prose blob — too heterogeneous, too many change rates; must be restructured as decision-derived rules | Leaning |
| K5 | [LESSONS.md](http://lessons.md/) | Strongest candidate for direct migration; needs decision and agent linkage added | Leaning |
| K6 | Query trigger | What causes the next query round — robot (zero results) or LLM (insufficient)? | Open |
| K7 | Results per round | N-bounded (top-3 / top-5 / top-8) vs. scope-bounded (everything in the broader scope) | Open |
| K8 | INDEX-first vs. expanding-first | Does the LLM see the ADR index before querying, or is expanding search the only navigation tool? | Open |
| K9 | LLM intent declaration | LLM should state what it is looking for before each round, not after — prevents semantic drift | Leaning |
| K10 | Node-type enforcement | Schema-driven (type metadata drives required fields) preferred over application-logic if-else. Confirmed — Session 3 (universal node + kind, hard/soft rules) | Leaning |

## Query interface — the expanding-window protocol

The proposed query flow has three rounds. Round 1 is a narrow search on the specific problem and its decisions. Round 2 broadens scope if round 1 is insufficient. Round 3 broadens further. The number of rounds is parameterised. Before each round the LLM declares its search intent.

What is not yet defined: the trigger for advancing to the next round, the maximum result count per round, and whether the LLM first sees a manifest (INDEX) so it can select by ID rather than search.

## Knowledge base restructuring — direction

**Decisions (a01–a22):** Most warehouse-ready. Atomic, individual files, Status / Context / Decision / Rationale / Consequences. Missing: explicit supersedes links between files, provenance, and auto-generated index. Manual [INDEX.md](http://index.md/) can drift.

**Conventions:** Not a category — a heterogeneous collection of naming rules, file-structure rules, service lists, UX patterns, actor-isolation tables, and commit-message formats. These have very different consumers (Praetor needs naming; Tribunus needs error patterns) and very different change rates. The restructuring axis is not yet decided.

**Architecture:** Dissolves into the decision layer. The three [ARCHITECTURE.md](http://architecture.md/) invariants (Views never navigate, AppCoordinator owns navigation, local-first) are each traceable to explicit ADRs. No separate node type needed.

**Lessons:** Append-only observation log. Different nature from decisions — a lesson is a point-in-time observation of a pipeline run, not a binding choice. Needs: links to related ADRs, the agent involved, and the ticket.

# Recommendations

- **Do now:** Use the decisions directory (a01–a22) as the prototype warehouse for migration planning — it is already close to atomic ADR format.
- **Do now:** Resolve K6, K7, K8 (the three query-interface open questions) before designing the robot query layer — these block everything else in the query stack.
- **Do now:** Decide the conventions restructuring axis — by consumer (which agent reads it), by change rate (static rule vs. living pattern), or by derivability (can it be inferred from ADRs or not).
- **Defer:** Worker architecture (ingestion workers, query workers) — depends on storage and query interface being settled.
- **Defer:** Ragas / TruLens measurement — valid approach for the golden query set validation phase; premature before schema exists.
- **Discard:** [ARCHITECTURE.md](http://architecture.md/) as a separate warehouse category.
- **Discard:** [CONVENTIONS.md](http://conventions.md/) as a prose blob — it must be restructured before migration, not migrated as-is.

# Descoped

- ID schema, edge ontology, provenance — not reached in this session; Session 3 candidates.
- Proposal-antechamber lifecycle details, concurrency handling — Session 4 or 5 candidates.
- Migration dedup and schema versioning — downstream of schema decisions.

# References

- Session 1 checkpoint: Knowledge Architecture & Token Optimization — Direction Checkpoint PoC (parent page)
- Foodoire decisions directory: Docs/decisions/a01–a22 (22 ADRs, the warehouse prototype)
- SPQR AGENT_LAWS — Law 3 (external record is truth) and Law 4 (independent view) both relevant to query-interface DENY constraints
- Gyuri and Laci roundtable personas — dev process architect and 2026 agentic trends expert