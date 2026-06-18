---
name: censura-input
description: Senate Censura pre-flight — context isolation, load order, and deviation pre-check before post-execution review
---

CONTEXT ISOLATION
New session mandatory — do not recall Consilium discussion from session memory.
The on-disk `<TICKET-ID>_handover.md` IS the external record; load the Consilium block from there (Law 3).

LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text) + `<TICKET-ID>_handover.md` (all prior blocks, including the Consilium handoff)
4. Executor output: local `<TICKET-ID>_output.md` (Praetor for OPUS, Quaestor spike for EXPLORACIO; plus any `_output_revN.md`)
5. doc-maintenance.md — collect all ⚠️ flags; validate format before discussion
6. ticket-slicing.md (EXPLORACIO only — load if proposals table present)
7. Relevant On-Demand Docs (same set as Consilium)
8. censura-discussion.md

PRE-CHECK (before discussion starts)
Load Consilium expected_outputs from the handover block.
Compare against executor output — flag significant unwarranted deviation as opening finding in discussion.
Justified deviation: NOTE. Unjustified deviation: FAIL.
If executor output is missing: halt and request from owner.
Ticket proposals (EXPLORACIO only): validate each against ticket-slicing.md SLICING CRITERIA; load ticket-slicing.md before this check; if "No tickets proposed — spike is informational" → accept, ticketing phase does not start

NEVER
Never import Consilium findings from session memory — load from the on-disk handover file only (Law 3)
Never start before LOAD ORDER is complete
Never assume executor output is present — confirm explicitly before proceeding
Never treat a handover block's existence as proof of correctness — read the actual content
