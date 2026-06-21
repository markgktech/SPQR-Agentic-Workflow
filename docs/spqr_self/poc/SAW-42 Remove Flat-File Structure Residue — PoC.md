---
type: poc
title: "SAW-42 Remove Flat-File Structure Residue — PoC"
decides: "How to excise residual flat-document references (DECISIONS/ARCHITECTURE/CONVENTIONS/DATA_MODEL/LESSONS/decisions+ADR) from the generic SPQR agents & skills, post-SAW-31 cutover"
status: draft
date: 2026-06-21
tags: [poc, decision]
---

# SAW-42 Remove Flat-File Structure Residue — PoC

## Context / question
SAW-31 made the generic SPQR agents/skills warehouse-primary, but left residual
references to flat knowledge documents (`DECISIONS.md`, `ARCHITECTURE.md`,
`CONVENTIONS.md`, `DATA_MODEL.md`, `LESSONS.md`, `docs/decisions/` + `INDEX.md` +
`a[NN]-title` ADR files). For an LLM running these skills, a half-migrated file that
mentions both a warehouse proposal and an "ADR format" is a contradiction/derailment
risk. SAW-42 removes that residue.

Framing correction (owner): this is the GENERIC repo — SPQR never *runs* here, only
the upgrade process does. These flat files have no home here; they live in consuming
projects (Foodoire). They are residue **because the warehouse takes over their role
as the knowledge authority**, not because they are absent here.

## Findings

### Residue sweep (generic `docs/agents` + `docs/skills` + template)
Clean legacy references: `quaestor.md:42` (DECISIONS.md), `quaestor-relatio.md:10`
(DECISIONS.md), `consilium-input.md:10` (DATA_MODEL/CONVENTIONS/ARCHITECTURE),
`code-review-checklist.md:10,12` (CONVENTIONS.md), `doc-maintenance.md` (whole file).
ADR placeholders: `quaestor-relatio-output.md:12`, `spike-document.md:30`,
`censura-output.md:34`. Navigation imports: `CLAUDE.md.template:70–73`.
Half-migrated (highest derail risk): `censura-output.md` already carries the
warehouse LESSON-NODE PROPOSAL block (`:54–63`) but still has `adr_proposal … per
doc-maintenance.md ADR format` (`:34`).

### Deliberately-correct, NOT residue (leave as-is)
`probator.md:23`, `senate.md:33`, `bug-pipeline.md:46`, `censura-output.md:54–63`,
`warehouse-usage.md:125`, and the `retro/*` "historical / pre-cutover, read-only"
LESSONS.md mentions. These describe the *physical* flat file (retired-but-not-deleted)
under warehouse-primary; they are not load-bearing knowledge references.

## Recommendation / decision

D1 — Excision mode = FULL (owner override of ticket text). #decision
what: Remove every residual flat-knowledge reference from the generic agents/skills —
neither primary nor secondary. The warehouse is the sole knowledge authority.
why: Owner chose full excision. A retained "secondary reference" leaves a stateless
agent with two competing authorities → the exact derail risk SAW-42 targets.
conflict: This OVERRIDES the SAW-42 ticket's items 2/3/4 wording, which would *demote*
the flat docs to "retained secondary reference". Newer decision (owner) takes
precedence; brief text is derived from THIS PoC, not the ticket diffs verbatim.
affected: all items below; SAW-42 ticket (owner reconciles wording at wrap-up).

D2 — Generic-side only; no propagation here. #decision
what: Apply excision in the generic repo only. Do not touch Foodoire; do not act on
propagation.
why: Propagation is a separate owner-run ticket with an already-settled policy; skills
& agents propagate ~1:1. No A18 reorder needed here.
affected: scope boundary; flag — see Open #1.

D3 — Physical files untouched (incl. the generic `docs/LESSONS.md` stub).
what: SAW-42 removes *references*, not files. The 7-line empty generic LESSONS.md stub
stays for the separate physical-retirement SAW.
why: Physical retirement is a distinct owner-gated SAW (migrate → backup → validate →
delete). Keeps scope clean; avoids mixing axes.
affected: none in this run; flag — see Open #3.

