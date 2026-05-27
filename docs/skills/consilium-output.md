---
name: consilium-output
description: Senate Consilium handoff format — structured output to Praetor or Quaestor via Notion comment
---

OUTPUT FORMAT
Post as Notion comment on ticket (ticket-comment.md protocol), addressed to Praetor (OPUS) or Quaestor (EXPLORACIO):

still_solving: [one sentence restating ticket goal]
mode: CONSILIUM
verdict: APPROVED | APPROVED_WITH_RISK | BLOCKED
decisions:
  - [DECIDED|BLOCK|RISK|OPEN] [HIGH|MED|LOW] [REVERSIBLE|HARD TO REVERSE] — [one sentence]
assumptions: [list — empty if none]
dissent: [minority positions not adopted — empty if none]
new_unknowns: [SPIKE tickets needed — empty if none; owner creates]
expected_outputs: [what Praetor or Quaestor must deliver or verify]
claude_md_flag: NONE | [preliminary change description]
unresolved_conflict: [significant persona disagreement flagged for next agent — empty if none]

VERDICT RULES
BLOCKED: any BLOCK finding unresolved
APPROVED_WITH_RISK: RISK items remain, no BLOCKs
APPROVED: all DECIDED or no findings

EXPLORACIO HANDOFF NOTE
Quaestor reads this comment in two passes:
Pass 1 (scope only — before own research): still_solving + expected_outputs
Pass 2 (after all chunks researched): decisions section
Never embed decisions inside still_solving — sections must stay separable.

NEVER
Never omit the handoff block — even on trivial tickets
Never set APPROVED with unresolved BLOCK
Never include implementation details — design deliberation only
Never omit unresolved_conflict if personas disagreed significantly on a finding
