---
up: "[[v1.5]]"
group: "Generic-side propagation mechanism"
order: 1/1
tags: [group]
---

# Group 1 — Generic-side propagation mechanism

## Brief

GROUP: Generic-side propagation mechanism
ORDER: 1/1
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/01-propagation-mechanism.md
RATIONALE: one cohesive generic-side markdown set defining the propagation mechanism; no shared-file conflicts, no code (AM4)
FILL_CHANGES_MADE: yes
PRE_FLIGHT:
  docs/spqr_self/poc/SPQR_Propagation_Mechanism_PoC.md   (the design — Q1–Q7 + AM1–AM6; authoritative for CONTENT)
  docs/upgrade/execution.md
  docs/CONFIGURE.md   (the token catalogue spqr.config is derived from)
  docs/agents/ , docs/skills/ , docs/retro/   (enumerate the CORE surface and its inline tokens)
  docs/upgrade/upgrade-agent.md   (FORM exemplar for the new agent definition — mirror its structure)
  CLAUDE.md.template + docs/spqr_self/templates/   (FORM exemplar for spqr.config.template)
CONVENTIONS (mandatory — match existing form, do not invent a new shape):
  - propagation-agent.md → mirror the structure of docs/upgrade/upgrade-agent.md (IDENTITY / CONFIG / PIPELINE / LAWS / ALLOWED TOOLS / NEVER).
  - spqr.config.template → mirror CLAUDE.md.template + the templates/ style (frontmatter, empty placeholder shape).
  - propagation-manifest.md → no exact analog; keep it declarative and simple, following the nearest existing exemplar's form.
  - Standing rule: templates/ and existing files are the convention of record — mirror them. If an on-disk example conflicts with templates/, templates/ wins.
  - The PoC is authoritative for CONTENT; the exemplars above are authoritative for FORM. Do not let form drift change the decided content (Q1–Q7 + AM1–AM6).
FILES:
  docs/upgrade/propagation-manifest.md: declarative, directory-level path classification — propagate (docs/agents, docs/skills, docs/retro) / generic-only (docs/upgrade, docs/spqr_self) / init-only (CLAUDE.md.template, CONFIGURE.md, LESSONS.md, UPGRADE.md, spqr.config.template) / project-owned (warehouse, flat docs, config values). Note .claude/rules as out-of-band (AM2). warehouse_robot deferred.
  docs/upgrade/propagation-agent.md: the new propagation agent definition — generic-resident, writes into a consuming project, does not self-propagate. Procedure: read project spqr.config (current + target version) → dry-run preview (add/update/delete within surface + placeholder re-instantiation from spqr.config + flag locally-modified core files, compared token-normalized) → owner confirmation (resolution recorded durably) → write on clean working tree → atomic version stamp only after all files written and all flags resolved → generated run-log → owner commits (one commit/run, rollback = revert). Include a read-only status mode. Fail loudly on a token absent from spqr.config.
  spqr.config.template: empty, init-only template at the generic root — the per-project footprint shape (config-token→value map derived from CONFIGURE.md + version stamp field). New project copies and fills it at first instantiation.
  docs/UPGRADE.md: add a pointer to the propagation flow (generic→project) and the propagation agent.
  docs/CONFIGURE.md: add one line noting it is the authoritative token source from which spqr.config is derived.

OUT OF SCOPE (do not do): touching any consuming project; creating Foodoire's spqr.config or its v1.3 baseline (that is a later owner-run activity using this agent); building any executable/deterministic code (AM4 — markdown definitions only).

## Changes Made

Five generic-side artifacts created/edited. Content from the PoC (Q1–Q7 + AM1–AM6); form mirrors the named exemplars. No consuming project touched; no code (AM4 — markdown only); not committed.

**Created**

