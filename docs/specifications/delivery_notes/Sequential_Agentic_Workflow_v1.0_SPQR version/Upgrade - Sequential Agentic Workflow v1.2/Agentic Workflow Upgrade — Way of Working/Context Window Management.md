---

---
## Why this matters

A non-trivial upgrade spans multiple sessions. Context window exhaustion mid-session loses work and breaks continuity. Managing it proactively is part of the process, not an afterthought.

---

## Master session rules

- Save memory at natural stopping points — after each roundtable, after each decision cluster, after each group closes. Frequency is a judgment call, not a schedule. The goal: if the session ends unexpectedly, no work is re-derivable from scratch
- Before compacting: request a summary from the current state; verify it captures all open decisions
- Use /clear between groups when context allows and there is no carry-over state needed
- Monitor context usage before starting a new group — estimate the group's size (number of files × average change scope) and compare against free headroom; a percentage alone is not sufficient
- The Notion upgrade doc is the external record — the master can be reconstructed from it if context is lost

---

## Execution session rules

- Each execution session starts fresh from the brief — no session memory from previous groups
- If a group is large enough to risk context exhaustion mid-execution, split it before launching (see Planning: Groups & Briefs)
- Before hitting context limit: post a partial Changes Made comment and a status note so the session can be resumed

---

## Compact protocol

When compacting the master session:

1. Save any unsaved decisions to memory first
2. Ensure the Notion upgrade doc reflects current state
3. Run `/compact [what we are doing and what remains]` — the compact args note is the continuity anchor for the next session; do not compact without it
4. The next session loads memory + Notion doc to reconstruct context — it does not re-derive what is already documented

---

## The Notion doc as continuity anchor

The upgrade Notion page (main + sub-pages) is the external record for the entire upgrade. If a session is lost, a new master session can resume from:

- Memory files (decisions, strategy)
- Notion upgrade doc (which groups are done, what changed, what is open)

This is Law 3 (Don’t be Dory) applied to the upgrade process.