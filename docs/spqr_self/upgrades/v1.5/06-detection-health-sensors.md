---
up: "[[v1.5]]"
group: "Detection-health telemetry sensors — derived counters + retro reader"
order: 6/6
saw: [SAW-27]
tags: [group]
---

# Group 6 — Detection-health telemetry sensors (SAW-27)

## Brief
GROUP:         Detection-health telemetry sensors
ORDER:         6/6
REPO:          SPQR (generic only this run; project-side retro template + SAW-27/SAW-24 ticket-text via owner/propagation, sequenced separately)
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/06-detection-health-sensors.md
RATIONALE:     One coherent read-side surface — the retro harvest/interpretation step plus the single producer field (Censura enum) it keys on.
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-27 Detection-Health Sensors — PoC.md
FILL_CHANGES_MADE: yes
PRE_FLIGHT:
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-27 Detection-Health Sensors — PoC.md   (SOURCE OF TRUTH — all decisions D1–D8 + A/C/D; derive, do not re-decide)
  - docs/skills/ticket-comment.md   (handover field contract — verdict/where-caught/revision/routing live here; the harvest source)
  - docs/retro/input.md
  - docs/retro/retrospector.md
  - docs/retro/output.md            (lineage: CLOSING MARKER + Retroactio MOC = where the trend persists; the template SLOT itself is owner/project-side, NOT edited here — see C)
  - docs/skills/censura-output.md
  - docs/LESSONS.md                 (evidence source for seeding the failure-category enum, D7)
FILES:
  - docs/retro/input.md: reframe the quantitative-telemetry ban (SCOPE BOUNDARY `:27` + NEVER `:35`) — derived, harvested-at-retro detection counters are IN scope; a standing telemetry store / quantitative instrumentation stays OUT (D3/D4).
  - docs/retro/retrospector.md: reframe the ban (READS `:20` + NEVER `:49`); add a harvest + interpretation step (D2/D4/D6/A/D) — derive the 4 counters since the last marker; counterfactual guard (compare where-caught only across same-terminal-stage runs); balance metric escape-to-owner (v1 = in-record FAIL routed to OWNER); co-locate the metric reframe read-side; report trend + narrative, never a threshold; retro flags candidate new enum categories (owner decides — rule-rot pattern).
  - docs/skills/censura-output.md: add a `[category:<enum>]` token to the findings format (`:30`) — 4–6 evidence-seeded values (e.g. receipt-missing, scope-creep, test-gap, spec-ambiguity) + `other`; this is the enum DEFINITION home; the recurring sensor keys on it (D7/D). Additive token only — do NOT touch the PASS/FAIL/RISK/NOTE enum, impact/effort tags, receipt enforcement, or verdict semantics (D6).

## Out of scope for this group (owner / project-side — flagged, not edited here)
- **C — retro template trend section** (`templates/retro_template.md`): the sink for the harvested trend; `retro/output.md:13` forbids ad-hoc template additions, so this is an owner/project edit reconciled generic→project via propagation.
- **D8 — SAW-27/SAW-24 ticket-text wording fix** (Notion, owner): "ticket-comment template / Notion comment" → "local `<TICKET-ID>_handover.md` (ticket-comment.md field contract)".
- **Open items:** post-close-defect tracking via CORRECTIO link; long-term enum-vocabulary curation → future owner SAW tickets.

## Changes Made

### 1. `docs/retro/input.md` — reframed the quantitative-telemetry ban (D3/D4)
- **`:27` SCOPE BOUNDARY** — replaced the flat "Quantitative telemetry is OUT of scope" line. Now: derived, harvested-at-retro detection counters (the four SAW-27 sensors) are **IN** scope; a standing telemetry store / quantitative instrumentation (a persisted aggregation surface) stays **OUT**. Cross-points to retrospector.md HARVEST + INTERPRETATION.
- **`:35` NEVER** — reframed "Never build quantitative instrumentation" → "Never build a **standing** telemetry store / quantitative instrumentation … the SAW-27 counters are derived at retro time from the record, not a persisted aggregation surface."
- **Verification:** `grep -n "OUT of scope\|instrumentation\|telemetry"` returns only the two reframed lines (`:27`, `:35`) — no naked ban remains; both surviving mentions scope the ban to a *standing store*.

