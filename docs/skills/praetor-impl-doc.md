IMPL DOC — CREATE
Create Notion child page under the ticket: title "Implementation Notes — [TICKET-ID]"
Link impl doc URL in ticket comment as impl_doc field.
Load this skill before creating the child page.

TEMPLATE

TICKET: [ID + Notion link]
SUMMARY: [2-3 sentences — what was built and the approach taken]

FILES CHANGED
[file] — [what changed and why; reference Consilium decision if applicable]

KEY DECISIONS
[decision] — [why this approach; what alternatives were rejected]

CODE SNIPPETS
[label — what this illustrates]
[snippet]

TEST COVERAGE
tests_written: [test file — method names]
test_data: [specific values used for edge case tests]
scenarios_covered: [nil / boundary / error state — per changed file]

KNOWN GAPS
[anything uncertain, incomplete, or flagged for follow-up]

--- TRIBUNUS NOTES ---

--- PROBATOR NOTES ---

--- CURATOR NOTES ---

FILL RULES
SUMMARY: implementation approach — not a restatement of the ticket title
FILES CHANGED: every file touched including single-line changes; include why, not just what
KEY DECISIONS: non-obvious choices only; pattern-following = omit
CODE SNIPPETS: tricky logic, novel patterns, non-obvious fixes; not boilerplate
TEST COVERAGE: mandatory even if no new tests — state "no new tests; existing suite covers [X]"
KNOWN GAPS: honest; do not omit to appear complete
NOTES sections: leave blank — reviewer territory

CONSTRAINTS
Never omit TEST COVERAGE — state coverage status even if unchanged
Never omit FILES CHANGED — every touched file listed
Never fill NOTES sections — reviewer territory
Never create impl doc before implementation is complete
