---

---
|   |   |
| --- | --- |
| **Epic Name** | PoC |
| **Component Name** | [CLAUDE.md](http://claude.md/) architecture + Agent v2 context model |
| **Document status** | In Progress |
| **Phase** | PoC |
| **Last updated** | 2026-05-22 |

# Overview

This PoC analyzes the current `CLAUDE.md` (282 lines) against 2026 best practices for agent context management, identifies structural bloat and missing elements, and proposes a modular split using `@imports`. The output is the foundation for a new agent version with improved context discipline, Law-based behavior, and anti-context-drift tooling.

Scope: [CLAUDE.md](http://claude.md/) restructuring, 4 Laws of Agentic Workflow, context drift solution. Out of scope: implementing new agent roles, new Notion templates (covered separately).

# Motivation

The current [CLAUDE.md](http://claude.md/) is 282 lines and growing. Every agent reads it in full on every ticket. Within 6 months it will exceed practical token limits, agents will skip sections silently, and there is no mechanism to detect goal drift between agents. The existing file also lacks explicit agent behavior laws, leaving sycophancy and context drift unaddressed at the framework level.

# Findings

- [**CLAUDE.md**](http://claude.md/)** is 2.3× the recommended upper limit.** 2026 best practice (Karpathy LLM Wiki pattern) targets 50–100 lines for the always-loaded context file, with larger sections loaded on demand via `@imports`.
- **The Agent Workflow section (lines 177–282) is the biggest bloat block.** It duplicates information already in Notion (agent prompts, quality signals) and does not belong in the file a Dev Engineer reads on every ticket.
- **Three structural gaps exist** that no current file covers: (1) explicit agent behavior laws, (2) handoff signals (`still_solving` / `expected_outputs` / `addressed`), and (3) `@import` declarations pointing to the extended docs.
- **CLAUDE_**[**proposed.md**](http://proposed.md/)** already exists** at 124 lines — a valid starting trimmed draft, but it still lacks the missing elements and has not replaced the original.
- **4 Laws of Agentic Workflow** were designed in this session as the behavior foundation for Agent v2. They require a dedicated `docs/AGENT_LAWS.md` file before they can be referenced from [CLAUDE.md](http://claude.md/).
- **Context drift** ("Don't be Dory") is solved at process level with `TaskCreate` for all open items + incremental Notion comments as external memory, not just end-of-session dumps.

# Breakdown

## What stays in [CLAUDE.md](http://claude.md/)

These sections are read on every ticket and must remain inline:

| Section | Why it stays |
| --- | --- |
| Critical rules | Absolute constraints; must be front-loaded |
| Phase boundaries | Prevents Phase 2+ implementation by default |
| Stack | Platform/architecture context for every code decision |
| Constants file pointers | RecipeConstants, CookingListConstants — single reference |
| Agent laws pointer | Points to `docs/AGENT_LAWS.md` — inline stub only |
| Handoff signals | `still_solving` / `expected_outputs` / `addressed` — format reference |
| @import declarations | The list of on-demand docs |

## What moves out via @imports

| Section | Target file | Status |
| --- | --- | --- |
| Entities (FoodoireSchemaV1) | `docs/DATA_MODEL.md` | File exists |
| Service layer | `docs/ARCHITECTURE.md` | File exists |
| Navigation rules, MV/MVVM, Error patterns | `docs/CONVENTIONS.md` | File exists |
| Build/test/lint commands | `docs/COMMANDS.md` | New file needed |
| Agent workflow detail, Skills table, Changelog | Notion only | Remove from [CLAUDE.md](http://claude.md/) |

## What's missing (new content to add)

| Missing element | Where it goes | Notes |
| --- | --- | --- |
| `docs/AGENT_LAWS.md` | New file | 4 Laws designed in this session |
| `@import` block | Top of [CLAUDE.md](http://claude.md/) | Points to DATA_MODEL, ARCHITECTURE, CONVENTIONS, COMMANDS, AGENT_LAWS |
| Handoff signal format | [CLAUDE.md](http://claude.md/) inline | `still_solving` / `expected_outputs` / `addressed` |
| Agent laws 1-line stub | [CLAUDE.md](http://claude.md/) inline | Full detail lives in AGENT_[LAWS.md](http://laws.md/) |

## 4 Laws of Agentic Workflow (designed this session)

| # | Name | MUST statement | Why |
| --- | --- | --- | --- |
| Law 1 | Follow the Ticket | Agent MUST execute the ticket as written. Raise concerns before starting, not after. | Trust the process else challenge it but do not deviate |
| Law 2 | Leave a Trail | Agent MUST record all open items, decisions, and blockers as Notion comments — incrementally, not just at session end. | A session without a trail never happened |
| Law 3 | Don't be Dory | Agent MUST use TaskCreate for all open items and verify context before acting. Never rely on implicit session memory. | Memory evaporates; the ticket is the truth |
| Law 4 | Be like Spock | Agent MUST think alongside the owner, arrive with a view, flag uncertainty, and challenge assumptions — never defer blindly. | Anti-sycophancy: value comes from honest analysis, not agreement |

## Proposed [CLAUDE.md](http://claude.md/) target structure

```javascript
# Foodoire — Claude Code Manifest
[2-3 sentence prologue]

## Critical rules          (~12 lines)
## Phase boundaries         (~6 lines)
## Stack                    (~8 lines)
## Constants                (~4 lines)
## Agent laws               (~8 lines — stub + pointer to AGENT_LAWS.md)
## Handoff signals          (~8 lines)
@import docs/DATA_MODEL.md
@import docs/ARCHITECTURE.md
@import docs/CONVENTIONS.md
@import docs/AGENT_LAWS.md
@import docs/COMMANDS.md
```

Target: ~55–65 lines inline, remainder on demand.

## Line count comparison

| File | Lines | Status |
| --- | --- | --- |
| [CLAUDE.md](http://claude.md/) (current) | 282 | Bloated |
| CLAUDE_[proposed.md](http://proposed.md/) | 124 | Trimmed draft (exists, not deployed) |
| Target after @imports | ~60 | Goal |

# Recommendations

- **Do now:** Create `docs/AGENT_LAWS.md` with the 4 Laws. Add `@import` block and handoff signals to CLAUDE_[proposed.md](http://proposed.md/). Deploy CLAUDE_[proposed.md](http://proposed.md/) as the new [CLAUDE.md](http://claude.md/).
- **Do now:** Create `docs/COMMANDS.md` with build/test/lint commands (currently in [CLAUDE.md](http://claude.md/)).
- **Defer:** Context7 MCP + Basic Memory MCP integration — covered in DOC-002 subpoint 7a; implement when MCP toolchain is ready.
- **Defer:** Full [RECENT.md](http://recent.md/) rotating log — B-tier from Sequential Agent Workflow PoC; worth doing after S+A tier is in place.
- **Discard:** Agent workflow detail, Skills table, Changelog from [CLAUDE.md](http://claude.md/) — these belong in Notion, not in agent context.

# Descoped

- Implementing new agent roles (Execution Agent, Judge Agent) — covered in Sequential Agent Workflow PoC; not part of this context restructuring.
- Context7 / Basic Memory MCP setup — infrastructure change, tracked in DOC-002.
- Automated [CLAUDE.md](http://claude.md/) staleness detection — descoped to later iteration.
- Personalised per-agent [MEMORY.md](http://memory.md/) (subagent memory) — descoped; requires B-tier agent workflow first.

# References

- Sequential Agent Workflow — 2026 Upgrade PoC: [[Sequential Agent Workflow — 2026 Upgrade PoC]]
- DOC-002 (context retrieval subpoint 7a): [[DOC-002 - AI Agentic Workflow Improvement Ideas]]
- Karpathy LLM Wiki pattern (April 2026): raw sources → LLM-maintained wiki → schema file
- CLAUDE_[proposed.md](http://proposed.md/): `/Users/kovacsmark/Documents/RecipeAPP/Foodoire/CLAUDE_proposed.md`
- Current [CLAUDE.md](http://claude.md/): `/Users/kovacsmark/Documents/RecipeAPP/Foodoire/CLAUDE.md`