---
name: consilium-output
description: Senate Consilium handoff format — structured output to Praetor or Quaestor as a handover block
---

OUTPUT FORMAT (D2/D7)
Append a handover block to `<TICKET-ID>_handover.md` (ticket-comment.md protocol), addressed to Praetor (OPUS) or Quaestor (EXPLORACIO). Consilium runs before the executor, so the hub usually does not exist yet — append the handover block only; the executor (Praetor/Quaestor) creates the hub and seeds its session table from the existing blocks. If the handover file is missing, create it (backfill invariant). Block header: `### Senate Consilium — <verdict> | <date>`.

still_solving: [one sentence restating ticket goal]
mode: CONSILIUM
da_designation: NONE | [persona name — designated DA for this session]
verdict: APPROVED | APPROVED_WITH_RISK | BLOCKED
decisions:
  - [DECIDED|BLOCK|RISK|OPEN] [HIGH|MED|LOW] [REVERSIBLE|HARD TO REVERSE] — [one sentence]
assumptions: [list — empty if none]
dissent: [minority positions not adopted — empty if none]
new_unknowns: [SPIKE tickets needed — empty if none; owner creates]
claude_md_flag: NONE | [preliminary change description]
unresolved_conflict: [significant persona disagreement flagged for next agent — empty if none]
expected_outputs: [what Praetor or Quaestor must deliver or verify]

VERDICT RULES
BLOCKED: any BLOCK finding unresolved
APPROVED_WITH_RISK: RISK items remain, no BLOCKs
APPROVED: all DECIDED or no findings

EXPLORACIO HANDOFF NOTE
Quaestor reads this handover block in two passes:
Pass 1 (scope only — before own research): still_solving + expected_outputs from the block
Pass 2 (after all chunks researched): decisions section
Never embed decisions inside still_solving — sections must stay separable.

NEVER
Never omit the handover block — even on trivial tickets
Never set APPROVED with unresolved BLOCK
Never include implementation details — design deliberation only
Never omit unresolved_conflict if personas disagreed significantly on a finding
Never omit expected_outputs from the handover block
