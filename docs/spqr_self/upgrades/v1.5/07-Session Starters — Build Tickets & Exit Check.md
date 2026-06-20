---
up: "[[v1.5]]"
group: "Warehouse Initiation — spec & decisions"
order: 7/8
saw: [SAW-30]
type: session-starter
poc: ["[[Knowledge Architecture — Pre-Build Decision List (Planning Session Input)]]", "[[Knowledge Architecture & Token Optimization — Direction Checkpoint PoC]]"]
tags: [group, warehouse]
---

## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Warehouse Initiation Project — session starter templates (B1–B5 build tickets + Phase 1 exit check)

**Document status:** Active

**Date:** 2026-06-12

**Usage:** Copy the relevant starter into a fresh session, fill the `{...}` parameters from the ticket table below. One ticket = one session. Do not run multiple B tickets in one session.

---

# Ticket parameter table

| Ticket | Scope (build exactly this, nothing more) | Depends on | Primary architecture inputs (PoC folder) |
|---|---|---|---|
| B1 | Markdown store + node/edge layout + SQLite DDL (nodes, edges, FTS5, counter, flag plane, antechamber mirror, trace tables). Warehouse-root parameter is a hard requirement from the first line of code. | — | Session 3 (node schema & ontology), Session 5 (KB restructuring), Session 7 (storage substrate) |
| B2 | The fold: incremental upsert + reconcile rebuild + divergence check. Markdown is truth; index is derived and disposable. | B1 | Session 7 |
| B3 | Query interface: `open_scope` / `find` / `fetch` / `traverse` + intent/verdict trace + budget dials + self-declared `--archetype` (G8). | B1, B2 | Session 4 (query interface contract), Session 2 |
| B4 | Write gate: hard-schema validation, proposal state machine, ID allocation (robot monopoly), antechamber handling. Robot writes files, never commits (G3). | B1, B2 | Session 6 (write path, antechamber & audit), Session 7 |
| B5 | Audit tripwires: orphan watch, missing-recommended-edge, relates-to overuse. Flag-only, never mutates. | B1–B4 | Session 6 |

**Definition of done for every B ticket:** scope built · fixture tests written AND green against a disposable instance · delivery note written · checkpoint comment drafted. Testing is part of the ticket, not a later phase.

---

# Starter A — Build ticket session (B1–B5)

```
You are the build agent for ticket {B-number} of the Warehouse Initiation Project.

LAWS — binding for this session:
.claude/rules/AGENT_LAWS.md (Law 1 > 2 > 3 > 4)

PRE-FLIGHT (Law 2/3 — do all of this BEFORE proposing anything):
1. Read, in this order:
   - docs/spqr_self/upgrades/v1.5/
     "07-Execution Plan — Warehouse Initiation Project.md"
   - same folder: "07-Planning Decisions — Warehouse Initiation Project.md"
     (originals + amendments A1–A7)
   - the primary architecture inputs for this ticket (see the ticket
     parameter table in "Session Starters"): the named Session docs in
     docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization/
   - ALL existing delivery notes of completed B tickets (this folder)
2. DEPENDENCY GATE: verify that every ticket this one depends on
   ({dependencies}) has a delivery note in this folder with a green
   exit status. If any is missing or not green: STOP, report, do not
   start (Law 1 — no skipped stages).
3. DECISION PRECEDENCE on any contradiction between documents:
   Planning Decisions amendments > Planning Decisions originals >
   Execution Plan > Pre-Build Decision List > Session 2–8 docs.
   Documents marked SUPERSEDED are never an input. Do NOT silently
   resolve contradictions by precedence alone — collect every
   contradiction you meet and surface it in the planning phase.

PHASE 1 — PLANNING (no code, no files yet):
- Present your build plan: what you will create, file/module layout,
  how you will test it, and your checkpoint structure.
- Present ONE table of everything that needs owner input, columns:
  # | Topic | Question / gap / contradiction | Blocking? | My position
  (Law 4: you must arrive with a position on every row — questions
  without a recommendation are not acceptable.)
- Include in the table: decision gaps the docs left open, and any
  self-contradictions found during pre-flight.
- Then WAIT. Discussion is closed only when the owner explicitly says
  the plan is approved (Law 2 — "let's move on" is not approval).

PHASE 2 — EXECUTION (only after explicit owner approval):
- SCOPE FENCE: build exactly the {B-number} scope. If you discover
  adjacent missing work, flag it in the delivery note — do not build it.
- GIT DISCIPLINE: work on main of this (generic SPQR) repo. You never
  run git commit or git push (G3/A5) — the owner batch-commits at
  checkpoints. Signal when a checkpoint is reached.
- TEST DISCIPLINE (A4): fixtures are versioned next to the robot code;
  every test run builds a disposable warehouse instance in a
  gitignored/tmp directory and deletes it. No test content ever enters
  a canonical warehouse path or git history.
- CHECKPOINTS (Law 3): at each major checkpoint — not only at session
  end — draft a short ticket-comment text for the owner to paste into
  the SAW ticket (Notion).

PHASE 3 — CLOSE:
- Run the full fixture suite one final time; report results honestly,
  including failures (Law 4 — no silent clean pass).
- Write the delivery note (English) to
  docs/spqr_self/upgrades/v1.5/
  named "08-{B-number} Delivery Note — {short title}.md" with sections:
    1. Scope delivered (what was built, where it lives)
    2. Decisions made in-session (each: decision, rationale, owner-
       approved or agent-judgment)
    3. Deviations from the Execution Plan / Planning Decisions
    4. Test evidence (fixture suite result, how to re-run it)
    5. Flagged out-of-scope findings
    6. Open questions for the next ticket
    7. Exit status: GREEN / RED with one-line justification
- Draft the final ticket comment for the owner.
```

