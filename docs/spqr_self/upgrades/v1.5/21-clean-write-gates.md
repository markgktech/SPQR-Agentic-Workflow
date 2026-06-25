---
up: "[[v1.5]]"
group: "Clean Warehouse Write Gates (SAW-55)"
order: 21/21
tags: [group]
---

# Group 21 — Clean Warehouse Write Gates (SAW-55)

## Brief
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/21-clean-write-gates.md
REPO:          SPQR (generic only — never touch Foodoire)
RATIONALE:     One ticket (SAW-55) = clean-in/clean-out discipline around warehouse write gates. Runs THIRD/LAST: extends the existing receipt discipline; rebases on groups 19+20.
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-54-55-56 Session Close-Out & Write-Gate Hardening — PoC.md
PRE_FLIGHT:
  - docs/spqr_self/poc/SAW-54-55-56 Session Close-Out & Write-Gate Hardening — PoC.md (D1, D2, D3, D4)
  - docs/skills/ticket-comment.md (READ AFTER groups 19+20 applied — note the existing `receipt:` FIELD RULES incl. the warehouse-write receipt; you EXTEND it, not replace)
  - docs/skills/warehouse-usage.md (`reconcile` · `check` · `reconcile-antechamber` verbs — owner/maintenance row; the divergence-check semantics)
  - docs/skills/warehouse-ingest.md (write path — SHARED with group 20; you own the write-gate anchor)
  - docs/agents/senate.md (CENSURA — note C-56 + C-54 already appended; append C-55 below)
  - docs/skills/censura-output.md (Censura checklist)

### Scope (SAW-55 items)
1. Pre-write clean check: before `propose`, `revise`, `resolve`, manifest/scope-vocabulary edit, or G3 verification — run `check`; if clean continue; if FTS/index divergence, run non-fresh `reconcile` → `reconcile-antechamber` → `check`; if still not clean, BLOCK.
2. Post-write leave-clean invariant: after any warehouse/antechamber/manifest mutation — run `check`; if non-clean due to index/projection divergence, non-fresh `reconcile` + `reconcile-antechamber` + `check`; stop only from clean state or report BLOCK.
3. Explicitly forbid unsanctioned `--fresh`: never a default repair path. "`--fresh` requires explicit owner authorization because it drops trace/grant/mirror state."
4. Require receipts: command run; exit code; final `check` result; pending/proposed count if relevant; whether reconcile was needed; confirmation that no `--fresh` was used.

### FILES
- `docs/skills/warehouse-usage.md`: add the pre-write gate (item 1), post-write leave-clean invariant (item 2), and the `--fresh` owner-only rule (item 3). This is the natural home — it already documents `reconcile`/`check`/`reconcile-antechamber` as owner/maintenance verbs. **RESOLVE THE MATRIX TENSION (owner amendment 2):** the existing matrix row marks `reconcile`/`check`/`reconcile-antechamber` as `owner / maintenance | owner-run`. For the write-gate pre/post-cleaning context, make **non-fresh `reconcile` + `reconcile-antechamber` a SANCTIONED agent-executed maintenance step** when `check` reports index/projection divergence — the agent may run them to restore a clean projection without owner HITL. Reconcile the matrix wording so it no longer reads as blanket owner-only for this path (e.g. annotate the row / add the write-gate exception); `--fresh` remains explicit owner-authorization only and is NOT covered by this sanction.
- `docs/skills/warehouse-ingest.md`: add a pointer at the write path that `propose`/`revise`/`resolve` are gated by the pre/post-write clean check defined in `warehouse-usage.md` (write-gate anchor — SHARED file, your anchor only).
- `docs/skills/ticket-comment.md`: EXTEND the existing `receipt:` FIELD RULES — add the write-gate receipt fields (item 4) for warehouse-mutating sessions: command run, exit code, final `check` result, pending/proposed count if relevant, reconcile-needed flag, no-`--fresh` confirmation. Do NOT create a separate block — extend the canonical receipt definition.
- `docs/agents/senate.md`: CENSURA checklist — append item **C-55** (D3 order, THIRD — directly BELOW C-54): "For any warehouse-mutating session, verify the write-gate receipt is present (command, exit code, final check result, reconcile-needed, no-`--fresh`). Missing receipt → YELLOW/FAIL."
- `docs/skills/censura-output.md`: add the matching C-55 checklist line below C-54.

### COORDINATION RULES (serialized — group 21 runs LAST, after 19+20)
- You OWN: the write-gate rules in `warehouse-usage.md`, the write-gate anchor in `warehouse-ingest.md`, the `receipt:` EXTENSION in `ticket-comment.md`, and checklist item **C-55**.
- Do NOT touch group 19's HUB CLOSE-OUT subsection / hub row, or group 20's WAREHOUSE DELTA subsection / `warehouse_delta:` field / no-auto-ingest note. In `warehouse-ingest.md`, group 20 owns the owner-approval/no-auto-ingest anchor — stay in your write-gate anchor.
- Extend the existing `receipt:` definition in place; do not duplicate or fork it (it is the canonical SAW-26 receipt rule).
- In the Censura checklist, append C-55 below C-54 (last). Do not renumber or merge.
- Non-fresh `reconcile` + `reconcile-antechamber` = sanctioned agent-executed write-gate maintenance (amendment 2). `--fresh` stays owner-authorized only — do not weaken. No Foodoire edits.

### ACCEPTANCE MAPPING (SAW-55 — kept separate, do not merge with 54/56)
- [ ] Pre-write check is required before propose, revise, resolve, manifest edit, and G3 verification.
- [ ] Post-write check is required after warehouse-mutating sessions.
- [ ] Non-fresh reconcile recovery path is documented.
- [ ] `--fresh` is explicitly owner-authorized only.
- [ ] Censura can fail/YELLOW a session that lacks the required write-gate receipt (C-55).

## Changes Made — _(executed 2026-06-25, GREEN — master-verified)_
- `docs/skills/warehouse-usage.md`: new **§5 Clean warehouse write gates (SAW-55)** — pre-write clean check (item 1), post-write leave-clean invariant (item 2), `--fresh` owner-only rule (item 3), receipt pointer. **D7 matrix tension resolved**: the `reconcile`/`check`/`reconcile-antechamber` row + a Notes carve-out now make non-fresh `reconcile` + `reconcile-antechamber` sanctioned agent-executed maintenance on the write-gate path; `--fresh` kept owner-only.
- `docs/skills/warehouse-ingest.md`: **WRITE-GATE CLEAN CHECK (SAW-55)** pointer at the WRITE PATH (distinct anchor from SAW-54's ANTECHAMBER note).
- `docs/skills/ticket-comment.md`: canonical `receipt:` FIELD RULE **extended in place** (not forked) with write-gate receipt fields (a)–(f): command, exit code, final `check` result, pending/proposed count, reconcile-needed, no-`--fresh` confirmation.
- `docs/agents/senate.md` + `docs/skills/censura-output.md`: item **C-55** appended below C-54; both now-consumed stale markers removed → clean C-56/C-54/C-55 list.
- Additive (except sanctioned marker cleanup); groups 19/20 content untouched. All 5 SAW-55 acceptance criteria satisfied.
- ⚠ Master note: terminology overlap — "write gate" (B4 hard-schema/ingest authority) vs SAW-55 "write gates" (clean-check); low severity, owner-flagged for optional Censura adjudication / rename.
