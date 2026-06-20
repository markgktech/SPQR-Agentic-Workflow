---
up: "[[v1.5]]"
group: "Warehouse Initiation — build (B1–B5)"
order: 8/8
saw: [SAW-30]
ticket: B5
status: green
tags: [group, warehouse, delivery]
---

## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Warehouse Initiation Project — B5 delivery note

**Ticket scope:** The audit layer — three deterministic, graph-structural tripwires (orphan / relates-to overuse / missing-recommended-edge) that ONLY flag, never mutate; flag-node emission on the separate audit plane with derived open/resolved status; idempotent re-run. The last warehouse build (B5 of B1–B5).

**Date:** 2026-06-20

**Session ID:** _(filled by the owner from the session record)_

**Model:** Opus 4.8 (claude-opus-4-8), Starter A (A9): plan-first → owner approval (`engage`) → execute.

**Dependency gate at session start:** B1 GREEN (65), B2 GREEN (95 cum.), B3 GREEN (171 cum.), B4 GREEN (215 cum.). Per A10 the prior suite was **re-run, not trusted**: 215/215 green locally before any B5 code (Python 3.9.6 / SQLite 3.51.0 — exact match to the B4 receipt). PASS.

---

# 1. Scope delivered

All B5 scope lives in the existing **`warehouse_robot/`** package:

| Item | Where it lives |
|---|---|
| The three tripwires (pure reads over the derived index): **orphan** = active knowledge node with 0 incident *knowledge-plane* edges, excl. foundational; **relates-to overuse** = src of > K=5 `relates-to` edges; **missing-recommended-edge** from a per-kind table seeded `{lesson: (about,)}`. Plus dedup, flag emission, heat census, the `audit()` orchestrator | `warehouse_robot/audit.py` (new) |
| **Shared `append_node` primitive** (PC1b Option A): the single ID-allocation path — `_burn_id` + write markdown + fold — extracted from `write_gate._ingest`; the gate **and** the audit both mint here (literal ID-monopoly, one code path) | `warehouse_robot/write_gate.py` (`append_node`, `_burn_id`; `_ingest` now calls it) |
| CLI `audit` subcommand: flag-only JSON on stdout; warn-on-divergence; exit 0 clean / 1 findings / 2 error | `warehouse_robot/cli.py` (extended) |
| `AuditError` (the audit cannot run — e.g. no derived index; the tripwires themselves never fault on a finding) | `warehouse_robot/errors.py` (extended) |
| Versioned audit fixtures (A16): `clean/` (3 connected nodes → zero flags) + `broken/` (orphan demo-n4, lesson-missing-about demo-n5, relates-to over-user demo-n6, + 2 clean targets demo-n7/n8) | `warehouse_robot/fixtures/audit/` (new) |
| Audit-contract doc travelling at import (NODE_FORMAT / QUERY_PROTOCOL / WRITE_PROTOCOL sibling) | `warehouse_robot/docs/AUDIT_PROTOCOL.md` (new) |
| Test suite: **26 new tests** — tripwire units, fixture-set pins, CLI; plus the **completed L1 vertical slice** and the **L2 subprocess session** extended with an `audit` leg | `warehouse_robot/tests/test_audit.py`, `test_audit_fixtures.py`, `test_cli_audit.py`, `_audit_helpers.py`, `test_vertical_slice.py` (completed), `test_cli_session.py` (extended) |

**No SQLite schema change** (PC2): B1's flag plane — `kind: flag`, `flag_type`, plane `f`, the `flags`/`resolves` edges, `v_flag_status` — already admits the full audit layer. `schema_version` stays **1**; `schema.py`, `config.py`, `store.py`, `fold.py`, `query.py` are **untouched**. The only prior-module change is the behaviour-preserving `write_gate` refactor (§3).

# 2. Decisions made in-session

All rows were presented in the Phase-1 plan table (the 5 brief plan-calls PC1–PC5 + my independent findings G-A…G-E + the PC1b code-structure call) and **owner-approved by `engage`**, except items explicitly marked agent-judgment.

