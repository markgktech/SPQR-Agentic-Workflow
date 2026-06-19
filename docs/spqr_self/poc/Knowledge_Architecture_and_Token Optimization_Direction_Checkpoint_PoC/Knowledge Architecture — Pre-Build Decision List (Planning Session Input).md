## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — open decisions left between the PoC arc (S3–S8) and implementation

**Document status:** Open — input for the warehouse-build planning session (schedule item 1.1)

**Phase:** Pre-build (the PoC arc is closed; nothing here reopens an S3–S8 decision)

**Date:** 2026-06-11

**Session scope:** The gap list only — items the S3–S8 sessions handed off but no session picked up, plus implementation-shaping decisions no session owned. Candidate directions are non-binding; the planning session decides.

**Purpose:** Give the planning mini-session (Sonnet/Opus) a complete, contextualized decision backlog so it closes decisions instead of rediscovering them.

**Status legend:** decided · leaning · mixed · open

---

# Overview

The S3–S8 arc closed the architecture, but a post-arc gap review (2026-06-10) found a set of items that fell between sessions: most are "session A handed it to session B, session B never picked it up" cases, the rest are implementation-shaping decisions no session owned. This page is the single backlog for them, grouped by **when they block**: Group 1 blocks the warehouse core build, Group 2 blocks the v1.5 SPQR-cutover planning, Group 3 is runbook additions and parked bookkeeping. Each item carries the problem framing, its origin, a non-binding candidate direction, and what waits on it. The planning session should walk Group 1 to closure; Group 2 may close here or in the v1.5 planning session; Group 3 needs no discussion, only carrying.

# Fixed inputs — owner decisions already taken (2026-06-11, do not re-litigate)

- **Source of truth is the Obsidian/git flat-file structure.** Notion copies are dead projections; Notion keeps ticketing only (FDP, SAW).
- **Update split:** one big **v1.5** = warehouse build + SPQR prepared to run on the warehouse; everything not warehouse-coupled goes to a separate independent batch (**v1.4**, may ship in parallel with the build). v1.3 is closed/committed as baseline before v1.5.
- **Versioning (2026-06-12):** the warehouse rollout is named **v1.5 — Knowledge Warehouse**; **v2.0 stays Semi-Automated Pipeline** on the roadmap and in the SAW epics — no renumbering. Rationale: renumbering existing epics/tickets/roadmap docs invites record drift; the warehouse is a 1.x-era substrate change (the manual pipeline stays manual), and v2.0 will consume it. The number "v1.5" was once an informal internal shorthand during the v1.1 era and never entered the record — officially unused, now claimed.
- **The old flat docs are NOT pruned for now.** S8 Phase 4 (prose-pruning) is deferred indefinitely: the warehouse run is a test run, the flat docs stay intact as fallback, and a full warehouse reset must remain possible if the content comes out distorted. Recorded as a deliberate deviation from the S8 P4 invariant — accepted cost: a dual-source window in which flat docs remain authoritative and the warehouse is a candidate, until an explicit owner cutover call.
- **First live write-path exercise:** after migration, the badly-updated flat-doc gaps from the dev-ticket runs are fed in as a backfill batch (schedule item 4, "process bugs"). This is the S8 backfill provenance class running as the first hot-path test.

# Breakdown — the decision backlog

## Group 1 — blocks the warehouse core build (close in planning session 1.1)

### G1 — Robot process lifecycle

- **Problem:** Is the warehouse robot a persistent process (server) or a per-call process (CLI invocation)? S7 chose SQLite precisely to be robust to this question, then carried it: "pin during SPQR-runtime implementation." Every line of robot code depends on the answer.
- **Origin:** S7 carried item.
- **Candidate (non-binding):** per-call process. Simpler, no daemon management, crash-safe by construction (state lives in markdown + SQLite, never in the process), and matches the single-writer gate model. A persistent server buys latency we don't need at ~10k nodes.
- **Blocks:** all robot code (B-phase).

### G2 — Agent-to-robot binding

- **Problem:** How does an agent physically call `open_scope` / `find` / `fetch` / `traverse`? MCP tool vs CLI over Bash. No session decided this. It touches W3 (portability): MCP is a standard but runtime-flavored; a CLI is universally callable from any runtime.
- **Origin:** unowned — implementation-shaping.
- **Candidate (non-binding):** CLI first (one binary/script, structured JSON out), optionally wrapped as an MCP tool later. The contract (S4) is the stable seam; the binding is swappable by design. Pairs naturally with G1=per-call.
- **Blocks:** query-interface build (B3) and the ingest skill design (v1.5).

