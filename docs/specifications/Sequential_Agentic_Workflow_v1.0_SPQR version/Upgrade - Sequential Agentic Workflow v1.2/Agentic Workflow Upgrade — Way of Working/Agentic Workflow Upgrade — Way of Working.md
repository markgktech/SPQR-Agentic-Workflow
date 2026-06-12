---

---
## What this is

This document defines the Way of Working for upgrading the SPQR agentic workflow — from identified gaps (DOC tickets) to a versioned, documented upgrade applied consistently across all files.

Use this when: a Censura retrospective surfaces friction, a spike reveals a workflow gap, or a new capability is needed across the pipeline.

**Owner-provided artefacts** (diagrams, notes, prior session outputs) are context, not specifications. The master interprets them and exercises judgment — it does not follow them literally.

**Owner communication is calibrated, not formalised.** A short confirmation is a valid gate signal. The master reads intent; it does not demand written acknowledgment when the owner communicates concisely.

**All four AGENT_LAWS apply.** The master agent operates under the same laws as all other SPQR agents. The session starter includes a reference to `.claude/rules/AGENT_LAWS.md` — load and apply before starting.

**The master agent brings independent judgment.** If execution output contains a surprise or gap, the master calls a roundtable — no owner approval needed for that call. Owner checkpoints are explicit gates (see below); everything between them is the master's call.

---

## Owner Checkpoints

Three explicit gates where the master agent waits for owner confirmation before proceeding:

1. **After roundtable closes** — owner confirms item list and decisions before planning starts
2. **After each group output** — owner reviews execution summary before next group launches
3. **Before wrap-up** — owner confirms all groups complete before main Notion page is updated

---

## The Process

Six phases. Master agent orchestrates; execution agents implement.

**Phase 1 — Context Loading**

Load all DOC tickets in scope. Load memory (decisions, file maps, versioning). Confirm scope with owner before proceeding.

**Phase 2 — Roundtable**

[Master Persona 1] and [Master Persona 2] review all tickets. Build flat item list. Identify gaps, conflicts, and open questions. Owner closes discussion explicitly before Phase 3 starts.

**Phase 3 — Decision Making**

Go through items one by one. Make architectural decisions. Save to memory in real time. Unresolvable items → flagged as new tickets, do not block progress.

**Phase 4 — Planning**

Group items into execution groups. Set order (project-specific repo first, generic sync after). Create Notion upgrade doc (main page + sub-pages per group). Write execution brief per group in typed format:

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

Dependency rule: if two groups touch the same file, merge them into one session. Never split file ownership across groups.

**Phase 5 — Execution**

Launch a separate agent session per group using the written brief. Agent executes file changes and fills in the Changes Made section. Master reviews output summary. Owner confirms before next group launches. Roundtable if gaps or surprises found — master calls this independently.

SPQR sync groups: mandatory grep after sync for sensitive data (Notion IDs, real names, project-specific content).

Stalled items: if an item cannot be completed within its group, mark as stalled → open item → new ticket. Does not block the group.

**Phase 6 — Wrap-up**

Master updates main Notion page. Open items become new DOC tickets (owner assigns prefix + number). Memory saved and marked complete. Owner confirms wrap-up complete.

---

## Context Window

Multiple sessions required for any non-trivial upgrade:

- Save memory before compacting
- Use /clear between groups when context allows
- Request summary output from execution agents before context limit hits
- Calculate context headroom before starting a new group

---

## Sub-pages

- Master vs Execution Agent
- Roundtable — When, Who, Rules
- Decision Making & Memory
- Planning: Groups & Briefs
- Execution Order
- Context Window Management
- Wrap-up Checklist

[[Master vs Execution Agent]]

[[Roundtable — When, Who, Rules]]

[[Decision Making & Memory]]

[[Planning Groups & Briefs]]

[[Execution Order]]

[[Context Window Management]]

[[Wrap-up Checklist]]

[[Upgrade Agent Architecture — Redesign Proposal]]