---
up: "[[v1.5]]"
group: "Warehouse Delta Close-Out (SAW-54)"
order: 20/21
tags: [group]
---

# Group 20 — Warehouse Delta Close-Out (SAW-54)

## Brief
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/20-warehouse-delta-closeout.md
REPO:          SPQR (generic only — never touch Foodoire)
RATIONALE:     One ticket (SAW-54) = force every session to declare warehouse-relevant knowledge change. Runs SECOND: rebases on group 19's applied hub close-out edits.
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-54-55-56 Session Close-Out & Write-Gate Hardening — PoC.md
PRE_FLIGHT:
  - docs/spqr_self/poc/SAW-54-55-56 Session Close-Out & Write-Gate Hardening — PoC.md (D1, D2, D3, D4)
  - docs/skills/ticket-comment.md (READ AFTER group 19 has applied its HUB CLOSE-OUT subsection — note the existing `warehouse_trace:` field; your `warehouse_delta:` pointer mirrors its terse pattern)
  - docs/agents/senate.md (CENSURA — note C-56 already appended by group 19; append C-54 below it)
  - docs/skills/censura-output.md (Censura checklist)
  - docs/skills/warehouse-ingest.md (owner-approval / no-auto-ingest discipline — SHARED with group 21; you own the ingest-disposition anchor)

### Scope (SAW-54 items)
1. Add a mandatory `## Warehouse Delta` section to every session close-out (structure: Status `none | candidates-present | proposals-authored | deferred`; Changed knowledge — Decisions/Constraints/Lessons/Supersedes; Recommended disposition; Owner-facing summary).
2. Require explicit `none` when no delta exists, with a one-line rationale. "Missing Warehouse Delta is a close-out defect. `none` is valid only with a short rationale."
3. Censura validation: verify the Warehouse Delta section exists and is credible; if `none`, confirm no durable decision/constraint/lesson/supersession was introduced; if candidates exist, verify owner-understandable + dispositioned.
4. Documentation states owner approval is required before antechamber proposal or canonical ingest (NOT automatic ingest).

### FILES
- `docs/skills/ticket-comment.md`: add a canonical **WAREHOUSE DELTA — SHARED** subsection (the full section structure from item 1 + the explicit-`none`-with-rationale rule from item 2). Per D2 + D2b LOCATION FALLBACK: add a terse one-line `warehouse_delta:` field to the handover block FORMAT (mirrors `warehouse_trace:`), pointing to disposition status (`none | candidates | proposals | deferred`). **Location of the FULL section depends on whether the stage has an output doc:**
  - **Session produces a separate output doc** → the full `## Warehouse Delta` lives in that output doc; the handover carries only the terse `warehouse_delta:` pointer.
  - **Session does not produce a separate output doc** → the full `## Warehouse Delta` lives in the **handover block itself**, regardless of agent role. A session may NOT omit the full delta just because it wrote no output doc. The rule keys on the artifact, never the role — do not assume any role always has an output doc. State this artifact-based rule explicitly in the shared subsection.
  Define ONCE here; output skills reference.
- `docs/agents/senate.md`: CENSURA checklist — append item **C-54** (D3 order, SECOND — directly BELOW C-56): "Verify Warehouse Delta is present; if `none`, confirm no durable decision/constraint/lesson/supersession was introduced; if candidates exist, verify they are owner-understandable and dispositioned. Owner approval required before antechamber proposal or canonical ingest — no auto-ingest."
- `docs/skills/censura-output.md`: add the matching C-54 checklist line below C-56.
- `docs/skills/warehouse-ingest.md`: add the explicit rule that owner approval is required before an antechamber proposal or canonical ingest is treated as accepted knowledge (item 4 — reinforces the no-auto-ingest principle; the Warehouse Delta declaration is NOT an ingest trigger). Anchor at the ingest-disposition / owner-HITL area only.

### COORDINATION RULES (serialized — group 20 runs SECOND, after 19)
- You OWN: the **WAREHOUSE DELTA — SHARED** subsection (incl. the D2b output-doc-vs-handover location fallback) + the `warehouse_delta:` handover field, checklist item **C-54**, and the no-auto-ingest note in `warehouse-ingest.md`.
- Do NOT touch group 19's HUB CLOSE-OUT subsection or the hub session-row contract. Do NOT touch the `receipt:` field or add write-gate receipt fields (those are group 21 / SAW-55).
- In the Censura checklist, C-56 already exists — append C-54 immediately below it; leave room for C-55 below yours. Do not renumber or merge.
- `warehouse-ingest.md` is SHARED with group 21: you own the **owner-approval/no-auto-ingest** anchor; group 21 owns the **write-gate (check/reconcile)** anchor. Stay in your anchor.
- Additive only.

### ACCEPTANCE MAPPING (SAW-54 — kept separate, do not merge with 55/56)
- [ ] Every relevant agent/session close-out template requires a Warehouse Delta section.
- [ ] `Warehouse Delta: none` is explicitly allowed only with rationale.
- [ ] Candidate deltas require recommended disposition but not automatic ingest.
- [ ] Censura checklist validates the section (C-54).
- [ ] Documentation states owner approval is required before antechamber proposal or canonical ingest.

## Changes Made — _(executed 2026-06-25, GREEN — master-verified)_
- `docs/skills/ticket-comment.md`: terse `warehouse_delta:` field added to handover FORMAT + FIELD RULES (below `warehouse_trace:`); new canonical **WAREHOUSE DELTA — SHARED (SAW-54)** subsection (full `## Warehouse Delta` structure, explicit-`none`-with-rationale rule, **D2b location fallback, ARTIFACT-based (owner-clarified 2026-06-25)** — if the session produces a separate output doc, the full section lives there + terse handover pointer; if the session does not produce a separate output doc, the full section lives in the handover block itself, regardless of role — the rule keys on the artifact, never the role).
- `docs/agents/senate.md`: CENSURA item **C-54** appended below C-56 (Warehouse Delta present+credible; `none` only with rationale; candidates dispositioned; owner approval before proposal/ingest — no auto-ingest).
- `docs/skills/censura-output.md`: matching C-54 line.
- `docs/skills/warehouse-ingest.md`: **OWNER APPROVAL BEFORE ACCEPTANCE — NO AUTO-INGEST (SAW-54)** note in ANTECHAMBER DISCIPLINE.
- Additive; `receipt:` untouched; C-55 marker + write-gate anchor left for group 21. All 5 SAW-54 acceptance criteria satisfied; D2b fallback explicit.
