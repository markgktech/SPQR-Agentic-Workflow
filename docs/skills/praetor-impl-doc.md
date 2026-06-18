OUTPUT DOC — CREATE (D3)
Create the local file `<TICKET-ID>_output.md` in the ticket's work_documents/ vault (not a Notion child page).
Reference its path in the handover block as the impl_doc field.
Load this skill before creating the file.

TEMPLATE

---
up: "[[<TICKET-ID>]]"
tags: [content/implementation-doc]
---

TICKET: [[<TICKET-ID>]]
SUMMARY: [2-3 sentences — what was built and the approach taken]

---

**FILES CHANGED**
[file] — [what changed and why; reference Consilium decision if applicable]

---

**KEY DECISIONS**
[decision] — [why this approach; what alternatives were rejected]

---

**CODE SNIPPETS**
[label — what this illustrates]
[snippet]

---

**TEST COVERAGE**
tests_written: [test file — method names]
test_data: [specific values used for edge case tests]
scenarios_covered: [nil / boundary / error state — per changed file]

---

**VERIFICATION (RECEIPT)**
build: [verbatim — `<build command> → <decisive stdout line>` (e.g. `BUILD SUCCEEDED`)]
lint: [verbatim — `<lint command> → <decisive stdout line>` (e.g. `0 violations`)]
[the receipt = the exact decisive tool-output line, not paraphrase; scoped to the decisive line, not the full log — canonical definition in ticket-comment.md. The compact line(s) also go in the handover `receipt:` field.]

---

**KNOWN GAPS**
[anything uncertain, incomplete, or flagged for follow-up]

FILL RULES
frontmatter: minimal — `up: "[[<TICKET-ID>]]"` linking the hub + the single `content/implementation-doc` tag; nothing else (the hub owns identity)
SUMMARY: implementation approach — not a restatement of the ticket title
FILES CHANGED: every file touched including single-line changes; include why, not just what
KEY DECISIONS: non-obvious choices only; pattern-following = omit
CODE SNIPPETS: tricky logic, novel patterns, non-obvious fixes; not boilerplate
TEST COVERAGE: mandatory even if no new tests — state "no new tests; existing suite covers [X]"
VERIFICATION (RECEIPT): mandatory for any build/lint claim — paste the verbatim decisive line(s) (`<command> → <decisive stdout>`); never paraphrase; never omit to save tokens (quality floor)
KNOWN GAPS: honest; do not omit to appear complete
Reviewer findings: NOT in this file (D14) — reviewers append their blocks to `<TICKET-ID>_handover.md`; the output carries no NOTES sections

CONSTRAINTS
Never omit TEST COVERAGE — state coverage status even if unchanged
Never omit VERIFICATION (RECEIPT) on a build/lint claim — verbatim decisive line(s), never paraphrased
Never omit FILES CHANGED — every touched file listed
Never add reviewer NOTES sections — reviewer findings live in the handover (D14)
Never create the output doc before implementation is complete
