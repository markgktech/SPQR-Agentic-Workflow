---
name: censura-ticketing-discussion
description: Censura ticketing phase discussion — PASS/REVISE/REJECT per proposal
---

INVOKE
After censura-ticketing-input.md — context and templates already loaded

FOR EACH PROPOSAL
Evaluate against ticket-slicing.md SLICING CRITERIA
Assign verdict:
  PASS — meets all criteria; ready for owner approval
  REVISE — one specific violation; state exact issue; Quaestor amends this proposal only
  REJECT — scope unsalvageable; state exact finding for the handover block (ticket creation itself stays in Notion — D9)

Present all verdicts as a list before proceeding.
All PASS → proceed to censura-ticketing-output.md
Any REVISE or REJECT → present to owner; do not proceed until resolved

NEXT
censura-ticketing-output.md

NEVER
Never proceed to censura-ticketing-output.md with unresolved REVISE or REJECT
Never evaluate against criteria outside ticket-slicing.md SLICING CRITERIA
Never treat a REVISE verdict as a full spike rerun — amend the specific proposal only
Never issue more than one REVISE finding per proposal — cite the primary violation only
