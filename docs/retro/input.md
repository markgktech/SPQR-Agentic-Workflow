---
name: retro-input
description: RETROACTIO pre-flight — load order, git boundary (marker-based, not commit messages), session_id; qualitative signals only
---

LOAD ORDER
1. AGENT_LAWS.md
2. docs/LESSONS.md — historical / pre-cutover lessons, read-only (full file since the last --- divider, for continuity). Under warehouse-primary it no longer grows — Censura proposes lesson-nodes to the warehouse, not LESSONS.md — so the live lesson signal is the Censura verdict blocks (item 4) + new warehouse lesson-nodes (read where the project's knowledge has been migrated), NOT LESSONS.md length.
3. Previous retro local file — via the `Retroactio.md` MOC; read fully for continuity; skip if first run
4. Censura verdict block from each in-scope ticket's local `<TICKET-ID>_handover.md` — **the PRIMARY lesson signal** (always present in the handover record, warehouse or not) — that block ONLY, not full handover chains or ticket bodies (token cost)
5. Warehouse audit flag/heat state (SAW-31) — the open flags + per-node heat from the most recent session-start `audit` (agent-run on owner HITL) JSON (D6 hook 1) / the derived `v_flag_status` view; read-only, derived-at-harvest (NO standing store). Read the flag plane only — never run `audit` (it emits flags = a write). Skip if the warehouse is not in use. Feeds retrospector.md AUDIT-FLAG HARVEST.
6. docs/retro/discussion.md — load before presenting findings; do NOT load output.md yet

REPO STATE (supplement, not primary)
git is a supplement for file-level ground truth, cross-checked against what tickets/comments claimed changed:
- git diff --stat <marker>..HEAD — committed churn since the previous retro's marker
- git status + git diff --stat — uncommitted working tree (work not yet committed)
Marker = the date / explicit marker recorded by the previous retro (output.md), NOT a commit boundary.
NOT commit messages or commit cadence — owner-only commit means those reflect the owner's commit habit, not work structure.
No full diffs by default — full diff only for a specific file under active investigation.
Read-only git (log / diff / status) — never touches the commit/push rule.

SESSION ID
Retrieve via: echo $CLAUDE_CODE_SESSION_ID — written as retro frontmatter by output.md.

SCOPE BOUNDARY
Metrics at this rung = qualitative record signals already in the record: Censura findings (the primary signal), historical LESSONS.md flags (read-only / pre-cutover), git --stat churn — enough to see "what's bleeding" without overhead.
Derived, harvested-at-retro detection counters (the four SAW-27 sensors, derived from this same record at retro time — see retrospector.md HARVEST + INTERPRETATION) are IN scope. The warehouse open-flag + per-node heat read (SAW-31) is the same shape — a derived-at-harvest read of the audit plane, IN scope; the retro reads and surfaces, it never runs `audit` and never writes `resolves`. A standing telemetry store / quantitative instrumentation — a separate aggregation surface that persists between runs — stays OUT of scope (a later north-star rung). Do not over-build into formal instrumentation.

NEVER
Never start the discussion phase before all LOAD ORDER items are read
Never read full ticket bodies or full handover chains — the Censura verdict block only
Never rely on commit messages or commit cadence as a work-structure signal
Never load full diffs by default
Never carry state from a prior session — start cold (Law 3)
Never build a standing telemetry store / quantitative instrumentation — out of scope this rung; the SAW-27 detection counters are derived at retro time from the record, not a persisted aggregation surface
Never run the warehouse `audit` or write `resolves` from the retro — read the derived flag/heat state only; flag emission is the owner's session-start act (D6 hook 1) and resolution is the owner-HITL sweep (D3)
