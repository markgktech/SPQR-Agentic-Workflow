CODE REVIEW CHECKLIST
Apply per changed file. Each item: PASS / FAIL / NA.
NA only if the file does not touch that area — justify NA if non-obvious.

PROJECT CRITICAL RULES
Load CLAUDE.md — verify each Critical Rule applies to changed files.
[ ] [Populate from CLAUDE.md Critical Rules for this project]

CONVENTIONS
[ ] Naming: follows the active naming constraints/decisions in the warehouse (query per the WAREHOUSE QUERY POLICY)
[ ] File placement: file name matches primary type; correct folder per project structure
[ ] Patterns: architectural patterns followed per active warehouse constraints/decisions
[ ] Dependency injection: services/dependencies injected per project conventions — no singletons
[ ] Localization: no hard-coded user-facing strings — project localization system only
[ ] Logging: correct logging category/level used — no raw print/console calls in production paths
[ ] No unused imports, dead variables, or unreachable code introduced
