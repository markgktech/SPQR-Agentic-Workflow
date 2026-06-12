---

---
| Field | Value |
| --- | --- |
| Status | Draft |
| Type | Documentation / Architecture |
| Created | 2026-05-24 |
| Author | Project Owner + Claude |

## Overview

The `doc-maintenance` skill defines the rules governing how all Foodoire documentation files may be read, flagged, and updated within the Collegium pipeline. Covers six documentation areas: [CLAUDE.md](http://claude.md/) (always loaded every session), `.claude/rules/AGENT_LAWS.md` (always auto-loaded via `.claude/rules/`), [CONVENTIONS.md](http://conventions.md/), DATA_[MODEL.md](http://model.md/), [ARCHITECTURE.md](http://architecture.md/) (all on-demand), and docs/decisions/ (individual ADR files + [INDEX.md](http://index.md/)). Loaded on demand — only when a ticket explicitly touches documentation. No agent writes directly to any of these files. Changes are flagged mid-pipeline and executed by the owner after ticket close.

## Motivation

Without explicit protection, agents will restore decorative formatting deliberately removed, duplicate content across files, write directly to doc files before code is stable, and produce vague flags without actionable text. An inline header comment does not prevent this — it is advisory and ignored under context pressure. A skill file is architectural: it loads on demand, carries CI/CD-level review rigor, and costs zero tokens when inactive.

**Industry backing:**

- ETH Zürich 2026 (Gloaguen et al.): LLM-generated context files cause ~3% task success drop and 20%+ inference cost increase vs. human-written files. Agents must never write instruction files directly.
- Anthropic Skill Authoring Best Practices: treat a [SKILL.md](http://skill.md/) change like a CI/CD pipeline change.
- HumanLayer: "Bloated [CLAUDE.md](http://claude.md/) files cause Claude to ignore your actual instructions."
- Agent Skills progressive disclosure: skill body loads only when needed — zero token cost when inactive.

## Rules

### File scope

| File | Always loaded | Canonical scope | Size target |
| --- | --- | --- | --- |
| [CLAUDE.md](http://claude.md/) | Yes — every session | What every agent must know in every session: stack, critical rules, coding principia, phase boundaries, navigation, agent workflow, doc refs. No patterns, no code examples, no entity detail. | ~80 lines, hard ceiling 200 |
| [CONVENTIONS.md](http://conventions.md/) | No — on demand | All coding patterns: naming, folder structure, MV/MVVM, services, positioning, JSON, OSLog, SwiftLint, error patterns. Canonical — no duplication allowed. Grows with project. | No ceiling — canonical |
| DATA_[MODEL.md](http://model.md/) | No — on demand | Schema reference only: entity tree, @Model definitions, JSON structs, constants, image storage, schema versioning, business invariants. Code blocks stay — Swift code IS the documentation. | No ceiling — grows per phase |
| [ARCHITECTURE.md](http://architecture.md/) | No — on demand | System topology map + architectural invariants not covered elsewhere. Consilium loads before whiteboarding. ~15 lines of unique content — everything else is duplication and must be removed. | ~15 lines, hard ceiling 30 |
| docs/decisions/ | No — on demand | Individual ADR files (A1–Ax), one architectural decision per file, 10–20 lines each. [INDEX.md](http://index.md/) is the always-scanned entry point (~25 lines). Agents load individual files by ID when relevant to the ticket. | [INDEX.md](http://index.md/) ~25 lines; ADR files 10–20 lines each |
| .claude/rules/AGENT_[LAWS.md](http://laws.md/) | Yes — auto-loaded | 4 Laws of Agentic Workflow: behavioral constraints applying to every agent in every session. No project-specific content. Placed in `.claude/rules/` — Claude Code auto-loads every .md file in that directory. Human-only writes. | ~20 lines, hard ceiling 40 |

### Format rules

- No `---` decorative separators in any file
- No `**bold labels**` on section headers
- No decorative empty lines between sections
- Code blocks kept — they are not decoration, they are the content
- Pointers over copies: [CLAUDE.md](http://claude.md/) references [CONVENTIONS.md](http://conventions.md/) and DATA_[MODEL.md](http://model.md/), never duplicates their content
- Every new section added to any file must fit its canonical scope — cross-scope content goes in the correct file

### Agent behavior rules

- Agents never write directly to any of the six documentation areas
- If a doc change is needed, the agent MUST output exact, copy-paste ready text — a vague flag is invalid
- Flagging happens mid-pipeline; execution happens only after Senate Censura closes the ticket and the owner reviews the proposed text
- The flag captures the decision immediately — only the file write is deferred until code is stable within the ticket

### Mandatory flag formats

**For file updates (**[**CLAUDE.md**](http://claude.md/)**, **[**CONVENTIONS.md**](http://conventions.md/)**, DATA_**[**MODEL.md**](http://model.md/)**, **[**ARCHITECTURE.md**](http://architecture.md/)**, **`**.claude/rules/AGENT_LAWS.md**`**):**

```javascript
⚠️ [FILE] UPDATE NEEDED
What changed: [one sentence]
Why: [one sentence — the non-obvious reason]
Suggested addition: [exact text, copy-paste ready — not optional]
```

**For new ADR entries (docs/decisions/):**

```javascript
⚠️ ADR NEEDED
Title: [decision title]
Suggested file: docs/decisions/aXX-[slug].md
Suggested content: [full file content — copy-paste ready, 10–20 lines]
```

A flag without `Suggested addition:` or `Suggested content:` is invalid. Tribunus must return it as a HIGH finding.

### Execution order (owner updates after ticket closes)

```javascript
1. docs/decisions/  → new ADR file(s) + one line added to INDEX.md
2. DATA_MODEL.md    → no dependency on other files, update independently
3. ARCHITECTURE.md  → no dependency on other files, update independently
4. CONVENTIONS.md   → after DATA_MODEL (may reference schema concepts)
5. CLAUDE.md        → always last — references CONVENTIONS.md and DATA_MODEL.md
```

## Validation Against Industry Standards

| Rule | Verdict | Source |
| --- | --- | --- |
| [CLAUDE.md](http://claude.md/) ~80 lines | ✅ Strong | HumanLayer, claudelint — ceiling 200 lines; 80 is well within best practice |
| On-demand loading for 4 of 6 files | ✅ Strong | Agent Skills progressive disclosure spec — official Anthropic pattern |
| Machine-first format (no ---, no **bold**) | ✅ Indirect | "Bloated context = ignored instructions" + "use a linter, not instructions, for style" |
| Code blocks stay | ✅ | WHAT/WHY/HOW framework — HOW layer = commands and examples |
| One canonical scope per file | ✅ Strong | Three-layer model: [AGENTS.md](http://agents.md/) / [SKILL.md](http://skill.md/) / [DESIGN.md](http://design.md/) (DEV Community, Google Labs 2026) |
| Agent never writes doc files directly | ✅ Strong | ETH Zürich 2026: LLM-written context → 3% task drop + 20% cost increase |
| Flag-and-defer (write after ticket closes) | ⚠️ Nuanced | Enterprise: "don't defer coordination decisions" — but our flag captures the decision immediately. Only the file write is deferred until code is stable. The distinction must be explicit in the skill. |
| Senate Censura collects and validates flags | ✅ | Living spec pattern: coordinator validates pre-merge (Augment Code 2026) |
| Execution order respects dependencies | ✅ | Standard dependency ordering — [CLAUDE.md](http://claude.md/) last because it references the others |
| Pointer not copy | ✅ Strong | HumanLayer: "prefer pointers to copies — snippets become stale" |
| Skill file = CI/CD review rigor | ✅ Strong | Anthropic Skill Authoring Best Practices |
| Stale instructions are actively harmful | ✅ Strong | Claude Code Best Practices: "stale instructions are harmful, not neutral" |
| Human-only writes | ✅ Strong | ETH Zürich 2026 + all sources |
| Progressive disclosure (frontmatter first, body on demand) | ✅ Strong | Agent Skills official spec — Anthropic |
| Exact proposed text mandatory in flag | ✅ | Consistent with "copy-paste ready" output standard from multi-agent coordination guidance |

## Pipeline Integration

| Agent | Loads skill? | When | What it does |
| --- | --- | --- | --- |
| Consilium (Master Architect) | Yes — conditional | Before and after whiteboarding sessions involving architecture or new decisions | Loads [ARCHITECTURE.md](http://architecture.md/) for big-picture context. Primary proposer of [ARCHITECTURE.md](http://architecture.md/) changes and new ADRs — outputs ⚠️ [ARCHITECTURE.md](http://architecture.md/) UPDATE NEEDED or ⚠️ ADR NEEDED with full proposed content after session. |
| Praetor (Dev Engineer) | Yes — conditional | When ticket touches any doc file, or when writing any ⚠️ flag | Follows format and scope rules when editing; outputs exact flag text with Suggested addition/content. Proposes ⚠️ ADR NEEDED if implementation reveals an undocumented architectural decision. |
| Tribunus (Peer Reviewer) | Yes — conditional | When reviewing output that includes any ⚠️ flag | Validates flag format — returns as HIGH finding if Suggested addition or Suggested content is missing or vague. |
| Probator (QA) | No | Never | Doc changes are not testable — QA does not touch or validate doc file content. |
| Curator (DevOps) | No | Never | Checks that flags exist in ticket output — scan for ⚠️ prefix in all Notion ticket comments. Does not validate flag content; that is Tribunus’s responsibility. |
| Senate Censura | Yes — always | Every ticket close | Collects all ⚠️ flags from ticket comments, validates format, confirms owner has reviewed Suggested addition/content before closing. |

## Constraints

NEVER:

- Write directly to [CLAUDE.md](http://claude.md/), [CONVENTIONS.md](http://conventions.md/), DATA_[MODEL.md](http://model.md/), [ARCHITECTURE.md](http://architecture.md/), `.claude/rules/AGENT_LAWS.md`, or any file in docs/decisions/
- Output a flag without exact Suggested addition or Suggested content text
- Add content to a file outside its canonical scope (wrong-file placement is a bug, not a shortcut)
- Restore decorative formatting: `---`, `**Section Header**`, empty lines used for spacing
- Duplicate content that belongs in another file
- Use "something about X should be added" — this is not a valid flag
- Execute a doc update mid-pipeline — wait for ticket close and owner review (the decision is captured immediately in the flag; only the file write is deferred until the ticket is closed and code is stable within the ticket)
- Create an ADR for a trivial decision (field notes, UI micro-decisions, deferred items with no rationale)

## Recommendations

### Do now

- Write the actual `docs/skills/doc-maintenance.md` skill file from this PoC
- Add pointer to [CLAUDE.md](http://claude.md/) Skills table: `doc-maintenance | Consilium + Praetor + Tribunus + Senate Censura | docs/skills/doc-maintenance.md`
- Add to Consilium, Praetor, Tribunus, and Senate Censura session starters: load `doc-maintenance` when ticket involves documentation
- Add to Tribunus finding checklist: "flag with missing Suggested addition/content → HIGH finding"

### Defer

- Machine-first reformatting of [CONVENTIONS.md](http://conventions.md/) — iteratively, only when sections are touched by a ticket
- Dedicated housekeeping agent that executes doc flags automatically after owner approval

### Discard

- Inline header comments as the protection mechanism — the skill file supersedes this entirely

## Descoped

- Validation of flag content quality (is the proposed text correct?) — this is a Tribunus judgment call, not enforced by the skill
- Global Design Decisions Notion page cleanup — separate task, not a doc file
- ADR tooling (adr-tools CLI, etc.) — plain files are sufficient at this scale
- Retroactive ADRs for future Phase 2+ decisions — written when those phases begin

## References

- AGENT_LAWS PoC: [[AGENT_LAWS PoC — .claude-rules-AGENT_LAWS.md]]
- Documentation Modernization PoC: [[Documentation Modernization PoC — CLAUDE.md + CONVENTIONS + DATA_MODEL + ARCHITECTURE]]
- [DECISIONS.md](http://decisions.md/) Restructuring PoC: [[DECISIONS.md Restructuring PoC — docs-decisions-]]
- Collegium Pipeline PoC: [[Collegium Pipeline Design PoC]]
- Anthropic Skill Authoring Best Practices: [https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- HumanLayer — Writing a good [CLAUDE.md](http://claude.md/): [https://www.humanlayer.dev/blog/writing-a-good-claude-md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- ETH Zürich 2026 context file research (Gloaguen et al.) — cited via Claude Code Best Practices
- [AGENTS.md](http://agents.md/), [SKILL.md](http://skill.md/), [DESIGN.md](http://design.md/) three-layer model: [https://dev.to/aws-builders/agentsmd-skillmd-designmd-how-ai-instructions-split-into-three-layers-d0g](https://dev.to/aws-builders/agentsmd-skillmd-designmd-how-ai-instructions-split-into-three-layers-d0g)