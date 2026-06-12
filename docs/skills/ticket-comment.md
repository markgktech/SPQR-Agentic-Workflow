TICKET COMMENT — SHARED PROTOCOL
Max 12 lines. One comment per stage. Post at stage completion — not only at session end.

FORMAT
session_id: [claude_cli_conversation_id]
still_solving: [one sentence — ticket goal]
mode: [PRAETOR | TRIBUNUS | PROBATOR | CURATOR]
approach_before_consilium: [Praetor only — 1-2 sentences, independent approach before Consilium load]
consilium_addressed: [Praetor only — one-line summary; detail in impl doc KEY DECISIONS]
addressed: [confirmation prior expected_outputs were met — empty on first Praetor comment]
expected_outputs: [changed file list — detail in impl doc FILES CHANGED]
impl_doc: [Praetor only — Notion child page URL]
routing: → [next agent | OWNER]

FIELD RULES
session_id: always present; retrieve own value via `echo $CLAUDE_CODE_SESSION_ID` (Bash) at comment-writing time; if the env var is unset, record `unknown` — never drop the field
approach_before_consilium: Praetor only; omit for all other agents
consilium_addressed: Praetor only; one-line summary only — full detail belongs in impl doc; omit for others
impl_doc: Praetor only; must be present before routing — reviewers load on-demand; omit for others
addressed: empty on first comment in a pipeline run; required on all subsequent comments
routing: name next agent explicitly; use OWNER if pipeline ends or HITL checkpoint reached

CONSTRAINTS
Never exceed 12 lines
Never omit session_id
Never omit expected_outputs
Never omit routing
Never omit impl_doc on Praetor comment — URL must exist before ticket comment is posted
Never post mid-implementation — only at stage completion checkpoints
Never carry forward prior agent opinions in your own comment fields
