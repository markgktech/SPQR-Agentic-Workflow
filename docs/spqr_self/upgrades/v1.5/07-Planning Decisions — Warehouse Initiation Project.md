---
up: "[[v1.5]]"
group: "Warehouse Initiation — spec & decisions"
order: 7/8
saw: [SAW-30]
type: decision
poc: ["[[Knowledge Architecture — Pre-Build Decision List (Planning Session Input)]]", "[[Knowledge Architecture & Token Optimization — Direction Checkpoint PoC]]"]
tags: [group, warehouse]
---

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

**Decision:** `docs/spqr_self/upgrades/v1.5/` (generic SPQR repo) is the documentation home for this project. Build sessions document their outputs here. This closes the "documentation home decision" item the schedule had folded into planning session 1.1 but the original output never recorded.

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

## A9 — Execution model for B4/B5: Starter A governs, augment-not-replace (2026-06-20)

**Decision:** B4 and B5 are each built in their own session under the **Starter A** model (plan-first → surface every contradiction → owner approval gate → execution). This **augments, does not replace** the B1–B3 discipline (dependency gate, A4 test isolation, delivery note, DoD). The master owns the hand-off (fills/derives the starter, attaches the dependency-gate evidence) and the critical re-test (A10). One ticket = one session.
**Rationale:** B4 carries genuine unresolved design questions (A15) that only surface if the plan phase exists; the brief-only model would force the agent to guess. Resolves roundtable R1.
**Affected:** `07-Session Starters — Build Tickets & Exit Check` (governance header), B4/B5 sessions.

## A10 — Verification loop: three distinct layers (2026-06-20)

**Decision:** (1) **execution-agent tests** in the suite; (2) **master critical re-test** — a bounded re-run of the just-built ticket's suite **plus a cross-B integration seam** (e.g. B4 allocates an id → B2 fold sees it → B3 query reads it → B5 audit flags a broken case), run immediately after each build session, before the next dependent ticket; (3) **independent Probator exit check** — the whole Phase-1 vertical slice in a fresh session that built none of B1–B5, which asserts its own session id differs from every delivery note's and that the Python + SQLite versions match the recorded receipt (A11).
**Rationale:** the dependency gate trusted the GREEN token while B2 shipped a flaky GREEN; layers (2) and (3) must be distinct (bounded-per-ticket vs whole-slice-fresh) or they collapse/duplicate. Resolves R3-exit, R4, R11; this is the owner's "master critically re-tests" ask made concrete.
**Affected:** `07-Session Starters` (Starter A close + Starter B), delivery-note DoD.

## A11 — Test evidence / DoD additions (2026-06-20)

**Decision:** every build/test claim in a delivery note carries a **verbatim `receipt:`** field — the decisive tool stdout line (`Ran N tests … OK`), never a paraphrase; the full suite is run **≥5× consecutively** at close and the clean-run count is cited; the **SQLite version** (`sqlite3.sqlite_version`) is recorded alongside the Python version. **Lint is out of scope** for the warehouse build (test-only); a `ruff` step is an optional later polish, not required.
**Rationale:** B3 §4 paraphrased ("171 tests") which the SAW-26 receipt rule forbids; the anti-flake repeat-run was de-facto convention but absent from the DoD; the exit-check needs the SQLite version to distinguish an environment mismatch (A8) from a real determinism failure. Resolves R5, R10, R11, M5.
**Affected:** delivery-note DoD §4, exit-check report.

## A12 — Test isolation hardening (2026-06-20)

**Decision:** a disposable test instance is the **warehouse root and its antechamber sibling** under one system-tmp parent, created and deleted together; the instance `.gitignore` must cover **node and antechamber markdown**, not only the derived index; the exit-check negative check must include the **antechamber directory**, not just `project_memory/warehouse/`.
**Rationale:** B4 writes node + antechamber files; the current instance `.gitignore` covers only `index.sqlite*`, so an in-repo instance could leak markdown into git. Resolves R12, G6/G7; the concrete form of the owner's "test data stays test data".
**Affected:** `warehouse_robot/cli.py` (`INSTANCE_GITIGNORE`), Planning Decisions A4 (concretised), exit-check negative check.

## A13 — Canonical antechamber is versioned, not gitignored (2026-06-20)

**Decision:** the **canonical** antechamber (`project_memory/antechamber/`) holding pending proposals is **committed (versioned)** — it is un-ingested work and truth (G6), and must survive an index rebuild and a machine loss. This is distinct from the derived index, which **is** gitignored, and from a **disposable test** antechamber, which lives in system-tmp (A12).
**Rationale:** proposals are not derivable from warehouse markdown; gitignoring them would silently risk losing un-ingested work. Resolves M3.
**Affected:** Foodoire `.gitignore` at first instantiation (Phase 1.5), the import package layout.

## A14 — B5 tripwire rule shapes + placeholder calibration (2026-06-20)

