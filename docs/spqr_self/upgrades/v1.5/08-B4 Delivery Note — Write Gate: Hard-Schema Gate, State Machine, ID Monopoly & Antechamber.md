---
up: "[[v1.5]]"
group: "Warehouse Initiation — build (B1–B5)"
order: 8/8
saw: [SAW-30]
ticket: B4
status: green
tags: [group, warehouse, delivery]
---

## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Warehouse Initiation Project — B4 delivery note

**Ticket scope:** Write gate — hard-schema validation, the proposal state machine, ID allocation (the robot monopoly), antechamber handling + verdict application. Robot writes files, never commits (G3).

**Date:** 2026-06-20

**Session ID:** _(filled by the owner from the session record)_

**Model:** Opus 4.8 (claude-opus-4-8), Starter A (A9): plan-first → owner approval (`engage`) → execute.

**Dependency gate at session start:** B1 GREEN (65), B2 GREEN (95 cum.), B3 GREEN (171 cum.). Per A10 the prior suite was **re-run, not trusted**: 171/171 green locally before any B4 code. PASS.

---

# 1. Scope delivered

All B4 scope lives in the existing **`warehouse_robot/`** package:

| Item | Where it lives |
|---|---|
| Proposal codec (a node file minus the robot-stamped `id`/`timestamp`/`schema_version`) + the hard-schema gate (per-kind required fields decision→scope, constraint→source, lesson→agent+ticket; per-edge source-kind legality S3; node-format validity reused from the B1 codec via a placeholder node — zero churn to `store.py`) | `warehouse_robot/write_gate.py` (new) |
| Proposal state machine `proposed → rejected-malformed \| validated → auto-ingested \| pending-senate → ingested \| rejected \| revise`; `revise` re-enters at `proposed`, bounded to N rounds (placeholder dial = 3) → owner escalation; `auto-ingested` reachable-but-empty (promotion policy = SAW-31) | `warehouse_robot/write_gate.py` |
| ID allocation (the monopoly): at ingest, burns the node id from `id_counter` in its own committed txn (`SELECT`+`UPDATE`, never markdown-max), writes markdown (truth first), then folds via B2 `upsert_node_file` (idempotent counter re-touch) | `warehouse_robot/write_gate.py` `_ingest` |
| Antechamber handling: append-only content files (`<key>.md`, revisions `<key>.rN.md`) + a mutable `<key>.state.json` sidecar (lifecycle); the SQLite `antechamber` table maintained as a disposable mirror; node + edges appended at the serializing gate | `warehouse_robot/write_gate.py` |
| Antechamber↔mirror **reconcile + divergence** (the B2-analogue; mirror re-derived from the dir → survives an index **loss**, not just a rebuild — L4/R3) | `warehouse_robot/write_gate.py` `reconcile_antechamber` / `check_antechamber` |
| Verdict application (robot side): `resolve` applies `ingested`/`rejected`/`revise`; the Senate wake that issues the verdict is SAW-31 | `warehouse_robot/write_gate.py` `resolve` |
| CLI: `propose` / `revise` / `resolve` / `reconcile-antechamber`; `check` now also reports the antechamber; `init --disposable` writes the A12 test-instance gitignore | `warehouse_robot/cli.py` (extended) |
| Write-path error types | `warehouse_robot/errors.py`: `GateError`, `MalformedProposal`, `AntechamberError`, `RevisionLimitReached` |
| Versioned proposal fixtures (A16): 5 valid (one per kind + born-retired), 5 rejected-malformed (each rejection reason), 1 structural | `warehouse_robot/fixtures/proposals/` (new) |
| Write-path contract doc (travels at import; NODE_FORMAT/QUERY_PROTOCOL sibling) | `warehouse_robot/docs/WRITE_PROTOCOL.md` (new) |
| Test suite: **44 new tests** — codec/gate, state machine, antechamber, fixtures, CLI, L1 vertical slice, L2 subprocess | `warehouse_robot/tests/test_write_gate.py`, `test_state_machine.py`, `test_antechamber.py`, `test_write_fixtures.py`, `test_cli_write.py`, `test_vertical_slice.py`, `test_cli_session.py`, `_write_helpers.py` |

**No SQLite schema change** (D5): B1's `antechamber` table + 7-state enum already admit the full machine; `schema_version` stays **1**. `schema.py`, `config.py`, `store.py` are **untouched** — the whole B4 surface is one new module + additive extensions, keeping B1–B3 regression-proof.

# 2. Decisions made in-session

All rows below were presented in the Phase-1 plan table and **owner-approved by `engage`** (the 5 brief plan-calls D1–D5 + the contradictions/gaps D6–D15), except the one refinement explicitly marked **agent-judgment (deviation)** and carried in §3.