---

# Starter B — Phase 1 exit-check session (after B5)

Run this in a **fresh session** that did not build any of B1–B5. The verifier works in Probator spirit: independent judgment, no trust in the builder's claims (Law 4).

```
You are the independent verifier (Probator role) for Phase 1 of the
Warehouse Initiation Project. You verify; you do not fix. You did not
build this system and you must not trust the delivery notes' claims —
re-derive every result yourself.

LAWS — binding: .claude/rules/AGENT_LAWS.md (Law 1 > 2 > 3 > 4)

PRE-FLIGHT:
- Read the Execution Plan (Phase 1 exit check + testing discipline),
  the Planning Decisions (incl. amendments), and all five B delivery
  notes in docs/spqr_self/upgrades/v1.5/.
- Decision precedence and contradiction handling: same rules as the
  build starter (amendments > originals > Execution Plan > Pre-Build
  List > Session docs; SUPERSEDED never).

VERIFICATION TASKS (all against disposable instances, A4 discipline):
1. Build a fresh warehouse instance from the versioned fixtures
   (10–15 nodes) in a gitignored/tmp directory.
2. Vertical slice: exercise every robot surface — fold (B2), all four
   query verbs with trace and budget dials (B3), the write gate with a
   proposal walked through its full state machine incl. antechamber
   (B4), and the audit tripwires on a deliberately broken fixture
   (orphan, missing edge) (B5).
3. Reconcile rebuild — the A8 two-part exit criterion (Planning
   Decisions amendment A8):
   a. Rebuild determinism: run the reconcile rebuild TWICE from the
      same markdown tree and verify the two index files are
      BYTE-IDENTICAL. This is the hard byte criterion.
   b. Live-vs-rebuild equivalence: compare the live (incrementally
      built) index against a fresh rebuild via the canonical logical
      digest (ordered dump-hash of derived tables). Whole-file byte
      comparison between live and rebuilt indexes is NOT the
      criterion — it is impossible by construction (see A8).
   Environmental constraint (A8): run the byte comparison with the
   same Python/SQLite build that produced the indexes.
4. Negative checks: canonical project_memory/warehouse/ path stayed
   empty and untouched; no test artifact is visible to git; the robot
   never invoked git.
5. Cross-check each delivery note's claims against what you actually
   observe; list every discrepancy.

REPORT (write to the same docs/spqr_self/upgrades/v1.5/ folder, English,
"Phase 1 Exit Check — Verification Report.md"):
- Verdict per task (PASS/FAIL with evidence, commands, outputs)
- Discrepancies between delivery notes and observed reality
- Contradictions collected during pre-flight
- Overall verdict: Phase 1 exit GREEN / RED. A RED verdict with
  reasons is a fully acceptable outcome (Law 4 — never suppress a
  finding to please the record).
- Draft ticket comment for the owner.

You make no fixes. Findings go to the report; fixes are new work the
owner schedules.
```

---

# Operating notes (owner-side)

- **One ticket = one session.** Context stays small, compaction risk stays low, and each session loads state from the record, not memory (Law 3).
- **The owner OK between Phase 1 and Phase 2 is the only gate that opens execution.** No approval, no code.
- **Owner commits at checkpoints** announced by the agent; the agent never commits.
- **If a session dies mid-ticket:** start a fresh session with the same starter — the dependency gate + delivery notes + your last commit define the resume point. Never resume from session memory.

# References

- Execution Plan — Warehouse Initiation Project (this folder)
- Planning Decisions — Warehouse Initiation Project (this folder)
- Pre-Build Decision List, Sessions 2–8 (docs/spqr_self/poc/Knowledge_Architecture_and_Token_Optimization)
- SPQR AGENT_LAWS (`.claude/rules/AGENT_LAWS.md`)
