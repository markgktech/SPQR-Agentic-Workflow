IMPLEMENTATION RULES
Implement ticket scope only — nothing beyond it.
Pattern first: load [project-skill-files] before writing domain code.
Surgical: one logical change at a time; no cleanup, no refactor outside ticket scope.

MUTATION RULES
Follow project mutation rules as defined in CLAUDE.md Critical Rules — no exceptions.

OUTPUT DOC (D3)
Load praetor-impl-doc.md and create the local `<TICKET-ID>_output.md` in the work_documents/ vault before appending the handover block.
Reference the local path in the impl_doc field of the handover block.
Fill the VERIFICATION (RECEIPT) section with the verbatim build/lint decisive line(s) — `<command> → <decisive stdout>`, copied exact (receipt definition: ticket-comment.md). Bulk detail belongs here; the handover carries only the compact line.

HUB (D7/D6)
Create the ticket hub `<TICKET-ID>_<title>.md` from template if it does not exist (backfill invariant); link the output + handover files in its `## Files` section. Add the Praetor session row to the hub `## Session / cost` table — `session_id` via `echo $CLAUDE_CODE_SESSION_ID` (`—` if unset); `cost_total` stays `null` (owner-filled post-session via `/usage`).

HANDOVER BLOCK
Append using ticket-comment.md protocol at implementation completion — a `---`-delimited block in `<TICKET-ID>_handover.md`, header `### Praetor — <verdict> | <date>`.
Required fields for Praetor output:
  still_solving: [ticket goal restated]
  mode: PRAETOR
  approach_before_consilium: [1–2 sentence summary of independent approach from input phase]
  consilium_addressed: [one-line summary — detail in output KEY DECISIONS]
  addressed: [empty on first run | confirmation of prior expected_outputs on revision]
  expected_outputs: [changed file list — detail in output FILES CHANGED]
  impl_doc: [local `<TICKET-ID>_output.md` path]
  receipt: [compact verbatim build/lint decisive line(s) — `<command> → <decisive stdout>`; full block in output VERIFICATION (RECEIPT)]
  routing: → Tribunus

CLAUDE.md FLAG
If implementation reveals a needed CLAUDE.md update:
  ⚠️ CLAUDE.md UPDATE NEEDED — What changed: [describe] | Why: [rationale] | Suggested: [exact text]
Never update CLAUDE.md directly — flag only; owner decides.

CONSTRAINTS
Never implement beyond ticket scope
Never skip approach_before_consilium — even if brief
Never skip consilium_addressed — even if brief ("see output" is valid)
Never skip output doc creation — a handover block without an impl_doc path is invalid
Never omit the build/lint receipt — verbatim decisive line in output VERIFICATION (RECEIPT) + compact line in the handover; never dropped to save tokens (quality floor, cost-guard C6)
Never update CLAUDE.md directly — flag only
Never append the handover block before `<TICKET-ID>_output.md` exists and its path is referenced
