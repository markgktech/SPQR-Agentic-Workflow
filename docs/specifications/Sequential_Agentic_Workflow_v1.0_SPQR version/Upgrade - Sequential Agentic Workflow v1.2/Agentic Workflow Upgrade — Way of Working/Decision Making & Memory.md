---

---
## When decisions happen

Decisions are made in Phase 3, one item at a time. The master goes through the flat item list built in Phase 2 and resolves each item: confirm, modify, descope, stall, or flag as unresolvable.

Decisions are saved to memory in real time — not at the end of the session. If context compacts or the session ends unexpectedly, no decision is lost.

---

## Binary state rule

Every item is either decided (with rationale saved) or explicitly flagged as open. There is no intermediate state. An item left ambiguous — "we'll see", "maybe", "depends" — is a silent failure that surfaces as a conflict during execution.

---

## Decision types

| Type | Meaning | Returns? | Action |
| --- | --- | --- | --- |
| Confirm | Item is valid as-is | — | Note rationale, save to memory |
| Modify | Valid but scope or approach changes | — | Document the delta, save to memory |
| Descoped | Out of scope for this upgrade | No — needs explicit owner decision to reopen | Flag, do not create ticket automatically |
| Stalled | Valid but could not be completed | Yes — becomes open item → new ticket | Flag as open item at wrap-up |
| Unresolvable | Cannot be decided without more information | Yes — becomes open item → new ticket | Flag as open item, do not block |

---

## Memory format

Every decision saved to memory includes:

- What was decided
- Why (rationale — one line minimum)
- Which file(s) or Notion page(s) are affected

Decisions without rationale are not valid saves — a future agent cannot evaluate edge cases without the why.

**Update-first rule:** before writing a new memory file, check if an existing one covers the same topic. Update the existing file rather than creating a duplicate. Stale memory is worse than no memory.

**Conflict rule:** if a new decision contradicts an existing memory entry, the newer decision takes precedence — but the conflict must be noted explicitly in the memory file. Silent overwrites are not allowed.

---

## What gets saved to memory vs Notion

**Memory (persistent across sessions):**

- Architectural decisions with lasting impact
- Scope boundaries and rules that apply across multiple groups
- Update to existing memory when a prior decision changes

**Notion upgrade doc (this upgrade only):**

- Item-level decisions that are execution-specific
- Group briefs
- Changes Made per group

---

## Open items

Items that cannot be resolved in Phase 3 are flagged immediately — they do not block progress. At wrap-up, each stalled or unresolvable item becomes a new DOC ticket. Owner assigns prefix and number after creation.