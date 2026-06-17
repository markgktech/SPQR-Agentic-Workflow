---

---
## Affected Files

- `docs/skills/quaestor-doc-execute.md` — NEW
- `docs/skills/quaestor-relatio.md` — UPDATE ⚠️ **shared with Group 2 — coordinate writes**
- `docs/agents/session-starters.md` — UPDATE (both repos: Foodoire + generic SPQR)
- `docs/agents/senate.md` — UPDATE ⚠️ **shared with Group 1 — write once, covers both groups**
- `docs/agents/quaestor.md` — UPDATE

---

## Items #19 + #21 + #22 — [quaestor-doc-execute.md](http://quaestor-doc-execute.md/)

**What:** New skill file for DOC-type ticket handling. Three concerns merged into one file:

- DOC trigger condition: ticket prefix DOC-XXX triggers this skill
- Discovery rules: how to find which files need updating (load ticket, read items, map to file paths)
- Ticket creation boundaries: what Quaestor can propose vs. what requires owner decision
- Per-fix re-verification protocol: after applying each fix, re-read the relevant section before moving to next item; never assume a fix landed correctly without checking

**Format:** Machine-first, ALLCAPS sections, NEVER constraints mandatory.

**Where:** `docs/skills/quaestor-doc-execute.md` — new file

---

## Item #20 — [quaestor-relatio.md](http://quaestor-relatio.md/) DOC Trigger Reference

**What:** Add one-line DOC trigger reference to [quaestor-relatio.md](http://quaestor-relatio.md/) + adjust load order to include [quaestor-doc-execute.md](http://quaestor-doc-execute.md/) when ticket prefix is DOC-XXX.

**Where:** `docs/skills/quaestor-relatio.md` — load order section; one-line conditional: if DOC prefix → load [quaestor-doc-execute.md](http://quaestor-doc-execute.md/)

**Depends on:** #19

---

## Item #3 — Persona Names → [session-starters.md](http://session-starters.md/)

**What:** Extract persona names from agent files into [session-starters.md](http://session-starters.md/) as a PERSONAS lookup table. Agent files keep definitions (Cicero/Rich Hickey etc.) but not the real names.

**Generic SPQR repo:**

- `docs/agents/session-starters.md` → add PERSONAS section with [Name 1] / [Name 2] / [Name 3] / [Name 4] placeholders
- `docs/agents/senate.md` → replace Tomi/Zsombi/Peti with [Name 1] / [Name 2] / [Name 3]
- `docs/agents/quaestor.md` → replace Timi with [Name 4]

**Foodoire repo:**

- `docs/agents/session-starters.md` → add PERSONAS section with real names: Tomi / Zsombi / Peti / Timi
- `docs/agents/senate.md` → replace hardcoded names with [Name 1] / [Name 2] / [Name 3]
- `docs/agents/quaestor.md` → replace Timi with [Name 4]

**Implementation note:** Definitions stay in agent files. Session-starters is the only place with real names (Foodoire) or customizable placeholders (generic SPQR). Agent uses the lookup at session start when a persona-carrying agent is invoked.

---

## Changes Made

- `docs/skills/quaestor-doc-execute.md` → new file: DOC ticket execution flow, per-fix verification, ticket creation boundaries, NEVER section
- `docs/skills/quaestor-relatio.md` → pre-flight load order: step 6 added — if DOC-XXX prefix → load [quaestor-doc-execute.md](http://quaestor-doc-execute.md/)
- `docs/agents/quaestor.md` → STAGE SKILL: DOC mention added; Timi → [Name 4]
- `docs/agents/senate.md` → Tomi→[Name 1], Zsombi→[Name 2], Peti→[Name 3]; DA role: Tomi→[Name 1]
- `docs/agents/session-starters.md` → PERSONAS section added at end of file with real names
- `docs/skills/consilium-discussion.md` → MANDATORY PER PERSONA: Tomi/Zsombi/Peti → [Name 1]/[Name 2]/[Name 3] (validation pass)
- `docs/skills/censura-discussion.md` → MANDATORY PER PERSONA: Tomi/Zsombi/Peti → [Name 1]/[Name 2]/[Name 3] (validation pass)