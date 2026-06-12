---

---
## Affected Files

- `consilium-input.md` — new file (`docs/skills/`)
- `curator-output.md` — update (existing)
- `session-starters.md` — update (existing)
- Notion Dev Tickets DB — schema change (one-time manual setup: self-referential relation property)

---

## Item 2.7a — Parent Ticket Relation

**What:** Tickets can reference a parent ticket via a self-referential relation property in the Notion Dev Tickets DB. Consilium loads the parent chain at session start for context. When creating new tickets (follow-ups, sub-tickets), the agent automatically sets the current ticket as parent.

**Schema setup:** One-time manual step — owner adds self-referential relation property to Dev Tickets DB in Notion (Add property → Relation → same database). **Prerequisite: must be done before the first v1.1 ticket runs.** Existing tickets get an empty parent field — no retroactive parenting required, but can be set manually if needed.

**Parent chain traversal logic (Consilium pre-flight):**

1. Walk up the parent chain
2. Stop when: SPIKE found — or — 3 levels reached — or — no more parent exists
3. If current ticket is itself a SPIKE: check one level up for a parent SPIKE

**New ticket creation:** When Consilium or Censura creates a follow-up ticket, the current ticket is automatically set as parent via Notion MCP relation property.

**Where:** `consilium-input.md` → pre-flight section: parent chain traversal + load

---

## Item 6.6 — [CLAUDE.md](http://claude.md/) Update Proposal

**What:** When Curator identifies a genuine pattern change or new architectural invariant from the current ticket, it proposes an exact [CLAUDE.md](http://claude.md/) update in its output. Owner decides whether to apply it and writes it manually. Agents never write to [CLAUDE.md](http://claude.md/) directly.

**Trigger condition:** Only when Curator identifies a pattern change or new invariant — not on every ticket. If nothing meaningful changed, no proposal is generated.

**Constraints:**

- Max 1-2 proposals per ticket run
- Scope: only what the current ticket revealed — no general cleanup
- Format: exact proposed text in diff format (not a description)
- Types allowed: new rule addition, clarification of existing rule — deletion only with explicit justification

**Where:** `curator-output.md` → conditional section: [CLAUDE.md](http://claude.md/) update proposal (only when triggered)

---

## Item 9.2 — Standalone Debugging Tribunus

**What:** Tribunus extracted from the pipeline as an on-demand tool. Owner can run it anytime on any code — no ticket, no Praetor, no impl doc required. Owner defines the scope at session start (file, function, error message, or any code fragment).

**When useful:**

- Quick fresh-eyes review on manually written code
- Debugging a specific file or function outside of a ticket flow
- Reviewing existing code that didn’t come from a ticket
- Fast “what’s wrong with this” question

**Toolset:** Read + `Bash(swiftlint *)` — same as pipeline Tribunus

**Output:** Findings list — no veto authority (no pipeline to block), no ticket comment written

**Where:** `session-starters.md` → new dedicated entry: Standalone Debugging Tribunus with scope prompt template