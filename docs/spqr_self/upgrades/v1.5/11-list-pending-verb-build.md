---
up: "[[v1.5]]"
group: "Warehouse — list-pending verb (wake backing; SAW-31 F5/#1)"
order: 11/11
saw: [SAW-31]
ticket: SAW-31
status: pending
type: brief
tags: [group, warehouse, build, brief]
---

# Group 11 — `list-pending` verb (the Senate-wake's backing; warehouse_robot code)

## Brief
GROUP:          Warehouse — `list-pending` verb (wake backing)
ORDER:          11/11 (code build; the G7/G4 wake's missing backing — SAW-31 F5/#1)
REPO:           SPQR (generic; warehouse_robot — B4 surface)
RUN_CONTAINER:  /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:        /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/11-list-pending-verb-build.md
RATIONALE:      The Senate session-start wake (G7/G4) must surface pending-senate proposals, but `check` only does divergence and no list verb exists — the wake silently misses the queue. Build the listing verb the wake needs. CODE + tests (Starter-A discipline), not a doc pass.
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md  (F5/#1) + the existing warehouse_robot patterns (do not re-architect)
FILL_CHANGES_MADE: yes
MODEL: Starter A — plan-first → surface any contradiction → owner approval → execute. Tests are mandatory.

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - warehouse_robot/write_gate.py   (check_antechamber, _iter_sidecars, the sidecar fields, _PROPOSAL_KEY_RE, the state constants STATE_*)
  - warehouse_robot/cli.py          (cmd_check + the subparser pattern; mirror its style exactly)
  - warehouse_robot/docs/WRITE_PROTOCOL.md   (the CLI section + state machine; keep this contract truthful)

DEPENDENCY GATE: warehouse build B1–B5 GREEN; the test suite green before you start (A10 — re-run, do not trust the token). STOP if red.

## Scope — build exactly this (one read-only listing verb + tests + the doc line)
- **`list_pending(warehouse_root, antechamber_root=None, state=None)`** in `write_gate.py`: iterate the antechamber **sidecars** (the truth, via `_iter_sidecars` — NOT the disposable mirror), return an ordered list of `{proposal_key, state, ticket, agent, created_at, content_file}`. Default returns the **live queue** — proposals NOT in a terminal state (exclude `ingested` / `rejected` / `rejected-malformed`); `state=<X>` filters to one state (the wake uses `pending-senate`). Deterministic order (by proposal-key number). Read-only — never writes, never mints anything.
- **`list-pending` CLI subcommand** in `cli.py` (mirror `cmd_check`): `--warehouse-root P [--antechamber-root P] [--state STATE]`. JSON on stdout: `{verb, count, pending: [...]}`. Exit 0 (a list, even empty, is success); exit 2 on robot error (no init). Hyphenated name, consistent with `open-scope` / `reconcile-antechamber`.
- **WRITE_PROTOCOL.md**: add `list-pending` to the CLI section; if the existing "`check` now also reports the antechamber" line overstates (check is divergence-only), correct it to point listing at `list-pending`.

## Test contract (binding — mirror the existing suite; A4 isolation)
- Fixtures: a disposable antechamber with proposals across states (`pending-senate`, `proposed`, `ingested`, `rejected`) — assert `list-pending` returns the live queue (excludes terminal), `--state pending-senate` returns exactly the pending-senate ones, an empty antechamber → `count: 0`, and order is deterministic. Disposable-instance only (A4); no canonical content.
- Evidence (A11): delivery-note verbatim `receipt:` (the decisive `Ran N tests … OK`), full suite ≥5× consecutively, Python + SQLite versions.
- DoD: scope built · tests green vs a disposable instance · WRITE_PROTOCOL.md updated · Changes Made filled. Master then runs the A10 critical re-test.

## Scope fence — do NOT do (flag if found, per Law 1)
- Do NOT touch the proposal-key RACE (`_allocate_key` lock/overwrite — F5/#3) here unless the owner folds it in — it is a separate CORRECTIO bug ticket. If you touch `write_gate.py` near it, FLAG it, do not fix silently.
- Do NOT change any existing verb, the state machine, the gate, or the id_counter monopoly. This is purely an additive read-only listing verb.
- Do NOT touch any agent/skill/retro doc (the session-starter re-point is the next, separate doc pass).

## Changes Made

### Dependency gate (A10 — re-run, not trusted)
Re-ran the full suite before any edit: **`Ran 241 tests in 11.178s · OK`** (Python 3.9.6, SQLite 3.51.0). B1–B5 GREEN confirmed. Proceeded.

### Built (additive, read-only — no existing verb / state machine / gate / id_counter touched)
1. **`warehouse_robot/write_gate.py`**
   - Added `TERMINAL_STATES = (rejected-malformed, auto-ingested, ingested, rejected)` next to the state constants. **Owner decision (2026-06-21):** exclude **all four** terminal states from the default live queue, per the brief's "NOT in a terminal state" semantics — the brief's prose enumerated only three but `auto-ingested` is equally a `_ingest` `final_state`. Live queue = the complement `{proposed, validated, pending-senate}`.
   - Added `list_pending(warehouse_root, antechamber_root=None, state=None)` + helper `_proposal_key_sort`. Iterates the **sidecars** via `_iter_sidecars` (the truth, NOT the disposable mirror); returns ordered `[{proposal_key, state, ticket, agent, created_at, content_file}]`. Default = live queue (excludes `TERMINAL_STATES`); `state=<X>` = exactly one state (wake passes `pending-senate`). Deterministic order by proposal-key **number** (lexical would mis-sort `p2` vs `p10`). `config.load_config` asserts an initialised root (→ exit 2 on no-init); `antechamber_root=None` resolves to the A3 sibling. Never writes, never mints.
2. **`warehouse_robot/cli.py`**
   - Added the hyphenated `list-pending` subparser (`--warehouse-root` / `--antechamber-root` / `--state`) + `cmd_list_pending`, mirroring `cmd_check` style. Emits `{verb, count, pending: […]}` JSON; **exit 0** for any list (empty included); robot error → exit 2 via `main()`.
3. **`warehouse_robot/docs/WRITE_PROTOCOL.md`**
   - Added the `list-pending` line to the CLI block + a paragraph (live-queue semantics, exit 0, ordering). **Corrected the overstated `check` line**: changed "now also reports the antechamber" → "antechamber **DIVERGENCE** only (dir vs mirror), not a listing" and pointed listing at `list-pending` (F5/#1: the wake doc had wrongly treated `check` as the lister).
4. **`warehouse_robot/tests/test_list_pending.py`** (new; disposable instance, A4)
   - Unit (8) + CLI (4): live queue excludes all terminals · `--state pending-senate` returns exactly the pending one · `--state` can address a terminal state · rows carry exactly the 6 contract fields · empty antechamber → `[]` / `count: 0` · **numeric-not-lexical order** across the p1/p10 boundary (11 proposals) · uninitialised root → `ConfigError` / CLI exit 2 · default antechamber resolves to the A3 sibling · CLI envelope shape.

### Test receipt (A11 — verbatim)
New file alone: `Ran 12 tests in 0.394s · OK`.
Full suite, **5× consecutive** (was 241 pre-change; +12 new = 253):
```
=== RUN 1 ===  Ran 253 tests in 4.048s   OK
=== RUN 2 ===  Ran 253 tests in 4.191s   OK
=== RUN 3 ===  Ran 253 tests in 4.111s   OK
=== RUN 4 ===  Ran 253 tests in 5.571s   OK
=== RUN 5 ===  Ran 253 tests in 4.898s   OK
```
Environment: **Python 3.9.6 · SQLite 3.51.0** (`python3 -m unittest discover -s warehouse_robot/tests -t .`).

### Scope-fence flag (Law 1 — found, NOT fixed)
**F5/#3 proposal-key allocation race is still present and untouched.** `_allocate_key` (`write_gate.py`, now ~line 314) is still `max+1` from the dir with **no lock**, and `propose` still `write_text`-overwrites the content file — two concurrent `propose` can collide and one clobbers the other. My change adds no locking and does not go near this path (read-only listing only). Flagged per the fence; it remains the separate owner-created CORRECTIO bug ticket.

### DoD
Scope built · tests green vs a disposable instance (5×) · WRITE_PROTOCOL.md updated · Changes Made filled. **Not committed** (G3/owner commits). Master to run the A10 critical re-test.
