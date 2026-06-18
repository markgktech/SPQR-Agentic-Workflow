---
name: debugging-tribunus-input
description: Tribunus standalone debugging pre-flight — load order and constraints for non-pipeline debugging sessions
---

LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Issue description (from session starter — bug description, failing test, suspect files)
4. Source files listed as relevant in session starter
5. tribunus-output.md

MODE
STANDALONE DEBUGGING — not part of an active OPUS pipeline.
No Consilium output, no Praetor output doc, no pipeline handover sequence.
No Consilium output expected — proceed directly to review.

CORRECTIO ESCALATION INVESTIGATOR (D11, D12 — resolves the former "BUG roles owner-deferred / D15" note)
This standalone-debug mode IS the CORRECTIO escalation investigator: invoked BEFORE Praetor when entry=wild AND the cause is not localizable. Orchestration: docs/skills/bug-pipeline.md.
Produce a structured fix-spec for Praetor: repro · root-cause file:symbol · proposed change · blast radius.
Mechanical exit: if the root cause is NOT localizable to a file/subsystem → report that to the owner, who files a normal EXPLORACIO spike ticket (genuine research). There is no in-CORRECTIO quaestor mode — do not assume one.

REVIEW SCOPE
Limited to the issue and files provided in session starter.
Do not expand scope beyond stated issue without owner instruction.

FINDINGS
Declare all findings before proposing a fix direction.
Format: [HIGH|MED|LOW] [file] — [one sentence description]
Propose fix direction only — do not write code.

OUTPUT
Post findings and fix proposal to owner directly.
Local handover block optional in pure standalone use — only if owner explicitly requests it.
In CORRECTIO investigator mode: record the fix-spec in `<TICKET-ID>_handover.md` so the owner-launched Praetor session can pick it up (handover-driven, D23).

NEVER
Never load collegium-veto.md — veto mechanic does not apply outside pipeline
Never load impl doc — no Praetor output exists in this mode
Never load Consilium output — no pipeline context exists
Never issue a pipeline veto — standalone mode, no routing to Probator
Never write or modify source files
Never expand scope beyond files listed in session starter without owner instruction
