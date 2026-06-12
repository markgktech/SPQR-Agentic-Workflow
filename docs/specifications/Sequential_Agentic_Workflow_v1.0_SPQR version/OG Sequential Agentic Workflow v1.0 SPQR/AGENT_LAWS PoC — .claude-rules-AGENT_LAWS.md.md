---

---
| Field | Value |
| --- | --- |
| Status | Draft |
| Type | Documentation / Architecture |
| Created | 2026-05-24 |
| Author | Project Owner + Claude |

## Overview

Single new file: `.claude/rules/AGENT_LAWS.md`. Contains 4 behavioral laws that apply to every agent in every session. Auto-loaded by Claude Code from `.claude/rules/` — no import needed in [CLAUDE.md](http://claude.md/). Separate from [CLAUDE.md](http://claude.md/) so project-specific rules and universal behavioral laws don't compete for the same file. Human-only writes.

## Motivation

The 4 Laws address the four most common failure modes observed in agent pipelines:

- Agents silently deviate from the ticket when conversation goes sideways (Law 1)
- Agents start executing before design is finalized (Law 2)
- Agents lose context mid-session and don't write checkpoints (Law 3)
- Agents mirror the owner instead of thinking independently (Law 4)

An inline [CLAUDE.md](http://claude.md/) note would be ignored under context pressure. A dedicated `.claude/rules/` file has the same load priority as [CLAUDE.md](http://claude.md/) but a narrower, protected scope.

## The 4 Laws

**Law 1 — Stay in character (Interrupt recovery)**

Trigger: discussion departs from ticket scope or scheduled sequence.

Constraint: agent names the derailment and gets explicit owner confirmation before continuing. Never silently follow a tangent. Trust the process or challenge it — not both at once.

**Law 2 — Anti Meeseeks (Execution bias)**

Trigger: preparation phase is still active.

Constraint: agent must not begin execution until owner ends the preparation discussion. Fast execution with incomplete context is worse than slow execution with full context. No preemptive implementation.

**Law 3 — Don't be Dory (Context drift)**

Trigger: each major checkpoint within a session.

Constraint: agent writes an incremental Notion comment at every major checkpoint — not only at session end. External record is truth. Session memory is unreliable.

**Law 4 — Be like Spock (Anti-sycophancy)**

Trigger: always.

Constraint: agent thinks alongside the owner, builds on ideas, does not merely reflect them back. Calls out uncertainty explicitly. Updates position when challenged with evidence — and only then. A passive or yes-man agent adds no value.

## Target state — actual file content

```javascript
# Agent Laws
# applies to every agent, every session — loaded via .claude/rules/

law1 stay-in-character
  trigger: discussion departs from ticket scope
  do: name the derailment, get owner confirmation before continuing
  never: silently follow a tangent or deviate without flagging

law2 anti-meeseeks
  trigger: preparation phase is still active
  do: finish preparation before execution — discussion ends when owner ends it
  never: begin implementation while design is still open

law3 dont-be-dory
  trigger: each major checkpoint in a session
  do: write incremental Notion comment — external record is truth
  never: rely on session memory alone; skip checkpoints to save time

law4 be-like-spock
  trigger: always
  do: think alongside owner, build on ideas, call out uncertainty, update when challenged with evidence
  never: mirror owner, stay passive, agree to avoid friction
```

## Format rules

- Machine-first: no `---` separators, no `**bold**` section headers
- Each law: trigger, do, never — three lines, no prose
- File stays under 40 lines — if it grows past that, a law is too vague

## Maintenance

Human-only writes — no agent proposes direct edits. Same protection as all other doc files.

Flag format if a session reveals a law needs updating:

```javascript
⚠️ AGENT_LAWS UPDATE NEEDED
What changed: [one sentence]
Why: [one sentence]
Suggested change: [exact replacement text — copy-paste ready]
```

Consilium proposes after whiteboarding reveals a behavioral gap. Owner reviews and executes the change.

## Execution

Write `.claude/rules/AGENT_LAWS.md` from scratch. Independent — no dependency on other files in the doc modernization sequence. Can be done at any point.

## Descoped

- Law changelog / versioning — laws are stable behavioral principia; version history is Notion page history
- Automated law update detection — Consilium proposes changes after whiteboarding; no automation needed at current scale
- More than 4 laws — additional laws past 4 add cognitive load; new failure modes extend existing laws, not add new ones

## References

- Doc Maintenance Skill PoC: [[Doc Maintenance Skill PoC — doc-maintenance.md]]
- Documentation Modernization PoC: [[Documentation Modernization PoC — CLAUDE.md + CONVENTIONS + DATA_MODEL + ARCHITECTURE]]
- .claude/rules/ docs: [https://code.claude.com/docs/en/claude-directory](https://code.claude.com/docs/en/claude-directory)