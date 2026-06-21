You are an execution agent for SPQR upgrade run v1.5, Group 10 (SAW-31 Warehouse Cutover — observers + usage/doc-regime; Agent B).

GATE: launch only AFTER Group 9 is owner-confirmed complete (its Changes Made filled). Group 10 depends on the Group-9 ingest skill + propose action.

PRE-FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md
  - warehouse_robot/docs/QUERY_PROTOCOL.md
  - warehouse_robot/docs/AUDIT_PROTOCOL.md
  - docs/spqr_self/upgrades/v1.5/09-warehouse-cutover-agent-layer.md   (dependency context)
  - docs/spqr_self/upgrades/v1.5/06-detection-health-sensors.md        (the SAW-27 retro-reader pattern this mirrors)

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/10-warehouse-cutover-observers-docs.md

Read the Brief there, do the work (handoff D4-LEAN + retro audit-reader + the owner usage/doc-regime doc), then fill its "## Changes Made" section (replace the _(pending execution)_ sentinel). Honour the brief's Scope fence (retro is read-only — no `resolves` write; no project-side retro_template). Do not touch MAIN (v1.5.md) or sibling sub-docs (09-*). Do not commit.