### 2. `docs/retro/retrospector.md` — reframed the ban + added the harvest/interpretation step (D2/D4/D6/A/D)
- **`:20` READS** — reframed last sentence: the four counters are **derived from the same record signals at harvest time**; a standing store remains OUT. Points to the new HARVEST + INTERPRETATION section.
- **`:49`→`:64` NEVER** — reframed to ban a *standing* store only; added a second NEVER: "Never auto-add a failure-category enum value — flag a candidate, owner decides."
- **New `HARVEST + INTERPRETATION (SAW-27 detection counters)` section** (after READS) — expressed as **operations, not a lens**: (1) derive the 4 counters since the last marker — verdict color+round (`### Senate Censura` blocks), revision rounds (`### Praetor`/amendment blocks), where-caught (first non-PASS block in order, **inferred**, no `vetoed_by`), recurring-failure category (keys on the `[category:<enum>]` token, not free-text `[area]`); (2) **counterfactual guard** — compare where-caught only across same-terminal-stage runs; (3) **balance metric escape-to-owner**, v1 = in-record half (FAIL routed to OWNER), post-close half deferred → CORRECTIO; (4) **read-side metric reframe** co-located — a Censura-RED caught upstream = a gate working, failure signal is escape-to-owner not RED count; (5) report **trend across markers + narrative, never a threshold/dashboard number**.
- **New `ENUM GOVERNANCE (D)` section** — retro FLAGs a candidate new enum category when a recurring failure doesn't fit (owner decides — rule-rot pattern); never auto-adds; definition stays with the producer.
- **Verification:** `grep -n` confirms reframed `:20`/`:64`, `HARVEST + INTERPRETATION` (`:22`), `ENUM GOVERNANCE` (`:34`), and `escape-to-owner` (`:30`/`:31`). No template-section / code / skill edits — stays inside this file's existing NEVER constraints (reads the enum, does not write it; no standing store).

### 3. `docs/skills/censura-output.md` — added the `[category:<enum>]` token + enum definition home (D7/D)
- **`:30` findings format** — added the token additively: `[PASS|FAIL|RISK|NOTE] [category:<enum>] [area] [Impact] [Effort] — …`.
- **New `[category:<enum>] — FAILURE-CATEGORY ENUM` block** (before ON RED — EXPLORACIO) — the **definition home**. Evidence-seeded values: `receipt-missing · scope-creep · test-gap · spec-ambiguity · other` (5 values; LESSONS.md currently holds no run entries, so seeded from the PoC D7 set established in the Roundtable). Explicit guard: additive token only — does **not** touch the PASS/FAIL/RISK/NOTE enum, impact/effort tags, receipt enforcement, or verdict semantics (a RED stays a RED at emit time). Producer writes; retro reads + may flag candidates.
- **Verification:** `grep -n` confirms the token at `:30`, the definition header at `:38`, and the seeded enum at `:40`. PASS/FAIL/RISK/NOTE enum, receipt enforcement, and verdict semantics untouched.

### Out-of-scope — flagged, NOT acted on (per brief / Law 1)
- **C — retro template trend section** (`templates/retro_template.md`): the sink for the harvested trend is still owner/project-side; `retro/output.md:13` forbids ad-hoc template additions, so the reader-loop is **not fully closed** until this slot is added via generic→project propagation. Surfaced for the master.
- **D8 — SAW-27/SAW-24 ticket-text wording fix** (Notion, owner): "ticket-comment template / Notion comment" → "local `<TICKET-ID>_handover.md`".
- **Open items:** post-close-defect tracking via CORRECTIO link; long-term enum-vocabulary curation → future owner SAW tickets.

### Notes for the master (Law 4)
- **LESSONS.md is empty of run entries** (header only). The D7 "evidence-seeded from LESSONS" instruction was satisfied from the PoC's already-seeded set, not from live entries. As real entries accumulate, the enum should be revisited against actual recurrence (this is the deferred "long-term enum curation" open item — worth a first review at the next retro).
- All four ban locations were **reframed, not deleted** — verified the loop closes (retrospector.md:64 no longer vetoes the harvest). No git commit/push run; generic SPQR only; no Foodoire / MAIN-note / sibling-sub-md files touched.
