---
name: censura-ticketing-output
description: Censura ticketing phase output — owner approval gate, Notion ticket creation, comment protocol
---

INVOKE
After censura-ticketing-discussion.md — all verdicts must be PASS before proceeding

OWNER APPROVAL GATE
Present full PASS proposals table to owner.
Owner approves each ticket explicitly — one by one, not as a batch.
Do not create any ticket without explicit approval for that specific ticket.
Bug ticket proposals: present with note "owner creates manually" — do not proceed to TICKET CREATION for these.

TICKET CREATION (D9)
For each approved ticket:
  1. Fetch template from Notion by page ID (already loaded — do not refetch)
  2. Map proposal fields to template sections; set the `Ticket type` field (Spike | Feature | Bug | Doc); title is a plain description (no prefix)
  3. Create ticket in Notion — numbering is central and Notion-assigned (Foodoire → FDP-N)
  4. Report created ticket URL in output

REJECT PROTOCOL
For each REJECT verdict:
  Append a REJECT finding to `<TICKET-ID>_handover.md`: "Ticketing issue: [exact finding]"
  Owner manually resumes Quaestor session with this finding
  On revalidation: Censura appends a new handover block confirming resolution
  (Ticket creation itself stays in Notion — only the finding's work-trace is local — D9/D2)

NEVER
Never create a ticket before explicit owner approval of that specific ticket
Never invent or assign a ticket number — numbering is central and Notion-assigned
Never set ticket type as a title prefix — use the `Ticket type` field
Never create bug tickets autonomously
Never proceed past approval gate with unresolved REVISE or REJECT
