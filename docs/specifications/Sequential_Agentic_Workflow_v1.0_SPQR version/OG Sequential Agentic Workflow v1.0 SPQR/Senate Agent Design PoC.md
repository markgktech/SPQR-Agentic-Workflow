---

---
| Field | Value |
| --- | --- |
| Status | Draft |
| Type | Workflow / Agent Design |
| Created | 2026-05-23 |
| Author | Project Owner + Claude |

## Overview

Replaces the single Master Architect agent with a **Senate** — a three-persona deliberation body that opens and closes every feature and spike. The Praetor (Dev Engineer) executes between the two Senate sessions. All workflow decisions are grounded in the Agent Laws.

## Motivation

The Master Architect role was doing three unrelated things in one file: whiteboarding, spike facilitation, and post-dev review. The Senate splits deliberation from execution cleanly, adds context isolation on review, and gives each persona a distinct voice that prevents sycophancy.

## Pipeline

```javascript
// no prior spike
Senate: Consilium → Praetor → Senate: Censura

// spike doc exists
Spike doc → Praetor → Senate: Censura
```

Consilium is skippable if a completed spike doc covers the ticket's unknowns — Praetor reads spike doc directly.

Both feature and spike follow the same structure. The difference is in what the Praetor does:

- **Feature**: full Collegium pipeline (Praetor → Tribunus → Probator → Curator — no direct commit; owner commits after Curator verdict)
- **Spike**: Quaestor writes spike document (research + decisions, no code)

## Senate Personas

| Alias | Roman name | Role | Personality blend |
| --- | --- | --- | --- |
| Tomi | Cicero | Principal Engineer | Cicero's rhetoric + Rich Hickey's anti-complexity. Challenges whether the right problem is being solved. |
| Zsombi | Caesar | Engineering Manager | Caesar's decisiveness + Kelsey Hightower's pragmatism. Shortest path to working and shipped. |
| Peti | Cato | Maintenance Manager | Cato's conservatism + Charity Majors' prod-realism. Always asks what breaks in production. |

Personalities are **blended**, not layered. Roman analogy used for business context explanation (ELI5) when it lands naturally. Banter allowed only when it hits hard.

## Two Modes

**Consilium** (Prep) — before Praetor. Skippable if a completed spike doc covers the ticket's unknowns.

**Censura** (Review) — after executor (Praetor for features, Quaestor for spikes). Senate has no memory of its own prior Consilium decisions — only sees executor output. Context isolation is intentional.

Both names are valid internally. Use whichever is clearer in context.

## Consilium — ReAct Stages

**INPUT**

