## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Warehouse Initiation Project — B3 delivery note

**Ticket scope:** Query interface — `open_scope` / `find` / `fetch` / `traverse` + intent/verdict trace + budget dials + self-declared `--archetype` (G8). Read-only against markdown; writes only trace and grant rows into the derived index.

**Date:** 2026-06-17

**Session note (honest record, Law 4):** The build ran in two passes. A Fable 5 session executed the pre-flight, the owner-approved Phase 1 plan, and checkpoints **CP1 (policy + query library API + DDL/fold extension)** and **CP2 (CLI surface + trace/verdict/budget/grant + DENY)** — both green (169 tests). That session ended at the end of CP2 when the `claude-fable-5` model became unavailable (owner limit reached), immediately after `test_cli_query.py` was written and the suite ran green. A resumed session (Opus 4.8) re-derived the state from the record (delivery notes + working tree + the green suite, per the Session Starters resume rule), reviewed the existing B3 tests clean-eye, and completed **CP3** (fixture query set, its harness, the protocol doc, this delivery note). No code from CP1/CP2 was rewritten; CP3 is purely additive.

**Dependency gate at session start:** B1 delivery note GREEN (65/65). B2 delivery note GREEN (95/95 cumulative). PASS.

---

# 1. Scope delivered

All B3 scope lives in the existing **`warehouse_robot/`** package:

