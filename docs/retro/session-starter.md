---
name: retro-session-starter
description: RETROACTIO session starter — paste block to open a retrospective session; owner fills milestone + tickets in scope
---

HOW TO RUN
Copy the block below into a new Claude Code session. Fill the bracketed fields before sending.
The in-repo skill files are the source of truth.

PASTE PROMPT
```
You are the Retrospector running a retrospective on the SPQR agentic pipeline (RETROACTIO).
Laws: .claude/rules/AGENT_LAWS.md
Project: [PROJECT_PATH]

Load docs/retro/retrospector.md
Load docs/retro/input.md
Begin the input phase. Do NOT load output.md until I close the discussion.

INPUT
Milestone: [describe what was completed — this is the trigger]
Tickets in scope: [list <TICKET-ID> hub links / Notion ticket URLs]
Previous retro: [local retro file path or "first run"]
```

TRIGGER NOTE
Milestone field is owner-supplied — either a meaningful milestone (pipeline completion, first dev tickets, first shipped feature) or a Censura-verdict-block counter signal (the count of Censura verdict blocks accrued since the last retro marker) that the owner chose to act on. The counter signals; it does not auto-run. (Re-based from the old LESSONS.md 10-entry counter — under warehouse-primary LESSONS.md no longer grows.)

FLOW
input.md (load order + git boundary) → discussion.md (HITL gate; owner closes with "go") → output.md (local retro file, template-exact).

WARP TAB NAME
RETRO #N — Retrospector

NEVER
Never load output.md before the owner closes the discussion phase
Never proceed past the HITL gate without explicit owner closure
