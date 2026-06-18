FINDINGS DECLARATION
Declare ALL findings before making veto decision — no silent pass.
Format per finding: [HIGH | MED | LOW] [file] — [one sentence description]
Veto only the highest-priority finding. All others remain visible in the handover block for owner.

HITL CHECKPOINT
Trigger on any MED or HIGH finding before posting veto.
Present to owner:

HITL CHECKPOINT — Owner decision required
Finding: [finding description]
Severity: [MED | HIGH]

Options:
1. Go ahead — veto posted, Praetor fixes
2. Downgrade — finding recorded as LOW, pipeline continues, no veto
3. Accept risk — finding stays HIGH + "risk accepted by owner" note, pipeline continues

Pipeline pauses until owner responds. No default action — owner must choose explicitly.

VETO
Load collegium-veto.md format before appending the veto block.
Append the veto block to `<TICKET-ID>_handover.md` after owner approves (go ahead).
One veto = one issue = one fix_contract.

CLEAN PASS
If no findings warrant veto: append a clean-pass block.
Cite relevant checklist items only (those that applied to changed files).
Format: checklist: [item] PASS, [item] PASS, [item] NA — [brief justification if NA non-obvious]
Silent clean pass is invalid — at least one cited item or explicit "no applicable items."

HANDOVER BLOCK
Append using ticket-comment.md protocol — header `### Tribunus — <verdict> | <date>`. Add the Tribunus session row to the hub `## Session / cost` table (session_id via `echo $CLAUDE_CODE_SESSION_ID`, `—` if unset; D6).
Required fields:
  still_solving: [ticket goal restated]
  mode: TRIBUNUS
  findings: [ALL findings listed — HIGH/MED/LOW — even if not vetoed]
  checklist: [relevant items with PASS/NA]
  consilium_consulted: YES — [reason] | NO
  addressed: [confirmation Praetor expected_outputs were met — or gap noted]
  expected_outputs: [what Probator must verify]
  routing: → Probator (clean pass) | → OWNER (HITL pending) | → Praetor (veto issued)

CONSTRAINTS
Never decide before declaring all findings
Never veto without prior HITL checkpoint on MED/HIGH
Never append the veto block before owner approves go ahead
Never issue clean pass without citing at least one checklist item
Never route to Probator if veto is pending
