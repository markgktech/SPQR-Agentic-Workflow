---

---
## Summary

- **v1.1 foundation:** 10 targeted improvements — feedback loop ([LESSONS.md](http://lessons.md/)), agent behavior hardening, output enrichment, tooling extension
- **v1.2 scope:** 22 items across DOC-006, DOC-007, DOC-008, DOC-009, DOC-011 — no new agents, no architecture changes; ticket creation flow automated, agent hygiene hardened, SPQR repo decoupled from Foodoire
- **Why now:** Ticket creation is owner-bottlenecked (time-consuming manual work); recurring process failures identified in SPIKE-004 Censura; generic SPQR repo contains Foodoire-specific content that prevents clean public presentation

---

## What's New — v1.2 vs v1.1

- **Ticket creation automated:** Quaestor proposes → Censura validates → owner approves → Notion tickets created (Spike, Feature, Bug, Doc) — owner no longer writes tickets manually
- **Ticket slicing skill:** New shared `ticket-slicing.md` with two modes — Quaestor "propose" (scope, priority, dependency) + Censura "validate + create" (Notion creation on owner approval); REJECT verdict loops back to Quaestor session
- **Censura two-phase model:** VERIFY pass (existing) + TICKETING phase (3 new files: censura-ticketing-input/discussion/[output.md](http://output.md/)) — clean separation, no process mixing
- **Agent hygiene hardened:** 8 fixes from SPIKE-004 Censura — handoff accuracy, web search date validation, context window alert, spike document location, discussion depth calibration, and more
- **DOC process skill:** New `quaestor-doc-execute.md` — DOC trigger detection, discovery rules, per-fix re-verification before output comment
- **SPQR repo decoupled:** Persona names extracted from [senate.md](http://senate.md/) and [quaestor.md](http://quaestor.md/) to [session-starters.md](http://session-starters.md/); generic SPQR repo uses [Name 1]–[Name 4] placeholders; Foodoire session-starters carries real names
- **SPQR repo public-ready:** All v1.2 changes synced to generic repo; all Foodoire-specific data replaced with placeholders; verified via grep (zero matches for names + Notion IDs)
- **Setup guide:** New `docs/CONFIGURE.md` in SPQR repo — every placeholder documented with location and value; Notion setup instructions; non-Notion alternatives (Linear, GitHub Issues, markdown files)

---

## Implementation Groups

**1. Ticket Automation** *(DOC-007 + DOC-008)*

Items: #9 [ticket-slicing.md](http://ticket-slicing.md/) · #10 naming convention rule · #5 quaestor-relatio-output Ticket Proposals · #6 censura-input VERIFY extension · #7 censura-output ticketing phase · #8 [senate.md](http://senate.md/) two-phase Censura

New files: `ticket-slicing.md` · `censura-ticketing-input.md` · `censura-ticketing-discussion.md` · `censura-ticketing-output.md`

Updated files: `quaestor-relatio-output.md` · `censura-input.md` · `censura-output.md` · `senate.md` · `CLAUDE.md`

**2. Agent Hygiene** *(DOC-009)*

Items: #11 expected_outputs → ticket body · #12 web search date validation · #13 handoff accuracy rule · #14 position reversal flag · #15 decision sourcing label · #16 context window alert · #17 spike document location · #18 discussion depth calibration

Updated files: `quaestor-relatio.md` (items #12, #14, #16, #18) · `quaestor-relatio-output.md` (items #13, #15, #17) · `consilium-output.md` (item #11)

**3. DOC Process & Naming** *(DOC-011 + DOC-006)*

Items: #19+21+22 [quaestor-doc-execute.md](http://quaestor-doc-execute.md/) · #20 [quaestor-relatio.md](http://quaestor-relatio.md/) DOC trigger · #3 persona names → [session-starters.md](http://session-starters.md/)

New files: `quaestor-doc-execute.md`

Updated files: `quaestor-relatio.md` · `session-starters.md` (both repos) · `senate.md` · `quaestor.md`

**4. SPQR Repo Sync**

All v1.2 Foodoire changes synced to generic SPQR repo with mandatory substitutions.

Substitutions applied: persona names → [Name 1–4] · iOS/SwiftData content → [PROJECT_BOUNDARIES] · all Notion IDs → named placeholders

Bonus fix: `spike-document.md` hardcoded Notion URL caught by verification grep and substituted.

New files synced: `ticket-slicing.md` · `censura-ticketing-input.md` · `censura-ticketing-discussion.md` · `censura-ticketing-output.md` · `quaestor-doc-execute.md`

Updated: 7 skill files · 3 agent files

**5. **[**CONFIGURE.md**](http://configure.md/)** — Setup Guide** *(SPQR repo only)*

New file: `docs/CONFIGURE.md` — 12 placeholders catalogued with file locations and values; Notion setup instructions; non-Notion alternatives documented.

New files: `docs/CONFIGURE.md`

**6. README + Version History** *(SPQR repo only)*

[README.md](http://readme.md/) updated for v1.2: title, [CONFIGURE.md](http://configure.md/) reference, How to adopt steps 4+5, file structure (6 new files), v1.2 version history entry.

`.claude/rules/AGENT_LAWS.md` scope line updated: v1.1 → v1.2.

Updated files: `README.md` · `.claude/rules/AGENT_LAWS.md`

---

## Action Plan

| # | Item | File | Type | Depends on |
| --- | --- | --- | --- | --- |
| 9 | [ticket-slicing.md](http://ticket-slicing.md/) | docs/skills/[ticket-slicing.md](http://ticket-slicing.md/) | NEW | — |
| 10 | Naming convention rule | [CLAUDE.md](http://claude.md/), [quaestor-relatio-output.md](http://quaestor-relatio-output.md/) | UPDATE | #9 |
| 5 | Ticket Proposals section | [quaestor-relatio-output.md](http://quaestor-relatio-output.md/) | UPDATE | #9 |
| 6 | VERIFY pass extension | [censura-input.md](http://censura-input.md/) | UPDATE | #9 |
| 7 | Ticketing phase trigger | [censura-output.md](http://censura-output.md/) | UPDATE | #9 |
| 8 | Two-phase Censura docs | [senate.md](http://senate.md/) | UPDATE | #7 |
| NEW | [censura-ticketing-input.md](http://censura-ticketing-input.md/) | docs/skills/ | NEW | #9 |
| NEW | [censura-ticketing-discussion.md](http://censura-ticketing-discussion.md/) | docs/skills/ | NEW | #9 |
| NEW | [censura-ticketing-output.md](http://censura-ticketing-output.md/) | docs/skills/ | NEW | #9 |
| 11 | expected_outputs → ticket body | [consilium-output.md](http://consilium-output.md/), [quaestor-relatio.md](http://quaestor-relatio.md/) | UPDATE | — |
| 12 | Web search date validation | [quaestor-relatio.md](http://quaestor-relatio.md/) | UPDATE | — |
| 13 | Handoff accuracy rule | [quaestor-relatio-output.md](http://quaestor-relatio-output.md/) | UPDATE | — |
| 14 | Position reversal flag | [quaestor-relatio.md](http://quaestor-relatio.md/) | UPDATE | — |
| 15 | Decision sourcing label | [quaestor-relatio-output.md](http://quaestor-relatio-output.md/) | UPDATE | — |
| 16 | Context window alert | [quaestor-relatio.md](http://quaestor-relatio.md/) | UPDATE | — |
| 17 | Spike document location | [quaestor-relatio-output.md](http://quaestor-relatio-output.md/) | UPDATE | — |
| 18 | Discussion depth calibration | [quaestor-relatio.md](http://quaestor-relatio.md/) | UPDATE | — |
| 19+21+22 | [quaestor-doc-execute.md](http://quaestor-doc-execute.md/) | docs/skills/ | NEW | — |
| 20 | DOC trigger reference | [quaestor-relatio.md](http://quaestor-relatio.md/) | UPDATE | #19 |
| 3 | Persona names → session-starters | [session-starters.md](http://session-starters.md/), [senate.md](http://senate.md/), [quaestor.md](http://quaestor.md/) | UPDATE | — |

---

## Changes Made

**Group 1 — Ticket Automation**

- `docs/skills/ticket-slicing.md` — NEW: two-mode skill (Quaestor propose + Censura validate+create), slicing criteria, NEVER section
- `docs/skills/censura-ticketing-input.md` — NEW: ticketing phase entry, Notion template IDs, context carry-over
- `docs/skills/censura-ticketing-discussion.md` — NEW: PASS/REVISE/REJECT per proposal
- `docs/skills/censura-ticketing-output.md` — NEW: owner approval gate, Notion creation, reject protocol
- `docs/skills/quaestor-relatio-output.md` — UPDATE: TICKET PROPOSALS section added
- `docs/skills/censura-input.md` — UPDATE: ticket proposals check in PRE-CHECK; [ticket-slicing.md](http://ticket-slicing.md/) in LOAD ORDER
- `docs/skills/censura-output.md` — UPDATE: TICKETING PHASE TRIGGER added
- `docs/agents/senate.md` — UPDATE: CENSURA two-phase model documented
- `CLAUDE.md` — pending owner action: naming convention rule

**Group 2 — Agent Hygiene**

- `docs/skills/consilium-output.md` — UPDATE: expected_outputs → ticket body Handoff section; NEVER rule added
- `docs/skills/quaestor-relatio.md` — UPDATE: pre-flight item 5; date validation; position reversal flag; discussion depth calibration; 80% context alert NEVER rule
- `docs/skills/quaestor-relatio-output.md` — UPDATE: decision sourcing label; spike doc → Exploracio/Spiking + backlink + URL report; handoff accuracy NEVER rule

**Group 3 — DOC Process & Naming**

- `docs/skills/quaestor-doc-execute.md` — NEW: DOC ticket execution, per-fix verification, ticket creation boundaries
- `docs/skills/quaestor-relatio.md` — UPDATE: DOC-XXX trigger in pre-flight load order
- `docs/agents/quaestor.md` — UPDATE: STAGE SKILL + DOC mention; Timi → [Name 4]
- `docs/agents/senate.md` — UPDATE: Tomi/Zsombi/Peti → [Name 1]/[Name 2]/[Name 3]
- `docs/agents/session-starters.md` — UPDATE: PERSONAS section added (Foodoire: real names)

**Group 4 — SPQR Repo Sync**

- 5 new skill files synced to SPQR repo with substitutions
- 7 existing skill files updated in SPQR repo
- 3 agent files updated in SPQR repo
- `spike-document.md` bonus fix: hardcoded Notion URL → [SPIKE_DOCUMENT_TEMPLATE_ID]
- [consilium-discussion.md](http://consilium-discussion.md/) + [censura-discussion.md](http://censura-discussion.md/): Tomi/Zsombi/Peti → [Name 1]/[Name 2]/[Name 3]

**Group 5 — **[**CONFIGURE.md**](http://configure.md/)

- `docs/CONFIGURE.md` — NEW in SPQR repo: 12 placeholders, Notion setup, non-Notion alternatives

**Group 6 — README + Version History**

- `README.md` — title v1.1→v1.2; [CONFIGURE.md](http://configure.md/) reference added; Step 4+5 updated; 6 new files in file structure; v1.2 version history entry
- `.claude/rules/AGENT_LAWS.md` — SCOPE: v1.1 → v1.2

---

## Stalled / Deferred

- DOC-006 #1 Session-starter config spec — overhead too high, single-person project
- DOC-006 #2 [session-starters.md](http://session-starters.md/) move — resolved as no-move; stays in docs/agents/
- DOC-006 #4 Foodoire migration — deferred; separate session after v1.2 closes
- DOC-010 — descoped entirely

[[Ticket Automation]]

[[Agent Hygiene]]

[[DOC Process & Naming]]

[[SPQR Repo Sync]]

[[CONFIGURE.md — Setup Guide for Template SPQR repo]]

[[README + Version History]]

[[Agentic Workflow Upgrade — Way of Working]]