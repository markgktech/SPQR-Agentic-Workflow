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
git worktree add ../TICKET-XXX-branch TICKET-XXX-branch

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
