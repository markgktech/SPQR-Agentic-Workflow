You are an execution agent for SPQR upgrade run v1.5, Group 6 (Detection-health telemetry sensors — SAW-27).

PRE-FLIGHT (load in order):
  - .claude/rules/AGENT_LAWS.md                                             (the four laws — apply before any action)
  - docs/upgrade/execution.md                                              (execution protocol — receive brief, execute only)
  - docs/spqr_self/upgrades/v1.5/06-detection-health-sensors.md            (YOUR BRIEF — FILES + out-of-scope list; where you write Changes Made)
  - docs/spqr_self/poc/SAW-27 Detection-Health Sensors — PoC.md           (SOURCE OF TRUTH — decisions D1–D8 + owner calls A/C/D; derive, do NOT re-decide)
  - docs/skills/ticket-comment.md                                          (handover field contract — verdict/where-caught/revision/routing live here; the harvest source — read, do NOT edit)
  - docs/retro/output.md                                                   (lineage: CLOSING MARKER + Retroactio MOC = where the trend persists; the template SLOT is owner/project-side — read, do NOT edit)
  - docs/LESSONS.md                                                        (evidence source for seeding the failure-category enum, D7)
  - docs/retro/input.md , docs/retro/retrospector.md , docs/skills/censura-output.md   (the 3 EDIT TARGETS — read current form first)

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = docs/spqr_self/upgrades/v1.5/06-detection-health-sensors.md

Read the Brief there, do the work on the 3 FILES listed, then fill its "## Changes Made" section (replace the _(pending execution)_ sentinel) — file by file, with a short Verification block.

Key reminders (full rationale in the PoC — D1–D8 + A/C/D):
  - Sensor set (D1): 4 detection counters DERIVED from the existing record — verdict color+round, revision rounds, where-caught, recurring. files_loaded is DROPPED (cost lives in the hub Session/cost table — do NOT add a cost counter here).
  - Derivation (D2): where-caught = the first block in order with a non-PASS verdict — KEEP IT INFERRED, do NOT add a self-reported `vetoed_by` field. recurring keys on the D7 enum, never on free-text `[area]`.
  - Execution model (D3): the harvest runs AT retro time over the record since the last marker. NO standing aggregation store. The spec lives INSIDE retro/input.md + retrospector.md — do NOT create a new skill file. Trend persists in the existing retro output lineage.
  - Ban reframe (D4): the quantitative-telemetry ban appears in FOUR places — retro/input.md `:27` + `:35`, retrospector.md `:20` + `:49`. REFRAME all four (do NOT just delete): derived, harvested-at-retro counters are IN scope; a standing telemetry store / quantitative instrumentation stays OUT. Editing only input.md leaves retrospector.md:49 vetoing the harvest — the loop must close.
  - Harvest + interpretation step in retrospector.md (D4/D6/A): express OPERATIONS, not a "lens" — (a) derive the 4 counters since the last marker; (b) counterfactual guard: compare where-caught ONLY across runs that reached the SAME terminal stage (truncated runs ≠ left-shift); (c) balance metric escape-to-owner, v1 = in-record half only (a FAIL surfaced in a Censura block routed to OWNER) — post-close half is deferred; (d) co-locate the metric reframe read-side ("a Censura-RED caught upstream = a gate working; the failure signal is escape-to-owner, not RED count"); (e) report TREND across markers + narrative, NEVER a threshold/dashboard number.
  - Enum (D7): add a `[category:<enum>]` token to the censura-output.md findings format (`:30`) — `[PASS|FAIL|RISK|NOTE] [category:<enum>] [area] [Impact] [Effort] — …`. Enum = 4–6 values SEEDED FROM what LESSONS actually shows recurring (e.g. receipt-missing, scope-creep, test-gap, spec-ambiguity) + `other`. Additive token ONLY — do NOT touch the PASS/FAIL/RISK/NOTE enum, impact/effort tags, receipt enforcement, or verdict semantics (a RED stays a RED at emit time, D6). This file is the enum DEFINITION home.
  - Enum governance (D): retrospector.md should also let the retro FLAG a candidate new enum category when a recurring failure doesn't fit (owner decides — matches the existing rule-rot "flag, owner decides" pattern). Do NOT auto-add categories.
  - OUT OF SCOPE — do NOT edit (flag only, owner/project-side): templates/retro_template.md trend section (C, via propagation); the SAW-27/SAW-24 ticket-text wording fix (D8, Notion); post-close-defect tracking + long-term enum curation (open items).
  - Generic SPQR only. Do NOT touch any Foodoire / consuming-project file. Do NOT touch the MAIN folder-note (v1.5.md) or sibling sub-docs. Do NOT run git commit or git push.

Report at the end; flag any out-of-scope discovery for the master — do not act on it.
