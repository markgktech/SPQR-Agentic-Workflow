---
up: "[[v1.5]]"
group: "Warehouse Cutover — agent layer (SAW-31)"
order: 9/10
saw: [SAW-31]
ticket: SAW-31
status: pending
type: brief
tags: [group, warehouse, cutover, brief]
---

# Group 9 — Warehouse Cutover: agent layer (read + propose + Senate judgment + session-start wake)

## Brief
GROUP:          Warehouse Cutover — agent layer (SAW-31)
ORDER:          9/10 (SAW-31 execution session 1 of 2 — Agent A)
REPO:           SPQR (generic; A18 generic-first — Foodoire receives this via later propagation, not here)
RUN_CONTAINER:  /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:        /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/09-warehouse-cutover-agent-layer.md
RATIONALE:      One coherent surface — the agent-layer warehouse-awareness sweep; the homogeneous query-policy block MUST stay consistent across all 6 agent files (one agent = drift-prevention). 7-FILES cap owner-overridden for this single coherent surface (owner confirmed the 2-agent split 2026-06-21).
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md  (D1–D6 + D2c + clarifications; DERIVE, do not re-decide)
FILL_CHANGES_MADE: yes

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md   (the decision record — authoritative)
  - warehouse_robot/docs/QUERY_PROTOCOL.md                  (enforcement authority for the query-policy block: verbs, bracket, dials, SCRUTINIZE DENY, exit codes)
  - warehouse_robot/docs/WRITE_PROTOCOL.md                  (the proposer contract: proposal format, hard-gate, state machine, antechamber, CLI)
  - warehouse_robot/docs/NODE_FORMAT.md                     (node frontmatter — the proposal is this minus id/timestamp/schema_version)
  - warehouse_robot/docs/AUDIT_PROTOCOL.md                  (the flag plane + heat the session-start audit hook surfaces)

DEPENDENCY GATE: warehouse build B1–B5 GREEN (Phase 1 COMPLETE — v1.5.md group 8). The CLI verbs/flags this brief references (`open_scope`/`find`/`fetch`/`traverse`/`verdict`/`grant`, `propose`/`revise`/`resolve`, `audit`, `check`) must exist in `warehouse_robot/`. STOP if any referenced verb is absent.

## Scope — build exactly this (PoC D1–D6 + D2c)

THE QUERY-POLICY BLOCK (D5) — apply the SAME block to each agent file, archetype-specific only in the declared `--archetype`:
- self-declare `--archetype <X>` + `--session <id>` on every verb (G8 honour system; both mandatory non-empty);
- the intent/verdict bracket discipline: open a round with an `intent`, ONE open round per session, ALWAYS close with `verdict` (terminal: FOUND-ENOUGH/ABSENT/FOUND-UNLINKED; non-terminal: WRONG-ENTRY/INSUFFICIENT-TRAVERSE);
- budgets: **reference QUERY_PROTOCOL §3 / `policy.py` as the authority — do NOT copy dial numbers into the agent file** (single source = the robot; the block is usage instruction, the robot is the enforcer);
- ABSENT handling: an empty slice is legitimate ABSENT evidence — never auto-broaden, surface/flag it;
- BudgetExhausted → the escalation packet is surfaced to the owner → owner issues a one-shot `grant` (consumed on the next round);
- SCRUTINIZE DENY (scrutinize agents only): `supersedes`/`derived-from`/`about` denied to traverse; hidden-but-declared in fetch; `include_inactive` denied.

ARCHETYPE MAPPING (D1): deliberate=Senate (incl. Censura — D1b) · execute=Praetor · synthesize=Quaestor · scrutinize=Tribunus/Probator/Curator · consult=parked (no agent).

