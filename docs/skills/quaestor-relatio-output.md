---
name: quaestor-relatio-output
description: Quaestor output skill — record owner decisions, create Spike Document page, handle failure fallback
---

TRIGGER
Load only after owner explicitly closes discussion in quaestor-relatio.md.

RECORD DECISIONS
For each topic record one of:
  DECIDED — approved scope, rationale, affected areas
  NO DECISION NEEDED — covered by [warehouse node-id / file:line / prior decision]
  OPEN — unresolved; candidate SPIKE sub-ticket; flag to owner
If a decision comes from owner consultation or another agent session (not from Quaestor research): label explicitly — "Source: owner" or "Source: [session name]".

SPIKE DOCUMENT (D3)
Create the local `<TICKET-ID>_output.md` in the ticket's work_documents/ vault (not a Notion page; no parent-page indirection).
The hub owns identity — the output carries minimal frontmatter only (`up: "[[<TICKET-ID>]]"` + `tags: [content/spike]`); no top metadata block.
Create the ticket hub `<TICKET-ID>_<title>.md` from template if missing (backfill invariant); link the output + handover in its `## Files`.
Report the local output path in the handover block.
Fill in order: per-topic decisions → Summary last.
Reference: docs/skills/spike-document.md for structure and fill rules.

TICKET PROPOSALS
Run ticket-slicing.md QUAESTOR mode before writing this section.
If no tickets: write "No tickets proposed — spike is informational."
Table columns: title | in | out | priority | dependency
Quaestor proposes only — does not create tickets in Notion.

ON FILE WRITE FAILURE
Alert owner immediately.
Output full spike document as plain text — owner pastes manually.
Do not silently fail — Law 3 (external record is truth).

HANDOVER BLOCK (D6)
Append a handover block to `<TICKET-ID>_handover.md` — header `### Quaestor — <verdict> | <date>`. Add the Quaestor session row to the hub `## Session / cost` table (session_id via `echo $CLAUDE_CODE_SESSION_ID`, `—` if unset).

still_solving: [one sentence restating spike goal]
mode: QUAESTOR
status: READY FOR CENSURA
decisions_recorded: [count of DECIDED + NO DECISION NEEDED + OPEN]
open_items: [list of OPEN topics — empty if none]
spike_document: [local `<TICKET-ID>_output.md` path]
expected_outputs: [what Senate Censura must verify]

NEVER
Never create the Spike Document before discussion is closed
Never omit the handover block
Never leave Summary blank — write it last, after all decisions are recorded
Never create tickets in Notion — propose via ticket-slicing.md only; Censura creates
Never use "note added", "applied", or "updated" language for changes not literally made in this session
Never present external decisions as Quaestor research findings
