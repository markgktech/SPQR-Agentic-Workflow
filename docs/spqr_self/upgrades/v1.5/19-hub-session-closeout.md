---
up: "[[v1.5]]"
group: "Hub Session Close-Out (SAW-56)"
order: 19/21
tags: [group]
---

# Group 19 — Hub Session Close-Out (SAW-56)

## Brief
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/19-hub-session-closeout.md
REPO:          SPQR (generic only — never touch Foodoire)
RATIONALE:     One ticket (SAW-56) = make hub close-out deterministic + part of the session contract. Runs FIRST: it hardens the hub/close-out skeleton the other two extend.
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-54-55-56 Session Close-Out & Write-Gate Hardening — PoC.md
PRE_FLIGHT:
  - docs/spqr_self/poc/SAW-54-55-56 Session Close-Out & Write-Gate Hardening — PoC.md (D1, D2, D3, D4 — read first; do not re-decide)
  - docs/skills/ticket-comment.md (canonical HANDOVER protocol — note the SAW-26 receipt precedent: define once, reference DRY)
  - docs/agents/senate.md (CENSURA section)
  - docs/skills/censura-output.md (Censura checklist)
  - docs/skills/praetor-output.md / probator-output.md / curator-output.md / tribunus-output.md / quaestor-relatio-output.md / quaestor-doc-execute.md / censura-output.md (existing hub `## Session / cost` row writers — reference, do not rewrite each)

### Scope (SAW-56 items)
1. Deterministic hub close-out requirement: every agent session updates the relevant ticket hub before stopping (when a hub exists). Required row fields: session role/agent, phase/stage, session_id, verdict/status, artifact links, next routing/owner action, cost/token placeholders.
2. Cost placeholder rule: if exact cost/tokens unavailable, write `owner-fill` / `pending owner entry` — **never omit the session row**.
3. Hub stays navigational; detailed evidence stays in handover/output. ("The hub records status, session lineage, routing, and links. Detailed receipts/evidence belong in the handover.")
4. Censura validation: hub session/status row exists, references the correct handover/output artifacts, and matches actual routing/verdict.

### FILES
- `docs/skills/ticket-comment.md`: add a canonical **HUB CLOSE-OUT — SHARED** subsection (the required session-row field contract from item 1 + the cost-placeholder rule from item 2 + the hub=navigational / evidence-in-handover guidance from item 3). Define ONCE here (SAW-26 pattern); the per-agent output skills reference it.
- `docs/agents/senate.md`: CENSURA checklist — add item **C-56** (D3 order, FIRST): "Verify the hub session/status row exists, references the correct handover/output artifacts, and matches the actual routing/verdict."
- `docs/skills/censura-output.md`: add the same C-56 checklist item to the Censura output checklist (keep wording aligned with senate.md; do not restate detail twice — one is the mandate, one the checklist line).
- (OPTIONAL, only if an output skill would otherwise not enforce the new required fields) a one-line pointer in the specific `*-output.md` to the new HUB CLOSE-OUT — SHARED subsection. No full-rule restatement.

### COORDINATION RULES (serialized — group 19 runs FIRST)
- You OWN: the new **HUB CLOSE-OUT — SHARED** subsection in `ticket-comment.md`, checklist item **C-56**, and the hub session-row contract. Edit only these.
- Do NOT add a Warehouse Delta field/section (SAW-54, group 20) or write-gate receipt fields (SAW-55, group 21). Leave the `receipt:` and `warehouse_trace:` fields as-is.
- In the Censura checklist, append C-56 as its own line and **leave room** after it: groups 20 and 21 will append C-54 then C-55 below yours. Do not renumber or merge.
- Additive only — never overwrite an existing block. Hub session-row writers already exist; harden/canonicalize, do not duplicate.

### ACCEPTANCE MAPPING (SAW-56 — kept separate, do not merge with 54/55)
- [ ] Agent close-out requires hub status/session row update when a hub exists.
- [ ] Session row includes session_id, role, status/verdict, artifacts, routing, and cost placeholders.
- [ ] Missing cost data uses explicit owner-fill placeholders.
- [ ] Detailed evidence remains in handover/output, not overloaded into hub.
- [ ] Censura validates hub/handover consistency (C-56).

## Changes Made — _(executed 2026-06-25, GREEN — master-verified)_
- `docs/skills/ticket-comment.md`: new canonical **HUB CLOSE-OUT — SHARED (SAW-56)** subsection — required session-row field contract (role/phase/session_id/verdict/artifacts/routing/cost), COST PLACEHOLDER RULE (`owner-fill`, never omit the row), HUB = NAVIGATIONAL guidance, CONSTRAINTS. Defined ONCE (SAW-26 precedent).
- `docs/agents/senate.md`: CENSURA CHECKLIST block — item **C-56** (hub row exists, references correct handover/output artifacts, matches routing/verdict).
- `docs/skills/censura-output.md`: matching CLOSE-OUT CHECKLIST line C-56.
- Additive; `receipt:`/`warehouse_trace:` untouched; markers left for C-54/C-55. All 5 SAW-56 acceptance criteria satisfied.
