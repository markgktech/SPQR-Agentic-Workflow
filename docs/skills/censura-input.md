---
name: censura-input
description: Senate Censura pre-flight — context isolation, load order, and deviation pre-check before post-execution review
---

CONTEXT ISOLATION
New session mandatory — do not recall Consilium discussion from session memory.
The Consilium Notion comment IS the external record; load it from there (Law 3).

LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text + all Notion comments, including Consilium handoff comment)
4. Executor output: Praetor Renuntiatio (OPUS) or Quaestor spike document (EXPLORACIO)
5. doc-maintenance.md — collect all ⚠️ flags; validate format before discussion
6. Relevant On-Demand Docs (same set as Consilium)
7. censura-discussion.md

PRE-CHECK (before discussion starts)
Load Consilium expected_outputs from handoff comment.
Compare against executor output — flag significant unwarranted deviation as opening finding in discussion.
Justified deviation: NOTE. Unjustified deviation: FAIL.
If executor output is missing: halt and request from owner.

NEVER
Never import Consilium findings from session memory — load from Notion comment only (Law 3)
Never start before LOAD ORDER is complete
Never assume executor output is present — confirm explicitly before proceeding
Never treat a Notion comment's existence as proof of correctness — read the actual content