## FILES (9 — cap overridden, single coherent surface)
  docs/skills/warehouse-ingest.md: **NEW** — the S8 proposer contract. Proposal frontmatter (NODE_FORMAT minus the 3 robot-stamped keys id/timestamp/schema_version — never hand-mint id), canonical key order, atomic-assertion guidance, kind/scope/edge authoring (per-kind required fields + per-edge source-kind from WRITE_PROTOCOL), **MANDATORY read-before-propose** (a `find`/`open_scope` query first — S6 three-layer dup defense), the `propose`/`revise` CLI + exit codes, antechamber discipline (append-only content, sidecar state).
  docs/agents/praetor.md: query-policy block (archetype=execute) + propose right + load `warehouse-ingest.md` as a reference skill; ALLOWED TOOLS gains the warehouse query+propose CLI (Bash already present).
  docs/agents/quaestor.md: query-policy block (archetype=synthesize) + propose right + `warehouse-ingest.md` ref; ALLOWED TOOLS gains warehouse query+propose CLI.
  docs/agents/tribunus.md: query-policy block (archetype=scrutinize, SCRUTINIZE DENY) + read CLI in ALLOWED TOOLS.
  docs/agents/probator.md: query-policy block (archetype=scrutinize, DENY) + read CLI.
  docs/agents/curator.md: query-policy block (archetype=scrutinize, DENY) + read CLI.
  docs/agents/senate.md: query-policy block (archetype=deliberate; Censura queries deliberate too — D1b) + ingest-judgment (`resolve` ingested/rejected/revise + `grant`, EXECUTED by the agent ONLY on explicit owner HITL — D2) + **amend "Never run shell commands"** → permit the warehouse CLI (read+propose freely; resolve/grant only on owner HITL); keep "never write code/source" + "never modify SPQR process files". Censura LESSONS write → **lesson-node PROPOSAL** via the ingest skill (D2c).
  docs/agents/session-starters.md: add the Senate **antechamber pending-check** + **audit-heat surfacing** at session start (owner-operated); add owner-driven **warehouse-maintenance starters** (D6b: `audit` run / pending-check / flag-resolution sweep / semantic-audit "review this"); refresh the stale "SPQR v1.1" version label.
  docs/skills/censura-output.md: Censura's lesson output path changes from writing `LESSONS.md` to emitting a **lesson-node proposal** to the antechamber via `warehouse-ingest.md` (D2c). (LESSONS.md is not deleted this run — flat-doc retirement is a separate owner SAW.)

## Scope fence — do NOT do (flag if found, per Law 1)
- Do NOT remove flat-doc loading / delete flat docs (warehouse is PRIMARY but flat-doc physical retirement is a separate owner SAW; this run is additive-capability + warehouse-primary instructions).
- Do NOT copy budget dial numbers into agent files (reference QUERY_PROTOCOL/`policy.py`).
- Do NOT build the auto-ingest promotion policy (Cluster C — stays reachable-but-empty), the full semantic-audit automation, or any Foodoire content / migration (later tickets).
- Do NOT touch retro/handoff/usage-doc files — those are Group 10 (no file-ownership split).

## Changes Made

**Status:** COMPLETE — 9 files (1 NEW skill + 6 agents + session-starters + censura-output). No commit (owner commits). DEPENDENCY GATE verified GREEN before any edit.

### Dependency gate (verified, not assumed)
Confirmed every referenced CLI verb exists in `warehouse_robot/cli.py`: `init` · `check` · `reconcile` · `open-scope` · `find` · `fetch` · `traverse` · `verdict` · `grant` · `propose` · `revise` · `resolve` · `reconcile-antechamber` · `audit`. Pinned the exact surface so the agent files reference reality, not the spec's prose: verbs are **hyphenated** (`open-scope`, not `open_scope`); invocation is `python3 -m warehouse_robot <verb> --warehouse-root … [--archetype A --session S --intent "…"]`; archetypes = `deliberate/execute/synthesize/consult/scrutinize` (`policy.py`); query verdicts = `FOUND-ENOUGH/ABSENT/FOUND-UNLINKED/WRONG-ENTRY/INSUFFICIENT-TRAVERSE`; write verdicts = `ingested/rejected/revise`; `verdict`/`grant` take `--session` only (no archetype); `--tighten DIAL=N` only tightens.

