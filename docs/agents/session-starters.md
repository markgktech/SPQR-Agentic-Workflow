SESSION STARTER — SPQR v1.1
One template. Replace [AGENT] and [TICKET_URL] each time.

PASTE PROMPT
Load docs/agents/[AGENT].md
Begin input phase.
Ticket: [TICKET_URL]
Project is located at: [PROJECT_PATH]

AGENT NAMES
senate / quaestor / praetor / tribunus / probator / curator

TICKET ID
`<TICKET-ID>` resolves to the consuming project's ticket id (Foodoire → FDP-N; `DEV-XXX` is a legacy alias). The executor agent (Praetor for DEV, Quaestor for SPIKE/DOC) creates the ticket hub + handover file in the work_documents/ vault at session start if missing.

WARP TAB NAME
<TICKET-ID> — [Agent]

PRAETOR PRE-STEP (before pasting prompt)
Ensure the repo is on main and clean. Praetor auto-opens the ticket branch (feature/<TICKET-ID>-slug) before coding — mechanics in docs/skills/git-workflow.md. If a branch already exists for the ticket, Praetor stops and asks owner.

---

DEBUGGING TRIBUNUS — STANDALONE
Load docs/agents/tribunus.md
Load docs/skills/debugging-tribunus-input.md
MODE: STANDALONE DEBUGGING
Issue: [describe the bug or test failure]
Relevant files: [list suspect or changed files]
Project is located at: [PROJECT_PATH]

WARP TAB NAME
<TICKET-ID> — Tribunus Debug

---

PERSONAS
Name 1: [Name 1]
Name 2: [Name 2]
Name 3: [Name 3]
Name 4: [Name 4]

Load this section when invoking a Senate or Quaestor agent.
If no persona-carrying agent is invoked: skip.
