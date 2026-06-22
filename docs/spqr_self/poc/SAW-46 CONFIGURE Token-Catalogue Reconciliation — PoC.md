---
type: poc
title: "SAW-46 — CONFIGURE.md + spqr.config.template Token-Catalogue Reconciliation"
decides: "Which tokens the v1.5 propagate surface needs catalogued, which are stale and removed, and how generic-only upgrade-master tokens are separated — so the first Foodoire v1.3→v1.5 propagation does not fail loud on step 3."
status: done
date: 2026-06-22
tags: [poc, decision, saw-46]
---

# SAW-46 — CONFIGURE.md + spqr.config.template Token-Catalogue Reconciliation

## Context / question
SAW-46 is **phase 0** of the Foodoire v1.3→v1.5 propagation. `docs/CONFIGURE.md` is still the "SPQR v1.2 Setup Guide" and `spqr.config.template` is derived from it. The propagation agent re-instantiates every `[TOKEN]` in the propagated core surface from a project's `spqr.config` and **fails loudly** on any propagated token absent from the catalogue. The warehouse cutover (SAW-31) introduced `[WAREHOUSE_ROOT]` (18× / 10 files) and `[ANTECHAMBER_ROOT]` (1×) into the core surface but never catalogued them. AC #3 widens the work: *every* token the propagate surface uses must exist in the catalogue, and no stale catalogue-only tokens may remain.

Roundtable (Phase 2) was **skipped per owner** for this run.

## Findings

### Propagate surface = `docs/agents/`, `docs/skills/`, `docs/retro/` (per `propagation-manifest.md`)
`docs/upgrade/` and `docs/spqr_self/` are **generic-only** (never propagate). `CONFIGURE.md` / `spqr.config.template` are **init-only**.

### Token-diff (grep of the propagate surface, 2026-06-22)
**Used but NOT catalogued (fail-loud source):**
- `[WAREHOUSE_ROOT]` — 18×, across `docs/agents/{senate,quaestor,praetor,tribunus,probator,curator,session-starters}.md` + `docs/skills/{warehouse-usage,warehouse-ingest,censura-output}.md`. Passed as `--warehouse-root` to the `warehouse_robot` CLI.
- `[ANTECHAMBER_ROOT]` — 1×, `docs/skills/warehouse-usage.md`. **Optional** — the robot defaults it to an `antechamber` sibling of the warehouse root (A3, SAW-31).

**Catalogued + in template, but NO LONGER used by the propagate surface (stale):**
- `[RETRO_PARENT_ID]` — retro went **local** in SAW-31/33 (`retro/output.md:14` creates a `work_documents/` vault file, not a Notion child page).
- `[RETRO_TEMPLATE_ID]` — retro now mirrors the local `templates/retro_template.md`, not a Notion template.

**Live, retained:** `[Name 1–4]`, `[PROJECT_PATH]`, `[PROJECT_BOUNDARIES]`, `[SPIKE_TEMPLATE_ID]`, `[FEATURE_TEMPLATE_ID]`, `[BUG_TEMPLATE_ID]`, `[DOC_TEMPLATE_ID]`, `[SPIKE_DOCUMENT_TEMPLATE_ID]`, `[SPIKE_DOC_PARENT_PAGE_ID]`, `[RETRO_SESSION_STARTER_ID]` (still mirrors a Notion starter page, `retro/session-starter.md:8`).

**Runtime placeholders (NOT config, correctly excluded):** `[AGENT]`, `[TICKET_URL]`, `[FILE]`, `[ID]`.

### Two catalogue defects beyond the warehouse tokens (independent finding — Law 4)
1. **Audience conflation.** `[SPQR_REPO_PATH]`, `[Master Persona 1]`, `[Master Persona 2]` are **not** consuming-project tokens — only `docs/upgrade/` (generic-only) uses them, filled by the upgrade-master in the `upgrade-agent.md` CONFIG block. They are correctly **absent** from `spqr.config.template`, yet `CONFIGURE.md §1` lists them in the same table as project tokens.
2. **Name drift.** `CONFIGURE.md` catalogues `[Master Persona 1/2]`, but `upgrade-agent.md` actually uses `[MASTER_PERSONA_1_NAME]` / `[MASTER_PERSONA_2_NAME]` and two tokens the catalogue omits entirely (`[YOUR_PROJECT_NAME]`, `[PROJECT_REPO_PATH]`). Further drift exists between `upgrade-agent.md` and `execution.md` (which uses `[Master Persona 1/2]`). All in generic-only files — outside the propagation fail-loud scope.