### G3 — Robot write/commit policy vs the owner git rule

- **Problem:** The warehouse markdown is git-native truth and the robot writes node files at ingest — but the standing owner rule says no agent or session ever runs `git commit`/`git push`. Is the deterministic robot bound by that rule? If yes, truth-versioning happens only at owner batch-commits; the window between ingest and commit is unversioned.
- **Origin:** S7 substrate decision × standing owner rule; surfaced in the gap review.
- **Candidate (non-binding):** the robot writes files but never commits; the owner batch-commits at checkpoints (e.g. after each ingest batch / migration phase). Keeps the rule intact; the unversioned window is acceptable because markdown-write + SQLite-index are already crash-consistent (S7), and the warehouse is in test-run regime anyway. Fold this into schedule item 3.1.11 (git-process formalization) as one decision.
- **Blocks:** write-gate build (B4); migration runbook.

### G6 — Antechamber physical store

- **Problem:** S6 fixed the proposal lifecycle, S7 fixed the substrate for *ingested* knowledge — but where proposals physically live (markdown dir vs SQLite table) was never pinned. Trade: a SQLite-resident antechamber is lost on index rebuild (the index is disposable by design — proposals are NOT disposable, they are un-ingested work); a markdown antechamber survives rebuilds but adds a second file-write path.
- **Origin:** fell between S6 and S7.
- **Candidate (non-binding):** markdown antechamber directory (e.g. `warehouse/antechamber/`), mirrored into the index like everything else. Rationale: the index must stay 100% derived/disposable — putting the only copy of pending proposals in it breaks that invariant. This is the one Group-1 item where the candidate direction contradicts an earlier casual suggestion (SQLite table) — discuss, don't rubber-stamp.
- **Blocks:** write-gate + antechamber build (B4); migration resumability (S8 checkpoint relies on the antechamber).

### G8 — Archetype identity for query-policy enforcement

- **Problem:** The S4 per-archetype query policy (budgets + the SCRUTINIZE DENY) is "robot-enforced" — but the robot must know which archetype is calling. Self-declared parameter (honor system) vs per-agent key/token. The DENY serves review independence (Law 4), so a silent policy bypass is exactly the failure it exists to prevent.
- **Origin:** S4 implementation seam, unowned.
- **Candidate (non-binding):** self-declared `--archetype` parameter in v1, logged in the trace (so a bypass is at least visible in retro), upgrade to enforced identity only if the trace shows violations. Honest about the trust level; zero infrastructure now.
- **Blocks:** query-interface build (B3).

## Group 2 — blocks v1.5 SPQR-cutover planning (close in 3.1 planning, or here if time allows)

### G4 — Continuation-grant issuance mechanism

- **Problem:** S4 fixed that budget exhaustion is an owner-escalation halt and a fresh budget needs an owner-issued continuation grant enforced by the robot as a consent-gate — then handed the *issuance mechanism* (how the owner grants, what the grant artifact is) to "S6/SPQR-level." S6 never picked it up.
- **Origin:** S4 → S6 dropped handoff.
- **Candidate (non-binding):** a grant is a one-shot token the owner issues in-session (a line the owner types / a file the owner touches), consumed by the robot on the next round. Detail it inside the v1.5 wake/escalation design (G7) — same machinery.
- **Blocks:** v1.5 agent-process design; not the core build.

### G5 — Scope-vocabulary governance

- **Problem:** S5 fixed that scope is a controlled vocabulary and "new values are a governed act (S6)" — S6 never addressed it. Who may mint a new scope value, and through what act? Free minting fragments the deterministic filter (the exact failure the controlled vocabulary prevents); too-heavy governance makes every novel topic an escalation.
- **Origin:** S5 → S6 dropped handoff.
- **Candidate (non-binding):** new scope = a Senate-gated proposal class (never auto-ingested, regardless of promotion state), because a scope value is schema-adjacent, not content. At migration, the vocabulary is re-derived wholesale under the owner bootstrap-gate (see G11).
- **Blocks:** v1.5 ingest skill + the migration triage.