D4 — Retro historical-LESSONS.md mentions stay.
what: Leave the `retro/*` (+ probator/senate/bug-pipeline/censura/warehouse-usage)
"historical / pre-cutover, read-only" LESSONS.md language untouched.
why: Owner-confirmed (self-corrected): the retro reading pre-cutover lessons read-only
is fine and not a contradiction; these point at the physical file, not a knowledge
authority.
affected: none; explicitly out of the excision sweep.

D5 — `doc-maintenance.md` = full rewrite, not surgical diffs. #decision
what: Rewrite the whole skill warehouse-primary. Only TWO protected flat files remain:
`CLAUDE.md` (navigation) and `AGENT_LAWS.md` (laws) — neither is warehouse knowledge.
Remove CONVENTIONS/DATA_MODEL/ARCHITECTURE/`docs/decisions/` as managed surfaces and
every "ADR" concept (FILE SCOPE, FORMAT RULES, FLAG FORMATS, EXECUTION ORDER, PIPELINE
ROLES, CONSTRAINTS).
why: Under full excision the ticket's surgical diffs (which keep "retained secondary
projection") would re-introduce the contradiction. The "Six protected files" frame
collapses to two; new knowledge → warehouse via `warehouse-ingest.md`.
affected: `docs/skills/doc-maintenance.md` (I8).

### Per-item dispositions (Phase 3)
| Item | File:loc | Type | Decision |
|------|----------|------|----------|
| I1 | `agents/quaestor.md:42` | MODIFY | Drop `DECISIONS.md` from the Read surface; prior decisions come from the warehouse per the WAREHOUSE QUERY POLICY (already present at `:45`). |
| I2 | `skills/quaestor-relatio.md:10` | MODIFY | Replace pre-flight step `3. DECISIONS.md` with a warehouse query step (find/open-scope per WAREHOUSE QUERY POLICY); an ABSENT verdict is valid evidence — no mandatory flat load. |
| I3 | `skills/quaestor-relatio-output.md:12` | MODIFY | `NO DECISION NEEDED — covered by [ADR-XX / file:line / prior decision]` → `covered by [warehouse node-id / file:line / prior decision]`. |
| I4 | `skills/consilium-input.md:10` | MODIFY | Replace LOAD ORDER step 4 (On-Demand Docs DATA_MODEL/CONVENTIONS/ARCHITECTURE) with a warehouse query step per the Senate WAREHOUSE QUERY POLICY (ABSENT verdict valid). Reconcile the `NEVER … halt if any LOAD ORDER item missing` so an absent (retired) flat doc is not a blocker after a completed warehouse query. |
| I5 | `skills/code-review-checklist.md:10,12` | MODIFY | Naming + Patterns checks → active warehouse constraints/decisions; drop the `CONVENTIONS.md` authority. |
| I6 | `skills/spike-document.md:30` | MODIFY | `Covered by [ADR-XX / file:line / prior decision]` → `[warehouse node-id / file:line / prior decision]`. |
| I7 | `skills/censura-output.md:34` | MODIFY | Replace `adr_proposal: NONE | [ … per doc-maintenance.md ADR format]` with a warehouse decision-proposal flag (`decision_proposal: NONE | [decision-node proposal per warehouse-ingest.md — title/rationale/body]`), consistent with the `:54–63` lesson-node block. |
| I8 | `skills/doc-maintenance.md` | MODIFY | Full rewrite per D5. |
| I9 | `CLAUDE.md.template:70–73` | MODIFY | Remove the four flat-doc `@imports`; replace with a warehouse-knowledge pointer (query per WAREHOUSE QUERY POLICY); keep `@docs/agents/` + `@docs/skills/` (74–75). Editable via brief — this is the template product file, not the live CLAUDE.md. |

## Open items (flag only — owner creates tickets; Notion auto-assigns IDs)
- Open #1 — Propagation gate: this excision must NOT propagate to Foodoire before the
  SAW-41 migration has populated Foodoire's warehouse, else Foodoire agents lose access
  to their not-yet-migrated flat knowledge. Owner-owned (separate propagation ticket).
- Open #2 — `docs/upgrade/propagation-manifest.md:25` still lists `docs/LESSONS.md` as a
  propagated file; under warehouse-primary that is residue too, but it belongs to the
  propagation ticket — flagged, not touched here.
- Open #3 — Physical retirement SAW: delete the retired flat docs (incl. the generic
  `docs/LESSONS.md` stub whose body still states pre-cutover protocol) — separate
  owner-gated SAW.
