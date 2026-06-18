---
name: censura-ticketing-input
description: Censura ticketing phase input — loads ticket-slicing.md and Notion template IDs; only starts after GREEN verdict + owner approval
---

INVOKE
Only from censura-output.md conditional trigger — never load independently
Context carries over from VERIFY phase — do not reload session inputs

PRE-FLIGHT
Notion MCP must be available — verify before proceeding
Load ticket-slicing.md
Load current proposals table from session context — if not in context, reload from spike document URL before proceeding

TEMPLATE IDS
Spike ticket: [SPIKE_TEMPLATE_ID]
Feature ticket: [FEATURE_TEMPLATE_ID]
Bug ticket: [BUG_TEMPLATE_ID]
Doc ticket: [DOC_TEMPLATE_ID]
Spike document template: [SPIKE_DOCUMENT_TEMPLATE_ID]
Spike doc parent (Exploracio/Spiking): [SPIKE_DOC_PARENT_PAGE_ID]

TEMPLATE FETCH RULE
Fetch template from Notion by page ID at session start — once, before evaluating any proposal.
Extract section structure. Apply template-first: never delete or reorder existing sections; add sections only if no existing section fits; flag any deviation in output.

NUMBERING + TYPE (D9)
Ticket creation stays in Notion. Numbering is central and Notion-assigned (Foodoire → FDP-N) — the agent never invents or assigns a number.
Ticket type is set in the Notion `Ticket type` field (Spike | Feature | Bug | Doc) — not as a title prefix; titles are plain descriptions.
The template IDs above are the new Notion templates carrying the `Ticket type` field.

LOAD ORDER
1. ticket-slicing.md
2. Notion templates (fetch by ID above)
3. Proposals table from session context

NEXT
censura-ticketing-discussion.md

NEVER
Never load independently — only from censura-output.md conditional trigger
Never reload session inputs — context carries over from VERIFY phase
Never proceed if Notion MCP is unavailable
Never fetch templates more than once per session