### The homogeneous query-policy block (D5)
A single **byte-identical core** (SELF-DECLARE · BRACKET DISCIPLINE · BUDGETS · ABSENT HANDLING · BUDGET EXHAUSTED) pasted into all 6 agent files — verified 1 distinct variant per line (drift-prevention, the brief's RATIONALE). Archetype-specific only in the `--archetype` line; addenda gated by role:
- **SCRUTINIZE DENY** addendum present in exactly the 3 scrutinize files (Tribunus/Probator/Curator) — verified.
- **WRITE PATH (propose)** addendum in the 2 authoring agents (Praetor, Quaestor) + Senate/Censura.
- Budgets reference `QUERY_PROTOCOL §3` / `policy.py` as the authority; **zero dial numbers copied** into agent files (verified — scope fence honoured).

### Per-file
- **docs/skills/warehouse-ingest.md — NEW.** The S8 proposer contract: proposal = NODE_FORMAT minus the 3 robot-stamped keys (`id`/`timestamp`/`schema_version`, never hand-mint — A15); canonical key order; one-atomic-assertion guidance; per-kind required fields (decision→scope, constraint→source, lesson→agent+ticket) and per-edge source-kind from WRITE_PROTOCOL; **MANDATORY read-before-propose** (find/open-scope dup-check, S6 three-layer defense; contradiction → superseding node, never in-place edit); `propose`/`revise` CLI + exit codes (0/1/2); antechamber discipline (append-only content + mutable `.state.json` sidecar; proposal not live until owner `resolve … ingested`); SAW-26 receipt line.
- **docs/agents/praetor.md** — query-policy block (`--archetype execute`) + WRITE PATH; `warehouse-ingest.md` added as on-demand reference skill; ALLOWED TOOLS Bash note extended to the warehouse query+propose CLI.
- **docs/agents/quaestor.md** — query-policy block (`--archetype synthesize`) + WRITE PATH; `warehouse-ingest.md` reference; Bash expanded from echo-only to the warehouse query+propose CLI; NEVER "no state-modifying shell" carved out for the warehouse CLI (propose writes the antechamber queue only, never warehouse/source; never resolve/grant).
- **docs/agents/tribunus.md** — query-policy block (`--archetype scrutinize` + SCRUTINIZE DENY); read-only warehouse CLI added to the swiftlint-only Bash line and its NEVER; added NEVER barring the write CLI (`propose`/`revise`/`resolve`/`grant`).
- **docs/agents/probator.md** — same scrutinize block + DENY; read-only CLI added to the xcodebuild/xctest/git-diff Bash line; added NEVER barring the write CLI.
- **docs/agents/curator.md** — same scrutinize block + DENY; read-only CLI added to the build/lint Bash line; added NEVER barring the write CLI.
- **docs/agents/senate.md** — query-policy block (`--archetype deliberate`; D1b: Consilium AND Censura both deliberate, see lineage) + **INGEST JUDGMENT** block (`resolve` per-proposal never bulk + `grant`, EXECUTED by the agent ONLY on explicit owner HITL — D2); WRITE PATH (Censura proposes lessons, free). **"Never run shell commands" amended** → permit the warehouse CLI (read+propose freely; resolve/grant only on owner HITL); "never write code/source" + "never modify SPQR process files" left standing. ALLOWED TOOLS gains a warehouse-CLI-only Bash. Censura CENSURA-mode line: LESSONS.md write → **lesson-node proposal** (D2c).
- **docs/agents/session-starters.md** — version label `SPQR v1.1` → `SPQR v1.5`; added **SENATE PRE-STEP — WAREHOUSE WAKE** (owner runs `check` pending + `audit` heat, pastes into the Senate session); added **WAREHOUSE MAINTENANCE — OWNER-DRIVEN STARTERS** (D6b): audit run · antechamber pending-check · flag-resolution sweep (agent-executes-on-owner-HITL `resolves`, D3 — retro surfaces, owner authorizes) · semantic-audit "review this" (owner-driven contradiction pass → superseding proposal). The three distinct acts (audit / harvest / sweep) kept separate per the PoC clarification.
- **docs/skills/censura-output.md** — `LESSONS.md WRITE` section → **LESSON-NODE PROPOSAL** (D2c): read-before-propose dup-check, lesson frontmatter (`kind: lesson` + required `agent`+`ticket`, `verdict` matching the Censura verdict, recommended `about` edge), `propose` CLI + receipt. Note added that `docs/LESSONS.md` is not deleted this run (flat-doc retirement = separate owner SAW).

### Scope fence — honoured
- No flat-doc loading removed, no flat doc deleted (LESSONS.md retained; behaviour changed to warehouse-primary only).
- No budget dial numbers copied (verified by grep).
- Auto-ingest promotion policy (Cluster C), full semantic-audit automation, and all Foodoire/migration content left untouched.
- retro/handoff/usage-doc files (Group 10) untouched — including the D4 `ticket-comment.md` `receipt:`/`warehouse_trace:` work, which belongs to Group 10, not here.

### Out-of-scope discoveries (report only — Law 1/Law 4; owner/master decides)
1. **NEW placeholder token `[WAREHOUSE_ROOT]`** (and the optional `[ANTECHAMBER_ROOT]`, defaulted by the robot as an `antechamber` sibling — A3) is introduced into the agent/skill CLI examples, following the existing `[PROJECT_PATH]` convention. It is **not yet catalogued in `docs/CONFIGURE.md`** (out of scope — CONFIGURE.md is not one of my 9 files, and the memory note on SAW-33 already flags a CONFIGURE-token reconciliation before first propagation). **Action for the sync group / owner:** add `[WAREHOUSE_ROOT]` to the CONFIGURE.md Variable Catalogue + `spqr.config`, else the propagation agent will fail loudly on an unknown propagated token (which is the desired loud failure, but should be pre-empted).
2. **Probator's CORRECTIO-close routine-knowledge write (D8) is unreconciled with the read-only scrutinize model.** Probator is `scrutinize` (read-only, no propose right — I added the NEVER barring the write CLI), yet its existing ALLOWED-TOOLS/NEVER still say it appends routine knowledge to "the project-knowledge sink — LESSONS.md → Warehouse, D8". The brief scoped probator.md to the query block + read CLI only, and PoC **D2c names only Censura's** LESSONS→proposal — so I did **not** convert Probator's close-write. This leaves a genuine inconsistency: either Probator needs a narrow propose right for its close-lesson (like Censura), or the owner ingests it. **Recommend** the owner/master open a follow-up to settle Probator's D8 write under warehouse-primary (mirrors the Censura D2c decision).
