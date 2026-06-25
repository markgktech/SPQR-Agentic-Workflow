---
name: censura-output
description: Senate Censura handoff format — verdict, recovery paths, follow-up ticket creation, and output constraints
---

VERDICT OPTIONS
GREEN: all requirements met, no FAILs
YELLOW: met but RISK items recorded; owner acknowledges before merge
RED: one or more FAILs, or Critical Rule violation

RECEIPT ENFORCEMENT (D6/D8 — enforcer only; Senate runs no shell → Censura checks presence, never produces a receipt)
No GREEN while any build/test/lint claim in the trail lacks its verbatim receipt.
Missing receipt = HITL flag + cheap producer bounce (producer re-attaches the decisive line) — NOT a standalone veto; a receipt is clerical, a full RED/revision cycle is disproportionate (D6).
A receipt showing an ACTUAL build/test failure IS a real failure → route the existing Probator-veto / Censura-RED machinery; do not build a new veto/RED path.
Enforcement lives here only (D8) — Tribunus/Curator do not check receipts.

CLOSE-OUT CHECKLIST (fixed order per D3 — mandate in senate.md CENSURA CHECKLIST)
C-56: hub session/status row exists, references the correct handover/output artifacts, and matches the actual routing/verdict.
C-54: Warehouse Delta present + credible; `none` only with rationale; candidates owner-understandable and dispositioned; owner approval required before antechamber proposal or canonical ingest — no auto-ingest.
C-55: write-gate receipt present for any warehouse-MUTATING session (command, exit code, final `check` result, reconcile-needed, no-`--fresh`); missing → YELLOW/FAIL.

TICKETING PHASE TRIGGER
Condition: GREEN + proposals table present (not "no tickets") + owner explicit approval
If condition met: context carries over → load censura-ticketing-input.md
If "no tickets proposed": pipeline closes here
No new input loading between VERIFY and TICKETING phases

OUTPUT FORMAT (D2/D6)
Append a handover block to `<TICKET-ID>_handover.md` (ticket-comment.md protocol), addressed to Project Owner. Block header: `### Senate Censura — <verdict> | <date>`. Add the Censura verdict row to the hub `## Session / cost` table (session_id `—` — Senate runs no shell, so it cannot capture `$CLAUDE_CODE_SESSION_ID`; cost_total stays owner-filled). Backfill invariant (D7): if the hub is missing, create it from template before finishing.

still_solving: [one sentence restating ticket goal]
mode: CENSURA
verdict: GREEN | YELLOW | RED
findings:
  - [PASS|FAIL|RISK|NOTE] [category:<enum>] [area] [HIGH|MED|LOW Impact] [HIGH|MED|LOW Effort] — [one sentence]
addressed: [Consilium expected_outputs verified — confirm each one]
commit_message: [GREEN only — final commit text for the owner to copy: one-line title + human-readable bullets at deliverable altitude, synthesized from the ticket trail + diff; describes the delivered state, not the veto journey. Empty on YELLOW/RED. Text output only — Censura never commits.]
claude_md_flag: NONE | [full consolidated change — incorporates Consilium flag, not just delta]
decision_proposal: NONE | [decision-node proposal per warehouse-ingest.md — title/rationale/body]
owner_override: [if owner overrode a finding — "overridden by Owner — [reason]"; empty if none]
emergent_gaps: [candidate SPIKE sub-tickets or DEV tickets — empty if none]

[category:<enum>] — FAILURE-CATEGORY ENUM (D7 — definition home)
The recurring-failure key the retro harvest counts on (retrospector.md); tag every finding with one value. Evidence-seeded, kept small so producers don't mis-bucket:
  receipt-missing · scope-creep · test-gap · spec-ambiguity · other
Additive token ONLY — does NOT change the PASS/FAIL/RISK/NOTE verdict enum, the impact/effort tags, receipt enforcement, or verdict semantics (a RED stays a RED at emit time). The enum DEFINITION lives here — the producer (Censura) writes the tag; the retro reads it and may FLAG a candidate new category, but never adds one (owner decides — rule-rot pattern).

ON RED — EXPLORACIO
gaps_to_address: [explicit list for Quaestor amendment]
Recovery: Quaestor new session → loads `<TICKET-ID>_handover.md` incl. this RED verdict → amendment block → Senate:Censura full check round

ON RED — OPUS
Recovery: Praetor fix → owner decides full or targeted Collegium re-review (default: full cycle)

EMERGENT GAPS
emergent_gaps field captures Censura-identified gaps not covered by Quaestor proposals — not auto-created.
Owner manually opens tickets for these after pipeline closes.

LESSON-NODE PROPOSAL (D2c — warehouse-primary; replaces the flat LESSONS.md write)
Execute before appending the Censura handover block — sequence: emit the lesson proposal → then append the handover block.
The lesson is authored as a **lesson-node proposal** to the warehouse antechamber via `docs/skills/warehouse-ingest.md` — NOT a flat-file write. `propose` is free (no owner HITL — the hard-gate + the Senate's own judgment is the control); the Senate later runs `resolve` on owner HITL.
- MANDATORY read-before-propose: a `find`/`open-scope` dup-check round first (per the WAREHOUSE QUERY POLICY block in senate.md). If the lesson already exists, do not re-propose; if it contradicts an active node, author a superseding decision instead.
- Proposal frontmatter (NODE_FORMAT minus the 3 robot-stamped keys id/timestamp/schema_version — never hand-mint an id):
  `kind: lesson` · `status: active` · `title: …` · `verdict: GREEN|YELLOW|RED` (matches the Censura verdict) · `origin: observed` · `ticket: <TICKET-ID>` · `agent: <subject agent — the erring/deciding one>` · then an `edges:` block with the recommended `about` edge (`type: about`, `target: <related node-id>`) when a related node exists. Body = one+ sentence: what worked or what failed.
  Per the hard-gate, a lesson REQUIRES `agent` + `ticket`; `verdict` is allowed only on a lesson.
- CLI: `propose --warehouse-root [WAREHOUSE_ROOT] --ticket <TICKET-ID> --agent Senate --file <lesson.md>|-`. Log the propose action + gate verdict (proposal key + state) into the handover receipt (SAW-26 discipline).
Retro cadence (10-entry trigger) is read off the warehouse trace/heat, not a flat-file divider count — owner-driven (see retrospector).
(docs/LESSONS.md is not deleted this run — flat-doc physical retirement is a separate owner SAW.)

NEVER
Never omit the handoff block
Never set GREEN with unresolved FAILs
Never set GREEN while any build/test/lint claim lacks its verbatim receipt — flag the gap as a HITL producer bounce (cheap, D6), not a standalone veto; a receipt showing an actual failure is RED via the existing machinery, not a new path
Never omit commit_message on GREEN — owner copies it into the commit
Never write only delta for claude_md_flag — always full consolidated change
Never create follow-up tickets without explicit owner approval in discussion
Never omit gaps_to_address on RED in EXPLORACIO
