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

TICKET CREATION
For each approved ticket:
  1. Fetch template from Notion by page ID (already loaded — do not refetch)
  2. Map proposal fields to template sections
  3. Create ticket in Notion
  4. Report created ticket URL in output
  5. Owner assigns final prefix and number

REJECT PROTOCOL
For each REJECT verdict:
  Write Notion comment on the spike ticket: "Ticketing issue: [exact finding]"
  Owner manually resumes Quaestor session with this finding
  On revalidation: Censura writes new Notion comment confirming resolution

NEVER
Never create a ticket before explicit owner approval of that specific ticket
Never assign ticket prefix or number — owner assigns after creation
Never create bug tickets autonomously
Never proceed past approval gate with unresolved REVISE or REJECT
