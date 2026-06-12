---

---
| Field | Value |
| --- | --- |
| Status | Draft |
| Type | Workflow / Agent Design |
| Created | 2026-05-23 |
| Author | Project Owner + Claude |

## Overview

The Collegium is the 4-agent sequential execution pipeline for feature tickets, running between the two Senate sessions. Praetor executes, Tribunus reviews code, Probator verifies tests, Curator checks operational readiness. Each agent has context isolation by design — no reviewer inherits prior agent opinions, only the Praetor output (ticket comment). Delta doc is created in revision flow only. Tribunus and Probator hold intercessio (single-issue veto); Curator issues a 3-level verdict. An optional Senate Censura may follow at the owner's discretion.

## Motivation

The old pipeline had 4 separate agents (Dev Engineer, Peer Reviewer, QA, DevOps) without formal veto format, no delta tracking, no anti-sycophancy guard, and no context isolation between reviewers. The Collegium formalizes the pipeline with a unified veto format (collegium-veto), progressive disclosure skill loading, and comment-driven reviews that prevent reviewers from re-litigating the entire codebase; delta doc is created only in revision flow.

## Pipeline Context

```javascript
// no prior spike
Senate: Consilium → Praetor → Tribunus → Probator → Curator → [Senate: Censura — optional]
                        ↑____________↑____________↑                      |
                            praetor-revision (veto loop)                 |
                                                              Censura RED → Praetor fix → Censura re-check
                                                              (Tribunus/Probator/Curator skip unless owner escalates)

// spike doc exists
Spike doc → Praetor → Tribunus → Probator → Curator → [Senate: Censura — optional]
                ↑____________↑____________↑
                    praetor-revision (veto loop)
```

Consilium is skippable if a completed spike doc covers the ticket's unknowns — Praetor reads spike doc directly.

## Agents

| Agent | Roman role | Maps to | Context source |
| --- | --- | --- | --- |
| Praetor | Commander — executes the mandate | Dev Engineer | Consilium output + ticket |
| Tribunus | Tribune — intercessio authority | Peer Reviewer | Ticket comments (Praetor output) |
| Probator | Verifier — proves correctness | QA Specialist | Ticket comments (Praetor output) |
| Curator | Operational steward | DevOps | Ticket comments + build/lint output |

No personas for execution agents — research confirms personas reduce accuracy on focused tasks (Stanford/Contextual AI 2026, 71.6% → 68.0%).

## Praetor — Execution Stages

**INPUT**