| Item | Where it lives |
|---|---|
| Per-archetype query policy: 5 S4 archetypes, `QueryPolicy` dataclass (altitude / wrong-entry / traverse / max-depth / body-fetch dials + the SCRUTINIZE DENY), default dial table, `policy_for`, `tightened` (tighten-only) | `warehouse_robot/policy.py` (new) |
| The four verbs as a library API: `open_scope` (complete scope slice, kind/scope facets on overflow, scope-facet entry view), `find` (FTS5/BM25 top-N side-door, one-step scope auto-broaden), `fetch` (bodies + edge TOC for explicit ids), `traverse` (bounded both-direction typed-edge walk). Plus `verdict` (closes a round) and `issue_grant` (one-shot consent). Trace writing, budget windowing, the consent-gate and the escalation packet | `warehouse_robot/query.py` (new) |
| CLI subcommands `open-scope` / `find` / `fetch` / `traverse` / `verdict` / `grant`, all with mandatory `--warehouse-root` + `--archetype` + `--intent` + `--session`; JSON on stdout; exit 0/1/2; check-on-open warns on stderr | `warehouse_robot/cli.py` (extended) |
| `trace` gained a `session_id` column (+ index); new `grants` table (one-shot continuation grant) | `warehouse_robot/schema.py` (extended) |
| `_TRACE_COLUMNS` updated to carry `session_id`; `grants` deliberately NOT carried over on rebuild and NOT in the logical digest (A8 untouched, B2 open-question #2 honoured) | `warehouse_robot/fold.py` (extended) |
| `QueryError` / `ProtocolError` / `PolicyDenied` / `BudgetExhausted` (the last carries the escalation packet) | `warehouse_robot/errors.py` (extended) |
| Query-protocol contract doc travelling with the package (NODE_FORMAT.md sibling) | `warehouse_robot/docs/QUERY_PROTOCOL.md` (new) |
| Fixture query set (A4 — the debt rolled since B1): 26 queries → verb + params + expected id set, with optional `not_found` / `auto_broadened` / `view` checks | `warehouse_robot/fixtures/queries.json` (new) |
| Test suite: 76 new tests — `test_policy.py`, `test_query_openscope.py`, `test_query_find.py`, `test_query_fetch_traverse.py`, `test_trace_budget.py`, `test_cli_query.py`, `test_query_fixtures.py` | `warehouse_robot/tests/` (new) |

# 2. Decisions made in-session

All twelve planning-table rows were owner-approved (with the clarifications below). Recorded here so the next ticket need not re-derive them.

| Decision | Rationale | Authority |
|---|---|---|
| Budget is accounted over a self-declared `--session` (the SPQR session id); new `session_id` column on `trace`; window = the session's rounds after the last consumed grant | Per-call CLI (G1) has no implicit session; the trace needs an explicit grouping key | Owner-approved (#1). Session id is self-declared (G8-analogue honour-system); abuse is trace-visible — a retro watchpoint |
| Verdict is a separate `verdict` subcommand closing the latest open round; a new round is refused while one is open, in the same session only; `verdict` is always allowed (no deadlock) | The intent-before/verdict-after bracket must be deterministically enforced or the trace (S7 proxy) is holed | Owner-approved (#2), explicitly covered by tests |
| Default dials are placeholders in `policy.py` (altitude 50; wrong-entry 3; traverse 3; depth 3; body-fetch 10, consult 3, scrutinize 5); per-call tighten-only | Numbers are pre-calibration; the retro lane sets the real values | Owner-approved (#3) |
| B3 builds the full consent-gate: exhaustion → refusal + escalation packet; `grant` subcommand writes a one-shot grant; rebuild does not carry grants; grants excluded from the digest | Consent is fresh and cheap to re-issue; v1.5 (G7/G4) hangs the issuance policy off this mechanism | Owner-approved (#4) |
| SCRUTINIZE DENY is edge-structural: `traverse` over `supersedes`/`derived-from`/`about` denied; `fetch` hides those TOC rows but declares them (`hidden_edge_types`); `include_inactive` denied to scrutinize | S4 — scrutinize must be blind to the lineage it re-derives; hiding is never silent (Law 4) | Owner-approved (#5) |
| Overflow facets by kind within the scope; `open_scope` with neither scope nor kind returns the scope-facet entry view; hierarchical scope flagged as future work | The scope vocabulary is flat (S3/S5); faceting is the deterministic altitude entry | Owner-approved (#6) |
| Auto-broaden is exactly one deterministic step, **only in `find`, only dropping `scope`**; `find` never drops `kind`, and `open_scope` never auto-broadens (an empty slice is legitimate ABSENT) | "Minimal robot trigger": dropping scope is a safe recall widening; dropping kind changes the question's meaning — that is agent judgment | Owner-approved with agent extension (#7, see section 3) |
| Default visibility is active/open; `include_inactive` opt-in; `fetch`-by-id and `traverse` ignore the status filter | S4 — explicit selection and edge walking are deliberate; the chain is the point of a traversal | Owner-approved (#8) |
| JSON object on stdout (deterministic key order); errors on stderr; exit 0 ok / 1 budget-refusal / 2 error | The consumer is an LLM agent | Owner-approved (#9) |
| Cheap divergence check once per CLI invocation, warn on stderr, never refuse | A stale read is degraded, not dangerous; refusal would block reads during the crash window the reconcile exists to heal (B2 #10) | Owner-approved (#10) |
| `--archetype` mandatory on all four verbs, only the 5 S4 values, no bypass value | The trace is the measurement proxy; anonymous queries would hole it | Owner-approved (#11) |
| Fixture query set as `fixtures/queries.json`, run as tests; the parked golden-set / IR-harness seed | A4 deliverable; one row = verb + params + expected id set | Owner-approved (#12) |
| Text tokenised and OR-quoted before hitting FTS5 (`"tok" OR "tok"`) | Recall-oriented finder (S7); quoting also disarms FTS5 query syntax (injection-safe) | Agent judgment |
| `BudgetExhausted` from an over-ceiling single `fetch` is instead a `ProtocolError` and consumes no grant | A grant could never admit it; consuming one would waste consent | Agent judgment |
| Fixture-set assertions compare the **set** of surfaced ids (order is the unit tests' job; the golden set guards recall/precision) | Avoids duplicating the order assertions; makes the set a clean recall contract | Agent judgment (CP3) |

# 3. Deviations from the Execution Plan / Planning Decisions

- **Auto-broaden — agent extension on #7 (Law 4).** The owner approved "auto-broaden drops scope only, one step", clarifying that dropping `kind` is an explicit agent re-query. Building it, I carried that principle one step further than the literal note: `open_scope` does **not** auto-broaden at all (its empty slice is legitimate ABSENT evidence), and `find` drops **only** scope, never kind. Flagged at approval time; the owner can revert to an `open_scope` kind-drop with a one-line change if that was the intent.
- **No mid-checkpoint ticket comments were posted during the Fable pass.** The session ran CP1→CP2 without pausing to draft the per-checkpoint comments the plan calls for (Law 3 record gap). Mitigated: this delivery note plus the closing comment carry the full record, and the suite was green at the break. Noted so the owner can backfill the Notion checkpoint trail if wanted.
- No scope additions. Everything outside the B3 fence (section 5) was flagged, not built.

# 4. Test evidence

- **Full suite: 171 tests, run 5× consecutively after CP3, 0 failures / 0 errors every run** (Python 3.9.6, macOS system interpreter, 2026-06-17). Breakdown: B1 65 + B2 30 + B3 76 (74 verb/policy/trace/CLI tests + 2 fixture-set tests).
- During the clean-eye review the prior B3 suite (169 tests, pre-CP3) was also run 10× with no flakes, specifically to rule out a repeat of the B2 byte-determinism flake class.
- Re-run from the repo root: `python3 -m unittest discover -s warehouse_robot/tests -t .`
- Run only the fixture query set: `python3 -m unittest warehouse_robot.tests.test_query_fixtures`.
- All tests build disposable instances under the system tmp directory and delete them (A4). The `traverse` depth-chain test mints an extra node **inside its disposable instance only**, never in `fixtures/` or git. `git status` shows only the intended deliverables.
- Coverage highlights: bracket enforcement incl. the no-deadlock invariant (#2); budget windows, the one-shot grant lifecycle, terminal-verdict closure, cross-session isolation; the escalation packet contents; the SCRUTINIZE DENY on both `fetch` (declared hiding) and `traverse`; overflow→faceting vs. truncation; one-step scope auto-broaden; FTS5 syntax disarmament; `top_n`/`depth` bool-rejection; index discipline (query traffic leaves the logical digest unchanged, trace survives rebuild, grants do not).

# 5. Flagged out-of-scope findings (not built — Law 1 scope fence)

- **Grant issuance policy is mechanism-only here.** `issue_grant` writes a one-shot grant; *who decides and when* is v1.5 (G7/G4). The CLI `grant` subcommand is owner-operated by design.
- **Hierarchical scope / sub-scope faceting** is not modelled — the scope vocabulary is flat (S3/S5). Overflow facets by `kind` within a flat scope. A future enhancement if scope grows a hierarchy.
- **Dial calibration is deferred.** All numbers are pre-retro placeholders in `policy.py`; the parked measurement lane sets the real values from trace data (SAW-27 telemetry consumes the S4 trace).
- **The golden query set is a seed, not an IR harness.** It asserts exact recall against the fixtures; precision/recall *metrics* over a larger corpus are the parked IR-harness lane.
- **Dangling edge targets** surface as `{missing: true}` neighbour skeletons (a B5 audit signal), not an error — consistent with B2's "fold is a mechanism, not a gate".

# 6. Open questions for the next ticket (B4 — write gate)

1. **Trace/grant on a gated write?** B3 writes trace + grants on the read path. B4's proposal state machine and antechamber are a separate write surface; confirm B4 does not need to emit trace rounds (the query trace is read-path only) — likely yes, but state it.
2. **ID allocation vs. the `id_counter` invariant.** B2's upsert advances `id_counter` to `max(next_value, number+1)`; B4 owns the allocation monopoly (S7). B4 must allocate from the counter, never from markdown max, and the antechamber mirror must not perturb it.
3. **Antechamber visibility from queries.** Should any verb ever see antechamber (pending) nodes? Current B3 answer: no — queries read the canonical knowledge/audit planes only. Confirm at B4, since the antechamber mirror table now coexists with the trace/grants tables.
4. **`status: retired` write path.** B3 reads derived status (`v_effective_status`) where stored `retired` wins over derived `superseded`; B4 is the only writer that can set `retired`. Confirm the gate's retire path.

# 7. Exit status

**GREEN** — full B3 scope delivered (four verbs + bracket + budget dials + consent-gate + SCRUTINIZE DENY + self-declared archetype/session); the A4 fixture query set and the travelling protocol doc shipped; 171/171 tests green against disposable instances, 5× consecutively. The build resumed cleanly across a model-availability break with no rework, and the record (this note + the closing comment) carries what the missing mid-checkpoint comments would have. Phase 1 still requires the independent verifier pass (Starter B / Probator) — that is a separate session by design and is not part of this GREEN.
