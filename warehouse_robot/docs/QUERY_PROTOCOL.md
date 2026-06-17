# Warehouse Query Protocol

**Component:** warehouse_robot — the query interface: four verbs, the intent/verdict bracket, budget dials and the consent-gate (B3, realizing the S4 contract).

**Status:** Active. This spec travels with the robot package at import (A2 plain copy).

---

## 1. Overview

The query path is **read-only against markdown**: the verbs read the derived SQLite index and write nothing back to it except trace rounds and grant-consumption bookkeeping. They never touch node files and never invoke git (G3).

Two phases, four verbs (S4):

| Phase | Verb | Purpose |
|---|---|---|
| Disambiguation | `open_scope` | Deterministic, scope-bounded feed — the **complete** slice or a facet breakdown, never a ranked truncation. |
| Disambiguation | `find` | The FTS5/BM25 finder side-door — rank-bounded top-N recall. |
| Retrieval | `fetch` | Bodies + edge TOC for explicitly selected ids. |
| Retrieval | `traverse` | Bounded typed-edge neighbourhood expansion, both edge directions. |

Plus two control verbs: `verdict` (closes a round) and `grant` (owner-issued one-shot consent).

Every verb is a per-call CLI command and a library function. Output is a JSON object on stdout with deterministic key order; errors go to stderr; the process exit code carries the outcome class (section 7).

## 2. The intent/verdict bracket (S4; planning #2)

Every verb call **opens a trace round** carrying its declared `intent`; `verdict` closes it. The bracket is enforced, not advisory:

- A new round is **refused while the session has an open round** (`ProtocolError`, "still open").
- An open round only ever blocks **its own session** — sessions are independent.
- `verdict` is **always** allowed against an open round, so there is no deadlock state.

The verdict vocabulary (S4):

- **Terminal** (closes the session): `FOUND-ENOUGH`, `ABSENT`, `FOUND-UNLINKED`.
- **Non-terminal** (round outcome, session continues): `WRONG-ENTRY`, `INSUFFICIENT-TRAVERSE`.

