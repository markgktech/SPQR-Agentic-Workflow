---

---
## Two roles, two session types

Every upgrade runs across two distinct agent types. Mixing them causes context pollution and unclear ownership.

**Master Agent**

Persistent session. Orchestrates the full upgrade from start to wrap-up. Holds context across all phases. Writes execution briefs. Reviews group outputs. Calls roundtable when needed. Executes Notion MCP operations (page creation, updates). Never modifies repo files directly.

**Execution Agent**

Stateless session. Receives one written brief. Executes file changes for one group. Fills in the Changes Made section in Notion. Posts output summary to owner. Session closes after the group is done.

---

## Responsibilities by role

| Responsibility | Master | Execution |
| --- | --- | --- |
| Load DOC tickets | yes | no |
| Run roundtable | yes | no |
| Write execution brief | yes | no |
| Modify repo files | no | yes |
| Notion MCP operations | yes | brief scope only |
| Fill Changes Made in Notion | no | yes |
| Confirm output + call roundtable | yes | no |
| Owner confirmation gate | yes | no |
| Update main Notion page | yes | no |
| Create open item tickets | yes | no |

---

## What the execution agent receives

Every execution session starts from a written brief in typed format:

```javascript
GROUP: [name]
ORDER: N/N
REPO: Foodoire | SPQR | Both
NOTION_REF: [URL of this group's sub-page]
RATIONALE: [one line — why this is one group]
FILL_CHANGES_MADE: yes
PRE_FLIGHT:
  [skill file or Notion URL the execution agent must load]
FILES:
  [filename]: [what changes — one line]
```

The execution agent loads this brief, executes, and posts a summary. It does not plan, does not expand its own scope, and does not touch files outside its brief.

---

## Out-of-scope discovery

If the execution agent finds a problem not covered by its brief (e.g. a hardcoded value in an unrelated file), it reports this in the output summary — it does not handle it unilaterally. The master decides whether to add a new group or open a ticket.

---

## Execution agent blockers

If the execution agent cannot proceed (e.g. unresolvable API error, missing context), it posts a blocker comment on the ticket and stops. Owner decides next step. It does not retry indefinitely or make assumptions to work around the blocker.

---

## Session handoff

The master writes the complete session starter for each execution group. The owner copies it and opens a new session. The master does not hand off verbally or summarise — the written brief IS the handoff. If the brief is incomplete, the execution session will be incomplete.

---

## What the master agent never does

- Modify repo files in the orchestration session
- Write to [CLAUDE.md](http://claude.md/) directly (propose text only; owner applies)
- Run git commit or git push (owner only)
- Move to the next group without owner confirmation