## Recommendation / decision

| # | Item | Type | Decision | Affected |
|---|------|------|----------|----------|
| D1 | Add `[WAREHOUSE_ROOT]` to the Variable Catalogue with its 10 using-files; value = warehouse root path passed to the robot CLI. **Required** (silent-failure risk if empty). | CONFIRM | adopt | `docs/CONFIGURE.md` |
| D2 | Add `[ANTECHAMBER_ROOT]` to the catalogue; value = antechamber root. **Optional** — empty ⇒ robot defaults to an `antechamber` sibling (A3); document it as not-silent-failure. | CONFIRM | adopt | `docs/CONFIGURE.md` |
| D3 | Add matching `WAREHOUSE_ROOT` (required) + `ANTECHAMBER_ROOT` (optional, empty=default) slots to the template, with the `# docs/CONFIGURE.md §1` provenance comment. | CONFIRM | adopt | `spqr.config.template` |
| D4 | Header/version: `# CONFIGURE.md — SPQR v1.2 Setup Guide` → v1.5; reconcile any other "v1.2" body reference. | CONFIRM | adopt | `docs/CONFIGURE.md` |
| D5 | **Remove** `[RETRO_PARENT_ID]` + `[RETRO_TEMPLATE_ID]` from BOTH `CONFIGURE.md` and `spqr.config.template` — stale since the SAW-31/33 local-retro cutover. (Owner: "töröljük mindkét helyről".) Note the removal reason inline near the retained `[RETRO_SESSION_STARTER_ID]` row so the deletion is not silent. | MODIFY | adopt | `docs/CONFIGURE.md`, `spqr.config.template` |
| D6 | ~~Keep `[RETRO_SESSION_STARTER_ID]` — still live (`retro/session-starter.md:8`).~~ **SUPERSEDED by Item 4 (scope extension, 2026-06-22):** retro is now fully local (Notion retained only for ticket creation/maintenance), so `[RETRO_SESSION_STARTER_ID]` is dropped end-to-end in the second pass. See run doc "Delta — Second pass". | MODIFY | superseded | `docs/retro/session-starter.md`, `docs/CONFIGURE.md`, `spqr.config.template` |
| D7 | **Separate** the generic-only upgrade-master tokens into a clearly-marked CONFIGURE.md subsection — e.g. `§1b — Upgrade-master config (generic-only; filled in upgrade-agent.md, NOT in spqr.config)` — covering `[SPQR_REPO_PATH]`, the master persona tokens, `[YOUR_PROJECT_NAME]`, `[PROJECT_REPO_PATH]`. Resolves why they are absent from the template. (Owner: "külön §-ba".) | MODIFY | adopt | `docs/CONFIGURE.md` |
| D8 | **Reconcile the name drift** within `CONFIGURE.md §1b` to the names `upgrade-agent.md` actually uses (`[MASTER_PERSONA_1_NAME]`, `[MASTER_PERSONA_2_NAME]`, add `[YOUR_PROJECT_NAME]`, `[PROJECT_REPO_PATH]`). The master edits **only `CONFIGURE.md`** here; `upgrade-agent.md` / `execution.md` are generic-only files not edited in this run — the residual `execution.md` ↔ `upgrade-agent.md` persona-token drift is **flagged** (open item), not touched. (Owner: "drift javítása itt".) | MODIFY | adopt | `docs/CONFIGURE.md` |
| D9 | AC #3 verification gate: after edits, re-grep the propagate surface for `[UPPER_TOKEN]` and confirm every one resolves via the template, and no catalogue-only stale token remains in §1 (the project-token section). | CONFIRM | adopt | verification |

### Open items (→ owner-created SAW tickets at wrap-up)
- **OI-1** Generic-only token-name drift between `docs/upgrade/execution.md` (`[Master Persona 1/2]`) and `docs/upgrade/upgrade-agent.md` (`[MASTER_PERSONA_*_NAME]`). Outside the propagation surface; not edited this run → housekeeping SAW.

### Scope guard
- All edits land via the **execution brief** (Phase 5), not authored by the master directly. Targets: `docs/CONFIGURE.md`, `spqr.config.template` (both init-only). No propagate-surface agent/skill file is edited — the tokens already live there correctly; only the catalogue/template catch up.
- `[WAREHOUSE_ROOT]`/`[ANTECHAMBER_ROOT]` are a path-style token (per-instance warehouse identity also lives in `warehouse.config.json`), but the agent/skill CLI examples use the placeholder following the `[PROJECT_PATH]` convention, so a catalogue row + config slot is required. Captured so it is not re-litigated.
