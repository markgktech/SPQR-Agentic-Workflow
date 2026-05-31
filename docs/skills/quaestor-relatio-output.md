---
name: quaestor-relatio-output
description: Quaestor output skill — record owner decisions, create Spike Document page, handle failure fallback
---

TRIGGER
Load only after owner explicitly closes discussion in quaestor-relatio.md.

RECORD DECISIONS
For each topic record one of:
  DECIDED — approved scope, rationale, affected areas
  NO DECISION NEEDED — covered by [ADR-XX / file:line / prior decision]
  OPEN — unresolved; candidate SPIKE sub-ticket; flag to owner
If a decision comes from owner consultation or another agent session (not from Quaestor research): label explicitly — "Source: owner" or "Source: [session name]".

SPIKE DOCUMENT
Create Notion page under the Exploracio/Spiking page ([SPIKE_DOC_PARENT_PAGE_ID]) using SPIKE DOCUMENT TEMPLATE.
NOT a child page of the dev ticket.
Add Ticket property linking back to the dev ticket.
Report created spike doc URL in output.
Fill in order: metadata → per-topic decisions → Summary last.
Metadata: Status = In Progress, Created = today, Author = Quaestor, Mandate = Consilium comment link, Ticket = spike ticket link.
Reference: docs/skills/spike-document.md for structure and fill rules.

TICKET PROPOSALS
Run ticket-slicing.md QUAESTOR mode before writing this section.
If no tickets: write "No tickets proposed — spike is informational."
Table columns: title | in | out | priority | dependency
Quaestor proposes only — does not create tickets in Notion.

ON NOTION WRITE FAILURE
Alert owner immediately.
Output full spike document as plain text — owner pastes manually.
Do not silently fail — Law 3 (external record is truth).

HANDOFF BLOCK
Post as Notion comment on ticket:

still_solving: [one sentence restating spike goal]
mode: QUAESTOR
status: READY FOR CENSURA
decisions_recorded: [count of DECIDED + NO DECISION NEEDED + OPEN]
open_items: [list of OPEN topics — empty if none]
spike_document: [Notion link to filled page]
expected_outputs: [what Senate Censura must verify]

NEVER
Never create the Spike Document before discussion is closed
Never omit the handoff block
Never leave Summary blank — write it last, after all decisions are recorded
Never create tickets in Notion — propose via ticket-slicing.md only; Censura creates
Never use "note added", "applied", or "updated" language for changes not literally made in this session
Never present external decisions as Quaestor research findings
