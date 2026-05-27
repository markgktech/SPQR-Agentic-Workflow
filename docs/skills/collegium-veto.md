COLLEGIUM VETO — SHARED FORMAT
Loaded by: Praetor (to recognize and respond), Tribunus (to issue), Probator (to issue)
One veto per agent per pipeline run. Single issue only.

VETO FORMAT
veto_from: [TRIBUNUS | PROBATOR]
issue: [one sentence — the specific finding that blocks]
location: [file(s) and function(s) affected]
fix_contract: [what must change — targeted, not a general rewrite]
resubmit_to: [TRIBUNUS | PROBATOR — the issuing agent]

PRAETOR ON RECEIPT
Load this file before reading the veto comment.
Fix only fix_contract scope — open praetor-revision.md.
Do not editorialize or dispute the veto — fix and resubmit.

TRIBUNUS / PROBATOR ON ISSUE
Declare all findings (LOW/MED/HIGH) before deciding to veto.
Veto only the highest-priority finding — one issue per run.
MED/HIGH: HITL checkpoint with owner before posting veto.
Post veto as Notion comment using ticket-comment.md format.

CONSTRAINTS
Never veto more than one issue per agent per pipeline run
Never issue veto without prior findings declaration
Never issue veto on LOW finding without owner approval
Never reopen a closed veto — new finding = new veto in next revision cycle
Never veto without specifying fix_contract — vague veto is invalid
