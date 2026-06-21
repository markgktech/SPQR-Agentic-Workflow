---
up: "[[v1.5]]"
group: "Warehouse Cutover — D2-phrasing exhaustive close (SAW-31)"
order: 10-amend-b/10
saw: [SAW-31]
ticket: SAW-31
status: pending
type: brief
tags: [group, warehouse, cutover, brief, amendment]
---

# Group 10-amend-b — D2-phrasing exhaustive close (the last 4 "owner-run" instances)

## Brief
GROUP:          Warehouse Cutover — D2-phrasing exhaustive close (SAW-31)
ORDER:          10-amend-b (completes 10-amend; the master's corpus-wide grep for the D2-superseded "owner-run/runs" phrasing — the definitively last D2-wording pass)
REPO:           SPQR (generic)
RUN_CONTAINER:  /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:        /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/10-amend-b-d2-phrasing-exhaustive.md
RATIONALE:      The D2 refinement (owner-executes → agent-executes-on-owner-HITL) landed mid-run; per-finding patches each missed instances. A master corpus-wide grep (docs/agents + docs/skills + docs/retro) found exactly four remaining D2-stale "owner-run" instances — fix all four in one pass. No new decision.
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md  (D2 final; F4)
FILL_CHANGES_MADE: yes

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md   (D2 final = agent-executes-on-owner-HITL)
  - docs/skills/warehouse-usage.md   (the who-runs-CLI matrix rows 30-35 are the canonical reference these must agree with)

DEPENDENCY GATE: 10-amend GREEN. STOP if any target line moved.

## Scope — exactly four wording deltas; reconcile the session-start/sweep/audit-attribution phrasing to final D2 (agent-executed on owner HITL). No behaviour change.

## FILES (4)
  docs/agents/session-starters.md (line ~23): "daemon-free — the owner runs these and pastes the result into the Senate session" → the Senate (agent) runs `check`/`audit` on session-open (agent-executed on owner HITL) and surfaces the result. (Matches warehouse-usage.md session-start + matrix row 33.)
  docs/skills/warehouse-usage.md (line ~86): "read-only; the owner runs the resulting flag-resolution sweep" → the flag-resolution sweep is agent-executed on owner HITL (D3) — matches this doc's own matrix row 34. (The retro SURFACES; it does not write.)
  docs/retro/retrospector.md (line ~39): "the most recent owner-run session-start `audit` JSON" → "the most recent session-start `audit` (agent-run on owner HITL)". Attribution only — the read itself is unchanged.
  docs/retro/input.md (line ~11): same "owner-run session-start `audit`" attribution → "session-start `audit` (agent-run on owner HITL)".

## Scope fence — do NOT do (flag if found, per Law 1)
- These four lines ONLY. Do NOT touch the CORRECT owner-manual lines: `warehouse-usage.md:68` + `:89` (semantic-audit by-hand) · `retrospector.md:42` (semantic-audit recommend) · `warehouse-usage.md:102` (later owner-run migration step) · `warehouse-usage.md:35` (reconcile/check maintenance grouping) · `doc-maintenance.md:60` (not warehouse).
- Do NOT change any decided behaviour or the retro LESSONS.md framing (#5a → residue sweep) or the mode enum (#5b → ticket).

## Changes Made

Four D2-phrasing deltas applied (owner-run → agent-executed on owner HITL). No behaviour change; attribution/phrasing only. All reconcile to the warehouse-usage.md who-runs-CLI matrix (rows 33–34) and D2 final.

1. **docs/agents/session-starters.md:23** — SENATE PRE-STEP parenthetical.
   - Before: "(daemon-free — the owner runs these and pastes the result into the Senate session)"
   - After:  "(daemon-free — the Senate agent runs `check`/`audit` on session-open and surfaces the result, agent-executed on owner HITL)"
   - Now matches warehouse-usage.md §3 session-start line + matrix row 33.

2. **docs/skills/warehouse-usage.md:86** — §3 "At retro" flag-sweep attribution.
   - Before: "(D6 hook 2 / D3) — read-only; the owner runs the resulting flag-resolution sweep."
   - After:  "(D6 hook 2 / D3) — read-only; the resulting flag-resolution sweep is agent-executed on owner HITL (D3)."
   - Now matches this doc's own matrix row 34 (flag `resolves` = agent-executed on owner HITL). Retro still SURFACES, does not write — unchanged.

3. **docs/retro/retrospector.md:39** — AUDIT-FLAG HARVEST step 1 source attribution.
   - Before: "the most recent owner-run session-start `audit` JSON — D6 hook 1, the act that emits flags"
   - After:  "the most recent session-start `audit` (agent-run on owner HITL) JSON — D6 hook 1, the act that emits flags"
   - Attribution only; the read (read-only, no `audit` run by retro) is unchanged.

4. **docs/retro/input.md:11** — LOAD ORDER item 5 source attribution.
   - Before: "the open flags + per-node heat from the most recent owner-run session-start `audit` JSON (D6 hook 1)"
   - After:  "the open flags + per-node heat from the most recent session-start `audit` (agent-run on owner HITL) JSON (D6 hook 1)"
   - Attribution only; "never run `audit`" guard unchanged.

**Verification:** corpus-wide grep (`owner[ -]runs?|owner runs these` over docs/agents + docs/skills + docs/retro) before/after. After the edits, the only remaining matches are the four scope-fenced CORRECT owner-manual lines — `warehouse-usage.md:35` (reconcile/check maintenance), `warehouse-usage.md:89` (semantic-audit recommend "the owner runs it"), `warehouse-usage.md:102` (later owner-run migration step), `retrospector.md:42` (semantic-audit recommend) — all left untouched per the Scope fence. Zero D2-stale "owner-run" instances remain in the corpus.

**Scope fence honoured:** only the four brief-named lines changed. No behaviour, no LESSONS.md framing (#5a residue), no mode enum (#5b) touched. No out-of-scope discovery. Not committed (owner commits).

**Dependency gate:** all four target lines matched the brief's expected text at the stated approximate line numbers — none had moved. 10-amend GREEN, proceeded.
