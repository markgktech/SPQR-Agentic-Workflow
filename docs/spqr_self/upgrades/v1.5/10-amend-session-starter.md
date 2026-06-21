You are an execution agent for SPQR upgrade run v1.5, Group 10-amend (SAW-31 final consistency amendment; Codex findings #1/#3/#4/#6).

PRE-FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md
  - warehouse_robot/write_gate.py            (propose returns pending-senate, not validated)
  - warehouse_robot/docs/QUERY_PROTOCOL.md   (§2 bracket; traverse = one edge_type per call)

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/10-amend-saw31-final-consistency.md

Read the Brief there, apply the 6-file accuracy/wording deltas (no behaviour change — reconcile prose to final D2/D2c): ticket-comment.md (receipt example → pending-senate), warehouse-usage.md (session-start audit = agent-on-owner-HITL; semantic-audit how-to → bracket + real traverse args), praetor.md + quaestor.md + warehouse-ingest.md + censura-output.md ("OWNER executes ingest" → "the Senate runs resolve on owner HITL"). Then fill the RUN_DOC's "## Changes Made". Honour the Scope fence (do NOT touch the retro LESSONS.md framing or the ticket-comment mode enum). Do not commit.
