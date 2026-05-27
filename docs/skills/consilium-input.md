---
name: consilium-input
description: Senate Consilium pre-flight — load order, skip rule, and entry constraints before design deliberation starts
---

LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text + all Notion comments)
4. Relevant On-Demand Docs (DATA_MODEL.md, CONVENTIONS.md, ARCHITECTURE.md as needed)
5. consilium-discussion.md

SKIP RULE (OPUS only)
Consilium skippable if a completed spike doc exists and covers the ticket's unknowns.
If asked to validate: load spike doc, confirm it addresses all ticket unknowns, then proceed or run full Consilium.
Never skip based on ticket size alone — small tickets can touch invariants.

NEVER
Never start discussion before all LOAD ORDER items are read
Never carry state from a prior session — start cold (Law 3)
Never proceed if any LOAD ORDER item is missing — halt and request from owner
Never skip in EXPLORACIO — Consilium always runs on spike tickets
