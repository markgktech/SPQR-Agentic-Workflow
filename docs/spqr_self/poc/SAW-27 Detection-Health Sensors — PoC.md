---
type: poc
title: "SAW-27 Detection-Health Sensors — PoC"
decides: "The thin telemetry-sensor now-wedge: which deterministic detection counters, derived how, harvested where, and how the retro reads them (left-shift + balance)."
status: draft
date: 2026-06-19
tags: [poc, decision, telemetry]
up: "[[SAW-27]]"
---

# SAW-27 Detection-Health Sensors — PoC

## Context / question
SPQR does not measure where in the pipeline a defect is caught, so the detection net can drift toward the costliest last gate unnoticed. SAW-27 is the thin now-wedge under the [[SAW-24]] epic: define deterministic detection counters from existing signals, harvested at ticket close, with the metric reframe ("health = left-shift; Censura-RED = upstream-gate failure, not success"). Residue guard: NOT a hand-maintained registry. Horizon (2.0/3.0, NOT here): [[Future Observe Layer & Orchestration Horizon — Research Note]].

Decisions D1–D8 below were pressure-tested in the Phase-2 Roundtable (Dev Process Architect / Agentic Trends Expert) and confirmed by the owner. Each: **what · why · affected · type**.

## Decisions

### D1 — Sensor set (MODIFY) #decision
- **what:** Four detection sensors: *verdict color + round* (derived), *revision rounds* (derived), *where-caught / veto-stage* (inferred), *recurring-failure category* (keys on the D7 enum). `files_loaded` is **dropped** (cost moves to the hub, D5).
- **why:** Three are directly derivable from the append-only handover; `files_loaded` was a noisy, obsolete token-proxy that duplicates the real hub cost. Thin sensor, not registry.
- **affected:** `retrospector.md` (harvest), `censura-output.md` (D7 enum for recurring).

### D2 — Derivation rules (CONFIRM) #decision
- **what:** *verdict + round* = count `### Senate Censura` blocks; *revision rounds* = count `### Praetor`/amendment blocks (append-only ⇒ countable). *where-caught* = the first block in order whose verdict is non-PASS (FAIL/RED) — its `<Agent>` is the catching stage; kept **inferred**, no `vetoed_by` self-report field. *recurring* keys on the D7 enum, never on free-text `[area]`.
- **why:** where-caught as an inferred trace signal is not gameable (a self-reported veto field would be); recurring needs a deterministic key, which free-text cannot provide.
- **affected:** `retrospector.md` harvest step.

### D3 — Execution model (CONFIRM) #decision
- **what:** A derivation/harvest pass run **at retro time** over the record since the last marker. **No standing aggregation store.** The sensor SPEC lives inside `retro/input.md` + `retrospector.md` (NOT a new skill file). The trend persists in the **retro output lineage** (`retro/output.md` CLOSING MARKER + `Retroactio.md` MOC — mechanism already exists).
- **why:** Residue guard (epic: not a hand-maintained registry); at SPQR's low volume a standing store is over-build with nothing to read; a standalone sensor-spec file would itself be residue (fires only in one pipeline).
- **affected:** `retro/input.md`, `retrospector.md`.

### D4 — Retro re-point (MODIFY) #decision
- **what:** **Reframe (do not delete)** the quantitative-telemetry ban in all four locations — `retro/input.md:27`, `:35`, `retrospector.md:20`, `:49` — to: *derived, harvested-at-retro counters are in scope; a standing telemetry store / quantitative instrumentation remains out of scope*. Add a harvest + interpretation step to `retrospector.md` expressed as **operations, not a "lens"**: (a) derive the four counters since the last marker; (b) **counterfactual guard** — compare where-caught only across runs that reached the **same terminal stage** (truncated runs are not left-shift); (c) the **balance metric** (A); (d) report **trend across markers + narrative, never a threshold/dashboard number**.
- **why:** Editing only `input.md` leaves `retrospector.md:49` vetoing the harvest → the reader-loop stays open. Reframing preserves the valid residue guard while admitting the sensor. "Add the left-shift lens" is not actionable for a stateless agent; the operation is.
- **affected:** `retro/input.md` (:27, :35), `retrospector.md` (:20, :49 + new step).

### D5 — Cost telemetry (CONFIRM) #decision
- **what:** Cost lives in the hub `## Session / cost` table, owner-filled manually via `/usage`. **No new build.** SAW-27 must not duplicate it elsewhere.
- **why:** The table and the manual-fill convention already exist (`praetor-output.md:15`, plus all executor outputs). Cross-window `/usage` aggregation stays out of scope (→ 2.0).
- **affected:** none (confirmation only).

