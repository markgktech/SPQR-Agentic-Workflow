LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text) + `<TICKET-ID>_handover.md` (Praetor block is primary context) + `<TICKET-ID>_output.md`
4. collegium-veto.md
5. code-review-checklist.md
6. In revision flow only: the `<TICKET-ID>_output_revN.md` referenced in the Praetor revision block
7. tribunus-output.md

FRESH EYES
Load the Praetor handover block as primary context — no Consilium output by default.
Do not load Consilium before forming independent review opinion.

CONSILIUM ON-DEMAND
If scope drift or approach mismatch is suspected during review:
1. Check consilium_addressed field in the Praetor handover block first
   — if deviation is documented there: NOTE, not a finding
   — if deviation is undocumented: potential scope drift finding
2. Only if still unclear: load the Consilium handover block scope-only (still_solving + expected_outputs)
   Never load the decisions section.
3. If Consilium was consulted: note it in your handover block (consilium_consulted: YES — [reason])

FILE MAPPING
Identify every changed file from Praetor expected_outputs.
Apply code-review-checklist.md against each changed file independently.
In revision flow: also apply checklist to collateral change files listed in the delta doc CHANGED section.

OUTPUT DOC
After completing independent code review: load `<TICKET-ID>_output.md` from the Praetor impl_doc path.
Purpose: cross-check KEY DECISIONS context; surface gaps between documented rationale and observed implementation.
Record the findings summary — or "no gaps found" — in your handover block (D14: no NOTES section in the output doc).
Do not load the output doc before completing independent review — sycophancy risk.

CONSTRAINTS
Never load Consilium output before completing independent review
Never expand review scope beyond files listed in Praetor expected_outputs (+ delta doc in revision)
Never carry state from a prior session — start cold (Law 3)
Never form opinions before all LOAD ORDER items are read
