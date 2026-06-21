---
name: consilium-input
description: Senate Consilium pre-flight — load order, skip rule, and entry constraints before design deliberation starts
---

LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text) + `<TICKET-ID>_handover.md` if it already exists (usually not — Consilium is first in the pipeline)
4. Warehouse query for prior decisions/constraints in scope — a `find`/`open-scope` round per the Senate WAREHOUSE QUERY POLICY (senate.md, `--archetype deliberate`); an ABSENT verdict is valid evidence, not a blocker.
5. consilium-discussion.md

SKIP RULE (OPUS only)
Consilium skippable if a completed spike doc exists and covers the ticket's unknowns.
If asked to validate: load spike doc, confirm it addresses all ticket unknowns, then proceed or run full Consilium.
Never skip based on ticket size alone — small tickets can touch invariants.

DA DESIGNATION
If DA role is designated in input context: note the DA persona name.
DA speaks first per topic in discussion (see consilium-discussion.md).
If no DA designation in input context: normal turn order — no action needed.

NEVER
Never start discussion before all LOAD ORDER items are read
Never carry state from a prior session — start cold (Law 3)
Never proceed if any LOAD ORDER item is missing — halt and request from owner. EXCEPTION: a completed warehouse query that returns ABSENT is not a missing item — an absent (retired) flat doc is valid evidence, not a blocker.
Never skip in EXPLORACIO — Consilium always runs on spike tickets
