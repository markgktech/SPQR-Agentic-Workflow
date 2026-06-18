---
name: censura-output
description: Senate Censura handoff format — verdict, recovery paths, follow-up ticket creation, and output constraints
---

VERDICT OPTIONS
GREEN: all requirements met, no FAILs
YELLOW: met but RISK items recorded; owner acknowledges before merge
RED: one or more FAILs, or Critical Rule violation

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
  - [PASS|FAIL|RISK|NOTE] [area] [HIGH|MED|LOW Impact] [HIGH|MED|LOW Effort] — [one sentence]
addressed: [Consilium expected_outputs verified — confirm each one]
commit_message: [GREEN only — final commit text for the owner to copy: one-line title + human-readable bullets at deliverable altitude, synthesized from the ticket trail + diff; describes the delivered state, not the veto journey. Empty on YELLOW/RED. Text output only — Censura never commits.]
claude_md_flag: NONE | [full consolidated change — incorporates Consilium flag, not just delta]
adr_proposal: NONE | [domain area — rationale; full content per doc-maintenance.md ADR format]
owner_override: [if owner overrode a finding — "overridden by Owner — [reason]"; empty if none]
emergent_gaps: [candidate SPIKE sub-tickets or DEV tickets — empty if none]

ON RED — EXPLORACIO
gaps_to_address: [explicit list for Quaestor amendment]
Recovery: Quaestor new session → loads `<TICKET-ID>_handover.md` incl. this RED verdict → amendment block → Senate:Censura full check round

ON RED — OPUS
Recovery: Praetor fix → owner decides full or targeted Collegium re-review (default: full cycle)

EMERGENT GAPS
emergent_gaps field captures Censura-identified gaps not covered by Quaestor proposals — not auto-created.
Owner manually opens tickets for these after pipeline closes.

LESSONS.md WRITE
Execute before appending the Censura handover block — sequence: write entry → then append block.
Load docs/LESSONS.md. If file does not exist: create it with the standard header.
Count entries since last --- divider. If no divider found: count all entries.
Write one entry: [YYYY-MM-DD] [TICKET-ID] [GREEN|YELLOW|RED] — [one sentence: what worked or what failed]
If count reaches 10: suggest retrospective to owner before writing entry — pipeline does not block.

NEVER
Never omit the handoff block
Never set GREEN with unresolved FAILs
Never omit commit_message on GREEN — owner copies it into the commit
Never write only delta for claude_md_flag — always full consolidated change
Never create follow-up tickets without explicit owner approval in discussion
Never omit gaps_to_address on RED in EXPLORACIO
