---

---
## Affected Files

- `docs/skills/quaestor-relatio.md` — UPDATE (items #12, #14, #16, #18)
- `docs/skills/quaestor-relatio-output.md` — UPDATE (items #13, #15, #17)
- `docs/skills/consilium-output.md` — UPDATE (item #11)

> All 8 items are independent — no dependencies between them. Can be applied in any order.

---

## Item #11 — expected_outputs → Ticket Body

**What:** Notion MCP truncates comments at ~4000 chars — expected_outputs get cut off and Quaestor misses scope. Move expected_outputs from Consilium comment to ticket body Handoff section.

**Where:**

- `docs/skills/consilium-output.md` → write expected_outputs to ticket body Handoff section, not comment
- `docs/skills/quaestor-relatio.md` → pre-flight load order item 5: read expected_outputs from ticket body, not comment

---

## Item #12 — Web Search Date Validation

**What:** Before any web search, agent checks today’s date and orients queries to current date. Prevents outdated data presented as current.

**Where:** `docs/skills/quaestor-relatio.md` → RESEARCH section — add step before first search: verify today’s date, orient all queries accordingly

---

## Item #13 — Handoff Accuracy Rule

**What:** Handoff expected_outputs may only list items that were actually executed. “Note added” / “applied” language forbidden unless the change was literally made in this session.

**Where:** `docs/skills/quaestor-relatio-output.md` → NEVER section — add: never use “note added” or “applied” language for changes not made in this session

---

## Item #14 — Position Reversal Flag

**What:** If agent changes position on a topic more than once, must explicitly flag to owner: “I have revised this answer X times — topic may require dedicated spike.” Must not quietly produce a third answer.

**Where:** `docs/skills/quaestor-relatio.md` → DISCUSSION section — add position reversal rule with explicit flag requirement

---

## Item #15 — Decision Sourcing Label

**What:** If a decision comes from owner consultation or another agent session (not Quaestor research), label it explicitly in spike document. Not to be presented as Quaestor research finding.

**Where:** `docs/skills/quaestor-relatio-output.md` → add sourcing label rule: decisions from owner or external sessions must be marked as such

---

## Item #16 — Context Window Alert

**What:** At 80% context, agent must alert owner. Rule existed in skill but was not followed. Reinforce as hard NEVER: never reach 100% without alerting.

**Where:** `docs/skills/quaestor-relatio.md` → NEVER section — add: never reach 100% context without alerting owner at 80%

---

## Item #17 — Spike Document Location

**What:** Spike documents created under Exploracio (Spiking) Notion page — not as child page of dev ticket. Link back to ticket via Ticket property in header table.

**Where:** `docs/skills/quaestor-relatio-output.md` → spike doc creation step: parent = Exploracio/Spiking (`36c68d5de1e880368560e60a35097ee1`); add Ticket property linking back to dev ticket; announce created page URL in output

---

## Item #18 — Discussion Depth Calibration

**What:** HIGH impact or HARD TO REVERSE topics must not be closed unilaterally. Agent must offer alternative, surface uncertainty, or request explicit owner confirmation before marking closed.

**Where:** `docs/skills/quaestor-relatio.md` → DISCUSSION section — add: HIGH impact or HARD TO REVERSE topics require explicit owner confirmation before closing

---

## Changes Made

- `docs/skills/consilium-output.md` → expected_outputs removed from comment block → new TICKET BODY HANDOFF section; EXPLORACIO HANDOFF NOTE Pass 1 updated to ticket body source; NEVER: "Never omit expected_outputs from ticket body Handoff section"
- `docs/skills/quaestor-relatio.md` → pre-flight item 5: read expected_outputs from ticket body, not comment; RESEARCH: date validation rule added; DISCUSSION: position reversal flag rule added; DISCUSSION: "before marking closed" → "before the owner closes discussion"; redundant "If context window filling" line removed; NEVER section added: "Never reach 100% context without alerting owner at 80%"
- `docs/skills/quaestor-relatio-output.md` → RECORD DECISIONS: decision sourcing label rule added; SPIKE DOCUMENT: parent → Exploracio/Spiking (36c68d5de1e880368560e60a35097ee1) + Ticket backlink + URL report; NEVER: "note added/applied/updated" language rule; NEVER: "Never present external decisions as Quaestor research findings"; Group 1 TICKET PROPOSALS preserved intact