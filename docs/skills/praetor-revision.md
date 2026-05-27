REVISION ENTRY
Load this file on: Tribunus veto | Probator veto | Censura RED.
Load collegium-veto.md to parse the incoming veto format.
If revision #2+: load existing delta doc child page from Notion before starting.

FIX SCOPE
Fix only the issue named in fix_contract — nothing else.
No cleanup, no refactor, no opportunistic improvements outside fix_contract.

COLLATERAL CHANGE RULE
Touch adjacent code only if the fix is incorrect or fails to compile without it.
Test: "Does the fix compile and run correctly without touching [file/function]?"
  If NO → collateral change allowed; document in delta doc CHANGED with explicit justification
  If YES → do not touch; document in delta doc NOT TOUCHED

DELTA DOC
Create Notion child page under the ticket: title "Delta Doc — Revision #[N]"
Link delta doc URL in ticket comment.
Max 100 lines; target ~20.

Format:
REVISION DELTA DOC
Ticket: [ID]
Revision: #[N]
Veto ref: [TRIBUNUS | PROBATOR | CENSURA — one sentence summary of vetoed finding]

CHANGED
[file] — [what changed, 1–2 lines]

NOT TOUCHED
[file/area] — [why not touched: "not required" or "explicitly excluded"]

SCOPE NOTE
[what was explicitly excluded and why; collateral change justification if applicable]

NOT TOUCHED cannot be empty if there are in-scope files that were not modified.

IMPL DOC UPDATE
After completing the revision fix: update the impl doc child page.
Update FILES CHANGED to reflect revised files.
Update TEST COVERAGE if tests were added or changed.
Do not rewrite existing NOTES sections — reviewer annotations are preserved.

TICKET COMMENT
Post using ticket-comment.md protocol after delta doc is created and impl doc is updated.
  mode: PRAETOR
  addressed: [confirmation of what fix_contract required — done]
  expected_outputs: [files the reviewing agent must re-verify; include collateral change files if any]
  impl_doc: [same Notion child page URL — updated]
  delta_doc: [delta doc child page URL]
  routing: → [TRIBUNUS | PROBATOR | CENSURA — the agent that issued the veto]

CONSTRAINTS
Never fix more than the vetoed issue — no cleanup, no scope creep
Never skip delta doc — even on trivial single-line fixes
Never skip impl doc update — reviewer NOTES sections must be preserved
Never leave NOT TOUCHED empty if in-scope files were not modified
Never post ticket comment before delta doc and updated impl doc both exist
Never resubmit to a different agent than the one that issued the veto
