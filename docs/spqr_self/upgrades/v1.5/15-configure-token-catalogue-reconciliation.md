---
up: "[[v1.5]]"
group: "CONFIGURE.md + spqr.config.template token-catalogue reconciliation (SAW-46)"
order: 15/15
tags: [group]
---

# Group 15 — CONFIGURE.md + spqr.config.template token-catalogue reconciliation (SAW-46)

## Brief
GROUP: CONFIGURE.md + spqr.config.template token-catalogue reconciliation (SAW-46)
ORDER: 15/15
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/15-configure-token-catalogue-reconciliation.md
RATIONALE: One coherent surface — the template is derived from the catalogue, so both move together.
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-46 CONFIGURE Token-Catalogue Reconciliation — PoC.md
FILL_CHANGES_MADE: yes
PRE_FLIGHT:
  - docs/upgrade/execution.md
  - docs/spqr_self/poc/SAW-46 CONFIGURE Token-Catalogue Reconciliation — PoC.md   (authoritative — D1–D9)
  - docs/upgrade/propagation-manifest.md   (propagate surface = docs/agents, docs/skills, docs/retro)
FILES:
  - docs/CONFIGURE.md: D1 add [WAREHOUSE_ROOT] (required) + D2 [ANTECHAMBER_ROOT] (optional, robot-defaults to antechamber sibling) catalogue rows with their using-files; D4 header v1.2→v1.5 + reconcile body v1.2 refs; D5 remove stale [RETRO_PARENT_ID]+[RETRO_TEMPLATE_ID] rows (note reason inline near [RETRO_SESSION_STARTER_ID]); D7 split generic-only upgrade-master tokens into a new "§1b — Upgrade-master config (generic-only; NOT in spqr.config)" subsection; D8 reconcile §1b names to upgrade-agent.md actuals ([MASTER_PERSONA_1_NAME], [MASTER_PERSONA_2_NAME], [YOUR_PROJECT_NAME], [PROJECT_REPO_PATH], [SPQR_REPO_PATH]).
  - spqr.config.template: D3 add WAREHOUSE_ROOT (required) + ANTECHAMBER_ROOT (optional, empty=robot default) slots with "# docs/CONFIGURE.md §1" provenance; D5 remove stale RETRO_PARENT_ID + RETRO_TEMPLATE_ID slots.

VERIFICATION (D9 — record verbatim in Changes Made):
  - grep `\[[A-Z][A-Z0-9_]+\]` across docs/agents docs/skills docs/retro → every UPPER token (excluding runtime [AGENT]/[TICKET_URL]/[FILE]/[ID]) resolves to a row in CONFIGURE.md §1 AND a slot in spqr.config.template.
  - confirm no stale catalogue-only token remains in §1 (project-token section): [RETRO_PARENT_ID]/[RETRO_TEMPLATE_ID] gone from both files.
  - confirm §1b generic-only tokens are NOT added to spqr.config.template.

