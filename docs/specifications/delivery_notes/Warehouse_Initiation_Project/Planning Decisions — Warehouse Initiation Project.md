## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Warehouse Initiation Project — decision record (planning session + amendments)

**Document status:** Active — authoritative decision record. Original decisions are append-only; changes arrive as dated amendments at the end. Do not re-litigate closed items; do amend them when the owner reopens one.

**Date:** 2026-06-12 (planning session); amendments dated individually

**Purpose:** Single decision record for the warehouse build (B1–B5), import, and surrounding process. Consumes the Pre-Build Decision List Groups 1 and 2. Replaces "Planning Session Output — Pre-Build Decisions" (deleted 2026-06-12; all content carried forward here).

---

# Original planning session decisions (2026-06-12)

## Group 1 — Warehouse core build decisions (closed)

### G1 — Robot process lifecycle
**Decision:** Per-call CLI process.
**Rationale:** Simpler, no daemon management, crash-safe by construction (state lives in markdown + SQLite, never in the process). Latency argument for a persistent server is irrelevant at <100 node migration volume. Matches the single-writer gate model.

### G2 — Agent-to-robot binding
**Decision:** CLI first; MCP wrapper only if a concrete need arises.
**Rationale:** CLI is callable from any runtime, no extra infrastructure, consistent with G1 per-call. The S4 contract is the stable seam — the binding is swappable. No overengineering for a second deployment that doesn't exist yet.

### G3 — Robot write/commit policy
**Decision:** Robot writes files, never runs `git commit` / `git push`. Owner batch-commits at checkpoints (after each ingest batch or migration phase).
**Rationale:** Consistent with the standing owner rule. The unversioned window is acceptable — markdown + SQLite are already crash-consistent (S7), and the warehouse is in test-run regime. Git history is audit trail, not real-time protection.

### G6 — Antechamber physical store
**Decision:** Markdown directory, physically outside the warehouse directory.
**Rationale:** The SQLite index is disposable by design — proposals are not (they are un-ingested work) and must survive an index rebuild. Physical separation reinforces the boundary between pending and canonical content. *Concretized by A3.*

### G8 — Archetype identity for query-policy enforcement
**Decision:** Self-declared `--archetype` parameter, logged in the intent/verdict trace.
**Rationale:** A per-agent key/token would require infrastructure disproportionate to v1. Self-declaration with trace logging means a bypass is visible in retro even if not prevented. Upgrade to enforced identity only if the trace shows violations.

## Group 2 — v1.5 SPQR cutover decisions (relevant items closed)

### G7 + G4 — Wake/escalation mechanics + continuation-grant
**Decision:** Antechamber is the queue. Every Senate session-starter includes a check for pending warehouse items. Senate-pending items surface to the owner at session start. Owner issues continuation grants in-session (one-shot, consumed by the robot on the next round). Zero infrastructure, daemon-free.
**Rationale:** In the owner-driven setup there is no orchestration — the owner controls all session starts. Antechamber-as-queue + session-starter-as-trigger is deterministic, Law 3 compliant, and requires nothing beyond what already exists.

### G5 — Scope-vocabulary governance
**Decision:** New scope values require owner approval. During migration or hot-path, if an agent cannot fit content into the existing vocabulary, it flags the case to the Senate; the owner makes the final call.
**Rationale:** Scope is schema-adjacent — free minting fragments the deterministic filter. Governance is lightweight: flag → owner decides.

## Deferred in the original session

- **G9 — Ticket→session-id map:** ticket reference is sufficient; session-id pulled from an external source when needed. Not a build blocker.
- **G10 — Seed vs local packaging:** originally "deferred until a second project requires it; build for Foodoire now." *Superseded by A1 + A2 below.*

---

# Amendments

## A1 — Build location: generic-first (2026-06-12)

**Decision:** The warehouse robot, DDL, and test suite are built and proven in the **generic SPQR repo** — the seed's natural home. Foodoire receives the proven package via import (Phase 1.5). Per-project warehouses are the standing plan: a Foodoire instance now, the generic seed maintained as the source.
**Supersedes:** the original session's "build for Foodoire now" framing (G10 note) and the earlier owner working plan (Foodoire-first, lift later).
**Rationale:** The robot is project-agnostic by design — building it in the generic repo means no later extraction, the import step exercises the G10 mechanism with fresh knowledge, and the Foodoire repo stays free of framework build noise (the lesson of the milestone-0 worktree era). Nothing in B1–B5 needs Foodoire-specific content; the first project-specific phase is migration, which runs after import anyway.

## A2 — G10 closed: import mechanism v1 = plain copy (2026-06-12)

