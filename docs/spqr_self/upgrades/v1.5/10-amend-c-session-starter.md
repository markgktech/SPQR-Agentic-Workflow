You are an execution agent for SPQR upgrade run v1.5, Group 10-amend-c (SAW-31 — runnable-CLI examples + terminology glossary; the FINAL pass).

PRE-FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - warehouse_robot/cli.py                  (the REAL required flags per verb — verify, do not guess)
  - warehouse_robot/docs/QUERY_PROTOCOL.md  (§2: terminal verdict closes the SESSION; non-terminal keeps it open)

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/10-amend-c-runnable-cli.md

Read the Brief there, apply the two-file fix: warehouse-usage.md (make the §2 semantic-audit CLI examples copy-paste runnable per cli.py — required flags on verdict/traverse; fix the terminal-vs-non-terminal verdict guidance per QUERY_PROTOCOL §2 — plus the one glossary line defining owner-operated = owner-authorized) and ticket-comment.md (clarify the receipt arrow is the decisive state+key from the CLI's JSON). Then fill "## Changes Made". Honour the Scope fence — do NOT chase "owner-operated" elsewhere, do NOT touch the PoC. Do not commit.