SCOPE GUARD:
  - Edit ONLY the two init-only files above. Do NOT edit any propagate-surface agent/skill/retro file (tokens already live there correctly), and do NOT edit docs/upgrade/* (generic-only). The residual execution.md ↔ upgrade-agent.md persona-token drift is an OPEN ITEM (OI-1) — flag, do not fix.
  - Do not commit.

## Changes Made

Two init-only files edited: `docs/CONFIGURE.md` and `spqr.config.template`. No propagate-surface, MAIN, sibling-sub-doc, or `docs/upgrade/*` file touched. Not committed.

### `docs/CONFIGURE.md`
- **D4** — Header `# CONFIGURE.md — SPQR v1.2 Setup Guide` → `v1.5`. Grep confirmed line 1 was the only `v1.2` reference in the file; no body refs to reconcile.
- **D1** — Added `[WAREHOUSE_ROOT]` row to the §1 Variable Catalogue listing all 10 using-files (`docs/agents/{senate,quaestor,praetor,tribunus,probator,curator,session-starters}.md`, `docs/skills/{warehouse-usage,warehouse-ingest,censura-output}.md`); value = warehouse root passed as `--warehouse-root` to the `warehouse_robot` CLI; marked **Required — silent failure risk if empty**.
- **D2** — Added `[ANTECHAMBER_ROOT]` row (`docs/skills/warehouse-usage.md`); marked **Optional**, documented that empty ⇒ robot defaults to an `antechamber` sibling of `[WAREHOUSE_ROOT]` (not a silent failure).
- **D5** — Removed the `[RETRO_PARENT_ID]` and `[RETRO_TEMPLATE_ID]` catalogue rows (stale since the SAW-31/33 local-retro cutover). Added an inline `> **Removed in v1.5 (SAW-46):**` note beneath the §1 table, next to the retained `[RETRO_SESSION_STARTER_ID]`, recording the reason so the deletion is not silent.
- **D7** — Split the generic-only upgrade-master tokens out of §1 into a new `## Section 1b — Upgrade-master config (generic-only; NOT in spqr.config)` subsection, with a preamble stating they are filled in `docs/upgrade/upgrade-agent.md` (generic-only, never propagates) and must not be added to `spqr.config.template`. This resolved the merged-row defect on the old line 27 (`[RETRO_SESSION_STARTER_ID]` and `[SPQR_REPO_PATH]` were on one physical line joined by `||`).
- **D8** — Reconciled §1b token names to the actuals used by `upgrade-agent.md`: `[Master Persona 1]`→`[MASTER_PERSONA_1_NAME]`, `[Master Persona 2]`→`[MASTER_PERSONA_2_NAME]`, and added the two tokens the catalogue previously omitted (`[YOUR_PROJECT_NAME]`, `[PROJECT_REPO_PATH]`) plus the relocated `[SPQR_REPO_PATH]`. Verified against `upgrade-agent.md`, which uses exactly these five tokens. `upgrade-agent.md` and `execution.md` were **not** edited (generic-only, out of scope) — the residual `execution.md` (`[Master Persona 1/2]`) ↔ `upgrade-agent.md` drift remains as **OI-1**, flagged not fixed.

### `spqr.config.template`
- **D3** — Added a `# Knowledge Warehouse — docs/CONFIGURE.md §1` section with `WAREHOUSE_ROOT: ""` (required; empty = silent failure) and `ANTECHAMBER_ROOT: ""` (optional; empty = robot defaults to an `antechamber` sibling of WAREHOUSE_ROOT) slots, carrying the `docs/CONFIGURE.md §1` provenance.
- **D5** — Removed the `RETRO_PARENT_ID` and `RETRO_TEMPLATE_ID` slots; left an inline comment recording the v1.5/SAW-46 removal and SAW-31/33 cause. `RETRO_SESSION_STARTER_ID` retained.
- §1b generic-only tokens deliberately **not** added to the template (D7 boundary).

### D9 verification (verbatim)

```
=== D9.1 — every propagate-surface UPPER token (excl runtime) resolves in BOTH CONFIGURE.md and template ===
[AGENT]                    -> runtime (excluded)
[ANTECHAMBER_ROOT]         -> CONFIGURE / TEMPLATE
[BUG_TEMPLATE_ID]          -> CONFIGURE / TEMPLATE
[DOC_TEMPLATE_ID]          -> CONFIGURE / TEMPLATE
[FEATURE_TEMPLATE_ID]      -> CONFIGURE / TEMPLATE
[FILE]                     -> runtime (excluded)
[PROJECT_BOUNDARIES]       -> CONFIGURE / TEMPLATE
[PROJECT_PATH]             -> CONFIGURE / TEMPLATE
[RETRO_SESSION_STARTER_ID] -> CONFIGURE / TEMPLATE
[SPIKE_DOCUMENT_TEMPLATE_ID] -> CONFIGURE / TEMPLATE
[SPIKE_DOC_PARENT_PAGE_ID] -> CONFIGURE / TEMPLATE
[SPIKE_TEMPLATE_ID]        -> CONFIGURE / TEMPLATE
[TICKET_URL]               -> runtime (excluded)
[WAREHOUSE_ROOT]           -> CONFIGURE / TEMPLATE

=== D9.2 — stale tokens gone from BOTH files (expect 0 each) ===
CONFIGURE.md RETRO_PARENT/TEMPLATE rows: 0
template RETRO_PARENT/TEMPLATE slots:    0

=== D9.3 — §1b generic-only tokens NOT in template (expect 0 each) ===
YOUR_PROJECT_NAME      in template: 0
PROJECT_REPO_PATH      in template: 0
SPQR_REPO_PATH         in template: 0
MASTER_PERSONA_1_NAME  in template: 0
MASTER_PERSONA_2_NAME  in template: 0
```

**Result:** every propagate-surface UPPER token (excluding runtime `[AGENT]`/`[TICKET_URL]`/`[FILE]`/`[ID]`) resolves to both a §1 catalogue row and a `spqr.config.template` slot — no `MISSING` entries. The two stale retro tokens are gone from both files. The five §1b generic-only tokens are absent from the template, as required. AC #3 satisfied; the first Foodoire v1.3→v1.5 propagation will not fail loud on an uncatalogued token.

### Out-of-scope / open items
- **OI-1** (carried from PoC) — generic-only token-name drift between `docs/upgrade/execution.md` (`[Master Persona 1/2]`) and `docs/upgrade/upgrade-agent.md` (`[MASTER_PERSONA_*_NAME]`). Outside the propagation surface; not edited this run → owner-created housekeeping SAW at wrap-up.
- No new out-of-scope discoveries during execution.
