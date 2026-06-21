You are an execution agent for SPQR upgrade run v1.5, Group 9c (SAW-31 — D2c consistency closure; Codex findings #5 + #7).

PRE-FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md
  - docs/agents/probator.md   (the 9b end-state these two files must agree with)

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/09c-warehouse-cutover-d2c-consistency.md

Read the Brief there, apply the two-file alignment: docs/skills/warehouse-ingest.md (add Probator to the proposer list for the CORRECTIO close lesson only; correct the "scrutinize do not author" blanket — Tribunus/Curator still don't author) and docs/skills/bug-pipeline.md (sink is now the warehouse — close entry is a lesson-node proposal via warehouse-ingest.md). Then fill the RUN_DOC's "## Changes Made" (replace the _(pending execution)_ sentinel). These two files ONLY — do not touch probator.md/curator.md/tribunus.md or any other file. Do not commit.