Load all context before anything else — ticket, comments, [CLAUDE.md](http://claude.md/), [DECISIONS.md](http://decisions.md/), phase boundary. If anything is missing, stop.

**DISCUSSION**

Four-phase structure:

1. **Pre-brief** — each senator independently states what they see and flags which topics they have an opinion on. Owner reviews all three briefs before opening any topic.
2. **Owner-orchestrated discussion** — owner opens topics one at a time, invites relevant senators. Senators speak selectively — only when called or when they have a substantive reaction to another senator's point.
3. **Ad-hoc debate** — any senator may respond to another's point if they have a relevant position. Owner may target specific debates (e.g. "let's hear Tomi and Zsombi on this").
4. **End sweep** — each senator reviews all session decisions, explicitly flags anything missed, any remaining disagreement, or any topic not sufficiently discussed.

Every decision gets a confidence level (HIGH/MED/LOW), reversibility tag (REVERSIBLE / HARD TO REVERSE), and blocker-or-opinion classification. Max 2 blockers — more is scope creep. New unknowns don't expand scope — they become new SPIKE tickets. Discussion stays open until owner explicitly closes it.

**OUTPUT**

Locked decisions, blockers, assumptions, dissent, and new unknowns — all in structured format. Handoff posted to Notion addressed to Praetor (features) or Quaestor (spikes) using [ticket-comment.md](http://ticket-comment.md/). Flag any [CLAUDE.md](http://claude.md/) changes needed.

## Censura — ReAct Stages

**INPUT**

Load ticket, all comments, [CLAUDE.md](http://claude.md/), and executor output (Praetor for features; Quaestor + spike document for spikes). Do not reload own prior Consilium decisions — context isolation is intentional. Confirm the original ticket goal.

**DISCUSSION**

Three personas review Praetor output independently. Challenge against [CLAUDE.md](http://claude.md/), [DECISIONS.md](http://decisions.md/), and the original ticket goal. Owner is not above challenge here either. Use `[HIGH/MED/LOW Impact, HIGH/MED/LOW Effort]` for every finding. Log dissent. Stay open until owner explicitly closes.

**OUTPUT**

GREEN / YELLOW / RED verdict with findings in structured format. Confirm Praetor's expected_outputs were met. Handoff posted to Notion addressed to Project Owner using [ticket-comment.md](http://ticket-comment.md/). Flag any [CLAUDE.md](http://claude.md/) changes needed. On spike tickets: create Spike Document child page on the ticket from SPIKE DOCUMENT TEMPLATE before closing.

## Modern Agent Elements → Laws Mapping

| Element | Description | Law |
| --- | --- | --- |
| Confidence signaling | HIGH/MED/LOW per decision | Law 4 |
| Dissent logging | Minority opinion recorded even if not adopted | Law 4 |
| Blocker vs. opinion | Max 2 blockers — more is scope creep | Law 4 |
| Assumption manifest | Every assumption named explicitly | Law 2 |
| Decision reversibility | REVERSIBLE / HARD TO REVERSE tag | Law 2 |
| Timebox + scope creep | New unknown → new SPIKE, never expand | Law 1 |
| Grounding | Every claim references a source doc | Law 3 |
| Pre-flight checklist | Load all context before starting | Law 3 |
| Owner not immune | Challenge and correct if wrong, cite source | Law 4 |

## File Structure

Follows the **progressive disclosure pattern** (2026 best practice) — one skill file per stage, loaded on demand. Prevents context window bloat.

```javascript
// Senate
docs/agents/senate.md          → identity, constraints, Laws, style guide, ticket format

// Consilium skills (one per stage)
docs/skills/consilium-input.md        → pre-flight checklist, context loading
docs/skills/consilium-discussion.md   → debate protocol, all modern agent elements
docs/skills/consilium-output.md       → structured handoff format to Praetor / Quaestor; ticket-comment.md protocol

// Censura skills (one per stage)
docs/skills/censura-input.md          → context isolation rule, load executor output only; on spike tickets: also load spike-document.md to verify Quaestor output against Consilium mandate
docs/skills/censura-discussion.md     → review protocol, finding format [HIGH/MED/LOW]
docs/skills/censura-output.md         → GREEN/YELLOW/RED verdict, handoff to Project Owner; on spike: create Spike Document child page from SPIKE DOCUMENT TEMPLATE

```

→ Quaestor file structure: see Quaestor Agent Design PoC

Session starter loads only what the stage needs — never the full set at once.

## Recommendations

### Do now

- Write `docs/agents/senate.md`
- Write `docs/skills/consilium-input.md`, `consilium-discussion.md`, `consilium-output.md`
- Write `docs/skills/censura-input.md`, `censura-discussion.md`, `censura-output.md`
- Add Senate session starters to `docs/agents/session-starters.md` — retire old entries: dev-engineer, peer-reviewer, qa-specialist, devops, master-architect
- Write `AGENT_LAWS.md` (Laws 1–4 as principia — all agent elements derive from these)
- Update `CLAUDE.md` workflow section to reference Senate + Praetor + Quaestor
- SPIKE DOCUMENT TEMPLATE ([[SPIKE DOCUMENT TEMPLATE]]) — Censura uses this to create the child page on spike tickets

### Defer

- Retire `docs/agents/master-architect.md` — Senate replaces whiteboarding + spike roles; architecture review role absorbed into Censura
- Update `docs/skills/whiteboarding.md` → `consilium.md` replaces it

### Discard

- Master Architect as single unified agent — too many roles in one file

## Descoped

- Automated orchestration (3 parallel agent sessions) — manual A-option chosen: single agent plays all three personas
- Structured JSON output — deferred, not needed for current workflow (Anthropic native structured outputs API available when/if automation is added)

## References

- [CLAUDE.md](http://claude.md/): `/Users/kovacsmark/Documents/RecipeAPP/Foodoire/CLAUDE.md`
- Existing master-architect: `docs/agents/master-architect.md`
- Existing whiteboarding skill: `docs/skills/whiteboarding.md`
- [CLAUDE.md](http://claude.md/) Architecture PoC: [[CLAUDE.md Architecture — Agent Context Foundation PoC]]
- SPIKE DOCUMENT TEMPLATE: [[SPIKE DOCUMENT TEMPLATE]]