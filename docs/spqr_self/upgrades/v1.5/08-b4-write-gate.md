---
up: "[[v1.5]]"
group: "Warehouse Initiation — build (B1–B5)"
order: 8/8
saw: [SAW-30]
ticket: B4
status: pending
type: brief
tags: [group, warehouse, brief]
---

# B4 — Write gate (brief)

## Brief
GROUP:         Warehouse Initiation — B4 write gate
ORDER:         8/8 (warehouse build; B4 of B1–B5)
REPO:          SPQR (generic; per A1 generic-first — no Foodoire content)
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/08-b4-write-gate.md
RATIONALE:     B4 is one coherent surface — the write path (Session 6 Cluster A) inside the `warehouse_robot/` package.
SOURCE_OF_TRUTH: 07-Planning Decisions — Warehouse Initiation Project (G1–G8 + A1–A18). Derive from it; do not re-decide. Roundtable findings: 08-roundtable-b4-b5-exit.
MODEL:         **Starter A (per A9)** — plan-first → surface every contradiction → WAIT for owner approval → execute. This augments, does not replace, the B1–B3 discipline. Not the brief-only "start without questions" model.
FILL_CHANGES_MADE: yes (one-line pointer to the 08-B4 delivery note, which is the full record per Starter A DoD)

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/upgrades/v1.5/07-Session Starters — Build Tickets & Exit Check  (Starter A)
  - docs/spqr_self/upgrades/v1.5/07-Execution Plan — Warehouse Initiation Project
  - docs/spqr_self/upgrades/v1.5/07-Planning Decisions — Warehouse Initiation Project  (G1–G8 + A1–A18 — esp. A9–A18)
  - docs/spqr_self/upgrades/v1.5/08-roundtable-b4-b5-exit  (the B4-relevant findings)
  - docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization/Knowledge Architecture — Session 6 Write Path, Antechamber & Audit  (Cluster A = B4)
  - docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization/Knowledge Architecture — Session 7 Storage Substrate & Retrieval Runtime
  - docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization/Knowledge Architecture — Session 3 Node Schema & Graph Ontology  (ontology the gate validates)
  - ALL of 08-B1 / 08-B2 / 08-B3 delivery notes (dependency gate + open questions for B4)

DEPENDENCY GATE: B1 + B2 delivery notes GREEN (B4 uses B1 schema + B2 fold). Per A10, the master RE-RUNS the prior suite at gate time — do not trust the GREEN token alone. STOP if any dependency is missing/not-green.

## Scope — build exactly this (Session 6 Cluster A)
- **Hard-schema gate:** validate a proposal's well-formedness (id/kind/origin per S3; required per-kind fields — decision→scope, constraint→source, lesson→agent+ticket). Malformed → `rejected-malformed`, no Senate cost.
- **Proposal state machine:** `proposed` → [robot hard-gate] → `rejected-malformed` | `validated` → [robot pre-check + escalation decision] → `auto-ingested` (see plan-call #1) | `pending-senate` → [verdict applied] → `ingested` | `rejected` | `revise`.
- **ID allocation (robot monopoly):** allocate from `id_counter` via the gate transaction, never markdown-max (A15); the antechamber mirror must not perturb the counter.
- **Antechamber handling:** write pending proposals to the antechamber markdown dir (sibling, outside warehouse — G6/A3) + maintain the antechamber mirror table; the append of an ingested node (node file + edges) happens at the serializing gate.
- **revise:** no separate state — re-enters at `proposed`, bounded N-round loop → owner escalation; binds self-declared `ticket`+`agent`, logged (A15).
- **Robot writes files, never commits (G3).**

## Plan-phase calls — surface these in PHASE 1, decide WITH the owner (A15/R9, do not silently pick)
1. **`auto-ingested` state:** build reachable-but-empty (DDL already admits it) vs defer the promotion gate. Position: build-empty (no dead DDL path); promotion logic is SAW-31/Cluster C.
2. **Antechamber↔mirror reconcile + divergence:** build it now (a B2-analogue check; the mirror is not markdown-derivable and is excluded from the A8 digest — L4/R3) vs defer-with-reason. Position: build a minimal reconcile + divergence signal; if deferred, the exit-check still re-derives the mirror from the antechamber dir.
3. **Antechamber-READ visibility policy** (archetype-conditional: SCRUTINIZE shielded / EXECUTE sibling-read / SYNTHESIZE delta — Session 6): B4 sub-surface vs defer to SAW-31 ingest discipline. Position: **defer to SAW-31** (B3 ships canonical-plane-only; B4 builds WRITE + mirror, not a new read verb) — confirm.
4. **Verdict application surface:** B4 builds the robot side that APPLIES a Senate verdict (ingest/reject/revise → state + append); WHO issues the verdict (Senate wake) is SAW-31. Confirm the boundary.
5. **Schema change?** If B4 adds columns/states (e.g. a proposal-event log), bump `schema_version` + carry it in fold/reconcile (A14-digest implications, M4). State whether B4 touches the schema.

## Test & verification contract (binding — A10/A11/A12/A16/A17)
- **Fixtures (A16):** add versioned, synthetic, project-neutral fixtures — malformed proposals (each rejection reason), a proposal walked through the FULL state machine, a born-retired node. Disposable-instance only (A12).
- **Isolation (A12):** disposable unit = warehouse root + antechamber sibling under ONE system-tmp parent, deleted together. Extend the instance `.gitignore` to cover **node + antechamber markdown**, not only `index.sqlite*`.
- **Evidence (A11):** delivery-note §4 carries a **verbatim `receipt:`** (decisive `Ran N tests … OK` line, no paraphrase); full suite run **≥5× consecutively**, count cited; record the **SQLite version** + Python version.
- **e2e (A17):** contribute the B4 leg of the L1 automated vertical-slice scenario (propose→gate→ingest) and at least one L2 subprocess CLI write-path session. (Full vertical slice completes at B5/exit.)
- **DoD (per Starter A + A10/A11):** scope built · fixtures green vs a disposable instance · the 08-B4 delivery note written · per-checkpoint comment drafted. The master then runs the A10 critical re-test (bounded smoke + cross-B seam: B4 allocates an id → B2 fold sees it → B3 query reads it).

## FILES (expected — confirm in the plan)
  warehouse_robot/write_gate.py: NEW — hard-schema gate, proposal state machine, ID allocation, antechamber write + verdict application
  warehouse_robot/schema.py: extend only if a new column/state is needed (bump schema_version — A15/M4)
  warehouse_robot/cli.py: NEW write-path subcommands; extend INSTANCE_GITIGNORE to cover node + antechamber markdown (A12)
  warehouse_robot/errors.py: write-path error types
  warehouse_robot/fixtures/: NEW write-path fixtures (A16)
  warehouse_robot/tests/: NEW write-gate + state-machine + isolation + L1/L2 tests
  warehouse_robot/docs/: write-path contract doc (NODE_FORMAT/QUERY_PROTOCOL sibling) if a new agent-facing contract is introduced

## Scope fence — do NOT build (flag if found, per Law 1)
- B5 audit tripwires (orphan/missing-edge/relates-to overuse) — separate session.
- The promotion-gate logic / auto-ingest *promotion* (Cluster C) — mechanism stub only (#1); policy is SAW-31.
- The Senate wake / session-starter pending-check (G7/G4) — SAW-31.
- Any Foodoire content or migration (A1 generic-first; M2 migration runs later, through this gate).

## Changes Made — _(pending execution)_
