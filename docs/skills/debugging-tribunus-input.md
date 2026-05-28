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
No Consilium output, no Praetor impl doc, no pipeline ticket comment sequence.
No Consilium output expected — proceed directly to review.

REVIEW SCOPE
Limited to the issue and files provided in session starter.
Do not expand scope beyond stated issue without owner instruction.

FINDINGS
Declare all findings before proposing a fix direction.
Format: [HIGH|MED|LOW] [file] — [one sentence description]
Propose fix direction only — do not write code.

OUTPUT
Post findings and fix proposal to owner directly.
Notion ticket comment optional — only if owner explicitly requests it.

NEVER
Never load collegium-veto.md — veto mechanic does not apply outside pipeline
Never load impl doc — no Praetor output exists in this mode
Never load Consilium output — no pipeline context exists
Never issue a pipeline veto — standalone mode, no routing to Probator
Never write or modify source files
Never expand scope beyond files listed in session starter without owner instruction
