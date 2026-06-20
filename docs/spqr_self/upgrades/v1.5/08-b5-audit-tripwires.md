---
up: "[[v1.5]]"
group: "Warehouse Initiation — build (B1–B5)"
order: 8/8
saw: [SAW-30]
ticket: B5
status: green
type: brief
tags: [group, warehouse, brief]
---

# B5 — Audit tripwires (brief)

## Brief
GROUP:         Warehouse Initiation — B5 audit tripwires
ORDER:         8/8 (warehouse build; B5 of B1–B5 — the last build)
REPO:          SPQR (generic; A1 generic-first — no Foodoire content)
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/08-b5-audit-tripwires.md
RATIONALE:     B5 is one coherent surface — the deterministic audit layer (Session 6 Cluster B) inside `warehouse_robot/`.
SOURCE_OF_TRUTH: 07-Planning Decisions — Warehouse Initiation Project (G1–G8 + A1–A19; the tripwire shapes are A14). Roundtable: 08-roundtable-b4-b5-exit. Derive, do not re-decide.
MODEL:         **Starter A (per A9)** — plan-first → surface every contradiction → WAIT for owner approval → execute. Augments, does not replace, B1–B4 discipline.
FILL_CHANGES_MADE: yes (one-line pointer to the 08-B5 delivery note)

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/upgrades/v1.5/07-Session Starters — Build Tickets & Exit Check  (Starter A)
  - docs/spqr_self/upgrades/v1.5/07-Planning Decisions — Warehouse Initiation Project  (esp. A14 tripwire shapes, A9–A19)
  - docs/spqr_self/upgrades/v1.5/08-roundtable-b4-b5-exit  (B5 findings: G15/L1 definitions, L7 scope-creep guard)
  - docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization/Knowledge Architecture — Session 6 Write Path, Antechamber & Audit  (Cluster B = B5)
  - docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization/Knowledge Architecture — Session 3 Node Schema & Graph Ontology  (edge ontology; the lesson→about rule)
  - ALL of 08-B1 / 08-B2 / 08-B3 / 08-B4 delivery notes (dependency gate; B5 reads the graph B1–B4 produce)

DEPENDENCY GATE: B1–B4 delivery notes GREEN (B5 reads the populated graph + the B1 flag plane; flags reuse the append machinery). Per A10, the master RE-RUNS the prior suite at gate time — do not trust the GREEN token. STOP if any dependency is missing/not-green.

