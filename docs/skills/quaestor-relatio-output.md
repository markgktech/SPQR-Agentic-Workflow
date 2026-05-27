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

SPIKE DOCUMENT
Create Notion child page under the spike ticket using SPIKE DOCUMENT TEMPLATE.
Fill in order: metadata → per-topic decisions → Summary last.
Metadata: Status = In Progress, Created = today, Author = Quaestor, Mandate = Consilium comment link, Ticket = spike ticket link.
Reference: docs/skills/spike-document.md for structure and fill rules.

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
Never create follow-up tickets — Censura handles those