**Decision:** B5's three tripwires are defined as **measurable predicates**, numeric parts as **placeholder dials** calibrated later from real data (B3 precedent):
- **orphan** = a *knowledge* node (kind decision/constraint/lesson) with **0 inbound AND 0 outbound** edges, **excluding** origin-flagged foundational nodes;
- **relates-to overuse** = a node carrying **> K** `relates-to` edges, **K = 5 (placeholder)**, retro-calibrated;
- **missing-recommended-edge** = a node lacking an edge its kind is expected to carry, per a **per-kind recommended-edge table seeded from Session 3** — initially the single architecture-stated rule **`lesson → about`** (strongly recommended); the table grows by governance (no invented rules).
B5 stays **purely graph-structural**; code/convention freshness (SAW-40) is explicitly **NOT** a B5 tripwire (that is the owner-driven semantic audit, Session 6 Cluster B).
**Rationale:** the tripwires were named in 5 docs and defined in none; a stateless B5 agent would invent thresholds (noise). The `flag` kind is the audit plane, not a knowledge kind. Resolves R2 (G15/L1) and the L7 scope-creep guard.
**Affected:** B5 brief, `warehouse_robot/` audit module, fixture set (A16).

## A15 — B4 design positions (ratified in the B4 plan phase) (2026-06-20)