**Decision:** A project consumes the robot by **plain copy** at import (matching existing SPQR template practice). `schema_version` stamped per node; a future schema bump ships as a re-fold transform script in the seed. Submodules rejected (git complexity the owner workflow doesn't want).
**Status change:** G10 is no longer deferred — the import to Foodoire is a named phase (1.5) of this project.

## A3 — Physical layout: `project_memory/` parent (2026-06-12)

**Decision:** In a consuming project, the warehouse lives under a single parent directory with the antechamber as a sibling:

```
project_memory/
├── warehouse/      ← canonical content (markdown truth) + derived SQLite index (gitignored)
└── antechamber/    ← pending proposals (markdown)
```

**Relation to G6:** this is a concretization, not a change — the antechamber stays physically outside the warehouse directory; the shared parent keeps the repo root clean.

## A4 — Test isolation: directory-level, not git-level (2026-06-12)

**Decision:**
- **Fixtures are versioned** test assets living next to the robot code (10–15 hand-made sample nodes + the query set). They are synthetic, project-neutral content — the robot's regression suite, and they travel with the robot at import. The golden query set (parked lane) grows out of them.
- **Every test run builds a disposable warehouse instance** in a gitignored/tmp directory (enabled by the robot's warehouse-root parameter, a B1 requirement), asserts against it, and deletes it.
- **No test branches.** Rejected because branch switching does not reset untracked/ignored files — the derived SQLite index would leak across branches, which is exactly the state a test must isolate. Branches also reintroduce accidental-merge risk and parallel-checkout pressure.
- **The canonical warehouse stays empty until Phase 2 migration.** No test content ever enters it or git history.

## A5 — Git working mode for the project (2026-06-12)

**Decision:** Development happens on `main` of the respective repo (generic for Phase 1, Foodoire from Phase 1.5). Owner batch-commits at checkpoints (G3 upheld). No worktrees and no long-lived branches while a single line of work is active. The full branching-methodology redesign is deferred to the post-warehouse batch (v1.5.1, git-process formalization remainder).
**Context:** the milestone-0-foundation worktree was merged back to Foodoire `main` (fast-forward, linear history) and dismantled on 2026-06-12; framework changes riding app milestone branches is the anti-pattern this rule prevents.

## A6 — Documentation home (2026-06-12)

**Decision:** `docs/specifications/delivery_notes/Warehouse_Initiation_Project/` (generic SPQR repo) is the documentation home for this project. Build sessions document their outputs here. This closes the "documentation home decision" item the schedule had folded into planning session 1.1 but the original output never recorded.

## A7 — Clean baseline achieved (2026-06-12)

**Status:** The "clean baseline before warehouse code hits the repo" constraint is satisfied: Foodoire DEV-001–003 cycle closed and merged to `main`, casing fix applied (`Docs/` → `docs/`), `.obsidian` untracked and gitignored, worktree removed, branch deleted both locally and on origin.

## A8 — Phase 1 exit criterion: byte-identity defined as a two-part check (2026-06-13)

**Decision:** The Execution Plan's Phase 1 exit criterion "reconcile rebuild reproduces the index byte-identically" is defined as a **two-part check**:

1. **Rebuild determinism (byte-level):** two reconcile rebuilds from the same markdown tree (and the same carried-over state, see below) produce **byte-identical** index files. This is the hard byte criterion.
2. **Live-vs-rebuild equivalence (logical digest):** the live, incrementally-built index and a fresh reconcile rebuild are compared via a **canonical logical digest** — an ordered dump-hash of the derived tables (`nodes`, `edges`, FTS content, `id_counter`, `meta`). Byte comparison between them is not required and not meaningful.

**Why a literal whole-file byte comparison is impossible:** the live index legitimately contains state that is not derived from warehouse markdown (trace rows, the antechamber mirror), `meta.created_at` is a creation-time value, and SQLite page layout depends on insertion order — an incrementally-built file can never be byte-identical to a freshly rebuilt one.

**Carry-over rule:** on reconcile rebuild, `trace` and `antechamber` rows are carried over verbatim from the previous index in deterministic order — they are not derivable from warehouse markdown (the trace is the S7 measurement proxy; the antechamber mirror's re-derivation is B4's concern). If the index file itself is lost, the trace is lost with it — an accepted cost of the S7 "disposable index" principle.

**Environmental constraint:** byte-identity is only guaranteed within one SQLite build (page format, FTS5 version). The exit-check byte comparison must run with the same Python/SQLite build that produced the indexes.

**Origin:** surfaced as a contradiction during B2 planning (B1 delivery note open question #4 anticipated the WAL part); owner-approved 2026-06-13.

---

# References

- Execution Plan — Warehouse Initiation Project (this folder) — the plan these decisions govern
- Pre-Build Decision List (PoC requirements folder) — problem framings and origins of G1–G12
- Sessions 3–8 (PoC requirements folder) — the fixed architecture
- SPQR AGENT_LAWS — Law 3 (external record is truth), Law 4 (independence)