### D6 — Reframe placement (CONFIRM) #decision
- **what:** Document the metric reframe at the **read-side** (`retrospector.md` harvest/interpretation step), **co-located with the balance metric**: "a Censura-RED caught upstream is a gate working; the failure signal is escape-to-owner / post-close defect, not RED count." Do **not** edit `censura-output.md` verdict semantics — a RED is still a RED at emit time.
- **why:** The reframe is a read-side interpretation, not an emit-time behavior change; pairing it with the balance metric in the same place prevents the Goodhart misread (optimizing toward fewer REDs by weakening gates).
- **affected:** `retrospector.md`.

### D7 — Failure-category enum (MODIFY) #decision
- **what:** Add a `[category:<enum>]` token to the `censura-output.md` findings format (currently `:30`): `[PASS|FAIL|RISK|NOTE] [category:<enum>] [area] [Impact] [Effort] — …`. Enum = 4–6 values **evidence-seeded from LESSONS** (e.g. `receipt-missing`, `scope-creep`, `test-gap`, `spec-ambiguity`) + `other`. The *recurring* sensor (D1/D2) keys on this.
- **why:** Free-text `[area]` cannot match deterministically across runs ("missing receipt" ≠ "no receipt"); the enum makes recurring a real countable sensor. Additive token — does not touch the PASS/FAIL/RISK/NOTE enum, impact/effort tags, or receipt enforcement. Keep it small + evidence-seeded so producers don't mis-bucket (a forced taxonomy would inflate recurring with leakage).
- **affected:** `censura-output.md` (:30 findings format).

### D8 — Transport-drift wording (CONFIRM — residue) #decision
- **what:** Correct SAW-27/SAW-24 spec wording from "ticket-comment template / Notion comment" to **"local `<TICKET-ID>_handover.md` (ticket-comment.md field contract, preserved verbatim per `ticket-comment.md:3`)."** Real harvest surfaces: `<TICKET-ID>_handover.md` + `docs/LESSONS.md` + hub `## Session / cost`.
- **why:** The text predates the SAW-33 transport swap; the field contract is intact but the physical surface changed from Notion comment to local handover. Pure residue cleanup — prevents a future implementer hunting for Notion comments that no longer exist.
- **affected:** SAW-27 / SAW-24 ticket text (owner, Notion); spec references in the run brief.

## Owner calls (folded in)

### A — Balance metric: escape-to-owner (MODIFY — owner-approved scope addition) #decision
- **what:** Add **escape-to-owner** as a paired counter. **v1 = the in-record half only:** a FAIL surfaced in a Censura block routed to OWNER. The **post-close half** (defects found after ticket close) is **deferred** (see Open items).
- **why:** left-shift alone is one-directional and gameable (Goodhart): weaker gates lower late-RED counts while quality drops. escape-to-owner rises when gates weaken, so the pair cannot both be gamed at once — left-shift only reads as health if escape-to-owner does not rise.
- **affected:** `retrospector.md` (harvested + interpreted alongside left-shift, D4/D6).

### C — Retro template trend section (STALLED → owner/project action) #decision
- **what:** `templates/retro_template.md` needs a trend/sensor section so the harvested counters have a sink; `retro/output.md:13` forbids ad-hoc template additions, so without this slot the reader-loop is NOT closed.
- **why:** Cross-surface dependency the generic skill edits cannot cover alone; the retro template is project-owned and must be reconciled generic→project via the propagation mechanism.
- **affected:** `templates/retro_template.md` (owner/project-side) + propagation.

### D — Enum governance (CONFIRM) #decision
- **what:** The enum **definition lives with the producer** (`censura-output.md`, since Censura writes the tag). The **retro flags candidate new categories** ("a recurring failure-mode doesn't fit the enum → propose adding"), owner decides — matching the existing rule-rot "flag, owner decides" pattern.
- **why:** The retro reads but does not write the tag, so it cannot own the definition; it is well placed to propose additions from observed recurrence.
- **affected:** `censura-output.md` (definition), `retrospector.md` (flag candidate).

## Open items (flag-only — owner creates the SAW ticket; Notion assigns the ID)
- **STALLED — Post-close-defect tracking** (the post-close half of the balance metric, A): ride on CORRECTIO (SAW-29) by linking a bug to its originating ticket; the retro then counts CORRECTIO bugs tracing to recently-closed tickets. Needs a CORRECTIO-link convention → future ticket.
- **UNRESOLVABLE — Long-term enum-vocabulary curation:** ongoing governance of the failure-category list as new modes appear (beyond the v1 retro-flag mechanism). Flag; do not block.

## Scope boundary
Generic SPQR only this run (skills under `docs/skills/`, `docs/retro/`). Project-side pieces — the retro template trend section (C) and the SAW-27/SAW-24 ticket-text fix (D8) — are owner/project actions reconciled via propagation, consistent with prior v1.5 runs.

## Recommendation / decision
Adopt D1–D8 + owner calls A/C/D as above. Planning (Phase 4) derives the execution brief(s) from this PoC; the run-container MAIN note links this PoC and does not inline the decisions.