**Decision:** the master records these positions; the B4 plan phase (A9) confirms them against the code and surfaces any contradiction:
- **ID allocation** from `id_counter` via the gate transaction (`UPDATE … RETURNING`), never from markdown-max; the fold's `max()` guard keeps the re-touch idempotent (B3 open-Q#2);
- **retire** = a **new superseding node** (append-only store refuses in-place mutation; explicit `retired` is for born-retired/inherited content) (B3 open-Q#4);
- a proposal **binds self-declared `ticket`+`agent`, logged** (G8 posture, abuse trace-visible);
- **antechamber↔mirror reconcile + divergence** — B4 **builds it OR defers-with-reason** (call made in the B4 plan; the exit-check must re-derive the mirror from the antechamber dir regardless — L4/R3);
- **`auto-ingested` state** — B4 builds it reachable-but-empty OR defers the promotion gate (call in the B4 plan; the exit-check catches any DDL-admitted dead path — L6/R9);
- if B4 changes the schema, **bump `schema_version`** and carry it in fold/reconcile (M4).
**Rationale:** these are real seams a fresh agent could get wrong; recording the position prevents guessing while the plan phase keeps the final call owner-gated. Resolves R6, M4.
**Affected:** B4 brief, `warehouse_robot/` write-gate module, schema.

## A16 — Fixture-set growth for B4/B5 (A4-governed) (2026-06-20)

**Decision:** B4 and B5 extend the **versioned, synthetic, project-neutral** fixture set: malformed proposals (schema rejection), a proposal walked through the full state machine, and deliberately-broken nodes (orphan, missing-recommended-edge) for B5. New fixtures are test assets only — they ride with the robot but only ever fold into disposable instances (A4).
**Rationale:** the existing 14 nodes + 26 queries are read-path fixtures; B4/B5 cannot be tested without write/audit fixtures. Resolves M1.
**Affected:** `warehouse_robot/fixtures/`.

## A17 — End-to-end test layering (2026-06-20)

**Decision:** **this run (generic):** an automated **vertical-slice scenario** (L1 — one node threaded fold→query→propose→gate→ingest→audit→reconcile, asserting at each hop + final graph digest) **plus at least one subprocess CLI agent-session** (L2 — `python3 -m warehouse_robot …` driven as a real process through a realistic session incl. the intent/verdict bracket, a budget exhaustion → grant → resume). **Later, in Foodoire (owner-run, post-migration):** the **system e2e** (L3 — a real SPQR agent running a real ticket against the migrated warehouse) = Execution Plan Phase 2–4.
**Rationale:** the only e2e in the plan was the manual one-shot exit check; the CLI contract (JSON/exit codes) is exactly what breaks silently and is painful to debug in Foodoire. L1/L2 prove the mechanism before it ships; L3 proves the process with real data. Resolves the e2e discussion.
**Affected:** `warehouse_robot/tests/` (new scenario + subprocess tests), exit-check, Execution Plan Phase 2–4.

## A18 — Cross-phase sequencing & deferrals (2026-06-20)

**Decision:**
- **Roadmap order (amends the Execution Plan):** B4+B5 → **SAW-31** (SPQR agents/skills made warehouse-aware, generic side) → **propagation** (robot + warehouse-aware agents in one snapshot) → **migration/ingest** in Foodoire → **test (L3)** → cutover decision. SAW-31 runs **before** propagation so the warehouse-aware agents propagate **once** (not old-then-new).
- **Migration mints only via the B4 gate** (no hand-minted artifacts, S7) — so **B4 quality gates the entire migration**.
- **Flat docs are not deleted** (LLM-extractable safety net; reset = re-extract); the flat-doc **prune (S8 P4) is deferred to the Phase 5 cutover decision**, after the Foodoire test passes — agents gain warehouse capability in SAW-31 but flat docs stay the authoritative fallback through the test-run regime.
- **Named deferrals:** write-path telemetry / proposal-event log (→ SAW-31/SAW-40 hook) and `kind` extensibility governance (→ SAW-40; `kind` documented as a deliberate frozen enum, a new kind is a seed-level schema bump per A2) — deferred, not silent.
**Rationale:** propagating once avoids double work; keeping flat docs preserves the reset path the whole test-run regime depends on. Resolves the roadmap discussion, R7, R8, M2.
**Affected:** Execution Plan (Phases 1.5–5 ordering note), SAW-31, propagation manifest.

## A19 — B4 execution refinements + master verification (2026-06-20)

**Decision:** three refinements surfaced and owner-approved during B4 execution (Starter A plan phase + close):
- **A12 scoping (from D6):** the broad instance `.gitignore` (node + antechamber markdown) is **TEST-scoped only** — written by `init --disposable` into a system-tmp instance. The **canonical** `init` stays **index-only** so the committed antechamber (A13) is never gitignored. A12's "instance .gitignore must cover node+antechamber" applies to disposable test instances, not the canonical layout.
- **A15 ID primitive (from D9):** allocation is `SELECT … then UPDATE id_counter` inside one gate transaction — **not** the literal `UPDATE … RETURNING` (which needs SQLite ≥3.35, above the stdlib floor). Identical semantics under the single-writer serialized gate; A15's intent was atomic allocation from the counter, not the specific syntax.
- **D13 reversed (owner-accepted):** `antechamber_root` is **NOT persisted** in the manifest. The default antechamber equals the A3 sibling (derivable from `warehouse_root.parent`), so persistence was dead weight and would break the manifest's strict-key contract. Reversible in one amendment if a non-sibling antechamber is ever needed (no current case).

**Master A10 critical re-test — PASS (independent):** full suite 215/215 green, 3× consecutive from the repo root (Python 3.9.6 / SQLite 3.51.0); R3/L4 closed in code (`reconcile_antechamber` + `AntechamberDivergenceReport`, the B2-analogue); L1 cross-B vertical slice + L2 real-`subprocess` session present and green; D6 verified (canonical init index-only); no git leakage. No new gaps → no roundtable.
**Rationale:** record the execution-surfaced refinements (newer takes precedence over A12/A15 literal wording; conflict noted) and the master verification, per Law 3.
**Affected:** `warehouse_robot/cli.py`, `warehouse_robot/write_gate.py`; A12, A15 (refined here).

## A20 — Phase 1 independent exit check: GREEN-with-waiver (2026-06-20)

**Decision:** the independent Phase-1 exit check was run by **Codex** (a different tool/system, not a Claude/Fable build session) and recorded in [[08-Phase 1 Exit Check — Verification Report (Codex)]]. **Code/behaviour verdict: GREEN, independently** — A8 both parts (two rebuilds byte-identical + live-vs-rebuild logical-digest equal), the full vertical slice, antechamber-mirror re-derivation, flag survival across reconcile, clean-graph-zero-flags, no git leakage, no robot git invocation, and all flagged deviations (D6/D9/D13/PC1b) confirmed present as documented. The verifier returned **RED on evidence-completeness only**, for the R11 session-id assertion.
**Waiver:** the **R11 session-id-difference sub-check is WAIVED**. The B4/B5 delivery-note session IDs were never recorded and are unrecoverable (owner). The assertion is a *proxy* for verifier independence; independence here is established more strongly by construction — the verifier was a **different tool (Codex)** that provably did not build B1–B5, ran after, and re-derived results with its own scripts. The proxy is moot when the property it stands for holds by a stronger argument. Owner-accepted.
**B1–B3 receipt/SQLite-version gaps (verifier #2/#3):** accepted as **historical** — B1–B3 shipped before A11; A11 is forward-only. Not exit-blocking; optional backfill only.
**Therefore: Phase 1 exit = GREEN** (build B1–B5 complete, independently verified; the exit RED-on-governance is adjudicated GREEN by this waiver).
**Lesson / process fix (flag, candidate):** capture the build session id in the delivery note **at build time**, not from owner memory, so the R11 anchor is never blank again — a small Starter-A / delivery-note-template improvement for future runs.
**Rationale:** never let a missing proxy-value block a verdict when the underlying property (independence) is established by stronger evidence; record the waiver and the lesson rather than silently passing (Law 4).
**Affected:** Phase 1 status (→ GREEN); the exit-check report (left as the verifier authored it — RED on its own terms); candidate: delivery-note template + Starter A (session-id capture).

---

# References

- Execution Plan — Warehouse Initiation Project (this folder) — the plan these decisions govern
- Pre-Build Decision List (docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization) — problem framings and origins of G1–G12
- Sessions 3–8 (docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization) — the fixed architecture
- SPQR AGENT_LAWS — Law 3 (external record is truth), Law 4 (independence)
