---
up: "[[v1.5]]"
group: "Warehouse Cutover — final consistency amendment (SAW-31)"
order: 10-amend/10
saw: [SAW-31]
ticket: SAW-31
status: pending
type: brief
tags: [group, warehouse, cutover, brief, amendment]
---

# Group 10-amend — SAW-31 final consistency amendment (Codex findings #1/#3/#4/#6)

## Brief
GROUP:          Warehouse Cutover — final consistency amendment (SAW-31)
ORDER:          10-amend (single consolidated amendment from the Group-10 validation gate; validate-before-confirm)
REPO:           SPQR (generic)
RUN_CONTAINER:  /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:        /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/10-amend-saw31-final-consistency.md
RATIONALE:      Accuracy/wording reconciliations to the already-decided D2/D2c, surfaced by the independent Codex review at the Group-10 gate — folded into ONE pass (no piecemeal follow-ups). No new decision.
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md  (D2 final = agent-executes-on-owner-HITL; F4 findings)
FILL_CHANGES_MADE: yes

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md   (D2 final + F4)
  - warehouse_robot/write_gate.py  (states: propose returns `pending-senate`, not the transient `validated` — lines 436/448/451)
  - warehouse_robot/docs/QUERY_PROTOCOL.md  (§2 the intent/verdict bracket; §6 traverse takes ONE edge_type)

DEPENDENCY GATE: Groups 9/9b/9c/10 GREEN. STOP if any target line is absent (the files moved).

## Scope — accuracy/wording deltas ONLY (no behavior change; reconcile to final D2/D2c)

