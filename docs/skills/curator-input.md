LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text) + `<TICKET-ID>_handover.md` (Praetor block is primary context) + `<TICKET-ID>_output.md`
4. In revision flow only: the `<TICKET-ID>_output_revN.md` referenced in the Praetor revision block
5. curator-output.md

OPERATIONAL LENS
Load the Praetor handover block as primary context.
Do not carry Tribunus or Probator findings into operational judgment — operational lens only.
Prior review blocks are visible in the handover but do not constrain your verdict.

AREA CHECK
Run build and lint before forming any verdict.
Check all 8 areas before declaring verdict — no area can be skipped.

  build — clean compile; no new warnings introduced
  lint — linter passes; no new violations
  CLAUDE.md compliance — Critical Rules from CLAUDE.md verified for all changed files
  scope boundary — no out-of-scope implementation; phase or milestone constraints respected
  localization — all user-facing strings use project's localization system; none hard-coded
  dead code — no unused imports, unreachable code, or orphaned symbols introduced
  operational risk — any change that could cause data loss, crash, or silent failure at runtime
  delta scope — revision only: Praetor fixed only the vetoed issue; N/A on first run

In revision flow: also check collateral change files listed in the delta doc CHANGED section.

OUTPUT DOC
After completing all 8 area checks: load `<TICKET-ID>_output.md` from the Praetor impl_doc path.
Purpose: cross-check KNOWN GAPS and KEY DECISIONS against operational findings.
Record the verdict summary or operational gaps found in your handover block (D14: no NOTES section in the output doc).
Do not load the output doc before completing area checks — results must be independent.

CONSTRAINTS
Never form verdict before running build and lint
Never skip an area — silence on any area is invalid
Never carry Tribunus or Probator judgments into your assessment
Never carry state from a prior session — start cold (Law 3)
Never form opinions before all LOAD ORDER items are read