| # | Decision | Rationale | Authority |
|---|---|---|---|
| PC1 | Flags emit via the serializing **append**, NOT the antechamber/Senate flow | A deterministic tripwire needs no semantic judgment; routing flags through the antechamber would pollute the proposal queue (G6/G7). Reconciles B4-openQ#1 ("flags ingest like nodes") with the B5 brief ("never enter the Senate flow"): reuse the **primitive**, not the proposal flow | Owner-approved |
| PC1b | **Option A** — extract a shared `append_node` from `_ingest`; gate + audit mint through it | One ID-allocation code path keeps the monopoly (A15) literal; behaviour-preserving (the B4 suite re-ran 215/215). Recommended over Option B (duplicate the burn → a second allocation site) | Owner-approved (my recommended position) |
| PC2 | **No schema change**; `schema_version` stays 1 | B1's flag plane already complete; minimise blast radius (M4) | Owner-approved |
| PC3 | **Minimal placeholder severity** in the flag **body** (small fixed floor per tripwire), not a column | Honours PC2 (no DDL); the real `frequency × damage` metric is the parked measurement lane (S6 hybrid) | Owner-approved |
| PC4 | B5 builds **emission + derived open/resolved READ** only; the resolution **write** (a `resolves` edge) reuses B4 / a retro-sweep | The two-stage write-path boundary (S6); resolution is not a hot-path act | Owner-approved |
| PC5 | Dedup key = **(target, flag_type)**; emit only if **no OPEN flag** of that type targets the node; a **resolved** flag does not block re-emission | Idempotent re-run, never a duplicate; a condition that recurs after resolution is a real new finding | Owner-approved |
| G-A | Orphan counts **knowledge-plane edges only** — `flags`/`resolves` excluded | Else flagging would "heal" the orphan and a flagged orphan (demo-n11, whose only edge is the inbound `flags` edge) could never be re-detected. Empirically validated against the demo graph | Owner-approved (definition-level) |
| G-B | **Foundational = `origin: inherited`** | No `foundational` field exists; inherited = platform axioms (Apple HIG / Swift naming) that legitimately stand alone. demo-n12 is the proof fixture | Owner-approved |
| G-C | relates-to overuse counts the **source** (the edges a node declares) | "Carrying" = the node's own frontmatter edges; the flag is attributable to the author | Owner-approved |
| G-D | Tripwires watch the **live** (active/open) graph; retired/superseded excluded | Consistent with B3's default visibility; a superseded node carries an inbound `supersedes` edge anyway, a retired node is deliberately dead | Owner-approved |
| G-E | `audit` exit **0 clean / 1 findings / 2 error**, warn-on-divergence, never refuse | Mirrors `check` so the audit is usable as a CI/retro gate; a stale read is degraded, not dangerous (B2 #1) | Owner-approved |
| — | `AuditError` added; emission in deterministic **(flag_type, target)** order (stable f-ids + rebuild digest); audit fixtures in a **`fixtures/audit/` subdir** (never globbed by the demo-wide fold tests); severity floor values medium/low/low | Per-surface error convention; determinism for the A8 digest; isolation of broken fixtures from B1–B4 tests | Agent judgment |

# 3. Deviations from the Execution Plan / Planning Decisions

- **The Option A refactor touched the GREEN B4 module `write_gate.py`** — a deviation from the B1–B4 "prior modules untouched" pattern (flagged here per Law 4). It is the deliberate, owner-approved (PC1b) honouring of the literal ID-monopoly: rather than a second id-burn site in `audit.py`, the burn→write→fold core was extracted into one shared `append_node` that both `_ingest` and the audit call. **Behaviour-preserving:** the full pre-B5 suite re-ran **215/215 identical** after the refactor. One incidental change: the unreachable "id_counter has no row" guard now raises `GateError` (the shared parent) instead of `AntechamberError` (which would be semantically wrong on the audit path); no test exercises that corrupt-instance path.
- **No scope additions.** Everything outside the B5 fence (§5) was flagged, not built. B5 stayed purely graph-structural.

# 4. Test evidence

- **Full suite: 241 tests, run 5× consecutively at close, 0 failures / 0 errors every run.** B1 65 + B2 30 + B3 76 + B4 44 + **B5 26** (18 tripwire units + 3 fixture-set pins + 5 CLI; the L1 slice and L2 session were *completed/extended*, not added).
- **Verbatim receipt** (decisive stdout line, A11 — no paraphrase):
  ```
  Ran 241 tests in 3.443s

  OK
  ```
- **Environment:** Python **3.9.6** (macOS system interpreter); SQLite **3.51.0** (`sqlite3.sqlite_version`) — matches the B4 receipt, so the A8 byte-determinism floor is unchanged.
- Re-run from the repo root: `python3 -m unittest discover -s warehouse_robot/tests -t .`
- Run only B5: `python3 -m unittest warehouse_robot.tests.test_audit warehouse_robot.tests.test_audit_fixtures warehouse_robot.tests.test_cli_audit warehouse_robot.tests.test_vertical_slice warehouse_robot.tests.test_cli_session`
- **L1 vertical slice COMPLETE (A17):** `test_vertical_slice` now threads the full chain — fold (B2) → query (B3) → propose → gate → ingest (B4) → **audit (B5)** → reconcile (B2) — asserting both B5 contract points: a clean post-ingest graph stays **flag-free** (zero emitted; demo-n11 skipped), then a gate-ingested orphan (demo-n14) is **flagged** (demo-f3), the re-run is **idempotent**, and the flag **survives a reconcile rebuild** with the live digest == a fresh rebuild (A8 part 2) and both projections clean. This is also the cross-B integration seam the master re-tests (A10).
- **L2 subprocess session extended (A17):** `test_cli_session` drives `python3 -m warehouse_robot audit` as a real process — the lone ingested decision is flagged as an orphan (exit 1), a re-run mints no duplicate, and `check` stays clean (the flag is canonical, folded markdown).
- **Empirically validated on the real demo graph:** orphan = knowledge-edges-only (demo-n11 detected despite its inbound flag edge), foundational exclusion (demo-n12 excused), idempotency (demo-n11's standing flag skipped) → a live audit emits **zero** new flags. The broken fixture set trips **exactly** orphan(n4)/missing(n5)/overuse(n6); the clean set trips nothing.
- **Isolation (A12):** every test builds a disposable instance under the system tmp dir and deletes it; `git status` shows only the intended deliverables — no `project_memory/`, index, node/flag, or antechamber artifact reaches git. The robot never invoked git (G3 — grep-confirmed: no `git`/`subprocess`/`os.system` in non-test package code).

# 5. Flagged out-of-scope findings (not built — Law 1 scope fence)

- **Periodic semantic / contradiction audit** — owner-driven (S6 Cluster B); NOT a deterministic B5 tripwire.
- **Code / convention freshness** (node ↔ external reality) — owner-driven semantic audit + **SAW-40**, explicitly NOT a B5 tripwire (A14/L7).
- **The promotion gate** (Cluster C) — calibrated *by* the audit metric, but the gate is **SAW-31**.
- **Severity-metric calibration** + the K dial + recommended-edge-table growth — the parked measurement / governance lanes. B5 ships placeholder severity and K=5; no calibration.
- **The flag-resolution WRITE path** (a `resolves` edge that closes a flag) — reuses the B4 gate / a retro-sweep (SAW-31). B5 builds only the derived open/resolved *read*.
- **in+out (hub) relates-to counting** — the calibration-time alternative to the src-count rule (G-C); not built.
- Any Foodoire content or migration (A1; M2 runs later).

# 6. Open questions for the next steps (exit-check / SAW-31)

1. **The Phase-1 exit-check (Starter B / Probator)** must run the audit on a deliberately-broken fixture (orphan + missing edge) per its task 2 — the broken set is `warehouse_robot/fixtures/audit/broken/` (folded on top of `clean/`); a fresh fold yields exactly orphan(demo-n4)/missing(demo-n5)/overuse(demo-n6). It should also confirm the audit-emitted flag survives the A8 reconcile rebuild.
2. **SAW-31 wires the audit into the SPQR flow:** when/who runs it (the session-starter pending-check is the natural hook), the resolution-write path (`resolves`), and the promotion gate that consumes the audit metric.
3. **Calibration is a retro/governance act:** K, the per-tripwire severity floors, and any growth of the recommended-edge table beyond `lesson → about` are owner-governed — the table grows by amendment, never by an agent inventing a rule.

# 7. Exit status

**GREEN** — full B5 scope delivered: the three deterministic graph-structural tripwires (orphan / relates-to overuse / missing-recommended-edge), flag-only and never mutating, emitting append-only audit-plane flag nodes through the single shared ID-allocation primitive with derived open/resolved status and (target, flag_type) idempotency; the `audit` CLI surface, the A16 fixture set, and the travelling AUDIT_PROTOCOL doc shipped; the **L1 vertical slice is complete** (fold→query→propose→gate→ingest→audit→reconcile, asserting both the audit leg and a flag-free clean graph) and the **L2 subprocess session carries an audit leg**. 241/241 tests green against disposable instances, 5× consecutively; no SQLite schema change; the only prior-module touch (the `write_gate` refactor) is behaviour-preserving and re-verified at 215/215. Phase 1 now requires the master A10 critical re-test and the independent Probator exit check (Starter B) — both separate sessions by design, not part of this GREEN.
