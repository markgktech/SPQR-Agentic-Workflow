LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text) + `<TICKET-ID>_handover.md` (Praetor block is primary context) + `<TICKET-ID>_output.md`
4. collegium-veto.md
5. In revision flow only: the `<TICKET-ID>_output_revN.md` referenced in the Praetor revision block
6. probator-output.md

FRESH EYES
Load the Praetor handover block as primary context.
Do not carry Tribunus findings into QA judgment — scope is tests and coverage, not code quality.
The Tribunus handover block is visible but does not constrain your findings.

TEST PATH MAPPING
Identify every changed file from Praetor expected_outputs.
For each changed file: identify all code paths that require test coverage.
Query the warehouse by scope (WAREHOUSE QUERY POLICY) for project-specific testing constraints and combine them with the general What to Test / What Not to Test criteria in this skill before marking paths as in-scope. No hit = legitimate ABSENT (close + flag); never fall back to a flat testing-guidelines file.
In revision flow: also map collateral change files listed in delta doc CHANGED section.

EDGE CASE ASSESSMENT
For each changed path, identify which scenarios should be covered:
  nil / empty input
  boundary values (min, max, boundary+1)
  error state / throw
  duplicate / already-exists record
  malformed input, wrong type
Only mark as in-scope if the component is testable per project test guidelines.
Untestable path: document reason explicitly — not a finding.

TEST SUITE RUN
Run existing test suite before forming any coverage opinion.
Record pass/fail per changed path — not aggregate suite-level results only.
Capture the verbatim decisive output line of the run (e.g. `Executed 42 tests, 0 failures`) — this is the receipt carried into the handover `receipt:` field (canonical definition in ticket-comment.md). Copy it exact, not paraphrased.
Do not assess coverage gaps until suite results are confirmed.

OUTPUT DOC
After test suite has run: load `<TICKET-ID>_output.md` from the Praetor impl_doc path.
Purpose: cross-check TEST COVERAGE section; confirm test_data and scenarios_covered match what Praetor declared.
Record the test results summary or gaps found in your handover block (D14: no NOTES section in the output doc).
Do not load the output doc before running the test suite — results must be independent.

CONSTRAINTS
Never form opinions before running the test suite
Never expand scope beyond files listed in Praetor expected_outputs (+ delta doc in revision)
Never carry Tribunus judgments into your assessment
Never carry state from a prior session — start cold (Law 3)
Never form opinions before all LOAD ORDER items are read
