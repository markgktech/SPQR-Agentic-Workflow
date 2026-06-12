---

---
## Summary

- **Problem:** `docs/upgrade/session-starter.md` is a monolithic file — paste prompt + agent definition + config block + skill index in one. This is against the SPQR agent pattern ([senate.md](http://senate.md/), [praetor.md](http://praetor.md/)), caused the 7k token upfront burn, and forced the owner to fill in the same variables in 3 different files.
- **Pattern fix:** Follow the existing delivery pipeline architecture: thin session-starter (paste prompt only) + separate agent file (IDENTITY, CONFIG, STAGE SKILLS, LAWS, TOOLS, NEVER). Skill files load on-demand per phase, not at session start.
- **Scope:** New `upgrade-agent.md`; rewrite `session-starter.md`; patch `roundtable.md`; update `CONFIGURE.md` and `README.md`.

---

## What's Changing

**New file — **`**docs/upgrade/upgrade-agent.md**`

Full agent definition extracted from [session-starter.md](http://session-starter.md/). Contains:

- `CONFIG` block at the top: all variables in one place (project name, repo paths, persona names, memory path). Owner fills this in once — no other file has placeholders.
- `PIPELINE`: 6 phases with scope-first Phase 1 (ask owner for tickets → fetch only what was provided — no blind Notion search)
- `STAGE SKILLS`: explicit which skill file loads at which phase, on-demand
- `LAWS`, `ALLOWED TOOLS`, `NEVER`

**Rewrite — **`**docs/upgrade/session-starter.md**`

Becomes a 3-line paste prompt only — identical in shape to `docs/agents/session-starters.md`:

```javascript
Load docs/upgrade/upgrade-agent.md
Load .claude/rules/AGENT_LAWS.md
Scope: [ticket URLs or description]
```

All config (paths, persona names, memory path) lives in [upgrade-agent.md](http://upgrade-agent.md/) CONFIG. Owner fills it in there before starting.

**Patch — **`**docs/upgrade/roundtable.md**`

PERSONAS section replaced with one line: `Personas: defined in upgrade-agent.md CONFIG — loaded before this file.` No placeholder duplication.

**Update — **`**docs/CONFIGURE.md**`

- `[Master Persona 1]` and `[Master Persona 2]` file reference changes from `session-starter.md, roundtable.md` → `upgrade-agent.md` only
- `[SPQR_REPO_PATH]` file reference: `session-starter.md` → `upgrade-agent.md`
- New row: `[MEMORY_PATH]` → `upgrade-agent.md` — absolute path to [MEMORY.md](http://memory.md/) on disk

**Update — **`**README.md**`

File structure updated ([upgrade-agent.md](http://upgrade-agent.md/) added); How to adopt step 5 updated.

---

## What Stays the Same

All 6 skill files keep their content unchanged: `roundtable.md` (minus the PERSONAS section), `decision-making.md`, `planning.md`, `execution.md`, `context-window.md`, `wrap-up.md`. No skill file logic changes.

---

## Implementation Groups

**Group 1 — **[**upgrade-agent.md**](http://upgrade-agent.md/)** (new file)**

- Affected files: `docs/upgrade/upgrade-agent.md` (new)
- What: full agent definition; CONFIG block; PIPELINE with scope-first Phase 1; STAGE SKILLS
- Dependency: none — first group

**Group 2 — **[**session-starter.md**](http://session-starter.md/)** (rewrite)**

- Affected files: `docs/upgrade/session-starter.md` (full rewrite)
- What: thin paste prompt only — 3 lines
- Dependency: Group 1 done

**Group 3 — **[**roundtable.md**](http://roundtable.md/)** + **[**CONFIGURE.md**](http://configure.md/)** + **[**README.md**](http://readme.md/)

- Affected files: `docs/upgrade/roundtable.md` (one-line patch), `docs/CONFIGURE.md` (3 changes), `README.md` (2 changes)
- What: remove PERSONAS from roundtable; update placeholder file refs; add MEMORY_PATH row
- Dependency: Group 1 done

---

## New File Sketch — [upgrade-agent.md](http://upgrade-agent.md/)

```javascript
IDENTITY
Role: Upgrade Master Agent — orchestrates SPQR workflow upgrades
from DOC tickets to versioned, documented changes applied across all files
No persona — orchestration accuracy; roundtable personas defined in CONFIG
Never modifies repo files — writes execution briefs only

CONFIG
[Fill in once before loading this file]
Project name:  [YOUR_PROJECT_NAME]
Project repo:  [PROJECT_REPO_PATH]
SPQR repo:     [SPQR_REPO_PATH]
Memory:        [MEMORY_PATH]
Persona 1:     [MASTER_PERSONA_1_NAME] — Dev Process Architect
Persona 2:     [MASTER_PERSONA_2_NAME] — Agentic Trends Expert

PIPELINE
Phase 1 — Context Loading
  1. Read [MEMORY_PATH] — load decisions, file maps, versioning
  2. Ask owner: which tickets are in scope? (provide URLs or describe)
  — wait for owner response —
  3. If URLs provided: fetch them. If description only: ask for specific URLs before fetching anything.
  4. Present summary; do not proceed until owner confirms scope
  SCOPE GATE: scope confirmed before Phase 2

Phase 2 — Roundtable
  Load: docs/upgrade/roundtable.md
  Personas from CONFIG review all tickets; build flat item list
  CHECKPOINT 1: owner closes Phase 2 before Phase 3 starts

Phase 3 — Decision Making
  Load: docs/upgrade/decision-making.md
  Item-by-item; save decisions to memory in real time

Phase 4 — Planning
  Load: docs/upgrade/planning.md
  Group items; create Notion upgrade doc + sub-pages; write briefs

Phase 5 — Execution
  Load: docs/upgrade/execution.md
  Launch execution agent per group; review output
  Load on-demand: docs/upgrade/context-window.md — before compacting or when group headroom is low
  CHECKPOINT 2: owner confirms each group before next launches
  CHECKPOINT 3: owner confirms all groups done before Phase 6

Phase 6 — Wrap-up
  Load: docs/upgrade/wrap-up.md

LAWS
Load: .claude/rules/AGENT_LAWS.md — all four laws apply before any action
Law 2 critical: owner discussion is mandatory preparation;
wait for explicit close before Phase 3 starts

ALLOWED TOOLS
Read (upgrade skill files, AGENT_LAWS.md, repo files — never modify)
Notion MCP: notion-fetch, notion-create-pages, notion-update-page, notion-create-comment
Memory: read [MEMORY_PATH] at Phase 1; write at each major checkpoint

NEVER
- modify repo files in the orchestration session
- write to CLAUDE.md directly — propose text only; owner applies manually
- run git commit or git push
- invent a ticket prefix or number — owner assigns
- start Phase 3 before owner explicitly closes Phase 2
- launch next execution group without owner confirmation
- leave any item without a clear disposition
- treat "let's move on" as explicit Phase 2 close (Law 2)
- suppress a roundtable finding or issue a silent clean pass (Law 4)
- load next phase skill before entering that phase
- fetch Notion pages before owner confirms scope
```

---

## New File Sketch — [session-starter.md](http://session-starter.md/) (thin)

```javascript
UPGRADE MASTER SESSION

Load docs/upgrade/upgrade-agent.md

Scope: [paste ticket URLs here, or describe what you want to upgrade]
```

Note: fill in [upgrade-agent.md](http://upgrade-agent.md/) CONFIG section before starting — project paths, persona names, memory path are all configured there.

---

## Changes Made

**docs/upgrade/**[**upgrade-agent.md**](http://upgrade-agent.md/) — NEW file created. Full agent definition: IDENTITY, CONFIG block (project name, repo paths, persona names, memory path), PIPELINE (6 phases with scope-first Phase 1 and explicit on-demand skill loading), LAWS, ALLOWED TOOLS, NEVER.

**docs/upgrade/**[**session-starter.md**](http://session-starter.md/) — Full rewrite. Now a 3-line paste prompt: `Load docs/upgrade/upgrade-agent.md` + `Scope:` placeholder + note directing owner to fill in CONFIG in [upgrade-agent.md](http://upgrade-agent.md/). All prior content (agent definition, PERSONAS, PRE-FLIGHT, FLOW, SKILL FILES, TOOLS, NEVER) removed.

**docs/upgrade/**[**roundtable.md**](http://roundtable.md/) — PERSONAS section (4 lines) replaced with 2-line pointer to [upgrade-agent.md](http://upgrade-agent.md/) CONFIG. Placeholder duplication eliminated.

**docs/**[**CONFIGURE.md**](http://configure.md/) — 4 changes: `[Master Persona 1]` and `[Master Persona 2]` file references updated from `session-starter.md, roundtable.md` → `upgrade-agent.md`; `[SPQR_REPO_PATH]` file reference updated from `session-starter.md` → `upgrade-agent.md`; new `[MEMORY_PATH]` row added before `[SPQR_REPO_PATH]` row.

[**README.md**](http://readme.md/) — 2 changes: file structure block updated ([session-starter.md](http://session-starter.md/) description changed to "paste prompt — scope + paths"; [upgrade-agent.md](http://upgrade-agent.md/) line added); How to adopt step 5 upgrade guidance rewritten to point to [upgrade-agent.md](http://upgrade-agent.md/) CONFIG as single configuration location.