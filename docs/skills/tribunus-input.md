LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text + all Notion comments — Praetor output is primary context)
4. collegium-veto.md
5. code-review-checklist.md
6. In revision flow only: delta doc child page linked in Praetor revision comment
7. tribunus-output.md

FRESH EYES
Load Praetor ticket comment as primary context — no Consilium output by default.
Do not load Consilium before forming independent review opinion.

CONSILIUM ON-DEMAND
If scope drift or approach mismatch is suspected during review:
1. Check consilium_addressed field in Praetor ticket comment first
   — if deviation is documented there: NOTE, not a finding
   — if deviation is undocumented: potential scope drift finding
2. Only if still unclear: load Consilium comment scope-only (still_solving + expected_outputs)
   Never load the decisions section.
3. If Consilium was consulted: note it in ticket comment (consilium_consulted: YES — [reason])

FILE MAPPING
Identify every changed file from Praetor expected_outputs.
Apply code-review-checklist.md against each changed file independently.
In revision flow: also apply checklist to collateral change files listed in delta doc CHANGED section.

IMPL DOC
After completing independent code review: load impl doc child page from Praetor impl_doc URL.
Purpose: cross-check KEY DECISIONS context; surface gaps between documented rationale and observed implementation.
Annotate TRIBUNUS NOTES section with findings summary — or "no gaps found" if nothing to add.
Do not load impl doc before completing independent review — sycophancy risk.

CONSTRAINTS
Never load Consilium output before completing independent review
Never expand review scope beyond files listed in Praetor expected_outputs (+ delta doc in revision)
Never carry state from a prior session — start cold (Law 3)
Never form opinions before all LOAD ORDER items are read
