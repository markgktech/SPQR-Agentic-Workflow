---
name: ticket-slicing
description: Shared ticket slicing skill — Quaestor proposes, Censura validates and creates. Two explicit modes.
---

INVOKE
Quaestor mode: after DISCUSSION closes, before quaestor-relatio-output.md
Censura mode: loaded by censura-ticketing-input.md — do not load independently

SLICING CRITERIA
Core test — ticket is correctly sized if:
  deliverable fits in one sentence
  executor needs max 3-4 reference files to fully understand the task
  verifier can confirm it in isolation without dependent work running

Slice when:
  "and also" appears anywhere in description → new ticket
  foundation + feature in same ticket → split: infra first, feature second
  more than 3-4 files will be touched → consider splitting
  two tickets are coupled → order them; second ticket declares first as dependency

Vertical over horizontal: thin but complete flow beats all-models or all-views.
Independence: each ticket implementable without knowing what another in-progress ticket will do.

PRIORITY
Critical — blocks deployment or another ticket entirely
Major — required for the feature or pipeline to function
Minor — improvement, cleanup, or non-blocking quality

[PROJECT_BOUNDARIES]
Replace with project-specific layer and entity slicing rules.

QUAESTOR — PROPOSE
Produce a proposals table — one row per ticket:
  title (descriptive working title — no prefix, no number)
  in (what is explicitly included)
  out (what is explicitly excluded)
  priority (Critical / Major / Minor)
  dependency (working title of blocking ticket, or none)

If no tickets needed: write "No tickets proposed — spike is informational."

Self-check before including any proposal:
  1. deliverable in one sentence?
  2. independent of all in-progress work?
  3. contains "and also"?
  4. verifiable in isolation?
  5. executor needs more than 3-4 reference files?
Fail on any → split or drop before proposing.

CENSURA — VALIDATE + CREATE
For each proposal: verify against all SLICING CRITERIA — one finding per violation.
Verdict per proposal:
  PASS — meets all criteria
  REVISE — specific violation cited; Quaestor amends that proposal only
  REJECT — scope unsalvageable; write exact finding to output
All proposals PASS → present full table to owner for approval.
Owner approves each ticket explicitly → fetch template from Notion by page ID → create ticket → report URL.
On REJECT: write Notion comment "Ticketing issue: [finding]" — owner resumes Quaestor manually with this finding.
On revalidation after Quaestor revision: write new Notion comment confirming resolution.
Owner assigns final prefix and number after creation.

NEVER
Never invent ticket prefix or number (SPIKE-XXX, DOC-XXX, or any other)
Never create a ticket in Notion before explicit owner approval of that specific ticket
Never create bug tickets autonomously — Bug tickets are owner-initiated only
Never propose a ticket that spans two pipeline stages
Never mark a dependent ticket as independent
Never include foundation and feature work in the same ticket
Never treat a REVISE verdict as a full spike rerun — amend the specific proposal only
Never skip the self-check before proposing
Never apply project-specific boundaries from another project — use only the boundaries defined in [PROJECT_BOUNDARIES] above
