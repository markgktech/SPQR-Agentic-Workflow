REVISION ENTRY
Load this file on: Tribunus veto | Probator veto | Censura RED.
Read the veto block from `<TICKET-ID>_handover.md`; load collegium-veto.md to parse its format.
If revision #2+: read the existing `<TICKET-ID>_output_revN.md` files from the vault before starting.

FIX SCOPE
Fix only the issue named in fix_contract — nothing else.
No cleanup, no refactor, no opportunistic improvements outside fix_contract.

COLLATERAL CHANGE RULE
Touch adjacent code only if the fix is incorrect or fails to compile without it.
Test: "Does the fix compile and run correctly without touching [file/function]?"
  If NO → collateral change allowed; document in delta doc CHANGED with explicit justification
  If YES → do not touch; document in delta doc NOT TOUCHED

DELTA DOC (D11)
Create the local file `<TICKET-ID>_output_revN.md` in the ticket's work_documents/ vault (not a Notion child page).
Reference its path in the handover block delta_doc field.
Max 100 lines; target ~20.

Format:
---
up: "[[<TICKET-ID>]]"
tags: [content/implementation-doc]
rev: [N]
---

REVISION DELTA DOC
Ticket: [[<TICKET-ID>]]
Revision: #[N]
Veto ref: [TRIBUNUS | PROBATOR | CENSURA — one sentence summary of vetoed finding]

CHANGED
[file] — [what changed, 1–2 lines]

NOT TOUCHED
[file/area] — [why not touched: "not required" or "explicitly excluded"]

SCOPE NOTE
[what was explicitly excluded and why; collateral change justification if applicable]

NOT TOUCHED cannot be empty if there are in-scope files that were not modified.

OUTPUT DOC UPDATE
After completing the revision fix: update `<TICKET-ID>_output.md`.
Update FILES CHANGED to reflect revised files.
Update TEST COVERAGE if tests were added or changed.

HANDOVER BLOCK
Append using ticket-comment.md protocol after the delta doc is created and the output doc is updated — header `### Praetor — Revision #N <verdict> | <date>`.
  mode: PRAETOR
  addressed: [confirmation of what fix_contract required — done]
  expected_outputs: [files the reviewing agent must re-verify; include collateral change files if any]
  impl_doc: [local `<TICKET-ID>_output.md` path — updated]
  delta_doc: [local `<TICKET-ID>_output_revN.md` path]
  routing: → [TRIBUNUS | PROBATOR | CENSURA — the agent that issued the veto]

CONSTRAINTS
Never fix more than the vetoed issue — no cleanup, no scope creep
Never skip the delta doc — even on trivial single-line fixes
Never skip the output doc update after a revision
Never leave NOT TOUCHED empty if in-scope files were not modified
Never append the handover block before the delta doc and updated output doc both exist
Never resubmit to a different agent than the one that issued the veto
