---
name: censura-output
description: Senate Censura handoff format — verdict, recovery paths, follow-up ticket creation, and output constraints
---

VERDICT OPTIONS
GREEN: all requirements met, no FAILs
YELLOW: met but RISK items recorded; owner acknowledges before merge
RED: one or more FAILs, or Critical Rule violation

OUTPUT FORMAT
Post as Notion comment on ticket (ticket-comment.md protocol), addressed to Project Owner:

still_solving: [one sentence restating ticket goal]
mode: CENSURA
verdict: GREEN | YELLOW | RED
findings:
  - [PASS|FAIL|RISK|NOTE] [area] [HIGH|MED|LOW Impact] [HIGH|MED|LOW Effort] — [one sentence]
addressed: [Consilium expected_outputs verified — confirm each one]
claude_md_flag: NONE | [full consolidated change — incorporates Consilium flag, not just delta]
adr_proposal: NONE | [domain area — rationale; full content per doc-maintenance.md ADR format]
owner_override: [if owner overrode a finding — "overridden by Owner — [reason]"; empty if none]
emergent_gaps: [candidate SPIKE sub-tickets or DEV tickets — empty if none]

ON RED — EXPLORACIO
gaps_to_address: [explicit list for Quaestor amendment]
Recovery: Quaestor new session → loads all comments incl. this RED verdict → amendment comment → Senate:Censura full check round

ON RED — OPUS
Recovery: Praetor fix → owner decides full or targeted Collegium re-review (default: full cycle)

TICKET CREATION (EXPLORACIO end only)
If emergent_gaps non-empty and owner approved in discussion: Censura creates follow-up tickets in Notion.
Set parent_ticket relation to current ticket ID on each created ticket.

LESSONS.md WRITE
Execute before posting Notion ticket comment — sequence: write entry → then post comment.
Load LESSONS.md. If file does not exist: create it with the standard header.
Count entries since last --- divider. If no divider found: count all entries.
Write one entry: [YYYY-MM-DD] [TICKET-ID] [GREEN|YELLOW|RED] — [one sentence: what worked or what failed]
If count reaches 10: suggest retrospective to owner before writing entry — pipeline does not block.

NEVER
Never omit the handoff block
Never set GREEN with unresolved FAILs
Never write only delta for claude_md_flag — always full consolidated change
Never create follow-up tickets without explicit owner approval in discussion
Never omit gaps_to_address on RED in EXPLORACIO
