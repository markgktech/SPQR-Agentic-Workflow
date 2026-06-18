HANDOVER BLOCK — SHARED PROTOCOL
Keep the block terse — a routing/signal record; detail belongs in the output doc, not here (no fixed line count). One block per stage. Append at stage completion — not only at session end.
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
receipt: [producer only — verbatim decisive tool-output `<command> → <decisive stdout line>` per build/test/lint claim; see FIELD RULES for the scoped definition]
routing: → [next agent | OWNER]

FIELD RULES
session_id: always present; retrieve own value via `echo $CLAUDE_CODE_SESSION_ID` (Bash) at block-writing time; if the env var is unset, record `unknown` — never drop the field
approach_before_consilium: Praetor only; omit for all other agents
consilium_addressed: Praetor only; one-line summary only — full detail belongs in the output file; omit for others
impl_doc: Praetor only; must be present before routing — reviewers load on-demand; points to the local `<TICKET-ID>_output.md`; omit for others
addressed: empty on first block in a pipeline run; required on all subsequent blocks
receipt: CANONICAL definition — defined ONCE here (D2); the producer/enforcer skills reference this, they do not restate it. A receipt binds every build/test/lint claim to verbatim tool evidence: `<command> → <decisive stdout line>`, copied exact — NOT paraphrased. Scoped to the decisive line, not the full log. Whitelist: build succeeded · tests ran + result · lint zero-warnings (e.g. `BUILD SUCCEEDED`, `Executed 42 tests, 0 failures`, `0 violations`). Producers: Praetor (build + lint), Probator (test). Senate runs no shell → Censura cannot produce one; it is the enforcer only. Praetor's verbatim build/lint lines live in `<TICKET-ID>_output.md` VERIFICATION (RECEIPT) and the handover field carries the compact decisive line(s); Probator (no output doc, D14) puts its decisive test line directly in this field. Producer field only — omit on Tribunus/Curator/Senate blocks.
routing: name next agent explicitly; use OWNER if pipeline ends or HITL checkpoint reached

CONSTRAINTS
Never bloat the block — keep it a terse routing/signal record; push detail to the output doc
Never omit session_id
Never omit expected_outputs
Never omit routing
Never omit a receipt on a build/test/lint claim to save tokens — it is a quality floor (cost-guard C6), never optional; a missing receipt is bounced at Censura
Never omit impl_doc on Praetor block — the local `<TICKET-ID>_output.md` must exist before the block is appended
Never append mid-implementation — only at stage completion checkpoints
Never carry forward prior agent opinions in your own block fields
Never overwrite or edit a prior block — the handover file is append-only