### G7 — Wake/escalation mechanics (the biggest v1.5 design item)

- **Problem:** S6's state machine says `revise` "wakes the proposing agent" and the robot "escalates to the Senate" — but in the Claude-session world there is no daemon that wakes anyone. The whole S6 write path hangs on this mechanism existing. Candidate shapes: a pending-queue the next session checks at start (session-starter discipline), an owner-mediated notification, or a scheduled sweep.
- **Origin:** S6 SPQR-side, explicitly descoped to the SPQR update.
- **Candidate (non-binding):** queue + session-starter check (no daemon): the antechamber IS the queue; every SPQR session-starter includes a "check pending warehouse items addressed to your ticket+agent" step; Senate-pending items surface to the owner at session start. Deterministic, zero infra, fits Law 3 (external record over memory). Design this FIRST in the v1.5 planning — D-phase items hang on it.
- **Blocks:** v1.5 everything (handoff, Senate judgment, revise loop).

### G10 — Seed vs local packaging mechanism

- **Problem:** The robot code + generic schema live in the generic SPQR repo (the seed); Foodoire grows local content. The schedule fixes the direction (generic first → import to Foodoire) but not the mechanism: how does a project consume the robot — copy, submodule, or path reference? How does an umbilical-cord schema update reach a live project warehouse (schema_version exists for this, but the update *procedure* doesn't)?
- **Origin:** S1 cross-cutting concept, never broken down.
- **Candidate (non-binding):** v1 = plain copy at import (matching the existing SPQR template practice), schema_version stamped per node; a schema bump ships as a re-fold transform script in the seed. Submodules add git complexity the owner workflow doesn't want.
- **Blocks:** v1.5 packaging + the Foodoire import step.

### G9 — Ticket→session-id map artifact

- **Problem:** S3/S5 fixed that the warehouse stores only the `ticket`+`agent` join key and "the full ticket→session-id map lives in Obsidian" — but that artifact doesn't exist and nobody defined its shape or maintenance.
- **Origin:** S3/S5 external reference, dangling.
- **Candidate (non-binding):** one append-only markdown table in the vault (ticket · agent · session tab-name · date), maintained by session-starter discipline. Cheap; only exists to make provenance reconstructable.
- **Blocks:** nothing hard — provenance reconstruction quality.

## Group 3 — runbook additions & parked items (no discussion needed, just carry)

- **G11 — scope re-derive step:** S5's mandatory guard ("re-derive the scope vocabulary against real content at migration; do not force-fit the provisional list") is not yet an explicit migration-runbook line. Add to Phase 0/1 of the S8 runbook when migration is ticketed.
- **P4 deferral (recorded):** S8 Phase 4 prose-pruning is deferred by owner decision (see Fixed inputs). The migration ticket set must exclude P4; cutover gets its own later decision point.
- **G12 — promotion-gate bookkeeping:** where promoted proposal-classes are recorded (config file vs warehouse node). Parked until the gate is activated (everything starts un-promoted anyway).
- **Parked measurement lane (unchanged):** golden query set + IR harness, reconcile schedule, semantic-audit cadence, model-tiering tuning, embedding trigger watch.

# Recommendations

- **Planning session 1.1 consumes Group 1 as its decision agenda** — five items, each pre-framed; the session's job is closure, not rediscovery. Walk them in order G1 → G2 → G3 → G6 → G8 (G1+G2 shape everything after).
- **Group 2 belongs to the v1.5 planning session (3.1)** — G7 first; G4 folds into G7's design; G5 and G10 are independent.
- **Candidates are non-binding** (ticket problem-framing rule): the problem and origin are the fixed part; challenge the candidate directions freely.
- **On closure, fold results back** into this page (status per item) and into the parent direction map — the per-session fold-back rule continues to apply.

# References

- Session 3–8 docs (this folder) — origin of each dropped handoff, cited per item
- Session Roadmap: Open-Question Map & Critical Decisions (this folder) — the arc this backlog post-dates
- Post-arc gap review, 2026-06-10 session — where G1–G12 were identified
- Project quick notes (Obsidian vault) — the high-level schedule this feeds (item 1.1)
- SPQR AGENT_LAWS — Law 3 (external record is truth), Law 4 (independence; G8's DENY rationale)
