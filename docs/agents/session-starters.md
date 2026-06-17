SESSION STARTER — SPQR v1.1
One template. Replace [AGENT] and [TICKET_URL] each time.

PASTE PROMPT
Load docs/agents/[AGENT].md
Begin input phase.
Ticket: [TICKET_URL]
Project is located at: [PROJECT_PATH]

AGENT NAMES
senate / quaestor / praetor / tribunus / probator / curator

WARP TAB NAME
TICKET-XXX — [Agent]

PRAETOR PRE-STEP (before pasting prompt)
Ensure the repo is on main and clean. Praetor auto-opens the ticket branch (feature/DEV-XXX-slug) before coding — mechanics in docs/skills/git-workflow.md. If a branch already exists for the ticket, Praetor stops and asks owner.

---

DEBUGGING TRIBUNUS — STANDALONE
Load docs/agents/tribunus.md
Load docs/skills/debugging-tribunus-input.md
MODE: STANDALONE DEBUGGING
Issue: [describe the bug or test failure]
Relevant files: [list suspect or changed files]
Project is located at: [PROJECT_PATH]

WARP TAB NAME
TICKET-XXX — Tribunus Debug

---

PERSONAS
Name 1: [Name 1]
Name 2: [Name 2]
Name 3: [Name 3]
Name 4: [Name 4]

Load this section when invoking a Senate or Quaestor agent.
If no persona-carrying agent is invoked: skip.
