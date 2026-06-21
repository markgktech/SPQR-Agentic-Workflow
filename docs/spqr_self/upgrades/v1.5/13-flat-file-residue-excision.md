---
up: "[[v1.5]]"
group: "Flat-file structure residue excision (SAW-42)"
order: 13/13
tags: [group]
---

# Group 13 — Flat-file structure residue excision (SAW-42)

## Brief
GROUP: Flat-file structure residue excision (SAW-42)
ORDER: 13/13
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/13-flat-file-residue-excision.md
RATIONALE:     One homogeneous single-surface sweep — excise residual flat-knowledge references left by the SAW-31 cutover (7-FILES cap owner-overridden, per the SAW-33 precedent; "never split by effort").
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-42 Remove Flat-File Structure Residue — PoC.md
FILL_CHANGES_MADE: yes

EXCISION MODE — FULL (PoC D1, owner override of the ticket text): remove every residual
flat-knowledge reference — neither primary NOR secondary. The warehouse is the sole
knowledge authority. Do NOT reproduce the SAW-42 ticket's "retained secondary reference"
wording (items 2/3/4) — that is superseded by PoC D1. Derive all text from the PoC, not
the ticket diffs.

SCOPE BOUNDARY: generic SPQR repo only (PoC D2). Touch NO physical flat files — references
only (PoC D3). Do NOT touch the deliberately-correct "historical / pre-cutover, read-only"
LESSONS.md mentions in retro/* · probator.md · senate.md · bug-pipeline.md ·
censura-output.md:54–63 · warehouse-usage.md (PoC D4). Do not commit.

PRE_FLIGHT:
  - docs/upgrade/execution.md
  - docs/spqr_self/poc/SAW-42 Remove Flat-File Structure Residue — PoC.md  (SOURCE OF TRUTH — read first, fully)
  - docs/skills/warehouse-ingest.md  (target vocabulary: node-id, decision-/lesson-node proposal, WAREHOUSE QUERY POLICY)
  - docs/agents/quaestor.md  (its WAREHOUSE QUERY POLICY block is the canonical query phrasing to mirror)

FILES:
  - docs/agents/quaestor.md (I1): drop `DECISIONS.md` from the ALLOWED TOOLS Read surface (line ~42); prior decisions come from the warehouse per the WAREHOUSE QUERY POLICY already present in this file.
  - docs/skills/quaestor-relatio.md (I2): replace PRE-FLIGHT step `3. DECISIONS.md` with a warehouse query step (find/open-scope per the WAREHOUSE QUERY POLICY); an ABSENT verdict is valid evidence — no mandatory flat load. Renumber the remaining steps.
  - docs/skills/quaestor-relatio-output.md (I3): in RECORD DECISIONS, `NO DECISION NEEDED — covered by [ADR-XX / file:line / prior decision]` → `covered by [warehouse node-id / file:line / prior decision]`.
  - docs/skills/consilium-input.md (I4): replace LOAD ORDER step 4 (On-Demand Docs DATA_MODEL/CONVENTIONS/ARCHITECTURE) with a warehouse query step per the Senate WAREHOUSE QUERY POLICY (ABSENT verdict valid); reconcile the `NEVER … halt if any LOAD ORDER item missing` so an absent retired flat doc is not a blocker after a completed warehouse query.
  - docs/skills/code-review-checklist.md (I5): Naming (line ~10) + Patterns (line ~12) checks → active warehouse constraints/decisions; remove the `CONVENTIONS.md` authority entirely.
  - docs/skills/spike-document.md (I6): in RESOLUTION TYPES, `Covered by [ADR-XX / file:line / prior decision]` → `[warehouse node-id / file:line / prior decision]`.
  - docs/skills/censura-output.md (I7): replace the OUTPUT FORMAT field `adr_proposal: NONE | [ … per doc-maintenance.md ADR format]` (line ~34) with a warehouse decision-proposal flag `decision_proposal: NONE | [decision-node proposal per warehouse-ingest.md — title/rationale/body]`, consistent with the existing LESSON-NODE PROPOSAL block (:54–63). Update any later reference to the old field name.
  - docs/skills/doc-maintenance.md (I8): FULL REWRITE warehouse-primary (PoC D5). Only TWO protected flat files remain — CLAUDE.md (navigation) + AGENT_LAWS.md (laws); both are NOT warehouse knowledge. Remove CONVENTIONS/DATA_MODEL/ARCHITECTURE/`docs/decisions/` as managed surfaces and every "ADR" concept across FILE SCOPE, FORMAT RULES, FLAG FORMATS (ADR flag → ⚠️ WAREHOUSE DECISION PROPOSAL NEEDED, submitted via warehouse-ingest.md), EXECUTION ORDER (warehouse acceptance first → CLAUDE.md navigation last), PIPELINE ROLES (Consilium/Praetor raise warehouse proposals, no ADR proposer), CONSTRAINTS. Keep the file's no-decorative-formatting house style.
  - CLAUDE.md.template (I9): in `## On-Demand Docs`, remove the four flat-doc imports (`@docs/ARCHITECTURE.md`, `@docs/DATA_MODEL.md`, `@docs/CONVENTIONS.md`, `@docs/decisions/INDEX.md`, lines ~70–73); replace with one warehouse-knowledge pointer (prior decisions/constraints/lessons → query the warehouse per the WAREHOUSE QUERY POLICY in the agent file); KEEP `@docs/agents/` + `@docs/skills/` (lines ~74–75). This is the template product file (not the live CLAUDE.md) — edit directly.

POST-CONDITION (self-check before writing Changes Made): grep the eight edited files + the template for `DECISIONS.md`, `ADR`, `docs/decisions`, `INDEX.md`, and a flat `CONVENTIONS.md`/`DATA_MODEL.md`/`ARCHITECTURE.md` authority reference — zero residue except the deliberately-retained physical-file mentions listed in SCOPE BOUNDARY. Report the grep result in Changes Made.

## Changes Made

EXCISION MODE = FULL (PoC D1). All text derived from the PoC, not the SAW-42 ticket diffs. References only — no physical flat files touched. Deliberately-correct "historical / pre-cutover, read-only" LESSONS.md mentions left untouched (PoC D4 / SCOPE BOUNDARY).

- I1 — `docs/agents/quaestor.md` (ALLOWED TOOLS, Read line): dropped `DECISIONS.md` from the Read surface; appended "prior decisions come from the warehouse per the WAREHOUSE QUERY POLICY" — the policy block already present at `:25` is the authority.
- I2 — `docs/skills/quaestor-relatio.md` (PRE-FLIGHT): replaced step `3. DECISIONS.md` with a warehouse `find`/`open-scope` query step per the WAREHOUSE QUERY POLICY (quaestor.md), explicitly noting an ABSENT verdict is valid evidence and no mandatory flat load. Remaining steps were already numbered 4–6; no renumber needed (the flat doc occupied slot 3, now reused).
- I3 — `docs/skills/quaestor-relatio-output.md` (RECORD DECISIONS): `covered by [ADR-XX / file:line / prior decision]` → `covered by [warehouse node-id / file:line / prior decision]`.
- I4 — `docs/skills/consilium-input.md` (LOAD ORDER step 4 + NEVER): replaced "Relevant On-Demand Docs (DATA_MODEL/CONVENTIONS/ARCHITECTURE)" with a warehouse query step per the Senate WAREHOUSE QUERY POLICY (senate.md, `--archetype deliberate`); reconciled `Never proceed if any LOAD ORDER item is missing` with an EXCEPTION clause so a completed warehouse query returning ABSENT (an absent retired flat doc) is not a blocker.
- I5 — `docs/skills/code-review-checklist.md` (CONVENTIONS block): Naming + Patterns checks now reference active warehouse constraints/decisions (query per the WAREHOUSE QUERY POLICY); the `CONVENTIONS.md` authority removed entirely.
- I6 — `docs/skills/spike-document.md` (RESOLUTION TYPES): `Covered by [ADR-XX / file:line / prior decision]` → `[warehouse node-id / file:line / prior decision]`.
- I7 — `docs/skills/censura-output.md` (OUTPUT FORMAT): `adr_proposal: NONE | [domain area — rationale; full content per doc-maintenance.md ADR format]` → `decision_proposal: NONE | [decision-node proposal per warehouse-ingest.md — title/rationale/body]`, consistent with the existing LESSON-NODE PROPOSAL block (`:54–63`). Repo-wide grep confirmed no later reference to the old `adr_proposal` field name (only the PoC + this run-doc mention it).
- I8 — `docs/skills/doc-maintenance.md`: FULL REWRITE warehouse-primary (PoC D5). The "six protected files" frame collapses to TWO — `CLAUDE.md` (navigation) + `AGENT_LAWS.md` (laws), both explicitly NOT warehouse knowledge. Removed CONVENTIONS/DATA_MODEL/ARCHITECTURE/`docs/decisions/` as managed surfaces and every "ADR" concept across FILE SCOPE, FORMAT RULES, FLAG FORMATS (ADR flag → `⚠️ WAREHOUSE DECISION PROPOSAL NEEDED`, submitted via warehouse-ingest.md), EXECUTION ORDER (warehouse acceptance first → CLAUDE.md navigation last), PIPELINE ROLES (Consilium/Praetor now raise warehouse proposals; no ADR proposer), CONSTRAINTS. Added a SCOPE OF THIS SKILL header stating knowledge lives in the warehouse, authored via warehouse-ingest.md. No-decorative-formatting house style preserved (no `---`, no bold headers, no decorative blank lines).
- I9 — `CLAUDE.md.template` (`## On-Demand Docs`): removed the four flat-doc `@imports` (`@docs/ARCHITECTURE.md`, `@docs/DATA_MODEL.md`, `@docs/CONVENTIONS.md`, `@docs/decisions/INDEX.md`); replaced with one warehouse-knowledge pointer (prior decisions/constraints/conventions/schema/architecture/lessons → query the warehouse per the WAREHOUSE QUERY POLICY in the agent file). Kept `@docs/agents/` + `@docs/skills/`. Edited the template product file directly (not the live CLAUDE.md).

POST-CONDITION grep self-check — `grep -nE 'DECISIONS\.md|ADR|docs/decisions|INDEX\.md|CONVENTIONS\.md|DATA_MODEL\.md|ARCHITECTURE\.md'` over the eight edited files + the template: ZERO matches (grep exit 1). No residual flat-knowledge authority references remain. No deliberately-retained physical-file mentions live in these nine files, so the "except SCOPE BOUNDARY mentions" carve-out did not apply here.

SCOPE BOUNDARY honored: generic repo only (D2); no physical flat files touched (D3); retro/* · probator.md · senate.md · bug-pipeline.md · censura-output.md:54–63 · warehouse-usage.md historical-LESSONS.md mentions left untouched (D4). Not committed.
