## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Execution schedule — warehouse build, migration, SPQR v2.0 cutover

**Document status:** Test draft — agent-proposed alternative rendering of the owner's high-level schedule; not authoritative

**Date:** 2026-06-11

**Purpose:** Show how the agent would structure the schedule and its documentation. The owner's "Project quick notes" remains the working plan; this is a comparison artifact.

---

# Principles the schedule follows

- **Build → load → cutover, in that order.** Agents can't follow a query policy against a warehouse that doesn't exist, and shouldn't meet an empty one.
- **Cutover is atomic in nature:** everything an agent needs to live on the warehouse ships in one update (v2.0); everything else waits (v2.1). Split rule: *does it touch a file or process the cutover rewrites? → v2.0; else → v2.1.*
- **Test-run regime until explicit cutover:** flat docs stay authoritative and intact (S8 P4 pruning deferred); the warehouse is a candidate that must earn trust; full reset stays possible.
- **Each phase ends with a fold-back** (status into this schedule + the decision list), per the established per-session rule.

# Schedule

## Phase 0 — Baseline (now, zero new scope)

- Commit/push v1.3 as-is + readme update. Clean baseline before the big jump.
- Mark Notion knowledge copies as dead projections (banner); Notion = ticketing only (FDP, SAW).
- Interim documentation regime active (see below).

## Phase 1 — Warehouse core build

- **1.1 Planning session** — consumes the *Pre-Build Decision List* Group 1 (G1, G2, G3, G6, G8) as its decision agenda; then breaks the build into tickets. Documentation home decision (Obsidian) is folded in here.
- **1.2 Build tickets (milestone-level, not full pipeline ceremony):**
  - B1 — markdown store + node/edge layout + SQLite DDL (nodes, edges, FTS5, counter, flag plane, antechamber mirror, trace)
  - B2 — the fold: incremental upsert + reconcile rebuild + divergence check
  - B3 — query interface: open_scope / find / fetch / traverse + intent/verdict trace + budget dials
  - B4 — write gate: hard-schema validation, proposal state machine, ID allocation, antechamber
  - B5 — audit tripwires: orphan watch, missing-recommended-edge, relates-to overuse
- **Exit check:** vertical slice proven with 10–15 hand-made test nodes; reconcile rebuild reproduces the index byte-identically.

## Phase 2 — Migration (first load)

- S8 runbook P0–P3 only (P4 pruning explicitly excluded — deferred to Phase 5).
- P0 triage includes the **scope-vocabulary re-derive** (G11, S5 mandatory guard).
- Owner-led parts: committed-vs-exploratory triage, backfill authoring, batch semantic review (bootstrap gate).
- **Exit check:** final reconcile clean; owner batch review done; warehouse content spot-checked against flat docs.

## Phase 3 — SPQR v2.0 planning + execution (the cutover update)

- **3.1 Planning session** — consumes Decision List Group 2, **G7 (wake/escalation) first** — everything else hangs on it; G4 folds into G7; SAW ticket/epic alignment, version number.
- **v2.0 scope (warehouse-coupled only):**
  - warehouse-ingest skill (the S8 proposer contract realized)
  - per-archetype query-policy blocks in agent files (budgets + the SCRUTINIZE DENY)
  - antechamber discipline + revise-wake + Senate ingest-judgment path (G7/G4)
  - new handoff process + SAW-26 verification-on-handoff (handoff carries trace + antechamber state → warehouse-coupled)
  - SAW-28 review: expected verdict *absorbed by warehouse* (auto-generated index + scoped TOC supersede the live-manifest idea) — close or rescope, don't redesign blind
  - documentation regime switch-over rules; generic-first → Foodoire import (G10)
- **Exit check:** one full SPQR run (a real ticket) executed against the warehouse in test-run regime, flat docs untouched.

## Phase 4 — First live write-path exercise (process bugs)

- Feed the badly-updated flat-doc gaps from the dev-ticket runs as a **backfill batch** — the S8 backfill provenance class as the first hot-path test of propose → gate → Senate → ingest.
- Retro on the run: trace review (WRONG-ENTRY/ABSENT rates), flag sweep, first calibration data for the parked measurement lane.

## Phase 5 — Cutover decision + v2.1

- **Owner cutover call:** warehouse earned trust? → execute S8 P4 (prose-pruning), warehouse becomes canonical. If not → reset path: wipe warehouse, fix, re-run Phase 2 (cheap by design — migration is a bulk write-path run).
- **v2.1 batch (independent items):** SAW-1, SAW-16, SAW-17, SAW-29 bug pipeline, model-usage switch area, git-process formalization remainder, SAW-27 telemetry thin layer (built to consume the S4 trace, not parallel to it).
- Deferred decisions stay deferred: multi-step prompting (not yet), sorting/orchestrator agent (not yet — consistent with the parked CONSULT lane).

# Interim documentation regime (Phase 0 → cutover)

- **One source of truth:** the Obsidian/git flat structure. Notion copies are dead.
- **New decision → one atomic ADR file** in `decisions/` (the prototype format); **new lesson → append-only LESSONS entry.** Append-only means late-arriving knowledge just joins the migration batch or ingests after — nothing waits.
- **Never hand-mint warehouse artifacts:** no hand-assigned `food-nNN` IDs, no hand-written node files — ID allocation is the robot gate's monopoly (S7). The ADR format is warehouse-ready enough; migration picks it up cheaply.
- **Known cost:** flat↔warehouse consistency during the dual-source window is manual (the S7 divergence check covers markdown-vs-index, not flat-docs-vs-warehouse). Accepted for the test run; the Phase 4 retro is the checkpoint where drift gets measured.

# Parked lane (recorded so it survives — Law 3)

Golden query set + IR harness · reconcile schedule · semantic-audit cadence · promotion-gate activation + bookkeeping (G12) · embedding trigger watch · model-tiering measurement · strategic lane (J, CONSULT, I, Curator).

# References

- Project quick notes (Obsidian vault) — the owner's working schedule this renders
- Knowledge Architecture — Pre-Build Decision List (this folder) — Groups 1/2/3 consumed by phases 1.1 / 3.1
- Session 3–8 docs (this folder) — the fixed architecture all phases implement
