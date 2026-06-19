---

---
## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — storage substrate, derived index, write-path runtime, retrieval engine, measurement

**Document status:** Complete — parent fold-back applied

**Phase:** PoC — Session 7 (depends on S3 schema + S4 query contract; consumes the S6 write path)

**Date:** 2026-06-10

**Usage:** claude-opus-4-8:  6.8k input, 61.6k output, 1.7m cache read, 107.7k cache write ($3.08)

**Session scope:** The physical realization — storage substrate, the derived index, the fold, the serializing gate, the finder engine, and retrieval measurement. Resolves the markdown-vs-DB contradiction (the roadmap's most critical open decision).

**Purpose:** Settle the substrate and the runtime so migration (S8) builds on a fixed foundation.

**Status legend:** decided · leaning · mixed · open

---

# Overview

Session 7 resolves the one unreconciled contradiction in the project: Session 1's git-native markdown document-graph versus the preparation notes' database substrate (Postgres + pgvector, BM25, recursive CTE). Resolution: **markdown is the source of truth; a disposable, rebuildable index is a derived projection** — the system's own append-only + derived-projection principle applied to its own storage. The index engine is **embedded SQLite** (not a Postgres server, not a custom build), chosen as the lowest-regret option that is robust to the still-open robot-lifecycle question. Embeddings are **deferred behind a measured trigger**; the finder side-door runs on FTS5/BM25 now. The serializing gate is the **single-writer ingest-robot plus a SQLite write transaction**. Retrieval measurement is reframed from RAG-answer-eval to **IR-retrieval-eval**. Everything here is a fixed input for migration (S8).

# Findings

- **The markdown-vs-DB contradiction is not a true conflict** — it dissolves into markdown-as-truth + derived-index, which is the project's own core principle (append-only + derived projection) applied to storage. The index is disposable and rebuildable; no lock-in.
- **For ~10k nodes with a side-door finder, a Postgres server and a full BM25 + dense + RRF hybrid are premature.** The decision narrows to in-memory derived graph vs embedded store.
- **SQLite is lower-regret than in-memory** because it is robust to the unresolved robot-lifecycle question (works whether the robot is a persistent server or a per-call process), and the S6 serializing-ID-gate requirement maps for free onto a SQLite single-writer transaction.
- **"Embedded index" is not "embedding / vector."** Adopting SQLite commits nothing to dense retrieval; FTS5 supplies the keyword/BM25 finder now, and sqlite-vec is a reserved empty slot. The embedding deferral and the substrate choice are decoupled.
- **The fold is not full-rebuild-vs-incremental.** Incremental upsert at the write gate is the hot path — forced by the event-triggered write path and the S8 migration burst, not by rebuild slowness. Full rebuild is the cold reconcile/recovery path, triggered by a cheap divergence check, not a blind schedule.
- **FTS5's ranking function is BM25** — the sparse half of the preparation notes' proposed hybrid is available for free, in-process. Only the dense half + RRF fusion is deferred. The residual paraphrase-miss is the measured trigger (S4 trace WRONG-ENTRY / ABSENT rates) for adding embeddings.
- **Measurement was mis-framed.** Ragas/TruLens are generation-eval frameworks; of their three classic metrics only Context Relevance maps to a deterministic retriever. Groundedness and Answer Relevance are agent-layer concerns, out of scope. Using an LLM-judge framework to measure a zero-token deterministic robot is self-defeating (W1).
- **The only fuzzy component is the finder;** the deterministic paths are correct-by-construction — unit-test territory, not metric territory.

# Breakdown — the five clusters

## Cluster 1 — Substrate decision (resolves the contradiction)

- **Markdown** (ADR frontmatter + body, stable IDs, links) = source of truth; **index** = derived, disposable, rebuildable projection.
- **Engine = embedded SQLite** (FTS5 + recursive CTE + a reserved sqlite-vec slot). Single file beside the markdown repo, gitignored, owned by the robot process. No server.
- **Discarded for now (documented upgrade path):** Postgres + pgvector (a server = a W3 cost; premature at 10k); the full BM25 + dense + RRF hybrid; a custom DB engine. Neo4j already discarded (S1).
- **In-memory derived graph considered and set aside:** viable only if the robot is persistent; SQLite is robust to that open question and gives trace/embedding persistence, inspectability, and incremental fold for near-zero added cost.

## Cluster 2 — The fold (markdown to index)

- **Hot path: incremental upsert at the serializing gate.** The delta = the new node + recomputed derived status of its edge-neighbors (active-status from `supersedes`, flag-status from `resolves`). Bounded and event-local.
- **Cold path: full rebuild = reconcile / recovery,** triggered by a cheap divergence check (count + content-hash, markdown vs index), at boot and/or periodically — not a blind schedule.
- **Crash consistency:** markdown written first (truth), index upserted second; a crash leaves the index behind truth, which the reconcile rebuild fixes. Index disposability is what makes incremental safe.

## Cluster 3 — Serializing gate (physical realization of the S6 gate)

- **The single-writer ingest-robot IS the gate:** all writes funnel through one robot processed sequentially; write concurrency is low (proposals go to the antechamber; ingest is Senate-gated).
- **The SQLite write transaction** is the atomicity/durability primitive for the index upsert and a backstop against an accidental second writer — not the primary serializer.
- **Order in the critical section:** allocate ID → write markdown (outside the DB transaction, to avoid holding a DB lock over filesystem I/O) → upsert index (in the transaction).
- **ID authority:** monotonic counter; canonical source is the markdown (max+1 on rebuild), cached in the index for O(1) allocation. IDs are unique, not gapless — a crash-skipped ID is acceptable.
- **Reads are lock-free and concurrent during writes** (SQLite WAL).
- **Upgrade path:** multiple concurrent writers would require an explicit serialization primitive (BEGIN IMMEDIATE / advisory lock) — not now.

## Cluster 4 — Retrieval engine & the finder side-door

- **Primary path:** deterministic scope + kind filter (SQL WHERE) + bounded edge traversal (adjacency walk / recursive CTE) — correct-by-construction, no finder involved.
- **Finder side-door:** FTS5 keyword/BM25 search over title + body, ranked top-N — used only when the agent cannot name the scope. This is the only fuzzy component.
- **Embeddings deferred:** no vector values on nodes now; sqlite-vec is a reserved empty slot. Backfill later = a re-fold (an embed pass over all nodes), not a migration; only the finder feed changes (keyword → hybrid via RRF). The methodology (two-phase, verdict vocabulary, scope filter) is invariant.
- **Agent-to-robot interface (instantiates the S4 contract):**
    - **open_scope(scope, kind?)** — skeleton candidate rows (id + title + kind + scope, no body); primary deterministic feed; faceting on overflow.
    - **find(text, kind?, scope?, top_n)** — the finder side-door; ranked skeleton (FTS5 now).
    - **fetch(ids[])** — bodies + edges (TOC rows) for explicitly selected IDs; phase 2.
    - **traverse(id, edge_type, depth?)** — bounded edge follow; serves INSUFFICIENT-TRAVERSE.
    - Intent-before / verdict-after per round; budget dials cap rounds and body-fetch.

## Cluster 5 — Measurement

- **Reframe: IR-retrieval-eval, not RAG-answer-eval.** Of the three classic metrics, only **Context Relevance** (= precision/recall of the returned node set) maps. Groundedness and Answer Relevance are agent-layer (faithfulness of a generated answer), out of S7 scope.
- **Target = the finder** (the only fuzzy component). Deterministic paths are correct-by-construction → unit tests, not metrics.
- **Two tiers:** (1) free continuous proxy = the S4 trace (WRONG-ENTRY / ABSENT rates with intent text) — also the embedding trigger; (2) offline ground truth = a golden query set (query → expected node IDs), giving precision/recall@k on the finder and validating the proxy.
- **Tooling: a home-grown lightweight IR harness,** not Ragas/TruLens — their LLM-judge machinery burns tokens (W1-hostile) or duplicates the trace (TruLens). Ragas's context_precision/recall are a naming reference only. An LLM-judge framework is deferred to the agent-answer-groundedness layer (not S7).
- **Golden set is a maintained, versioned artifact** validated against the warehouse (expected IDs must still exist and be active); measurement runs offline, off the hot path → parked measurement lane / retro.

# Recommendations

- **Resolves the markdown-vs-DB contradiction.** Folded into the parent direction table: row **A** (knowledge form — storage realization: markdown truth + derived SQLite index), row **C** (retrieval — substrate + FTS5 finder + embedding deferral with a measured trigger), row **H** (build vs buy — embedded SQLite, own / no-server, Postgres as documented upgrade path).
- **Fixed inputs for Session 8 (migration):** markdown as the ingest target (truth); incremental upsert at the gate (migration = N cheap upserts + one final reconcile); the agent-to-robot interface; the IR measurement harness as the migration-quality check.
- **Open item carried, not blocking:** the robot process lifecycle (persistent vs per-call). SQLite is robust to it; pin during SPQR-runtime implementation.
- **SPQR not-now tasks:** implement the ingest-robot + gate; build the golden-set IR harness; schedule the periodic reconcile divergence check.

# Descoped

- Migration / chunking / atomic-splitting — Session 8.
- Embedding / dense finder implementation and RRF fusion — deferred behind the measured trigger.
- Agent-answer groundedness measurement and any LLM-judge framework — agent layer, not S7.
- Robot process lifecycle and SPQR-side implementation — SPQR runtime work.
- Multi-writer concurrency primitive — documented upgrade path, not now.

# References

- Session 3: Node Schema & Graph Ontology (universal node + 3 kinds, edge ontology, append-only, derived status)
- Session 4: Query Interface Contract (two-phase contract, verdict vocabulary, finder side-door, archetype policy, trace)
- Session 6: Write Path, Antechamber & Audit (serializing ID gate + audit plane — physical realization descoped here)
- Session Roadmap: Open-Question Map & Critical Decisions (S7 scope; the markdown-vs-DB contradiction; fold-back-per-session rule)
- Separate preparation for warehouse (the DB-substrate assumption this session reconciles)
- Parent checkpoint — Direction Checkpoint PoC (direction table rows A / C / H — folded back)
- SPQR AGENT_LAWS — Law 3 (the external record is truth)