---

---
## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — one-time migration of existing project knowledge into the warehouse

**Document status:** Draft — pending owner review

**Phase:** PoC — Session 8 (consumes all of S3–S7; the execution-planning capstone of the warehouse arc)

**Date:** 2026-06-10

**Usage:** claude-opus-4-8:  10.1k input, 40.3k output, 1.1m cache read, 85.5k cache write ($2.16)

**Session scope:** The migration runbook — triage, extraction, backfill, batch-review, prose-pruning. The proposal-JSON ingestion format. Nothing about substrate (S7), the write-path mechanism (S6), or SPQR-side implementation of the migration agent.

**Purpose:** Fix how existing project knowledge enters the warehouse on a fixed S3–S7 foundation, and resolve the migration-time gaps S6 left open (gating cost, proposal format, inherited-knowledge surfacing).

**Status legend:** decided · leaning · mixed · open

---

# Overview

Session 8 plans the one-time migration of existing project knowledge into the warehouse. The central reframe: migration is **the normal S6 write path run in bulk** (N cheap incremental upserts + one final S7 reconcile), not a special pipeline. Two facts shape the whole design. First, the corpus is **tiny** — the entire project knowledge set is ~830 lines — so the volume/LLM-limit concerns that motivated page-chunking do not exist here; the 10k-node figure is the steady-state ceiling, not the migration volume. Second, the existing documentation is **already incomplete and mixed**: it interleaves committed decisions, exploratory spike/spec material, and prose restatements. Migration therefore splits into faithful **extraction** of what exists and owner-led **backfill** of what was decided but never written, kept as two distinct provenance classes. The warehouse becomes the single canonical knowledge base; the prose docs are pruned to thin orientation only — but pruning happens last, after the warehouse is verified, so the source is never deleted before capture is confirmed.

# Findings