Load ticket, [CLAUDE.md](http://claude.md/), and relevant source files. If spike doc exists, read Decision Table before forming own solution. Form own solution before reading Consilium output — sycophancy guard. Reconcile approaches only after independent draft is complete.

**DISCUSSION**

Present approach to owner before writing any code. No code until explicit approval or redirect. Redirect = new ticket, not scope expansion.

**OUTPUT**

Implement ticket scope only — nothing beyond it. Post ticket comment using [ticket-comment.md](http://ticket-comment.md/). Update `updatedAt` on every mutation. Call `context.save()` after every SwiftData mutation.

**REVISION**

Load veto. Fix only the flagged issue — no cleanup, no scope creep. Create delta doc child page in Notion under the ticket. Document what changed and what was explicitly not touched.

## Tribunus — Review Stages

**INPUT**

Load ticket comments (Praetor output) only — fresh eyes by default. If scope drift or approach mismatch is suspected during review: load Consilium comment scope-only (still_solving + expected_outputs; never the decisions section). If Consilium was consulted: note it in ticket comment. In revision flow: also load delta doc child page. Map changed files. Run code-review-checklist against each.

**OUTPUT**

Declare all findings (LOW/MED/HIGH) before deciding. MED/HIGH triggers HITL checkpoint with owner before veto is logged. Clean pass must cite verified checklist items — silence is invalid. Post ticket comment using [ticket-comment.md](http://ticket-comment.md/).

## Probator — QA Stages

**INPUT**

Load ticket comments (Praetor output). In revision flow: also load delta doc child page. Identify every changed code path that needs coverage. Run existing test suite before forming any opinion.

**OUTPUT**

Report test results explicitly — pass/fail per changed path. Missing coverage on a changed path = finding. Any failure or MED/HIGH gap triggers veto. Post ticket comment using [ticket-comment.md](http://ticket-comment.md/).

## Curator — Operational Stages

**INPUT**

Load ticket comments (Praetor output). In revision flow: also load delta doc child page. Run build and lint — no prior agent opinions, operational lens only. Check each area before forming verdict. "Needs Attention" items must be explicitly listed in output comment — Censura loads these as mandatory input.

**OUTPUT**

Issue verdict per area: Ready to Merge / Needs Attention / Needs Work. Every area explicitly verified — silence is not a pass. Post ticket comment using [ticket-comment.md](http://ticket-comment.md/).

## Veto Mechanism (Intercessio)

Tribunus and Probator each hold one veto — single issue only. Owner receives the veto via Notion comment and decides: revision needed or override. If revision: Praetor opens praetor-revision, fixes only the flagged issue, re-submits to the vetoing agent. Curator does not veto — issues verdict instead.

Senate Censura may also issue RED verdict — treated as pipeline veto. Censura RED on OPUS: Praetor targeted fix → Censura re-check only. Tribunus, Probator, Curator do not re-run unless owner explicitly escalates to full cycle. If Censura RED is triggered by a Curator "Needs Attention" item that was not blocked: Censura output must log "pipeline miss" — Curator flagged but did not block.

## Skill Tree

**Praetor**

| Skill | Size | Load | Summary |
| --- | --- | --- | --- |
| praetor-input | ~2-3k | Preloaded | Load context. If spike doc exists, read Decision Table first. Form own solution before reading Consilium output — sycophancy guard. Reconcile only after independent draft is done. |
| praetor-discussion | ~500t | On-demand | Present approach. No code until owner approves. Redirect = new ticket, not scope expansion. |
| praetor-output | ~1k | On-demand | Implement ticket scope only — nothing beyond it. Post ticket comment using [ticket-comment.md](http://ticket-comment.md/). Update `updatedAt` on every mutation. |
| praetor-revision | ~2k | On-demand | Load veto. Fix only the flagged issue — no cleanup, no scope creep. Create delta doc child page in Notion under the ticket. Document what changed and what was explicitly not touched. |
| swift-patterns | ~3-5k | On-demand | Reference for iOS/Swift conventions. Load before writing any Swift code. Replicate existing patterns — never invent new ones. |
| swiftdata-patterns | ~3-5k | On-demand | Reference for SwiftData query, mutation, and relationship patterns. Load before touching any `@Model` or `context.save()` call. Pattern-first — no improvisation. |

**Tribunus**

| Skill | Size | Load | Summary |
| --- | --- | --- | --- |
| tribunus-input | ~1-2k | Preloaded | Load ticket comments (Praetor output) only — fresh eyes by default. If scope drift or approach mismatch is suspected during review: load Consilium comment scope-only (still_solving + expected_outputs; never the decisions section). If Consilium was consulted: note it in ticket comment. In revision flow: also load delta doc child page. Map changed files. Run code-review-checklist against each. |
| tribunus-output | ~1k | On-demand | Load [ticket-comment.md](http://ticket-comment.md/). Declare all findings before deciding. MED/HIGH = HITL checkpoint then veto. Clean pass must cite verified checklist items — silence is invalid. Post ticket comment. |
| code-review-checklist | ~2-3k | On-demand | Existing skill. Apply each item explicitly against the delta. No implicit "looks fine." |

**Probator**

| Skill | Size | Load | Summary |
| --- | --- | --- | --- |
| probator-input | ~1-2k | Preloaded | Load ticket comments (Praetor output). In revision flow: also load delta doc child page. Identify every changed code path that needs coverage. Run existing test suite before forming any opinion. |
| probator-output | ~1k | On-demand | Report test results explicitly — pass/fail per changed path. Missing coverage on a changed path = finding. Any failure or MED/HIGH gap triggers veto. Post ticket comment using [ticket-comment.md](http://ticket-comment.md/). |
| ios-testing | ~2-3k | On-demand | Existing skill. Testing patterns for SwiftUI, SwiftData, and iOS. Load before evaluating any test coverage. |

**Curator**

| Skill | Size | Load | Summary |
| --- | --- | --- | --- |
| curator-input | ~1-2k | Preloaded | Load ticket comments (Praetor output). In revision flow: also load delta doc child page. Run build and lint — no prior agent opinions, operational lens only. Check each area before forming verdict. "Needs Attention" items must be explicitly listed in output comment — Censura loads these as mandatory input. |
| curator-output | ~1.5k | On-demand | Issue verdict per area: Ready to Merge / Needs Attention / Needs Work. Every area explicitly verified — silence is not a pass. Post ticket comment using [ticket-comment.md](http://ticket-comment.md/). |

**Shared**

| Skill | Size | Load | Summary |
| --- | --- | --- | --- |
| collegium-veto | ~500t | Preloaded | Shared veto format for all review agents. Preloaded so Praetor recognizes a valid veto on arrival. Response must be targeted — not a general rewrite. |

## Modern Agent Elements → Laws Mapping

| Element | Description | Law |
| --- | --- | --- |
| Anti-sycophancy guard | Own draft before Consilium read — independent first | Law 4 |
| Delta doc | Revision artifact only — created when veto occurs; Praetor links it in ticket comment | Law 2 |
| Context isolation | Tribunus/Probator load ticket comments — no prior opinions; delta doc in revision only | Law 3 |
| Pre-flight checklist | All context loaded before starting any stage | Law 3 |
| Single-issue veto | One flagged issue per review agent — scope discipline | Law 1 |
| HITL checkpoint | Owner review on MED/HIGH before veto is logged | Law 4 |
| Mandatory findings declaration | All findings before veto decision — no silent pass | Law 4 |
| Revision scope lock | Fix only vetoed issue — document what was not touched | Law 1 |
| Operational verdict | Curator checks all 8 areas explicitly | Law 2 |
| Scope creep guard | Redirect = new ticket, never scope expansion | Law 1 |

## File Structure

Follows the **progressive disclosure pattern** — one skill file per stage, loaded on demand.

```javascript
docs/agents/praetor.md
  → identity; constraints; Laws mapping; no persona; allowed tools: Read, Edit, Write, Bash; isolation: worktree

docs/agents/tribunus.md
  → identity; constraints; Laws mapping; no persona; intercessio authority; allowed tools: Read

docs/agents/probator.md
  → identity; constraints; Laws mapping; no persona; veto authority; allowed tools: Read, Bash

docs/agents/curator.md
  → identity; constraints; Laws mapping; no persona; 3-level verdict authority; allowed tools: Read, Bash

docs/skills/praetor-input.md
  → pre-flight; spike doc Decision Table reading (if exists); anti-sycophancy (own draft before Consilium read); reconciliation; context checkpoint

docs/skills/praetor-discussion.md
  → approach presentation; owner approval gate; redirect = new ticket rule

docs/skills/praetor-output.md
  → implement ticket scope only; post ticket comment (ticket-comment.md); updatedAt rule; context.save() rule

docs/skills/praetor-revision.md
  → veto load; single-issue fix scope lock; create delta doc child page under ticket; revision delta doc (changed + explicitly not touched)

docs/skills/tribunus-input.md
  → ticket comment load (default); Consilium comment on-demand only — if scope drift suspected (still_solving + expected_outputs, never decisions); note in ticket comment if consulted; fresh eyes by default; in revision: delta doc child page; code-review-checklist trigger per file

docs/skills/tribunus-output.md
  → findings declaration before veto decision; MED/HIGH HITL checkpoint; veto or clean pass with evidence

docs/skills/probator-input.md
  → ticket comment load; in revision: delta doc child page; test path mapping; test suite run; no prior agent opinions

docs/skills/probator-output.md
  → pass/fail per changed path; missing coverage = finding; failure or MED/HIGH = veto

docs/skills/curator-input.md
  → ticket comment load; in revision: delta doc child page; build run; lint run; 8-area check (build, lint, CLAUDE.md compliance, phase boundary, localization, dead code, operational risk, delta scope)

docs/skills/curator-output.md
  → verdict per area; Ready to Merge/Needs Attention/Needs Work definition; every area must be cited

docs/skills/ticket-comment.md
  → shared comment etiquette; max 15 lines; still_solving + addressed + expected_outputs + routing; stage update after posting

docs/skills/collegium-veto.md
  → single-issue format; targeted fix contract; veto response scope rule (Praetor + Tribunus + Probator)
```

## Recommendations

### Do now

- Write `AGENT_LAWS.md` (Laws 1–4 as principia — prerequisite for all agent files)
- Write `docs/skills/ticket-comment.md` (shared comment etiquette — all Collegium agents load before posting)
- Define delta doc format in `docs/skills/praetor-revision.md` — revision-only artifact; Praetor creates child page and links from ticket comment
- Write `docs/agents/praetor.md` and all Praetor skill files
- Write `docs/skills/collegium-veto.md`
- Write `docs/agents/tribunus.md`, `probator.md`, `curator.md` and their skill files
- Add all agents to `docs/agents/session-starters.md` — retire old entries: dev-engineer, peer-reviewer, qa-specialist, devops, master-architect
- Add Coding Principia section to `CLAUDE.md` (surgical, pattern first, no comments, no speculation)

### Defer

- Senate Censura session starter — mandatory closing step per pipeline design (Senate PoC: Censura always closes every pipeline run); owner decides when to initiate the session, not whether to run it
- Automated veto loop — currently manual (owner reads Notion comment, directs revision)
- Reformatting existing skills (swift-patterns, swiftdata-patterns, code-review-checklist, ios-testing) to machine-first format

### Discard

- Personas for execution agents — performance degradation confirmed on focused tasks (Stanford/Contextual AI 2026)
- Consilium Principiorum (pre-execution Collegium alignment) — sequential HITL sufficient for current scale

## Descoped

- Parallel agent execution — sequential pipeline sufficient for current scale
- Automated orchestration — manual session-per-agent chosen (same pattern as Senate)
- Structured JSON output — not needed for current manual workflow (Anthropic native structured outputs API available when/if automation is added)

## References

- Senate Agent Design PoC: [[Senate Agent Design PoC]]
- Quaestor Agent Design PoC: [[Quaestor Agent Design PoC]]
- [CLAUDE.md](http://claude.md/): `/Users/kovacsmark/Documents/RecipeAPP/Foodoire/CLAUDE.md`
- Silicon Mirror (2026) — staged information revelation, anti-sycophancy research
- Stanford/Contextual AI 2026 — persona accuracy on focused tasks
- Agent prompts: [[Agent Delivery]]
- Ticketing: [[NOTION_PAGE:34468d5d-e1e8-8092-a8e5-ed0976c21d26]]