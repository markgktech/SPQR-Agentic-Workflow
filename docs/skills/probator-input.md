LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text + all Notion comments — Praetor output is primary context)
4. collegium-veto.md
5. In revision flow only: delta doc child page linked in Praetor revision comment
6. probator-output.md

FRESH EYES
Load Praetor ticket comment as primary context.
Do not carry Tribunus findings into QA judgment — scope is tests and coverage, not code quality.
Tribunus comment is visible in the ticket but does not constrain your findings.

TEST PATH MAPPING
Identify every changed file from Praetor expected_outputs.
For each changed file: identify all code paths that require test coverage.
Reference [project-testing-guidelines] — What to Test / What Not to Test — before marking paths as in-scope.
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
Do not assess coverage gaps until suite results are confirmed.

IMPL DOC
After test suite has run: load impl doc child page from Praetor impl_doc URL.
Purpose: cross-check TEST COVERAGE section; confirm test_data and scenarios_covered match what Praetor declared.
Annotate PROBATOR NOTES section with test results summary or gaps found.
Do not load impl doc before running the test suite — results must be independent.

CONSTRAINTS
Never form opinions before running the test suite
Never expand scope beyond files listed in Praetor expected_outputs (+ delta doc in revision)
Never carry Tribunus judgments into your assessment
Never carry state from a prior session — start cold (Law 3)
Never form opinions before all LOAD ORDER items are read
