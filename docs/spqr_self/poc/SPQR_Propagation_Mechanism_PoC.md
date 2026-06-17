---
type: poc
title: "SPQR Propagation Mechanism"
decides: "How generic SPQR updates propagate to consuming projects (direction + mechanism) — SAW-38"
status: done         # draft | done
date: 2026-06-17
tags: [poc]
---

# SPQR Propagation Mechanism

## Context / question

**Ticket:** SAW-38 — *Propagate generic SPQR updates to consuming projects (Foodoire) — direction + mechanism.*

The generic SPQR (this repo) is the source of truth. Foodoire runs its own copy of the workflow and now lags after every generic change, with no defined "bring-current" path. Historically knowledge flowed project→generic; the owner now wants generic→project. This PoC settles **how** and **in which direction** generic updates reach consuming projects (Foodoire first, N consumers later) — repeatable and followable by a stateless execution agent.

This PoC designs the mechanism. It does not build it and does not touch any consuming project. Once settled (status → done), the v1.5 run picks it up via its `poc:` field and plans execution.

### Decision list (from Phase 2 roundtable)

- **Q1** — Boundary of the "core engine": what propagates vs. generic meta/self vs. project-owned. **(closed — see below)**
- **Q2** — Unit of propagation: full core version vs. selective changes. **(closed — see below)**
- **Q3** — How project-owned areas are protected from overwrite/deletion. **(closed — see below)**
- **Q4** — Project-side footprint/marker (real values + current generic version): one artifact or split. **(closed — see below)**
- **Q5** — Who runs it (upgrade master vs. dedicated propagation agent) + whether the generic run emits a machine-readable propagation manifest. **(closed — see below)**
- **Q6** — Fate of the legacy project→generic reverse direction (retire vs. keep bidirectional). **(closed — see below)**
- **Q7** — Scaling to N consumers (cross-cutting constraint). **(closed — see below)**

## Findings

**Three-category propagation surface (not two).** The surface narrows from both ends:
- *Source side* excludes the generic meta/self layer (the project does not run the upgrade machinery).
- *Target side* protects project-owned content (warehouse, flat docs, instantiated config values).

**Init-time vs. ongoing.** A second axis separates artifacts needed only at first instantiation (templates the project already holds) from artifacts that flow on every bring-current update. The ongoing surface is much narrower than "the whole generic repo."

## Recommendation / decision

### Q1 — Boundary of the "core engine" (CLOSED)

**Decision:** The propagation surface is defined by a two-axis classification, made machine-readable via a **declarative propagation manifest** in the generic repo.

**Axis 1 — init-time vs. ongoing:**
- **Init-only (NOT propagated on ongoing updates; consumed once at first instantiation):** `CLAUDE.md.template`, `docs/CONFIGURE.md`, `docs/LESSONS.md`, `docs/UPGRADE.md`. Foodoire already instantiated these (it has a live `CLAUDE.md` etc.), so ongoing propagation must not overwrite them.