| # | Decision | Rationale | Authority |
|---|---|---|---|
| D1 | `auto-ingested` built **reachable-but-empty**: escalation predicate `_NEVER_AUTO`; a test injects a promoting predicate to ingest with no verdict | No dead DDL state (L6/R9); promotion policy is Cluster C / SAW-31 | Owner-approved |
| D2 | Built `reconcile_antechamber` + `check_antechamber` | The mirror is excluded from the A8 digest and not markdown-derivable; without this a corrupt/lost mirror is invisible (L4 blocker) | Owner-approved |
| D3 | Archetype-conditional antechamber **READ** policy **deferred to SAW-31** | B4 builds WRITE + mirror, not a new read verb; B3 ships canonical-plane-only | Owner-approved |
| D4 | `resolve` builds the **robot side** of verdict application; the Senate **wake** is SAW-31 | Two-stage write path boundary (S6) | Owner-approved |
| D5 | **No SQLite schema change**; revise-round derived (counted), not a column; write telemetry deferred | B1 antechamber table already complete; minimise blast radius (M4/A18) | Owner-approved |
| D6 | **A12↔A13 reconciled**: production `init` stays index-only (A13); the broad node+antechamber gitignore is written only by `init --disposable` (test instances) | A12 is test-isolation-scoped; broadening production `init` would gitignore the committed canonical truth (A13) | Owner-approved (overrides the brief's literal "extend INSTANCE_GITIGNORE") |
| D7 | Antechamber state = **mutable `.state.json` sidecar + append-only content**; mirror = projection | The antechamber is a queue (G7/G4); content stays append-only; simplest derivable model surviving index loss | Owner-approved |
| D8 | Proposal codec reuses the B1 codec via a placeholder node | Zero validation drift, zero churn to GREEN `store.py` | Owner-approved |
| D9 | ID burn via **`SELECT`+`UPDATE`** in the gate txn, not `RETURNING` | Identical semantics under the single-writer gate; no SQLite ≥3.35 dependency (A15 intent honoured, literal wording deviated) | Owner-approved |
| D10 | Proposal keys `<prefix>-p<n>` from the antechamber dir (separate namespace) | Proposal keys are not node ids; the A15 counter-monopoly governs node ids only | Owner-approved |
| D11 | New CLI command `resolve` (the existing `verdict` closes a query round) | Avoid surface collision | Owner-approved |
| D12 | revise reuses the key; revisions are new `<key>.rN.md`; bound 3 (placeholder), escalate at the bound | Append-only content + bounded loop (A15); B3 dial precedent | Owner-approved |
| D13 | `antechamber_root` **not persisted** in the manifest — see §3 (refinement of the approved "persist") | Agent-judgment (deviation) |
| D14 | Unparseable → raised at the door (exit 2, unpersisted); schema-invalid → persisted `rejected-malformed` (exit 1) | The state machine's `proposed→[hard-gate]→rejected-malformed` needs a persisted record; truly non-proposal-shaped input cannot be persisted | Owner-approved |
| D15 | No write-path query-trace rows; write telemetry is a **named** deferral (A18/L3/R8) | Trace is read-path only | Owner-approved |
| — | Edge source-kind table verified against all 14 B1 fixtures before locking (`resolves`/`relates-to` = any source; demo-n7 is a decision emitting `resolves`) | Avoid rejecting valid existing content; B1's "tighten without fixture churn" holds | Agent judgment |

# 3. Deviations from the Execution Plan / Planning Decisions

- **D13 — `antechamber_root` not persisted (refinement of the approved plan, Law 4).** In Phase 1 I recommended, and the owner approved, persisting `antechamber_root` in the manifest. While building I found the **default sibling resolution already equals the canonical A3 layout** (`project_memory/warehouse` + `project_memory/antechamber`), so persistence is dead weight that would also break the manifest's strict 3-key contract (a `config.py` change + B1 config-test churn). I therefore resolved the antechamber as: explicit `--antechamber-root` override, else the A3 sibling — **no manifest change**. This keeps `config.py` untouched. If a future instance needs a non-sibling antechamber, persistence is a one-amendment add. Flagged here per Law 4; revertible on request.
- **D6 — the brief's literal "extend INSTANCE_GITIGNORE" was not followed** (owner-approved in plan): doing so would gitignore the canonical committed truth (A13). The broad ignore is `init --disposable` only. Recorded as the A12↔A13 reconciliation.
- **D9 — A15's literal `UPDATE … RETURNING`** was implemented as `SELECT`+`UPDATE` in the gate txn (portability; identical semantics under the serialized writer). Owner-approved in plan.
- No scope additions; everything outside the B4 fence (§5) was flagged, not built.

# 4. Test evidence

- **Full suite: 215 tests, run 5× consecutively after CP3, 0 failures / 0 errors every run.** B1 65 + B2 30 + B3 76 + **B4 44**.
- **Verbatim receipt** (decisive stdout line, A11 — no paraphrase):
  ```
  Ran 215 tests in 10.640s

  OK
  ```
- **Environment:** Python **3.9.6** (macOS system interpreter); SQLite **3.51.0** (`sqlite3.sqlite_version`). _(B2/B3 receipts recorded Python only; the SQLite version is added here per A11/R11 so the exit-check can distinguish an environment mismatch from a determinism failure — A8.)_
- Re-run from the repo root: `python3 -m unittest discover -s warehouse_robot/tests -t .`
- Run only B4: `python3 -m unittest warehouse_robot.tests.test_write_gate warehouse_robot.tests.test_state_machine warehouse_robot.tests.test_antechamber warehouse_robot.tests.test_write_fixtures warehouse_robot.tests.test_cli_write warehouse_robot.tests.test_vertical_slice warehouse_robot.tests.test_cli_session`
- **Cross-B seam proven (A10):** `test_vertical_slice` threads the gate-allocated id (B4) → fold sees it (B2) → query reads it + demo-n1 derived-superseded (B3) → live digest == fresh rebuild (A8) → antechamber mirror re-derives clean.
- **ID monopoly proven:** allocation is `n13,n14,n15` from the counter (not markdown-max); a simulated crash-skip yields a **gap, never a collision** (S7); flag proposals allocate on the audit plane (`f3`).
- **Mirror survives index loss:** `test_antechamber` deletes the index, rebuilds nodes (B2) + re-derives the mirror from the antechamber dir (B4), states intact (L4/R3).
- **A16 fixtures:** all 11 proposal fixtures hit their expected outcome; all 5 valid fixtures ingest through the gate.
- **Isolation (A12):** every test builds a disposable instance (warehouse + antechamber sibling) under the system tmp dir and deletes it; `git status` shows only the intended deliverables — no `project_memory/`, index, or antechamber artifact reaches git. The robot never invoked git (G3).

# 5. Flagged out-of-scope findings (not built — Law 1 scope fence)

- **The auto-ingest promotion POLICY (Cluster C / SAW-31)** — the mechanism path is built and reachable; *which class* auto-ingests is empty by design.
- **The Senate wake / session-starter pending-check (G7/G4)** — SAW-31. `resolve` is owner-operated here.
- **Archetype-conditional antechamber READ** (SCRUTINIZE shielded / EXECUTE sibling-read / SYNTHESIZE delta, Session 6) — deferred to SAW-31 (D3).
- **Write-path telemetry / proposal-event log** (rejected counts, revise-depth, time-in-pending) — the named deferral (A18/L3/R8). The sidecar keeps the *current* state for derivability; it does not keep transition history.
- **B5 audit tripwires** (orphan / missing-recommended-edge / relates-to overuse) — next session; the `valid-flag` fixture only proves the gate *accepts* a flag, it does not *generate* one.
- **`kind` frozen-enum cost** (R7/L2): documented as deliberate in WRITE_PROTOCOL — a new kind is a seed-level schema bump (A2), not a content add. `constraint` already homes inherited conventions.

# 6. Open questions for the next ticket (B5 — audit tripwires)

1. **Flags are written through this gate.** B5 generates flag proposals; they ingest via `propose`/`resolve` exactly like knowledge nodes (the `valid-flag` fixture is the template). B5 should not open a second write path.
2. **B5 stays purely graph-structural (A14/L7).** Orphan = 0 in+out edges AND not origin-foundational; relates-to overuse = > K (K=5 placeholder); missing-recommended-edge from a per-kind table seeded with `lesson → about`. Numbers are placeholder dials (B3/B4 precedent).
3. **Audit reads the canonical plane; it does not read the antechamber.** Pending proposals are not yet knowledge.
4. **The exit-check (Starter B) must re-derive the antechamber mirror from the dir** (`reconcile-antechamber`) and assert `mirror == dir` after a full state-machine walk (R3), and record Python **+ SQLite** versions against the receipt (R11).

# 7. Exit status

**GREEN** — full B4 scope delivered: hard-schema gate, the complete proposal state machine (incl. bounded revise + reachable auto-ingest), the ID-allocation monopoly, append-only antechamber with a derivable mirror (reconcile + divergence), and robot-side verdict application; the A16 proposal fixtures and the travelling WRITE_PROTOCOL doc shipped; 215/215 tests green against disposable instances, 5× consecutively, with the L1 cross-B seam and an L2 subprocess session. No SQLite schema change; B1–B3 untouched and re-verified. Phase 1 still requires the independent verifier pass (Starter B / Probator) and the master A10 critical re-test — both separate sessions by design, not part of this GREEN.
