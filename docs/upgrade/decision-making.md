BINARY STATE RULE
Every item is either decided (rationale saved) or explicitly flagged open. No intermediate state. "We'll see" / "maybe" / "depends" = silent failure that surfaces as conflict during execution.

DECISION TYPES
CONFIRM — item valid as-is | returns: no | save rationale to memory
MODIFY — valid but scope or approach changes | returns: no | document delta, save to memory
DESCOPED — out of scope for this upgrade | returns: no — requires explicit owner decision to reopen | flag; do not create ticket automatically
STALLED — valid but could not be completed | returns: yes → open item → new ticket | flag as open item at wrap-up
UNRESOLVABLE — cannot be decided without more information | returns: yes → open item → new ticket | flag as open item; do not block

MEMORY FORMAT
Each saved decision must include:
- what: the decision made
- why: rationale (one line minimum)
- affected: which file(s) or Notion page(s) are impacted

MEMORY RULES
update-first: check existing memory files before creating new; update, do not duplicate
conflict: if new decision contradicts existing entry, newer takes precedence; note conflict explicitly in the file
save-frequency: real time — not end of session; if context compacts or session ends unexpectedly, no decision is lost
scope-split: cross-group architectural decisions and scope rules that apply beyond this upgrade → persistent memory; item-level execution decisions and group briefs → Notion upgrade doc only

OPEN ITEMS
Stalled and unresolvable items do not block Phase 3 progress. At wrap-up, each becomes a new DOC ticket. Owner assigns prefix and number after creation.

NEVER
- leave any item in ambiguous state
- save a decision without rationale
- create a new memory file when an existing one covers the topic
- silently overwrite a conflicting memory entry
- create tickets with assigned prefixes or numbers