**Axis 2 — category (ongoing surface):**
- **CORE → propagates (ongoing):** `docs/agents/` and `docs/skills/` — the live workflow the project runs. This is the real ongoing propagation surface.
- **GENERIC META/SELF → never propagates:** `docs/upgrade/` (upgrade agent + skills), `docs/spqr_self/` (generic's own run records + templates).
- **MACHINE-LEVEL, not per-project (excluded):** `.claude/rules/` (AGENT_LAWS) — its real home is the central machine-level Claude config (`~/.claude/rules/`), not the project repo. A constitution base that changes rarely; not project-specific, not copied per project.
- **PROJECT-OWNED → never overwritten (target-side):** instantiated config values, warehouse content/data, flat documentation in the consuming project.

**Hard constraint (non-destructive):** propagation never deletes files it does not own. Extra files present in the project (e.g. additional files under `docs/`) that are not in the manifest stay intact. Propagation adds/updates the core surface; it does not prune.

**Mechanism (agreed):** the boundary is not inferred by the agent — a **declarative propagation manifest** in the generic repo tags each path (`propagate` / `generic-only` / `init-only` / `project-owned`). Single source, versioned, readable by any stateless agent.

**Rationale:** the ongoing surface is essentially the live agents and skills; init-time templates and the machine-level constitution are out of the ongoing path because the project already holds instantiated copies. A declarative manifest keeps the boundary explicit rather than guessed. **#decision**

**Deferred sub-item — `warehouse_robot/` (DESCOPED, owner decision):** out of scope for SAW-38. The warehouse is still in progress; at first instantiation the robot is pulled in, and thereafter it updates only when the robot itself needs a fix. How warehouse-robot propagation works is decided at the warehouse stage, not here. Flagged only; no ticket created.

---

### Q2 — Unit of propagation (CLOSED)

**Decision:** The unit is a **full core-version snapshot** — at propagation time the entire manifest-defined core surface is brought to a known target generic version, atomically. Not selective/cherry-pick.

**Manifest vs. snapshot (two distinct things):**
- The **manifest** (Q1) is the *definition* — the single source of truth for which paths are core.
- The **snapshot** (Q2) is the *unit* — "take the manifest's core surface, set it to the target generic version." The snapshot follows the manifest; there is no second place to maintain.

**Directory-level manifest rules:** the manifest tags by directory (e.g. everything under `docs/agents/` and `docs/skills/` propagates). Consequence: a new agent/skill file flows automatically with no manifest edit; the manifest is touched only on a *structural* change (a new top-level area, or reclassifying one).

**Extensibility (owner constraint):** propagation will expand later (the warehouse is the likely next area). The mechanism must allow adding a new propagating area as a new manifest line, without redesign. Directory-level manifest rules satisfy this. The warehouse itself stays out of scope here (see Q1 deferred sub-item).

**Rejected:** stepwise version-range application (v1.3→v1.4→v1.5 applied one at a time). With a markdown=truth core there is no migration-chain constraint (unlike a DB schema); jumping directly to the target version is deterministic.

**Rationale:** the narrow core surface (Q1) plus a single version number is atomic and auditable, and directly serves the Q4 version marker. Selective propagation reintroduces drift — the project state stops being a single number. **#decision**

---

### Q3 — Protection of project-owned areas (CLOSED)

**Decision:** Protection is structural, plus a safety net and an explicit deletion boundary.

**Protection by omission (primary):** the propagation agent writes *only* to the manifest `propagate` surface. Everything else — warehouse, flat docs, instantiated config values — is not on the surface, so it is never touched. Protection is not an enumerated "do not touch" list; the agent simply only knows the core surface.

**Core is generic-owned (no in-place project edits):** the core surface is generic-owned by definition. A project that needs different behavior puts it in a **project-owned extension area outside the core surface** (already excluded by the manifest), never by editing a core file. Keeps the snapshot clean and protection structural.

**Safety net (no silent overwrite):** if propagation detects a core file was locally modified (differs from the expected generic content), it **flags to the owner** rather than silently overwriting. Surfaces accidental local edits.

**Deletion boundary:** within the `propagate` surface, propagation mirrors generic — including deletions (a core file removed in generic is removed in the project, for snapshot integrity). Outside the surface, propagation never deletes. The owner's "project's extra files must not disappear" constraint holds because those files live outside the surface.

**Rationale:** structural protection (only-touch-the-surface) is the most stateless-agent-actionable model and directly satisfies the owner's warehouse/flat-docs concern. The safety net catches the one case structure cannot — accidental in-core edits. **#decision**

---

### Q4 — Project-side footprint (CLOSED)

**Finding (evidence):** core files *do* contain per-project placeholders, so the footprint cannot be version-only. Two kinds, which must be separated:
- **Runtime placeholders — left literal (not config):** `[AGENT]`, `[TICKET_URL]`, `[FILE]`. Filled per-session at runtime; propagation leaves them untouched.
- **Per-project config placeholders — re-instantiated on propagation:** `[PROJECT_PATH]`, `[PROJECT_BOUNDARIES]`, and the Notion template IDs (`[SPIKE_TEMPLATE_ID]`, `[FEATURE_TEMPLATE_ID]`, `[BUG_TEMPLATE_ID]`, `[DOC_TEMPLATE_ID]`, `[SPIKE_DOCUMENT_TEMPLATE_ID]`, `[SPIKE_DOC_PARENT_PAGE_ID]`).

**Decision:** **one artifact** — a dedicated, machine-readable project config (e.g. `spqr.config.yml`) in the consuming project, holding:
- (a) the config-token → real-value map (used to re-instantiate placeholders when propagation brings a new/changed core file), and
- (b) the current generic **version stamp**.

The token→value map doubles as the authoritative list of which tokens are project-config; any token not in it (e.g. the runtime ones) is left alone.

**Not a prose doc:** it is config, not an md document. Dedicated machine-readable file rather than embedding in `CLAUDE.md` prose, because the propagation agent must read the token→value pairs deterministically.

**Rationale:** core genuinely carries per-project placeholders, so re-instantiation values must live somewhere machine-readable; co-locating them with the version stamp gives the project a single footprint. **#decision**

### Q5 — Who runs it + manifest (CLOSED)

**Decision:** a **new, dedicated propagation agent**, part of the upgrade machinery (lives in `docs/upgrade/`, alongside the master). The owner runs it to bring a consuming project current.

- **Generic-driven, generic-resident:** the agent definition + the manifest + the source core all live in the generic repo. Being upgrade-meta, the propagation agent **does not propagate itself** to the project (consistent with Q1 — the machinery stays generic). The project never receives this agent.
- **Writes into the project:** unlike the master (which never touches a project), this agent's whole job is to write the generic core surface into the consuming project repo, taking that project's path/config as input. This is why it is a separate agent.
- **No per-run manifest:** only the standing path-classification manifest (Q1) + the target version drive it; the diff (project's current core vs. target generic core) is computed at run time. *Position update (Law 4):* the roundtable's earlier per-run machine-readable manifest suggestion (F6) is withdrawn — the snapshot model makes it unnecessary.

**Rationale:** the master's NEVER list forbids touching projects; propagation by definition touches a project, so it must be a distinct agent. Keeping it generic-resident and non-self-propagating preserves the three-category boundary. **#decision**

### Q6 — Reverse direction (CLOSED)

**Decision:** the automatic project→generic content sync is **retired**. Content flows one way only: generic→project. Project insight travels upward only as a **signal** (a SAW ticket), never as an automatic content sync.

The loop:
1. A problem/insight with SPQR surfaces while working in the project → **raise a SAW ticket** (the only thing that goes up).
2. The owner picks up the ticket → PoC → implements it **in the generic** → releases a new generic **version**.
3. Propagation then pulls that version **down** into the project (forward direction).

**Rationale:** a single source of truth with one automatic content direction avoids two competing auto-syncs (roundtable F1). The deliberate upgrade pipeline *is* the upward path; it carries insight, not content. **#decision**

### Q7 — Scaling to N consumers (CLOSED)

**Decision:** the design already scales without redesign. The manifest is generic-side and shared; each consumer carries its own `spqr.config` (its values + its version stamp, Q4); the propagation agent runs per project, reading that project's config. Nothing is Foodoire-specific.

- N consumers = the same agent run in each, each with its own config.
- A consumer registry (to track who is on which version) is an optional future addition, not required to operate. Deferred — only one consumer for the foreseeable future.

**Rationale:** per-project config + shared manifest + per-project agent run is inherently N-safe; no per-consumer special-casing exists. **#decision**

## Roundtable amendments (2026-06-17)

Independent from-scratch review by two reviewers (Dev Process Architect + Agentic Trends Expert), framed to critique the solution space rather than validate the plan. Directional decisions (Q1 categories, Q2 reject-stepwise, Q6, Q7 shape) confirmed sound. The following amendments take precedence over the original text where they conflict.

**AM1 — Q3/Q4 contradiction fixed (first-run breaker).** Config tokens live *inline* inside core files (e.g. `[PROJECT_PATH]` in `session-starters.md`/`ticket-slicing.md`), so every snapshot *must* rewrite core files in place to re-instantiate them. This **supersedes** Q3's "core is generic-owned, no in-place project edits" wording: propagation overwrites the core surface, then re-instantiates placeholders in place from `spqr.config`. The Q3 drift safety-net must compare the project file against the generic file **with this project's tokens re-applied** (token-normalized), otherwise every freshly-instantiated file false-positives on every run. Flagged-divergence resolution is **recorded durably** (run-log / owner decision) so a re-run does not re-prompt (Law 3).

**AM2 — Q1 surface gaps.** (a) `docs/retro/` is live workflow with project tokens but was unclassified — it joins **CORE (propagates)**. (b) `.claude/rules` (AGENT_LAWS) exclusion assumes a shared machine; for a fresh clone / CI / N consumers the constitution is simply absent. Its distribution is therefore an **explicit out-of-band step** (named in the mechanism), not an unstated assumption.

**AM3 — Q4 single source of tokens.** `docs/CONFIGURE.md` is already the authoritative token catalogue. `spqr.config` is **derived from CONFIGURE.md**, not a second hand-authored list (the original Q4 list was already incomplete — it omitted the Senate persona tokens `[Name 1–4]` and the retro tokens). Propagation **fails loudly** if a propagated file contains a token absent from `spqr.config`. A `spqr.config` schema/shape is defined so the agent reads it deterministically.

**AM4 — Q5 stays agent-driven (owner decision; determinism rejected for now).** The reviewers recommended making copy/delete/merge deterministic (git-backed). **Owner rejected** building code at this stage. The mechanism remains agent-executed; safety is **procedural**, not git-based: clean-tree precondition → dry-run preview (agent proposes add/update/delete + re-instantiation + flags) → owner confirmation (resolution recorded) → write → atomic version stamp only after all files written and all flags resolved → owner commits (one commit/run) → rollback = revert. A **generated** run-log records what each run changed (restores the auditability the "no per-run manifest" choice had removed — generated, not hand-authored). *Accepted trade-off: outsourcing this to deterministic code later is a candidate SAW ticket.*

**AM5 — Operational additions.** Clean working-tree precondition; one commit per run; rollback via revert; dry-run/preview mode; read-only **status mode** ("is the project current?") without running a full propagation; version stamp written only at the atomic commit point.

**AM6 — Init/setup artifacts.** The generic ships an **empty `spqr.config.template`** (init-only) that a new project copies and fills at first instantiation. Establishing the marker is a one-time setup step. **Baseline:** Foodoire is currently on **v1.3** (generic is at v1.5); the first execution must create Foodoire's `spqr.config` stamped at v1.3 before any propagation.

## References

- SAW-38 (Notion) — the ticket this PoC settles
- Knowledge Architecture & Token Optimization PoC (poc lane) — adjacent precedent
- SPQR AGENT_LAWS — Law 3 (external record is truth), Law 4 (independence)

## Process finding (out of SAW-38 scope — owner to ticket)

Surfaced while recording Q1: the upgrade pipeline assumes a version container is created once, from scratch, for a single run; it has no model for new scope entering an already-open version (SAW-38 into v1.5). Combined with `decision-making.md` pointing decisions at a MAIN folder-note that v1.5 lacks (legacy shape), and the only on-disk example being the stale Warehouse-era format, this caused a wrong first attempt (standalone decision file in legacy format). Candidate fixes: `planning.md` rule for "scope into existing version"; `decision-making.md` forbidding a free-standing decisions file; `group_submd_template.md` lacks a `## Decisions` section; general "templates/ wins over a possibly-stale sibling example." Flagged for a separate SAW ticket.
