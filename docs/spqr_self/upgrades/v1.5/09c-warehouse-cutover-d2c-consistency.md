---
up: "[[v1.5]]"
group: "Warehouse Cutover — 9c D2c consistency closure (SAW-31)"
order: 9c/10
saw: [SAW-31]
ticket: SAW-31
status: pending
type: brief
tags: [group, warehouse, cutover, brief, followup]
---

# Group 9c — Warehouse Cutover: D2c consistency closure (Codex findings #5 + #7)

## Brief
GROUP:          Warehouse Cutover — 9c D2c consistency closure (SAW-31)
ORDER:          9c/10 (follow-up to 9b; closes two consistency gaps the independent Codex review found)
REPO:           SPQR (generic; A18 generic-first)
RUN_CONTAINER:  /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:        /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/09c-warehouse-cutover-d2c-consistency.md
RATIONALE:      Independent Codex review found two leftovers that contradict the 9b Probator-as-proposer change: the ingest skill's proposer list/blanket, and the bug-pipeline sink wording. Two-file consistency closure; no new decision (the decision is D2c + its 9b extension).
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md  (D2c + the F2/9b extension; DERIVE, do not re-decide)
FILL_CHANGES_MADE: yes

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md
  - docs/agents/probator.md            (the 9b end-state these two files must agree with)

DEPENDENCY GATE: 9b GREEN (probator.md carries the narrow propose right + the close-lesson-as-proposal). STOP if absent.

## Scope — exactly two files, align them with the 9b Probator end-state

## FILES (2)
  docs/skills/warehouse-ingest.md:
   - Proposer list (≈ line 16): ADD Probator — ONLY for its CORRECTIO close lesson (D2c extension; scrutinize-on-read ⊥ a narrow propose right).
   - The blanket "Scrutinize agents read but do not author" (≈ line 18): correct it — Probator is the one scrutinize exception (the CORRECTIO close lesson); **Tribunus and Curator** read but do not author. Keep read-before-propose mandatory for every proposer.
  docs/skills/bug-pipeline.md:
   - The sink statement (line 46 "today LESSONS.md; soon the Warehouse … one-line swap"): reconcile to v1.5 warehouse-primary — the project-knowledge sink IS the warehouse; the close routine-knowledge entry is a **lesson-node proposal** to the antechamber via `docs/skills/warehouse-ingest.md` (read-before-propose; `propose` is free). LESSONS.md is not deleted this run (separate later owner SAW).

## Scope fence — do NOT do (flag if found, per Law 1)
- These two files ONLY. Do NOT touch probator.md (9b, done), curator.md / tribunus.md (correctly non-authoring — leave their "no propose right" as-is), or any other agent / Group-10 file.
- Do NOT give Tribunus or Curator a propose right (only Probator among reviewers authors — the CORRECTIO close lesson).
- Do NOT delete LESSONS.md or hardcode a warehouse path beyond the documented CLI.

## Changes Made

Dependency gate verified before any edit: `docs/agents/probator.md` (9b end-state) carries the narrow propose right + the close-lesson-as-proposal (probator.md:33, :47–48, :55). **9b GREEN — gate passed.** Two files aligned to that end-state; no new decision (derived from D2c + its F2/9b extension in the PoC). No commit.

### 1. `docs/skills/warehouse-ingest.md` — WHO LOADS THIS (was lines 15–18)
- ADDED Probator to the proposer set, scoped to its ONE narrow authoring act — the CORRECTIO close lesson (D2c extension; scrutinize-on-read ⊥ a narrow propose right).
- CORRECTED the blanket: the old "Scrutinize agents read but do not author" was a flat contradiction of 9b. Now: "Among the scrutinize agents Probator is the sole exception; **Tribunus and Curator** read but do not author." Probator's exception is bounded to the CORRECTIO close lesson.
- Reasserted "Read-before-propose is mandatory for every proposer" so the new proposer inherits the dup-defence discipline.
- Untouched: Praetor / Quaestor / Censura proposer entries; the rest of the contract.

### 2. `docs/skills/bug-pipeline.md` — PROBATOR CLOSE, sink statement (line 46)
- RECONCILED the stale sink wording ("today LESSONS.md; soon the Warehouse (v1.5) … one-line swap") to v1.5 warehouse-primary: the routine knowledge entry is now "authored at close as a **lesson-node proposal** to the warehouse antechamber via `docs/skills/warehouse-ingest.md`." The project-knowledge sink **IS** the warehouse.
- Recorded the proposer discipline: read-before-propose mandatory; `propose` is free (no owner HITL — the gate + Senate judgment is the control).
- Recorded that the flat `LESSONS.md` append is retired in favour of the proposal, and that **LESSONS.md is not physically deleted this run** (separate later owner SAW).
- This now matches probator.md:23 and the BUG CLOSE MODE block; the D8 reference is preserved.

### Scope fence honoured
- Exactly the two briefed files. probator.md (9b, done), curator.md, tribunus.md, and all Group-10 files left untouched.
- No propose right granted to Tribunus or Curator — they remain correctly non-authoring (read-only).
- LESSONS.md not deleted; no warehouse path hardcoded beyond the documented CLI / skill reference.

### Observation (in-scope, no action taken — Law 1/Law 4)
- `bug-pipeline.md:49` (D7b, conditional Censura) reads "Censura … runs ONLY to expand the repo **project-knowledge sink**". With the sink now reconciled to the warehouse this phrasing stays consistent (Censura's lesson write is already a proposal per D2c in `senate.md`), and it falls outside this brief's two-file scope, so it was left as-is. Flagging for master visibility only — no change recommended.
