---
up: "[[v1.5]]"
group: "Warehouse Cutover — F2 Probator close-write follow-up (SAW-31)"
order: 9b/10
saw: [SAW-31]
ticket: SAW-31
status: pending
type: brief
tags: [group, warehouse, cutover, brief, followup]
---

# Group 9b — Warehouse Cutover: F2 Probator close-write follow-up (D2c extension)

## Brief
GROUP:          Warehouse Cutover — F2 Probator close-write (SAW-31, D2c extension)
ORDER:          9b/10 (follow-up to Group 9; same file-ownership surface as Group 9 — probator.md)
REPO:           SPQR (generic; A18 generic-first)
RUN_CONTAINER:  /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:        /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/09b-warehouse-cutover-probator-followup.md
RATIONALE:      F2 (master-found, owner-approved fix-now) — Probator authors the CORRECTIO close lesson to the knowledge sink (D8); warehouse-primary requires that as a PROPOSAL, but Group 9 left Probator read-only because D2c named only Censura. One-file delta; Curator verified NOT affected (it writes verdicts to the local vault, not knowledge to the warehouse).
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md  (Findings F2 + the D2c extension; DERIVE, do not re-decide)
FILL_CHANGES_MADE: yes

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md   (F2 + D2c extension)
  - docs/skills/warehouse-ingest.md                         (the proposer contract Probator's close lesson now uses — built in Group 9)
  - docs/agents/senate.md                                   (the Censura D2c pattern to mirror — lesson-node proposal, propose-is-free-no-HITL)

DEPENDENCY GATE: Group 9 GREEN (the `warehouse-ingest.md` skill + the Senate D2c pattern exist). STOP if absent.

## Scope — build exactly this (PoC F2 / D2c extension)
The scrutinize archetype governs READ blindness (the DENY), NOT write — read-archetype ⊥ propose-right. Probator stays scrutinize-on-read AND gains a narrow propose right for its one authoring act (the CORRECTIO close lesson), mirroring Censura's D2c.

## FILES (1)
  docs/agents/probator.md:
   - CORRECTIO CLOSE MODE (the D8 close-write): the routine knowledge entry becomes a **lesson-node PROPOSAL** to the antechamber via `docs/skills/warehouse-ingest.md` (MANDATORY read-before-propose), not a flat `LESSONS.md` append. (LESSONS.md not deleted this run.)
   - WAREHOUSE QUERY POLICY block line "Read-only — no propose right": amend to "read-blind (scrutinize) for queries; ONE narrow authoring act — the CORRECTIO close lesson via `propose`."
   - ALLOWED TOOLS (Write/Edit + Bash): the close-write to the sink = a `propose` (lesson-node proposal) via the warehouse write CLI; add `propose`/`revise` to the allowed warehouse-CLI verbs (scoped to the close lesson). `propose` is free (no owner HITL — the gate + Senate judgment is the control), mirroring Censura.
   - NEVER "Never run the warehouse write CLI (propose/revise/resolve/grant)": amend to permit `propose`/`revise` for the CORRECTIO close lesson ONLY; still **never `resolve`/`grant`** (Senate + owner-HITL). Keep the SCRUTINIZE DENY (read blindness) and the no-source-code bar intact.

## Scope fence — do NOT do (flag if found, per Law 1)
- `probator.md` ONLY. Do NOT touch `curator.md` (verified not affected), the other agents, or any Group-10 file.
- Do NOT give Probator `resolve`/`grant` (those stay Senate + owner-HITL).
- Do NOT remove the SCRUTINIZE DENY or the read-blindness — propose-right is orthogonal to read-archetype.
- Do NOT delete LESSONS.md.

## Changes Made (2026-06-21)

Single-file delta to `docs/agents/probator.md` — F2 / D2c extension: Probator stays scrutinize-on-read AND gains a narrow `propose` right for its one authoring act (the CORRECTIO close lesson), mirroring Censura's D2c. Four edits:

1. **CORRECTIO CLOSE MODE (D8 close-write, was line 23).** The routine knowledge entry is now emitted as a **lesson-node proposal** to the warehouse antechamber via `docs/skills/warehouse-ingest.md` (MANDATORY read-before-propose), no longer a flat `LESSONS.md` append. Noted `propose` is free (no owner HITL — the gate + Senate judgment is the control). Recorded that LESSONS.md is not physically deleted this run (separate later owner-gated SAW).

2. **WAREHOUSE QUERY POLICY header (was line 33).** Replaced "Read-only — no propose right (a reviewer does not author knowledge)" with "Read-blind (scrutinize) for queries; ONE narrow authoring act — the CORRECTIO close lesson via `propose` (D2c extension; read-archetype ⊥ propose-right — the scrutinize archetype governs READ blindness, not write)."

3. **ALLOWED TOOLS — Write/Edit + Bash.** Write/Edit: the CORRECTIO close knowledge entry is now authored as a `propose` via the warehouse write CLI, not a flat-file append (cross-refs `warehouse-ingest.md`). Bash: added `propose`/`revise` to the warehouse-CLI verb set `{open-scope,find,fetch,traverse,verdict,propose,revise}`, scoped to the CORRECTIO close lesson ONLY; `propose` free (no owner HITL, mirroring Censura); never `resolve`/`grant`.

4. **NEVER block.** Reworded the source-file line so the close lesson is described as a `propose` (not a flat-file append). Replaced "Never run the warehouse write CLI (`propose`/`revise`/`resolve`/`grant`)…" with "Never run `resolve`/`grant`…" — Probator's ONLY warehouse write is `propose`/`revise` for the CORRECTIO close lesson; never an ingest verdict or consent grant. Explicitly preserved the SCRUTINIZE DENY (read blindness) and the no-source-code bar.

**Scope fence honoured:** `probator.md` ONLY — `curator.md`, the other agents, and Group-10 files untouched. SCRUTINIZE DENY (`probator.md:40`) and read-blindness intact. `resolve`/`grant` remain Senate + owner-HITL. LESSONS.md not deleted. No commit (owner commits).

**Dependency gate:** Group 9 GREEN confirmed — `warehouse-ingest.md` skill present and the Senate D2c pattern (`senate.md:33`, `:58`, `:78`) present before execution.

**Out-of-scope discovery:** none.