## Scope — build exactly this (Session 6 Cluster B), per A14
Three **deterministic, graph-structural** tripwires that **only ever FLAG — never mutate** the target:
- **orphan** = a *knowledge* node (kind decision/constraint/lesson) with **0 inbound AND 0 outbound** edges, **excluding** origin-flagged foundational nodes.
- **relates-to overuse** = a node carrying **> K** `relates-to` edges; **K = 5 (placeholder dial**, calibrated later — B3 budget-dial precedent).
- **missing-recommended-edge** = a node lacking an edge its kind is expected to carry, per a **per-kind recommended-edge table seeded from Session 3** — initially the single architecture-stated rule **`lesson → about`**; the table grows by governance (no invented rules).
**Flag = an append-only audit-node on a SEPARATE plane** (plane discriminator `f` vs `n`), pointing at its target via a `flags` edge, never mutating the target; **open/resolved status is DERIVED** from an incoming `resolves` edge (mirror of S3's "superseded is derived"). Multiple flags per node = multiple flag-nodes (node "heat" = aggregate of open flags).

## Plan-phase calls — surface in PHASE 1 with your position (do not silently pick)
1. **Flag emission mechanism:** flags are deterministic audit-nodes on the `f` plane via the existing serializing append (reuse B1/B4 machinery) — NOT through the proposal/Senate path. Position: reuse the append; flags never enter the antechamber/Senate flow. Confirm.
2. **Schema touch?** B1 already laid the flag plane. Position: B5 USES it, no schema change (no `schema_version` bump). State explicitly if you must touch the schema (then bump + carry in fold/reconcile — M4).
3. **Severity (Session 6 hybrid):** emit a severity field — emergent `frequency × damage` as a **placeholder** + a small fixed floor for categorically-critical cases. Position: structural tripwires emit a minimal placeholder severity; the real metric is the parked measurement lane (do not build calibration). Confirm minimal.
4. **Flag resolution write:** status is DERIVED (no hot-path human clearing); the resolution WRITE (a `resolves` edge) reuses the B4 write path / a retro-sweep. Position: B5 builds emission + derived open/resolved READ; resolution-write reuses B4. Confirm boundary.
5. **Idempotency / re-run:** running the audit twice must not duplicate flags for the same standing condition. Position: a flag is keyed to (target, tripwire-type) so a re-run updates/no-ops rather than piling duplicates. Confirm the dedup rule.

## Test & verification contract (binding — A10/A11/A12/A16/A17)
- **Fixtures (A16):** deliberately-broken nodes — an orphan, a `lesson` missing its `about` edge, a node with > K `relates-to`; plus a clean graph that must produce ZERO flags (no false positives). Disposable-instance only (A12; canonical init index-only per A19).
- **e2e (A17):** **complete the L1 vertical slice** — B5 is the last surface, so the full scenario now runs fold → query → propose → gate → ingest → **audit** → reconcile, asserting the audit leg + that a clean graph stays flag-free. Extend the L2 subprocess session with an `audit` invocation.
- **Evidence (A11):** delivery-note §4 verbatim `receipt:` (decisive `Ran N tests … OK`), full suite **≥5× consecutively** with the count, Python + SQLite versions.
- **DoD (Starter A + A10/A11):** scope built · fixtures green vs a disposable instance · 08-B5 delivery note · checkpoint comment drafted. The master then runs the A10 critical re-test (incl. the completed vertical slice) and a roundtable if gaps appear, then the independent Probator Phase-1 exit check follows.

## FILES (expected — confirm in the plan)
  warehouse_robot/audit.py: NEW — the three tripwires + flag-node emission (append-only, flag-only)
  warehouse_robot/cli.py: NEW `audit` subcommand (flag-only output; structured JSON)
  warehouse_robot/schema.py: only if the flag plane needs extension (bump schema_version — M4); expected: no change
  warehouse_robot/fixtures/: NEW broken-node + clean-graph fixtures (A16)
  warehouse_robot/tests/: NEW audit tests + the COMPLETED L1 vertical slice + L2 audit step
  warehouse_robot/docs/: audit contract doc if a new agent-facing surface is introduced

## Scope fence — do NOT build (flag if found, per Law 1)
- The **periodic semantic / contradiction audit** — owner-driven (Session 6 Cluster B); NOT a B5 deterministic tripwire.
- **Code / convention freshness** (node ↔ external reality) — explicitly NOT a B5 tripwire (A14/L7); that is the owner-driven semantic audit + SAW-40. B5 stays purely graph-structural.
- The **promotion gate** (Cluster C) — it is calibrated BY the audit metric, but the gate itself is SAW-31.
- **Severity-metric calibration** — parked measurement lane.
- Any Foodoire content or migration (A1; M2 runs later).

## Changes Made

GREEN — full B5 scope delivered (Starter A; owner-approved by `engage`). See **08-B5 Delivery Note — Audit Tripwires: Orphan, relates-to Overuse & Missing-Recommended-Edge**. `warehouse_robot/audit.py` (the three tripwires + flag emission), a shared `append_node` ID-allocation primitive (PC1b Option A, behaviour-preserving), the `audit` CLI subcommand, the `fixtures/audit/` set, `AUDIT_PROTOCOL.md`, and 26 new tests; the L1 vertical slice is complete and the L2 subprocess session carries an audit leg. 241/241 tests green, 5× consecutively (Python 3.9.6 / SQLite 3.51.0); no schema change. Awaits the master A10 re-test + the independent Probator exit check.
