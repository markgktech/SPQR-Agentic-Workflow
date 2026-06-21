You are an execution agent for SPQR upgrade run v1.5, Group 14 (SAW-44 — warehouse robot propagation).

PRE-FLIGHT (load in order):
  - docs/upgrade/execution.md
  - docs/spqr_self/poc/SAW-44 Warehouse Robot Propagation — PoC.md   (SOURCE OF TRUTH — read fully first; D1/D2/D3)
  - docs/upgrade/propagation-manifest.md   (file to edit #1)
  - docs/upgrade/propagation-agent.md      (file to edit #2)

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/14-warehouse-robot-propagation.md

Read the Brief there, do the work, then fill its "## Changes Made" section
(replace the sentinel). Do not touch MAIN or sibling sub-docs. Do not commit.

CRITICAL — SCOPE IS DELIBERATELY MINIMAL (owner-simplified after roundtable over-engineering):
  - Only two files change: propagation-manifest.md + propagation-agent.md. Markdown only, NO executable code (AM4).
  - DO NOT build any number-comparison, robot CLI command, or robot-reported-version mechanism. The "handbrake" (D3) is a single documented stop rule in the agent's instructions — release-notes-driven, not a computed check.
  - DO NOT touch warehouse_robot/ itself, any consuming project, or any warehouse data.
  - The one technical nuance that MUST land (D2): in propagation-agent.md PIPELINE step 3, state that verbatim/code paths (warehouse_robot/) SKIP token re-instantiation and the token-absence fail-loud — otherwise the robot's regex literals (e.g. `[a-z][a-z0-9-]*`) would falsely halt propagation. This is required for the plain copy to work, not extra machinery.
  - Record explicitly that D1 SUPERSEDES the SAW-38 deferred "out-of-band" warehouse_robot note (ref SAW-44) — the reversal must not be silent.
  - Derive every edit from the PoC (D1/D2/D3), not from this starter's summary.
