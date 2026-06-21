---
up: "[[v1.5]]"
group: "Warehouse robot propagation (SAW-44)"
order: 14/14
tags: [group]
---

# Group 14 — Warehouse robot propagation (SAW-44)

## Brief

GROUP: Warehouse robot propagation (SAW-44)
ORDER: 14/14
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/14-warehouse-robot-propagation.md
RATIONALE: two generic-side markdown edits (manifest + propagation agent); no code (AM4); deliberately minimal scope per owner.
FILL_CHANGES_MADE: yes
PRE_FLIGHT:
  docs/spqr_self/poc/SAW-44 Warehouse Robot Propagation — PoC.md   (authoritative for CONTENT — D1/D2/D3)
  docs/upgrade/propagation-manifest.md   (the file to edit — current classification, DEFERRED warehouse_robot block)
  docs/upgrade/propagation-agent.md      (the file to edit — PIPELINE, NEVER list, STATUS MODE)
  docs/spqr_self/poc/SPQR_Propagation_Mechanism_PoC.md   (SAW-38 — the deferred note D1 supersedes)
CONVENTIONS (mandatory — match existing form, do not invent a new shape):
  - Edit in place; mirror the existing section style of each file. No new top-level structure.
  - Keep it minimal — this scope was explicitly simplified with the owner. No number-comparison/robot-command machinery; no executable code (AM4).

FILES:
  docs/upgrade/propagation-manifest.md:
    - Move `warehouse_robot/` from DEFERRED into `propagate` (CORE) as a directory line (D1). It carries no per-project tokens, so it is a plain source copy.
    - State the copy is **tracked source only** (e.g. the agent's copy set = `git ls-files warehouse_robot/`): never the generated/derived artifacts (`index.sqlite*`, `__pycache__/`, `*.pyc`, `.pytest_cache/`). `tests/`, `fixtures/`, `docs/` (the robot's own) travel with it.
    - Replace the DEFERRED block with a one-line note that this **supersedes the SAW-38 deferred "out-of-band" note** (ref SAW-44) — so the reversal is explicit, not silent.
    - Confirm the project's warehouse data (`nodes/`, `flags/`, `warehouse.config.json`) stays `project-owned` and is never written/deleted (unchanged — restate only if it sharpens the boundary).
  docs/upgrade/propagation-agent.md:
    - PIPELINE step 3 (token re-instantiation + drift check): add that **verbatim/code paths (warehouse_robot/) skip token re-instantiation and the token-absence fail-loud**, and their drift check is a plain compare. RATIONALE: the robot's source contains regex literals like `[a-z][a-z0-9-]*` that the token-absence rule (AM3) would otherwise halt on. This is required for the plain copy to work — it is not extra machinery.
    - Add the D3 stop rule. Cleanest placement: a PIPELINE note + a NEVER-list line. Wording target: "Propagation copies `warehouse_robot/`; it NEVER runs the robot (no `init`/ingest/fold/reconcile). If this version's release notes flag a warehouse note-format change, HALT at the warehouse step: tell the owner a migration is required, do not migrate, and do not write the version stamp." (D3)

OUT OF SCOPE (do not do): build the migration engine; build any number-comparison or robot-reported-version mechanism; touch any consuming project or its warehouse data; write executable code; edit warehouse_robot/ itself.

## Changes Made

Two generic-side markdown files edited; no executable code (AM4). All content derived from the SAW-44 PoC (D1/D2/D3).

### `docs/upgrade/propagation-manifest.md` (3 edits)

1. **D1 — `warehouse_robot/` promoted to `propagate` (CORE).** Added as a directory line under CORE: it carries no per-project tokens (per-instance identity lives in the project's `warehouse.config.json`), so it is a plain source copy, not a token re-instantiation. Copy set stated as **tracked source only** (`git ls-files warehouse_robot/` — package + its own `docs/`, `fixtures/`, `tests/`), explicitly **never** the generated/derived artifacts (`index.sqlite*`, `__pycache__/`, `*.pyc`, `.pytest_cache/`). Noted propagation only copies the robot, never runs it.
2. **Supersession recorded (not silent).** Replaced the old `DEFERRED` block with a `SUPERSEDED` block stating the SAW-38 deferred "out-of-band / update-only-on-fix" note is superseded by SAW-44, with warehouse_robot now a CORE line. Reversal is explicit.
3. **Project-owned boundary sharpened.** Expanded the `project-owned` warehouse line to name `nodes/`, `flags/`, the derived SQLite index, and `warehouse.config.json`, and to draw the engine-vs-data line: the engine (`warehouse_robot/`) propagates as CORE, but the warehouse DATA does not — propagation copies the engine and never runs it, so it cannot write or delete a node/flag/config.

### `docs/upgrade/propagation-agent.md` (3 edits)

4. **D2 — verbatim-path exemption (PIPELINE step 3).** Added a bullet: verbatim/code paths (`warehouse_robot/`) are copied byte-for-byte — SKIP token re-instantiation AND the token-absence fail-loud, and their drift check is a plain (non-token-normalized) compare. Rationale captured: the robot's regex literals (e.g. `[a-z][a-z0-9-]*`) would otherwise read as unresolved tokens and falsely HALT propagation. This is the one technical nuance required for the plain copy to work — not extra machinery.
5. **D3 — handbrake (PIPELINE step 6, Write).** Added the warehouse-step stop rule: propagation copies `warehouse_robot/` but NEVER runs it (no init/ingest/fold/reconcile); if this version's release notes flag a warehouse note-format change, HALT at the warehouse step, tell the owner a migration is required, do NOT migrate, and do NOT write the version stamp. Stated as a documented release-notes-driven stop rule, not a computed check; migration engine out of scope.
6. **D3 — NEVER-list line.** Added a NEVER entry: never run the warehouse robot; HALT at the warehouse step on a flagged format change and do not write the version stamp.

### Scope guardrails honored
- Only the two named files changed. No number-comparison, robot CLI command, or robot-reported-version mechanism built. No executable code (AM4). `warehouse_robot/` itself, consuming projects, and warehouse data untouched.
- The ALLOWED TOOLS clause ("write only the `propagate` surface") already covers the newly-CORE `warehouse_robot/` with no edit needed.

### Master amendment (validation, 2026-06-21)
Master read both edited files in full and checked them against the PoC (D1/D2/D3) + the regex-literal claim against `config.py`/`NODE_FORMAT.md`. Verdict GREEN — all three decisions landed faithfully, no out-of-scope machinery. One gap surfaced and folded in place (not a new group): D3's trigger ("release notes flag a format change") was an undefined artifact for a stateless agent. Per owner decision (b), the trigger is now stated as **owner-provided at the dry-run confirmation gate (step 5)**, not autonomously read — clarified in `propagation-agent.md` (step 6 + NEVER line) and in the PoC D3. No machine-readable release-notes source added (consistent with the no-machinery scope).