- `docs/upgrade/propagation-manifest.md` — declarative, directory-level path classification. Four categories: `propagate` (CORE: `docs/agents/`, `docs/skills/`, `docs/retro/`) / `generic-only` (`docs/upgrade/`, `docs/spqr_self/`) / `init-only` (`CLAUDE.md.template`, `docs/CONFIGURE.md`, `docs/LESSONS.md`, `docs/UPGRADE.md`, `spqr.config.template`) / `project-owned` (warehouse, flat docs, instantiated config values). `.claude/rules` noted OUT-OF-BAND (AM2); `warehouse_robot/` DEFERRED. States the non-destructive rule, directory-level (not file-level) rule, and full-snapshot unit (Q1/Q2/Q3). Form: no exact analog — kept declarative/simple per the convention.

- `docs/upgrade/propagation-agent.md` — new propagation agent definition, mirroring `docs/upgrade/upgrade-agent.md` structure (IDENTITY / CONFIG / PRECONDITIONS / PIPELINE / STATUS MODE / LAWS / ALLOWED TOOLS / NEVER). Generic-resident, writes into a consuming project, does not self-propagate (Q5). 9-step pipeline: read project `spqr.config` (current + target version) → run-time diff (add/update/delete within surface) → token re-instantiation + token-normalized drift check, fail loudly on a token absent from `spqr.config` (AM1/AM3) → dry-run preview → owner confirmation recorded durably (AM1/Law 3) → write on clean tree → atomic version stamp only after all files written + flags resolved → generated run-log (AM4) → owner commits (one/run, rollback = revert, AM5). Read-only status mode included (AM5).

- `spqr.config.template` — empty, init-only template at the generic root. Mirrors `CLAUDE.md.template` framing (fenced header + fill instructions) with a machine-readable token→value map. Tokens derived from `docs/CONFIGURE.md` (AM3): `version` stamp field + personas (`Name 1`–`Name 4`) + `PROJECT_PATH` + `PROJECT_BOUNDARIES` + Notion IDs (`SPIKE_/FEATURE_/BUG_/DOC_TEMPLATE_ID`, `SPIKE_DOCUMENT_TEMPLATE_ID`, `SPIKE_DOC_PARENT_PAGE_ID`) + retro IDs (`RETRO_PARENT_ID`, `RETRO_TEMPLATE_ID`, `RETRO_SESSION_STARTER_ID`). Runtime placeholders (`[AGENT]`, `[TICKET_URL]`, `[FILE]`, `[ID]`) explicitly excluded as non-config (Q4). Token set verified against an actual grep of the propagated surface (`docs/agents`, `docs/skills`, `docs/retro`); the generic-only upgrade-agent tokens (`[SPQR_REPO_PATH]`, `[Master Persona 1/2]`) correctly do not appear and are excluded.

**Edited**

- `docs/UPGRADE.md` — added a "Propagating a release to a consuming project" section pointing to the propagation flow (generic→project), the propagation agent, the manifest, and per-project `spqr.config` from `spqr.config.template`; notes upward travel is a SAW ticket only (Q6).

- `docs/CONFIGURE.md` — added one line noting it is the authoritative token source from which `spqr.config` is derived, and that the propagation agent fails loudly on any propagated token absent from it (AM3).

**Verification**
- Token catalogue cross-checked: every per-project token in the propagated surface has a key in `spqr.config.template`; runtime literals excluded.
- Out of scope respected: no consuming project touched; Foodoire `spqr.config` / v1.3 baseline NOT created (later owner-run activity, AM6); no executable code; MAIN folder-note (`v1.5.md`) and sibling sub-docs untouched; not committed.

**Notes for master**
- Traceability comment on SAW-38 (execution.md TRACEABILITY) not posted by this agent — no SAW-38 page ID in the brief and posting to Notion is an outward action outside the listed FILES; flagged for the master to post the run-container backlink + completion comment.
- Out-of-scope discovery: none beyond what the PoC already flagged (its own "Process finding" re: scope entering an already-open version, already owner-flagged for a separate SAW ticket).
