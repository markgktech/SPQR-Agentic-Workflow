You are an execution agent for SPQR upgrade run v1.5, Group 11 — the `list-pending` warehouse verb (the Senate-wake's backing). This is a CODE build with mandatory tests (Starter-A discipline: plan-first → surface contradictions → owner approval → execute).

PRE-FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - warehouse_robot/write_gate.py   (check_antechamber, _iter_sidecars, sidecar fields, STATE_* constants)
  - warehouse_robot/cli.py          (cmd_check + subparser pattern — mirror it)
  - warehouse_robot/docs/WRITE_PROTOCOL.md

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/11-list-pending-verb-build.md

Read the Brief there. Verify the dependency gate (re-run the suite, do not trust the token). Build the read-only `list-pending` verb (write_gate.py function + cli.py subcommand) + tests against a disposable instance + the WRITE_PROTOCOL.md line. Fill "## Changes Made" with the verbatim test receipt (Ran N tests … OK, ≥5×, Python+SQLite versions). Honour the Scope fence (do NOT fix the proposal-key race — flag it; do NOT touch any doc beyond WRITE_PROTOCOL.md). Do not commit.