## FILES (6)
  docs/skills/ticket-comment.md (#1): the warehouse-write receipt EXAMPLE uses the transient `validated`; `propose` actually returns **`pending-senate`** (write_gate.py:448-451). Fix the example to the real returned state (e.g. `propose … → pending-senate <key>`); keep "decisive line copied from the CLI output" discipline. NOTE the CLI emits JSON — the receipt is the decisive state+key line, not a fabricated arrow if that misleads.
  docs/skills/warehouse-usage.md (#3): the "Session start (Senate): owner runs `check`/`audit`" line contradicts the doc's own who-runs-CLI matrix + final D2. Reword to **the Senate (agent) runs `check`/`audit` on the owner's session-open authorization** (agent-executed on owner HITL).
  docs/skills/warehouse-usage.md (#6): the semantic-audit how-to (section 2) must respect the **intent/verdict bracket** — each query verb opens a round and is closed with `verdict` before the next (QUERY_PROTOCOL §2); and use **real CLI args** — `traverse` takes ONE `--edge-type` per call (separate calls for supersedes / derived-from / about; NO `a|b|c` pipe syntax), not a single trailing verdict for a multi-verb chain.
  docs/agents/praetor.md (#4): line ~45 "the Senate judges and the OWNER executes the ingest" → "the Senate judges and, on owner HITL, runs `resolve` (the ingest); you never run `resolve`."
  docs/agents/quaestor.md (#4): line ~33 — same fix as praetor.
  docs/skills/warehouse-ingest.md (#4): lines ~11 + ~99 "the OWNER executes the ingest" / "owner-executed" → "the Senate executes `resolve` on owner HITL (owner consents, the Senate runs it)."
  docs/skills/censura-output.md (#4): line ~56 "the OWNER later executes the ingest" → "the Senate later runs `resolve` on owner HITL."

## Scope fence — do NOT do (flag if found, per Law 1)
- These 6 files ONLY, and ONLY the listed wording/accuracy deltas. Do NOT change any decided behaviour — D2/D2c stand; this only makes the prose match them.
- Do NOT touch the retro LESSONS.md / 10-entry-counter framing (#5a — deferred to the post-Group-10 residue sweep).
- Do NOT touch the ticket-comment `mode:` enum (#5b — pre-existing SAW-33-era gap, a separate housekeeping ticket).
- Do NOT add `resolve`/`grant` rights to any non-Senate agent; do NOT alter the SCRUTINIZE DENY or any query-policy core.

## Changes Made

Executed 2026-06-21. Six-file accuracy/wording reconciliation to final D2/D2c — no behaviour change. Dependency gate GREEN (every target line present). All four Codex findings (#1/#3/#4/#6) folded into this one pass.

**#1 — `docs/skills/ticket-comment.md`** (FIELD RULES → `receipt:` def)
- Receipt example `propose … → validated demo-k7` → `propose … → pending-senate demo-k7`. `validated` is the transient pre-escalation state; `propose` actually returns `pending-senate` (write_gate.py:448-451 — `_evaluate` sets `validated` then immediately advances to `STATE_PENDING_SENATE` as the returned state). Arrow `<command> → <state + key>` convention kept (consistent with the rest of the receipt discipline; the decisive state+key is what the CLI's JSON yields).

**#3 — `docs/skills/warehouse-usage.md`** (§3 cadence, session-start bullet)
- `owner runs check … and audit …, pastes the result` → `the Senate (agent) runs check … and audit … on the owner's session-open authorization (agent-executed on owner HITL), surfacing the result`. Removes the contradiction with the file's own who-runs matrix (line 33: audit = agent-executed) + final D2 (agents execute on owner HITL/consent, not owner keystrokes). `pastes` → `surfacing` (the agent runs it).

**#6 — `docs/skills/warehouse-usage.md`** (§2 semantic-audit how-to, step 1)
- Rewrote step 1 to respect the intent/verdict bracket (QUERY_PROTOCOL §2): each verb opens a round closed with `verdict` before the next — `open-scope` → `verdict`, then each `traverse` its own round closed with `verdict`.
- Real CLI args: `traverse … --edge-type supersedes|derived-from|about` (non-real pipe syntax) → three separate calls, **one `--edge-type` per call** (`supersedes`, then `derived-from`, then `about`) per QUERY_PROTOCOL §6 (`traverse(id, edge_type, depth)` takes ONE edge_type). Step 2 already closed its `fetch` round with a verdict — left as-is.

**#4 — stale "OWNER executes the ingest" → "the Senate runs `resolve` on owner HITL"** (D2 refinement: owner HITL = consent, the agent executes)
- `docs/agents/praetor.md` (WRITE PATH): `the Senate judges and the OWNER executes the ingest` → `the Senate judges and, on owner HITL, runs resolve (the ingest)`. The trailing `you never mint ids or run resolve` retained.
- `docs/agents/quaestor.md` (WRITE PATH): identical fix.
- `docs/skills/warehouse-ingest.md` PURPOSE (line ~11): `the Senate makes the semantic judgment, and the OWNER executes the ingest` → `the Senate makes the semantic judgment and executes resolve on owner HITL (owner consents, the Senate runs it)`.
- `docs/skills/warehouse-ingest.md` WHAT YOU NEVER DO (line ~99): `those are the Senate-judged, owner-executed privileged writes (D2)` → `those are privileged writes the Senate executes on explicit owner HITL (D2)`.
- `docs/skills/censura-output.md` (LESSON-NODE PROPOSAL, line ~56): `the OWNER later executes the ingest` → `the Senate later runs resolve on owner HITL`.

**In-file residue folded (same finding #4, not separately enumerated in the brief — flagged here per Law 1):**
- `docs/skills/warehouse-ingest.md` ANTECHAMBER DISCIPLINE (line ~95): `the markdown written only when the OWNER runs resolve … ingested` → `the Senate runs resolve … ingested on owner HITL`. This is the **identical D2-stale phrase** finding #4 exists to eliminate, in a file already in scope; leaving it would make the file self-contradict the line-11 fix. Pure prose reconciliation, zero behaviour change. Surfaced explicitly for owner visibility — the brief listed "lines ~11 + ~99"; this was a third occurrence of the same pattern.

## Scope fence — honoured
- 6 listed files only. Did NOT touch retro `LESSONS.md` / 10-entry-counter framing (#5a, residue sweep) or the ticket-comment `mode:` enum (#5b, separate ticket). No `resolve`/`grant` rights added to any non-Senate agent; SCRUTINIZE DENY and query-policy core untouched.

## Out-of-scope observations (report-only, per execution.md — master decides)
- `warehouse-usage.md:86` (§3, flag-resolution sweep): `the owner runs the resulting flag-resolution sweep` is the loose pre-refinement phrasing vs the same file's matrix line 34 (`agent-executed sweep | explicit owner HITL`). Same D2-refinement pattern as #4 but **not** flagged by Codex and **not** a listed delta — left unchanged. Candidate for the residue sweep if the owner wants full D2-phrasing consistency.
- `warehouse-usage.md:89` (§2, semantic-audit pass): `the owner runs it` is **correct as-is** — section 2 is explicitly an owner by-hand pass (no CLI verb mints the contradiction flag; automation deferred). No action.
