You are an execution agent for SPQR upgrade run v1.5, Group 13 (SAW-42 — flat-file structure residue excision).

PRE-FLIGHT (load in order):
  - docs/upgrade/execution.md
  - docs/spqr_self/poc/SAW-42 Remove Flat-File Structure Residue — PoC.md   (SOURCE OF TRUTH — read fully first)
  - docs/skills/warehouse-ingest.md
  - docs/agents/quaestor.md   (mirror its WAREHOUSE QUERY POLICY phrasing)

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/13-flat-file-residue-excision.md

Read the Brief there, do the work, then fill its "## Changes Made" section
(replace the _(pending execution)_ sentinel). Do not touch MAIN or sibling
sub-docs. Do not commit.

CRITICAL: EXCISION MODE = FULL (PoC D1). Remove flat-knowledge references entirely —
neither primary nor secondary. Do NOT reproduce the SAW-42 ticket's "retained secondary
reference" wording; it is superseded by PoC D1. Derive every edit from the PoC, not the
ticket diffs. References only — touch no physical flat files. Leave the deliberately-correct
"historical / pre-cutover, read-only" LESSONS.md mentions untouched (see Brief SCOPE BOUNDARY).
Run the POST-CONDITION grep self-check and report it in Changes Made.
