---
up: "[[v1.5]]"
group: "Warehouse Initiation — spec & decisions"
order: 7/8
saw: [SAW-30]
type: spec
poc: ["[[Knowledge Architecture — Pre-Build Decision List (Planning Session Input)]]", "[[Knowledge Architecture & Token Optimization — Direction Checkpoint PoC]]"]
tags: [group, warehouse]
---

## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Warehouse Initiation Project — authoritative execution plan (build, import, migration, SPQR v1.5 cutover)

**SAW Ticket (build + migration):** https://app.notion.com/p/37d68d5de1e8817faeacec620076f128

**SAW Ticket (SPQR upgrade):** https://app.notion.com/p/37d68d5de1e8813a964ed3855557d2b4

**Document status:** Active — this is the plan to follow. Supersedes the test-draft "Execution Schedule — Warehouse Build & SPQR Cutover - test" (docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization) and the former Overview document (deleted 2026-06-12).

**Date:** 2026-06-12

**Decision record:** Planning Decisions — Warehouse Initiation Project (this folder). Do not re-derive decisions; read that file.

---

# Principles

- **Build → import → load → cutover, in that order.** The warehouse is built and proven in the generic SPQR repo, imported into Foodoire, loaded by migration, and only then does SPQR cut over to it.
- **Generic-first build (A1):** robot code, DDL, and the test suite are born in the generic repo — the seed's natural home. Foodoire receives a proven package via import; no later extraction needed.
- **Cutover is atomic:** everything an agent needs to live on the warehouse ships in one update (v1.5). Clean non-coupled items go to the v1.5.1 post-warehouse batch.
- **Test-run regime until explicit cutover:** flat docs stay authoritative and intact (S8 P4 pruning deferred); the warehouse is a candidate that must earn trust; full reset stays possible.
- **Each phase ends with a fold-back** — status into this plan and into the decision record.

# Phases

## Phase 0 — Baseline — DONE

- v1.3 committed/pushed as baseline. DONE.
- Notion knowledge copies marked dead projections (main folder); Notion = ticketing only (FDP, SAW). DONE.
- Foodoire clean baseline achieved 2026-06-12: DEV-001–003 cycle merged to `main` (fast-forward), worktree removed, branch deleted. Single checkout, linear history. DONE (A7).
- Interim documentation regime active (see below).

## Phase 1 — Warehouse core build (generic SPQR repo)

All build work happens in the generic SPQR repo, on `main`, owner-committed at checkpoints (A5). The robot takes a warehouse-root parameter from day one (A4) — no hardcoded paths.

**Build tickets (milestone-level ceremony — see decision record for what that includes):**

- **B1** — markdown store + node/edge layout + SQLite DDL (nodes, edges, FTS5, counter, flag plane, antechamber mirror, trace)
- **B2** — the fold: incremental upsert + reconcile rebuild + divergence check
- **B3** — query interface: `open_scope` / `find` / `fetch` / `traverse` + intent/verdict trace + budget dials
- **B4** — write gate: hard-schema validation, proposal state machine, ID allocation, antechamber
- **B5** — audit tripwires: orphan watch, missing-recommended-edge, relates-to overuse

**Testing discipline (A4):** fixtures (10–15 hand-made sample nodes + query set) are versioned next to the robot code. Every test run folds fixtures into a disposable warehouse instance in a gitignored/tmp directory, asserts there, and deletes the instance. No test content ever enters a canonical warehouse or git history.

**Exit check:** vertical slice proven against a fixture-built instance; reconcile rebuild reproduces the index byte-identically.

## Phase 1.5 — Foodoire import (the G10 mechanism, first live run)

- Copy robot code + DDL + test suite into Foodoire (plain copy, A2 — no submodules).
- Create the empty physical layout in Foodoire (A3): `project_memory/warehouse/` + `project_memory/antechamber/` siblings; derived index gitignored.
- Smoke test: run the fixture suite against a disposable instance inside Foodoire to prove the copy works in its new home.
- **Exit check:** fixture suite green in Foodoire; canonical `project_memory/warehouse/` exists and is empty.

## Phase 2 — Migration (first load, in Foodoire)

