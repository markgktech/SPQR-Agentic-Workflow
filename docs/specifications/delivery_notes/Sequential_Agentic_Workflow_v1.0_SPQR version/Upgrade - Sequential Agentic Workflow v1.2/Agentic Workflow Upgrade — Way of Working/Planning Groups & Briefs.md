---

---
## What a group is

A group is a set of items that can be executed in a single agent session without creating file ownership conflicts. One group = one execution session.

---

## Grouping rules

- Items that touch the same file belong in the same group
- Items with a dependency (B requires A to be done first) must be in the same group, or A's group must be ordered before B's
- One group should be completable in a single session without hitting context limits — if too large, split only along file ownership boundaries, never by effort or time
- Generic repo sync is always after all project-specific groups

**Dependency rule:** if two groups touch the same file, merge them into one session. Never split file ownership across groups.

---

## Execution order

Order is dependency-driven, not category-driven. The general pattern that follows from dependencies:

1. Project-specific repo groups first (real content, testable context)
2. Generic repo sync group after (depends on project-specific being done)
3. Documentation-only or cross-cutting groups last (when they have no upstream dependency)

If a group has no dependency on anything before it, its position is flexible — place it where it causes least disruption.

---

## Notion upgrade doc structure

Before execution starts, the master creates:

- A main Notion page for the upgrade (title, overview, implementation groups)
- One sub-page per execution group (brief + Changes Made section)

The execution agent fills in the Changes Made section. The master fills in everything else.

Creating the sub-page structure is part of planning, not documentation of a completed plan. The act of writing group titles and scopes surfaces dependencies and ordering issues — if you can’t name a group cleanly, the grouping is wrong.

---

## Brief format

Every brief uses typed format. Pre-flight references tell the execution agent what to load before starting — without this, the agent has to guess.

```javascript
GROUP: [name]
ORDER: N/N
REPO: Foodoire | SPQR | Both
NOTION_REF: [URL of this group’s sub-page]
RATIONALE: [one line — why this is one group]
FILL_CHANGES_MADE: yes
PRE_FLIGHT:
  [skill file or Notion URL the execution agent must load]
  [skill file or Notion URL the execution agent must load]
FILES:
  [filename]: [what changes — one line]
  [filename]: [what changes — one line]
```

**Brief writing rule:** the brief must be complete enough that the execution agent can start without asking clarifying questions. If writing the brief surfaces ambiguity, resolve it before handing off — this is the system working correctly, not a failure. Ambiguity discovered during planning is far cheaper than ambiguity discovered mid-execution.

---

## Brief length

A brief is too large if it requires more than 7 FILES entries or a RATIONALE longer than one line. If either threshold is hit, split along file ownership boundaries or resolve the ambiguity first.