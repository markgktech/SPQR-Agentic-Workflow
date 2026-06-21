---
name: spike-document
description: Spike Document output format — Quaestor writes, Senate Censura reads; shared structure and fill rules
---

PURPOSE
Canonical output artifact of the EXPLORACIO pipeline. Quaestor creates and fills it as the local `<TICKET-ID>_output.md` in the ticket's work_documents/ vault. Senate Censura reads during review.
Structure = this spec minus the top metadata block — the hub owns identity (D3).

STRUCTURE

Frontmatter (minimal — the hub owns identity; no top metadata block)
up: "[[<TICKET-ID>]]"
tags: [content/spike]

Summary
2–4 sentences: what was investigated and what the outcome is.
Written after research is complete, before Censura review — never first.

Decision Table
One row per topic: #, Topic, Decision, Why, Dependency
Owner navigation aid — always present.

Decisions
One section per Decision Table row.
Per section: Problem / Options considered / Decision / Rationale / Affected areas

RESOLUTION TYPES
DECIDED — decision reached, ready for implementation
NO DECISION NEEDED — already covered; log as: "Covered by [warehouse node-id / file:line / prior decision] — no action required"
OPEN — unresolved; flag to owner; becomes candidate SPIKE sub-ticket

FILL RULES
Fill order: per-topic decisions → Summary last
If decision count >10: flag to owner before presenting — scope likely too wide
On file write failure: alert owner, output full document as plain text for manual paste

NEVER
Never invent a decision to fill the template — use NO DECISION NEEDED if already resolved
Never write Summary before research is complete
Never omit the `up:` hub link in frontmatter
Never leave Decision Table empty if decisions exist