- S8 runbook P0–P3 only (P4 pruning explicitly excluded — deferred to Phase 5).
- P0 triage includes the **scope-vocabulary re-derive** (G11, S5 mandatory guard).
- Owner-led parts: committed-vs-exploratory triage, backfill authoring, batch semantic review (bootstrap gate).
- **Exit check:** final reconcile clean; owner batch review done; warehouse content spot-checked against flat docs.

## Phase 3 — SPQR v1.5 planning + execution (the cutover update)

- **3.1 Planning session** — consumes decision record Group 2, **G7 (wake/escalation) first** — everything else hangs on it; G4 folds into G7; SAW ticket/epic alignment.
- **v1.5 scope (warehouse-coupled only):**
  - warehouse-ingest skill (the S8 proposer contract realized)
  - per-archetype query-policy blocks in agent files (budgets + the SCRUTINIZE DENY)
  - antechamber discipline + revise-wake + Senate ingest-judgment path (G7/G4)
  - new handoff process + SAW-26 verification-on-handoff
  - documentation regime switch-over rules
- **Exit check:** one full SPQR run (a real ticket) executed against the warehouse in test-run regime, flat docs untouched.

## Phase 4 — First live write-path exercise (process bugs)

- Feed the badly-updated flat-doc gaps from the dev-ticket runs as a **backfill batch** — the S8 backfill provenance class as the first hot-path test of propose → gate → Senate → ingest.
- Retro on the run: trace review (WRONG-ENTRY/ABSENT rates), flag sweep, first calibration data for the parked measurement lane.

## Phase 5 — Cutover decision

- **Owner cutover call:** warehouse earned trust? → execute S8 P4 (prose-pruning), warehouse becomes canonical. If not → reset path: wipe warehouse, fix, re-run Phase 2 (cheap by design).
- Deferred decisions stay deferred: multi-step prompting, sorting/orchestrator agent (consistent with the parked CONSULT lane).
- **Next era:** v2.0 — Semi-Automated Pipeline (roadmap unchanged) consumes what v1.5 leaves behind.

## Post-warehouse batch — v1.5.1 (after Phase 5)

- v1.4 parallel track dropped (owner decision 2026-06-12); clean items carry forward.
- **Carry-forward:** SAW-17, SAW-26, SAW-27, SAW-29; model-usage switch area; git-process formalization remainder (incl. branching-methodology redesign, A5). SAW-27 telemetry designed to consume the S4 trace.
- **Obsoleted:** SAW-1 (superseded by the v1.5 write path), SAW-28 (absorbed by warehouse projection model). Closed in Notion 2026-06-12.

# Interim documentation regime (Phase 0 → cutover)

- **One source of truth:** the Obsidian/git flat structure. Notion copies are dead.
- **New decision → one atomic ADR file; new lesson → append-only LESSONS entry.** Late-arriving knowledge joins the migration batch or ingests after — nothing waits.
- **Never hand-mint warehouse artifacts:** no hand-assigned IDs, no hand-written node files — ID allocation is the robot gate's monopoly (S7).
- **This project documents here:** the `docs/spqr_self/upgrades/v1.5/` folder is the documentation home (A6); build sessions write their outputs here.
- **Known cost:** flat↔warehouse consistency during the dual-source window is manual. Accepted for the test run; the Phase 4 retro measures drift.

# Git working rules for this project (A4 + A5)

- Development on `main` in the respective repo (generic for Phase 1, Foodoire from Phase 1.5). No worktrees, no long-lived branches while a single line of work is active.
- Owner batch-commits at checkpoints; the robot writes files, never commits (G3).
- No test branches: test isolation is directory-level (disposable instances), not git-level — branch switching does not reset untracked index files, so a branch cannot isolate the derived state.
- Canonical `project_memory/warehouse/` stays empty until Phase 2 migration.

# Parked lane (recorded so it survives — Law 3)

Golden query set + IR harness (grows out of the fixture query set) · reconcile schedule · semantic-audit cadence · promotion-gate activation + bookkeeping (G12) · embedding trigger watch · model-tiering measurement · strategic lane (J, CONSULT, I, Curator).

# References

- Planning Decisions — Warehouse Initiation Project (this folder) — the decision record this plan executes
- Sessions 3–8 (docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization) — the fixed architecture
- Pre-Build Decision List (docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization) — origin of G1–G12
- Superseded: "Execution Schedule — Warehouse Build & SPQR Cutover - test" (docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization)