`intent` and `session` are mandatory non-empty strings on every round (K9). Both `session` and `--archetype` are **self-declared** (G8 honour-system; planning #1): abuse is visible in the trace as a retro watchpoint, not a prevented act.

## 3. Budget dials and the consent-gate (S4; planning #3, #4)

Budget is the "how much" dial; the DENY (section 4) is the "what not" dial. The **robot is the authoritative enforcer** — the per-archetype policy blocks in v1.5 agent files are usage instructions, never the enforcement source.

Usage is counted over the session's **current budget window**: all rounds after the boundary set by the last consumed grant. Default dials (placeholders awaiting retro calibration — they live in `policy.py`, one edit + reconcile away):

| Dial | What it caps | deliberate / execute / synthesize | consult | scrutinize |
|---|---|---|---|---|
| `altitude_ceiling` | skeleton rows one `open_scope` may return before it facets; also the `find` `top_n` upper bound | 50 | 50 | 50 |
| `wrong_entry_cap` | rounds ending `WRONG-ENTRY` per window | 3 | 3 | 3 |
| `traverse_cap` | rounds ending `INSUFFICIENT-TRAVERSE` per window | 3 | 3 | 3 |
| `max_depth` | depth of a single `traverse` call | 3 | 3 | 3 |
| `body_fetch_ceiling` | bodies fetched per window | 10 | **3** | **5** |

Per-call overrides may only **tighten** a dial; loosening raises `PolicyDenied` — a larger budget is exactly what the continuation grant exists for.

**Exhaustion** (a cap reached, or a session already closed by a terminal verdict) refuses the round and raises a `BudgetExhausted` carrying an **escalation packet** — `reason`, the `refused` call, `window_usage`, and the full `session_trace` — for the owner. A refused round is **not** a trace row; the packet is the record the agent must surface. Exhaustion is never a silent fail (S4 / Law 4).

A fresh window requires a **one-shot owner grant** (`grant` verb), consumed by the robot on the next round (consent-gate, never a cooldown). A grant for another session does not help. Grants are deliberately **not** carried over on reconcile rebuild — consent is fresh, re-issuing is cheap (planning #4) — and are excluded from the A8 logical digest. An outright over-ceiling single `fetch` is a `ProtocolError`, not a budget refusal: a grant could never admit it, so it must not consume one.

## 4. The SCRUTINIZE DENY (S4; planning #5)

The single true structural DENY. `scrutinize` (Tribunus, Probator, Curator) must be blind to the reasoning chain it is meant to re-derive:

- **Lineage + journey edge types** `supersedes`, `derived-from`, `about` are denied. `traverse` over them raises `PolicyDenied`; in `fetch` those edge-TOC rows are **hidden but declared** (`hidden_edge_types` in the response), never silently dropped (Law 4).
- `include_inactive` is denied to `scrutinize` (the superseded chain is lineage).

Every other archetype has no denied edge types and may opt into `include_inactive`.

## 5. Status visibility and the plane rule

- Status is the **derived** status (S3/S6 views): knowledge nodes are `active` / `superseded` (`v_effective_status`), flags are `open` / `resolved` (`v_flag_status`).
- Default visibility is **active/open only**. `include_inactive=true` is the explicit opt-in (denied to scrutinize).
- `fetch` by explicit id and `traverse` **ignore** the status filter by design — explicit selection and edge walking are deliberate acts, and the chain is the point of a traversal.
- **Plane rule:** queries address the knowledge plane unless `kind` is `flag`, which addresses the audit plane explicitly.

## 6. Verb response shapes

All responses include `verb`, `round_id`, and a `budget` snapshot (`{wrong_entry, traverse, bodies}` as `used/cap`).

- **`open_scope(scope?, kind?, include_inactive=false)`**
  - No `scope` and no `kind` → entry view: `{view: "scope-facets", facets: [{scope, count}...]}` (scopes ascending, the null bucket last).
  - Slice within the altitude ceiling → `{scope, kind, candidates: [skeleton...], count}` in **id order**.
  - Slice over the ceiling → `{overflow: true, count, ceiling, facets: [{kind, count}...] | null, guidance}` — facet, never truncate.
  - An empty slice is legitimate **ABSENT** evidence and is **never** auto-broadened (planning #7).
- **`find(text, kind?, scope?, top_n=8, include_inactive=false)`** → `{query, auto_broadened, dropped_filter, candidates: [skeleton...], count}` in **rank order** (BM25, id tiebreak). Text is tokenised and OR-quoted, which disarms FTS5 query syntax. Auto-broaden is the only robot-triggered round event and is strictly **one** deterministic step: only here, only by dropping `scope`. A `kind` filter is never dropped by the robot (planning #7).
- **`fetch(ids)`** → `{nodes: [{...full fields, body, edges:{out,in}}...], not_found: [...]}`. Edge TOC rows are neighbour **skeletons**, not bodies. Duplicate ids, an empty list, or a malformed id are `ProtocolError`.
- **`traverse(id, edge_type, depth=1)`** → `{origin, edge_type, depth, steps: [{level, from, direction, to}...], nodes: [skeleton...]}`. Each edge is reported once even when reachable from both ends.

A **skeleton** is `{id, title, kind, scope, status}` — never a body.

## 7. Exit codes (CLI)

| Code | Meaning |
|---|---|
| 0 | success |
| 1 | `budget-exhausted` — the JSON on stdout carries the escalation packet |
| 2 | any other error (`ProtocolError` / `PolicyDenied` / malformed input) — message on stderr |

`open_scope` / `find` / `fetch` / `traverse` run the cheap divergence check once per CLI invocation and **warn on stderr** if the index is stale; they never refuse on divergence (a stale read is degraded, not dangerous — B2 planning #10).

## 8. Trace format (the S7 measurement proxy)

One row per opened round in the `trace` table, carried over verbatim on reconcile rebuild (A8), excluded from the logical digest. Columns: `round_id, ts, session_id, ticket, agent, archetype, verb, intent, params, result_count, result_ids, verdict, budget`. `verdict` is `NULL` until the closing `verdict` lands. `params` and `budget` are canonical JSON (sorted keys).

## 9. Out of scope for this spec (owned by later tickets / parked)

- The write gate, proposal state machine and ID allocation — B4.
- Audit tripwire emission (orphan watch, missing-recommended-edge, relates-to overuse) — B5.
- Grant *issuance policy* (who/when/how the owner decides) and the Senate ingest-judgment path — v1.5 (G7/G4).
- The golden query set's growth into a full IR harness, dial calibration from retro data — parked lane.
