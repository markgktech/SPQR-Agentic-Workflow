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

CORRECTIO — BUG FLOW (owner-launched, handover-driven)
The owner moves the Notion bug ticket through stages and launches each hop as a fresh session; context flows via the local handover (D20, D23). Default 2 hops: Praetor (investigate → HITL cause-note gate → fix) → Probator (verify + close). Conditional inserts: [investigator →] before Praetor, [→ Tribunus-review] / [→ Curator] after, [→ Censura iff decision].

PASTE PROMPT — Praetor (bug executor)
Load docs/agents/praetor.md
Load docs/skills/bug-pipeline.md
MODE: CORRECTIO (bug) — investigate-first, STOP at the HITL cause-note gate before any code
Ticket: [TICKET_URL]
Project is located at: [PROJECT_PATH]

PASTE PROMPT — Probator (verify + close)
Load docs/agents/probator.md
Load docs/skills/bug-pipeline.md
MODE: CORRECTIO (bug) — verify repro pre/post, tests, conditional regression test, write close + routine knowledge entry
Ticket: [TICKET_URL]
Project is located at: [PROJECT_PATH]

Escalation hops (conditional): investigator → use the DEBUGGING TRIBUNUS — STANDALONE starter (CORRECTIO investigator mode); Tribunus-review / Curator → their standard OPUS starters on the same fix/ branch.

WARP TAB NAME
<TICKET-ID> — [Agent] (CORRECTIO)

PRAETOR PRE-STEP (CORRECTIO)
Repo on main and clean. Praetor opens the bug branch (fix/<TICKET-ID>-slug) ONLY after the HITL cause-note gate clears — not before. If a branch already exists for the ticket, Praetor stops and asks owner.

---

PERSONAS
Name 1: [Name 1]
Name 2: [Name 2]
Name 3: [Name 3]
Name 4: [Name 4]

Load this section when invoking a Senate or Quaestor agent.
If no persona-carrying agent is invoked: skip.