- **Migration is a bulk run of the normal write path, not a separate mechanism.** S7 already fixed this (migration = N upserts + one reconcile). Everything reuses the S6 robot gate and the S3 append-only machinery; no new ingestion mechanism is introduced.
- **The corpus is tiny, so chunking is trivial.** [CLAUDE.md](http://claude.md/) 104 lines, ARCHITECTURE 17, DATA_MODEL 231, CONVENTIONS 277, LESSONS 18 (313 words, dense), decisions/ = 22 ADRs / 183 lines total. Nothing approaches an LLM context limit; the original 2–3-page cap solved a scale problem that does not exist here. File-granular chunking is correct; a deterministic pre-splitter was considered and rejected.
- **decisions/ is already atomized — the work there is review and selection, not splitting.** One ADR ≈ one atomic decision; the migration job is "which do we still need", with occasional 1-file→2-node (decision + constraint) or 1-file→0-node (stale) cases.
- **The migration gating cost is a gap S6 left open, and per-node Senate would be W1-hostile.** S6 starts everything un-promoted (auto-ingest empty) → naively every migrated node would cost an Opus call. Resolution: a **migration bootstrap-gate** = owner batch semantic review, mirroring S6 Cluster B's owner-driven semantic audit. This fills a gap; it is not a deviation from S6.
- **The proposal-JSON format S6 referenced but never defined is pinned here.** It doubles as the normal hot-path ingestion format, so defining it for migration defines the proposer contract for the whole system.
- **"Inherited / never-explicitly-decided knowledge" is handled by the backfill class, not by importing external docs.** The warehouse captures the project's *adoption decision* (e.g. "we follow Apple HIG"), linked to an external ref — not a mirror of the external material. Migration surfaces the gap; the owner mints the backfill node.
- **The warehouse ingests at commitment, not exploration.** Spike/Consilium preparation is not fixed → it stays in process artifacts; a decision written into a dev ticket is fixed-as-intent → it enters, even before code exists; code is downstream realization. "Written into a dev ticket" is the operational proxy for "fixed", consistent with S3's "spec excluded as source-of-intent".
- **Dedup is a rule at this scale, not a mechanism.** The realistic duplicate is a prose restatement of an ADR; the ADR is canonical and the restatement is dropped. The FTS5 pre-check flags suspected dups (append-only → flag, never block); batch review resolves.

# Breakdown — the five phases

## Phase 0 — Triage

- **Inventory the source set on two axes.** Relevance (keep / stale) and maturity (**committed** → migrate or backfill; **exploratory / pre-commitment** → stays in process, owner-led).
- **Scope line:** only project knowledge migrates — [CLAUDE.md](http://claude.md/), [ARCHITECTURE.md](http://architecture.md/), DATA_[MODEL.md](http://model.md/), [CONVENTIONS.md](http://conventions.md/), [LESSONS.md](http://lessons.md/), decisions/. The SPQR-process artifacts (Docs/agents/, Docs/skills/, Docs/retro/) are **out of scope** for the project-warehouse — they belong to a separate SPQR-warehouse.
- **Owner-led classification** for spec/spike-origin content: the owner drives the committed-vs-exploratory call.
- **Output:** the migration source set + the backfill candidate list.

## Phase 1 — Extraction (migration proper)

- **File-granular chunks.** Each file = one read pass; CONVENTIONS H2-split only as a quality fallback. decisions/ = one pass, output reviewed ADR-by-ADR.
- **One chunk → N atomic node proposals** (S3 atomic-assertion principle), origin `migration`, faithful to the source text.
- **Two-pass run.** Pass 1: mint all nodes with no edges, building the `temp_ref → food-nNN` map. Pass 2: resolve `proposed_edges` against the full map + existing warehouse. `supersedes` edges → batch review (rare at migration: the warehouse starts empty); all other edge types resolve robot-auto.
- **Strict structured output**, schema-validated by the S6 robot hard-gate; malformed → re-prompt that chunk. Resumable via antechamber checkpoint (Law 3).

## Phase 2 — Backfill

- **Owner-led authoring** of decisions that were committed (in the 3 dev tickets) but never written, origin `backfill`. This is the mechanism that surfaces inherited / never-explicitly-decided knowledge.
- **Parallel, not gated on completeness.** Append-only means backfill nodes can be added during or after Phase 1, attaching edges to already-ingested nodes — no "complete final list" is required before ingestion starts.

## Phase 3 — Batch-review + reconcile

- **The migration bootstrap-gate:** owner batch semantic review (not per-node Senate), resolving `supersedes` and flagged duplicates.
- **Final S7 reconcile** (cold-path full rebuild + divergence check) confirms markdown↔index consistency.
- **Output:** a verified canonical warehouse.

## Phase 4 — Prose-pruning (make the warehouse canonical)

- **Destructive, and strictly last** — only after Phase 3 verification, so the source is never removed before capture is confirmed.
- **Invariant:** no canonical decision content is duplicated in prose. [CLAUDE.md](http://claude.md/) keeps a thin orientation / bootstrap section (how to query the warehouse, project shape at a glance); the how-to bulk lives in agents/skills. Decision content becomes a pointer or a generated projection, never a hand-maintained copy.
- **Effect:** kills the W2 drift source and removes the prose-doc maintenance burden.

## The proposal-JSON schema (pinned)

Doubles as the normal hot-path ingestion format. Fields:

- **temp_ref** — batch-local reference (e.g. `$1`) so Phase-1 edges resolve before the real `food-nNN` ID is allocated at the gate.
- **kind** — decision / constraint / lesson (S3).
- **scope** — S5 taxonomy.
- **title** · **body** — body = the single atomic assertion.
- **proposed_edges[]** — `{type, target}`; target = a `food-nNN` ID or a `temp_ref`.
- **schema_version** — stamped per node; `v1` at migration. A later schema change is a re-fold transform (like the S7 embedding backfill), not a re-migration.
- **provenance** — `origin` (migration | backfill) · `source_doc` + `source_loc` (required for migration; the audit + inherited-knowledge anchor) · `agent` · `authored_by` (backfill) · `ticket` (backfill, when one exists; otherwise owner extracts later).

## Proposer contract (S8-owned) vs the skill file (SPQR-not-now)

- **S8 owns the contract:** what a proposer must know to emit a valid proposal — the schema (machine-validated by the robot gate) plus the authoring guidance (what "atomic" means, how to pick kind/scope, when to propose an edge).
- **The "warehouse-ingest skill" file** (machine-first + negative constraints) is written during SPQR implementation. It is reused by all hot-path proposers — not migration-specific — so the contract defined here is the system-wide proposer contract.

# Recommendations

- **Fold-back (light).** Session 8 is the execution-planning capstone; it flips no parent direction-table row to a new decision. It does pin two items the prior sessions left implicit: the **proposal-JSON ingestion format** (a retroactive S6 detail) and the **migration bootstrap-gate** (an owner-batch extension of the S6 gate model). It also gives the S3-deferred inherited-knowledge boundary a concrete migration-time mechanism (the backfill class + the commitment principle).
- **Run the phases in order P0 → P4;** Phase 2 backfill may overlap Phase 1; Phase 4 is strictly last.
- **Owner-led where flagged:** the committed-vs-exploratory triage, the backfill authoring, and the batch semantic review are judgment acts the owner performs; this session fixes the mechanism.
- **SPQR not-now tasks (carry into the SPQR update):** implement the migration agent + two-pass runner; write the warehouse-ingest skill (the proposer contract realized); execute P0–P4 against milestone-0-foundation; stand up the FTS5 dup pre-check feed.

# Descoped

- SPQR-process knowledge (agents / skills / retro) — a separate SPQR-warehouse, not this migration.
- The write-path mechanism, the audit plane, the substrate — fixed by S6/S7; consumed here, not redesigned.
- Embedding / dense finder — deferred behind the S7 measured trigger; irrelevant to migration.
- Steady-state scale handling (toward 10k nodes) — not a migration concern; the migration corpus is ~830 lines.
- SPQR-side implementation of the migration agent and the ingest skill file — separate SPQR update.

# References

- Session 3: Node Schema & Graph Ontology (universal node + 3 kinds, edges, append-only, derived status, atomic-assertion principle, the deferred inherited-knowledge boundary)
- Session 4: Query Interface Contract (the FTS5 finder side-door used for the dup pre-check; the agent-to-robot interface)
- Session 5: Knowledge Base Restructuring (per-file target structure; the project-vs-SPQR-process split that sets the scope line)
- Session 6: Write Path, Antechamber & Audit (the robot gate + Senate model this migration runs in bulk; the proposal format referenced and now pinned; the owner-driven semantic audit the bootstrap-gate mirrors)
- Session 7: Storage Substrate & Retrieval Runtime (migration = N upserts + one reconcile; markdown as ingest target; the IR harness as the migration-quality check)
- Session Roadmap: Open-Question Map & Critical Decisions (S8 scope; the fold-back-per-session rule)
- SPQR AGENT_LAWS — Law 3 (the external record is truth)