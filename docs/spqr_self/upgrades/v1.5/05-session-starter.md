You are an execution agent for SPQR upgrade run v1.5, Group 5 (Receipt rule — verbatim build/test/lint evidence — SAW-26).

PRE-FLIGHT (load in order):
  - docs/upgrade/execution.md                                              (execution protocol — receive brief, execute only)
  - docs/spqr_self/upgrades/v1.5/05-receipt-rule.md                        (YOUR BRIEF — FILES, Decisions D1–D8 — binding; this run has no separate PoC, decisions are inlined here)
  - docs/skills/ticket-comment.md , docs/skills/praetor-impl-doc.md , docs/skills/praetor-output.md , docs/skills/probator-output.md , docs/skills/probator-input.md , docs/skills/censura-input.md , docs/skills/censura-output.md   (the 7 edit targets — read current form first)
  - docs/agents/praetor.md , docs/agents/probator.md                       (FORM reference ONLY — confirm Praetor/Probator have Bash + write scope; DO NOT edit)

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = docs/spqr_self/upgrades/v1.5/05-receipt-rule.md

Read the Brief there, do the work on the 7 FILES listed, then fill its "## Changes Made" section
(replace the _(pending execution)_ sentinel) — file by file, with a short Verification block.

Key reminders (full rationale in the brief Decisions D1–D8):
  - Receipt = `<command> → <decisive stdout line>`, VERBATIM, not paraphrase (D3). Whitelist: build succeeded · tests ran + result · lint zero-warnings. Scoped to the decisive line, NOT the full log.
  - Producer/enforcer split (D1): Praetor produces build+lint, Probator produces test. Censura is the ENFORCER (Senate runs no shell — it cannot produce a receipt, only check presence). Do NOT add receipt-production to Censura.
  - Canonical definition lives ONCE in ticket-comment.md (D2); the other skills reference it, do not restate the full definition.
  - Physical home (D5): Praetor verbatim build/lint → `_output.md` new `**VERIFICATION (RECEIPT)**` section + compact `receipt:` line in the handover block. Probator has no output doc (D14) → its decisive test line goes directly in the handover `receipt:` field.
  - Cost-guard C6 (D4): receipt is a quality floor — never omitted to save tokens. State as a CONSTRAINT in the producer skills.
  - Missing receipt (D6): Censura flags it as a HITL gap + cheap producer bounce — NOT a standalone veto. A receipt showing an ACTUAL build/test failure routes through the EXISTING Probator-veto / Censura-RED machinery. Do NOT build a new veto/RED path.
  - Enforcement at Censura ONLY (D8) — do NOT add receipt checks to Tribunus or Curator skills.
  - DO NOT touch the "Max 12 lines" cap in ticket-comment.md (`:2` / `:29`) — that is R1, owner-pending, handled by the master separately. The compact receipt line fits within the existing cap.
  - This is generic SPQR only (D7). Do NOT touch any Foodoire / consuming-project file. Do NOT touch the MAIN folder-note (v1.5.md) or sibling sub-docs. Do NOT run git commit or git push.

Report at the end; flag any out-of-scope discovery for the master — do not act on it.
