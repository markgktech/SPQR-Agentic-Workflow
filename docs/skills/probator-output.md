FINDINGS DECLARATION
Declare ALL findings before making veto decision — no silent pass.
Format per finding: [HIGH | MED | LOW] [file] — [one sentence description]
Veto only the highest-priority finding. All others remain visible in ticket comment for owner.

Finding criteria:
  Test failure on changed path = HIGH
  Missing coverage on changed core logic path = MED
  Missing edge case coverage (nil, boundary, error state) on changed path = MED if core logic, LOW if secondary
  Untestable path (per ios-testing.md scope rules) = document reason, not a finding

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
Load collegium-veto.md format before posting veto.
Post veto as Notion comment after owner approves (go ahead).
One veto = one issue = one fix_contract.

CLEAN PASS
If no findings warrant veto: post clean pass.
Cite test results and coverage status per changed path.
Format: [file] — suite: PASS | coverage: [status]
Silent clean pass is invalid — every changed path must be cited.

TICKET COMMENT
Post using ticket-comment.md protocol.
Required fields:
  still_solving: [ticket goal restated]
  mode: PROBATOR
  findings: [ALL findings — HIGH/MED/LOW — even if not vetoed]
  test_results: [pass/fail per changed path]
  addressed: [confirmation Praetor expected_outputs were met — or gap noted]
  expected_outputs: [what Curator must verify]
  routing: → Curator (clean pass) | → OWNER (HITL pending) | → Praetor (veto issued)

CONSTRAINTS
Never decide before declaring all findings
Never veto without prior HITL checkpoint on MED/HIGH
Never post veto before owner approves go ahead
Never issue clean pass without citing test results per changed path
Never route to Curator if veto is pending
