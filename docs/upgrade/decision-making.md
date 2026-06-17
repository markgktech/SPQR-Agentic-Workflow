BINARY STATE RULE
Every item is either decided (rationale recorded) or explicitly flagged open. No intermediate state. "We'll see" / "maybe" / "depends" = silent failure that surfaces as conflict during execution.

DECISION TYPES
CONFIRM — item valid as-is | returns: no | record rationale in the run container
MODIFY — valid but scope or approach changes | returns: no | document delta, record in the run container
DESCOPED — out of scope for this upgrade | returns: no — requires explicit owner decision to reopen | flag; do not create ticket automatically
STALLED — valid but could not be completed | returns: yes → open item → new ticket | flag as open item at wrap-up
UNRESOLVABLE — cannot be decided without more information | returns: yes → open item → new ticket | flag as open item; do not block

DECISION FORMAT
Decisions are recorded in the run container (the MAIN folder-note, or the relevant group sub-md), not in central memory. Each recorded decision must include:
- what: the decision made
- why: rationale (one line minimum)
- affected: which file(s) / run-container file(s) are impacted

DECISION RULES
in-repo: decisions live in the run container markdown; do not write them to central Claude memory (it accrues stale data over time)
findable: tag cross-run, durable decisions (e.g. #decision) so they surface across runs via the vault (tags / Dataview / grep)
conflict: if a new decision contradicts an earlier one, the newer takes precedence; note the conflict explicitly where it is recorded
save-frequency: real time — not end of session; if context compacts or the session ends unexpectedly, no decision is lost
scope-split: cross-run, durable architectural decisions and scope rules → tagged in the run container (findable in the vault); item-level execution decisions and group briefs → the run container only

OPEN ITEMS
Stalled and unresolvable items do not block Phase 3 progress. At wrap-up, each becomes a new SAW ticket — the owner creates it; Notion auto-assigns the ID.

NEVER
- leave any item in ambiguous state
- record a decision without rationale
- write decisions to central memory instead of the run container
- silently overwrite a conflicting decision — note the conflict
- create tickets or assign ticket numbers — the owner creates the SAW ticket; Notion auto-assigns the ID
