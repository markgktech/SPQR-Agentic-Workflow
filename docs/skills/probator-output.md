FINDINGS DECLARATION
Declare ALL findings before making veto decision — no silent pass.
Format per finding: [HIGH | MED | LOW] [file] — [one sentence description]
Veto only the highest-priority finding. All others remain visible in the handover block for owner.

Finding criteria:
  Test failure on changed path = HIGH
  Missing coverage on changed core logic path = MED
  Missing edge case coverage (nil, boundary, error state) on changed path = MED if core logic, LOW if secondary
  Untestable path (per project testing constraints from the warehouse; general judgment if ABSENT) = document reason, not a finding

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
Cite test results and coverage status per changed path.
Format: [file] — suite: PASS | coverage: [status]
Silent clean pass is invalid — every changed path must be cited.
Carry the verbatim test receipt in the handover `receipt:` field — Probator has no output doc (D14), so the decisive test line lives directly there.

HANDOVER BLOCK
Append using ticket-comment.md protocol — header `### Probator — <verdict> | <date>`. Add the Probator session row to the hub `## Session / cost` table (session_id via `echo $CLAUDE_CODE_SESSION_ID`, `—` if unset; D6).
Required fields:
  still_solving: [ticket goal restated]
  mode: PROBATOR
  findings: [ALL findings — HIGH/MED/LOW — even if not vetoed]
  test_results: [pass/fail per changed path]
  receipt: [verbatim test decisive line — `<test command> → <result line>` (e.g. `Executed 42 tests, 0 failures`); no output doc → the line lives here; definition in ticket-comment.md]
  addressed: [confirmation Praetor expected_outputs were met — or gap noted]
  expected_outputs: [what Curator must verify]
  routing: → Curator (clean pass) | → OWNER (HITL pending) | → Praetor (veto issued)

CONSTRAINTS
Never decide before declaring all findings
Never veto without prior HITL checkpoint on MED/HIGH
Never append the veto block before owner approves go ahead
Never issue clean pass without citing test results per changed path
Never issue a clean pass or handover without the verbatim test receipt — the decisive test line, not paraphrased; never dropped to save tokens (quality floor, cost-guard C6)
Never route to Curator if veto is pending
