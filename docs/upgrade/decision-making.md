BINARY STATE RULE
Every item is either decided (rationale recorded) or explicitly flagged open. No intermediate state. "We'll see" / "maybe" / "depends" = silent failure that surfaces as conflict during execution.

DECISION TYPES
CONFIRM — item valid as-is | returns: no | record rationale in the run's PoC
MODIFY — valid but scope or approach changes | returns: no | document delta, record in the run's PoC
DESCOPED — out of scope for this upgrade | returns: no — requires explicit owner decision to reopen | flag; do not create ticket automatically
STALLED — valid but could not be completed | returns: yes → open item → new ticket | flag as open item at wrap-up
UNRESOLVABLE — cannot be decided without more information | returns: yes → open item → new ticket | flag as open item; do not block

DECISION FORMAT — PoC-FIRST
Decisions are recorded in the run's PoC (in the `poc/` lane, authored from `templates/poc_template.md`) — capture the question, answer, and rationale there FIRST. The execution brief is derived from the PoC afterwards (planning.md); the run container's MAIN folder-note LINKS the PoC via its `poc:` frontmatter and does not inline the decisions. Not in central memory. Each recorded decision must include:
- what: the decision made
- why: rationale (one line minimum)
- affected: which file(s) / run-container file(s) are impacted

DECISION RULES
in-repo: decisions live in the run's PoC markdown; do not write them to central Claude memory (it accrues stale data over time)
findable: tag cross-run, durable decisions (e.g. #decision) so they surface across runs via the vault (tags / Dataview / grep)
conflict: if a new decision contradicts an earlier one, the newer takes precedence; note the conflict explicitly where it is recorded
save-frequency: real time — not end of session; if context compacts or the session ends unexpectedly, no decision is lost
scope-split: all answered questions, decisions and rationale → the run's PoC (tagged, findable in the vault); group briefs and execution records (Changes Made) → the run container

OPEN ITEMS
Stalled and unresolvable items do not block Phase 3 progress. At wrap-up, each becomes a new SAW ticket — the owner creates it; Notion auto-assigns the ID.

NEVER
- leave any item in ambiguous state
- record a decision without rationale
- write decisions to central memory, or inline them into the run-container briefs, instead of the PoC
- silently overwrite a conflicting decision — note the conflict
- create tickets or assign ticket numbers — the owner creates the SAW ticket; Notion auto-assigns the ID
