HANDOVER BLOCK — SHARED PROTOCOL
Max 12 lines. One block per stage. Append at stage completion — not only at session end.
Transport (D2): append a `---`-delimited block to `<TICKET-ID>_handover.md` in the ticket's work_documents vault — NOT a Notion comment. The work-trace is local. The field contract below is PRESERVED verbatim; only the transport changed.

APPEND MECHANICS
The executor agent creates `<TICKET-ID>_handover.md` if it does not exist: frontmatter `up: "[[<TICKET-ID>]]"` + `tags: [content/handover]`, then a `## <TICKET-ID> Handover Chain` heading and an `*Append-only.*` note. Backfill invariant (D7): any agent that finds the file missing creates it.
To append: locate the last `---` block in the file, add a new `---` delimiter, then the block header `### <Agent> — <verdict> | <date>` followed by the fields below. Never overwrite or edit a prior block — append only (D10).

FORMAT
session_id: [claude_cli_conversation_id]
still_solving: [one sentence — ticket goal]
mode: [PRAETOR | TRIBUNUS | PROBATOR | CURATOR]
approach_before_consilium: [Praetor only — 1-2 sentences, independent approach before Consilium load]
consilium_addressed: [Praetor only — one-line summary; detail in output KEY DECISIONS]
addressed: [confirmation prior expected_outputs were met — empty on first Praetor block]
expected_outputs: [changed file list — detail in output FILES CHANGED]
impl_doc: [Praetor only — local `<TICKET-ID>_output.md` path]
routing: → [next agent | OWNER]

FIELD RULES
session_id: always present; retrieve own value via `echo $CLAUDE_CODE_SESSION_ID` (Bash) at block-writing time; if the env var is unset, record `unknown` — never drop the field
approach_before_consilium: Praetor only; omit for all other agents
consilium_addressed: Praetor only; one-line summary only — full detail belongs in the output file; omit for others
impl_doc: Praetor only; must be present before routing — reviewers load on-demand; points to the local `<TICKET-ID>_output.md`; omit for others
addressed: empty on first block in a pipeline run; required on all subsequent blocks
routing: name next agent explicitly; use OWNER if pipeline ends or HITL checkpoint reached

CONSTRAINTS
Never exceed 12 lines in the block body
Never omit session_id
Never omit expected_outputs
Never omit routing
Never omit impl_doc on Praetor block — the local `<TICKET-ID>_output.md` must exist before the block is appended
Never append mid-implementation — only at stage completion checkpoints
Never carry forward prior agent opinions in your own block fields
Never overwrite or edit a prior block — the handover file is append-only
